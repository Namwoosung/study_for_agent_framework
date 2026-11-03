"""Web transport and observation shared by the two independent runtimes."""
import contextlib
import importlib
import json
import os
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
DATA = {
    "A17": {"tested": 1000, "failed": 42, "previous_rates": [0.029, 0.033, 0.038]},
    "B04": {"tested": 800, "failed": 12, "previous_rates": [0.011, 0.014, 0.013]},
}


def bin_metrics(bin_id: str) -> dict:
    """Read a synthetic semiconductor inspection snapshot."""
    row = DATA[bin_id.upper()]
    return {"bin_id": bin_id.upper(), "snapshot": "FAB-DEMO-r3", **row,
            "defect_rate": row["failed"] / row["tested"]}


def snapshot(value):
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "__dataclass_fields__"):
        return {key: getattr(value, key) for key in value.__dataclass_fields__ if not key.startswith("_")}
    if hasattr(value, "__fspath__"):
        return os.fspath(value)
    return str(value)


class Run:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.events = []
        self.lock = threading.Lock()
        self.done = False
        self.approval = None

    def emit(self, category, title, value=None, **metadata):
        # Copy immediately. Framework messages can be mutated on the next iteration.
        payload = json.loads(json.dumps(value, default=snapshot, ensure_ascii=False))
        with self.lock:
            self.events.append(dict(n=len(self.events)+1, category=category, title=title,
                                    value=payload, time=time.time(), thread=threading.current_thread().name,
                                    **metadata))

    def ask(self, details):
        signal = threading.Event()
        with self.lock:
            if self.approval:
                raise RuntimeError("An approval is already pending")
            request = self.approval = {"id": uuid.uuid4().hex, "signal": signal, "allow": False}
        self.emit("approval", "사람의 결정 대기", {"id": request["id"], "details": details})
        signal.wait(90)
        with self.lock:
            self.approval = None
        self.emit("approval", "승인 결정", {"approved": request["allow"], "expired": not signal.is_set()})
        return request["allow"]

    def decide(self, ident, allow):
        with self.lock:
            req = self.approval
            if not req or req["id"] != ident or req["signal"].is_set():
                return False
            req["allow"] = allow
            req["signal"].set()
            return True


@contextlib.contextmanager
def observe_http(run, endpoint):
    """Observe serialized HTTP request bodies at the SDK's transport boundary."""
    target = urlsplit(endpoint)

    def capture(client, request):
        url = request.url
        if url.host != target.hostname or url.port != target.port:
            return False
        if request.method == "POST" and url.path.endswith("/chat/completions"):
            try:
                body = json.loads(request.content)
            except Exception:
                return False
            # Headers are intentionally excluded. Do not export hidden reasoning.
            metadata = {"request_id": uuid.uuid4().hex[:12], "scope": str(id(client))}
            run.emit("context", f"모델 전송 직전 · {url.path}", body, **metadata)
            if "tools" in body:
                run.emit("tool", "모델에 전달된 Tool 명세", body["tools"], **metadata)
            return metadata
        return False

    def capture_result(response, metadata):
        if response.is_stream_consumed:
            try:
                value = response.json()
            except ValueError:
                return
            if isinstance(value, dict):
                for choice in value.get("choices", []):
                    msg = choice.get("message", {})
                    for key in ("reasoning", "reasoning_content"):
                        msg.pop(key, None)
                    if msg.get("tool_calls"):
                        run.emit("tool", "모델이 반환한 Tool Call", msg["tool_calls"], **metadata)
            run.emit("response", f"모델 HTTP {response.status_code}", value, **metadata)

    def wrap(send, asynchronous=False):
        if asynchronous:
            async def async_send(client, request, **kwargs):
                relevant = capture(client, request)
                response = await send(client, request, **kwargs)
                if relevant:
                    capture_result(response, relevant)
                return response
            return async_send

        def sync_send(client, request, **kwargs):
            relevant = capture(client, request)
            response = send(client, request, **kwargs)
            if relevant:
                capture_result(response, relevant)
            return response
        return sync_send

    with contextlib.ExitStack() as stack:
        seen = set()
        for library in ("httpx", "httpx2"):
            try:
                module = importlib.import_module(library)
            except ImportError:
                continue
            for cls, asynchronous in ((module.Client, False), (module.AsyncClient, True)):
                if cls in seen:
                    continue
                seen.add(cls)
                send = cls.send
                stack.callback(setattr, cls, "send", send)
                cls.send = wrap(send, asynchronous)
        yield


