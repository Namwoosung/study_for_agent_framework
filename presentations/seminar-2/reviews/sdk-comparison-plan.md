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
