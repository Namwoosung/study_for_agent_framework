# PydanticAI 발표 보강 계획 — 개발 코드에서 내부 실행까지

> 작성일: 2026-11-03 · 상태: **발표 83~143쪽에 반영**
>
> 목표: 현재 PydanticAI 19장(S20–S38)을 Hermes 수준의 코드·흐름 분석으로 확장한다. 개념의 반복보다 **개발자가 작성한 선언이 내부 객체·요청·상태 전이·실행 정책으로 바뀌는 과정**을 설명한다.

## 1. 자료 기준과 설명의 깊이

- [개인 기본 학습자료](../../../study/PydanticAI/PydanticAI.md): 기초·기능·책임 구분·반도체 사례·점검 질문.
- [개인 심층 학습자료](../../../study/PydanticAI/PydanticAI_2차_심층_학습_분석.md): 27개 단원, W1–W9 코드 추적, F01–F24 실패 시나리오.
- [개인 실무 코멘트](../../../study/PydanticAI/PydanticAI_발표_실무_시사점_코멘트.md): Node 관찰·병렬 데이터 계약·EndStrategy 부작용·승인 주체의 네 항목.
- [개인 발표 흐름과 보강 질문](../docs/flow.md): `<pydanticAI>` 아래 전체, 특히 `보강`, `Demo`, `QnA` 및 본문에 삽입한 의문.
- [현재 발표](../index.html), [발표 노트](../presenter-notes.md), [기준 blueprint](../docs/blueprint.md), [데모 계획](../docs/demo-plan.md).
- [Hermes 코드 대조 기록](hermes-code-review.md), [Claude Code 계획](claude-code-revision-plan.md): 설명 순서와 분석 깊이의 비교 기준.

발표 코드는 **사용자 작성 코드 / 공식 소스 발췌 / 공식 소스 축약 / 의사코드**를 구분한다. 내부 호출 설명에 `advance()` 같은 가상 메서드를 실 API처럼 사용하지 않는다. 앱에서 만든 함수는 앱 코드라고 표시한다. 실제 API 이름·분기·상태 필드는 유지하고, 소스 전체를 장표에 복사하지 않는다.

### 기준 버전

Core는 학습자료와 같은 **v2.61.0**을 유지한다. 공식 저장소의 같은 태그에서 Harness 소스도 확인했고, 별도 패키지 메타데이터는 **Harness 0.61.0**을 기준으로 한다. 두 패키지를 동일한 버전 번호로 적지 않는다. Harness의 동적 버전 규칙과 slim 의존성은 해당 태그의 `src/pydantic_ai_harness/pyproject.toml`에 명시되어 있다.

고정 commit: `dd82a00ae3ef9a5f147405153eb877221d74d1c7`. 조사한 소스의 경로·SHA-256·실제 심볼과 행 번호는 [출처 인덱스](../research/pydanticai-plan-sources.json)에 보관한다. 온라인 최신 문서는 설명을 보완하는 자료이며 고정 버전 코드와 충돌하면 고정 소스를 우선한다. 이전 교재의 대략적인 행 번호는 그대로 복사하지 않는다.

이번 계획은 소스 정적 확인에 기반한다. 패키지 설치, 예제 실행, 실제 모델 호출, 성능 측정은 아직 수행하지 않았다. 후속 작성 단계의 실행 통과 조건을 아래에 따로 명시한다.

## 2. 발표의 기준 질문과 순서

청중이 끝나고 답할 질문은 “PydanticAI를 쓰면 무엇을 덜 구현하고, 어떤 업무 로직은 여전히 작성해야 하는가?”다.

**작은 Agent 구성 → 요청/Loop → 입력/대화 → Tool → 출력/종료 → Capability/승인 → 선택 Harness → 위임/관측/Demo** 순서로 진행한다. Hermes와 같은 문제를 순회하되, 완성형 Harness의 사용법 대신 Python 프레임워크의 구성·실행 계약을 설명한다.

공통 agent loop·Tool calling 정의는 한 문장으로 연결한다. 깊게 설명할 부분은 Graph Node/State, 스키마 생성과 검증, ToolManager/Executor 분리, EndStrategy, Capability 합성, Conversation/Deferred 재개, Harness의 실제 저장·주입·압축이다. “타입 안전해서 좋다”로 마무리하지 않고 직접 반복 엔진을 구현할 때 사라지는 코드와 남는 책임을 대응한다.

### 가독성과 장표 수

**본문 PA01–PA52 52장 + 시작 PA00 1장 + 소주제 구분 PAD01–PAD08 8장 = 총 61장**을 작성 기준으로 삼는다. 시간 제약이 생기면 구현 상세를 부록으로 이동하되 질문 대응 자체를 삭제하지 않는다. 이는 PydanticAI 부분만의 계획 수이며 현재 전체 81장을 이미 바꿨다는 의미가 아니다.

대주제 시작은 공식 Pydantic 자산과 전체 구조로 명확히 구분한다. 소주제는 앞 구분 페이지와 상단의 짧은 경로로 알리고, 본문에 큰 범주 목록을 반복하지 않는다. 기존 slate 디자인을 유지하며 코드·도식·전후 비교를 한 장에 과밀하게 넣지 않는다. 본문 한 장은 하나의 질문, 핵심 도식 하나 또는 8–14행 핵심 코드가 원칙이다. 긴 함수·옵션·경계 사례는 다음 장과 sources 설명에 나눈다.

PA00은 **PydanticAI / Python 코드로 Agent를 구성하고 실행을 제어하기**로 시작한다. 앞서 본 Hermes와 개발 형태가 어떻게 다른지 전체 구조의 두 지점만 짚는다.

## 3. 소주제별 장표 설계

아래 `PAxx`는 후속 구현용 고정 ID다. 화면 페이지 번호는 Claude Code 부분 확장 후 재계산한다. 각 PAD 구분 장표에는 해당 범주의 질문과 구조상 위치만 둔다.