@contextlib.contextmanager
def observe_functions(run, select):
    """Record real Python calls and returns, including worker threads."""
    original, thread_original = sys.getprofile(), threading.getprofile()

    def profile(frame, event, value):
        if event not in ("call", "return"):
            return
        module = frame.f_globals.get("__name__", "")
        name = frame.f_code.co_name
        category = select(module, name)
        if not category:
            return
        fields = {key: frame.f_locals[key] for key in (
            "query", "role_filter", "limit", "tool_name", "function_args",
            "pattern_key", "description", "command", "rule_key", "tool_call",
            "action", "skill_name", "name", "tasks", "goal", "provider", "api_call_count", "args",
        ) if key in frame.f_locals}
        if event == "return" and category in {"search", "approval", "skill", "delegation", "tool"}:
            if isinstance(value, (dict, list, str, int, bool, type(None))):
                fields["return"] = value
        try:
            run.emit(category, f"{module}.{name} · {event}", fields)
        except (TypeError, ValueError):
            run.emit(category, f"{module}.{name} · {event}", {"note": "값을 JSON으로 표현할 수 없습니다."})

    sys.setprofile(profile)
    threading.setprofile(profile)
    try:
        yield
    finally:
        sys.setprofile(original)
        threading.setprofile(thread_original)


def serve(engine, scenarios, execute, port, endpoint):
    runs = {}
    gate = threading.Lock()

    def work(run, scenario, prompt, session):
        try:
            execute(run, scenario, prompt, session)
        except Exception as exc:
            run.emit("error", type(exc).__name__, str(exc))
        finally:
            run.done = True
            gate.release()

    class Handler(BaseHTTPRequestHandler):
        def send(self, status, data, kind="application/json; charset=utf-8"):
            body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            return self.headers.get("Host") in {f"127.0.0.1:{port}", f"localhost:{port}"}

        def do_GET(self):
            if not self.valid_host():
                return self.send(403, {"error": "Local access only"})
            path = urlsplit(self.path).path
            if path in ("/", "/app.js", "/style.css"):
                file, mime = {
                    "/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                    "/style.css": ("style.css", "text/css"),
                }[path]
                return self.send(200, (ROOT / "web" / file).read_bytes(), mime+"; charset=utf-8")
            if path == "/api/config":
                return self.send(200, {"engine": engine, "scenarios": scenarios, "modelEndpoint": endpoint})
            if path.startswith("/api/runs/") and (run := runs.get(path.rsplit("/", 1)[-1])):
                with run.lock:
                    data = {"events": list(run.events), "done": run.done}
                return self.send(200, data)
            self.send(404, {"error": "Not found"})

        def do_POST(self):
            origin = self.headers.get("Origin")
            allowed = {f"http://127.0.0.1:{port}", f"http://localhost:{port}"}
            if not self.valid_host() or (origin and origin not in allowed) or self.headers.get("X-Demo") != "1":
                return self.send(403, {"error": "Local demo request required"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16384:
                    raise ValueError
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError
            except (ValueError, UnicodeError):
                return self.send(400, {"error": "Invalid JSON"})
            if self.path == "/api/runs":
                scenario = data.get("scenario")
                if not isinstance(scenario, str) or scenario not in scenarios:
                    return self.send(400, {"error": "Unknown scenario"})
                prompt, session = data.get("prompt"), data.get("session", "seminar")
                if not isinstance(prompt, str) or not isinstance(session, str) or len(prompt) > 6000 or len(session) > 80:
                    return self.send(400, {"error": "Invalid prompt or session"})
                if not gate.acquire(blocking=False):
                    return self.send(409, {"error": "현재 실행이 끝나거나 승인에 답한 뒤 시작하세요."})
                run = Run()
                runs[run.id] = run
                while len(runs) > 20:
                    del runs[next(iter(runs))]
                threading.Thread(target=work, args=(run, scenario, prompt, session),
                                 name=f"{engine}-run", daemon=True).start()
                return self.send(202, {"id": run.id})
            if self.path.startswith("/api/approve/"):
                run = runs.get(self.path.rsplit("/", 1)[-1])
                if run and run.decide(data.get("id"), data.get("allow") is True):
                    return self.send(200, {"ok": True})
                return self.send(409, {"error": "Approval no longer pending"})
            self.send(404, {"error": "Not found"})

    print(f"{engine}: http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
