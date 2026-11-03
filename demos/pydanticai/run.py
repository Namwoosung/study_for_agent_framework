"""Interactive observation of PydanticAI Core and Harness."""
import asyncio
import os
import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, bin_metrics, observe_functions, observe_http, serve
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ModelRetry, NativeOutput, PromptedOutput, TextOutput, ToolOutput
from pydantic_ai.conversation import ConversationTypeAdapter
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.usage import UsageLimits

ENDPOINT = "http://127.0.0.1:10001/v1"
STORE = ROOT / ".local" / "pydanticai-state"
INSTRUCTIONS = """합성 반도체 BIN 분석 데모다. A17/B04의 실제 입력값은 read_bin으로 조회한다.
불량률은 failed/tested로 검증한다. 예측은 과거 값에 근거한 가설로 표시한다.
실제 제조 데이터나 외부 시스템은 사용하지 않는다."""
SCENARIOS = {
    "graph": ["실행 Graph", "A17의 불량률과 최근 추세를 조회해서 설명해 줘.", ["node", "context", "tool", "response"]],
    "deps": ["Deps와 접근 범위", "B04 불량률을 조회해 줘. 조회가 거부되면 이유를 말해 줘.", ["deps", "node", "tool", "context"]],
    "conversation": ["대화 저장·복원", "이 대화에서 마지막으로 조회한 BIN을 기억해? 없다면 A17을 조회해 줘.", ["state", "context", "node"]],
    "outputs": ["출력 모드 4종", "A17 불량률을 조회해 결과로 반환해 줘.", ["case", "context", "tool", "result", "error"]],
    "end": ["같은 응답과 종료 정책", "A17 4.2% 보고서를 제출하면서 record_review도 같은 응답에서 호출해 줘.", ["case", "context", "tool", "result", "error"]],
    "core": ["Core로 만드는 업무 Agent", "A17을 조회한 뒤 수율 보고서를 검증해서 반환해 줘.", ["case", "deps", "node", "tool", "result"]],
    "harness": ["Harness Memory", "A17의 추세를 확인하고 다음 분석에서 확인할 가설을 기억에 저장해 줘.", ["case", "memory", "tool", "context", "result"]],
    "delegation": ["Harness Subagents", "A17을 먼저 조회한 뒤 조회 결과를 통계 검토자와 공정 검토자에게 각각 전달해 분석을 위임하고 두 결과를 종합해 줘.", ["delegation", "node", "context", "tool", "result"]],
}


@dataclass
class Deps:
    tenant: str
    allowed_bins: frozenset[str]


class Report(BaseModel):
    bin_id: str
    defect_rate: float = Field(ge=0, le=1)
    finding: str


def clean_text(text: str) -> str:
    return text.strip()


class CapturingModel(OpenAIChatModel):
    """The first response is captured from the endpoint, then can be replayed verbatim."""
    first = None
    replay = None

    async def request(self, messages, model_settings, model_request_parameters):
        if self.replay is not None:
            response, self.replay = deepcopy(self.replay), None
        else:
            response = await super().request(messages, model_settings, model_request_parameters)
        if self.first is None:
            self.first = deepcopy(response)
        return response


def select(module, name):
    if module.startswith("pydantic_ai._agent_graph") and name in {
        "run", "_prepare_request_parameters", "_handle_tool_calls", "_process_response_output",
    }:
        return "node"
    if module.startswith(("pydantic_ai.tool_manager", "pydantic_ai._tool_execution")) and name in {
        "validate_tool_call", "execute_tool_call", "process_tool_calls", "_run_strategy",
    }:
        return "tool"
    if module.startswith("pydantic_ai_harness.memory") and name in {
        "for_run", "before_model_request", "write_memory", "read_memory", "search_memory",
    }:
        return "memory"
    if module.startswith("pydantic_ai_harness.subagents") and name in {"delegate_task", "_run_delegation"}:
        return "delegation"
    return None