### PAD01 · Python 코드로 Agent 구성하기

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA01 | Pydantic과 PydanticAI가 맡는 일 | Field 제약이 틀린 수율을 걸러내는 예 / 수치의 사실 여부는 별도 검사 | 기본 §1–2 · 심층 §2 |
| PA02 | 전체 구조: 내 코드에서 모델까지 | App → Agent → Graph → Model/Provider, 옆으로 ToolManager·Capability; Core와 Harness 분리 | 기본 §11 · 심층 §2–3 |
| PA03 | 가장 작은 Agent는 어디까지 동작할까 | Agent(model) + run/결과; 모델 연결·Loop·업무 코드의 소유자를 색으로 구별 | 기본 §4 · Agent/AbstractAgent |
| PA04 | Tool과 출력 타입을 하나씩 붙이기 | 동일 예제를 plain 답변 → 읽기 Tool → YieldReport 순서로 확장 | 기본 §4·8 · OutputSchema |
| PA05 | 개발자가 작성할 코드와 실행 때 만들어지는 것 | 내 함수/타입/지침 → Tool schema·Output schema·Graph state·메시지; 숨겨진 생성물을 대응 | 기본 §11.2 · 심층 W1·W3·W6 |

### PAD02 · 요청이 반복되고 끝나는 과정

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA06 | run()에서 Graph가 열리기까지 | AbstractAgent.run → Agent.iter/준비·리소스 open → Graph → 결과·정리; 실제 메서드 위치 | Agent._prepare_run · _PreparedAgentRun.open |
| PA07 | 세 노드가 나누어 맡는 실행 | UserPromptNode → ModelRequestNode → CallToolsNode → 재요청/End; LangGraph와 구분 | _agent_graph.py · 심층 §4–6 |
| PA08 | 한 요청을 세 번의 모델 호출로 따라가기 | 고정 모의 응답: 잘못된 인자 → 수정된 조회 → 유효 출력; Node/Step/요청/메시지 변화 | 심층 §4.1 · 코멘트 1 |
| PA09 | 상태, 의존성, RunContext를 구별하기 | GraphAgentState(message_history/usage/output_retries_used/run_step/run_id), Graph deps, 앱 deps의 실제 필드 | GraphAgentState · build_run_context |
| PA10 | 응답에서 다음 노드를 고르는 조건 | Function/Output/일반 텍스트/Unknown/Deferred 분기; 유효하지 않은 출력은 End가 아님 | CallToolsNode._handle_tool_calls/_process_response_output |
| PA11 | 예산 소진·오류·취소 때 남는 상태 | consume_output_retry·UsageLimits·예외 전파·Task 정리·이미 완료된 부작용의 경계 | GraphAgentState · usage.py · _call_tools |
| PA12 | 실행 API 다섯 가지를 같은 요청으로 비교 | run_sync/run/run_stream/run_stream_events/iter: 반환 객체·관찰 단위·완료/commit 시점·소비자 코드 | AbstractAgent · 심층 §5·21 |

### PAD03 · 모델 입력과 대화 상태

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA13 | 모델에 전달되는 것과 Python에 남는 것 | instructions·system prompt·history·Tool schema·Output schema·settings와 deps를 분리한 실제 요청 봉투 | UserPromptNode · _prepare_request_parameters |
| PA14 | Instructions와 System Prompt의 수명 | 새 Run/기존 대화에서 동적 재평가·계승 비교; OpenAI Chat/Responses와 Anthropic 요청 형식 비교 | _reevaluate_dynamic_prompts · Model adapter |
| PA15 | deps를 이용해 조회 범위를 전달하기 | 서버가 만든 tenant/allowed_lots/snapshot/DB 객체 → RunContext → Tool; tenant는 모델 인자가 아님 | 기본 §6 · 심층 §14 |
| PA16 | History를 넘기는 것과 Conversation을 넘기는 것 | all_messages vs result.conversation/conversation=: messages·usage·conversation_id·deferred_tool_requests 비교 | conversation.py · 심층 §17 |
| PA17 | 저장·불러오기·동시 갱신은 누가 구현할까 | ConversationTypeAdapter 직렬화 → 앱 저장소 → 인증 후 load → 후속 Run; 세션 메타데이터·충돌·TTL | Conversation · 기본 §10 · 앱 설계 예시 |

### PAD04 · Tool 등록과 실제 실행

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA18 | Python 함수가 모델용 스키마가 되는 과정 | signature/docstring → function_schema → Tool/FunctionToolset → ToolDefinition → 요청 JSON; 소스가 아닌 메타데이터 노출 | _function_schema.py · tools.py · FunctionToolset |
| PA19 | tool과 tool_plain을 선택하는 기준 | RunContext 유무를 제외한 같은 계산을 비교; sync/async는 독립 축, deps를 schema 인자에서 제외 | Agent.tool/tool_plain · 기본 §7 |
| PA20 | Toolset은 도구 목록을 어떻게 바꿀까 | get_tools/call_tool 계약; Combined/Filtered/Prefixed 및 prepare 단계, Step별 재해석·Capability 캐시 | ToolManager.for_run_step · toolsets/ |
| PA21 | 호출 검증과 함수 실행은 다른 단계 | name resolve → _run_validate_hooks → ValidatedToolCall → execute_tool_call → call_tool; 인자 오류/미노출/일반 예외 | ToolManager.validate_tool_call/execute_tool_call |
| PA22 | 검증 통과 뒤에도 검사할 업무 조건 | 타입 → LOT 인가 → snapshot 일치 → 데이터 조회 → 결과 크기/단위; 각 검사 위치와 실패 기록 | 심층 §10·14·22 · 앱 Tool 코드 |
| PA23 | 여러 Tool을 동시에 실행하는 실제 코드 | asyncio.create_task와 sync offload; [A,B]→[C barrier]→[D,E], 이벤트 완료순서와 history 인덱스순서 분리 | _segment_by_barriers · _call_tools · 코멘트 2 |
| PA24 | Local Tool·MCP·Native Tool의 서로 다른 실행 위치 | Python host / MCP remote call / provider-side native execution 3갈래; 모두 동일 Toolset dispatch라는 오해 수정 | mcp.py · capabilities/mcp.py · Native Tools docs |

