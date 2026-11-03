# PydanticAI 이후 네 SDK의 발표 구성

PydanticAI의 작성 목적은 **Python에 작성한 Agent 선언이 모델 요청, Tool 실행, 출력 검증, 상태 전이로 바뀌는 과정과 개발자가 직접 맡는 부분을 코드로 설명하는 것**이다. 네 후속 주제에서는 이 과정을 공통 기준으로 사용한다. Hermes 이후 Claude Code에서 공통 루프를 짧게 연결하고 지침, 권한, 위임의 구현 차이를 다룬 것과 같은 편집 원칙이다.

## 공통 구성

- PA05–10의 선언과 실행, PA13–17의 입력과 대화, PA18–30의 Tool과 출력, PA35–37의 승인, PA46–50의 위임과 관측을 비교 기준으로 쓴다.
- 각 편의 첫 장은 같은 LOT-A 요청을 누가 실행하고, 누가 다음 단계로 전환하며, 어떤 상태를 앱이 갖는지 보여 준다. Tool schema나 LLM 루프의 일반 설명은 해당 차이를 읽는 데 필요한 만큼 연결한다.
- 동일한 합성 입력을 사용한다. LOT-A와 snapshot r3에서 92/100을 읽어 보고서를 만든다. 편마다 하나의 차이를 드러내는 실패 사례를 추가한다.
- 화면에는 짧은 실제 API 코드, 이벤트나 상태의 전후, 실패 조건을 배치한다. Sources에는 고정 버전과 파일·심볼, 설정 조건, 앱의 책임, 실행 검증 여부를 표시한다. 교재의 코드와 현행 문서가 다르면 선택 버전을 기준으로 다시 확인한다.
- 초안은 연결 1장과 네 주제 27장이다. 제시 순서를 따른다. 마지막 OpenAI 편에서 PydanticAI와 가장 직접적으로 맞물리는 Runner 비교로 돌아온다.

## 1. Claude Agent SDK · Claude Code 실행을 앱에 어떻게 연결할까? · 6장

비교 시작점은 PA04의 Python 함수 등록과 Claude Code 편의 권한·Hook이다. 이 편의 목적은 **업무 앱의 Python 프로세스와 Claude 실행 환경의 경계**를 그리는 것이다.

1. **두 프로세스의 책임** — PydanticAI Agent의 호스트 실행과 Python SDK → transport → Claude 런타임을 나란히 그린다. 공개 SDK의 subprocess transport와 메시지 경계를 따라간다.
2. **단발 요청과 계속 이어가는 클라이언트** — `query()`와 `ClaudeSDKClient`를 같은 요청으로 비교한다. 입력, 비동기 메시지 소비, 연결 수명, 결과 메시지를 표시한다.
3. **같은 LOT 조회 함수의 두 연결법** — PydanticAI `@agent.tool`과 SDK `@tool` + `create_sdk_mcp_server`를 대비한다. 함수의 물리적 실행 위치와 런타임의 호출 전달을 따로 그린다.
4. **실행 환경과 권한을 앱에서 구성하기** — 앱이 설정한 cwd·도구·권한 모드, 권한 콜백과 Hook의 적용 지점을 표시한다. 금지된 파일이나 LOT 접근이 들어왔을 때 어느 경계에서 막을지 보여 준다.
5. **대화 재개와 분석 파일 재현** — session ID를 이어 받아도 보고서 파일과 원본 snapshot은 별도 상태다. resume 전후 대화, 작업 디렉터리, 파일 버전을 표로 비교한다.
6. **앱이 받는 최종 결과** — 메시지 스트림과 구조화 결과를 앱의 검증·오류 처리에 연결한다. 예시는 조회 Tool 1개와 권한 거절 1건으로 구성한다.

