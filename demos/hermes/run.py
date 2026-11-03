"""Embed Hermes v0.22.5 and expose its real execution to the seminar UI."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common import ROOT, bin_metrics, observe_functions, observe_http, serve

ENDPOINT = f'http://{os.environ.get("DEMO_HERMES_MODEL_HOST", "127.0.0.1")}:10000/v1'
SOURCE = HERE / ".runtime" / "source" / "hermes-agent-0.22.5"
HOME = ROOT / ".local" / "hermes-home"
WORKSPACE = HOME / "workspace"
SCENARIOS = {
    "loop": ["함수 실행 루프", "A17 불량률과 추세를 조회하고, 다음 검사에서 확인할 가설을 제시해 줘.", ["loop", "tool", "context", "response"]],
    "context": ["전송 직전 Context", "A17을 조회한 뒤 결과에 근거해 최근 추세를 설명해 줘.", ["context", "loop", "response"]],
    "search": ["세션 검색", "session_search에 FABVACUUM을 검색어로 넣어 과거 A17 진공 경보를 찾고 현재 불량률과 연결해 줘.", ["search", "tool", "context"]],
    "tools": ["Tool 스키마와 Hook", "read_fab_bin으로 b04를 소문자 그대로 먼저 요청한 다음 A17을 조회해서 비교해 줘.", ["tool", "hook", "context", "response"]],
    "approval": ["사용자 승인", "A17을 조회한 뒤 publish_fab_report 도구로 합성 보고서 r3 발행을 요청해 줘.", ["hook", "approval", "tool", "context"]],
    "guard": ["가드레일과 거절", "read_fab_bin에 UNKNOWN을 넣어 조회하고 inspect_terminal_guard도 호출해 두 차단 결과를 비교해 줘.", ["hook", "approval", "tool", "context"]],
    "skill": ["Skill 생성", "skill_manage의 create로 fab-bin-review-demo 스킬을 만들어 줘. 검사 수량과 불량 수량을 조회하고 분모를 검증하는 절차를 담아 줘.", ["skill", "tool", "hook", "context"]],
    "delegate": ["Subagent 위임", "A17 불량률을 조회하고 delegate_task의 tasks에 두 항목을 넣어 통계 검토와 공정 가설 검토를 각각 위임한 뒤 합쳐 줘.", ["delegation", "loop", "tool", "context"]],
}

SYSTEM = """합성 반도체 BIN 분석 실습이다. 실제 제조 데이터와 외부 발행은 금지한다.
수치는 read_fab_bin으로 조회하고 불량률은 failed/tested로 계산한다.
예측은 가설로 표시한다. 승인 거부·권한 거부 뒤 같은 작업을 다시 시도하지 않는다."""


def select(module, name):
    if module.startswith(("hermes_state_search", "tools.session_search_tool")) and (
        "search" in name or name in {"_normalize_query", "_sanitize_fts_query"}
    ):
        return "search"
    if module.startswith("tools.approval") and name in {
        "request_tool_approval", "_run_approval_gate", "_human_decision", "prompt_dangerous_approval",
        "detect_dangerous_command", "check_dangerous_command", "_floor_block", "_presence",
    }:
        return "approval"
    if module.startswith(("tools.skill_manager", "agent.skill")) and any(
        k in name for k in ("create", "validate", "write", "manage")
    ):
        return "skill"
    if module.startswith(("tools.delegate_tool", "agent.delegation_runtime")) and any(
        k in name for k in ("delegate", "child", "spawn", "task")
    ):
        return "delegation"
    if module.startswith(("agent.tool_executor", "model_tools", "tools.registry")) and name in {
        "execute_tool_calls", "_prepare_tool_call", "dispatch", "handle_function_call",
        "_pre_tool_block", "_parse_tool_call", "_parse_tool_arguments",
        "_commit_tool_result", "_blocked_tool_result", "get_tool_definitions",
    }:
        return "tool"
    if module.startswith(("agent.conversation_loop", "agent.turn_", "agent.turn_api",
                          "agent.turn_facade", "agent.chat_completion")) and name in {
        "run_conversation", "begin_iteration", "prepare_iteration", "assemble_api_request",
        "run_preflight_gate", "_run_api_retry_loop", "perform_api_call", "build_api_request",
        "normalize_model_response", "validate_tool_calls", "run_tool_round", "finish_text_response",
    }:
        return "loop"
    return None


def execute(run, scenario, prompt, session):
    from run_agent import AIAgent
    from hermes_state import SessionDB
    from tools.registry import registry
    from hermes_cli.plugins import get_plugin_manager
    from tools.approval_context import set_hermes_interactive_context, reset_hermes_interactive_context
    from tools.terminal_tool import set_approval_callback
    approved = set()

    def read(args, **kwargs):
        value = bin_metrics(args["bin_id"])
        run.emit("tool", "업무 Tool의 실제 반환", value)
        return json.dumps(value, ensure_ascii=False)

    def publish(args, **kwargs):
        key = (str(args["bin_id"]).upper(), args["report_version"])
        if key not in approved:
            return json.dumps({"error": "No human approval for this BIN and report version"})
        approved.remove(key)
        value = {"report_version": args["report_version"], "bin_id": args["bin_id"], "status": "recorded"}
        run.emit("tool", "승인 후 로컬 모의 발행 기록", value)
        return json.dumps(value, ensure_ascii=False)

    def register(name, description, properties, handler):
        registry.register(name=name, toolset="fab_demo",
                          schema={"name": name, "description": description,
                                  "parameters": {"type": "object", "properties": properties,
                                                 "required": list(properties), "additionalProperties": False}},
                          handler=handler, override=True)

    register("read_fab_bin", "Read inspection counts and historical rates for a synthetic BIN.",
             {"bin_id": {"type": "string"}}, read)
    register("publish_fab_report", "Record a synthetic report publication locally after human approval.",
             {"bin_id": {"type": "string"}, "report_version": {"type": "string"}}, publish)
    if scenario == "guard":
        from tools.approval import check_dangerous_command

        def inspect_guard(args, **kwargs):
            command = "rm -rf /"
            decision = check_dangerous_command(command, env_type="local")
            run.emit("approval", "Hermes 명령 가드 판정", {"command": command, "decision": decision})
            return json.dumps(decision, ensure_ascii=False)

        registry.register(name="inspect_terminal_guard", toolset="fab_guard",
                          schema={"name": "inspect_terminal_guard",
                                  "description": "Inspect Hermes guard decision for a fixed command. Executes no shell.",
                                  "parameters": {"type": "object", "properties": {}, "additionalProperties": False}},
                          handler=inspect_guard, override=True)

    def guard(tool_name, args, **ids):
        if tool_name == "delegate_task" and args.get("background") is True:
            decision = {"action": "modify", "args": {"background": False}}
            run.emit("hook", "위임 결과를 현재 실행에서 기다리도록 설정", decision)
            return decision
        if tool_name not in {"read_fab_bin", "publish_fab_report"}:
            return None
        requested = args.get("bin_id")
        decision = None
        if not isinstance(requested, str) or requested.upper() not in {"A17", "B04"}:
            decision = {"action": "block", "message": "합성 fixture에는 A17과 B04만 있습니다."}
        elif tool_name == "publish_fab_report":
            if scenario != "approval" or args.get("report_version") != "r3":
                decision = {"action": "block", "message": "승인 데모의 보고서 r3만 기록할 수 있습니다."}
            else:
                decision = {"action": "approve", "message": f"{requested.upper()} / 보고서 r3 모의 발행",
                            "rule_key": f"fab-demo:{run.id}:{requested.upper()}:r3"}
        elif requested != requested.upper():
            decision = {"action": "modify", "args": {"bin_id": requested.upper()}}
        run.emit("hook", "실제 pre_tool_call에서 반환한 정책", {"tool": tool_name, "input": args,
                 "directive": decision, "call_id": ids.get("tool_call_id")})
        return decision

    def ask(command, description, **kwargs):
        allowed = run.ask({"command": command, "description": description})
        if allowed and scenario == "approval" and command.startswith("<publish_fab_report>"):
            approved.add((description.split(" / ", 1)[0], "r3"))
        return "once" if allowed else "deny"

    def after_model(**data):
        message = data["assistant_message"]
        calls = [{"id": call.id, "name": call.function.name, "arguments": call.function.arguments}
                 for call in (getattr(message, "tool_calls", None) or [])]
        run.emit("response", "Hermes가 수신한 모델 응답",
                 {"finish_reason": data["finish_reason"], "content": message.content, "tool_calls": calls,
                  "session": data["session_id"], "round": data["api_call_count"]})
        if calls:
            run.emit("tool", "모델 응답의 Tool Call", calls)

    def tool_complete(call_id, name, args, result):
        run.emit("tool", "Hermes Tool 실행 완료", {"id": call_id, "name": name, "args": args, "result": result})

    tools = ["fab_demo"]
    if scenario == "guard":
        tools.append("fab_guard")
    if scenario == "search":
        tools.append("session_search")
    if scenario == "skill":
        tools.append("skills")
    if scenario == "delegate":
        tools.append("delegation")
    model = os.environ.get("DEMO_HERMES_MODEL", "seminar-model")
    db = SessionDB(db_path=HOME / "state.db")
    fixture = "fab-demo-a17-vacuum-r3"
    if not db.get_session(fixture):
        db.create_session(fixture, "cli", model=model)
        db.append_message(fixture, "user", "A17 진공 경보 이력과 불량률을 점검해 줘.")
        db.append_message(fixture, "assistant", "FABVACUUM 합성 점검 기록: A17 진공 경보 VAC-17이 검사 구간 T-2에 3회 발생했다. 원인 확정에는 압력 로그와 대조가 필요하다.")
        db.end_session(fixture, "agent_close")

    hooks = get_plugin_manager()._hooks
    hook_list = hooks.setdefault("pre_tool_call", [])
    hook_list.append(guard)
    response_hooks = hooks.setdefault("post_api_request", [])
    response_hooks.append(after_model)
    token = set_hermes_interactive_context(True)
    set_approval_callback(ask)
    agent = None
    try:
        with observe_http(run, ENDPOINT), observe_functions(run, select):
            agent = AIAgent(base_url=ENDPOINT, api_key="local-demo", provider="custom",
                            api_mode="chat_completions", model=model, session_id=run.id,
                            max_iterations=14, run_budget_seconds=180, quiet_mode=True,
                            enabled_toolsets=tools, session_db=db, cwd=str(WORKSPACE),
                            tool_complete_callback=tool_complete,
                            skip_background_review=True, checkpoints_enabled=False)
            names = [item["function"]["name"] for item in agent.tools]
            run.emit("tool", "Hermes Registry에서 선택한 도구", names)
            unexpected = set(names) - {"read_fab_bin", "publish_fab_report", "session_search", "inspect_terminal_guard",
                                       "skills_list", "skill_view", "skill_manage", "delegate_task"}
            if unexpected:
                raise RuntimeError(f"데모에 허용하지 않은 도구: {sorted(unexpected)}")
            result = agent.run_conversation(prompt, system_message=SYSTEM)
            run.emit("result", "Hermes 실행 결과", {key: result[key] for key in
                     ("final_response", "completed", "failed", "error", "api_calls") if key in result})
            if result.get("failed") or result.get("error"):
                run.emit("error", "Hermes 실행 실패", result.get("error") or result.get("final_response"))
    finally:
        if agent is not None:
            agent.close()
        set_approval_callback(None)
        reset_hermes_interactive_context(token)
        hook_list.remove(guard)
        response_hooks.remove(after_model)
        db.close()


def configure():
    if not (SOURCE / "run_agent.py").is_file():
        raise SystemExit("먼저 demos/setup.ps1로 Hermes 공식 소스를 설치하세요.")
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    os.environ["HERMES_HOME"] = str(HOME)
    os.environ["HERMES_YOLO_MODE"] = "0"
    config = HOME / "config.yaml"
    config.write_text('approvals:\n  mode: manual\ntools:\n  tool_search:\n    enabled: "off"\n', encoding="utf-8")
    (WORKSPACE / "AGENTS.md").write_text("합성 FAB-DEMO-r3 데이터만 사용하고 수치를 Tool 결과와 대조합니다.\n", encoding="utf-8")
    sys.path.insert(0, str(SOURCE))


if __name__ == "__main__":
    configure()
    serve("hermes", SCENARIOS, execute, int(os.environ.get("DEMO_HERMES_WEB", "18000")), ENDPOINT)