### PAD05 · 출력 검증과 종료·재시도

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA25 | 출력 모드 네 가지는 요청부터 다르다 | ToolOutput은 미리 output tool schema 공개 / Native는 provider schema / Prompted는 지시+parse / TextOutput은 text callback | output.py · _output.py |
| PA26 | 출력 타입이 있으면 범용 Agent가 될 수 없을까 | 최종 결과 계약과 중간 Tool 반환 타입 분리; str/복수 Output/union·실행별 override를 실제 API 기준 비교 | OutputSchema · 기본 §8 · 개인 QnA |
| PA27 | 타입 검사 뒤에 수치와 근거를 검증하기 | Pydantic → output_validator → snapshot 재계산 → ModelRetry/성공; Tool return annotation만으로 대체 불가 | ObjectOutputProcessor · run_output_with_hooks |
| PA28 | 같은 모델 응답, 서로 다른 종료 정책 | [조회 A, output O1, 배포기록 B, output O2]를 고정해 early/graceful/exhaustive 실행표·stub 결과 | process_tool_calls · 전략별 Processor · 코멘트 3 |
| PA29 | 최종 출력이 있어도 재요청하는 경우 | invalid Output·function ModelRetry·retry-wins·deferred·이미 commit된 stream 예외를 분리 | _ToolCallProcessor._apply_retry_wins · CallToolsNode |
| PA30 | Retry의 계층과 실제 요청 수 | Tool/Output retry, provider fallback/SDK/transport/App retry; 예산 소유자·한도·외부 부작용·멱등성 | ToolManager · GraphAgentState · usage.py · Retries docs |

### PAD06 · Capability, Guardrail, 승인 재개

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA31 | Capability 하나가 묶는 구성요소 | Toolset·instructions·settings·model·hooks를 묶은 Python 컴포넌트; Tool/Skill과 차이 | capabilities/abstract.py · 심층 §15 |
| PA32 | 여러 Capability가 합쳐지는 순서 | CombinedCapability의 정규화·정렬·for_run; before 정방향/after 역방향/wrap 중첩을 각각 설명 | CombinedCapability.before_model_request/after_model_request/wrap_model_request |
| PA33 | 업무 정책을 Hook에 넣는 실제 코드 | 동일 Tool에 tenant검사·결과 마스킹·호출시간 기록을 나누어 적용; 단일 Agent는 직접 Tool, 반복 정책은 Capability | ToolManager._run_validate_hooks/_run_execute_hooks |
| PA34 | Guardrail은 어느 시점에 무엇을 막을까 | Core schema/validator와 Harness Input/Tool/Output guards 구분; allow/block/retry/approve/replace 지원 위치 | InputGuardrail.wrap_model_request · ToolGuardrail · OutputGuardrail |
| PA35 | 승인이 필요하다는 판단은 누가 할까 | requires_approval 정적/조건부, ApprovalRequired 동적; 검증 전 deferral 제한, 승인 없는 실행은 보류 | ValidatedToolCall · tools.py · Deferred Tools docs |
| PA36 | 승인 UI 없이도 처리할 수 있을까 | Inline HandleDeferredToolCalls / CLI 응답 / DeferredToolRequests 반환을 비교; Run 종료와 프로세스 무한대기 구별 | deferred_tool_handler.py · 심층 §16.3 · 코멘트 4 |
| PA37 | 승인 결과로 이어지는 다음 Run | Conversation + DeferredToolResults + call ID + 보고서 버전; override_args 재검증·거부·누락·만료·위조 승인 | UserPromptNode._handle_deferred_tool_results · ToolManager |

### PAD07 · Harness로 기억과 작업 환경 더하기

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA38 | Core 위에 Harness를 붙이는 구조 | 별도 패키지 0.61.0/Capabilities 조합, Coder·Researcher의 역할; 기능별 사용 여부를 고름 | Harness pyproject.toml · Harness overview |
| PA39 | Memory를 저장·수정·검색하는 Tool | write_memory/read_memory/delete_memory/search_memory → MemoryStore; namespace/agent scope·파일명·write metadata | MemoryToolset · MemoryStore |
| PA40 | 기억이 다음 모델 입력에 들어가는 시점 | Memory.for_run → before_model_request → MEMORY.md bounded user-role snapshot; default InMemoryStore 수명 | Memory._load_snapshot/before_model_request |
| PA41 | 과거 대화 검색과 Memory 검색의 차이 | Conversation source → 섹션/토큰화/BM25 → 발췌; 노트 검색과 별도 경로·검색어 선택/범위 결정 주체 | ConversationSearchToolset.search_conversation_history · MemoryToolset.search_memory |
| PA42 | Context 압축 전후를 같은 메시지로 보기 | sliding/tool-clear/summary 전후·ToolCall↔Return 쌍·식별자·요약 비용·원본 vs ctx.messages 변형 | SlidingWindowCompaction.before_model_request · SummarizingCompaction |
| PA43 | Skill을 발견하고 필요할 때 로딩하기 | SKILL.md parse/catalog → deferred Capability 목록 → load_capability → 지침/참고파일; 중복·실패·자체 생성 검수 | Skills.for_run/_load · load_skill_libraries |
| PA44 | 파일·Shell·계획 기능을 어디까지 조합할까 | Core에 기본 shell 없음; Workspace/FileSystem/Shell/Planning/Sandbox 각 역할과 외부 환경·권한 책임 | Harness docs · 패키지의 해당 모듈 추가 추적 |
| PA45 | 대화 저장, Step 저장, Durable 실행을 구별하기 | Conversation save/load / StepPersistence settled steps와 effect 기록 / 외부 엔진 replay·복구 경계 | StepPersistence · Durable Execution docs |

### PAD08 · 위임, 관측, 개발 범위와 Demo

| ID | 장표 제목 | 본문에서 보여 줄 내용·시각화 | 근거·코드 추적 |
|---|---|---|---|
| PA46 | 위임·Handoff·Graph는 누가 다음 작업을 정할까 | Agent-as-tool은 부모 복귀 / programmatic handoff는 앱 제어 / 사용자 Graph는 명시적 분기; 내부 Agent Graph와 구분 | Multi-agent docs · 심층 §20 |
| PA47 | Harness Subagent의 자식 Run은 무엇을 받나 | delegate_task → fresh child history, deps forwarding·usage/tools 옵션·깊이 제한·오류/취소·반환 병합 | SubAgentToolset._run_delegation · Subagents |
| PA48 | Dynamic Workflow와 Advisor를 붙이는 경우 | 계획된 그래프 실행/전문가 조언의 제어권·입출력·부모 결과 반영 차이; 일반 delegation과 비교 | dynamic_workflow/_capability.py · advisor/_capability.py |
| PA49 | Trace로 모델·Tool·검증·승인을 이어 보기 | Instrumentation.wrap_run/wrap_model_request/wrap_tool_execute → OTel spans; Logfire/다른 exporter·retry·usage·민감정보 | capabilities/instrumentation.py · Observability docs |
| PA50 | 흐름 테스트와 실제 답변 평가는 따로 준비하기 | FunctionModel/TestModel/override로 경로 재현, Evals Case/Dataset/Evaluator로 수치·근거·실패율 평가 | Testing/Evals docs · 심층 §23–24 |
| PA51 | 우리 Agent는 어디까지 개발하면 될까 | 최소 실행/반복 업무 Agent/서비스 경계의 파일·함수·통과 기준; Hermes 비교는 기본 제공 범위로 설명 | 기본 §11.2·28 · 본 계획 개발 범위표 |
| PA52 | Demo: 내가 쓴 코드와 내부 실행을 함께 보기 | 같은 요청의 code/schema/Node/history/Tool/Output/Trace를 연결; 고정 응답 시험과 실제 모델 실행 구분 | 개인 Demo 요구 전부 · 본 계획 D1–D9 |