async def workflow(run, scenario, prompt, session):
    model_id = os.environ.get("DEMO_PYDANTIC_MODEL", "seminar-model")
    provider = OpenAIProvider(base_url=ENDPOINT, api_key="local-demo")
    profile = OpenAIModelProfile(supports_json_schema_output=True)
    deps = Deps("training-fab", frozenset({"A17"} if scenario == "deps" else {"A17", "B04"}))

    def model():
        return CapturingModel(model_id, provider=provider, profile=profile)

    def make_agent(llm, output=str, strategy="graceful", capabilities=()):
        agent = Agent(llm, deps_type=Deps, output_type=output, end_strategy=strategy,
                      instructions=INSTRUCTIONS, capabilities=capabilities, retries=2)

        @agent.tool
        def read_bin(ctx: RunContext[Deps], bin_id: str) -> dict:
            run.emit("deps", "Python Tool에서 읽은 RunContext.deps",
                     {"tenant": ctx.deps.tenant, "allowed_bins": sorted(ctx.deps.allowed_bins), "requested": bin_id})
            if bin_id.upper() not in ctx.deps.allowed_bins:
                return {"error": "BIN access denied"}
            value = bin_metrics(bin_id)
            run.emit("tool", "업무 Tool 반환값", value)
            return value

        if scenario == "end":
            @agent.tool_plain
            def record_review(note: str) -> str:
                run.emit("tool", "record_review 실제 실행", note)
                return "Recorded in this demo trace"
        if scenario == "core":
            @agent.output_validator
            def verify(ctx: RunContext[Deps], report: Report) -> Report:
                if report.bin_id.upper() not in ctx.deps.allowed_bins:
                    raise ModelRetry("허용된 BIN만 사용하세요.")
                expected = bin_metrics(report.bin_id)["defect_rate"]
                run.emit("tool", "앱의 결정적 수치 검증", {"expected": expected, "actual": report.defect_rate})
                if abs(expected - report.defect_rate) > 0.00001:
                    raise ModelRetry("조회한 failed/tested를 다시 계산하세요.")
                return report
        return agent

    async def invoke(agent, user, conversation=None):
        async with agent.iter(user, deps=deps, conversation=conversation,
                              usage_limits=UsageLimits(request_limit=8)) as stream:
            async for node in stream:
                state = stream.ctx.state
                name = type(node).__name__
                role = {
                    "UserPromptNode": "사용자 입력과 대화 이력 준비",
                    "ModelRequestNode": "모델 요청 구성 및 전송",
                    "CallToolsNode": "Tool 호출과 최종 출력 처리",
                    "End": "최종 결과 반환",
                }.get(name)
                run.emit("node", name, {"role": role, "run_step": state.run_step,
                         "message_count": len(state.message_history), "usage": state.usage})
        result = stream.result
        run.emit("result", "Agent 최종 출력", result.output)
        run.emit("state", "실행 뒤 메시지 이력", result.all_messages())
        return result

    if scenario == "outputs":
        for name, output in [
            ("ToolOutput", ToolOutput(Report)), ("NativeOutput", NativeOutput(Report)),
            ("PromptedOutput", PromptedOutput(Report)),
            ("TextOutput", TextOutput(clean_text)),
        ]:
            run.emit("case", name, {"mode": name, "model": model_id})
            try:
                await invoke(make_agent(model(), output), prompt)
            except Exception as exc:
                run.emit("error", name + " 실패", str(exc))
        return

    if scenario == "end":
        # Use the actual first model response from the live early run, not a synthetic ToolCall.
        llm = model()
        outcomes = {}

        async def compare_policy(engine, strategy):
            start = len(run.events)
            run.emit("case", strategy + (" · 실제 응답 수집" if strategy == "early" else " · 첫 모델 응답 재사용"))
            error = None
            result = None
            try:
                result = await invoke(make_agent(engine, ToolOutput(Report, name="submit_report"), strategy), prompt)
            except Exception as exc:
                error = exc
                run.emit("error", strategy + " 실행 실패", str(exc))
            outcomes[strategy] = {
                "실행된 기록 Tool": [e["value"] for e in run.events[start:] if e["title"] == "record_review 실제 실행"],
                "실제 모델 요청 수": sum(e["category"] == "context" for e in run.events[start:]),
                "결과": result.output if result else None,
                "오류": str(error) if error else None,
            }
            return error

        first_error = await compare_policy(llm, "early")
        if llm.first is None:
            raise first_error or RuntimeError("재사용할 모델 응답이 없습니다.")
        names = [p.tool_name for p in llm.first.parts if hasattr(p, "tool_name")]
        run.emit("case", "같은 실제 응답을 이후 정책에 재사용", {"tools": names, "response": llm.first})
        if not {"submit_report", "record_review"}.issubset(names):
            run.emit("case", "이번 응답에 두 Tool이 함께 들어오지 않았습니다", names)
        for strategy in ("graceful", "exhaustive"):
            replay = model()
            replay.replay = llm.first
            await compare_policy(replay, strategy)
        run.emit("case", "정책별 실제 실행 비교", outcomes)
        return

    capabilities = []
    if scenario == "harness":
        from pydantic_ai_harness.memory import Memory
        capabilities.append(Memory(store=MEMORY.store, namespace="fab-seminar"))
        run.emit("case", "Harness Memory 추가", {"store": type(MEMORY.store).__name__, "scope": "fab-seminar"})
    if scenario == "delegation":
        from pydantic_ai_harness.subagents import SubAgent, SubAgents
        children = [
            SubAgent(Agent(model(), instructions=role), name=name, description=role)
            for name, role in [
                ("statistics", "합성 불량률과 추세의 수치 근거를 검토합니다."),
                ("process", "공정 가설과 추가 검증 조건을 검토합니다."),
            ]
        ]
        capabilities.append(SubAgents(agents=children))
    if scenario == "core":
        run.emit("case", "Core 구성", {"앱": ["조회 함수", "Deps", "Report", "output_validator"],
                                     "Core": ["Graph", "Tool schema", "검증 및 재시도"]})
    agent = make_agent(model(), Report if scenario == "core" else str, capabilities=capabilities)
    conversation = None
    path = None
    if scenario == "conversation":
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", session):
            raise ValueError("세션 키는 영문·숫자·밑줄·하이픈 1~64자입니다.")
        STORE.mkdir(parents=True, exist_ok=True)
        path = STORE / f"{session}.json"
        if path.exists():
            conversation = ConversationTypeAdapter.validate_json(path.read_bytes())
        run.emit("state", "Conversation 저장소에서 로드", {"session": session, "conversation": conversation})
    result = await invoke(agent, prompt, conversation)
    if path:
        data = ConversationTypeAdapter.dump_json(result.conversation)
        temp = path.with_suffix(".tmp")
        temp.write_bytes(data)
        temp.replace(path)
        run.emit("state", "ConversationTypeAdapter로 직렬화해 저장", {"session": session, "bytes": len(data)})


def execute(run, scenario, prompt, session):
    with observe_http(run, ENDPOINT), observe_functions(run, select):
        asyncio.run(workflow(run, scenario, prompt, session))


if __name__ == "__main__":
    from pydantic_ai_harness.memory import Memory
    MEMORY = Memory()
    serve("pydanticai", SCENARIOS, execute, int(os.environ.get("DEMO_PYDANTIC_WEB", "18001")), ENDPOINT)