개인 코멘트인 도메인 함수의 실행기 연결과 대화 이동성·파일 재현성을 각각 3번과 5번에 배치한다. 근거는 [Python SDK 레퍼런스](https://code.claude.com/docs/en/agent-sdk/python)와 [공개 Python SDK](https://github.com/anthropics/claude-agent-sdk-python)다.

## 2. Google ADK · Event가 세션과 업무 상태를 어떻게 바꿀까? · 7장

비교 시작점은 PA07의 내부 Graph 노드와 PA16의 Conversation이다. 이 편의 목적은 **Runner가 내보내는 Event와 세션에 쌓이는 변경을 읽는 법**을 설명하는 것이다.

1. **같은 요청의 실행 지도** — 앱 → Runner → Agent/Flow → Event를 그리고 SessionService가 관여하는 곳을 표시한다.
2. **Tool 결과가 이벤트가 되는 과정** — 모델 호출, FunctionCall, FunctionResponse, `Event.actions.state_delta`를 순서대로 읽는다. 결과 텍스트와 상태 갱신을 따로 표시한다.
3. **어떤 상태가 어디까지 남나** — Session, state, 장기 검색 및 Artifact를 구분한다. `session_id`, snapshot r3, 보고서 Artifact 식별자를 연결하는 저장 예시를 쓴다.
4. **누가 다음 Agent를 선택하나** — Agent 전이와 Sequential/Parallel/Loop 계열의 코드 제어를 비교한다. 동일 업무에서 모델이 도구를 고르는 경우와 앱이 단계 순서를 고정한 경우를 보여 준다.
5. **ADK 2.0 Graph Workflow** — Node/Edge로 업무 단계를 그린다. 앞 장의 기존 Workflow Agent, PydanticAI 내부 Graph, 사용자 업무 Graph의 역할을 비교하고 버전별 API를 표시한다.
6. **답변 완료와 업무 완료** — 모델이 보고서를 설명한 Event와 보고서 검증·저장 완료를 각각 표현한다. Artifact 저장에 실패하는 경우 어떤 상태가 남는지 질문한다.
7. **이벤트를 기준으로 테스트하기** — 상태 변경, Artifact 참조, 후속 단계 진입을 확인한다. 콜백·Plugin의 일반 목록은 Sources로 두고 필요한 개입 지점만 실코드로 보여 준다.

개인 코멘트의 분석가 응답과 업무 완료, 대화 기록과 분석 근거 저장을 3번과 6번에서 직접 다룬다. 근거는 [ADK Runtime](https://adk.dev/runtime/)과 [ADK Python 공개 소스](https://github.com/google/adk-python)다.

## 3. Microsoft Agent Framework · 업무 흐름 자체를 어떻게 실행하고 복구할까? · 7장

비교 시작점은 PA37의 승인 재개와 PA45의 대화·Step·Durable 실행 구분이다. 이 편의 목적은 **Agent 한 번의 Run을 외부 업무 Workflow의 한 단계로 넣고, 단계 사이 메시지와 복구 계약을 설계하는 법**을 설명하는 것이다. 네 편의 비교 언어는 Python으로 맞추고 .NET API는 별도 표기한다.

1. **Agent 실행과 업무 Workflow의 두 층** — 조회 Agent 내부 Tool loop와 `조회 → 계산 → 승인 → 발행`을 제어하는 외부 Workflow를 겹쳐 그린다.
2. **Executor와 Edge의 메시지 계약** — Python Executor의 입력, Edge 라우팅, 다음 Executor가 받는 값을 같은 LOT 보고서 타입으로 보여 준다.
3. **AgentExecutor가 하는 변환** — Workflow 메시지를 Agent 실행에 넘기고 세션 및 출력 이벤트가 연결되는 지점을 살펴본다.
4. **병렬 분석을 어떤 키로 합칠까?** — 온도·압력 결과를 fan-out/fan-in으로 그리고 응답 도착 순서를 바꾼다. LOT, snapshot, 분석 종류 키로 합쳐야 하는 이유를 보여 준다.
5. **승인 입력을 기다렸다가 재개** — `RequestPort` 또는 해당 버전의 executor request/response를 사용해 대기 이벤트와 승인 응답을 추적한다. 보고서 r4에 r3 승인을 재사용하지 않는 검사는 앱에서 표시한다.
6. **Checkpoint에서 어디까지 돌아올까?** — 저장된 Workflow·executor 상태, 이전 승인 요청, 이미 완료된 외부 발행을 구분한다. 모의 발행에 멱등 키를 둔 경우와 중복 실행되는 경우를 비교한다.
7. **어느 부분을 Agent로 둘까?** — 근거 요약은 Agent, 수율 재계산·승인 게이트·발행은 명시적 Executor로 나눈 코드 배치를 보여 준다.

개인 코멘트의 승인 범위와 병렬 결과 결합을 4–6번에 배치한다. 근거는 [Agent Executor](https://learn.microsoft.com/agent-framework/workflows/advanced/agent-executor)와 [Workflow의 Human-in-the-loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)다.

## 4. OpenAI Agents SDK · Runner는 언제 멈추고 누구에게 넘길까? · 7장

비교 시작점은 PA25–30의 출력·종료 정책과 PA46의 위임이다. 이 편의 목적은 **같은 응답에서 Runner가 최종 결과, 후속 모델 호출, 주체 전환을 어떻게 선택하는지**를 설명하는 것이다.

1. **PydanticAI Graph와 OpenAI Runner의 한 턴** — 같은 ToolCall 입력에서 실행 상태, 후속 호출, 최종 출력이 생성되는 경로를 나란히 그린다.
2. **Tool 결과가 곧 답이면 다시 모델을 호출할까?** — `tool_use_behavior`의 재호출과 직접 종료를 같은 정형 조회로 비교한다. PydanticAI `EndStrategy`와 적용 조건 및 같은 응답의 다른 Tool에 미치는 효과를 분리한다.
3. **전문가에게 묻기와 답변 책임 넘기기** — `Agent.as_tool()`은 부모가 결과를 받는 경우, handoff는 다음 Agent가 실행의 주체가 되는 경우로 그린다. 입력 필터와 다음 Agent가 보는 이력을 확인한다.
4. **어떤 상태를 저장할까?** — Session의 대화 이력, `RunState`의 중단·재개 상태, 모델 공급자 측 대화 식별자를 비교한다. PydanticAI Conversation/Deferred와 저장 책임을 대응시킨다.
5. **실행 전 검사와 승인 대기** — input/output guardrail과 function tool guardrail의 경계를 구별한다. 승인 필요한 발행 Tool을 중단하고 재개하는 예에서 앱의 승인 검증을 표시한다.
6. **Trace에서 주체가 바뀐 곳 찾기** — 모델, 함수, handoff, guardrail span을 같은 요청에 연결한다. 전송 및 민감 데이터 수집 설정을 선택 버전에 맞춰 정리한다.
7. **같은 고정 응답으로 결과 비교** — 모델 호출 수, 실행된 Tool, 최종 응답을 맡은 Agent, 저장·재개 상태를 표로 확인한다. 서로 다른 SDK의 처리 규칙을 보여 주는 실험으로 구성한다.

개인 코멘트의 후속 모델 해석 여부와 답변 책임 이전을 2–3번의 핵심으로 삼는다. 근거는 [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), [Handoffs](https://openai.github.io/openai-agents-python/handoffs/), [Tracing](https://openai.github.io/openai-agents-python/tracing/)이다.

## 작성과 검수 순서

1. 각 교재의 기본·심층·실무 코멘트에서 장표별 근거 절을 연결하고 SDK/런타임 버전을 잠근다.
2. 각 편에서 가장 중요한 차이부터 고정 입력으로 재현한다. Claude는 Tool 실행 위치와 resume, ADK는 Event와 상태 반영, Microsoft는 승인 대기와 병렬 결합, OpenAI는 재호출·직접 종료와 handoff를 우선한다.
3. 한 장마다 앱 코드, SDK가 처리하는 경로, 관찰할 상태 변화, 실패의 의미를 점검한다. 외부 모델·실서비스에서 확인할 항목은 로컬 고정 응답 결과와 구분해 기록한다.
4. 기술별 개념 소개와 중복 설명을 줄이고 Sources에 실제 함수·버전·제약을 넣는다. 네 편의 분량은 시연 시간에 따라 조정한다.

## 2026-11-03 소스 조사와 구현 기준

Python으로 통일한다. 기존 네 교재의 기본편·심층편·실무 코멘트를 장표의 편집 근거로 사용하고, 동작과 기본값은 아래 고정 태그를 우선한다. 이번 조사에서는 태그의 소스 파일과 공식 레퍼런스를 대조했다. 라이브 모델 실행, 패키지 설치 후 예제 실행, 모든 예외 분기 검증은 아래 구현 단계에 포함한다.

### Claude Agent SDK · Python v0.2.177

- **1–3장 구현 경로.** `query()`에서 SDK 내부 Query 및 subprocess transport로 들어간다. `SubprocessCLITransport._build_command()`에서 옵션이 CLI 인자로 변환되는 예를 표시한다. 이어 `_handle_control_request()`와 `_handle_sdk_mcp_request()`로 CLI에서 Python 쪽 콜백·도구로 돌아오는 방향을 그린다. 단발 호출과 상호작용 클라이언트의 수명 차이를 짧은 코드 두 조각으로 보여 준다. CLI 내부의 모델 반복·도구 계획은 공식 계약과 관찰된 이벤트 수준으로 표시한다. [공개 진입점](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.177/src/claude_agent_sdk/query.py) · [transport](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.177/src/claude_agent_sdk/_internal/transport/subprocess_cli.py#L570) · [control/MCP 처리](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.177/src/claude_agent_sdk/_internal/query.py#L606)
- **4–6장 설정과 검증.** `ClaudeAgentOptions`의 `permission_mode=None`, `max_turns=None`, `setting_sources=None`은 Python 옵션의 값으로 기록하고 실제 CLI 인자 및 권한 판정과 분리한다. `include_partial_messages=False`와 결과 수집을 연결한다. 같은 `read_lot` 요청에서 권한 콜백 거절과 도메인 함수의 LOT 인가 거절을 별도로 시연하고 실행 횟수를 확인한다. 프로젝트 설정 로딩, cwd, sandbox, 세션 resume/fork, 구조화 결과와 실패 subtype을 Sources에서 각각 설명한다. sandbox 지원 조건과 파일 복구 범위는 런타임/OS별 확인 항목으로 둔다. [옵션 정의](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.177/src/claude_agent_sdk/types.py#L2393) · [Anthropic 공식 Cookbook](https://platform.claude.com/cookbook/claude-agent-sdk-01-the-chief-of-staff-agent)
- **장점·비용.** 파일·셸·기존 Claude Code 실행환경을 업무 앱에 붙일 때 조립할 부분이 줄어든다. 그만큼 CLI 버전, 작업 디렉터리, 배포 격리와 정책의 영향이 커진다. 코드 실행을 설명하는 3장에는 in-process MCP와 외부 MCP를 구별하고, Sources에는 subagents, hooks, plugins 및 설정 로딩을 별도 색인으로 남긴다.

### Google ADK · Python v2.13.0

- **1–3장 구현 경로.** `Runner.run_async()` → `BaseLlmFlow` → 모델/함수 응답 → `Runner._process_and_append_event()` → `SessionService.append_event()` 순서로 따라간다. Runner에서 부분 이벤트와 저장 후보를 거르는 위치를 코드로 표시하고, before/after 이벤트와 `state_delta`를 실제 데이터로 비교한다. 상태 스코프(`app:`, `user:`, 세션, `temp:`), Memory, Artifact를 별도 열로 보여 준다. [Runner](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/runners.py#L1536) · [LLM flow](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/flows/llm_flows/base_llm_flow.py) · [SessionService](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/sessions/base_session_service.py#L166)
- **4–7장 설정과 검증.** 일반 LLM 실행의 `streaming_mode=NONE`, `max_llm_calls` 기본 500 및 `ADK_MAX_LLM_CALLS` 경로를 읽는다. Live 실행은 별도 경로다. Graph의 `Workflow._run_loop()`, `_schedule_ready_nodes()`, `_emit_node_checkpoint()`를 사용해 준비된 노드가 실행되고 중간 상태가 남는 지점을 그린다. ADK 2.x 그래프와 기존 Sequential/Parallel/Loop, 모델이 고르는 transfer, AgentTool 반환을 구분한다. 고정 모델 응답, 실제 세션·Artifact 구현, 강제 저장 실패를 조합해 final response와 발행 완료를 구별한다. [RunConfig](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/agents/run_config.py) · [Graph scheduler](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/workflow/_workflow.py#L305) · [공식 Runtime 문서](https://adk.dev/runtime/)
- **장점·비용.** 이벤트와 서비스 인터페이스로 상태 변화와 산출물의 경계를 관찰하기 쉽다. 서비스 구현과 스코프를 잘못 고르면 저장 범위나 복구 의미를 오해하기 쉽다. Sources에는 callback과 plugin 개입 순서, Graph 중단·재개, context compaction·prefix caching, Live 및 평가 기능을 남긴다. Google 관리형 배포와 Python 라이브러리 동작은 별도로 표시한다.

### Microsoft Agent Framework · Python 1.24.0

- **1–4장 구현 경로.** `WorkflowBuilder`의 executor·edge 연결 → `Workflow.run()`의 초기 메시지/복구 분기 → `AgentExecutor.from_message()` → `_run_agent_and_emit()`로 흐름을 그린다. AgentSession은 내부 대화 상태로, workflow 메시지와 checkpoint는 바깥 단계 상태로 표시한다. fan-out/fan-in 코드에서 SDK가 전달하는 입력 타입과 앱이 검증하는 LOT·snapshot 키를 구분한다. 기본 실행 경로 확인 시 deprecated Runner를 진입점으로 사용하지 않는다. [WorkflowBuilder](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_workflow_builder.py) · [Workflow](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_workflow.py#L712) · [AgentExecutor](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_agent_executor.py#L447)
- **5–7장 설정과 검증.** `checkpoint_storage=None`에서 외부 저장소를 지정하는 경우로 넘어가고, Python 1.13.0부터 추가된 최초 입력·응답 전달 시점의 entry checkpoint와 superstep 완료 checkpoint를 타임라인에 표시한다. 메모리 저장과 파일 저장을 별도 시험한다. 승인 요청 ID, 보고서 revision 및 발행 멱등 키를 기록하고, 체크포인트 복구로 외부 발행이 중복될 수 있는 상황을 만든다. 일반 workflow 요청과 AgentExecutor가 중계하는 tool 승인 요청은 별도 경로로 표시한다. [공식 Python 체크포인트 가이드](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/checkpoints?pivots=programming-language-python) · [체크포인트 구현](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_checkpoint.py)
- **장점·비용.** 승인, 병렬 결합, 복구 위치를 업무 그래프와 타입에 드러낼 수 있다. 그래프·저장소·메시지 버전 관리와 외부 부작용 통제가 추가된다. Sources에는 orchestration builders, Agent/Function middleware 및 context providers를 남기고 Azure Foundry와 .NET 의존 조건을 Python 핵심 예제와 구분한다.

### OpenAI Agents SDK · Python v0.24.0

- **1–3장 구현 경로.** `Runner.run()` → 모델 응답 분류 → function-tool 처리 → `_maybe_finalize_from_tool_results()` 또는 `execute_handoffs()` 흐름을 추적한다. 같은 응답에 두 Tool 호출을 넣어 `stop_on_first_tool`에서 최종값 선택과 실제 실행된 도구 목록을 각각 기록한다. 이를 PydanticAI `EndStrategy`와 비교할 때 함수 도구 종료 정책과 출력 도구 처리의 적용 위치를 구분한다. `Agent.as_tool()`의 중첩 실행과 handoff의 활성 Agent·이력 전환을 나란히 그린다. [Runner](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run.py) · [turn resolution](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/turn_resolution.py) · [Agent 정의](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/agent.py)
- **4–7장 설정과 검증.** Runner 기본 10턴과 `None`의 의미, `tool_use_behavior="run_llm_again"` 기본값을 표시한다. Session과 Responses API 대화 식별자 및 `RunState`의 저장 책임을 비교한다. 첫 Agent의 input guardrail, 최종 출력 Agent의 output guardrail, function tool의 guardrail, approval 중단을 구분한다. 병렬·선행 input guardrail에서 모델 호출이 이미 시작됐는지, 승인 전후 함수 실행 횟수가 몇 회인지 고정 응답과 호출 카운터로 검증한다. trace 수집과 민감 데이터 포함 설정은 실험에서 명시적으로 지정하고 SDK 기본값과 분리해 표기한다. [RunConfig](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_config.py) · [RunState](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_state.py) · [Guardrails](https://openai.github.io/openai-agents-python/guardrails/) · [Running agents](https://openai.github.io/openai-agents-python/running_agents/)
- **장점·비용.** 주체 전환, Tool 종료, 승인, trace를 작은 앱 코드로 구성할 수 있다. 어떤 이력이 전달되는지, 저장소가 어디인지, hosted 기능을 어느 provider가 제공하는지에 따라 실행 계약이 달라진다. Sources에는 hosted tools/MCP, Realtime, sandbox·skills를 별도로 남기고 각 기능의 API 및 서비스 전제를 표시한다.

## 장표 구현 순서와 완료 조건

1. **기준 정리.** blueprint의 구 예약 순서(S39–S42)를 이번 사용자 지정 순서와 맞춘다. 기존 마지막 PydanticAI 슬라이드와 실습 동선을 확인하고, 후속 파트가 시작되는 연결 슬라이드에서 ‘다음 단계의 주체 / 상태 소유자 / 외부 실행 경계’ 세 축을 소개한다. 28장은 장표 후보 총량이며 각 편의 대표 코드와 실패를 본 발표에 우선 배정한다. 상세 설정·지원 조건·추가 기능은 같은 장의 Sources와 발표 노트에서 찾을 수 있게 한다.
2. **예제부터 확정.** 별도 환경에 SDK 버전과 전이 의존성을 고정한다. Claude는 Python SDK와 실제 선택된 CLI 버전을 각각 기록한다. 공통 fixture는 LOT-A, snapshot r3, 92/100, r3에만 유효한 승인이다. 공통 로그는 모델 호출 수, 실행 주체, tool/request ID, 상태·산출물 참조, 종료 이유, 발행 횟수다. Claude transport 검증과 실제 CLI 모델 실행, ADK/OpenAI의 고정 모델 응답과 실제 provider 실행, Microsoft의 로컬 워크플로와 외부 서비스 호출을 별도 검증 항목으로 기록한다.
3. **실패 기준 고정.** Claude는 금지된 호출에서 도메인 함수 실행 0회, ADK는 저장 실패 시 발행 완료 0회와 실제로 남은 이벤트 확인, Microsoft는 r3 승인으로 r4 발행 0회 및 동일 키 재생 시 중복 발행 0회, OpenAI는 동일 고정 응답에서 모드별 모델 호출 수·도구 호출 수·최종 Agent를 각각 검증한다. 모의 환경에서 확인한 결과만 해당 범위의 성공으로 표기한다.
4. **기존 덱에 연결.** `build.py`의 주제별 revision/ORDER 패턴과 Sources 생성 규약을 재사용한다. 장표마다 고정 태그 또는 커밋, 파일·심볼, 공식 가이드, 대응하는 학습 문서 절, 설정의 적용 범위, 실험 결과를 연결한다. 코드에서 생략한 부분은 축약 표기를 붙인다. 시연에 필요한 UI는 기존 흐름에 맞춰 계획하고, 정적 장표에서도 전후 상태를 읽을 수 있게 한다.
5. **재생성 및 확인.** 구현 후 `python presentations/seminar-2/build.py`로 HTML·PDF·notes·manifest를 재생성한다. blueprint/내용 검사와 `validate.cjs`를 기존 실행 방식으로 돌린다. 실제 브라우저에서 네 구분 장표의 순서, Next/Prev, 목차, Sources와 근거 링크, PDF의 코드 및 흐름도 잘림을 확인한다. 이번 작업의 산출물은 이 계획 문서다.