## 4. 실제로 확인한 핵심 경로와 작성 기준

아래는 전체 감사 결과가 아니라 이번 계획에서 직접 확인한 소스 경로다. 각 장표의 sources에는 **개념 → 해당 장표의 실행 설명 → 실제 심볼·소스 링크 → 실패 사례 → 앱에 남는 책임**을 적는다.

### A. Run과 Graph

`Agent._prepare_run`, `_PreparedAgentRun.open`, `_run_lifecycle_hooks`를 출발점으로 `UserPromptNode.run`, `ModelRequestNode.run`, `CallToolsNode.run`으로 연결한다. `Agent.run` 등 공개 실행 함수는 `AbstractAgent` 경로도 함께 확인한다. 정상 흐름만 그리지 않고 deferred 재개가 모델 요청보다 먼저 처리되는 분기를 포함한다.

PA08의 고정 응답 예시는 세 번의 모델 요청으로 설계한다. 첫 응답은 잘못된 조회 인자, 두 번째는 유효한 조회, 세 번째는 유효 Output이다. Node 방문 횟수, 모델 요청 횟수, Tool 실행 횟수를 같은 “루프 3번”으로 합쳐 쓰지 않는다. 실제 함수가 어떤 상태를 바꾸었는지 별도 표로 남긴다. 무Tool 정상 종료·Output retry 소진·사용량 제한·취소는 개별 사례로 분리한다.

### B. Tool 정의와 실행

`ToolManager.validate_tool_call`은 `_resolve_tool` → `_build_tool_context` → `_run_validate_hooks` → 검증 결과 객체를 만드는 경로다. `execute_tool_call`은 별도 실행 단계다. 검증 후 발생한 합법적 deferral은 `args_valid=True` 결과에 실려 실행 시점에 처리된다. 검증 전의 부적절한 `ApprovalRequired`/`CallDeferred`는 별도 오류 경로를 갖는다. “승인부터 받고 나중에 인자를 검사한다”는 그림을 사용하지 않는다.

Tool input은 Pydantic schema validator로 검사한다. JSON Schema는 모델에 전달되는 계약이며 Python이 매번 JSON Schema 문서를 직접 실행해 검사한다고 표현하지 않는다. Tool 함수 return annotation과 최종 `output_type`도 같은 검증 경로로 그리지 않는다. 중간 Tool 결과의 업무 검증은 명시적인 Python 코드로 보여 준다.

`_segment_by_barriers`는 순서를 `[A,B] → [C] → [D,E]`로 분할한다. `_call_tools`는 각 구간을 `asyncio.create_task`로 스케줄하며 결과를 인덱스로 모은다. 정상 완료 이벤트의 노출 순서와 history 조립 순서는 구별한다. 예외·취소 시 `cancel_and_drain`, 이미 완료한 결과 보존, 마지막 인덱스 정렬 경로를 함께 표시한다. 실제 속도 향상 수치를 추정해서 적지 않는다.

### C. Output과 EndStrategy

`output.py`의 공개 Marker → `_output.py`의 `OutputSchema`/Processor → 모델 요청 방식 → 검증/후처리 → 최종화 경로를 연결한다. `ToolOutput`은 미리 Tool schema를 공개하는 방식이다. 모델 응답을 아무 형식으로 받은 뒤 임의로 ToolCall로 바꾼다는 개인 메모의 해석을 보정한다.

`process_tool_calls`는 `_EarlyProcessor`, `_GracefulProcessor`, `_ExhaustiveProcessor`를 선택한다. 소스의 주요 규칙은 다음과 같다.

- early: 출력 Tool을 방출 순서로 검증하고 첫 성공을 선택한다. 모두 실패하면 function tool을 실행할 수 있다.
- graceful: 출력 앞의 function 구간이 완료된 후 output을 검사한다. 실패한 output을 지난 뒤 다음 구간으로 진행할 수 있으므로 “output 뒤 tool은 절대 실행 안 함”으로 단정하지 않는다.
- exhaustive: 여러 호출을 실행하고 유효한 output의 선택 순서는 방출 순서를 따른다. sequential tool은 barrier가 된다.
- graceful/exhaustive에서 function/unknown tool의 retry는 final result를 억제할 수 있다. 이미 `run_stream`에서 확정한 결과 등의 예외는 별도다.

PA28은 유효 Output 사례, PA29는 실패/재시도/stream 예외를 맡는다. 일반 텍스트를 무조건 구조화 final과 동일한 신호로 취급하지 않는다. 네 정책처럼 보이는 불필요한 분류를 추가하지 않는다.

### D. Capability와 Guardrail

`CombinedCapability`는 nested 구성을 정규화하고 정렬·run별 binding을 처리한다. `before_model_request`는 정방향, `after_model_request`는 역방향, `wrap_model_request`는 역방향으로 handler chain을 만든다. **모든 Hook이 단순히 `[A,B]` 순서**라고 쓰지 않는다. get_ordering/active 상태/for_run 복제가 합성에 미치는 효과를 확인한다.

Harness `InputGuardrail.wrap_model_request`는 첫 모델 호출에서 판정한다. 순차 모드와 `parallel=True`를 구분하고, 병렬 모드는 guard와 model을 동시에 시작한 뒤 guard verdict를 먼저 기다리며 취소·정리한다는 코드를 표시한다. 병렬이면 모델로 입력 전송 전 차단을 보장한다고 쓰지 않는다.

`ToolGuardrail.before_tool_execute`는 검증된 인자를 대상으로 판정한다. allow/block/retry/approve/replace 분기를 실제 예외·반환과 대응한다. approve는 `ctx.tool_call_approved`를 확인해 무한 재승인 요청을 피한다. `OutputGuardrail.after_output_process`는 partial output을 건너뛰며, 출력 guard의 approve는 지원되는 일반 승인 동작이 아니다. 방화벽·DB ACL·sandbox는 이 Hook의 자동 제공 범위로 넣지 않는다.

### E. Conversation, Memory, 압축

`Conversation`은 messages뿐 아니라 usage, conversation_id, deferred_tool_requests를 가진다. `message_history=all_messages()`만 이어 붙이는 설명에서 이 차이를 반드시 보완한다. 같은 Agent 객체 재사용을 사용자별 세션 자동복원으로 그리지 않는다.

Harness `Memory`는 기본 `InMemoryStore`이므로 기본 저장의 수명은 프로세스다. `namespace`는 모델 Tool 인자로 받지 않는 scope 설정이다. `for_run`은 scope가 분리된 복제본을 만들고, `before_model_request`는 제한된 snapshot을 최신 사용자 입력 곁의 user-role context로 주입한다. MEMORY.md가 항상 system prompt 전체에 붙는다고 쓰지 않는다. 코드의 기본 한도(max_tokens=2000, max_lines=200 등)는 sources에 버전과 함께 두고 본문에는 핵심 한두 개만 표시한다.

`MemoryToolset`의 write/read/delete/search와 `MemoryStore`를 연결한다. 모델이 쓰기를 선택하는 시점과 앱이 저장 scope·정책을 정하는 시점을 구분한다. Memory 노트 검색과 `ConversationSearchToolset`의 대화 검색/BM25는 별개다. 검색어를 모델이 생성하는 경로와 내부 query normalization/tokenization을 나눠 설명한다.

`SlidingWindowCompaction.before_model_request`는 임계조건 확인 → compact → `ctx.messages[:] = compacted` → 새 요청 context 반환 경로를 갖는다. 압축이 요청용 임시 복사만 바꾼다고 가정하지 않는다. 요약은 별도 모델 비용·정보 손실 가능성을, 원본 저장은 앱의 보존 정책을 보여 준다. 정확한 LOT/snapshot/수치 근거를 무작정 요약에서 재생성하지 않는다.

`Skills.for_run`은 library를 읽고 catalog를 만든 뒤 model-invocable skill을 deferred Capability로 제공한다. 발견·선택·본문 로딩·참고파일 접근·실행은 서로 다른 단계다. 자체 Skill/Capability 작성 기능은 실제 선택 버전의 별도 경로를 추가 확인한 뒤 설명하고, Hermes의 curator와 같은 자동 정리 기능이 있다고 가정하지 않는다.

### F. 위임과 관측

`SubAgentToolset`은 delegate tool을 등록하고 fresh child run으로 작업을 보낸다. 자식은 부모 대화를 그대로 받지 않으며 deps forwarding, usage 공유, tool 상속, shared_capabilities는 설정별로 설명한다. 코드 위임·앱 handoff·사용자 Graph·Harness delegate를 단일 기능명으로 합치지 않는다.

`Instrumentation.wrap_run`, `wrap_model_request`, `wrap_tool_execute`, `wrap_output_process` 및 validation error hook을 trace map에 연결한다. Trace는 observability이고 durable checkpoint/감사 기록 전체를 대체하지 않는다. Logfire만 가능한 것처럼 설명하지 않으며 실제 exporter·내용 수집·redaction 설정을 후속 검증한다. `TestModel`/`FunctionModel` 테스트와 Evals 품질 평가의 대상도 구분한다.

## 5. 개발 범위: 어느 수준까지 코드를 작성할 것인가

모든 단계에서 같은 합성 LOT/snapshot 데이터를 쓴다. 모델은 자료 조회·가설·설명을 맡고, 수율 계산과 권한·승인 여부는 결정적 코드가 맡는다. 이 설계는 학습용 앱 예시다.

| 수준 | 작성할 파일·함수(앱 코드) | 프레임워크에 맡길 부분 | 완료 기준 |
|---|---|---|---|
| A. 최소 실행 | `agent.py`: Agent·지침·Output; `tools.py`: 조회 함수; `models.py`: 출력 타입; 모델 접속 설정 | 모델/Tool 반복·스키마 생성·인자/출력 검증·결과 반환 | 합성 조회 1개와 유효한 결과, 잘못된 인자 피드백까지 재현 |
| B. 재사용 업무 Agent | `deps.py`: tenant/snapshot/DB; `validators.py`: 계산·근거 대조; `policy.py`: 반복 정책; `conversation_store.py`: save/load; `approval.py`: pending/resolve; `tests/` | RunContext 전달·Hook·typed feedback·Conversation 직렬화·Deferred 프로토콜 | 교차권한 차단·다음 Run 연결·보고서 변경 시 이전 승인 거부·한도 소진 재현 |
| C. 필요한 Harness 기능 | `harness_config.py`: Memory/Store/Skills/compaction/Subagents 구성; 검수된 SKILL.md·workspace·scope | 제공된 Capability·Toolset·압축 전략·저장소 구현·자식 Run | Core-only 대비 추가 Tool/Context와 상태 변화 관찰 |
| D. 서비스 연결 | 인증 API·요청 라우팅·저장소 충돌 처리·승인 화면/CLI·작업 상태·취소·로그 exporter·운영 설정 | 공개 run/stream·통합 인터페이스 사용 | 서비스 요구에 맞는 별도 운영 검증; 실제 구축·회고는 3차 |

개발량을 임의의 코드 줄 수로 확정하지 않는다. A는 작은 실행 예제로, B는 업무 계약을 갖춘 구조로 보여 주되 인증 서버·결재 UI·분산 큐 전체를 2차에서 제작하지 않는다. 최소한 Loop 재구현은 필요 없지만 Tool의 실제 데이터 접근·계산·권한 코드는 작성해야 한다는 점을 코드로 입증한다.

### PA04·PA15·PA27에 나눠 보여 줄 사용자 코드 초안

아래는 실제 공개 API를 사용한 **후속 구현용 앱 코드 초안**이며 현재 실행 완료 코드가 아니다. 모델 객체는 호출자가 구성해 넘긴다. 검증 실패 재요청과 일반 업무 예외를 구분하며, 결과 숫자는 앱이 보유한 같은 snapshot으로 재계산한다.

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext

@dataclass
class Deps:
    allowed_lots: set[str]
    snapshot: str
    counts: dict[str, tuple[int, int]]

class YieldReport(BaseModel):
    lot_id: str
    snapshot: str
    yield_pct: float = Field(ge=0, le=100)

def build_agent(model):  # 앱이 정의한 factory
    agent = Agent(model, deps_type=Deps, output_type=YieldReport, retries=2)

    @agent.tool
    def read_counts(ctx: RunContext[Deps], lot_id: str) -> dict:
        if lot_id not in ctx.deps.allowed_lots:
            raise PermissionError('조회 범위 밖 LOT')
        good, total = ctx.deps.counts[lot_id]
        return dict(lot_id=lot_id, snapshot=ctx.deps.snapshot,
                    good=good, total=total)

    @agent.output_validator
    def verify(ctx: RunContext[Deps], out: YieldReport) -> YieldReport:
        if out.lot_id not in ctx.deps.allowed_lots:
            raise PermissionError('결과의 LOT도 인가 확인')
        good, total = ctx.deps.counts[out.lot_id]
        if total <= 0:
            raise ValueError('분모가 유효하지 않은 fixture')
        expected = 100 * good / total
        if out.snapshot != ctx.deps.snapshot or abs(out.yield_pct - expected) > 0.01:
            raise ModelRetry('동일 snapshot의 good/total로 다시 계산하세요.')
        return out

    return agent
```

예제의 데이터는 서버가 만든 합성 fixture이며 클라이언트가 allowed_lots를 마음대로 정하는 구조로 구현하지 않는다. Tool에서 데이터가 없거나 계산 불가능한 사례도 별도 실패 테스트로 둔다. `retries=2`가 모든 HTTP 요청의 총 재시도 횟수라고 설명하지 않는다. 출력 다형성은 PA26에서 별도 예제로 보여 주어 위 보고서 전용 예제의 목적과 범용 Agent의 가능성을 구분한다.

## 6. Demo·검증 준비 계획

현재 Demo 안내 화면을 실제 구현으로 교체하는 것은 후속 작업이다. 라이브 화면은 **앱 코드 → 모델로 보낸 schema/메시지 → Node/Tool 이벤트 → 최종 검증/Trace**를 연결하되 숨겨진 추론을 표시한다고 주장하지 않는다. 실모델은 실제 사용감을, 고정된 FunctionModel 응답은 분기 비교를 담당한다.

| ID | 재현할 사례 | 관찰값과 통과 기준 | 대응 |
|---|---|---|---|
| D1 | 무Tool 정상 종료 / 조회 Tool 1회 / 3-step 수정 흐름 | Node·모델 요청·실제 Tool 실행 횟수와 history가 서로 대응 | PA06–12 |
| D2 | missing arg·타입 오류·unknown/unavailable Tool | 함수 본체 미실행, validation 결과·feedback·retry 한도 표시 | PA18–22 |
| D3 | schema 통과 수치 오류·정상 수정·예산 소진 | 업무 validator에서 거부, 같은 fixture 계산과 비교, 최종 실패도 표현 | PA25–30 |
| D4 | 독립 온도/압력 병렬 vs 의존 조회·barrier | 완료순서 변경에도 기록 대응; snapshot 불일치가 후속 계산에서 거부 | PA23 |
| D5 | [조회, 유효/무효 Output, 기록용 배포 Tool] 고정 응답 | 3종 EndStrategy 실행 로그, retry-wins/stream commit 예외; 외부 배포 없음 | PA28–29 |
| D6 | Capability A/B와 guard block/replace/retry | before/after/wrap 실제 순서·미실행 Tool·설정 충돌 확인 | PA31–34 |
| D7 | inline/승인 대기 후 재개·거절·초안 수정 | Conversation·call ID·args·version 일치, 중복/위조/만료 승인 거부 | PA35–37 |
| D8 | Core history → Harness Memory → compaction | 모델 입력 전후 diff·namespace·원본/history 변경 범위, 프로세스 재시작 시 Store 수명 | PA16–17,39–43 |
| D9 | 자식 Agent·Trace·Evals | 자식 history/deps/usage 계약, 부모결과 복귀, trace span 연결, 고정 정답 평가 | PA46–50 |

기존 접속 계약을 유지한다. **Codex용 Demo는 10000, Antigravity용 Demo는 10001**로 모델 요청을 보낸다. 이는 두 Demo에 서로 다른 포트를 임의 배정하는 뜻이 아니다. Agent는 vLLM/OpenAI-compatible endpoint만 알고, 현재 PC의 별도 프록시가 OpenAI 변환과 실제 API key를 관리한다. 이관 PC는 같은 endpoint 계약으로 실제 vLLM에 연결한다. 포트 뒤 서비스 탐지나 OpenAI key를 Demo에 넣지 않는다. Provider native-only 기능을 필수 성공 경로로 잡지 않는다.

모든 live 요청은 실제 모델 ID·기능 profile·Tool/Output/stream 지원을 확인한 후 실행한다. 고정 응답 시험은 네트워크 없이 동작하게 구성한다. 설치와 실모델 호출은 이 계획 작성 중 수행하지 않았다.

## 7. 개인 질문·코멘트 반영표

`PA` 접두사를 생략한 숫자는 해당 본문 장표 ID다. 질문을 통합한 경우에도 원문 의문과 판정 기준은 아래에 남긴다. 단순 미지원 추측은 사실로 발표하지 않는다.

| 질문 ID | 개인 정리·질문·보강 포인트 | 장표 | 반드시 담을 답변/확인 |
|---|---|---|---|
| Q01 | Pydantic이 무엇인가 | 01 | 기초를 짧게 정의하고 실제 Field 검증 1회 |
| Q02 | 어느 코드까지 작성해야 Agent가 되는가 | 03–05,51–52 | 최소/업무/서비스 3단계와 파일·함수 계약 |
| Q03 | 교재 코드가 실제 문법인가; 가상 함수 대신 실함수 유지 | 전체 | 실제 API/내부 발췌/앱 코드/의사코드 표시와 후속 실행 검증 |
| Q04 | run_sync, run, run_stream, run_stream_events, iter 차이 | 06–12 | 제어·반환·stream commit·정리 비교 |
| Q05 | Instructions/System Prompt/DI가 어떻게 전달되나; 모델별 차이 | 13–15 | 메시지/파라미터/deps와 adapter payload 대조 |
| Q06 | tool과 tool_plain: 언제·왜 쓰나 | 18–19 | ctx 인자 유무와 async 여부를 별도 축으로 |
| Q07 | Tool 실행은 Thread인가; 여러 Call은 어떻게 실행되나 | 21–23 | task/sync offload/barrier/결과순서/취소 |
| Q08 | Toolset 내부와 개발자 구현 수준 | 18–24 | get_tools/call_tool, 노출 필터·실행 인가 구분 |
| Q09 | 현재 Retry 목록이 전부인가 | 11,29–30 | Tool/Output/SDK/transport/fallback/App 계층과 설정 근거 |
| Q10 | 매 Run 이전 이력을 넣나; 자동 Session은 없나 | 16–17 | message_history 또는 Conversation을 caller가 전달; 객체 재사용만으로 세션 복원 아님 |
| Q11 | 직렬화만 제공하나; 메타데이터·저장·압축 책임 | 16–17,39–45 | Core 표현, Harness 기능, 앱 저장/권한/수명주기 분리 |
| Q12 | LangGraph를 쓰나; Graph 이름만 같은가 | 07,46 | 내부 pydantic-graph와 별도 사용자 Graph의 관계 |
| Q13 | Loop Node별 실제 세부 구현 | 06–11 | 호출자→입력→변경 State→분기→다음 Node |
| Q14 | Hook 사용법; 반도체 업무에서는 어떻게 쓰나 | 31–34 | LOT인가·결과 마스킹·지연 측정, 적용 지점과 우선순위 |
| Q15 | Capability가 무엇이고 합성이 어떻게 되나 | 31–33 | 정렬/flatten/for_run/before/after/wrap 실코드와 충돌 |
| Q16 | Capability로 구현하는 게 일반적인가; 추천 개발 구조인가 | 31–33,51 | 다른 프레임워크의 hook 개념과 구별; 재사용 정책이면 유리, 작은 Tool은 직접 구현 판단 |
| Q17 | Memory는 직접 설계하나; 어느 수준까지 추상화되나 | 38–41 | 기존 Store/Tool/주입 사용 + namespace/데이터/갱신 정책 작성 |
| Q18 | sliding/summarization/tool clearing을 직접 구현하나 | 42 | Harness 전략 재사용 가능, 정책·한도·원본/정확성 계약은 앱 결정 |
| Q19 | Skill과 MCP는 어디까지 제공; 사용자 코드 수준 | 24,43–44 | Skill library/workspace 설정 vs MCP 서버/client/auth, 실제 호출 경로 |
| Q20 | delegation=agent-as-tool인가; handoff와 같은가 | 46 | 부모복귀/앱 제어권/SDK 고유 handoff API를 구별 |
| Q21 | orchestration/delegation/graph/subagents/advisor 사용·내부 | 46–48 | 각 패턴별 입력·자식 상태·예산·결과 통합 코드 |
| Q22 | Core로 직접 개발 가능; Harness는 선택 패키지인가 | 02–05,38,51 | Core-only 예제 후 선택 기능 추가, 버전 각각 고정 |
| Q23 | Harness 핵심 기능들의 내부 로직 | 38–48 | Memory/검색/압축/Skills/작업환경/StepPersistence/위임 추적 |
| Q24 | requires_approval=True이면 UI는 누가 만드나; 평생 멈추나 | 35–37 | 조건 충족 구성에서 Deferred 결과 반환/inline handler/CLI; 후속 응답 없으면 미해결 상태 |
| Q25 | 승인 주체·위임 방지·재개 권한 재검사 의미 | 35–37 | 원본 call/args/보고서버전/승인자 server-side binding; 수정·만료·위조 사례 |
| Q26 | 타입검증 외에 PydanticAI를 채택할 실구현 이점 | 05–12,20–21,28–33,37,51 | Loop/manager/executor/typedfeedback/합성/재개를 직접 구현할 비용과 교환 |
| Q27 | 설치해서 Demo해도 되나 | 03,50–52 | 격리 env·버전 pin으로 후속 구현; 이번 작업은 계획 작성, 실제 설치·호출 미수행 |
| Q28 | output_type 고정이면 범용 Agent 불가; Tool return만 검증하는 게 낫나 | 25–27 | 최종 계약/중간 반환 별개; str·복수 출력·override와 도구 결과 검증 보완 |
| Q29 | ToolOutput을 받은 뒤 ToolCall로 해석하는가 | 25 | 미리 output tool schema를 모델에 전달하고 해당 Call을 검증 |
| Q30 | NativeOutput은 공급자 기능인가; Prompted 위반 시; Text 후처리 | 25–27 | provider 요청/로컬 파싱·validation/retry/text callback 경로 대조 |
| Q31 | 모델에 Tool이 어느 정도 공개되는가 | 13,18,20 | name/description/schema와 Python 본체·비밀 deps 비노출 |
| Q32 | 일반 Function/Native Tool이 모두 Toolset으로 실행되나 | 24 | 개인 흐름 문서 표현 보정: provider-native는 호스트 FunctionToolset dispatch와 다름 |
| Q33 | Node Demo: 무Tool/잘못된인자/정상Output; 실모델과 mock 차이 | 08,50,52 | 코멘트 1, D1·D2·D3 |
| Q34 | 같은 LOT·snapshot의 독립 조회와 선행결과 의존 조회 | 22–23,50,52 | 코멘트 2, 완료순서/버전 불일치 D4 |
| Q35 | EndStrategy는 부작용 정책; invalid/ModelRetry/stream 예외 | 28–29,52 | 코멘트 3, 실제 배포 없는 기록용 Tool D5 |
| Q36 | 즉시 코드판정 vs 엔지니어 판단; 초안수정 후 이전승인 | 35–37,52 | 코멘트 4, 보고서version 바인딩 D7 |
| Q37 | 메모리 구현별 실제 Context·compaction 시각화 | 39–43,52 | D8 전후 입력 diff와 원본 저장 구분 |
| Q38 | 모델 연결 Demo의 10000/10001 계약 | 13,24,52 | Codex10000/Antigravity10001, 프록시 뒤 서비스·키는 Demo에서 알 필요 없음 |
| Q39 | Guardrail 기본/적용 수준과 Trace 실제 코드 | 34,49–50 | Core 기본검증과 선택 Guardrail·Instrumentation 활성화 분리 |

### 심층 자료 전체 범위 대조

| 기존 자료 범위 | 반영 위치 | 편집 판단 |
|---|---|---|
| 기본 §1–10 / 심층 §1–10 | PA01–22,25–30 | 기초 정의는 줄이고 실제 코드·요청·실패 경로 확대 |
| 심층 §11–16 | PA23,25–37 | 병렬·Output·Retry·Deps·Capability·승인에 집중 |
| 심층 §17–19 | PA13–17,24,38–45 | Core 대화 관리 먼저, 선택 Harness 내부는 뒤에서 연결 |
| 심층 §20–23 | PA11–12,34–37,45–50 | 위임·Stream·보안·장애·복구 책임을 관련 장표에 배치 |
| W1–W9 | W1 PA06, W2 PA13–16, W3 PA18–22, W4 PA28–29, W5 PA23, W6 PA25–27, W7 PA35–37, W8 PA31–34, W9 전체 sources | 각 소스 추적의 호출자·입력·State·분기·부작용을 작성 |
| F01–F24 | D1–D9 및 각 장표 sources 실패 사례 | 24개를 본문에 나열하지 않고 해당 분기의 검증 fixture로 유지 |
| 기본 §27–28 반도체 사례/체크리스트 | 동일 LOT/snapshot 예제, PA15·22·27·33·37·51 | 사례를 여러 Agent 이야기로 분산하지 않고 동일 데이터 계약 재사용 |
| 비교·복습·용어·공식 출처 | PA02·05·46·51, sources | 여러 SDK의 미확인 구현을 단정하는 비교는 제외, 학습 질문은 보존 |
| 개인 실무 코멘트 1–4 | PA08 / PA23 / PA28–29 / PA35–37 | 네 항목 모두 본문 + Demo + 3차 검증 질문 반영 |

## 8. 후속 작성 순서와 완료 기준

1. **API·코드 확정:** 아래 출처 인덱스의 고정 소스에서 각 장표 심볼·분기를 연결한다. 이번에 세부를 아직 읽지 않은 provider adapter·Workspace/Shell/Planning·자체 확장·DynamicWorkflow/Advisor 상세는 추가 추적한다. 이름만으로 내부를 추측해 채우지 않는다.
2. **작은 실행 예제:** 격리 환경에서 Core 2.61.0과 필요 시 Harness 0.61.0 및 provider extra를 lock한다. 공개 API 예제 import·decorator·serialization·type/output 구성·FunctionModel 응답을 실제 실행한다. 내부 메서드를 업무 코드에서 직접 호출하지 않는다.
3. **실행 관찰:** D1–D9 중 기본 Graph/Tool/Output/EndStrategy/승인/Memory 경로를 결정적으로 재현한다. 실모델의 출력 재현성과 프레임워크 분기 재현성을 구별한다. 생성된 schema/payload/history/trace를 장표 근거로 저장한다.
4. **발표 내용 작성:** PA01–52와 PAD01–08로 쪼개고 sources의 개념 설명·실함수·예외·앱 책임을 완성한다. 현재 S20–S38의 내용은 아래 대응대로 통합한다. blueprint·발표 흐름·notes·manifest를 최종 구현에 맞춰 함께 갱신한다.
5. **검수:** 실제 코드 여부·버전·질문 Q01–Q39·워크북 W1–W9·네 코멘트와 본문을 대조한다. 데스크톱/작은 화면에서 코드·화살표·텍스트 넘침·강조 대비·sources 읽기·구분 장표·키보드 흐름을 검수한다.

| 현재 장표 | 후속 장표 |
|---|---|
| PYDANTIC, S20–S22 | PA00–05 |
| S23–S24 | PA06–15 |
| S25–S26 | PA18–24 |
| S27–S29 | PA25–30 |
| S30 | PA31–34 |
| S31–S33 | PA16–17,39–42,45 |
| S34 | PA24,43–44 |
| S35 | PA46–48 |
| S36 | PA35–37 |
| S37–S38 | PA38,49–52 |

완료 판정은 장수보다 다음 조건을 따른다.

- 개발자 코드와 프레임워크 내부 코드의 경계가 모든 핵심 사례에서 보인다.
- 추상 API마다 최소 한 개의 실제 호출 경로·상태 변화·실패 분기가 연결된다.
- 최종 Output, 중간 Tool 결과, 승인된 업무 실행, Trace가 서로 다른 계약임을 설명한다.
- 개인 질문 전부가 본문/소스 설명/실험 계획 중 하나 이상에 연결되고, 불확실한 부분은 미검증으로 남는다.
- 발표 화면은 읽을 수 있는 양을 유지하며 상세 내용은 분할·sources로 이어진다.
- 3차에 남길 운영 검증은 서버 인증·실제 DB/승인 화면·부하/성능·실장애 복구이며, 2차에는 그 경계와 필요한 코드 계약을 설명한다.

## 9. 공식 자료와 소스 인덱스

소스는 위 고정 commit을 대상으로 직접 받아 Python AST로 실제 심볼·행을 확인했다. 다운로드한 원본은 작업용 scratch에 두고 저장소에는 [경로·hash·심볼 인덱스](../research/pydanticai-plan-sources.json)만 둔다. 공식 자료는 아래와 같다.

- [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/) · [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/) · [Output](https://pydantic.dev/docs/ai/core-concepts/output/)
- [Advanced tools](https://pydantic.dev/docs/ai/tools-toolsets/tools-advanced/) · [Toolsets](https://pydantic.dev/docs/ai/tools-toolsets/toolsets/) · [Deferred tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/)
- [Capabilities](https://pydantic.dev/docs/ai/capabilities/overview/) · [Harness](https://pydantic.dev/docs/ai/harness/) · [Harness 0.61.0 배포 메타데이터](https://pypi.org/pypi/pydantic-ai-harness/0.61.0/json)
- [Memory](https://pydantic.dev/docs/ai/harness/memory/) · [Skills](https://pydantic.dev/docs/ai/harness/skills/) · [Compaction](https://pydantic.dev/docs/ai/harness/compaction/) · [Guardrails](https://pydantic.dev/docs/ai/harness/guardrails/)
- [Observability](https://pydantic.dev/docs/ai/integrations/logfire/) · [Testing](https://pydantic.dev/docs/ai/guides/testing/) · [Durable execution](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/)

온라인 문서는 조사 시점에도 경로·API가 바뀔 수 있다. 실제 발표 코드의 기준은 고정 소스이며, 링크 상태와 최신 문서 차이는 구현 직전에 재확인한다. 실제 구현에서는 graceful이 유효한 O1 뒤의 B도 실행하는 것을 고정 응답으로 확인해 PA28에 반영했다. 검증 스크립트는 Core 2.61.0과 Harness 0.61.0 환경에서 실행할 수 있다. [검증 스크립트](../verify-pydantic-examples.py)
