# 2차 세미나 — 발표자 전용 노트

## S00 — Agent Framework 세부 구조

## Agent Framework 세부 구조

### 주요 개념

**Agent Framework**: 모델 호출, 도구 실행, 상태 관리 등 Agent를 구성하고 실행하는 기능을 제공하는 소프트웨어입니다.

### 설명

이번 세미나는 공통 개념을 배운 1차에 이어 실제 기술의 세부 구조를 살펴봅니다. 이 발표에서는 Hermes와 PydanticAI를 중심으로 실행 흐름과 상태 관리 방법을 설명하고 Claude Code와도 비교합니다.

### 발표 포인트

Hermes · Claude Code · PydanticAI

### 화면 읽기

발표의 공통 질문은 누가 모델을 호출하고, 도구 실행을 허용하고, 실행 상태를 저장하는가입니다.

### 적용 예와 확인할 경계

반도체 검사 요청을 예로 듭니다. 불량률을 설명하는 것과 보고서를 발행하는 것은 서로 다른 실행 결과입니다.

## S01 — Agent Framework의 구성

## Agent Framework의 구성

### 주요 개념

**Runtime / Harness**: 모델 호출과 Tool 실행을 반복하면서 상태, 종료 조건, 권한을 관리합니다.

**Context Builder**: 지침, 현재 상태, 대화 이력, 필요한 기억을 모아 모델 입력을 구성합니다.

**Guardrails / Trace**: 실행 전후의 검사·승인과 실행 기록을 뜻합니다. 각 기능이 적용되는 지점은 구현에 따라 다릅니다.

### 설명

사용자 목표와 지침을 바탕으로 Runtime이 Context를 준비하고 모델을 호출합니다. 모델이 Tool을 요청하면 Runtime이 실행 조건을 확인하고 도구를 통해 환경에 접근합니다. 결과는 상태와 다음 Context에 반영됩니다. 도식은 특정 제품의 호출 순서를 복제한 것이 아니라 이번 발표의 공통 구성도입니다.

### 발표 포인트

각 기술이 이 구조를 어떻게 구현하는지 살펴봅니다.

### 화면 읽기

사용자 요청은 Harness가 받아 지시·상태를 조합합니다. 모델의 Tool Call은 실행 요청이고 결과는 다시 모델 입력으로 들어갈 수 있습니다.

### 적용 예와 확인할 경계

Context Builder, Memory Store, Guardrail, Trace는 역할을 설명하기 위한 이름입니다. 제품마다 배치와 분리 수준은 다릅니다.

## S02 — 2차 세미나 진행 계획

## 2차 세미나 진행 계획

### 주요 개념

**모델 개발·서빙**: AI Studio, vLLM, SGLang을 다루는 파트입니다.

**Agent 개발·워크플로**: DeepAgents, LangChain, LangGraph를 다루는 파트입니다.

**Agent Harness·SDK**: Hermes, PydanticAI, OpenAI, Claude 관련 기술을 다루는 파트입니다.

### 설명

1차 세미나의 개념을 바탕으로 세 파트가 각 기술의 세부 사항을 설명합니다. 담당자는 위에서부터 강준혁, 박건, 남우성입니다. 이번 발표는 세 번째 파트이며 실제 개발, 검증과 회고는 3차에서 진행합니다.

### 발표 포인트

3차에서는 직접 개발하고, 결과를 검증하며 회고합니다.

### 화면 읽기

서빙, Agent 구성, Harness·SDK 세 발표의 순서입니다. 단계에서 각 범위 담당자가 나타납니다.

### 적용 예와 확인할 경계

2차에서는 실행 경로를 읽고 비교합니다. 실제 업무 개발과 검증 결과는 3차에서 이어집니다.

## S03 — Agent Harness와 SDK

## Agent Harness와 SDK

### 주요 개념

**Agent Harness**: CLI, 도구, 세션 등 갖춰진 Agent 실행환경에서 시작합니다. 여기서는 Hermes와 Claude Code를 묶었습니다.

**Agent SDK**: 개발자가 Agent, Tool, 실행 조건을 코드로 정의하고 애플리케이션에 연결하는 출발점입니다.

### 설명

Harness와 SDK는 배타적인 제품 분류가 아닙니다. Hermes의 프로그래밍 통합이나 PydanticAI의 선택적 Harness처럼 기능이 겹칠 수 있습니다. 이 장은 발표를 위한 두 출발점을 보여주며, Hermes와 PydanticAI를 각 행의 주요 설명 대상으로 강조합니다. 다른 SDK는 이름과 편집 위치만 표시하며 기능 비교가 완료됐다는 뜻은 아닙니다.

### 발표 포인트

Hermes와 PydanticAI를 중심으로 살펴봅니다.

### 화면 읽기

위 행은 사용자에게 실행환경을 제공하는 제품, 아래 행은 개발자가 앱에 연결하는 SDK입니다.

### 적용 예와 확인할 경계

Hermes와 PydanticAI를 각 계층의 중심 사례로 봅니다. 제품이 SDK를 제공하거나 SDK에 선택형 Harness가 있어도 이 장의 비교 단위는 그대로입니다.

## S03H — Hermes

## Hermes

### 주요 개념

**AIAgent**: 모델 요청과 Tool 실행을 이어가는 Hermes의 Agent Runtime입니다.

**Session / Memory / Skills**: 대화 기록, 지속 사실, 재사용 절차를 서로 다른 방식으로 보관하고 사용합니다.

### 설명

CLI나 Gateway 등에서 들어온 요청은 AIAgent로 이어집니다. Prompt를 구성해 모델을 호출하고, 필요한 Tool을 실행한 뒤 결과를 다시 모델에 전달합니다. 이 과정에서 세션, Memory, Skills를 사용합니다. 왼쪽은 대표 관계를 단순화한 전체 구조도이며 이후 장표에서 각 부분을 나누어 설명합니다.

### 발표 포인트

전체 구조를 먼저 보고, 각 기능의 동작을 살펴봅니다.

### 화면 읽기

Hermes를 단독 모델 호출기가 아닌 여러 입력 경로와 상태, 도구를 운영하는 Harness로 소개합니다.

### 적용 예와 확인할 경계

먼저 한 요청이 끝나는 과정부터 보고, 같은 흐름에서 기억·승인·위임이 어디에 끼어드는지 확인합니다.

## S04 — Hermes 내부 구성과 설명 순서

## Hermes 내부 구성과 설명 순서

### 주요 개념

**범용 Agent Harness**: 모델 호출뿐 아니라 도구 실행, 이력·지식 관리, 작업 제어를 제공하는 실행환경입니다.

### 설명

제품 기능 전체를 다시 나열하는 장표가 아니라 이번 Hermes 본편의 설명 범위입니다. Gateway·API 운영 구조는 요청에 따라 제외했습니다. CLI/TUI/Desktop 등의 입력 표면이 있다는 사실과 상세 운영 아키텍처를 강의하는 것은 구분합니다.

### 발표 포인트

실행 흐름을 먼저 보고, 입력·도구·상태·확장 기능을 차례로 확인합니다.

### 화면 읽기

섹션 이름은 기능을 읽는 순서입니다. 실행 루프에서 시작해 입력, Tool, 실행 제어, 예약으로 넘어갑니다.

### 적용 예와 확인할 경계

예를 들어 승인 규칙은 Tool 실행에 연결되고, Trace는 이 단계들이 실제로 지나간 순서를 관찰하는 별도 경계입니다.

## S05 — 사용자 요청 한 건의 실행 과정

## 사용자 요청 한 건의 실행 과정

### 개념

**Turn**: 사용자 입력 한 건을 처리하는 실행 단위입니다. 여러 모델·Tool 호출을 포함할 수 있습니다.

**Agent Loop**: 모델 응답을 분류하고 Tool 실행, 다음 호출, 종료를 결정합니다.

**Provider Adapter**: 내부 메시지·도구 정의를 선택한 API의 요청 형식으로 바꿉니다.

### 설명

입력과 Task를 준비한 뒤 지침·대화 이력·Tool schema를 모아 모델을 호출합니다. Tool Call이 있으면 Runtime이 검증과 실행을 거쳐 결과를 이력에 추가하고 다음 모델 호출로 이어갑니다. 최종 답변이면 Turn을 정리하고 세션을 저장합니다.

사용자 중단, 실행 예산, API 오류, 잘못된 응답 등은 각각 다른 분기입니다. Tool 결과를 보고 다음 행동을 고르는 정상 반복과 통신 retry를 구분합니다. 압축용 보조 호출이나 자식 Agent 호출도 사용자 요청 수와 별도로 세어야 합니다. 모델의 최종 답변이 업무의 정확성을 보장하지는 않습니다.

### 발표 포인트

사용자 요청 수와 모델 호출 수는 다릅니다.

### 설명 순서

전체 흐름을 먼저 한 번 따라간다. 이후 장표는 이 흐름의 Context, Tool, 저장, 확장 부분을 차례로 확대한다.

### 학습자료 근거

심층 학습 §3·4; 기초 학습자료 및 추가 코멘트와 대조. 구현 설명·문서 설명·업무 설계 제안을 구분한다.

### 화면 읽기

한 Turn 안에서 모델 요청은 여러 번 일어날 수 있습니다. Tool Call이 오면 런타임이 실행하고 결과를 다음 요청에 연결합니다.

### 적용 예와 확인할 경계

A17 조회를 제안한 메시지와 42/1000을 반환한 Tool 메시지를 구분합니다. 외부 조회의 실행 주체는 Tool입니다.

## HLOOP — Hermes는 언제 다시 모델을 부를까?

## Hermes는 언제 다시 모델을 부를까?

**① 들어갈 조건 확인** — 준비 단계가 중단되지 않았고 횟수와 예산이 남거나 정리 호출이 허용됨

**② begin_iteration** — 중단 플래그를 확인한 뒤 호출 번호를 올리고 예산 한 회를 사용

**③ prepare_iteration** — 이번 반복의 메시지와 상태를 준비

**④ assemble_api_request** — 메시지와 도구를 공급자 요청 형식으로 조립

**⑤ run_preflight_gate** — 보내기 직전 검사. 결과에 따라 전송 전 종료하거나 다음 반복으로 이동

**⑥ announce_api_call** — 모델을 호출하기 전에 진행 상황을 알림

prelude_ok, calls, remaining, grace_call은 지면용 이름입니다. 원래 조건은 _prelude_action != "break" and ((s.api_call_count < agent.max_iterations and agent.iteration_budget.remaining > 0) or agent._budget_grace_call)입니다. phase 결과 분기는 생략했습니다.

### 화면 읽기

루프 조건과 begin_iteration을 순서대로 읽습니다. 진입 조건을 통과해도 요청 직전 검사에서 종료되거나 다음 반복으로 넘어갈 수 있습니다.

### 적용 예와 확인할 경계

예산 한 회를 소비하는 지점과 실제 전송은 별도입니다. 모델 통신 재시도는 다음 장의 내부 루프에서 확인합니다.

## HTRACE — 모델 응답을 받고 루프를 잇는 코드

## 모델 응답을 받고 루프를 잇는 코드

**① _run_api_retry_loop** — 모델 응답을 얻는 구간. 통신 재시도는 이 호출 내부에서 처리

**② apply_retry_restarts** — 모델 전환 등으로 요청을 다시 준비해야 하면 바깥 루프로 돌아감

**③ normalize_model_response** — 받은 응답을 공통 메시지로 정리해 도구 호출 목록을 읽을 수 있게 함

**④ run_tool_round** — 예: A17 조회 → 반환값을 이력에 추가 → 다음 모델 요청이 그 값을 읽음

**⑤ finish_text_response** — 도구 호출이 없으면 텍스트 종료 경로. 응답 상태에 따른 예외 분기는 Sources 참고

원본은 두 handler를 조건식으로 골라 _run_phase에 넘깁니다. Tool 분기도 승인 대기나 종료 같은 상태를 반환할 수 있고 텍스트 분기에도 복구·연장 조건이 있습니다. SDK의 네트워크 재시도는 외부 반복 카운터와 별개입니다.

### 화면 읽기

응답을 표준 메시지로 바꾼 다음 도구 목록 유무에 따라 실행 경로를 고릅니다.

### 적용 예와 확인할 경계

A17 도구 반환이 이력에 들어가면 다음 모델 호출이 42/1000을 읽습니다. 모델 교체 때문에 요청을 다시 조립하는 분기는 이 업무 반복과 구분합니다.

## HEXIT — 루프가 멈추는 세 가지 이유

## 루프가 멈추는 세 가지 이유

**중단** — 새 호출 전에는 중단 표시를 확인. 호출 중 InterruptedError는 별도로 처리.

**호출 예산 소진** — max_turns 기본 null. 설정된 상한을 소진하면 조건부 정리 호출만 허용.

**모델 요청 오류** — api_max_retries 기본 3. 원인에 따라 재시도·대체 모델·실패 처리.

기본값은 hermes_cli/config_defaults.py 기준입니다. 3은 Hermes 내부 재시도 루프의 상한이며 최초 호출 외에 항상 세 번 더 요청한다는 뜻이 아닙니다. SDK 재시도는 별도입니다. finalize_turn은 루프 종료 후 정리하며 일부 조기 반환 경로는 따로 있습니다.

### 화면 읽기

중단 표시는 새 호출 전에 읽고, 호출 중 인터럽트와 통신 예외는 각 처리 경로에서 다룹니다.

### 적용 예와 확인할 경계

max_turns 기본 null과 api_max_retries 기본 3은 서로 다른 제한입니다. 이미 외부에 쓴 값은 Turn 종료만으로 되돌아가지 않습니다.

## HCTX — 시스템 프롬프트에는 무엇이 들어갈까?

## 시스템 프롬프트에는 무엇이 들어갈까?

기본 지시 — SOUL · 모델/도구 안내 · 고정 Skill

작업 환경 — 프로젝트 규칙 · workspace · 호출자 지시

기억과 확장 — Skills 목록 · MEMORY/USER · 외부 Memory

환경에 따른 정보 — Plugin · 프로필 · 시간 · 실행 환경

환경과 설정에 따라 블록은 생략됩니다. 소스의 stable/context/volatile 조립 순서와 역할별 분류는 별개입니다.

### 화면 읽기

네 블록은 정체성, 작업 환경, 기억, 환경 정보를 역할별로 묶어 놓은 것입니다.

### 적용 예와 확인할 경계

어떤 프로젝트 파일을 읽었고 어떤 Memory를 가져왔는지는 설정과 세션마다 다릅니다. 그림의 카드 순서를 직렬화 순서로 읽지 않습니다.

## S07 — 모델 입력과 Session·Memory의 관계

## 모델 입력과 Session·Memory의 관계

### 주요 개념

**System snapshot**: 정체성·지침·Skills·Memory·외부/Plugin·런타임 정보를 구성하며 조건에 따라 생략됩니다.

**Session과 Memory**: Session은 이력, Memory는 snapshot의 지속 사실을 공급합니다.

**최종 payload**: 이력·호출별 정보·tools와 API 옵션을 Provider 형식으로 변환한 결과입니다.

### 설명

system_prompt.py의 실제 assemble 계층을 대조했습니다. stable에는 identity, Tool/모델 안내, pinned auto-load와 coding 지침이 들어가고 context에는 system_message·프로젝트 파일·workspace snapshot·operator/platform 안내가 들어갑니다. volatile에는 Skills 인덱스와 built-in/외부 Memory, Plugin after_memory 섹션, profile/time/environment가 구성됩니다. 모든 블록이 항상 활성화되는 것은 아닙니다.

공식 Prompt Assembly 문서에는 Skill 인덱스 위치가 서로 다르게 적힌 부분이 있으므로 이 도식은 논리 역할을 보여주고 순서는 고정 소스를 기준으로 설명합니다. 대화 메시지에는 텍스트 외에 미디어·추론·도구 메타데이터가 있을 수 있고 API 모드에 따라 표현이 다릅니다. 이 그림은 바이트 단위 전체 payload 명세가 아닙니다. 실제 조립 결과는 Demo에서 adapter 전후 JSON으로 확인합니다. 세션 중 Memory 파일 변경만으로 snapshot이 즉시 바뀌지 않지만, 새 세션·명시 갱신·압축 재빌드 경계에서 다시 읽는 경로는 존재합니다.

### 발표 포인트

구성 요소의 역할을 확인하고, 실제 payload는 Demo에서 살펴봅니다.

### 화면 읽기

시스템 지시와 대화 이력, 이번 호출에 붙는 정보, 공개 Tool 목록을 따로 읽습니다.

### 적용 예와 확인할 경계

API 요청에는 Tool 이름·설명·인자 계약이 전달됩니다. 함수 본체나 인증 객체가 보내지는지는 메시지·Tool 반환 내용을 별도로 봅니다.

## S08 — System Prompt를 고정해 Prefix를 재사용하기

## System Prompt를 고정해 Prefix를 재사용하기

같은 System Prompt와 이력의 앞부분을 다시 사용할 수 있습니다.

세션 snapshot과 append 중심 이력은 안정적인 Prefix를 유지하는 데 도움이 됩니다. 반대로 앞부분의 지침 변경, schema 순서 변경, History 수정·압축은 재사용 구간에 영향을 줄 수 있습니다. 일부 앞부분만 바뀌었다고 모든 캐시가 항상 동일하게 무효화된다고 단정하지 않습니다.

8,000/2,000 tokens는 설명용 수치입니다. PromptCachePlan, cache_control, TTL·one-shot 조건은 특정 Provider 경로의 심화 설명이며 vLLM 공통 계약으로 보지 않습니다. 실제 적중·비용·TTFT는 지원 모델과 환경에서 측정해야 하고 OpenAI 프록시 기록을 vLLM 캐시 실측으로 제시하지 않습니다.

Hermes는 입력을 구성하고, 캐시 적중은 추론 서비스가 판단합니다.

### 화면 읽기

Prefix Cache는 제공자가 이전 요청과 같은 앞부분을 재사용하는 최적화입니다.

### 적용 예와 확인할 경계

시스템 지시가 같아도 도구 순서나 이전 메시지 앞부분이 변하면 재사용 범위가 줄 수 있습니다. 실제 hit는 제공자 지표에서 확인합니다.

## S10 — memory 도구에 무엇을 보낼까?

## memory 도구에 무엇을 보낼까?

**파일 선택** — MEMORY.md 2,200자 / USER.md 1,375자. 프로필 설정에서 변경 가능.

**저장할 작업 지정** — add는 추가, patch는 찾아서 수정, remove는 지정한 내용을 삭제.

**여러 변경을 함께 요청** — 여러 작업은 operations 배열로 전달. 한도 초과 시 오류를 반환하고 쓰지 않음.

**현재 대화에서 알 수 있는 값** — 모델은 자신의 호출 인자와 Tool 응답을 이력으로 봄. 시스템 프롬프트는 그대로.

성공 응답 예시는 필드 일부입니다. 기본 성공 결과는 기억 전체를 반환하지 않습니다. 따라서 현재 대화의 모델은 방금 입력한 문장과 저장 성공을 알 수 있지만, 변경된 MEMORY.md 전체가 자동으로 다시 주입되지는 않습니다.

### 화면 읽기

memory는 대상 파일과 변경 작업을 입력으로 받고 쓰기 결과를 반환합니다.

### 적용 예와 확인할 경계

새 사실을 저장한 직후 모델은 자기 호출 인자와 성공 응답을 볼 수 있습니다. 기존 세션의 시스템 프롬프트 전체가 다시 조립되는 시점과는 다릅니다.

## HMEM — 기억을 쓰기 전에 사람에게 물어볼까?

## 기억을 쓰기 전에 사람에게 물어볼까?

기본: write_approval: false. 파일 크기, 내용, 수정 대상 검사는 별도입니다.

대화형: true이고 승인 통로가 있으면 변경을 보여주고 결정받습니다.

무인 실행: 검토 요청을 보류 파일에 남길 수 있습니다. /memory approve <id>와 /memory reject <id>로 처리합니다. 백그라운드 삭제에는 별도 보호가 적용될 수 있습니다.

### 화면 읽기

기본 쓰기 검증과 사용자의 명시적 결정은 서로 다른 검사입니다.

### 적용 예와 확인할 경계

대화 중에는 지원되는 승인 통로에서 결정하고, 무인 Cron에서는 보류 목록에 남을 수 있습니다. 승인 후에도 오래된 수정 대상이 그대로인지 확인할 필요가 있습니다.

## S11 — session_search에 무엇을 보낼까?

## session_search에 무엇을 보낼까?

**① 특정 메시지 주변 보기** — 세션과 메시지 번호가 있으면 주변 조회. window 기본 5.

**② 세션 열기** — 세션 ID만 있으면 해당 세션을 읽음.

**③ 최근 세션 목록** — 세션 ID 없이 검색어가 비면 최근 목록. limit 기본 3, 허용 범위 1~10.

**④ 검색어로 찾기** — 검색어가 있으면 DB에서 검색. after/before는 세션 시작 시각 기준.

sort는 newest/oldest, detail은 adaptive/full을 받습니다. 검색 범위는 profile 및 제외 세션 등 런타임 필터에도 영향을 받습니다. 예시 ID와 내용은 설명용입니다.

### 화면 읽기

session_id가 있으면 읽기 모드부터 고릅니다. 세션 ID가 없을 때만 빈 query인지 확인합니다.

### 적용 예와 확인할 경계

특정 메시지 주변 탐색의 window는 기본 5이고 1~20 범위로 조정합니다. 검색 및 최근 목록의 limit 기본 3과는 별개입니다.

## HSEARCH — 검색어 정리와 범위 확인은 누가 할까?

## 검색어 정리와 범위 확인은 누가 할까?

### 주요 개념

**Sanitizer**: 인용구를 보존하고 지원하지 않는 구문·끝 연산자·기호를 정리하며 점·하이픈 단어를 인용하는 문자열 처리입니다.

**FTS/범위**: SQL에 role/source/time 조건을 넣고 가시성과 계보를 고려해 세션과 메시지를 선택합니다.

### 설명

hermes_state_search.py의 _sanitize_fts5_query는 인용 문구를 임시 보존하고 지원되지 않는 문자, 퍼센트·와일드카드·dangling boolean을 정리한 뒤 dotted/hyphenated/underscored 단어를 인용하고 문구를 복구합니다. 이는 결정적 Python 처리이며 LLM이 검색어 의미를 재해석하는 단계가 아닙니다. ALARM-17 인용은 이 코드 규칙을 보여주는 예입니다.

DB는 MATCH와 rank/snippet, 공통 role/source/session-start 필터를 사용하고 환경·문자열에 따라 CJK 인덱스나 LIKE fallback을 택합니다. Tool은 현재 live context와 계보, 제외 세션, 제목 일치와 limit 등을 고려해 결과를 구성합니다. 검색된 코드가 맞더라도 다른 설비·기간이면 업무상 정답이 아닐 수 있습니다. 이 마지막 검증은 사용자 업무 평가 기준이며 Hermes가 측정 데이터의 도메인 정답을 자동 보장하는 기능은 아닙니다.

### 발표 포인트

문법상 검색 성공과 업무상 올바른 근거 검색은 따로 확인합니다.

### 화면 읽기

검색어의 의미는 호출자가 정하고 DB에 넣기 전 문법은 코드가 정리합니다.

### 적용 예와 확인할 경계

ALARM-17을 인용 처리해도 다른 LOT 경보가 검색될 수 있습니다. 검색 결과의 세션·측정 기간이 업무 질문과 맞는지 별도로 확인합니다.

## S09 — 예시 Context가 압축되는 과정

## 예시 Context가 압축되는 과정

### 주요 개념

**Prune**: 보호되지 않는 오래되고 큰 Tool 결과를 줄이는 처리입니다.

**Summary + Tail**: 중간 이력 요약과 최근 메시지·호출/결과 쌍을 합쳐 요청을 구성합니다.

### 설명

표시의 5,000행, call_7, LOT-A, artifact URI와 요약 문장은 설명용 가상 Context이며 실제 compressor 출력이나 실행 Trace가 아닙니다. 실제 기능은 필요 판단→오래된 큰 Tool 결과 prune→최근/미사용 결과·호출 쌍 보호→중간 이력 요약→합성·프로토콜 정합성 보정입니다.

원문 계산 조건은 별도 artifact로 보존하고 Context에는 식별자·단위·리비전·요약을 두는 업무 설계를 보여줍니다. 압축은 내용 손실과 캐시 Prefix 변경을 수반할 수 있습니다. timeout/감소 실패·재로딩 마커·session lineage를 처리하는 경로와 압축 후 system snapshot 재빌드 경계도 존재합니다. 모든 임계값을 고정 50%/85%라고 단정하지 않습니다.

### 발표 포인트

실제 문자열·행 수를 재현한 로그가 아닌 압축 원리의 예시입니다.

### 코드 표시

가상 Context의 Before/Prune/Summary 예시. 실측·완전한 compressor 출력이 아님.

### 화면 읽기

그림의 앞부분은 오래된 이력이 줄어드는 과정이고, 뒷부분은 현재 실행에 필요한 메시지의 관계를 보존하는 과정입니다.

### 적용 예와 확인할 경계

A17 Tool 결과를 유지할 때 대응하는 호출도 같이 봅니다. 요약을 장기 기록과 동일한 정확도의 원본으로 사용하지 않습니다.

## HTOOL — Tools와 Skills

## Tools와 Skills

### 주요 개념

**Tools와 Skills**: 실행 능력과 재사용 절차를 연결합니다.

### 설명

다음 범주를 시작하는 전환 장표입니다. 도구 등록·검증 → 승인·실행 → Skill 작성·관리 순서로 살펴봅니다.

### 발표 포인트



### 화면 읽기

Tools는 실행 가능한 기능이고 Skills는 작업 절차를 제공하는 지식입니다.

### 적용 예와 확인할 경계

검사 원칙을 담은 SKILL.md를 읽어도 데이터 접근 권한이 생기지는 않습니다. 실제 조회는 별도의 Tool로 수행합니다.

## S13 — Hermes Tool은 이렇게 등록됩니다

## Hermes Tool은 이렇게 등록됩니다

### 주요 개념

**등록**: ToolRegistry가 name/toolset/schema/handler/check_fn 등을 보관합니다.

**Discovery**: 최상위 registry.register 호출을 찾은 모듈을 import해 등록 코드를 실행합니다.

### 설명

표시 코드는 tools/skills_tool.py의 실제 registry.register 항목을 읽기 좋게 재배치한 축약이며 handler lambda 본문과 emoji 등을 생략했습니다. 실제 handler는 skills_list(category=args.get("category"), task_id=kw.get("task_id"))를 호출합니다. 모듈 discovery는 AST를 사용하며 helper 파일 전체를 임의 실행 가능한 Tool로 만드는 방식은 아닙니다.

활성 Toolset과 가용성 검사를 거친 이름 집합으로 get_definitions를 구성합니다. 현재 소스의 check_fn probe에는 TTL·scope cache와 예외/last-known 처리 등 세부 로직이 있으므로 단순 매 요청 무조건 재검사라고 말하지 않습니다. ToolEntry.description은 Registry 메타데이터이고 모델 설명의 기준은 schema.description입니다.

### 발표 포인트

Python 파일을 두는 것만으로 모든 함수가 Tool이 되지는 않습니다.

### 코드 표시

공식 등록 코드의 항목 재배치·handler 생략. 이름과 파라미터는 실제 코드에 존재한다.

### 화면 읽기

등록 항목의 schema는 모델 계약, handler는 로컬 실행 함수, check_fn은 사용 가능 조건을 맡습니다.

### 적용 예와 확인할 경계

skills_list가 레지스트리에 있다는 사실과 현재 모델 요청에 포함된다는 사실을 구분합니다.

## HSCHEMA — 모델에게 공개되는 Tool의 실제 수준

## 모델에게 공개되는 Tool의 실제 수준

### 주요 개념

**모델용 schema**: name·schema.description·parameters 등이 function definition으로 전달됩니다.

**서버용 구현**: handler/check_fn/credential은 모델 schema를 구성하는 실행 함수와 동일한 데이터가 아닙니다.

### 설명

registry.py get_definitions는 entry.schema에 name을 결합하고 dynamic schema override를 반영한 뒤 {type:function,function:schema_with_name} 형식을 반환합니다. 실제 전송 형식은 Provider Adapter에서 바뀔 수 있습니다. skills_list의 category string과 required=[]는 공식 schema의 필드를 따른 예이며 description은 화면에서 줄였습니다.

별도 description= 인자로 Registry 메타데이터만 채워도 모델 schema에 자동 복사되는 것은 아닙니다. 실제 인가와 데이터 범위는 handler/Backend에서 검사해야 합니다. handler 자체를 schema에 보내지 않는다는 설명이지 Tool의 반환 데이터에 비밀이 절대 포함되지 않는다는 보장은 아닙니다.

### 발표 포인트

모델은 실행 코드를 받는 것이 아니라 호출 가능한 계약을 받습니다.

### 코드 표시

실제 schema 기반 설명용 JSON. description 축약, 실제 wire capture 아님.

### 화면 읽기

모델 쪽에는 공개 Tool의 인자 정의가 보이고, 호스트 쪽에는 실행 함수와 런타임 상태가 남습니다.

### 적용 예와 확인할 경계

read_fab_bin에 문자열 bin_id를 받더라도 그 BIN의 실제 접근 가능 여부는 실행 측에서 판단합니다.

## HCONNECT — Local Tool·MCP·Plugin은 Hermes 어디에 붙을까?

## Local Tool·MCP·Plugin은 Hermes 어디에 붙을까?

### 주요 개념

**Native**: 직접 등록된 schema/handler를 model_tools와 Registry가 연결합니다.

**MCP**: 발견한 외부 명세를 Hermes Tool에 등록하고 transport를 통해 서버를 호출합니다.

**Plugin**: register(ctx)로 실행환경에 접점을 추가하는 코드 확장이며 신뢰·호환성을 관리해야 합니다.

### 설명

공식 Tools Runtime과 v0.22.5 registry/model_tools를 대조한 역할도입니다. Native discovery 후 MCP discovery와 Plugin 로딩이 기능을 추가합니다. MCP 서버는 stdio subprocess 또는 네트워크 transport를 쓸 수 있으며 이름·schema·서버별 필터와 credential 전달을 확인해야 합니다. Plugin은 ctx.register_tool/register_hook뿐 아니라 MemoryProvider/ContextEngine 등 Hermes 내부 기능도 확장할 수 있습니다.

Agent 상태를 사용하는 memory·session_search·delegate_task는 Inline 가로채기가 있습니다. 따라서 모든 Tool이 동일한 pre/post Hook, terminal guard를 지나간다는 그림은 부정확합니다. MCP 서버 권한과 Plugin 코드 권한도 별도이며 연결 표준이나 schema만으로 데이터 인가가 완성되지는 않습니다.

### 발표 포인트

중앙 Hook 하나가 모든 Inline·외부 실행을 감싼다고 가정하지 않습니다.

### 화면 읽기

로컬 함수, 원격 MCP 연결, Plugin 확장은 서로 다른 연결 경로입니다.

### 적용 예와 확인할 경계

같은 조회 도구라도 로컬 호출과 MCP 왕복은 실패 위치가 다릅니다. Plugin Hook은 도구가 실행되기 전후 정책을 덧붙일 수 있습니다.

## HVALID — validate_tool_calls가 검사하는 순서

## validate_tool_calls가 검사하는 순서

### 주요 개념

**ID·이름**: 이미 사용된 ID와 충돌을 정리하고 허용 이름 및 repair 가능성을 확인합니다.

**인자 정규화**: dict/list를 JSON string으로, 빈 인자를 {}로 정리하고 json.loads를 시도합니다.

### 설명

turn_tool_validation.py의 순서는 ID 고유화/Provider ID 정규화→이름 repair 및 valid_tool_names 비교→JSON 정규화와 parse입니다. 정상·unknown 이름이 섞이면 정상 호출을 살리고 unknown에 대응 오류 결과를 반환합니다. 유효 호출이 전혀 없는 이름 오류만 strike가 누적되며 3회 후 partial로 나가는 경로입니다.

JSON은 잘림을 감지하면 실행을 거부하고 partial 종료합니다. 일반 JSON 오류는 제한 retry 뒤 호출/결과 관계를 맞춘 오류 결과를 넣어 모델 복구 기회를 줍니다. 이는 JSON 문법 검사이지 임의 Tool의 모든 business schema를 Pydantic처럼 검증한다는 뜻이 아닙니다. 실제 Tool handler와 별도 정책에서 타입·범위·권한을 추가로 확인합니다.

### 발표 포인트

여기서 하는 검사는 모든 Tool의 업무 의미·권한 검증을 대신하지 않습니다.

### 화면 읽기

이 검사는 모델이 제출한 호출을 실행기에 넘길 수 있는지 판단하는 지점입니다.

### 적용 예와 확인할 경계

등록되지 않은 이름이나 잘못된 인자 표현을 업무상 권한 부족과 구분합니다. 검사를 통과해도 발행 허가가 내려진 것은 아닙니다.

## S13A — Tool 요청이 실제 실행으로 이어지는 과정

## Tool 요청이 실제 실행으로 이어지는 과정

### 개념

**Persist-before-execute**: 부작용을 시작하기 전에 Tool Call 정본을 저장하고, 그 저장이 실패하면 실행을 중단합니다.

**Call / Result 대응**: 유효하지 않은 호출과 실행 오류도 대응 결과로 처리하여 메시지 관계를 유지합니다.

**실행 후 장애**: 외부 작업 완료 뒤 결과 저장 전에 중단되면 실제 효과를 별도로 확인해야 합니다.

### 설명

학습자료의 v0.22.5 Tool round는 호출 이름·인자·ID를 검증하고 Tool Call을 먼저 기록한 뒤 실행기로 전달하는 경로를 설명합니다. 유효하지 않은 호출이 섞인 배치는 유효 호출 처리와 오류 결과 대응을 구분합니다. 검증을 통과했다고 모든 인자의 업무적 의미가 옳다는 뜻은 아닙니다.

대표 흐름은 검증→호출 기록→해당 경로의 정책·승인→handler→결과 기록→다음 모델 요청입니다. Inline/Registry/MCP/Plugin에 같은 Hook 순서를 보장하는 도식은 아닙니다. 호출 정본 저장 실패는 부작용 실행 전 중단합니다. 반면 외부 효과 발생 후 결과 기록 전 crash는 여전히 가능하므로 재시도에는 대상 시스템의 멱등성이나 효과 확인이 필요합니다. 후자는 일반 설계 원칙이며 모든 Tool에 내장됐다고 주장하지 않습니다.

### 발표 포인트

Tool 실행 전 기록은 필요하지만 외부 작업의 중복 방지까지 보장하지는 않습니다.

### 학습자료 근거

심층 학습 §3.1·4.3·11.3~11.4·17.2; 기초 학습자료 및 추가 코멘트와 대조. 구현 설명·문서 설명·업무 설계 제안을 구분한다.

### 화면 읽기

호출 이름으로 실행 경로를 찾고, 정책과 검사 뒤에 handler를 실행합니다.

### 적용 예와 확인할 경계

Tool Call ID로 모델의 요청과 결과를 연결합니다. 같은 이름의 조회가 두 번 나와도 두 호출 결과는 각각 연결해야 합니다.

## S13B — 실행 전 검사는 실제로 어떤 순서일까?

## 실행 전 검사는 실제로 어떤 순서일까?

### 주요 개념

**Command guard**: 격리/host 접근, floor, prepared guard, mode·allowlist, 무인 정책, 위험 패턴 등을 순서대로 판단합니다.

**Tool별 검사**: 파일 경로 정책·Plugin 규칙·MCP 서버 인가는 해당 Tool 경로에서 별도로 적용됩니다.

### 설명

v0.22.5 approval.py를 대조했습니다. host 접근 없는 충분히 격리된 backend는 별도 user-deny 확인 경로이고, 그 밖에는 _floor_block을 mode=off나 yolo보다 먼저 검사합니다. prepared guard 재사용, 영구 allowlist, UI 존재와 무인 문맥, 위험 패턴 및 세션 승인 cache를 거쳐 _human_decision에 도달합니다.

이 그림은 terminal command guard의 순서를 축약한 것이며 파일/MCP/Inline Tool 전부의 단일 순서가 아닙니다. 다른 도구는 경로·인자·handler 검증, pre_tool_call 규칙과 request_tool_approval 등의 경로가 있습니다. 표시의 floor_block 등은 실제 private 함수명의 축약이며 그대로 실행하는 코드가 아닙니다. 승인 전후 최종 인자 일치와 OS/DB 권한도 별도로 확인합니다.

### 발표 포인트

off·격리 실행도 모든 Tool·권한 정책을 전부 해제한다는 뜻은 아닙니다.

### 코드 표시

공식 command guard의 조건 순서를 재구성한 의사코드. 함수명/return shape를 짧게 표시.

### 화면 읽기

실행 전 검사를 순서대로 읽고 어느 조건에서 호출을 막는지 확인합니다.

### 적용 예와 확인할 경계

명령을 검사하는 경로와 업무 Tool Hook의 판정을 구분합니다. 둘은 입력과 허용 규칙이 다를 수 있습니다.

## HHUMAN — 어떤 경우에 실제 사용자 승인을 요청할까?

## 어떤 경우에 실제 사용자 승인을 요청할까?

### 주요 개념

**smart**: 보조 guardian의 approve/deny/escalate 결과를 사용하는 경로가 있습니다.

**사용자 승인**: CLI callback·지원 transport 등에서 허용 범위를 검토하고 요청 결과를 기록합니다.

### 설명

approval_smart.py는 보조 LLM verdict를 approve/deny/escalate로 정규화하고 실패·빈 응답·불확실한 값은 escalate합니다. 실제 human decision은 mode·surface·기존 승인·정책에 따라 보조 판단과 사용자 UI를 연결하므로 smart=항상 사람 질문도, smart=무조건 안전 승인도 아닙니다.

사용자 선택은 once/session/always/deny 등이며 도구·표면·설정에 따라 영구/세션 승인이 제한될 수 있습니다. DEFAULT_CONFIG의 approvals.mode는 smart, cron_mode/single_query_mode/unattended_mode는 deny입니다. off·allowlist 등 앞선 승인 조건과 위험 패턴 검사를 먼저 거칩니다. 실제 사용자 응답이 불가능한 문맥은 해당 policy로 정리합니다. Memory/Skill write_approval은 이 명령 승인과 별도 Gate입니다.

### 발표 포인트

smart가 모든 요청을 사람에게 묻는 모드인 것은 아닙니다.

### 화면 읽기

사용자 확인은 런타임이 정책을 적용해 사람의 결정이 필요하다고 판단할 때 열립니다.

### 적용 예와 확인할 경계

발행 요청에서 규칙, 실제 인자, 승인 범위를 같이 확인합니다. 거절된 호출은 외부 효과가 발생하지 않았는지 Tool 기록으로 확인합니다.

## HFAIL — 오류·취소가 실제 작업에 남기는 것

## 오류·취소가 실제 작업에 남기는 것

### 주요 개념

**실행 전 실패**: Tool-call 정본 저장 실패는 해당 실행 시작을 막습니다.

**실행 후 실패**: 외부 작업 뒤 결과 저장 실패는 효과가 남은 미상 상태가 될 수 있습니다.

### 설명

명령·경로·인자 검사와 사람 승인, 실행환경의 실제 권한을 구분합니다. 승인 모드 off가 모든 강제 차단까지 없앤다는 뜻은 아니며 무인 실행 정책도 별도로 적용됩니다. Tool Output이나 검색 문서는 데이터로 다루어야 하며, 그 안의 지시를 실행 권한으로 승격해서는 안 됩니다. 검사·Hook만으로 모든 공격을 차단한다고 주장하지 않습니다.

API 장애는 통신 retry나 설정된 fallback, Tool 오류는 모델이 읽는 오류 결과와 수정 경로로 이어집니다. 외부 쓰기 작업의 재실행에는 중복 효과를 확인해야 합니다. Timeout·취소 뒤 결과가 미상일 수 있고 opt-in Checkpoint는 지원 범위의 파일 복구 기능입니다. 검토한 인자와 최종 실행 인자 일치, 멱등성과 보상은 추가 검증할 업무 설계이며 Hermes 전 경로의 안전성 보증은 아닙니다.

이 장은 실제 Tool round와 command policy, interrupt/timeout의 서로 다른 상태를 연결합니다. Checkpoint는 opt-in 파일 복구 범위이며 외부 API·DB 전체 rollback이 아닙니다.

### 발표 포인트

기록 실패·중단·외부 효과 미상을 같은 성공 상태로 합치지 않습니다.

### 화면 읽기

응답이 실패했다는 표시와 도구의 외부 효과를 별도 상태로 읽습니다.

### 적용 예와 확인할 경계

기록 도구가 저장한 뒤 응답 전송이 실패하면 사용자 화면에는 오류가 떠도 쓰기가 끝났을 수 있습니다.

## S14 — Hermes의 병렬 Tool 실행 코드

## Hermes의 병렬 Tool 실행 코드

### 주요 개념

**Segment planner**: read-only·대화형·파일 경로 충돌과 effect 가능성을 보고 구간을 나눕니다.

**Concurrent batch**: Context를 전파해 Worker를 제출하고 원래 index의 결과 slot을 채웁니다.

### 설명

executor.submit(propagate_context_to_thread(self.run_worker), i, submit_index)는 v0.22.5의 실제 호출이며 화면은 줄바꿈만 조정했습니다. run_worker는 middleware·권한·시작 순서 gate를 사용하고 outcome을 self.results[index]에 저장합니다. deadline·interrupt 시 미상 효과와 abandoned 결과를 처리할 수 있습니다.

모델이 호출을 여러 개 제안했다고 전부 즉시 병렬 수행하지 않습니다. _plan_tool_batch_segments는 Reader·write 경로 중첩·대화형 도구 등을 고려하고 unknown/Plugin/MCP는 기본 effect-capable로 보수적으로 다루는 경로가 있습니다. thread pool은 CPU 병렬 성능 보증이 아니며 외부 I/O·GIL·락에 좌우됩니다. 결과 call_id 정합성과 데이터 snapshot 검증은 별개입니다.

### 발표 포인트

thread 여러 개와 독립 Agent 여러 개는 다른 실행 방식입니다.

### 코드 표시

executor.submit 실제 호출 발췌(줄바꿈 조정). 주석의 결과 대입은 인접 run_worker 소스의 실제 코드이다.

### 화면 읽기

병렬 실행에 적합한 묶음과 단독 실행이 필요한 호출을 분리해 읽습니다.

### 적용 예와 확인할 경계

독립적인 두 BIN 조회는 대기를 겹칠 수 있습니다. 앞 조회 결과가 뒤 호출의 인자라면 실행 묶음만으로 의존성이 해결되지 않습니다.

## S12 — Skills를 찾고 읽는 Hermes의 경로

## Skills를 찾고 읽는 Hermes의 경로

목록·본문·참고 자료와 명시·자동 로딩을 구분합니다.

skills_list는 설치 Skill의 이름·설명·category를 보여주고, skill_view(name)는 본문과 linked_files를 반환합니다. 필요한 경우 file_path로 references/templates/scripts를 추가로 읽습니다. 목록 노출과 전체 본문 로딩은 다릅니다.

명시 slash invocation, skills.auto_load, 모델의 Tool 호출, Cron 첨부라는 로딩 입구가 있습니다. auto_load는 pinned system 영역에 들어갈 수 있고 일반 인덱스와 동적 로딩은 다른 경로입니다. 내용 작성과 승인·Curator 관리는 다음 장들에서 따로 설명합니다.

Skill은 실행 함수가 아니라 도구 사용 절차를 담은 재사용 문서입니다.

### 화면 읽기

목록의 설명으로 Skill을 고른 뒤 실제 절차가 필요할 때 본문을 읽습니다.

### 적용 예와 확인할 경계

수율 검증 절차를 읽은 이후에도 모델이 어떤 Tool을 부르고 어떤 입력을 넣었는지는 실행 로그에서 확인합니다.

## HLEARN — Hermes는 언제 새 Skill을 만들까?

## Hermes는 언제 새 Skill을 만들까?

### 주요 개념

**생성 판단**: 작업 경험·피드백과 System guidance를 보고 모델이 재사용 가치를 판단합니다.

**nudge / review**: 실행 중 주기적 안내와 백그라운드 검토가 저장을 유도할 수 있지만 결정적 성공 판정기는 아닙니다.

### 설명

System Prompt의 Tool-aware guidance와 Skills 지침은 비사소한 절차·재사용 가능한 해결·사용자 수정 등을 Skill로 남기도록 유도합니다. prepare_iteration에는 skill_manage가 사용 가능할 때 _iters_since_skill을 증가시키는 nudge bookkeeping이 있습니다. 실제 생성은 모델이 skill_manage를 요청해야 일어납니다. 고정된 성공률 기준으로 Runtime이 최적 절차를 자동 증명하는 알고리즘이 아닙니다.

명시적인 /learn도 자료를 읽고 절차를 저술하는 진입점입니다. background review의 모델·입력 budget·주기와 활성 기능에 따라 동작이 달라질 수 있습니다. 새 기록은 다음 로딩에서 영향을 주므로 틀린 절차도 확산될 수 있고 검토와 적용 범위가 필요합니다.

### 발표 포인트

자기 개선은 재사용 절차의 갱신이며 모델 가중치 학습이 아닙니다.

### 화면 읽기

모델이 반복 가능한 절차를 발견했을 때 Skill로 저장할 수 있는 경로입니다.

### 적용 예와 확인할 경계

일회성 측정값보다 단위를 확인하고 분모를 재검증하는 절차가 재사용에 적합합니다. 저장 여부는 실제 Tool 호출로 확인합니다.

## HWRITE — skill_manage의 변경은 어떻게 반영될까?

## skill_manage의 변경은 어떻게 반영될까?

### 주요 개념

**Skill 변경**: operations 배열의 action/name/content 또는 old_string/new_string 등으로 SKILL.md와 지원 파일을 변경합니다.

**기본 정책**: v0.22.5 write_approval=false, guard_agent_created=false, ledger=true를 확인했습니다.

### 설명

표시 Tool 요청은 모델에게 공개되는 operations 배열 schema를 따른 예이며 함수 SDK 호출이나 실제 생성 기록이 아닙니다. 각 operation은 action별 anyOf/additionalProperties=false로 구분됩니다. patch는 old_string/new_string(부분 치환) 또는 content(본문 전체 교체)를 받습니다. write_file/remove_file은 지원 파일, delete는 단독 operation만 허용합니다. batch 실패는 변경 대상을 rollback하는 원자적 처리이며, 레거시 flat action/name 인자는 기존 이력 재생을 위해 수용하지만 모델에는 공개하지 않습니다. 경로·대상·동작 검증과 쓰기 Gate가 파일 변경을 처리합니다. write_approval=true이면 Skill 본문이 크므로 foreground도 항상 stage해 /skills pending, /skills diff <id>, /skills approve|reject <id>로 검토합니다. Memory foreground inline과 다릅니다.

agent-created Skill 내용 scanner는 guard_agent_created 설정에 의존하며 이 태그 기본 false입니다. Hub 설치 scan과 Agent 작성 scan을 같은 기본값으로 합치지 않습니다. advisory linter도 보증 검사가 아닙니다. ledger는 변경 전후 hash를 기록하지만 감사 기록 실패를 모든 변경의 강제 차단으로 쓰는 것은 아닙니다. scope·SOP 버전·만료·검증은 업무 설계이고 자동 가중치 학습과 무관합니다.

### 발표 포인트

내용 검사와 사람의 승인, 업무 정확성 검증은 서로 다른 절차입니다.

### 코드 표시

공식 Tool schema 기반 인자 예시 + 실제 DEFAULT_CONFIG 발췌 항목. 생성 실행하지 않음.

### 화면 읽기

Skill을 수정한 도구 결과와 디스크에 남은 파일을 함께 확인합니다.

### 적용 예와 확인할 경계

이미 읽은 Skill 본문이 같은 요청에서 자동으로 새로 읽히는지 단정하지 말고, 다음 본문 로딩 시점을 구분합니다.

## HCURATOR — Curator는 언제 무엇을 정리할까?

## Curator는 언제 무엇을 정리할까?

### 주요 개념

**발동**: 기본 interval_hours=168, min_idle_hours=2이며 세션 시작·maintenance에서 조건을 확인합니다.

**자동 정리**: 기본 stale 14일, archive 30일. pinned/예약 참조 등 보호 대상을 확인합니다.

### 설명

v0.22.5 Curator 코드와 고정 문서의 기본값을 확인했습니다. cron job 자체가 아니라 inactivity 조건 점검으로 실행됩니다. 첫 관찰에는 last_run_at을 초기화하고 한 interval 뒤 실제 pass를 미루는 경로가 있습니다. 활성 turn·profile maintenance 주체·CLI/serve 등 표면별 실행 조건은 소스를 확인합니다.

기본 대상은 Agent 생성 Skill이고 Hub 설치는 제외됩니다. pinned 및 Cron 참조 Skill은 자동 전이에서 보호하며 built-in 정리는 prune_builtins opt-in입니다. 미사용 14일 stale, 30일 archive, never-used grace 조건 등을 적용합니다. 자동 archive는 복구 가능한 이동이며 영구 자동 삭제로 설명하지 않습니다. 품질·정답을 검증한 상태값은 아닙니다.

### 발표 포인트

active → stale → archived는 사용 이력 관리이며 품질 점수 판정이 아닙니다.

### 화면 읽기

Curator가 사용 이력과 정책에 따라 관리할 대상을 고르는 경로입니다.

### 적용 예와 확인할 경계

최근에 쓰이지 않았다는 이유와 절차가 틀렸다는 판단은 다릅니다. 이동·정리된 항목을 어떤 규칙이 골랐는지 확인합니다.

## HCONSOLIDATE — Curator의 LLM 통합은 별도 선택입니다

## Curator의 LLM 통합은 별도 선택입니다

### 주요 개념

**consolidate**: 기본 false. 활성화하면 보조 Agent가 겹침을 검토해 통합·수정을 제안/적용하는 경로입니다.

**점검**: status와 dry-run으로 상태·예상 결과를 확인할 수 있습니다.

### 설명

고정 문서에서 기본 deterministic prune과 opt-in LLM consolidation을 구분합니다. LLM pass는 독립 prompt cache의 fork이며 현재 대화에 직접 문맥을 섞는 단계가 아닙니다. 지원 파일을 포함한 Skill package를 유지/이관하고 상대 참조를 고쳐야 하며 SKILL.md만 납작하게 복사하는 것으로 통합을 설명하지 않습니다.

보조 모델 비용과 광범위 변경 때문에 consolidate 기본 false입니다. hermes curator run --dry-run은 변경 없는 점검, --consolidate는 수동 통합 선택입니다. ledger/backup/rollback은 실제 태그의 명령·제약을 확인해야 하며 pin이 모든 수정을 막는 lock과 동일하지 않습니다. 실제 실행 결과나 개선 성능을 측정한 것은 아닙니다.

### 발표 포인트

Skill을 합칠 때 본문뿐 아니라 references·scripts·템플릿도 함께 관리합니다.

### 화면 읽기

정리와 LLM을 통한 내용 통합은 서로 다른 작업입니다.

### 적용 예와 확인할 경계

두 절차를 합친 후에는 원래 있던 데이터 검증·승인 조건이 빠지지 않았는지 본문을 비교합니다.

## HSAFE — 안전장치와 실행 기록

## 안전장치와 실행 기록

### 주요 개념

**안전장치와 실행 기록**: 실행을 제한하는 판단과 실행을 설명하는 기록을 연결합니다.

### 설명

다음 범주를 시작하는 전환 장표입니다. 기본 보호 장치 → 반복·정책 제어 → Trace 수집·활용 순서로 살펴봅니다.

### 발표 포인트



### 화면 읽기

안전장치는 실행을 제한하고, 기록은 어떤 일이 있었는지 관찰하는 데 쓰입니다.

### 적용 예와 확인할 경계

Tool 호출이 기록됐다는 것과 실행을 막았다는 것은 다릅니다. 차단 판정과 handler 진입 여부를 함께 확인합니다.

## HGUARD — Hermes의 기본 안전장치는 어디에 있을까?

## Hermes의 기본 안전장치는 어디에 있을까?

### 주요 개념

**실행 승인**: 명령 패턴·hardline floor·기존 승인·smart/manual 경로를 처리합니다.

**파일 보호**: 민감 경로와 config, 프로젝트 지침 파일에 대한 별도 검사입니다.

**격리**: backend 기본 local은 자동 컨테이너 격리가 아닙니다. Checkpoint 기본값도 false입니다.

### 설명

DEFAULT_CONFIG를 대조하면 terminal.backend=local, approvals.mode=smart, security.allow_private_urls=false, security.redact_secrets=true, security.protected_instruction_files=true, checkpoints.enabled=false입니다. dangerous command approval은 이미 앞 장에서 본 별도 경로이며, 여기서는 전체 보호 지점을 묶어 봅니다.

file_tools_write_guards는 raw NT/device 경로와 정규화/실제 경로, 민감 시스템 경로·Hermes config를 검사합니다. 프로젝트의 AGENTS.md/CLAUDE.md/SOUL.md/.cursorrules와 .hermes 지침은 별도 일회 승인 경로이고, yolo와 무인 실행 예외도 구분합니다. HERMES_WRITE_SAFE_ROOT로 추가 쓰기 범위를 제한할 수 있지만 일반 파일 Tool 보호가 임의 Python·Shell·외부 MCP의 모든 쓰기를 동일하게 가두는 OS sandbox는 아닙니다.

활용할 때는 필요한 backend와 파일/네트워크 범위, 승인 가능한 표면을 먼저 정하고, 업무 규칙은 Handler/Backend 또는 명시적인 정책 확장으로 더합니다. 지침 텍스트는 실행 권한 검사의 대체물이 아닙니다.

### 발표 포인트

기본 local 실행의 권한과 격리 환경의 권한을 구분해 설정합니다.

### 화면 읽기

Guardrail의 적용 위치를 입력·Tool·루프 제어로 나눠 봅니다.

### 적용 예와 확인할 경계

사용자에게 묻는 정책, 명령을 검사하는 정책, 반복 행동을 감지하는 정책은 각각 다른 조건에 반응합니다.

## HGUARDFLOW — 반복되는 Tool 호출을 코드에서 감지하기

## 반복되는 Tool 호출을 코드에서 감지하기

### 주요 개념

**Signature**: Tool 이름과 정규화 인자의 hash로 동일 호출을 식별합니다.

**실행 전/후**: before_call은 cap/반복 차단, after_call은 실패·진전 카운터, observe_call은 동일 streak·cycle을 관찰합니다.

### 설명

ToolCallGuardrailController는 reset_for_turn으로 상태를 초기화합니다. before_call은 먼저 web_search/subagent cap을 검사하고, hard_stop_enabled일 때 변경 없는 동일 실패나 idempotent 결과 반복을 차단합니다. tool_executor의 policy 경로는 scope→Plugin pre-hook/modify→pruned argument 검사→before_call→실제 dispatch 순서를 가집니다.

after_call은 실패 분류, exact signature·같은 Tool 실패 누적, 성공한 수정 이후 진전 표시, idempotent result hash를 관리합니다. HTTP rate-limit은 정상 cooldown 재시도일 수 있어 exact-failure 증가를 건너뛰는 예외가 있고, terminal 등의 다양한 실패 명령은 진단 과정일 수 있어 failure-tolerant 예외를 둡니다. observe_call은 A,A,A와 A,B,A,B 같은 cycle을 따로 다루고 큰 동일 결과는 Context 참조 stub으로 줄일 수 있습니다. stub은 이미 실행된 결과의 표현 축소이며 실행 생략 cache가 아닙니다.

Controller는 결정 객체를 반환하고 Runtime이 안내·합성 오류·halt를 소비합니다. 차단된 호출은 실제 실행 결과처럼 실패 카운터에 다시 넣지 않습니다. 이 판단은 반복/실패 제어이며 업무 결과의 진실을 검증하는 모델이 아닙니다.

### 발표 포인트

실패를 몇 번 했는지뿐 아니라 그 사이에 진전이 있었는지를 봅니다.

### 코드 표시

실제 Controller 메서드 기반 제어 흐름 예시. execute/name/args/after/seen은 설명용 변수이며 원문 전체 실행 코드가 아니다.

### 화면 읽기

반복되는 호출을 판단하려면 호출의 이름뿐 아니라 인자와 변화 여부가 중요합니다.

### 적용 예와 확인할 경계

A17을 다른 날짜로 다시 조회하는 상황과 같은 인자를 반복하며 진전이 없는 상황을 구분해 봅니다.

## HGUARDCONFIG — 기본 경고와 강제 중단의 차이

## 기본 경고와 강제 중단의 차이

### 주요 개념

**기본값**: 경고 true, interactive hard stop false, non-interactive hard stop true입니다.

**한도**: loop_caps의 web_search와 subagent 기본 한도는 각각 turn당 50이며 0은 해당 cap 해제입니다.

### 설명

ToolCallGuardrailConfig.from_mapping은 nested warn_after/hard_stop_after를 읽고, 알려진 대화형 platform 이외의 비어 있지 않은 platform에서는 non_interactive_hard_stop_enabled에 따라 hard stop을 켭니다. 고정 소스의 attended 집합은 cli/tui/desktop/acp/subagent/api_server입니다. api_server를 무조건 무인으로 묶지 않습니다.

Exact failure는 같은 인자 실패가 2회 누적되면 안내, hard stop을 켰을 때 5회 누적 뒤 다음 before_call에서 차단합니다. 같은 Tool 실패는 3회 경고/8회 halt가 기본이지만 failure-tolerant 도구·진전·throttle 등 예외가 있습니다. 따라서 모든 여섯 번째 Tool이 차단된다는 예로 일반화하지 않습니다. loop_caps는 이 soft/hard switch와 독립적으로 적용합니다. 무인 점검에서는 cap·예산·종료 결과를 함께 관측하고, 대화형 진단에서는 의도된 반복을 오탐하는지 확인합니다.

### 발표 포인트

threshold는 실패 분류·진전·표면 조건과 함께 해석합니다.

### 화면 읽기

경고를 모델에 알려주는 동작과 추가 실행 자체를 막는 동작을 구분합니다.

### 적용 예와 확인할 경계

발표 버전의 기본 설정과 데모에서 별도로 켠 제한을 혼용하지 않습니다. 마지막 Tool이 실제로 실행됐는지 기록을 봅니다.

## HHOOK — 필요한 실행 정책을 Hook으로 추가하기

## 필요한 실행 정책을 Hook으로 추가하기

### 주요 개념

**정책 반환**: pre_tool_call은 block 또는 modify(args)로 실행에 개입할 수 있습니다.

**실패 처리**: 고정 코드의 pre_tool_call은 예외/timeout/still-running에서 차단 directive를 생성합니다.

### 설명

Plugin register(ctx)에서 register_hook을 쓰는 활용 예시이며 기본 내장 정책 코드 자체를 복사한 것은 아닙니다. Tool executor는 get_pre_tool_call_directive 계열의 결과를 검사해 block/modify를 적용합니다. 다른 write_file·MCP 도구를 허용한 상태에서는 terminal만 막아도 전체 read-only가 되지 않습니다. 필요한 전체 Toolset/Backend 권한도 따로 제한해야 합니다.

중요한 코드 대조 결과: observer 문서의 일반적인 fail-open 설명을 모든 Hook에 적용하면 부정확합니다. plugins_dispatch.py의 _HOOK_TIMEOUT_FAIL_CLOSED_HOOKS={pre_tool_call}이며 timeout/이미 실행 중/예외에 block을 반환합니다. 기본 plugins.hook_callback_timeout은 30초, timeout<=0 등 설정 예외가 있습니다. 일반 pre/post API 관측 callback은 실패를 기록하고 건너뛰는 경로입니다.

Middleware의 tool_request는 인자를 먼저 바꾸고 그 유효 인자로 정책·guardrail·승인을 평가하게 합니다. middleware 자체의 실패는 fail-open 경로가 있으므로 반드시 차단해야 하는 정책을 단순 인자 수정 callback 하나에만 의존시키지 않습니다. Hook 종류와 Inline/Registry 적용 범위를 확인해야 합니다.

### 발표 포인트

이 예시는 terminal 차단이며 모든 파일·외부 쓰기를 막는 완전한 조회 모드는 아닙니다.

### 코드 표시

공식 Plugin API를 사용한 제한된 사용자 정책 예시. 전체 보안 정책이나 설치된 Plugin이 아니다.

### 화면 읽기

Hook은 특정 실행 경계에서 정책을 추가하는 지점입니다.

### 적용 예와 확인할 경계

예를 들어 발행 도구만 matcher로 고른 뒤 인자에 따라 승인 요청을 반환합니다. Hook이 본 값을 실제 실행 인자와 대조합니다.

## HTRACEBASE — Hermes에 기본으로 남는 기록은 무엇일까?

## Hermes에 기본으로 남는 기록은 무엇일까?

### 주요 개념

**Session / 로그**: 대화·호출 결과 보존과 실행 중 INFO/WARNING 진단은 다른 데이터입니다.

**외부 관측**: 라이프사이클 소비자·Exporter를 연결해야 원하는 Span을 수집할 수 있습니다.

### 설명

hermes_logging.setup_logging은 프로필 home/logs에 agent.log와 errors.log 등을 구성합니다. agent.log 기본 INFO, 5MB/backup 3이며 errors.log는 구현에서 WARNING, 2MB/backup 2로 별도 지정합니다. security.redact_secrets 기본 true의 formatter를 사용하지만 모든 PII의 완전 제거를 보장하지는 않습니다. Session SQLite 기록과 이 일반 로그를 상세 API payload capture로 혼동하지 않습니다.

AIAgent의 save_trajectories 기본은 false이며 opt-in이면 ShareGPT 형식의 JSONL 기록을 저장하는 경로가 있습니다. moa.save_traces도 기본 false입니다. monitoring.gateway_health_export.enabled와 monitoring.export.otlp.enabled는 모두 기본 false입니다. 이 OTLP 경로는 내용 없는 서비스 건강·운영 진단용이며 대화/Tool args/results trajectory와 다릅니다.

Observer는 built-in 소비자와 Plugin 소비자를 lifecycle에서 함께 호출합니다. 설정된 Relay 공유 metrics 등의 경로는 별도 계약입니다. 기본적으로 외부 전체 대화 Trace가 자동 생성/전송된다고 설명하지 않습니다. 목적에 맞춰 보존 기간·필드·Exporter를 선택합니다.

### 발표 포인트

Session 기록만으로 모든 API 시도의 지연·재시도를 복원할 수는 없습니다.

### 화면 읽기

세션에 남는 메시지, 로그, 추가 Hook에서 얻는 이벤트의 관측 범위가 다릅니다.

### 적용 예와 확인할 경계

답변과 Tool 반환은 대화 이력에서 읽을 수 있어도 전송 지연이나 정책 판정까지 모두 같은 파일에 남는 것은 아닙니다.

## HOBSERVER — Observer Hook으로 실행 경계를 연결하기

## Observer Hook으로 실행 경계를 연결하기

### 주요 개념

**API 이벤트**: 요청 준비 뒤 pre, 성공 응답 post, 실패/복구 경로 api_request_error를 보냅니다.

**Tool 이벤트**: 완료뿐 아니라 blocked/cancelled/error에도 terminal post 이벤트를 제공하는 경로입니다.

**부모·자식**: 명시적인 session/turn 식별자로 위임 관계를 구성합니다.

### 설명

turn_api_request._fire_pre_api_request_hook은 has_hook으로 소비자를 확인한 뒤 effective request를 전송합니다. turn_response_check 및 api_request_hooks의 성공/오류 경로에서 사용량·지연·종료 이유·에러 정보를 제공합니다. tool_executor는 호출의 한 terminal post_tool_call을 소유하며 block/cancelled도 닫히게 처리합니다. transform_tool_result는 post 이후 모델에 들어갈 표현을 바꾸는 별도 Hook입니다.

주의: 코드의 api_request_id는 conversation_loop에서 바깥 논리 반복 번호로 생성하며 안쪽 retry에서 재사용될 수 있습니다. 문서의 per-attempt 설명만 보고 이를 고유 HTTP span ID로 쓰면 덮어쓸 수 있습니다. api_request_id를 opaque correlation key로 두고 timestamp/retry_count/수집 측 attempt index를 더해야 합니다. api_duration은 초, Tool duration_ms는 밀리초이므로 단위를 맞춥니다.

on_session_end는 run/turn 종료 이벤트이고 session identity의 최종 종료와 같지 않습니다. 장기 session 정리는 on_session_finalize/reset을 봅니다. approval 관측 Hook의 반환으로 승인을 대신 응답할 수는 없고 차단 정책은 pre_tool_call에서 수행합니다.

### 발표 포인트

발생 순서만 보고 연결하지 않고 명시적인 ID와 시간 정보를 사용합니다.

### 화면 읽기

전송 전후와 도구 실행 전후 이벤트를 관측 가능한 경계로 사용합니다.

### 적용 예와 확인할 경계

시간이 가까운 로그만으로 연결하면 병렬 호출에서 틀릴 수 있습니다. 세션·요청·Tool Call 식별자를 사용합니다.

## HTRACECODE — 짧은 Plugin으로 API 관측을 시작하기

## 짧은 Plugin으로 API 관측을 시작하기

### 주요 개념

**등록**: register_hook으로 원하는 이벤트를 구독하고 Plugin을 활성화해야 합니다.

**Sanitizer**: JSON 호환 변환·민감 key 마스킹·문자열/시퀀스/전체 크기 제한을 적용합니다.

### 설명

코드는 실제 공식 API를 사용하는 사용자 Plugin 예시이며 실행·설치하지 않았습니다. 기존 Hermes logging 설정이 적용된 환경에서 turn/request/duration만 INFO로 남기는 최소 형태입니다. Tool/approval/subagent는 해당 Hook과 callback을 추가하고 parent/child 관계 및 상태를 별도로 저장해야 합니다. 네트워크 Exporter는 queue/batch/retry를 구성하고 callback에서 긴 blocking IO를 피하는 편이 적절합니다.

api_request_hooks._hook_jsonable 기본은 depth 8, string 8000자, sequence 200개이고 api_key/authorization/cookie 등의 key를 가립니다. 전체 payload 기본 cap은 HERMES_PLUGIN_PAYLOAD_MAX_CHARS=50000이며 줄인 cap 후에도 크면 preview로 축소합니다. 따라서 payload가 원문과 동일하다고 가정하지 않습니다. 이 key 기반 sanitizer는 프롬프트 문자열 속 모든 credential·개인정보를 의미적으로 탐지하는 보증도 아닙니다. legacy compatibility fields보다 sanitized request/response/error를 사용하고 Export 전 별도 마스킹·최소화를 검토합니다.

### 발표 포인트

관측 callback의 성공 여부가 작업 성공 여부와 같지는 않습니다.

### 코드 표시

공식 Plugin 등록 API 기반 실행 가능한 형태의 최소 사용자 예시. Hermes 내장 Plugin 원문/실행 결과가 아니다.

### 화면 읽기

Plugin은 실행 흐름의 경계에서 필요한 필드를 수집합니다.

### 적용 예와 확인할 경계

모델 요청을 관측할 때 헤더나 자격 증명 대신 요청 ID·모델·메시지 역할처럼 설명에 필요한 항목을 고릅니다.

## HTRACEUSE — Trace로 무엇을 확인하고 개선할까?

## Trace로 무엇을 확인하고 개선할까?

### 주요 개념

**진단**: 에러 타입·status·reason과 ID를 연결해 모델 장애/정책 차단/도구 실패를 분리합니다.

**평가**: Trace는 실행 근거이며 계산 정확성·근거 문서 버전·권한 적합성은 업무 평가 기준이 필요합니다.

### 설명

표시는 가상 이벤트이며 요청·실행 또는 성능 실측을 한 것이 아닙니다. 같은 api_request_id에 실패/성공 이벤트가 이어질 수 있으므로 한 ID에 마지막 값을 덮어쓰는 저장 구조를 피합니다. 이벤트 시각과 retry_count/수집 순번을 보존하고 Tool Call ID 및 parent/child 관계를 연결합니다.

사용량은 실제 응답 usage를 정규화해 집계하되 실패 시 usage 누락, 공급자 캐시/과금 방식, auxiliary model과 자식 비용을 구분해야 합니다. API duration과 전체 turn latency는 승인 대기·Tool·재시도·자식 시간 때문에 다릅니다. blocked status는 미실행일 수 있고 ok status도 업무 정답을 보증하지 않습니다. 앞서 설명한 Guardrail 경고/차단과 Memory/Skill 쓰기의 반환·파일 확인을 Demo 관찰 지점으로 연결합니다.

### 발표 포인트

실행 완료·정책 통과·업무 정답 여부를 별도의 기준으로 평가합니다.

### 화면 읽기

Trace는 어느 구간에서 대기·재시도·실패가 일어났는지 확인하는 자료입니다.

### 적용 예와 확인할 경계

모델 시간이 길어진 경우와 사람이 승인할 때까지 기다린 경우를 나누면 개선 대상이 달라집니다.

## HTRACESHARE — 실행 대화를 Trace Viewer로 공유하는 경로

## 실행 대화를 Trace Viewer로 공유하는 경로

### 주요 개념

**변환**: build_trace_jsonl은 system을 제외하고 Tool Call/Result를 Viewer용 메시지로 바꿉니다.

**기본 옵션**: upload_session_trace의 redact/private 기본값은 모두 true이며 자동 업로드가 아닙니다.

### 설명

agent/trace_upload.py는 SessionDB에서 messages/meta를 읽고 build_trace_jsonl로 Claude Code JSONL shape을 만듭니다. assistant tool_calls는 tool_use, Tool 결과는 user 형태의 tool_result로 바꾸며 uuid/parentUuid로 순서를 연결합니다. 포맷 이름은 Hermes가 Claude Code 내부 Runtime을 사용한다는 의미가 아닙니다.

코드는 base_ts=_now_iso()를 export 시 한 번 정하고 각 행에 넣습니다. 따라서 이 Viewer의 timestamp 차이로 원래 API 지연을 계산하면 안 됩니다. 실제 latency는 앞의 Observer 이벤트에서 수집해야 합니다. 토큰과 huggingface_hub 의존성을 확인한 뒤 private dataset의 sessions/<id>.jsonl에 명시 업로드합니다. redact=true는 force=True로 redactor를 적용하고 마스킹 실패/변환 JSON 오류 시 업로드를 거부합니다.

실제 외부 업로드는 하지 않았습니다. 일반 로그 redaction과 이 export redaction, Observer key sanitizer는 적용 범위가 다릅니다. 업무상 민감 데이터·경로·사용자 메시지는 공유 전에 직접 검토할 대상입니다.

### 발표 포인트

내보내기 전 원문·비밀값·공유 범위를 검토합니다.

### 코드 표시

실제 내보내기 경로의 도식. 외부 업로드나 인증 요청을 실행하지 않음.

### 화면 읽기

Trace Viewer에 전달할 수 있는 대화 데이터와 운영 감사 데이터의 용도가 다릅니다.

### 적용 예와 확인할 경계

합성 대화의 Tool 인자·출력만 공유하는 경우에도 사용자 식별자와 민감한 파일 경로가 있는지 점검합니다.

## HLONG — 위임

## 긴 작업과 위임

### 주요 개념

**긴 작업과 위임**: 입력의 크기와 실행 단위를 확장합니다.

### 설명

다음 범주를 시작하는 전환 장표입니다. System Prompt·압축 → 병렬 Tool → Subagent·다중 모델 순서로 살펴봅니다.

### 발표 포인트



### 화면 읽기

위임은 부모가 작업을 정의하고 자식의 실행 결과를 회수하는 구조입니다.

### 적용 예와 확인할 경계

부모가 수율을 조회하고, 자식에게 통계적 의미를 검토시키고, 부모가 사용자에게 설명하는 예로 읽습니다.

## S14A — delegate_task는 자식을 어떻게 만들까?

## delegate_task는 자식을 어떻게 만들까?

### 주요 개념

**Child 설정**: 부모 설정을 바탕으로 모델·허용 Toolset·별도 반복 예산과 Task를 구성합니다.

**Context 격리**: 자식 메시지는 별도이며 goal/context와 허용된 프로젝트 지침 등을 전달합니다.

### 설명

화면은 실제 Tool schema 기반의 가상 tasks 요청입니다. delegate_tool.py와 delegate_tool_child_run.py는 입력 정규화·할당량·도구 제한·자식 AIAgent 생성과 등록을 나누어 처리합니다. 자식은 새 대화를 가지며 부모의 과거 Tool 결과를 자동으로 전부 이해한다고 가정하지 않습니다. workspace 프로젝트 지침 등 명시적 로더 예외는 존재합니다.

고정 DEFAULT_CONFIG의 자식 max_iterations 기본은 250이며 부모 상한과 별개입니다. MCP 상속·toolset 제한·worktree/credential 등은 설정과 Backend 조건을 확인해야 합니다. 파일·DB·secret 권한 격리는 Context 분리와 다르며 Task 분리만으로 운영 격리가 보장되지는 않습니다.

### 발표 포인트

자식이 알아야 할 데이터·버전·작업 범위를 context에 명시합니다.

### 코드 표시

공식 Tool schema에 맞춘 설명용 인자. 실제 호출 Trace 또는 공개 Python SDK 예제가 아님.

### 화면 읽기

delegate_task의 입력이 자식 실행의 목표와 환경 선택에 연결됩니다.

### 적용 예와 확인할 경계

부모 대화에서 필요한 값은 작업 설명에 명시합니다. 자식이 부모 대화 전체를 알고 있다고 가정하면 근거가 누락될 수 있습니다.

## HCHILD — 자식 실행과 결과 전달의 세부 경로

## 자식 실행과 결과 전달의 세부 경로

### 주요 개념

**실행**: _run_batch와 _run_children_parallel 등이 자식 실행·상태·중단·정리를 관리합니다.

**Background**: 최상위 요청은 handle을 먼저 반환하는 경로가 있으며 결과 전달은 실행 완료와 별도입니다.

### 설명

확인한 고정 소스에서 _run_batch는 동기/백그라운드 실행 경로를 나누고 background 응답에는 dispatched 상태·delegation_id·자식 식별자 등이 담길 수 있습니다. orchestrator 자식이 worker를 기다리는 경로와 최상위 사용자 대화의 background 전달을 동일한 동기 반환 그림으로 합치지 않습니다.

output_schema 검증 실패 시 제한된 수정 turn을 주고 최종 실패는 원문 summary를 버리지 않고 schema_valid=false와 오류를 표시하는 경로입니다. 실제 필드는 버전·경로에 따라 확인합니다. 자식 background 프로세스의 수명도 자식 정리에 연결될 수 있어 서버를 띄우고 ID만 반환하면 부모 소유가 된다는 가정은 피합니다. 비용·partial·중단·전달 실패를 함께 관찰합니다.

### 발표 포인트

Child 완료와 결과의 구조·업무 정확성 통과는 별개입니다.

### 화면 읽기

자식의 호출 예산·도구·반환값은 부모가 받은 최종 위임 결과와 구별해 읽습니다.

### 적용 예와 확인할 경계

자식 실행 중 오류가 나면 어떤 실패 정보가 부모의 Tool 결과로 돌아왔는지 확인합니다.

## HMULTI — Hermes는 delegate_task만 사용할까?

## Hermes는 delegate_task만 사용할까?

### 주요 개념

**Delegation**: 목표를 쪼개 독립 Agent가 실행하고 부모가 결과를 사용하는 방식입니다.

**MoA**: 여러 reference 모델 분석을 aggregator가 사용하며 acting model의 정상 Agent Loop를 유지합니다.

**Kanban**: Task/board와 profile worker를 활용하는 지속 작업 조정 기능입니다.

### 설명

delegate_task만이 유일한 멀티에이전트 방식이라고 결론내릴 수 없습니다. 고정 태그의 Mixture of Agents는 moa 가상 Provider의 reference/aggregator 모델 구성이며, aggregator가 실제 응답·Tool Call을 내는 acting model입니다. 각 reference가 모두 별도의 업무 Tool Loop를 맡는 Subagent와 다릅니다. Kanban은 Board·Task·Profile·worker의 지속 작업 상태를 조정하는 다른 수준의 기능입니다.

delegate_task는 한 대화에서 하위 목표를 독립 Context·Toolset·예산으로 맡기고 반환받는 데 적합한 설계입니다. MoA는 여러 모델의 관점 합성, Kanban은 지속 작업 조정에 쓰는 선택지입니다. 이 비교는 확인한 대표 방식이며 Hermes의 모든 orchestration 확장을 전수 열거했다는 뜻은 아닙니다. 추가 기능의 배포/복구 구조는 이번 발표 범위에서 상세 설명하지 않습니다.

### 발표 포인트

작업 위임과 다중 모델 합성, 보드 기반 협업을 구분합니다.

### 화면 읽기

런타임 내부 위임과 별도의 세션·모델 조합은 실행 주체와 결과 전달 방식이 다릅니다.

### 적용 예와 확인할 경계

누가 다음 작업을 정하며 누가 결과를 합치는지 물으면 기능 이름이 달라도 구조를 비교할 수 있습니다.

## HCRON — 예약 실행과 활용

## 예약 실행과 활용

### 주요 개념

**예약 실행과 활용**: 반복 작업을 예약하고 실행 상태를 직접 다룹니다.

### 설명

다음 범주를 시작하는 전환 장표입니다. Cron 구조 → 생성·관리 명령 → Session·Skill 활용 순서로 살펴봅니다.

### 발표 포인트



### 화면 읽기

이제 현재 대화에 대한 반응에서 시간을 기준으로 실행하는 작업으로 넘어갑니다.

### 적용 예와 확인할 경계

매일 검사 추세를 조회하는 작업에서는 실행 시각과 결과 전달 위치, 실패 기록을 각각 정합니다.

## S14C — Cron으로 예약 작업 실행하기

## Cron으로 예약 작업 실행하기

예약 시각이 되면 새 Agent 작업을 시작하고 결과를 전달합니다.

Agent 작업 모드의 Cron은 Gateway tick 또는 관리형 Trigger에서 실행 시각과 Lock/Claim을 확인하고 새 세션을 구성한 뒤 Prompt와 첨부 Skills 등을 사용해 Loop를 실행합니다. jobs.json, pending_slot과 next-run 관리의 세부 동작은 문서·코드 태그를 함께 확인합니다. 새 Session이라도 지속 Memory와 Skills는 로드될 수 있어 완전 stateless로 설명하지 않습니다.

예약 회차 중복 시작을 줄이는 것과 외부 API/DB 효과가 정확히 한 번 발생하는 것, 결과가 사용자에게 전달되는 것은 다릅니다. 멱등성·효과 확인·전달 재시도는 대상 시스템과 업무 설계가 필요합니다. 공식 문서에는 no-agent script 모드도 있어 Cron을 무조건 Agent 실행이라고 일반화하지 않습니다. 사전 Script가 실행되면 Tool 승인과 같은 정책이 자동 적용된다고 보지 않으며 무인 승인·권한을 별도로 확인합니다.

실행 슬롯의 중복 방지는 외부 작업의 exactly-once 보장과 다릅니다.

### 화면 읽기

Cron 항목은 일정, 실행할 작업, 전달 경로를 결합합니다.

### 적용 예와 확인할 경계

실행 환경에서 사용자 승인을 받을 통로가 있는지와 작업이 어떤 입력을 참조하는지 확인합니다.

## HCRONUSE — Cron 작업을 만들고 관리하기

## Cron 작업을 만들고 관리하기

### 주요 개념

**예약 명령**: /cron add와 hermes cron create는 서로 다른 입력 표면입니다.

**cronjob_manage**: 모델이 create/list/update/pause/resume/run/remove 등의 action으로 관리하는 Tool입니다.

### 설명

표시 예시는 공식 /cron add "every 2h" "..."와 standalone CLI의 positional schedule/prompt 문법을 따릅니다. 실제 예약을 생성한 것은 아닙니다. 5필드 cron·상대 지연·반복 간격·ISO 시각 등 지원 표현과 시간대를 확인합니다.

자연어 요청도 내부적으로 cronjob_manage로 이어질 수 있습니다. 고정 문서의 일부 예제에는 cronjob이라는 옛 표기가 남아 있어 함수 이름을 그대로 복사하지 않고 현재 Tool 이름과 CLI 문법을 구분했습니다. 첨부 Skills, 실행 경로, 모델 선택·인증·무인 승인·전달 조건은 실제 환경에 맞게 검증해야 합니다. 생성/일시중지/재개/수동실행/삭제는 별도 동작입니다.

### 발표 포인트

schedule 표현과 prompt, 권한·전달 대상을 함께 확인합니다.

### 코드 표시

공식 command 문법 기반 예시. 실제 예약 생성/실행은 하지 않았다.

### 화면 읽기

생성, 목록 조회, 변경, 삭제는 예약 정의를 관리하는 동작입니다.

### 적용 예와 확인할 경계

시험 실행의 성공과 다음 예약이 실제로 트리거됐는지는 별도 실행 기록으로 확인합니다.

## HCRONTRADE — Cron은 언제 유용하고 무엇을 주의할까?

## Cron은 언제 유용하고 무엇을 주의할까?

### 주요 개념

**적합한 활용**: 주기적 조회·점검·요약처럼 시간 조건이 명확하고 결과를 검토할 수 있는 작업입니다.

**모드와 권한**: Agent 모드와 no-agent Script 모드를 구분하고 외부 효과·무인 정책을 별도로 확인합니다.

### 설명

Hermes Cron의 강점은 일정 표현, reusable Skill, fresh Agent session, 저장·전달이 제품 기능으로 연결된다는 점입니다. 반면 모델 호출비, 인증과 실패 알림, 재시도·중복 부작용·결과 누락을 운영해야 합니다. 새 Session도 지속 Memory/Skills를 읽을 수 있어 완전 stateless하지 않습니다.

회차 Lock/Claim/receipt와 외부 대상 시스템의 멱등성, Delivery 보장은 다른 문제입니다. no-agent는 Script 실행과 stdout 전달 경로이며 비용·권한·오류 형태가 Agent 모드와 다릅니다. 사용자 코드의 권한과 Tool approval을 혼동하지 않습니다. 이벤트 기반·장기 복구 요구는 다른 trigger/workflow 설계와 비교할 사안입니다.

### 발표 포인트

예약 회차 Claim이 외부 작업과 전달까지 exactly-once로 만들지는 않습니다.

### 화면 읽기

반복 점검의 자동화는 시간을 절약하지만 무인 실패와 중복 실행을 운영해야 합니다.

### 적용 예와 확인할 경계

결과 전달 실패 뒤 재실행할 수 있다면 같은 날 보고서를 두 번 발행하지 않도록 업무 식별자를 둡니다.

## HCOMMAND — 구조를 알고 쓰면 유용한 Hermes 명령

## 구조를 알고 쓰면 유용한 Hermes 명령

### 주요 개념

**/new**: 새 Session ID·History로 작업 경계를 만들고 Memory snapshot을 다시 읽는 계기입니다.

**/learn**: 자료·경험을 바탕으로 Skill을 저술하는 진입점이며 지식 검증을 자동 보장하지 않습니다.

### 설명

새 작업·주제 전환에서 /new로 세션 경계를 만들면 지속 Memory를 다시 읽고 필요 시 과거 세션을 검색하는 사용 흐름을 설명하기 쉽습니다. /learn은 문서나 경험을 재사용 Skill로 만들도록 요청하는 기능이며 생성 절차·지원 파일을 검토해야 합니다.

/skills diff <id>는 write_approval을 켜 보류된 변경이 있을 때 검토하는 명령이며 기본 false 환경에서 모든 쓰기가 반드시 pending이라고 설명하지 않습니다. /memory pending/approve/reject와 /skills pending/approve/reject도 관리하는 subsystem이 다릅니다. 설치된 Skill의 /skill-name은 built-in 명령과 충돌 시 fallback을 확인해야 합니다.

### 발표 포인트

명령의 이름보다 무엇이 바뀌고 언제 반영되는지를 확인합니다.

### 화면 읽기

명령은 세션 상태를 확인하거나 특정 실행 경로를 제어하는 진입점입니다.

### 적용 예와 확인할 경계

사용 중인 CLI·Gateway 표면에서 명령의 지원 범위를 확인합니다. 동일한 명령이 모든 입력 표면에서 같은 효과를 내는 것은 아닙니다.

## S15 — Hermes Demo

## Hermes Demo

### 개념

**관찰 단위**: 사용자 요청→모델 입력→Tool Call/Result→세션·파일 변경을 ID로 연결합니다.

**Memory 확인**: 실제 Tool 반환과 파일 diff, 현재 snapshot/다음 세션을 나누어 봅니다.

**실행 기록의 구분**: live·사전 기록·fixture를 표시하고 이번 실행에서 일어나지 않은 기능을 시연한 것처럼 표시하지 않습니다.

### 설명

합성 검사 데이터로 루프, 모델 요청, 세션 검색, Tool과 Hook, 승인, 가드레일, Skill, 위임을 각각 실행합니다. 요청과 Tool 인자·반환은 해당 실행에서 실제로 관측된 값을 확인합니다.

발표의 연결 페이지는 Hermes 실행 화면(18000)을 엽니다. Hermes 런타임은 10000번의 OpenAI 호환 모델 endpoint에 요청합니다. 모델 endpoint와 데모 서비스는 각각 실행해야 합니다.

### 발표 포인트

기본 흐름을 먼저 확인하고, 확장 기능은 실제 발생한 경로만 살펴봅니다.

### 학습자료 근거

심층 학습 §3·8·11·14; 기초 학습자료 및 추가 코멘트와 대조. 구현 설명·문서 설명·업무 설계 제안을 구분한다.

### 화면 읽기

Context와 Tool Demo를 각각 열어 입력 데이터와 모델의 실행 제안을 구별합니다.

### 적용 예와 확인할 경계

합성 A17의 Tool 반환을 다음 모델 요청의 Tool 메시지에서 찾습니다. 모델이 예상한 호출을 내지 않으면 그 실행 결과를 그대로 읽습니다.

## CLAUDE — Claude Code

Claude Code는 프로젝트를 읽고 도구를 호출하며 결과를 확인하는 코딩 Harness입니다. 도식은 CLI와 SDK에서 접근하는 실행 구조를 설명합니다. 로컬 교재의 비교 기준은 CLI v2.1.314입니다. 현행 문서의 기능은 각 기능에 필요한 제품 버전과 설정을 따릅니다.

### 화면 읽기

코딩 Harness로서 프로젝트 규칙과 파일·셸 도구가 실행을 좌우합니다.

### 적용 예와 확인할 경계

공개 문서로 확인 가능한 입출력과 설정으로 설명합니다. 내부 Python 함수 구조를 Hermes와 대응시키지 않습니다.

## CC01 — 코딩 작업은 어떻게 진행될까?

Hermes에서 본 모델·Tool·관찰의 반복을 그대로 연결해 설명합니다. Claude Code에서는 지침을 읽는 시점, Tool을 공개하는 방식, 권한 판정과 위임이 개입하는 지점을 살펴봅니다. 이 도식은 공식 문서의 동작을 요약한 개념도입니다.

### 화면 읽기

저장소 탐색, 코드 수정, 테스트 결과 확인이 한 작업에서 반복됩니다.

### 적용 예와 확인할 경계

실패한 테스트 출력은 다음 판단의 입력입니다. 편집이 성공했다는 응답만으로 검증이 끝나지 않습니다.

## CCA — Context와 기억

먼저 요청의 논리 계층을 소개하고 프로젝트 지침과 기억 파일이 어느 시점에 들어오는지 살펴봅니다. 대화 재개와 저장소 파일의 현재 상태도 구분합니다.

### 화면 읽기

지금부터 프로젝트 규칙, 자동 저장 기억, 대화 이력이 어느 시점에 읽히는지 구분합니다.

### 적용 예와 확인할 경계

팀의 규칙은 프로젝트 문서에서, 과거 실행의 단서는 Auto Memory와 이력에서 찾을 수 있습니다.

## CC02 — 모델 입력의 세 계층

공식 캐싱 문서가 설명하는 System, Project, Conversation의 논리적 계층입니다. 도구 가용성이나 설정이 바뀌면 앞쪽 입력도 달라질 수 있습니다. 각 계층은 이해를 위한 묶음이며 실제 요청의 필드와 메시지 배열은 연결 방식에 따라 확인합니다.

### 화면 읽기

기본 지시, 프로젝트 지시, 실행 중 추가된 문맥을 별도 계층으로 읽습니다.

### 적용 예와 확인할 경계

현재 파일이나 Tool 출력이 모델 입력에 추가되더라도 항상 세션 전체의 고정 규칙이 되는 것은 아닙니다.

## CC03 — 어떤 지침을 언제 읽을까?

관리형, 사용자, 프로젝트 지침이 적용되는 위치를 먼저 구별합니다. 현행 문서에서 instructionFiles 기본값은 claude-md-or-agents-md입니다. 작업 디렉터리와 상위 경로에 CLAUDE.md 또는 CLAUDE.local.md가 없을 때 AGENTS.md를 읽습니다. claude-md-and-agents-md로 둘 다 읽을 수 있습니다. 내장 Plugin 비활성이나 이전 버전에서는 CLAUDE.md의 @AGENTS.md import를 사용할 수 있습니다. 직접 로딩은 InstructionsLoaded를 발생시키지 않으며 import는 해당 이벤트를 발생시킵니다.

### 화면 읽기

어디에 둔 지침이 어느 디렉터리에서 적용되는지 보는 장입니다.

### 적용 예와 확인할 경계

상위 프로젝트 규칙과 하위 디렉터리 규칙의 적용 범위를 확인합니다. 모든 지침 파일을 처음에 읽는다고 가정하지 않습니다.

## CC04 — Auto Memory는 색인부터 읽습니다

Auto Memory를 활성화한 환경에서 저장소별 기억은 worktree 사이에 공유됩니다. 시작 로딩은 200줄과 25KB 중 먼저 도달한 한도까지이며 상세 파일은 필요할 때 읽습니다. Hermes의 기억 파일과 비교할 수 있고, Hermes의 Session FTS는 이전 대화를 검색하는 별도 기능입니다. Claude Code의 resume 역시 대화 이력을 이어가는 별도 동작입니다.

### 화면 읽기

Auto Memory의 색인은 무엇을 다시 읽을지 찾는 데 쓰입니다.

### 적용 예와 확인할 경계

색인 항목과 세부 토픽 파일을 구분합니다. 자동 기억에 남은 내용은 현재 저장소 상태와 다시 대조합니다.

## CCB — Tools와 Skills

모델에 도구 이름과 스키마가 공개되는 시점부터 살펴봅니다. 이어서 Skill 본문과 권한의 수명, 여러 구성 요소를 배포하는 Plugin을 설명합니다.

### 화면 읽기

프로젝트 밖의 실행 기능과 반복 절차를 연결합니다.

### 적용 예와 확인할 경계

MCP 도구는 실제 실행 계약이고 Skill은 선택해서 읽는 절차입니다. Plugin은 관련 설정을 묶어 배포할 수 있습니다.

## CC05 — 필요한 MCP Tool의 명세를 불러오기

지연 로딩으로 시작 요청에 들어가는 전체 도구 명세의 양을 줄입니다. ENABLE_TOOL_SEARCH=auto는 10% 임계값 모드이고 auto:N은 비율을 지정합니다. 비호환 모델이나 일부 제공자 경로에서는 먼저 로딩할 수 있습니다. Gateway가 beta 헤더나 defer_loading을 처리하는지도 확인합니다.

### 화면 읽기

MCP 서버가 가진 도구와 현재 요청에 상세 명세가 포함된 도구를 구분합니다.

### 적용 예와 확인할 경계

도구 탐색이 켜져 있다면 검색으로 상세 명세를 가져온 뒤 실제 호출을 별도로 보냅니다.

## CC06 — Skill 본문과 권한의 수명

Skill의 이름과 설명으로 호출 여부를 판단하고 호출 시 본문을 읽습니다. 사용자나 모델의 호출 가능 여부는 frontmatter로 제어할 수 있습니다. allowed-tools는 해당 호출 턴에서 지정 도구의 사전 승인을 다룹니다. 사용 가능한 도구 자체를 제한하는 disallowed-tools나 관리형 권한과 적용 범위가 다릅니다.

### 화면 읽기

Skill 선택, 본문 로딩, 호출 중 도구 허용 범위를 구분합니다.

### 적용 예와 확인할 경계

배포된 Skill의 allowed-tools는 모든 세션에 영구 적용되는 전역 권한으로 해석하지 않습니다.

## CC07 — Skill fork와 대화 fork의 입력

Skill의 context: fork는 Skill 내용을 별도 Subagent에게 작업으로 넘깁니다. agent 필드로 사용할 역할을 지정할 수 있습니다. 반대로 Subagent 설정의 skills는 자식 시작 때 지정한 지침을 미리 넣습니다. 대화 fork는 기존 대화를 분기하는 별도 경로입니다.

### 화면 읽기

Skill의 fork는 절차를 별도 실행 문맥에 전달하고 대화 fork는 기존 대화에서 분기를 만듭니다.

### 적용 예와 확인할 경계

같은 파일을 수정하는 두 대화 분기는 별도 작업 디렉터리가 없다면 파일 충돌을 일으킬 수 있습니다.

## CC08 — Plugin으로 작업 환경을 배포하기

Claude Code Plugin은 문서, 설정, 외부 연결을 묶는 배포 단위입니다. Hermes의 register(ctx)는 Python 확장 등록 인터페이스입니다. Claude Code에서 코드로 권한 판정에 관여하는 Mods는 Plugin manifest와 별도이며 적용 가능한 환경과 정책을 권한 장에서 확인합니다.

### 화면 읽기

Plugin을 설치하면 설정과 함께 명령·Skill·Hook 등의 기능을 연결할 수 있습니다.

### 적용 예와 확인할 경계

기능의 출처와 버전을 먼저 확인합니다. 설치했다는 사실만으로 도구의 외부 접근이 허용되지는 않습니다.

## CCC — 안전장치와 실행 기록

Permission, Hook, Sandbox가 각각 제어하는 범위를 살펴봅니다. 이어서 대화 기록과 별도로 수집할 수 있는 지표, 이벤트와 Trace를 비교합니다.

### 화면 읽기

권한 규칙은 허용 범위를, Hook은 실행 경계의 정책을, Trace는 실제 실행 기록을 다룹니다.

### 적용 예와 확인할 경계

쓰기 요청이 멈췄다면 권한 판정, Hook 결과, 실제 실행 여부를 따로 확인합니다.

## CC09 — 권한 규칙은 Tool 호출에 적용됩니다

예시는 규칙 우선순위를 설명하는 일부 설정입니다. 적용 규칙은 사용자·프로젝트·관리형 설정을 확인합니다. Plan은 탐색 중심의 모드이고 Auto의 자동 판단은 지원 환경과 별도 정책을 따릅니다. 일반 Hook allow는 명시적인 deny/ask를 우회하지 않습니다. Mod tool.check가 개입하는 조건은 로그인, 모드와 관리형 설정에 따라 공식 권한 문서를 대조합니다.

### 화면 읽기

권한 규칙은 요청의 자연어만 보는 대신 실제 Tool 이름과 입력에 적용됩니다.

### 적용 예와 확인할 경계

파일 읽기, 수정, 셸 명령은 정책 적용 범위가 다를 수 있습니다. 세션의 권한 모드도 함께 확인합니다.

## CC10 — PreToolUse가 받는 입력과 돌려주는 결정

Command hook은 stdin의 JSON에서 tool_name과 tool_input을 읽고 stdout으로 결정 JSON을 돌려줍니다. 예를 들어 handler에서 보호 경로와 일치하는지를 검사하고 이 JSON을 출력합니다. 입력을 수정하는 updatedInput과 실행 허용 여부인 permissionDecision은 서로 다른 필드입니다. 실행 뒤의 PostToolUse는 앞서 일어난 부작용을 되돌리는 단계가 아닙니다.

### 화면 읽기

PreToolUse는 실행 전 Tool 이름과 인자를 받아 해당 이벤트가 허용하는 결정을 반환합니다.

### 적용 예와 확인할 경계

발행·삭제 명령 예시에서는 Hook이 본 입력, 권한 판정, 실제 Tool 호출 여부를 세 단계로 나눠 읽습니다.

## CC11 — Hook이 실패하면 실행은 계속될까?

실행 파일을 찾지 못하거나 명시적 거부 없이 종료 코드 1로 끝난 경우, 일반적으로 정책 결정이 없어 정상 권한 흐름으로 이어집니다. command/http Hook은 onFailure 설정으로 실패 차단을 요청할 수 있으며 플랫폼과 이벤트별 제약이 있습니다. SDK callback timeout의 동작은 별도입니다. Hermes의 실패 차단 Hook과 비교할 때 같은 실패 유형을 대응시킵니다.

### 화면 읽기

명령 Hook의 정상 출력, 차단 종료 코드, 기타 실패, 시간 초과를 구분합니다.

### 적용 예와 확인할 경계

이벤트·handler 종류·실패 시 차단 설정에 따라 결과가 다릅니다. 모든 Hook 오류를 차단이나 허용으로 일반화하지 않습니다.

## CC12 — Bash Sandbox가 제한하는 범위

Sandbox Runtime은 공개 부품입니다. 공개 API는 SandboxManager.initialize로 정책을 설정하고 wrapWithSandbox로 실행 명령을 감싸는 경로를 제공합니다. 이 API를 CLI 내부 호출의 증거로 쓰지 않습니다. 현행 Claude Code 문서는 네이티브 Windows에서 제품 Shell Sandbox가 적용되지 않는다고 설명합니다. 독립 Runtime의 플랫폼 지원과 제품 적용 범위는 별개입니다.

### 화면 읽기

Sandbox는 주로 셸 프로세스의 파일·네트워크 접근을 제한하는 실행 경계입니다.

### 적용 예와 확인할 경계

특정 도구 허용과 프로세스 격리를 별도로 봅니다. 플랫폼 및 실행 환경의 지원 여부도 확인합니다.

## CC13 — 지표, 이벤트, Trace는 무엇을 남길까?

로컬 대화 기록과 OpenTelemetry 수집은 목적과 수명이 다릅니다. 환경 변수로 telemetry와 exporter를 선택합니다. 분산 Trace는 CLAUDE_CODE_ENABLE_TELEMETRY=1, CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1, OTEL_TRACES_EXPORTER 설정을 조합해 활성화합니다. 상세 beta 수집과 사용자 입력, Tool 내용의 수집 조건은 별도로 확인합니다. Hermes와 비교할 때는 Gateway 상태 지표와 대화 실행 Trace의 기록 단위를 구분합니다.

### 화면 읽기

지표는 집계, 이벤트는 특정 사실, Trace는 실행 구간과 상관관계를 보여줍니다.

### 적용 예와 확인할 경계

토큰 사용량 집계만으로 어느 명령이 거절됐는지 알 수 없습니다. 로그 수집 항목과 민감 데이터 설정을 함께 봅니다.

## CC14 — 승인 대기와 실행 시간을 나눠 보기

도식은 공식 span 계층을 축약한 예시입니다. blocked_on_user와 execution의 전체 이름에는 claude_code.tool 접두사가 붙습니다. Tool 실패, 권한 거부와 API 오류는 발생 위치가 다릅니다. Agent SDK와 비대화형 실행은 조건에 따라 상위 TRACEPARENT를 이어받습니다. 사용자 입력, 도구 세부 정보, 상세 beta payload는 각 수집 조건을 확인합니다.

### 화면 읽기

사람이 승인할 때까지 기다린 시간과 Tool 자체가 실행된 시간을 분리합니다.

### 적용 예와 확인할 경계

두 시간의 원인이 다르므로 실행 ID로 승인 이벤트와 Tool 호출을 묶어 비교합니다.

## CCD — 긴 작업과 위임

Prefix Cache와 압축이 입력에 주는 영향을 설명합니다. 이어서 위임할 때 전달하는 Context, 작업 공간 격리와 복원 가능한 상태를 비교합니다.

### 화면 읽기

오래 실행되는 작업에서 모델 문맥, 별도 작업 단위, 복구를 나눠 봅니다.

### 적용 예와 확인할 경계

대화 압축과 자식 위임은 모두 문맥을 줄이는 데 쓰일 수 있지만 입력을 나누는 방식이 다릅니다.

## CC15 — 변경이 캐시에 미치는 범위

Hermes에서 본 Prefix Cache 원리와 연결합니다. 실제 무효화 범위는 변경된 입력 위치와 캐시 경계에 달려 있습니다. 예를 들어 SOP가 바뀌었어도 모델이 최신 파일을 다시 읽었는지는 별도로 확인해야 합니다. 캐시 효율과 업무 근거의 최신성을 같은 지표로 보지 않습니다.

### 화면 읽기

캐시를 판단할 때는 같은 앞부분이 어느 범위까지 유지되는지를 봅니다.

### 적용 예와 확인할 경계

프로젝트 지시, 도구 목록 또는 이력의 변경이 어느 지점에 적용되는지 확인합니다. 실제 비용 절감은 측정값으로 확인합니다.

## CC16 — 압축 뒤에는 무엇을 다시 읽을까?

압축 뒤 루트 지침이 다시 들어오는 동작, 파일 접근으로 발동하는 경로 규칙, 사용한 Skill의 제한된 재주입을 구분합니다. 요약에는 진행 상황을 남기고 정확한 파일 내용이나 수치가 필요하면 원본을 다시 읽습니다. 이 흐름은 문서의 로딩 규약을 설명하기 위한 가상 예시입니다.

### 화면 읽기

압축된 대화와 필요한 지침을 다시 읽는 경로를 구분합니다.

### 적용 예와 확인할 경계

요약 뒤에도 반드시 지켜야 할 프로젝트 규칙은 문서에 남기고, 직전 코드 상태는 실제 파일에서 확인합니다.

## CC17 — Subagent의 역할을 파일로 정의하기

Hermes와 공통인 위임 원리를 짧게 연결합니다. Claude Code는 Markdown frontmatter로 도구와 모델, permissionMode, memory, skills 등을 구성합니다. 일반 전문 Subagent는 별도 Context에서 작업을 시작합니다. 자식이 받는 시작 지침과 대화 범위는 자식 종류와 fork 여부에 따라 확인합니다.

### 화면 읽기

Subagent 파일은 역할·도구·모델 등 별도 작업 실행의 구성을 선언합니다.

### 적용 예와 확인할 경계

검토자에 읽기 도구만 제공하는 예에서는 역할 지시와 도구 사용 권한을 별도로 설정합니다.

## CC18 — 새 Context, 대화 fork, background

전문 역할을 별도로 시작하는 방법과 대화 분기를 구분합니다. Foreground와 background는 실행을 기다리는 방식의 차이입니다. 현행 제품 문서는 중첩 위임과 named-agent 메시징도 다룹니다. 권한과 가용성 조건을 확인하고 공개되지 않은 스케줄러 구현을 추정하지 않습니다.

### 화면 읽기

새 문맥으로 시작하는 위임, 대화 이력에서 분기하는 실행, 뒤에서 이어지는 실행을 구분합니다.

### 적용 예와 확인할 경계

별도 문맥이 별도 파일 환경을 뜻하지는 않습니다. 파일 수정이 겹치는 경우 작업 공간을 별도로 확인합니다.

## CC19 — Teams는 작업 목록과 메시지로 협업합니다

Teams의 핵심은 공유 작업 목록과 독립 세션 간 조정입니다. Subagent에서도 설정에 따라 메시징과 중첩 위임을 쓸 수 있으므로 통신 가능 여부만으로 두 구성을 구별하지 않습니다. 독립 작업의 비용, 충돌 가능성과 작업 상태를 함께 비교합니다.

### 화면 읽기

팀원 사이의 메시지와 작업 목록이 협업의 근거입니다.

### 적용 예와 확인할 경계

결과를 부모에게 한 번 반환하는 위임과 달리, 진행 중 누가 일을 맡고 어떤 결과를 공유했는지 확인합니다. 실험 기능의 지원 조건을 따릅니다.

## CC20 — 대화와 파일을 각각 복구하기

Worktree의 파일 격리와 Subagent의 Context 격리를 구분합니다. Checkpoint는 편집 도구가 추적하는 변경에 적용되며 모든 Bash 변경이나 외부 호출을 복원하는 범위로 확대할 수 없습니다. Background 실행의 변경도 main checkpoint와 함께 보장된다고 가정하지 않습니다. Hermes와는 checkpoint를 켜는 방식과 추적 범위를 비교합니다.

### 화면 읽기

대화 이력을 되돌리는 조작과 작업 파일을 되돌리는 조작은 복구 대상이 다릅니다.

### 적용 예와 확인할 경계

외부 서비스에 이미 반영한 변경이나 별도 셸 명령의 결과까지 자동 복구된다고 가정하지 않습니다.

## CCE — 예약과 활용

반복 작업을 등록할 때 실행 위치와 세션 의존성을 먼저 살펴봅니다. 이어서 프로젝트를 읽고 실행하고 검토할 때 활용할 명령을 소개합니다.

### 화면 읽기

사용자가 실행환경을 운영할 때 자주 쓰는 예약·탐색·검토 기능으로 넘어갑니다.

### 적용 예와 확인할 경계

작업을 어느 위치에서 실행하고 다음 세션에 무엇이 남는지 중심으로 봅니다.

## CC21 — 예약 작업은 어디에 남을까?

현재 문서의 Session 예약은 만료 여부와 저장 조건에 따라 resume 시 복원될 수 있습니다. 복원 가능한 예약과 세션이 꺼져 있는 동안 실제로 실행되는 예약은 별개의 조건입니다. Hermes Cron과 비교할 때 스케줄 저장 위치, 실행 프로세스, 만료와 복원 조건을 확인합니다.

### 화면 읽기

예약 기능의 수명과 실행 주체를 구분합니다.

### 적용 예와 확인할 경계

현재 세션에 묶인 반복 작업과 별도 실행 인프라를 사용하는 예약은 앱을 닫았을 때 동작이 다를 수 있습니다.

## CC22 — 탐색, 실행, 검토에 필요한 명령

코드 검토를 시작할 때 지침과 Context를 살피고 실행 전 권한과 Hook을 확인합니다. 대화가 길어지면 압축하고 다시 이어갈 때 세션을 선택합니다. 복구가 필요하면 대화와 파일의 복원 범위를 고릅니다. 명령의 가용성은 사용하는 버전과 인터페이스에서 확인합니다.

### 화면 읽기

명령을 기능 이름 대신 탐색, 제어, 검토 목적에 연결합니다.

### 적용 예와 확인할 경계

예를 들어 문맥 상태를 먼저 확인하고, 변경 작업을 한 뒤 별도 검토를 실행합니다. 설치 버전의 명령 도움말을 확인합니다.

## CC23 — 두 Harness에서 어디까지 바꿀 수 있을까?

업무 규칙을 수정하는 일과 Harness 실행기를 수정하는 일을 구분합니다. Hermes는 공개 코어를 직접 읽고 수정할 수 있습니다. Claude Code에서는 문서화된 설정과 확장 접점으로 필요한 동작을 구성합니다. Python Agent SDK의 공개 subprocess transport는 앱과 CLI의 통합 경계를 보여 줍니다. 다음 구간에서 Python으로 Agent 구성과 업무 코드를 직접 정의하는 PydanticAI를 살펴봅니다.

### 화면 읽기

두 제품의 차이는 제어 가능한 설정과 관측 가능한 실행 경계를 비교하면 드러납니다.

### 적용 예와 확인할 경계

공개 문서의 외부 동작과 고정 소스에서 추적 가능한 내부 동작을 같은 수준의 증거로 취급하지 않습니다.

## PYDANTIC — PydanticAI

## PydanticAI

코드로 구성하는 Agent 실행과 검증

### 화면 읽기

완성형 실행환경에서 Python 코드로 실행을 조합하는 쪽으로 넘어갑니다.

### 적용 예와 확인할 경계

같은 LOT 조회에서 앱이 제공할 모델 연결, 데이터 접근, 출력 타입을 차례로 고릅니다.

## PAD01 — Python 코드로 Agent 구성하기

작은 LOT 조회 Agent에서 시작합니다. yield_pct=120은 Field 범위에서 거절됩니다. 90은 타입과 범위를 통과해도 실제 92와 다를 수 있으므로 앱이 원본을 재계산합니다.

### 화면 읽기

작은 Agent에 모델, 조회 함수, 보고서 타입을 붙이는 흐름입니다.

### 적용 예와 확인할 경계

먼저 동작 확인용 Agent를 만들고, 그 뒤에 실제 업무 권한과 계산 검증을 추가합니다.

## PA01 — Pydantic과 PydanticAI, 어디까지 맡을까?

## Pydantic과 PydanticAI, 어디까지 맡을까?

Pydantic · 데이터 검증 — Report에서 bin_id와 defect_rate 타입 확인 문자열·숫자 등 입력을 선언된 계약으로 검증

PydanticAI Core · 실행 — 모델 호출 → 도구 인자 검증 → Python 실행 결과를 다음 메시지로 넣거나 최종 타입으로 반환

Harness · 선택 기능 — Memory, Skills, Subagents를 연결 저장소나 호출 범위는 앱 설정으로 선택

업무 앱 · 실제 기준 — 조회 가능한 BIN인지, 42/1000이 맞는지 데이터를 다시 조회하고 승인·저장을 관리

yield_pct=120은 Field 범위에서 거절됩니다. 90은 타입과 범위를 통과해도 실제 92와 다를 수 있으므로 앱이 원본을 재계산합니다.

### 화면 읽기

데이터 계약의 검증, 모델·도구 실행, 선택 기능, 업무 규칙을 네 칸으로 나눕니다.

### 적용 예와 확인할 경계

42와 1000이 숫자라는 검증과 42/1000이 실제 원본 값이라는 검증은 별도입니다.

## PA02 — PydanticAI Core의 네 부분

## PydanticAI Core의 네 부분

Agent 설정 — 모델 · 지시 · Deps · 도구 · 출력 타입

Graph 실행 — 입력 → 모델 요청 → 응답 처리

실행 경계 — Model Adapter · ToolManager · 출력 검증

상태와 운영 — Conversation · 사용량 · Capability/Hooks

### 화면 읽기

설정에서 실행이 시작되고 Graph가 모델·도구·출력 경계를 반복해 호출합니다.

### 적용 예와 확인할 경계

그림의 화살표는 학습 순서를 정리합니다. Conversation과 Hooks는 여러 실행 경계에 걸쳐 사용됩니다.

## PA03 — 가장 작은 Agent 실행

테스트 모델을 주입하면 네트워크 없이 호출 계약을 검증할 수 있습니다. 실제 모델 연결에서는 앱이 provider 설정과 모델 ID를 준비합니다.

```python
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent(TestModel())
result = agent.run_sync('LOT-A 조회 준비')
print(result.output)
```

### 화면 읽기

TestModel을 연결해 공개 API로 Agent가 실행되는지 확인합니다.

### 적용 예와 확인할 경계

이 예제는 모델 자격 증명이나 네트워크 없이 Core 연결을 확인합니다. 실제 모델의 호출 판단 품질을 측정하는 실험은 별도입니다.

## PA04 — 조회 도구와 보고서 타입을 붙이기

## 조회 도구와 보고서 타입을 붙이기

**① 결과 타입** — 최종 결과의 형태를 정함. 수치가 실제 조회값과 같은지는 별도 검사.

**② Agent 설정** — Repo는 앱에서 넣을 의존성 타입. YieldReport는 모델 출력 계약.

**③ 조회 함수 등록** — 모델에는 lot_id 인자만 공개. 함수는 서버에서 ctx.deps로 조회.

**④ 실행** — 조회와 출력 검증을 마치면 앱이 YieldReport 객체를 받음.

Core는 read_counts 인자와 최종 출력 계약을 요청에 반영합니다. 실제 집계 조회와 허용 범위, 결과 의미 검증은 앱 코드입니다.

```python
class YieldReport(BaseModel):
    lot_id: str
    snapshot: str
    yield_pct: float = Field(ge=0, le=100)

agent = Agent(model, deps_type=Deps,
              output_type=YieldReport)

@agent.tool
def read_counts(ctx: RunContext[Deps], lot_id: str):
    return ctx.deps.read_counts(lot_id)
```

### 화면 읽기

모델은 lot_id를 제안하고 호스트 함수가 저장소를 읽습니다. 최종 결과는 선언한 Python 타입으로 돌아옵니다.

### 적용 예와 확인할 경계

출력 타입은 반환 형식을 정합니다. 조회 범위와 수율 계산식은 별도 검증이 필요합니다.

## PAD02 — 요청이 반복되고 끝나는 과정

노드와 메시지를 따라 한 번의 Run을 읽습니다. _PreparedAgentRun.open이 실행 범위를 엽니다. run은 Graph를 소비하고 iter는 앱에 노드 진행을 노출합니다. 예외 시 리소스 정리 범위를 확인합니다.

### 화면 읽기

한 실행이 어떻게 시작되고 어떤 조건으로 다음 모델 호출을 만드는지 살펴봅니다.

### 적용 예와 확인할 경계

아래에서는 모델 호출 수와 실제 업무 Tool 실행 수를 따로 셉니다.

## PA06 — run()이 Graph를 여는 과정

## run()이 Graph를 여는 과정

**① 앱의 진입점** — run은 노드들을 끝까지 진행해 AgentRunResult를 반환.

**② 실행 준비** — 모델, 상태, 도구와 Capability 등 이 실행에서 사용할 구성을 준비.

**③ 리소스 열기** — 실행 범위 안에서 리소스를 열고 첫 UserPromptNode를 Graph에 전달.

**④ 순회와 정리** — 노드가 다음 작업을 돌려줌. 실행 컨텍스트를 빠져나오며 리소스 정리.

_PreparedAgentRun.open이 실행 범위를 엽니다. run은 Graph를 소비하고 iter는 앱에 노드 진행을 노출합니다. 예외 시 리소스 정리 범위를 확인합니다.

### 화면 읽기

run은 끝까지 소비하고 iter는 노드 단위로 실행을 관찰할 수 있게 합니다.

### 적용 예와 확인할 경계

같은 요청이라도 웹 UI가 단계 상태를 보여주려면 노드나 이벤트를 소비하는 API를 선택합니다.

## PA07 — pydantic-graph가 Agent 루프를 돌리는 방법

## pydantic-graph가 Agent 루프를 돌리는 방법

**① GraphBuilder** — Graph 타입과 시작점을 정의. GraphRun이 노드의 실행 결과를 받아 진행.

**② UserPromptNode** — 이력을 불러오고 새 사용자 요청을 구성. 승인 재개라면 보류 결과도 처리.

**③ ModelRequestNode** — 요청용 메시지·옵션을 준비하고 모델 호출. 응답을 이력에 넣어 CallToolsNode로 전달.

**④ CallToolsNode** — 도구 반환이나 수정 요청은 다음 모델 입력. 최종 결과는 SetFinalResult에서 End로 넘김.

CallToolsNode는 다음 ModelRequestNode로 이어지거나 결과와 함께 종료합니다. 승인 응답으로 재개할 때는 기존 보류 호출을 먼저 처리할 수 있습니다. 사용자 정의 업무 Graph와 내부 노드는 다른 층입니다.

### 화면 읽기

입력 노드, 모델 요청 노드, 응답 처리 노드가 각각 다음 실행을 반환합니다.

### 적용 예와 확인할 경계

업무 자체의 조회→검증→발행 순서를 정의한 Graph와 Core의 내부 모델·도구 루프는 서로 다른 층입니다.

## PA09 — Graph 상태와 앱 데이터가 만나는 곳

## Graph 상태와 앱 데이터가 만나는 곳

**실행 중 누적 상태** — 모델과 주고받은 이력, 사용량, 진행 단계를 현재 실행에서 누적.

**실행 구성** — 어떤 모델과 한도, 종료 정책을 현재 Graph 실행에서 사용할지 보관.

**도구가 읽는 값** — 도구는 앱이 넣은 권한과 데이터 기준을 읽음. 모델에는 도구가 반환한 값이 전달될 수 있음.

build_run_context가 내부 상태의 일부와 앱 deps를 Tool·Hook에 전달합니다. deps 객체는 Python에 남으며 Tool이 반환한 값은 모델 입력이 될 수 있습니다.

### 화면 읽기

변하는 이력·사용량, 실행 설정, 앱이 넣은 데이터 접근 객체를 따로 읽습니다.

### 적용 예와 확인할 경계

허용 LOT 목록이 Python 의존성에 있어도 Tool 반환이나 별도 지시에 담으면 모델이 볼 수 있습니다.

## PA10 — 모델 응답을 어느 경로로 보낼까?

## 모델 응답을 어느 경로로 보낼까?

**업무 도구 요청** — 도구 반환을 메시지에 추가. 다음 ModelRequestNode에서 모델이 읽음.

**최종 출력 후보** — 텍스트·파일은 출력 계약에 맞춰 검사. 출력용 Tool은 Tool 호출 처리 경로에서 검사.

**수정 또는 보류** — 수정 요청은 다음 모델 호출에 전달. 승인 대기는 앱에 넘겨 후속 실행에서 해결.

CallToolsNode._handle_tool_calls와 _process_response_output을 구별합니다. 유효한 출력과 실행할 Tool이 함께 있으면 EndStrategy가 처리에 관여합니다.

### 화면 읽기

텍스트·파일·Tool Call을 응답 형식과 출력 계약에 맞게 처리합니다.

### 적용 예와 확인할 경계

잘못된 인자는 재요청으로, 사용자 확인이 필요한 호출은 보류 결과로 이어질 수 있습니다. 둘은 실행 재개 방식이 다릅니다.

## PA11 — 다음 모델 요청이 막히는 지점

## 다음 모델 요청이 막히는 지점

**모델 요청 횟수** — 기본 요청 한도 50회. 한도에 도달하면 다음 모델 요청 전에 UsageLimitExceeded.

**출력 재시도** — 출력 검증 실패는 해당 재시도 예산을 사용. 모델 요청 횟수 한도와 별개.

**실행 취소** — 취소 시점에 기록 가능한 실행 상태를 정리. 이미 외부에 저장한 결과의 복구는 앱 책임.

consume_output_retry에서 출력 한도를 확인합니다. 동시에 실행한 작업의 취소로 이미 성공한 외부 쓰기가 되돌아가지는 않으므로 앱이 멱등성과 보상 절차를 설계합니다.

### 화면 읽기

요청 한도는 새 모델 요청 전 검사하고 출력 오류는 별도 retry 예산을 씁니다.

### 적용 예와 확인할 경계

동시에 여러 Tool을 실행하는 중 취소하더라도 이미 성공한 외부 작업은 남을 수 있습니다.

## PA12 — 실행 API 다섯 가지

## 실행 API 다섯 가지

**run_sync** — 동기 함수에서 최종 결과를 기다림.

**run** — 비동기 서버에서 최종 결과와 이력을 받음.

**run_stream** — 출력을 점진적으로 표시. 최종 출력 확정 시점에 유의.

**run_stream_events** — 모델 응답과 도구 실행 이벤트를 같은 스트림에서 소비.

**iter** — 현재 Graph 노드를 보며 실행. run.result에서 최종 결과 확인.

run_stream은 최종 출력이 스트림에서 확정되는 시점에 주의합니다. 모든 실행 이벤트를 소비하고 싶다면 run_stream_events를 비교합니다. iter는 프레임워크 내부 노드 진행을 관찰할 때 사용합니다.

### 화면 읽기

동기 결과, 비동기 결과, 출력 스트림, 이벤트 스트림, Graph 노드의 다섯 관측 단위를 나눕니다.

### 적용 예와 확인할 경계

텍스트 UI에는 출력 스트림이 적합하고, 모든 실행 경계를 기록하려면 이벤트나 노드를 소비합니다.

## PAD03 — 모델 입력과 대화 상태

공급자에게 보내는 값과 앱에 저장하는 값을 나눕니다. _prepare_request_parameters에서 Tool·출력 계약이 요청용 데이터로 준비됩니다. 인증 객체를 deps에 넣는다고 공급자에 직렬화되는 것은 아니며 앱이 Tool 반환과 로그에 노출되는 값은 관리해야 합니다.

### 화면 읽기

모델에게 전달하는 문맥과 다음 실행까지 앱에 보관하는 상태를 구분합니다.

### 적용 예와 확인할 경계

같은 문장이라도 현재 instructions, 역사에 남는 메시지, 저장소 내부 값은 다른 경로로 전달됩니다.

## PA13 — LOT-A 요청에서 모델이 실제로 받는 값

## LOT-A 요청에서 모델이 실제로 받는 값

① 메시지 — 예: “LOT-A 수율을 알려줘” 이전 조회 결과가 있다면 이력으로 함께 전송

② 도구·출력 계약 — read_counts의 lot_id는 문자열 YieldReport 필드는 출력 모드에 맞게 전송

③ Python 실행 환경 — ctx.deps에 허용 LOT와 DB 연결 도구가 실행될 때 이 객체로 접근 권한 검사

④ 다음 모델 요청 — 도구가 반환한 good=920, total=1000 ToolReturnPart가 이력에 합쳐져 모델에 전달

_prepare_request_parameters에서 Tool·출력 계약이 요청용 데이터로 준비됩니다. 인증 객체를 deps에 넣는다고 공급자에 직렬화되는 것은 아니며 앱이 Tool 반환과 로그에 노출되는 값은 관리해야 합니다.

### 화면 읽기

현재 메시지와 Tool 계약을 모델에 보내고, 조회 권한과 DB 연결은 호스트에 둡니다.

### 적용 예와 확인할 경계

good=920, total=1000을 도구가 반환하면 그 값은 다음 모델 요청에 들어갈 수 있습니다. 수치는 설명용입니다.

## PA14 — 새 Run에서 어떤 지시가 남을까?

## 새 Run에서 어떤 지시가 남을까?

**첫 실행의 두 지시** — Instructions는 현재 실행의 지시로 계산. System prompt는 메시지 Part로 기록 가능.

**다른 Agent로 계속 실행** — 새 instructions는 “표로 작성”. 기존 SystemPromptPart는 넘긴 이력에 남음.

**동적 System Prompt** — 현재 Agent가 해당 동적 프롬프트를 인식하는 경로에서 다시 평가.

동적 system prompt는 _reevaluate_dynamic_prompts 경로에서 재평가될 수 있습니다. OpenAI Chat의 메시지와 Responses의 입력 항목은 서로 다른 요청 형식입니다. Anthropic 역시 별도 adapter의 system 블록 조립을 따릅니다.

### 화면 읽기

새 Agent의 instructions와 이전 이력의 SystemPromptPart가 어디서 오는지 비교합니다.

### 적용 예와 확인할 경계

지침을 교체했는데 과거 SystemPromptPart가 여전히 영향을 주는지 확인하려면 다음 요청의 실제 메시지를 봅니다.

## PA15 — deps로 조회 범위를 전달하기

서버가 허용한 LOT 목록과 읽기 snapshot을 RunContext에 넣습니다. 모델은 lot_id를 제안하며 Tool이 접근 권한을 확인합니다. 같은 schema를 보내도 tenant에 따라 실행 가능한 데이터는 달라집니다.

```python
@dataclass
class Deps:
    allowed_lots: set[str]
    snapshot: str
    counts: dict[str, tuple[int, int]]

    def read_counts(self, lot_id: str):
        if lot_id not in self.allowed_lots:
            raise PermissionError(lot_id)
        good, total = self.counts[lot_id]
        return dict(good=good, total=total,
                    snapshot=self.snapshot)
```

### 화면 읽기

Deps는 앱에서 결정한 조회 범위를 Tool 실행 시점에 제공하는 방법입니다.

### 적용 예와 확인할 경계

모델이 접근 불가 LOT를 제안하더라도 서버의 허용 목록을 통과해야 실제 조회가 일어납니다.

## PA16 — History와 Conversation의 차이

all_messages()는 메시지를 넘기는 경로입니다. result.conversation에는 누적 상태와 deferred_tool_requests도 포함됩니다. 새 요청에 어떤 상태를 전달할지 호출자가 정합니다.

### 화면 읽기

메시지 재사용과 Conversation 전체 복원은 넘기는 상태 범위가 다릅니다.

### 적용 예와 확인할 경계

승인 대기 뒤 이어서 실행할 때는 대화 텍스트 외에 보류된 호출과 연결 정보가 필요합니다.

## PA17 — 대화 불러오기 → 실행 → 새 버전 저장

## 대화 불러오기 → 실행 → 새 버전 저장

**① 불러오기** — 사용자와 세션을 확인한 뒤 저장된 JSON을 메시지·실행 상태가 있는 Conversation으로 복원.

**② 이어서 실행** — 이전 요청·응답을 참고해 새 메시지 추가. 빈 세션은 conversation=None으로 시작.

**③ 갱신** — 갱신한 상태를 다시 저장. 버전 확인과 충돌 처리는 앱 예시.

Conversation을 DB에 저장하는 위치와 TTL은 앱이 선택합니다. 동시에 두 Run이 진행되면 버전을 비교해 나중 저장이 먼저 저장한 메시지를 덮어쓰는 문제를 막습니다.

### 화면 읽기

저장된 JSON 복원 → 새 Run → 갱신된 Conversation 직렬화 순서입니다.

### 적용 예와 확인할 경계

같은 세션에 동시 쓰기가 가능하면 버전 비교는 앱 저장소 계약으로 구현합니다. 슬라이드의 store 메서드는 앱 예시입니다.

## PAD04 — Tool 등록과 실제 실행

함수 선언부터 인자 검증과 병렬 실행까지 추적합니다. FunctionToolset이 호출할 함수를 관리합니다. 이름, 설명과 schema가 모델에 전달되고 인자 검증에는 Pydantic validator가 쓰입니다. 함수 본체는 Python에서 실행됩니다.

### 화면 읽기

함수 등록에서 모델 명세, 검증과 실행을 거쳐 도구 결과가 돌아오는 경로입니다.

### 적용 예와 확인할 경계

입력 형식 오류가 났을 때 실제 함수 본문에 들어갔는지부터 확인합니다.

## PA18 — 함수 한 개에서 스키마와 검증기가 만들어지는 과정

## 함수 한 개에서 스키마와 검증기가 만들어지는 과정

**함수 선언** — 함수 이름과 설명을 읽음. lot_id는 모델이 넘길 입력.

**Core 내부 준비** — 함수 서명과 타입을 바탕으로 JSON Schema와 입력 검증기를 준비.

**모델에 공개하는 값** — 모델은 이름·설명·인자 계약을 받음. 함수 본문과 Repo는 Python에 남음.

FunctionToolset이 호출할 함수를 관리합니다. 이름, 설명과 schema가 모델에 전달되고 인자 검증에는 Pydantic validator가 쓰입니다. 함수 본체는 Python에서 실행됩니다.

### 화면 읽기

함수 서명에서 검증기와 모델용 스키마를 준비하고, 호스트에서 함수를 실행합니다.

### 적용 예와 확인할 경계

RunContext는 실행 측 인자이므로 모델에게 공개할 lot_id와 구분합니다.

## PA19 — tool과 tool_plain 선택하기

tool은 RunContext가 필요한 조회·인가에 사용합니다. tool_plain은 앱 의존성이 필요 없는 순수 계산에 적합합니다. sync/async 선택은 함수가 I/O를 기다리는지에 따라 별도로 결정합니다.

```python
@agent.tool
def read_counts(ctx: RunContext[Deps], lot_id: str):
    return ctx.deps.read_counts(lot_id)

@agent.tool_plain
def yield_percent(good: int, total: int) -> float:
    return 100 * good / total
```

### 화면 읽기

의존성이 필요한 도구와 계산만 하는 도구의 선언을 비교합니다.

### 적용 예와 확인할 경계

저장소 조회에는 RunContext가 필요하지만 두 숫자의 비율 계산에는 외부 접근 객체가 필요하지 않습니다.

## PA20 — 다음 모델 요청에서 도구 목록을 바꾸기

## 다음 모델 요청에서 도구 목록을 바꾸기

**요청 단계마다 목록 준비** — 현재 RunContext에 맞게 모델에 공개할 도구 정의를 준비.

**prepare 콜백으로 숨기기** — 권한이 없으면 None을 반환해 그 요청의 공개 목록에서 제외.

**실행할 때 다시 확인** — 공개 목록에 있었다고 해서 실제 작업이 지금도 허용된다는 뜻은 아님.

ToolManager.for_run_step이 실행 단계에 맞는 도구를 준비합니다. Combined, Filtered, Prefixed는 묶기·걸러내기·이름 구분에 쓰입니다. 데이터에 접근할 권한은 실행 경계에서도 검사합니다.

### 화면 읽기

Toolset은 실행 단계마다 현재 문맥에 맞는 공개 목록을 준비할 수 있습니다.

### 적용 예와 확인할 경계

발행 도구를 숨겨도 서버 인가는 따로 검사합니다. 목록 공개 뒤 권한이 바뀔 수 있기 때문입니다.

## PA21 — Tool 인자가 틀리면 어디에서 멈출까?

## Tool 인자가 틀리면 어디에서 멈출까?

**① 도구 찾기** — 도구 이름을 현재 실행에서 공개한 목록과 대조. 도구가 없으면 함수에 진입하지 않음.

**② 인자 검증** — {}는 필수 lot_id 누락. 검증 오류는 RetryPromptPart로 돌려보냄.

**③ 정책 Hook과 실행** — {"lot_id": "LOT-A"}가 검증을 통과한 뒤 서버에서 업무 권한을 확인하고 조회.

_resolve_tool과 _build_tool_context를 거쳐 _run_validate_hooks가 수행됩니다. 검증된 인자로 ValidatedToolCall을 만들고 실행 경로에 넘깁니다. 미등록 이름과 유효하지 않은 인자는 각 오류 경로로 처리됩니다.

### 화면 읽기

도구 이름 확인, JSON·Python 인자 검증, Hook과 함수 실행을 순서대로 읽습니다.

### 적용 예와 확인할 경계

lot_id를 빠뜨린 호출과 올바른 문자열이지만 권한이 없는 호출은 각각 형식 오류와 업무 인가 실패입니다.

## PA22 — 타입 검사 이후의 업무 조건

합성 LOT-A의 동일 snapshot에서 good과 total을 읽습니다. 모델이 다른 LOT를 제안하면 조회를 차단하고 조회 권한 오류와 인자 수정 요청을 별도로 기록합니다.

### 화면 읽기

타입, 인가, 결과 검증을 각기 다른 경계에서 검사합니다.

### 적용 예와 확인할 경계

A17에 접근할 수 있어도 조회 snapshot과 보고서가 다른 기간을 가리키면 결과를 그대로 발행할 수 없습니다.

## PA23 — 병렬 조회 사이에 단독 작업을 넣기

## 병렬 조회 사이에 단독 작업을 넣기

**① 도구에 단독 실행 표시** — C 앞의 조회가 끝나야 C를 시작. C가 끝나기 전에는 D/E를 시작하지 않음.

**② 실행 묶음 계산** — 실행기는 모델이 낸 호출 순서에서 단독 도구를 기준으로 묶음을 분할.

**③ 독립 호출을 동시에 시작** — 독립 I/O는 대기 시간을 겹칠 수 있음. 공유 상태 쓰기나 호출량 폭주는 앱에서 제어.

_segment_by_barriers가 구간을 나누고 _call_tools가 task를 실행합니다. 동기 함수는 offload될 수 있습니다. 완료 이벤트 순서와 history 조립 인덱스는 구분합니다. B 입력에 A 결과가 필요하면 앱이나 후속 모델 요청이 의존성을 해결해야 합니다.

### 화면 읽기

실행기는 같은 응답의 호출들을 단독 실행 도구를 기준으로 구간을 나눕니다.

### 적용 예와 확인할 경계

A/B가 끝나 C가 실행되고 이후 D/E가 시작됩니다. C에 A 결과를 전달하는 데이터 의존성은 앱 또는 다음 모델 호출에서 연결합니다.

## PA24 — Local, MCP, Native Tool의 실행 위치

MCP는 서버가 공개한 schema를 받아 원격 호출로 전달합니다. Native Tool의 실행과 결과 표현은 공급자 지원을 확인합니다. 앱은 MCP 인증과 접근 범위, 실제 모델 호환성을 관리합니다.

### 화면 읽기

Python 함수, MCP 서버, 모델 공급자에서 실행하는 Tool의 위치를 비교합니다.

### 적용 예와 확인할 경계

같은 네트워크 조회라도 요청 인증·오류·결과 관측이 어느 경계에서 일어나는지 확인합니다.

## PAD05 — 출력 검증과 종료 정책

결과 계약과 실행할 작업을 함께 판단합니다. ToolOutput은 처음부터 출력용 Tool을 제시합니다. NativeOutput의 지원 범위는 adapter에 달려 있습니다. PromptedOutput의 파싱·검증 실패는 retry 경로를 타며 TextOutput 콜백도 반환 형식을 앱이 결정합니다.

### 화면 읽기

최종 결과의 모양과 같은 응답에 포함된 나머지 호출의 실행 여부를 나눠 봅니다.

### 적용 예와 확인할 경계

보고서가 유효하다는 판정 이후에도 기록 Tool이 실행될 수 있는 정책이 있습니다.

## PA25 — 출력 모드 네 가지

ToolOutput은 처음부터 출력용 Tool을 제시합니다. NativeOutput의 지원 범위는 adapter에 달려 있습니다. PromptedOutput의 파싱·검증 실패는 retry 경로를 타며 TextOutput 콜백도 반환 형식을 앱이 결정합니다.

### 화면 읽기

출력용 Tool, 공급자 구조화 계약, 프롬프트 유도 JSON, 텍스트 처리 경로를 비교합니다.

### 적용 예와 확인할 경계

같은 보고서라도 실제 요청의 tools나 출력 옵션이 달라집니다. 공급자의 NativeOutput 지원은 모델별로 확인합니다.

## PA26 — 범용 Agent에서 최종 결과 타입 고르기

Agent는 실행에 필요한 중간 Tool을 호출하면서 최종 출력 계약을 맞춥니다. 복수 출력은 앱이 각 타입을 처리할 수 있을 때 유용합니다. run별 override는 기존 validator와의 제약을 확인합니다.

### 화면 읽기

중간 도구 반환 형식과 최종 앱 결과 형식을 별도 계약으로 선택합니다.

### 적용 예와 확인할 경계

조회 결과에 good과 total이 있어도 최종 보고서는 lot_id, 수율, 근거를 별도로 선언할 수 있습니다.

## PA27 — 수율과 근거를 원본에서 다시 검증하기

output_validator에서 snapshot과 수치를 대조합니다. ModelRetry는 모델에게 수정 피드백을 줍니다. 권한 오류나 신뢰할 수 없는 원본은 앱이 실패로 다룹니다.

```python
@agent.output_validator
def verify(ctx: RunContext[Deps], out: YieldReport):
    counts = ctx.deps.read_counts(out.lot_id)
    expected = 100 * counts['good'] / counts['total']
    if out.snapshot != counts['snapshot']:
        raise ModelRetry('snapshot을 확인하세요.')
    if abs(out.yield_pct - expected) > 0.01:
        raise ModelRetry('수율을 다시 계산하세요.')
    return out
```

### 화면 읽기

모델이 반환한 수치가 schema를 통과한 뒤 원본 데이터와 다시 대조합니다.

### 적용 예와 확인할 경계

원본이 920/1000이면 90%는 형식이 맞아도 값은 틀립니다. 단위와 비교 허용 오차는 앱이 정합니다.

## PA28 — 같은 모델 응답에서 무엇을 실행할까?

## 같은 모델 응답에서 무엇을 실행할까?

**early** — 출력 도구를 먼저 검사. 유효한 출력이 있으면 업무 함수는 생략.

**graceful · 기본** — 모델이 낸 순서에 따라 함수 묶음을 처리. O1을 얻어도 뒤의 업무 함수는 실행 가능.

**exhaustive** — 단독 실행 경계를 제외하면 함께 시작. 유효한 출력 선택은 응답에 나온 순서 기준.

process_tool_calls가 각 Processor를 선택합니다. 고정 응답 시험에서 early는 A와 B를 실행하지 않았고 graceful과 exhaustive는 둘 다 실행했습니다. graceful은 방출 순서에 따라 함수 묶음을 처리하며 O1을 채택해도 뒤에 있는 B가 실행될 수 있습니다. 기록 B는 시험용 부작용이며 실제 발행은 별도 권한 경계로 둡니다.

### 화면 읽기

고정 응답의 A, O1, B, O2 순서로 정책별 실제 실행 범위를 비교합니다.

### 적용 예와 확인할 경계

early는 유효 출력이 있으면 업무 Tool을 건너뛸 수 있고, graceful과 exhaustive에서도 발행 권한은 별도로 걸어야 합니다.

## PA29 — 최종 출력 후보가 있어도 재요청하는 경우

graceful은 실패한 출력 뒤의 함수 구간을 이어갈 수 있습니다. graceful/exhaustive의 retry-wins를 적용할 때 run_stream에서 이미 확정한 출력은 별도 경로로 처리합니다. Deferred의 보류 상태도 정상 완료와 구분합니다.

### 화면 읽기

출력 검증 실패와 업무 도구의 retry 요청이 최종 결과 선택에 미치는 영향을 봅니다.

### 적용 예와 확인할 경계

출력 후보가 하나 유효해도 실행 정책과 스트림 확정 시점에 따라 추가 모델 요청이 필요할 수 있습니다.

## PA30 — Retry 횟수는 어느 층에서 셀까?

retries=2의 적용 범위는 Agent와 Tool·출력 설정을 확인합니다. HTTP 계층과 앱 재시도가 겹치면 실제 요청은 늘 수 있습니다. 이미 쓴 외부 효과의 재실행을 통제합니다.

### 화면 읽기

Core가 모델에게 수정을 요청하는 횟수와 SDK의 네트워크 재전송 횟수는 별개입니다.

### 적용 예와 확인할 경계

외부 쓰기를 다시 시도할 때는 같은 업무 키를 사용해 중복 반영 여부를 추적합니다.

## PAD06 — Capability와 승인

공통 정책을 조합하고 보류된 실행을 이어갑니다. Capability는 실행 경계와 구성 요소를 조합합니다. LOT 인가처럼 특정 Tool에만 필요한 정책은 해당 함수에서 검사하고 여러 도구가 공통으로 쓰는 정책은 재사용 가능한 단위로 둘 수 있습니다.

### 화면 읽기

공통 검사와 관측을 Capability에 넣고, 사람의 판단이 필요하면 보류 결과로 넘깁니다.

### 적용 예와 확인할 경계

승인 요청 발생, 사람의 응답, Tool 실행은 서로 다른 이벤트입니다.

## PA31 — Capability가 묶는 구성요소

Capability는 실행 경계와 구성 요소를 조합합니다. LOT 인가처럼 특정 Tool에만 필요한 정책은 해당 함수에서 검사하고 여러 도구가 공통으로 쓰는 정책은 재사용 가능한 단위로 둘 수 있습니다.

### 화면 읽기

Capability는 여러 Agent에서 재사용할 Toolset·지시·Hook을 모을 수 있습니다.

### 적용 예와 확인할 경계

여러 도구에 같은 기록 정책을 붙이는 사례와 특정 조회 함수 안의 업무 권한 검사를 분리합니다.

## PA32 — Capability의 앞·뒤·감싸기 순서

CombinedCapability가 중첩 구조를 정규화하고 get_ordering과 for_run을 적용합니다. before_model_request와 after_model_request의 순서가 다르며 wrap_model_request는 handler chain을 구성합니다.

### 화면 읽기

Hook의 진입 순서와 응답이 돌아오는 순서를 비교합니다.

### 적용 예와 확인할 경계

두 Hook이 같은 메시지를 바꾼다면 어느 Hook의 변경 결과를 다음 Hook이 받는지 확인합니다.

## PA33 — 업무 정책을 Hook에 넣는 위치

ToolManager._run_validate_hooks와 _run_execute_hooks는 서로 다른 단계입니다. DB 접근 권한은 데이터 경계에서 보장하고 Capability는 공통 정책과 관측을 조합하는 데 씁니다.

```python
from pydantic_ai.capabilities import AbstractCapability

class LotPolicy(AbstractCapability[Deps]):
    async def before_tool_execute(
        self, ctx, *, call, tool_def, args
    ):
        if call.tool_name == 'read_counts':
            if args['lot_id'] not in ctx.deps.allowed_lots:
                raise PermissionError(args['lot_id'])
        return args
```

### 화면 읽기

입력 검사, 실행 측 정책, 실행 후 관측을 각각 필요한 경계에 둡니다.

### 적용 예와 확인할 경계

발행 차단은 쓰기 전에 해야 하고, 결과 마스킹은 반환 내용을 확인하는 경계에 둘 수 있습니다.

## PA34 — 가드레일을 어느 경계에 걸까?

## 가드레일을 어느 경계에 걸까?

**입력 검사** — 예: 생산 데이터 반출 요청 차단. 병렬 모드는 모델 요청이 이미 시작될 수 있음.

**도구 검사** — 예: publish 호출을 승인 대기로 전환. allow / block / retry / approve / replace.

**출력 검사** — 예: 최종 불량률이 원본과 맞는지 확인. partial 출력은 이 검사에서 건너뜀.

InputGuardrail의 병렬 모드는 모델 호출과 guard를 함께 시작할 수 있습니다. ToolGuardrail의 allow/block/retry/approve/replace는 실행 위치와 승인 상태를 확인합니다. OutputGuardrail은 partial output을 건너뜁니다.

### 화면 읽기

입력·Tool·출력 검사는 모델 요청, 외부 실행, 사용자 결과의 서로 다른 경계에 놓입니다.

### 적용 예와 확인할 경계

입력 가드가 병렬이면 모델 호출이 이미 시작됐을 수 있습니다. 데이터 전송 자체를 막아야 하면 선행 검사 경로를 봅니다.

## PA35 — 승인 필요 여부를 결정하는 곳

인자가 검증된 이후에 승인할 작업을 확정합니다. 조건부 정책과 승인 상태에 따라 실행을 보류하고 결과 타입에 보류 결과를 받을 구성을 둡니다.

### 화면 읽기

승인 필요 조건을 Tool과 인자에 연결하고, 사람의 판단이 오기 전 호출을 보류합니다.

### 적용 예와 확인할 경계

검증된 발행 대상과 원본 인자를 저장해야 앱이 승인 화면에서 정확한 작업을 보여줄 수 있습니다.

## PA36 — 승인 요청을 처리하는 세 경로

서버는 승인 UI를 직접 선택합니다. 보류 결과를 반환하는 구성에서는 실행이 끝나고 앱에 요청이 전달됩니다. 사람의 응답이 없으면 앱의 대기·만료 정책을 적용합니다.

### 화면 읽기

승인을 앱 코드에서 처리하거나, 대화형 CLI에 묻거나, 후속 Run을 통해 재개할 수 있습니다.

### 적용 예와 확인할 경계

사람이 접속하지 않은 서버에서는 보류 ID, 만료 정책, 상태 저장을 앱에서 관리합니다.

## PA37 — 승인한 호출 ID로 실행 이어가기

## 승인한 호출 ID로 실행 이어가기

**보류된 호출 저장** — 호출 ID와 원래 인자를 보관. 실행한 결과 대신 승인 요청이 앱에 도착.

**사람이 결정** — 원래 호출 ID에 승인 또는 거절을 연결. 승인 권한과 유효기간은 앱에서 검사.

**새 Run으로 재개** — Core는 보류했던 호출과 결정을 연결. 승인 결과를 처리한 뒤 실행을 이어감.

DeferredToolResults를 기존 보류 호출에 연결합니다. override_args를 쓰는 경우 새 인자를 다시 확인합니다. 앱은 초안 수정, 중복 승인, 위조 및 접근 권한 변경을 재개 전에 검사합니다.

### 화면 읽기

보류 호출 ID에 결정을 붙여 원래 Conversation과 함께 후속 Run에 전달합니다.

### 적용 예와 확인할 경계

승인 뒤 보고서 버전이 바뀌었다면 이전 결정을 재사용하지 않도록 앱에서 확인합니다.

## PAD07 — 선택 Harness 기능

필요한 기억, 작업 환경, 복구 기능을 연결합니다. Core만으로 작은 Agent를 실행할 수 있습니다. Harness 기능을 조합하면 저장·작업 환경·위임에 필요한 구성 요소를 재사용합니다. Coder와 Researcher는 용도별 구성을 보여 줍니다.

### 화면 읽기

Core에 필요한 기억, Skill, 실행 환경, 지속 기능을 선택해서 붙입니다.

### 적용 예와 확인할 경계

사용자가 원하는 운영 정책은 저장소와 권한 설정까지 결정해야 완성됩니다.

## PA38 — Core 위에 선택 Harness 붙이기

Core만으로 작은 Agent를 실행할 수 있습니다. Harness 기능을 조합하면 저장·작업 환경·위임에 필요한 구성 요소를 재사용합니다. Coder와 Researcher는 용도별 구성을 보여 줍니다.

### 화면 읽기

Core 실행 위에 Harness Capability가 기능을 추가하는 방향으로 읽습니다.

### 적용 예와 확인할 경계

작은 조회 Agent에는 Core만 사용할 수 있습니다. 파일 탐색이나 기억이 필요한 경우에 관련 기능을 붙입니다.

## PA39 — Harness Memory에 메모 한 줄 쓰기

## Harness Memory에 메모 한 줄 쓰기

**앱에서 연결** — 실행에서 사용할 저장소와 scope를 결정. 기본 InMemoryStore는 프로세스 수명.

**모델의 쓰기 요청** — Toolset이 인자를 검사하고 scope 내에서 메모 저장 또는 수정 처리.

**다시 조회** — 정확한 파일을 읽거나 검색어로 노트를 찾음. 원본 대화 전체와는 별도의 저장 대상.

write_memory 등의 호출이 Store에 연결됩니다. namespace는 앱이 정하며 모델 인자가 아닙니다. 업무 데이터를 언제 기록할지와 사용자별 저장 범위는 앱 정책입니다.

### 화면 읽기

Toolset이 쓰기·읽기 요청을 받고 MemoryStore는 정해진 namespace에 내용을 보관합니다.

### 적용 예와 확인할 경계

기본 인메모리 저장과 영속 저장을 구분합니다. 저장소 범위는 모델이 입력한 파일 이름과 별개입니다.

## PA40 — 저장한 Memory가 다음 모델 입력에 들어가는 곳

## 저장한 Memory가 다음 모델 입력에 들어가는 곳

**실행 범위 정하기** — 현재 실행에서 쓸 저장소와 scope를 결정해 다른 실행의 메모와 구분.

**요청 전에 읽기** — 메모를 읽고 줄 수와 토큰 예산 안에서 현재 요청에 붙일 문맥을 준비.

**메시지로 넣기** — 중복 주입을 정리하고 사용자 입력 근처에 기억 문맥을 추가하는 경로.

Memory는 기본 InMemoryStore를 사용하므로 수명은 프로세스입니다. 기본 snapshot 예산은 최대 2000토큰과 200줄이며 설정을 확인합니다. 앱은 영속 저장소와 기억의 공개 범위를 선택합니다.

### 화면 읽기

Run별 저장 범위를 결정하고 모델 요청 직전에 읽을 기억을 구성합니다.

### 적용 예와 확인할 경계

토큰·줄 수 한도 안에 들어간 기억만 확인합니다. 저장된 전체 노트와 모델이 실제 받은 입력은 다를 수 있습니다.

## PA41 — 과거 대화 검색과 노트 검색

ConversationSearchToolset은 대화 소스에서 범위를 정하고 결과를 발췌합니다. 모델이 낸 검색어와 내부 normalization, 앱이 제한한 세션 범위를 각각 관찰합니다.

### 화면 읽기

대화 검색은 과거 메시지를 찾고 노트 검색은 따로 저장한 내용을 찾습니다.

### 적용 예와 확인할 경계

같은 ALARM-17 질의라도 검색 대상, 결과의 근거, 세션 접근 정책이 달라집니다.

## PA42 — 대화 압축 전후를 메시지로 보기

## 대화 압축 전후를 메시지로 보기

**압축 전** — 전체를 보내면 오래된 요청과 결과도 모델 입력에 들어가 토큰을 사용.

**임계조건에서 처리** — 크기와 보존 조건을 검사한 뒤 남길 최근 턴을 선택.

**압축 후 예** — 현재 질문을 뒷받침하는 최근 도구 호출과 반환을 함께 유지하는 예.

SlidingWindowCompaction은 임계조건을 확인하고 ctx.messages를 갱신합니다. 요약은 모델 비용과 손실 가능성이 있으며 Tool 결과 정리는 별도 전략입니다. LOT 식별자와 정확한 수치가 필요하면 원본을 다시 조회합니다.

### 화면 읽기

오래된 턴을 줄이고 현재 질문과 최근 도구 호출·반환을 보존하는 예입니다.

### 적용 예와 확인할 경계

압축은 모델 입력 범위의 변경입니다. 원본 대화 저장 또는 삭제 정책은 별도로 확인합니다.

## PA43 — Harness Skill이 실행에 들어오는 과정

## Harness Skill이 실행에 들어오는 과정

**목록 준비** — 실행에 연결된 Skill을 발견하고 메타데이터로 사용할 절차를 안내.

**필요한 것 선택** — 모델이 절차를 선택하면 해당 Capability의 본문이나 연결 기능을 활성화.

**참고파일 접근** — 세부 절차가 필요할 때 파일 접근. 경로와 실행 권한은 연결한 환경에 따름.

Skills.for_run과 loader가 카탈로그를 만듭니다. 본문을 사용하려면 적절한 Capability를 로딩합니다. 중복과 파싱 오류, 참고 파일 접근 및 자체 작성 절차는 앱의 검수 경계와 연결합니다.

### 화면 읽기

Skill 이름과 설명이 노출된 뒤 필요한 본문과 참고 파일을 읽는 흐름입니다.

### 적용 예와 확인할 경계

도구 접근은 연결한 작업 환경 정책을 따릅니다. Skill 선택 자체가 파일 권한을 바꾸는 것은 아닙니다.

## PA44 — 파일·Shell·계획 기능 조합하기

개별 기능의 제공 범위와 실행 권한은 별도로 확인합니다. 업무 Agent는 읽기 전용 LOT 조회만으로 시작할 수 있습니다. 실제 Shell 환경을 붙일 때 작업 디렉터리와 권한, 격리 구현을 앱이 선택합니다.

### 화면 읽기

파일 범위, 명령 실행 격리, 계획을 표현하는 기능을 각각 선택합니다.

### 적용 예와 확인할 경계

읽기 전용 조회만 필요한 앱에 Shell을 연결할 필요는 없습니다. 도구를 연결한 경우 실행 경로와 접근 권한을 함께 봅니다.

## PA45 — 서버가 멈췄을 때 무엇부터 복구할까?

## 서버가 멈췄을 때 무엇부터 복구할까?

Conversation — 사용자 요청·도구 호출·결과와 보류 상태 앱이 이 상태를 다음 Run에 전달

StepPersistence — 완료한 단계와 효과를 checkpoint에 기록 복구 시 어디까지 했는지 결정하는 데 사용

Durable 실행 — 실행기가 정한 경계에서 replay 또는 재개 공급자 호출과 도구 효과를 구분해 설정

앱의 중복 방지 — 보고서 ID·버전으로 멱등 키 지정 발행 성공 후 응답을 잃어도 중복 발행 차단

직렬화된 대화와 실행 중 checkpoint의 복구 범위는 다릅니다. 외부 효과에 대한 정확히 한 번 실행을 보장하려면 저장 시점, replay 계약과 멱등성 정책을 따로 설계합니다.

### 화면 읽기

복구하려는 것이 대화인지, 완료한 단계인지, 중단된 업무 실행인지 먼저 정합니다.

### 적용 예와 확인할 경계

보고서가 저장된 직후 프로세스가 죽었다면 재개할 때 보고서 ID로 이미 수행된 효과를 확인합니다.

## PAD08 — 위임, 관측, 개발 범위

자식 실행과 운영 경계를 같은 사례에 연결합니다. Agent-as-tool은 부모 모델의 Tool 실행 안에서 자식을 호출합니다. 앱 Handoff에서는 앱이 주체를 전환합니다. 사용자 Graph는 공정 검토 단계를 명시하며 Core 내부 모델·Tool 루프와 다른 역할입니다.

### 화면 읽기

자식에게 전달하는 작업, 실행 추적, 업무 앱에 남는 책임을 한 사례로 연결합니다.

### 적용 예와 확인할 경계

자식 실행이 성공했다는 결과와 부모가 사용한 근거가 무엇인지를 따로 확인합니다.

## PA46 — 위임과 Handoff에서 다음 작업을 정하는 곳

Agent-as-tool은 부모 모델의 Tool 실행 안에서 자식을 호출합니다. 앱 Handoff에서는 앱이 주체를 전환합니다. 사용자 Graph는 공정 검토 단계를 명시하며 Core 내부 모델·Tool 루프와 다른 역할입니다.

### 화면 읽기

Agent-as-tool은 부모에게 결과를 돌려주고, Handoff는 다음 실행 주체를 바꿉니다.

### 적용 예와 확인할 경계

검토 의견을 받아 부모가 답하는 경우와 검토자가 최종 답을 맡는 경우를 비교합니다.

## PA47 — 위임 요청을 자식 Run으로 실행하기

## 위임 요청을 자식 Run으로 실행하기

**부모에서 업무 구성** — 자식에게 필요한 데이터와 목표를 명시. 부모의 전체 이력을 공유한다고 가정하지 않음.

**자식 실행** — 선택된 자식의 Agent 실행. Deps 전달과 사용량 추적은 설정을 확인.

**부모에 결과 반환** — 부모가 도구 결과를 읽고 답변을 종합. 위임과 별도 앱 Handoff의 차이.

SubAgentToolset._run_delegation의 실행 범위를 봅니다. 부모 history와 권한을 모두 공유한다고 가정하지 않습니다. deps 전달, 도구 상속, usage 공유와 깊이 제한은 각각 설정과 동작을 확인합니다.

### 화면 읽기

부모가 작업 설명을 구성하고 자식이 자기 Run을 실행한 뒤 결과가 Tool 반환으로 들어옵니다.

### 적용 예와 확인할 경계

자식에게 필요한 측정값과 근거를 명시합니다. 부모의 이력과 앱 권한이 자동 공유된다고 가정하지 않습니다.

## PA48 — Dynamic Workflow와 Advisor 선택하기

두 기능은 Harness의 별도 Capability입니다. 작업 단계를 구조화해야 할 때와 모델 판단을 보강할 의견이 필요할 때를 나눕니다. 자식의 입력과 결과를 누가 통합하는지 비교합니다.

### 화면 읽기

Workflow는 단계와 의존성을 실행하고 Advisor는 별도 관점의 의견을 돌려줍니다.

### 적용 예와 확인할 경계

측정값 검증을 반드시 거쳐야 하는 경우와 가설에 대한 반대 의견만 필요한 경우는 실행 구성이 다릅니다.

## PA49 — Trace로 모델과 Tool 실행 이어 보기

Instrumentation의 wrap_run, wrap_model_request, wrap_tool_execute, wrap_output_process를 관측 경계에 연결합니다. OpenTelemetry exporter와 모델 입력·Tool 결과의 공개 범위는 앱이 설정합니다. 승인 감사 기록은 별도 계약입니다.

### 화면 읽기

Run·모델·Tool·출력 처리의 관측 경계를 연결합니다.

### 적용 예와 확인할 경계

사용량과 지연을 볼 때 정책 판정과 승인 감사 기록은 별도 필드로 남길 수 있습니다. 민감한 원문을 포함할지 설정을 확인합니다.

## PA50 — 흐름 테스트와 답변 평가

테스트에서 잘못된 호출과 수정 응답을 주입해 실제 Tool 실행 횟수를 확인합니다. Evals에서는 원본 집계와 최종 수율 오차, 근거 연결 여부를 평가합니다.

### 화면 읽기

고정 모델 응답으로 실행 규칙을 재현하고 평가 데이터로 실제 답변의 품질을 확인합니다.

### 적용 예와 확인할 경계

인자 누락 시 Tool 실행 0회는 실행 테스트이고, 최종 수율과 근거 정확도는 결과 평가입니다.

## PA51 — 어디까지 개발해야 Agent가 될까?

Agent와 Tool을 정의하면 반복 실행은 Core에 맡길 수 있습니다. 실제 업무에는 deps.py, validators.py, conversation_store.py, approval.py의 책임이 남습니다. Memory나 Skills가 필요하면 Harness 구성 파일에서 선택합니다.

### 화면 읽기

Core가 실행을 제공해도 업무 규칙, 권한, 저장 충돌, 중복 방지의 정의는 앱에 남습니다.

### 적용 예와 확인할 경계

작은 Agent의 완성 기준과 보고서를 운영 발행하는 서비스의 완성 기준을 나눠 봅니다.

## PA52 — 코드와 내부 실행을 한 요청으로 따라가기

고정 응답은 분기와 호출 횟수 재현에 쓰고 실모델 연결은 호환성과 결과 품질을 확인하는 별도 단계입니다. PydanticAI 데모 화면은 18001번이며 런타임은 10001번의 OpenAI 호환 모델 endpoint를 사용합니다. 고정 응답 시험에서 인자 오류와 수율 수정, 세 종료 정책, 대화 직렬화, 승인 재개를 재현했습니다.

실행 화면은 Graph, Deps, 대화 저장·복원, 출력 모드, 종료 정책, Core, Harness Memory, Subagents를 각각 다룹니다.

### 화면 읽기

데모에서 한 요청의 노드 전이, 실제 도구 반환, 출력 검증을 연결해 확인합니다.

### 적용 예와 확인할 경계

Hermes 연결 포트는 10000, PydanticAI는 10001입니다. 발표 HTML은 데모 실행 화면으로 연결하며 모델은 별도 환경에서 실행합니다.

## SDKMAP — SDK 실행 경계 비교

PydanticAI의 Agent 선언·Tool 실행·출력 정책을 기준으로 Claude Agent SDK, Google ADK, Microsoft Agent Framework, OpenAI Agents SDK를 차례로 비교합니다. 네 편의 실패 장면은 합성 입력을 사용한 설명이며 라이브 실행 결과는 아닙니다.

### 화면 읽기

PydanticAI에서 본 모델 호출·Tool·상태·정책을 네 SDK에서 같은 질문으로 비교합니다.

### 적용 예와 확인할 경계

Claude는 CLI 경계, ADK는 Runner와 이벤트, Microsoft는 Workflow, OpenAI는 Runner의 전이와 중단에 초점을 둡니다.

## CAS01 — Claude Agent SDK의 프로세스 경계

SDK 공개 범위에서 SubprocessCLITransport._build_command와 Query._handle_control_request를 읽는다. 실행 환경의 파일·셸을 활용하기 쉽지만 운영 격리와 CLI 버전의 영향을 받는다.

### 화면 읽기

Python 앱과 Claude CLI 사이에서 메시지와 제어 요청이 오가는 구조입니다.

### 적용 예와 확인할 경계

SDK로 직접 확인할 수 있는 것은 전송과 공개 타입입니다. CLI 내부의 모델 루프는 문서화된 동작 범위로 설명합니다.

## CASA — 요청 준비와 CLI 제어 채널

옵션 준비 · ClaudeAgentOptions — cwd·시스템 지시·MCP 설정을 준비.

프로세스 연결 · SubprocessCLITransport._build_command — 옵션을 CLI 명령 인자로 변환.

제어 요청 · Query._handle_control_request — 권한·Hook·MCP 요청을 앱에서 처리.

CLI 내부의 요청 조립 순서와 재시도 분기는 공개 SDK 소스로 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

LOT-A 분석을 실행할 때 Python은 cwd와 허용 도구를 준비합니다. CLI가 제어 요청을 보내면 Query는 요청 종류에 맞는 콜백으로 전달하고 응답을 CLI로 돌려줍니다. 모델 호출 횟수와 Python 콜백 횟수는 별도입니다.

## CAS02 — 단발 요청과 대화형 클라이언트

SDK 클라이언트의 async with 범위 안에서 질문과 후속 질문을 전송할 수 있다. SDK 메시지 타입과 CLI 세션 수명은 별도로 추적한다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, ResultMessage):
        print(message.subtype)

async with ClaudeSDKClient(options=options) as client:
    await client.query(prompt)
    async for message in client.receive_response():
        if isinstance(message, ResultMessage):
            print(message.subtype)
```

### 화면 읽기

단발 query와 연결을 유지하는 ClaudeSDKClient는 앱이 관리할 연결 수명이 다릅니다.

### 적용 예와 확인할 경계

같은 LOT에 후속 질문을 보내는 경우 ResultMessage까지 읽고 이후 입력을 언제 보낼지 정합니다.

## CASB — Context·기억·재개 구분

실행 입력 · ClaudeAgentOptions.system_prompt — 지시와 cwd, 프로젝트 설정 범위를 선택.

대화 연결 · ClaudeAgentOptions.resume — 기존 세션 ID를 CLI에 전달.

업무 상태 · 앱 예시: LOT-A / r3 — 스냅샷과 보고서 버전은 앱에 기록.

전체 모델 payload의 조립 순서와 내부 기억 선택 로직은 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

r3 대화를 재개해도 디스크의 측정 파일은 r4로 바뀌었을 수 있습니다. 세션 ID는 대화 연결용으로 쓰고, 근거가 되는 보고서에는 조회 snapshot을 명시합니다.

## CAS05 — 세션 재개와 산출물 버전

CLI에 전달하는 resume/fork 옵션과 앱의 파일 버전 계약을 따로 설명한다. 파일 checkpointing/rewind는 별도 지원 조건을 확인해야 한다.

### 화면 읽기

세션 재개는 대화 연결이고 보고서 버전과 조회 시점은 별도 업무 상태입니다.

### 적용 예와 확인할 경계

이전 대화를 재개해도 cwd에 있는 파일이 바뀔 수 있으므로 결과의 snapshot과 revision을 함께 기록합니다.

## CAS03 — Python 조회 함수를 SDK MCP로 연결

SDK MCP는 Python 프로세스 안에서 함수를 실행한다. 외부 stdio/HTTP MCP는 별도 서버 경계를 가진다. 샘플의 권한 있는 범위는 앱에서 주입하는 fixture다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
@tool("read_lot", "Read an allowed LOT", {"lot_id": str})
async def read_lot(args):
    report = read_allowed_lot(args["lot_id"])
    return {"content": [{"type": "text", "text": report}]}

server = create_sdk_mcp_server(name="lot", tools=[read_lot])
options = ClaudeAgentOptions(
    mcp_servers={"lot": server},
    allowed_tools=["mcp__lot__read_lot"],
)
```

### 화면 읽기

Python 함수가 SDK MCP에 등록되면 CLI의 도구 요청을 SDK 제어 채널이 Python으로 전달합니다.

### 적용 예와 확인할 경계

SDK 내부 MCP의 실행 위치와 외부 stdio·HTTP 서버의 위치를 구분합니다. 도구 이름의 서버 접두사가 호출을 식별합니다.

## CASC — Tool 실행과 승인 경로

함수 연결 · create_sdk_mcp_server — Python 함수가 SDK 프로세스에 등록됨.

호출 정책 · Query._handle_control_request — CLI의 권한 요청을 콜백으로 연결.

함수 실행 · Query._handle_sdk_mcp_request — SDK MCP 요청을 처리하고 응답 반환.

내장 Tool의 스케줄링과 CLI 내부 검증 전부는 공개 SDK에서 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

SDK MCP의 read_lot은 Python에서 실행합니다. CLI가 요청한 인자가 LOT-B라면 Python의 업무 인가에서 거절합니다. 파일·셸 권한은 CLI 쪽 실행 정책과 별도로 확인합니다.

## CAS04 — 작업 환경과 도구 권한

Python 기본값은 permission_mode=None, max_turns=None, setting_sources=None이다. 이는 옵션 값이며 실효 권한 모드나 CLI 턴 한도와 분리한다. 파일 설정 사용은 명시적으로 설정하고 런타임별 sandbox 조건을 확인한다. Subagent·Plugin은 Sources에서 읽는다.

### 화면 읽기

작업 위치, CLI 정책, 데이터 인가를 각각 확인합니다.

### 적용 예와 확인할 경계

CLI가 read_lot 호출을 허용해도 업무 함수에서 LOT 접근 범위를 검사합니다. 옵션의 None은 유효 권한 모드 자체를 뜻하지 않습니다.

## CAS06 — 스트림과 구조화 결과

output_format의 JSON Schema와 앱 업무 규칙을 따로 둔다. 예시에는 조회 1건과 권한 거절 1건을 사용한다. CLI가 보고한 오류 subtype과 앱 검증 실패를 다른 로그로 남긴다.

### 화면 읽기

진행 중 메시지와 최종 ResultMessage를 구별하고 구조화 결과를 앱에서 검사합니다.

### 적용 예와 확인할 경계

수율 JSON이 스키마를 만족해도 해당 LOT의 조회값과 일치하는지 확인합니다.

## CASD — 결과·실패·관측을 구분하기

실행 진행 · StreamEvent — 부분 응답을 사용할 경우 진행 상태 기록.

실행 종료 · ResultMessage — subtype·세션 ID·구조화 결과 확인.

업무 저장 · 앱 예시: 92 / 100 확인 — LOT·버전·수치를 검증하고 발행.

Python에서 관측하는 메시지와 CLI 내부 전체 Trace의 대응은 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

부분 텍스트로 92%가 먼저 보여도 ResultMessage의 종료 상태와 구조화 결과를 확인합니다. 분모가 100인지 확인한 뒤 저장하고, 종료 오류와 저장 오류를 다른 상태로 기록합니다.

## CASE — Claude Code 환경을 앱에 연결하기

SDK가 연결 · ClaudeSDKClient — 세션·메시지·제어 요청을 앱에 노출.

실행환경이 제공 · ClaudeAgentOptions — 파일·셸·MCP·Subagent 구성.

앱이 구현 · 앱 예시: 격리·권한·저장 — 작업 디렉터리와 데이터 인가를 관리.

기존 Claude Code 방식의 도구와 작업 환경을 재사용할 때 적합합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

배포할 앱은 CLI의 설정 파일과 작업 폴더를 함께 결정합니다. 사용자마다 저장소 접근 범위가 다르면 인가를 Python 도구에서 적용하고, 내장 도구에는 별도 실행 격리를 설정합니다.

## ADKA — Agent 선언과 실행 준비

Agent · LlmAgent — 모델·지시·도구를 선언.

세션 · Runner.run_async — user_id·session_id로 실행 문맥 구성.

루프 · BaseLlmFlow — 모델·함수 처리 결과를 이벤트로 내보냄.

Agent 선언, 모델 실행, 상태 저장을 서로 다른 경계로 읽습니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

앱이 LOT-A 요청을 새 Content로 보내면 Runner가 세션과 호출 문맥을 준비합니다. Agent가 내보낸 이벤트에는 부분 메시지와 도구 실행 정보가 포함될 수 있으므로 UI가 최종 응답을 별도로 판단합니다.

## ADK01 — Runner와 이벤트 스트림

런타임 진입점은 Runner다. 앱의 세션 식별자와 실행 invocation을 분리한다. 인메모리 서비스는 실습용으로 적합하며 저장 수명은 서비스 구현에 따라 달라진다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
runner = Runner(agent=agent, app_name="yield_demo",
                session_service=session_service)
await session_service.create_session(
    app_name="yield_demo", user_id="operator", session_id="r3")
async for event in runner.run_async(
    user_id="operator", session_id="r3", new_message=message
):
    print(event.author, event.actions.state_delta)
```

### 화면 읽기

Runner는 앱의 요청을 invocation으로 실행하고 Agent 이벤트를 소비자와 세션 서비스에 연결합니다.

### 적용 예와 확인할 경계

user_id·session_id는 대화를 찾는 키이며 한 실행의 invocation과 범위가 다릅니다.

## ADK03 — Session·State·Memory·Artifact

temp: 값은 invocation용으로 취급한다. 보고서 바이트와 저장된 이벤트를 동일 저장물로 간주하지 않는다. context compaction·prefix caching은 모델 입력 비용과 관련된 별도 기능이다.

### 화면 읽기

Session, State, Memory, Artifact가 보관하는 내용과 생명주기를 비교합니다.

### 적용 예와 확인할 경계

보고서 바이트는 Artifact에, 버전 참조는 State에 둘 수 있습니다. 임시 State 값은 현재 invocation 범위를 따릅니다.

## ADK02 — 함수 응답과 상태 반영

Runner._process_and_append_event는 partial 및 저장 조건을 검사한다. BaseSessionService.append_event에서 state delta를 적용하는 경로를 확인한다. fixture의 응답은 good=92, total=100이다.

### 화면 읽기

함수 응답에는 모델에 반환할 값이 있고 state_delta에는 저장할 상태 변화가 들어갈 수 있습니다.

### 적용 예와 확인할 경계

92/100을 모델에 반환한 이벤트와 snapshot 값을 세션에 남기는 처리를 나눠 봅니다. 부분 이벤트도 구분합니다.

## ADKB — 함수 호출이 모델 응답으로 돌아가기

함수 계약 · FunctionTool — 함수를 모델용 Tool로 노출.

실행 문맥 · ToolContext — 업무 함수가 현재 실행의 상태에 접근.

이력 반영 · Runner._process_and_append_event — 저장 조건에 따라 SessionService로 전달.

함수 반환과 state_delta는 서로 다른 용도로 사용됩니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

read_lot이 92/100을 반환하고 ToolContext의 상태에 snapshot=r3을 남기는 예입니다. 모델에 전달하는 함수 응답과 세션에 반영할 state_delta를 각각 확인합니다.

## ADKC — 중단·승인·재개의 관찰 경계

승인 요청 · FunctionTool.check_require_confirmation — 인자에 따라 사용자 확인 필요 여부 검사.

이벤트 확인 · Event — 승인 요청과 응답을 호출과 연결.

업무 검증 · 앱 예시: r3 승인 → r4 거부 — 보고서가 바뀌면 다시 확인.

실효 승인 UI와 만료 정책은 실행 앱과 배포 환경에 따라 정합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

발행 함수의 확인 조건이 참이면 승인 전 상태와 승인 후 실행을 구분합니다. 같은 호출을 이어갈 때 실제 보고서 revision이 바뀌었다면 함수 본체에서 다시 검증합니다.

## ADK06 — 답변 완료와 발행 완료

고정 모델 응답에서 답변 이벤트는 수집하되 발행 상태는 앱에서 저장 성공 이후 기록하도록 설계한다. 예제의 실패 기대값이며 SDK 재시도나 원자성을 가정하지 않는다.

### 화면 읽기

모델이 최종 답변을 보낸 시점과 업무 산출물이 저장된 시점은 각각 확인합니다.

### 적용 예와 확인할 경계

Artifact 저장을 실패시키면 앱은 사용자 응답과 발행 상태를 다르게 기록해야 합니다.

## ADK04 — Agent 전이와 고정 순서

조회·계산·승인의 순서가 업무 계약이면 실행 모델에 드러낸다. ADK 2.x Graph는 다음 장에서 별도 실행 경로로 설명한다.

### 화면 읽기

도구로 하위 Agent를 부르는 경우, 실행을 넘기는 경우, 코드가 순서를 정하는 경우입니다.

### 적용 예와 확인할 경계

검증을 반드시 거쳐야 한다면 모델의 선택에만 맡기는 구조와 명시적 Workflow를 비교합니다.

## ADK05 — ADK 2.x Graph 스케줄러

Workflow._run_loop를 중심으로 준비된 노드 스케줄과 노드 체크포인트를 설명한다. 장표의 LOT 그래프는 업무 설계 예시다. 체크포인트를 전체 Python 프로세스 스냅샷으로 해석하지 않는다.

### 화면 읽기

Graph는 준비된 노드를 의존성과 스케줄 조건에 맞춰 시작합니다.

### 적용 예와 확인할 경계

조회 후 두 분석 노드가 준비되는 예입니다. 노드 체크포인트를 프로세스 전체 상태나 외부 발행 복구 보장과 동일시하지 않습니다.

## ADKD — 그래프와 모델 루프의 경계

의존성 · Workflow._run_loop — 업무 노드의 실행 가능 상태를 읽음.

실행 선택 · _schedule_ready_nodes — 준비된 노드의 실행을 조율.

진행 기록 · _emit_node_checkpoint — 노드 체크포인트를 남기는 경계.

모델 내부 추론과 관리형 배포 내부의 복구 구현은 공개 Python 소스로 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

조회가 끝나야 분석 두 개를 시작하고, 두 분석이 끝나야 검증에 진입하는 예입니다. Node 준비 조건과 Agent 모델 요청 횟수를 따로 기록하면 병렬성이 어느 층에서 생겼는지 확인할 수 있습니다.

## ADK07 — 실행 설정과 이벤트 검증

Callback과 Plugin 개입은 어떤 이벤트 또는 호출을 변경하는지 함께 기록한다. Live, 평가, 관리형 배포는 공식 가이드의 지원 범위를 별도로 확인한다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
config = RunConfig(max_llm_calls=3)
async for event in runner.run_async(
    user_id="operator",
    session_id="r3",
    new_message=message,
    run_config=config,
):
    if event.is_final_response():
        print(event.author)
```

### 화면 읽기

실행 설정으로 바꾼 조건이 이벤트 흐름과 업무 결과에 어떻게 드러나는지 확인합니다.

### 적용 예와 확인할 경계

테스트에서는 정상 실행과 실패 실행을 같은 입력으로 비교하고 완료 이벤트뿐 아니라 저장 성공을 검사합니다.

## ADKE — ADK의 이벤트 중심 개발 방식

실행 · Runner.run_async — 모델과 도구 진행을 이벤트로 소비.

상태 · BaseSessionService.append_event — 저장할 이벤트와 변경 상태를 반영.

앱이 구현 · 앱 예시: Artifact 발행 검증 — 답변과 파일 저장을 별도로 확인.

세션·산출물·업무 그래프를 함께 관리하는 앱에서 실행 경계가 드러납니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

분석 결과 텍스트가 도착해도 Artifact 저장이 실패하면 발행 상태는 실패입니다. 이벤트를 소비하는 화면과 업무 저장소에서 각각 같은 LOT 및 revision을 확인합니다.

## MAF01 — Agent 실행과 업무 Workflow

WorkflowBuilder와 Workflow.run이 바깥 실행이다. AgentSession과 Workflow checkpoint를 각각 저장할 이유가 있다. .NET과 Foundry 배포 기능은 Python 코드와 구분한다.

### 화면 읽기

한 Agent의 모델·도구 실행과 업무 단계를 명시한 Workflow를 나눕니다.

### 적용 예와 확인할 경계

조회·검증·발행의 필수 순서가 있다면 각 단계가 받은 값과 보낸 값을 별도로 기록합니다.

## MAFA — Agent와 Workflow를 연결하는 순서

Agent 실행 · AgentExecutor — Agent를 업무 단계 하나로 연결.

경로 선언 · WorkflowBuilder — Executor 사이의 Edge와 시작점 정의.

외부 실행 · Workflow.run — 메시지를 전달하고 실행 이벤트를 내보냄.

한 Agent의 모델 반복과 업무 Workflow의 진행을 별도 단위로 추적합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

조회 Agent의 출력은 Workflow의 다음 단계 입력입니다. Agent 내부에서 여러 번 모델을 불러도 바깥에서는 한 업무 단계의 입력과 출력을 기준으로 추적합니다.

## MAF02 — Executor와 Edge의 메시지 계약

WorkflowBuilder에서 연결한 Edge는 워크플로의 연결 계약이다. SDK 실행 계약에 더해 앱이 최신 데이터와 업무 키를 검사한다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
builder = WorkflowBuilder(start_executor=read_lot)
builder.add_edge(read_lot, analyze)
builder.add_edge(analyze, approve)
builder.add_edge(approve, publish)
workflow = builder.build()

async for event in workflow.run(request, stream=True):
    print(event.type)
```

### 화면 읽기

Executor는 업무 처리를 담당하고 Edge는 결과를 다음 실행으로 보냅니다.

### 적용 예와 확인할 경계

출발점의 보고서 타입과 수신 단계가 기대하는 타입을 맞춰 검증 오류를 더 일찍 드러냅니다.

## MAF03 — AgentExecutor의 입력과 출력

str, Message 및 메시지 목록 등 입력 경로가 있다. Agent가 생성한 결과와 호출자가 소비하는 이벤트 및 다음 단계의 데이터 타입을 구별한다.

### 화면 읽기

AgentExecutor의 입력과 출력은 Workflow가 전달하는 메시지 계약입니다.

### 적용 예와 확인할 경계

모델에게 보여 준 대화와 다음 Executor에 보낼 업무 결과가 같아야 한다고 가정하지 않습니다.

## MAFB — 도구 결과와 업무 출력 전달

입력 받기 · AgentExecutor.from_message — Workflow 메시지를 Agent 입력으로 전달.

실행과 중단 · AgentExecutor._run_agent_and_emit — Agent 응답·사용자 입력 요구 처리.

후속 검증 · AgentExecutorResponse — 다음 단계에서 LOT·snapshot을 대조.

공급자 측 도구 호출 정책과 모델 내부 추론은 Workflow 소스로 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

검증 Executor는 AgentExecutorResponse를 받아 근거의 LOT와 snapshot을 확인합니다. r4 데이터가 섞였으면 타입이 정상이어도 r3 보고서 발행으로 보내지 않습니다.

## MAFC — 대화와 체크포인트에 남는 값

대화 · AgentSession — Agent가 후속 요청에 사용할 상태.

업무 진행 · Workflow.run — 체크포인트에서 실행 위치 복원.

업무 효과 · 앱 예시: 발행 멱등 키 — 이미 처리된 r3 발행의 재실행 방지.

외부 저장소의 트랜잭션과 발행 복구 정책은 앱에서 별도로 정합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

발행 직후 중단된 경우 체크포인트만으로 외부 발행 성공 여부를 단정할 수 없습니다. 재개할 때 저장소에서 LOT-A/r3 멱등 키를 조회해 중복 쓰기를 막습니다.

## MAF05 — 승인 대기와 응답 연결

Workflow의 일반 외부 요청과 AgentExecutor의 도구 승인 중계 경로를 구분한다. 업무 승인 범위와 만료, 요청 ID 대응은 호스트 계약이다.

### 화면 읽기

사람에게 보낸 질문과 돌아온 응답을 해당 요청 ID로 연결합니다.

### 적용 예와 확인할 경계

승인 대기 이벤트와 실제 발행 이벤트 사이에 보고서 버전과 승인 범위를 확인합니다.

## MAFD — 승인 요청과 재개 이벤트

실행 중 요청 · AgentExecutor._run_agent_and_emit — Agent 입력 요청을 Workflow로 연결.

호스트 확인 · 앱 예시: 요청 ID + r3 — 승인자·버전·유효기간 검증.

후속 실행 · Workflow.run — 사용자 응답을 전달하고 실행 관찰.

승인 완료, 업무 검증 성공, 발행 성공을 각각 확인합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

응답에 연결할 요청 ID와 검토한 보고서 revision을 호스트에 저장합니다. 승인 이벤트가 도착해도 입력 검증을 통과해야 후속 단계로 넘깁니다.

## MAF04 — 병렬 결과를 결합하는 업무 키

SDK가 제공하는 fan-in 경로와 결합 데이터의 업무 검증은 별개다. 같은 키의 중복, 서로 다른 snapshot 혼입, 한 결과 누락을 각각 검증한다.

### 화면 읽기

병렬 분석 결과는 도착 시간 대신 LOT와 snapshot 같은 업무 키로 연결합니다.

### 적용 예와 확인할 경계

같은 LOT의 다른 날짜 결과를 잘못 합치지 않도록 두 분석이 참조한 snapshot을 대조합니다.

## MAF06 — 체크포인트와 외부 발행 복구

checkpoint_storage 기본 None. 인메모리는 프로세스 내 확인, 파일 저장은 재시작 확인에 사용한다. 체크포인트 스키마와 외부 부작용이 별개이므로 발행에 idempotency key를 둔다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
storage = FileCheckpointStorage("./checkpoints")
builder = WorkflowBuilder(
    start_executor=read_lot, checkpoint_storage=storage
)
builder.add_edge(read_lot, analyze)
workflow = builder.build()
await workflow.run(request)
checkpoints = await storage.list_checkpoints(
    workflow_name=workflow.name
)
```

### 화면 읽기

Workflow 체크포인트는 어디서 재개할지 알려주고 외부 서비스는 별도의 발행 상태를 가집니다.

### 적용 예와 확인할 경계

발행 직후 장애가 나면 먼저 같은 업무 키의 성공 기록을 확인한 뒤 재호출 여부를 결정합니다.

## MAF07 — Agent와 명시적 Executor의 배치

빌더는 반복되는 orchestration의 시작점이다. Agent/Function middleware, context provider, Foundry 연동과 .NET은 기능별 지원 범위를 Sources에서 분리한다.

### 화면 읽기

언어를 이해하고 제안을 만드는 단계와 업무 규칙을 고정해야 하는 단계를 나눕니다.

### 적용 예와 확인할 경계

모델이 가설을 쓰고 Executor가 92/100 계산과 승인 계약을 검사하는 구조를 생각하면 됩니다.

## MAFE — 업무 순서와 복구를 코드로 선언하기

실행 그래프 · WorkflowBuilder — 조회·분석·검증 순서를 앱 코드에 표현.

Agent 경계 · AgentExecutor — 언어 판단을 업무 단계 하나로 배치.

앱이 구현 · 앱 예시: 동일 revision 검증 — 병렬 결합 키와 외부 효과를 관리.

순서·승인·복구 요구가 명확한 업무에서 구조를 드러낼 수 있습니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

조회·승인·발행의 필수 순서를 Edge로 명시하면 실패한 단계를 찾기 쉽습니다. Executor 사이에 전달하는 값과 복구 저장소는 업무 규모에 맞춰 설계합니다.

## OAIA — Agent 선언에서 Runner까지

Agent 선언 · Agent — 지시·모델·Tool·출력 타입 설정.

실행 시작 · Runner.run — 입력으로 실행을 시작하거나 상태로 재개.

다음 상태 · turn_resolution.py — 응답에서 도구·전이·종료 경로를 선택.

활성 Agent가 바뀌면 다음 턴의 지시와 도구도 달라질 수 있습니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

Agent가 read_lot을 제안하면 Runner는 함수 실행 결과를 처리하고 다음 모델 요청이나 종료를 결정합니다. 전문 Agent로 전이했다면 다음 요청의 지시와 도구 구성이 바뀔 수 있습니다.

## OAI01 — Runner가 한 턴을 해석하는 방식

Runner.run의 진입과 turn_resolution의 후속 상태 결정 경로를 짚는다. max_turns=None은 턴 한도를 비활성화한다. 모델 호출과 Tool 횟수는 각각 기록한다.

### 화면 읽기

Runner가 현재 Agent의 모델 응답에서 출력, Tool, Handoff 경로를 고릅니다.

### 적용 예와 확인할 경계

같은 요청에 Tool 응답이 오면 그 결과로 다시 호출할 수 있고, 유효한 최종 결과 경로는 실행을 마칠 수 있습니다.

## OAI04 — Session과 RunState의 저장 경계

업무 보고서·승인 이력은 앱이 별도로 보관한다. 관리되는 대화 기능에는 provider 전제가 있다. RunState는 멈춘 실행의 재개에 쓰고 중복 발행 제어는 업무 키로 처리한다.

### 화면 읽기

Session은 대화 입력을 이어주는 데 쓰고 RunState는 중단된 실행을 이어주는 데 씁니다.

### 적용 예와 확인할 경계

승인 대기 중 저장해야 할 호출·결정과 이전 대화 이력, 공급자 대화 식별자를 분리합니다.

## OAIC — 모델 입력과 실행 중단 상태

대화 이력 · Runner.run — Session에서 이전 입력·결과를 읽음.

중단 보존 · RunState — 미결 승인과 실행 진행을 보관.

업무 상태 · 앱 예시: r3 보고서 참조 — 산출물·승인 기록을 별도 관리.

공급자 측 대화 연결은 API 지원 범위에 따르며 서버 내부는 확인 불가.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

Session은 앞선 대화 항목을 다음 Run에 연결합니다. 발행 승인에서 멈춘 현재 Run을 이어가려면 호출과 결정이 포함된 RunState를 보관합니다.

## OAIB — 도구 등록·인가·실행 경로

등록 · function_tool — 함수에서 모델용 인자 계약을 구성.

실행 경계 · FunctionTool — 인자 처리와 입력 검사, 함수 실행.

다음 턴 · _maybe_finalize_from_tool_results — 결과에 적용할 종료 정책 판단.

Tool schema 검증을 통과해도 LOT와 보고서 버전 인가는 앱이 수행합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

같은 조회 결과에서 run_llm_again은 후속 모델 호출을 허용하고 stop_on_first_tool은 결과를 최종값으로 선택합니다. 최종값을 고르는 정책이 같은 턴의 호출 실행 횟수까지 뜻하지는 않습니다.

## OAI02 — 도구 결과로 종료하는 정책

_maybe_finalize_from_tool_results와 도구 결과 선택 함수를 함께 읽는다. 함수 도구 결과의 종료 정책과 PydanticAI EndStrategy가 적용되는 출력 경로를 구분한다. 두 도구가 제안된 턴에서 최종값과 실제 실행 횟수를 함께 기록한다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
agent = Agent(
    name="Yield analyst",
    tools=[read_lot],
    tool_use_behavior="run_llm_again",
)
normal = await Runner.run(agent, prompt)
direct = await Runner.run(
    agent.clone(tool_use_behavior="stop_on_first_tool"), prompt
)
```

### 화면 읽기

Tool 결과를 다시 모델에 전달할지 그대로 종료에 사용할지 정책에 따라 달라집니다.

### 적용 예와 확인할 경계

동일한 A17 조회 응답으로 모델 요청 수와 최종 결과 타입을 비교합니다. 도구 호출 정책은 실행 권한과 별도입니다.

## OAI05 — Guardrail과 Tool 승인

입력 guardrail의 선행 실행을 선택할 수 있다. Tool guardrail은 function-tool 경로에 적용되며 기본 승인 순서와 사전 검사 옵션을 구분한다. 전역 업무 인가를 별도로 검증한다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
@function_tool(needs_approval=True)
async def publish_report(lot: str, revision: str) -> str:
    return await publish_once(lot, revision)

result = await Runner.run(agent, prompt)
if result.interruptions:
    state = result.to_state()
    for item in result.interruptions:
        if approved_for_r3(item):
            state.approve(item)
    result = await Runner.run(agent, state)
```

### 화면 읽기

Agent 입력·출력 검사, Function Tool 검사, 승인 대기는 적용 위치가 다릅니다.

### 적용 예와 확인할 경계

승인 필수 Tool의 입력 검사는 기본적으로 승인 뒤 실행 직전에 수행됩니다. 사전 검사 설정을 켜도 승인 뒤 다시 검사합니다.

## OAID — 승인과 Guardrail 순서 따라가기

호출 중단 · function_tool(needs_approval=True) — 발행 전에 승인 결정을 기다림.

검사 순서 · pre_approval_tool_input_guardrails — 사전 검사를 켜도 승인 후 다시 검사.

후속 실행 · RunState.approve — 해당 호출을 승인하고 Runner에서 재개.

Function Tool의 검사를 Handoff 자체에 적용되는 정책으로 읽지 않습니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

승인 필수 도구는 기본 경로에서 승인 후 실행 직전에 입력 검사를 합니다. 사전 검사 옵션을 켠 경우에도 승인 뒤 다시 확인하므로 시간에 따라 바뀌는 업무 조건을 검사할 수 있습니다.

## OAI03 — Agent.as_tool과 handoff

Agent.as_tool의 중첩 실행과 execute_handoffs를 대비한다. 입력 필터와 다음 Agent에 전달되는 이력을 확인하고, 중첩 Agent 승인 전파는 보충 해설에 둔다.

Python API 발췌입니다. 앱 정의와 import를 생략했습니다.

```python
manager = Agent(
    name="Manager", tools=[expert.as_tool(
        tool_name="ask_expert", tool_description="Summarize LOT"
    )]
)
triage = Agent(
    name="Triage", handoffs=[handoff(expert, input_filter=filter_history)]
)
result = await Runner.run(triage, prompt)
print(result.last_agent.name)
```

### 화면 읽기

Agent.as_tool은 중첩 실행 결과를 부모에게 반환하고 handoff는 실행 주체를 전환합니다.

### 적용 예와 확인할 경계

통계 검토 뒤 부모가 답하는 경우와 검토 Agent가 이후 사용자 응답을 맡는 경우를 비교합니다.

## OAI06 — Trace에서 실행 주체 확인

tracing_disabled의 RunConfig 기본값은 False이며 전역 설정도 영향을 준다. trace_include_sensitive_data는 환경 기반 기본값을 읽는다. 화면에는 합성 데이터와 명시적 민감 데이터 제외 설정을 사용한다.

### 화면 읽기

Trace에서 현재 Agent와 모델 호출, 함수, 전이 구간을 연결합니다.

### 적용 예와 확인할 경계

민감 데이터 포함 설정을 먼저 확인합니다. Trace에서 호출이 보인다는 사실과 승인 감사 기록을 보관했다는 사실은 별개입니다.

## OAI07 — 고정 모델 응답으로 실행 비교

시연의 기준 입력은 LOT-A, snapshot r3, 92/100이다. Hosted tools, MCP, Realtime 및 sandbox·skills는 지원 API 및 provider 전제가 다른 별도 기능이다. 장표에는 실험 설계와 예상 관찰값을 제시한다.

### 화면 읽기

고정 응답을 써서 모델의 선택과 SDK의 실행 규칙을 분리하는 실험입니다.

### 적용 예와 확인할 경계

동일 입력에서 Tool 실행 횟수, 최종 Agent, 승인 전후 실행 기록을 비교합니다. 이 장의 설계와 실모델 결과는 구분합니다.

## OAIE — 실행 주체 전환을 앱에서 읽기

결과 위임 · Agent.as_tool — 하위 실행 결과가 부모에게 돌아옴.

주체 전환 · execute_handoffs — 다음 응답을 맡을 Agent가 바뀜.

앱이 구현 · 앱 예시: 승인·발행 기록 — 전이와 외부 효과를 각각 추적.

업무 분배 방식과 최종 응답의 책임을 함께 정합니다.

### 화면 읽기

Space로 각 행을 강조합니다. 가운데 열은 고정 버전의 소스 심볼 또는 명시한 앱 예시이며, 오른쪽 열에서 그 단계가 맡는 일을 확인합니다.

### 적용 예와 확인할 경계

수율 검토 결과만 받아 종합하려면 부모가 하위 Agent를 도구로 호출합니다. 이후 질의 대응까지 넘기려면 handoff 경로를 사용하고 Trace에서 활성 Agent를 확인합니다.

## S43 — Agent를 어디에서 실행할까?

## Agent를 어디에서 실행할까?

### 주요 개념

**중앙 실행**: 서버가 Agent·작업·사용자 격리·공통 운영을 관리합니다.

**로컬 실행**: 사용자 PC에 설치·업데이트·실행 권한 관리가 필요합니다.

### 설명

Agent의 CPU/메모리, Tool I/O, 승인·모델 대기와 모델 서버 GPU 자원은 수명이 다릅니다. 로컬 Agent도 모델 요청으로 정보를 보낼 수 있어 데이터 경로를 확인해야 합니다. Worker/GPU 수는 모델, 부하, Context와 실제 대기를 측정한 뒤 정합니다.

### 발표 포인트

Agent 실행 자원과 모델 서버 자원을 나누어 살펴봅니다.

### 화면 읽기

실행 위치가 달라지면 파일, 자격 증명, 도구, 사용자 승인에 접근하는 경계도 바뀝니다.

### 적용 예와 확인할 경계

같은 검사 데이터를 중앙과 로컬에서 실행할 때 어떤 값이 환경을 넘어가는지 그림을 따라 확인합니다.

## S44 — 한 요청을 끝까지 검증하기

입력 — 요청 직전 messages·tools 확인. 지시·조회 범위·이력 전달.

실행 — Tool Call ID와 실제 실행 연결. 검증 실패·승인 전에는 실행 0회.

결과 — 원본 snapshot과 수치 비교. A17의 42 / 1000 = 4.2%.

복구 — 실패 후 같은 업무 키로 재시도. 저장 성공 여부와 중복 발행 확인.

### 화면 읽기

실행 과정의 증거와 최종 업무 결과의 검증을 나눕니다.

### 적용 예와 확인할 경계

Tool 호출의 성공 여부와 보고서 수치가 원본과 일치하는지는 별도 기준으로 기록합니다.

## S45 — 내 Agent를 만들 때 결정할 것

어떤 작업을 맡길까? — 조회·분석·발행의 경계. 모델 판단 / 고정 업무 규칙.

어떤 기능을 줄까? — Tool과 실제 데이터 접근 범위. 읽기 / 쓰기 / 사용자 승인.

무엇을 다음 실행에 남길까? — 대화·기억·실행 상태·보고서. 저장 수명 / 복원 / 버전.

어떻게 맞았다고 확인할까? — 실행 기록과 원본 근거. 재시도 / 중복 방지 / 평가.

### 화면 읽기

발표에서 본 실행 구조를 실제 개발의 선택으로 연결합니다.

### 적용 예와 확인할 경계

같은 문제를 구현할 때 모델·도구·정책·상태의 담당자를 정하고 3차에서 결과와 검증 기록을 비교합니다.

# 심층 개념 해설

발표자 개념 해설 — 슬라이드에 억지로 넣지 말 것

## C-1. 이번 발표의 용어와 공개 범위

| 용어 | 여기서의 의미·조건 |
|---|---|
| Hermes Turn | 사용자 입력을 받아 여러 모델/도구 왕복을 거칠 수 있는 실행 단위 |
| PydanticAI Run | Agent 실행 호출 단위. 하나의 Run에 여러 Step이 있을 수 있음 |
| Conversation/Session | 이어지는 대화의 논리적 단위. 일반 용어와 특정 API 타입을 구별 |
| Internal Graph | PydanticAI 내부의 pydantic-graph 실행. LangGraph 아님 |
| Function Tool | 앱이 구현한 함수 실행 경로. 모델은 이름/인자 요청을 생성 |
| Native Tool | 공급자 측 실행 기능. 로컬 함수와 실행·관찰 경계가 다를 수 있음 |
| Capability | Python 실행 동작·지시·도구·설정을 조합하는 확장 단위 |
| Harness 패키지 | PydanticAI Core와 별도 설치·버전의 기능 모음. Hermes 같은 완성형 제품과 동일한 배포 형태라는 뜻은 아님 |
| Trace | 요청·실행·반환·상태 전이의 외부 기록. 비공개 추론 원문 아님 |

Hermes는 공개 소스와 문서로 구현을 설명한다. Claude Code는 공개 계약 중심이며 SDK 래퍼 공개를 엔진 전체 공개로 확대하지 않는다. PydanticAI는 고정 Core 소스와 현행 Harness 문서를 구별한다.

## C-2. 최소 코드 — 실제 API와 앱 코드를 함께 보여주기

다음은 **실제 API를 사용한 합성 데이터 예제, 미실행**이다. C-2/C-6/C-8 코드는 독립 예제이며 한 파일로 단순 연결하지 않는다. 모델·패키지 설치와 endpoint는 E의 계약을 따른다. `SEMINAR_MODEL_BASE_URL`은 Codex에서 10000, Antigravity에서 10001로 설정한다. 실제 OpenAI key는 이 환경에 넣지 않는다.

```python
import asyncio
import os
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

@dataclass
class DemoDeps:
    allowed_lots: frozenset[str]
    snapshot_id: str

model = OpenAIChatModel(
    'demo-model',
    provider=OpenAIProvider(
        base_url=os.environ['SEMINAR_MODEL_BASE_URL'],
        api_key=os.environ['SEMINAR_PROXY_TOKEN'],
    ),
)
agent = Agent(model, deps_type=DemoDeps,
              instructions='조회 결과로만 답하고 분모와 시점을 함께 밝혀라.')

@agent.tool
async def get_bin_summary(ctx: RunContext[DemoDeps], lot_id: str) -> dict:
    """합성 LOT의 BIN-X 집계를 반환한다. 실제 DB가 아닌 교육용 데이터다."""
    if lot_id not in ctx.deps.allowed_lots:
        raise PermissionError('허용되지 않은 LOT')
    return {'lot_id': lot_id, 'bin': 'BIN-X', 'count': 4, 'total': 100,
            'ratio': 0.04, 'snapshot_id': ctx.deps.snapshot_id}

@agent.tool_plain
def calculate_ratio(numerator: int, denominator: int) -> float:
    """0보다 큰 분모로 비율을 계산한다."""
    if denominator <= 0:
        raise ValueError('분모는 양수여야 한다')
    return numerator / denominator

async def main():
    deps = DemoDeps(frozenset({'LOT-DEMO'}), 'synthetic-v1')
    first = await agent.run('LOT-DEMO의 BIN-X를 조회해줘', deps=deps)
    second = await agent.run('그 비율의 분모는?', deps=deps,
                             message_history=first.all_messages())
    print(second.output)

if __name__ == '__main__':
    asyncio.run(main())
```

`OpenAIChatModel`을 명시해 Chat Completions 계약을 고른다. 원문의 `Agent('openai:<model-id>')`는 실존 API 사용 예지만 Provider 기본 선택을 맡기므로 vLLM 이관 예제에 그대로 사용하지 않는다. OpenAI라는 클래스/프로토콜 이름이 실제 upstream을 Demo에 알려주는 것은 아니다. [P07]

PermissionError/ValueError가 항상 ModelRetry로 자동 바뀐다고 설명하지 않는다. 업무적으로 고칠 수 있는 실패만 명시적으로 ModelRetry로 바꾸고, 권한 거절은 재시도로 우회하지 못하게 한다. Tool 내부 서버 인가는 UI·모델 선택과 무관하게 집행한다.

## C-3. 실행 API·스트리밍을 정확히 고르기

| 실제 이름 | 반환/관찰 목적 | 발표 시 구분 |
|---|---|---|
| run_sync() | 동기 최종 결과 | 일반 스크립트. 이미 event loop가 도는 서버에서는 async run 사용 |
| await run() | 비동기 최종 결과 | ‘비동기’ 자체가 청중에게 delta를 출력한다는 뜻은 아님 |
| run_stream() | context manager 안에서 출력 stream 소비 | 첫 출력 확정과 나머지 Tool 처리의 관계 주의 |
| run_stream_events() | 모델/도구/최종 결과 이벤트 소비 | 델타·호출·결과를 직접 UI에 연결할 때 |
| iter() | 노드 단위 Graph 실행·관찰 | UserPromptNode/ModelRequestNode/CallToolsNode와 state 확인 |

원문의 `run_steam_evnets`는 `run_stream_events`로 정정한다. Demo는 기본 실행을 바꾸지 않고 이벤트/요청 경계 관찰을 우선한다. `run_stream()`에서 이미 출력이 확정된 경우를 비스트리밍 EndStrategy 시험과 섞지 않는다. 스트림 종료가 원격 Tool 부작용 취소나 DB rollback을 뜻하지 않는다. [P01][P03][P10]

## C-4. Toolset·병렬·2단계 처리

`@agent.tool`은 RunContext가 필요한 함수, `@agent.tool_plain`은 일반 함수를 등록한다. 모델 schema에는 ctx 객체를 요구하지 않는다. FunctionToolset으로 함수를 묶고 filtered/prefixed/combined 같은 변형을 적용한다. Toolset은 함수 목록뿐 아니라 노출·준비·실행을 감싸는 확장 접점이다. [P05][P09]

ToolManager에서 step별 정의를 준비하고 인자 validation/execute를 구분한다. 버전별 내부 메서드를 화면에 10개 나열하는 대신 **검증된 인자→정책/보류→실행** 경계를 설명한다. 원문 tool_manager 행 번호와 ‘21.2’는 안정 출처가 아니므로 고정 파일·심볼 참조로 대체한다. [P08]

PydanticAI는 async task로 I/O 대기를 겹치며 sync Tool은 worker thread를 쓸 수 있다. `sequential=True`는 barrier이지 transaction이 아니다. 결과 완료 시각과 메시지 기록 순서를 구별해 관찰한다. Hermes도 여러 Tool을 실행하는 것과 자식 AIAgent 실행을 구분한다. 상호작용·파일 경로 충돌 등 실제 segment planner 조건을 무시한 ‘전부 ThreadPool 병렬’ 그림을 쓰지 않는다. [P10][H13]

## C-5. Output과 EndStrategy — 중요한 예외

최종 구조는 `output_type`/output function의 계약이며 Tool의 Python 반환형은 개별 실행 결과의 계약이다. 둘은 상호 대체가 아니다. `Finding`만 지정하면 최종 성공 출력은 그 타입을 따라야 한다. 범용 대화와 보고서를 함께 원하면 text+structured output 같은 여러 허용 타입, 역할별 Agent, 업무 단계를 설계할 수 있다. 무한히 모든 용도에 한 고정 보고서 schema를 적용할 필요는 없다. [P11]

다음은 **실제 API 기반 독립 예제, 미실행**이다. schema는 수치 범위만, validator는 근거 문장 최소 조건만 확인한다. 실제 근거 데이터와의 일치는 별도 코드가 검사해야 한다. `test`는 SDK 시험 모델이므로 vLLM 연결 Demo와 구분한다.

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry

class Finding(BaseModel):
    lot_id: str
    ratio: float = Field(ge=0, le=1)
    basis: str

agent = Agent('test', output_type=Finding, retries=2)

@agent.output_validator
def check_finding(output: Finding) -> Finding:
    if len(output.basis.strip()) < 10:
        raise ModelRetry('basis에 조회 근거와 기간을 구체적으로 적어라.')
    return output
```

v2.61.0 `_tool_execution.py`의 `_EarlyProcessor`, `_GracefulProcessor`, `_ExhaustiveProcessor`를 기준으로 S28을 설명한다. 다음은 **비스트리밍, 모두 유효, Retry/승인 없음, 출력용 도구 두 개 O1/O2가 등록됨**이라는 통제 조건이다. [P10]

| 정책 | Function A | Output O1 | Function B | Output O2 | 결과 |
|---|---|---|---|---|---|
| early | 생략 | 실행 | 생략 | 생략 | O1 |
| graceful | O1 전 실행 | 실행 | 실행 가능·이 예에서는 실행 | 생략 | O1 |
| exhaustive | 실행 | 실행 | 실행 | 실행 | emission 순서상 첫 유효 O1 |

graceful은 pending Function batch를 Output 앞에서 비우고, 성공 Output 이후 다른 Output은 stub 처리하지만 뒤 Function batch도 flush한다. exhaustive는 기본 동시 실행이므로 완료가 빠른 Output이 무조건 최종 승자가 아니다. `sequential=True` barrier가 있으면 구간이 나뉜다.

예외는 노트에서 분명히 설명한다. early에서도 모든 Output이 실패하면 수정에 필요한 Function 실행 경로가 있다. graceful/exhaustive에서는 Function ModelRetry가 선택한 결과를 억제해 다음 호출을 요구할 수 있다. Native/Prompted structured output과 Function call의 혼합은 출력용 Tool의 순서 사례와 별도이며, plain str preamble도 같은 조기 종료로 해석하면 안 된다. 이미 stream에서 확정된 결과는 retry-wins 예외가 있다. [P03]

**시사점:** 보고서 생성과 배포를 분리하고, Tool 권한·승인·멱등성을 독립적으로 구현한다. 성공 Output을 받았다는 사실만으로 후행 부작용이 없었다고 결론내리지 않는다.

## C-6. Hooks/Capabilities — 실제 API 골격과 합성

다음은 **현행 공식 API 기반 축약, 미실행**이다. 관찰 Hook은 payload를 복사/가림 처리해 기록하고 원본을 반환한다. 이 위치는 provider 직전 최종 wire JSON과 같지 않을 수 있어 transport 관찰도 별도로 필요하다. [P13]

```python
from pydantic_ai import Agent, ModelRequestContext, RunContext
from pydantic_ai.capabilities import Hooks

hooks = Hooks()

@hooks.on.before_model_request
async def observe_request(ctx: RunContext,
                          request_context: ModelRequestContext) -> ModelRequestContext:
    # 교육용: 메시지 개수만 관찰한다. 실제 payload는 별도 안전한 recorder 사용.
    print(len(request_context.messages))
    return request_context

agent = Agent('test', capabilities=[hooks])
```

단순 애플리케이션 Hook은 Hooks, 재사용할 Tool·지침·설정까지 묶는 기능은 Capability 또는 AbstractCapability로 구성한다. 원문의 `Capability(id='fab-policy', instructions=...)` 형태는 현행 문서에서 확인되는 코드 정의 방식이므로 잘못된 API라고 폐기하지 않는다. 다만 이 예만으로 실행 인가 Hook이 생기는 것은 아니다. [P14][P18]

여러 Capability의 전형적인 before는 바깥→안쪽, after는 역순, wrap은 중첩된다. **한 Hooks 인스턴스 내부 등록 순서와 Capability 간 순서는 구분**한다. 명시 ordering 제약이 있으면 실제 합성 순서가 단순 list와 다를 수 있으므로 Demo 기록으로 확인한다. 공용 capability 인스턴스에 tenant별 변경 상태를 무심코 저장하지 말고 Run 단위 수명으로 분리한다. [P14]

반도체 설계 예시: before model에서 근거 snapshot 기록, Tool execute 앞에서 인증된 tenant·조회 범위 검사, 결과 후처리에서 단위·민감정보 처리, wrap에서 감사·시간 측정. 모델에게 보여줄 지시와 코드로 강제할 정책을 섞지 않는다.

## C-7. History·Memory·Compaction의 제공 경계

| 문제 | 제공되는 것 | 앱이 정할 것 |
|---|---|---|
| 다음 Run 이어가기 | typed messages, serialization, message_history, 현행 conversation | 사용자 인증·불러오기·저장·동시 갱신·TTL |
| 오래된 요청 내용 줄이기 | Provider-native/Core 또는 Harness 전략 | 원본 보관, 정확 수치·Tool 쌍·최신 정책 보존 |
| 여러 대화의 기억 | 별도 Harness Memory와 store 추상화 | namespace의 인증, 저장할 사실·수명·수정 권한 |
| 도메인 지식 검색 | Function Tool/MCP 통합 | SOP revision·검색 품질·접근 제어 |

따라서 ‘대화·메모리·압축을 전부 직접 구현해야 한다’는 답은 부정확하다. 반대로 Agent 객체 하나 만들면 모든 사용자의 과거 대화가 자동 조회된다는 답도 부정확하다. 같은 객체의 설정과 각 대화의 실행 상태를 분리한다. [P06][P15][P16][P17]

Core의 native compaction은 모델/Provider 지원에 의존한다. vLLM 이관은 범용 Harness 전략부터 시험한다. trim/clear/summary가 Run history에 반영되는 경우 이전 전체 이력이 자동 복원된다고 말하지 않는다. 대형 raw Tool 결과는 조회 단계에서 요약/범위를 제한하는 것도 필요하다. [P16]

## C-8. Skills/MCP — 개발자가 실제로 적는 구성

아래는 **현행 API 기반 구성 조각, 미실행**이다. 공개된 이름을 유지하고 서버 주소·작업 경로는 실행 가이드에서 확정한다. MCP endpoint는 모델 프록시 포트와 별개다.

```python
from pydantic_ai import Agent
from pydantic_ai.capabilities import LocalWorkspace
from pydantic_ai_harness import Skills

agent = Agent('test', capabilities=[
    LocalWorkspace('.'),
    Skills('.agents/skills'),
])
```

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset

server = MCPToolset('http://127.0.0.1:11010/mcp')
agent = Agent('test', toolsets=[server])
```

Skills는 파일을 검증·등록하고 목록을 보여준 뒤 load_capability로 본문을 불러오는 기능이다. 실제 SOP 문서·지원 파일·검수는 앱이 준비한다. MCP client 추상화가 있어도 실제 서버와 인증·수명·업무 API 구현이 필요하다. ‘Skill=실행 함수’, ‘MCP=저장소’, ‘MCP가 있어야 모든 Tool 실행 가능’으로 표현하지 않는다. [P18][P19]

## C-9. Orchestration을 제어권·반환·상태로 설명하기

| 패턴 | 다음 행동 주체·반환 | 개발자가 지정할 것 |
|---|---|---|
| Agent-as-a-tool / delegation | 부모가 호출하고 자식 결과를 받아 계속함 | 전달 context·deps·usage·자식 도구·결과 형식 |
| Programmatic handoff | 앱 코드가 결과/조건을 보고 다음 Agent 호출 | 라우팅 조건·history 전달·종료 책임 |
| 명시적 Graph | 노드와 전이 조건이 다음 단계를 정함 | 공유 state·branch·오류·종료 |
| Harness Subagents | 제공된 위임 기능으로 자식 Run 구성 | 역할/권한/예산/공유 자원·합류 |
| Advisor | 실행 Agent가 다른 모델의 조언을 받음 | 조언 입력·채택 기준·추가 비용 |

‘위임=handoff’로 합치지 않는다. 부모가 멈춰 자식 결과를 받는 것과 대화의 담당자가 바뀌는 것은 다르다. Graph도 모든 분기가 모델 자율 선택인 것은 아니다. 별도 Context가 생겨도 같은 파일·DB 계정은 공유될 수 있다. [P20][P21][P22]

## C-10. 승인 UI·재개·위임 방지의 의미

`requires_approval=True`/ApprovalRequired는 호출을 보류하는 SDK 경로다. SDK가 업무용 승인 화면을 만들어 주는 것은 아니다. 기본 stop-the-world 흐름에서는 DeferredToolRequests를 허용 output에 포함하고, 호스트가 Call ID별 승인/거절을 모아 DeferredToolResults와 원래 이력으로 재개한다. inline resolver를 쓰면 한 Run 안에서 해결할 수도 있다. [P23]

승인자는 인증된 담당자여야 한다. 승인 화면은 **검증 후 실제 실행할 인자·대상 보고서/데이터 버전**을 보여줘야 한다. 인자나 초안이 바뀌면 이전 승인이 같은 행동을 승인한 것이 아니다. 클라이언트가 임의 history/approved 값을 보내 승인했다고 주장하지 못하게 서버가 pending 상태를 소유한다. Tool에서도 현재 권한을 다시 확인한다. 자식에게 위임해 승인 Gate를 우회하지 못하도록 같은 서버 정책을 적용한다. [설계 예시]

UI가 없으면 자동 창이 뜨지 않는다. CLI·정책 handler·반환 후 대기 중 무엇을 지원할지 명시해야 한다. 저장/재시작 복구는 별도 persistence/durable 실행 설계이며 `True` 플래그 하나로 보장되지 않는다.

---

# Q&A

3명 전체 발표 후 Q&A 대비

청중 순회에 넣지 않는 발표자용 자료다. 다음 답변의 조건과 근거는 C/F를 참조한다.

1. **Hermes가 알아서 학습한다는 말은?** Memory/Skill 같은 재사용 정보 갱신이다. 모델 가중치 학습과 다르며 틀린 절차도 재사용될 수 있다. S10/S12.
2. **파일을 고치면 즉시 현재 기억도 바뀌나?** 저장 파일과 세션 snapshot은 별개다. 새 Tool 결과나 명시 갱신 경로와 구별한다. S07/S10/S19.
3. **FTS5가 있으니 RAG는 불필요한가?** 대화 검색과 도메인 지식 검색은 대상·질의가 다르다. 정확 코드/표현 변화 질의의 근거 누락을 평가한다. S11.
4. **Subagent가 격리된 보안 환경인가?** Context/역할 분리와 OS/DB/네트워크 격리는 다르다. 실제 자원 접근을 봐야 한다. S14/S18.
5. **PydanticAI를 설치해 Demo로 써도 되나?** 실제 패키지 사용이 이 Demo의 목표다. 별도 가상환경과 고정 버전으로 설치하고 라이선스·모델·네트워크 조건은 제작 단계에서 점검한다. 설치했다고 실행 검증 완료는 아니다.
6. **고정 output_type이면 범용 Agent가 불가능한가?** 한 Run의 성공 최종 계약을 정한 것이다. 여러 타입/텍스트 또는 역할 분리가 가능하며 Tool return type과 목적이 다르다. C-5.
7. **타입이 맞으면 분석도 맞나?** 아니다. 분모·기간·계산·근거·인과/예측을 별도로 검증한다. S27/S44.
8. **Agent 객체를 계속 쓰면 자동으로 대화가 이어지나?** 설정 재사용과 대화 복원은 별개다. history/conversation 또는 명시 persistence 연동을 쓴다. S31.
9. **Memory/압축은 전부 직접 개발하나?** Core/별도 Harness에 기능이 있으나 저장·권한·보존 정책을 구성해야 한다. S32/S33.
10. **PydanticAI가 LangGraph를 쓰나?** 내부 실행은 pydantic-graph다. graph라는 표현이 같은 라이브러리를 뜻하지 않는다. S21/S23.
11. **graceful이면 최종 답변 뒤 실행은 없나?** 아니다. Function Tool이 실행될 수 있으므로 승인과 업무 단계 분리가 필요하다. S28/C-5.
12. **Hook과 Capability는 왜 나누나?** Hook은 시점, Capability는 재사용할 동작 묶음이다. wrapper 순서·상태 수명도 설계해야 한다. S30.
13. **승인 UI가 없으면 영원히 멈추나?** 호스트가 해결 경로를 제공해야 한다. inline 처리 또는 보류 결과 반환/저장 후 재개가 가능하다. S36.
14. **OpenAI 테스트 후 vLLM으로 옮기면 완전히 같나?** HTTP 계약을 유지하는 목표다. Tool parser·출력·stream·한도·모델 판단과 성능은 따로 확인한다. E-6.
15. **두 프레임워크가 10000/10001을 나눠 쓰나?** 아니다. Codex 지시의 두 Demo는 10000, Antigravity 지시의 두 Demo는 10001이다. E-6.
16. **실제로 vLLM으로 시연한 것인가?** 이번 단계는 설계다. 현재 PC 구현은 로컬 호환 프록시→OpenAI, 대상 PC는 같은 계약→vLLM을 계획한다. 실행 기록의 환경을 밝혀야 한다.
17. **네 SDK의 비교 기준은 무엇인가?** 동일한 LOT-A 요청으로 실행 주체, 상태 반영, 다음 단계 선택, 실패 후 재개를 비교한다. SDKMAP과 각 장의 Sources를 참고한다.
18. **GPU/Worker는 몇 개가 필요한가?** 모델·동시 실행·Tool I/O·Context·승인 대기·하드웨어 실측 없이는 정할 수 없다. 책임 배치를 먼저 고른다. S43.

---

# 근거와 정정

조사·참고자료와 적용 범위

## F-1. 내용 원본과 조사 범위

- **[FLOW]** [0_2차_세미나_발표_흐름.md](docs/flow.md): 전체 발표 순서·질문·추가 검증 요청·Demo 요구. 이번 데모 계약을 먼저 개정했다.
- **[DESIGN]** [1차 blueprint](../../archive/presentations/seminar-1/blueprint.md): A~G 구조·정보 위계·색·도식·노트 분리·탐색의 기준.
- [Hermes 추가 코멘트](../../study/hermes/Hermes_Agent_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md)와 [PydanticAI 추가 코멘트](../../study/PydanticAI/PydanticAI_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md)는 원문의 보강 의도와 관련된 snapshot/검색/병렬/최종화/승인 설계 해석을 확인했다. 이를 공식 제품 보장이나 실측 결과로 취급하지 않는다.
- 2026-11-03 공식 웹문서와 아래 고정 소스를 열람했다. 특히 `_GracefulProcessor`와 memory Tool의 patch 동작은 고정 raw source도 대조했다. 패키지를 설치해 API를 호출하거나 모든 교재 코드를 실행한 것은 아니다.
- 이번 API 코드 조각은 공식 이름을 유지하고 앱 함수/placeholder를 명시했다. Python 문법 정적 검사는 실행 검증과 구분한다. 기존 교재 전체에 대한 코드 감사가 완료됐다고 주장하지 않는다.

## F-2. 직접 확인한 공식 근거

현행 웹문서는 계속 바뀔 수 있다. 코드 링크의 버전은 링크에 고정되어 있다. 아래 ID는 본문 노트에서 사용한다.

| ID | 공식 자료 | 적용 |
|---|---|---|
| H01 | [Hermes Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | S04 전체 지도 |
| H02 | [Agent Loop Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop) | S05/S06 실행·분기 |
| H03 | [Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) | S07 계층·고정/일시 정보 |
| H04 | [Context Compression and Caching](https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching) | S08/S09 임계값·캐싱 |
| H05 | [Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | S10 용량·snapshot·승인 |
| H06 | [memory_tool.py v0.22.5](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/memory_tool.py) | add/patch/remove |
| H07 | [Session Storage](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage) | state.db/FTS/Profile |
| H08 | [Sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions) | refresh-prompts |
| H09 | [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | 단계 로딩·관리 |
| H10 | [Curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator) | Agent 생성 Skill 유지관리 |
| H11 | [Tools Runtime](https://hermes-agent.nousresearch.com/docs/developer-guide/tools-runtime) | registry/schema/dispatch |
| H12 | [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) | 확장·Hook·명령 |
| H13 | [tool_dispatch_helpers.py v0.22.5](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/tool_dispatch_helpers.py) | segment/barrier |
| H14 | [delegate_tool.py v0.22.5](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/delegate_tool.py) | Child 실행 경계 |
| H15 | [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) | 다층 승인·격리·checkpoint 조건 |
| H16 | [Scheduled Tasks](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | Cron 실행 입구·모드 |
| C01 | [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | Gather/Act/Verify |
| C02 | [Memory](https://code.claude.com/docs/en/memory) | CLAUDE.md·Auto Memory |
| C03 | [Subagents](https://code.claude.com/docs/en/sub-agents) | 독립 Context·도구 설정 |
| C04 | [Agent Teams](https://code.claude.com/docs/en/agent-teams) | 협업·실험적 제약 |
| C05 | [Interactive mode](https://code.claude.com/docs/en/interactive-mode) | 명령 인터페이스 |
| P01 | [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/) | 실행 API·내부 Graph |
| P02 | [PydanticAI Harness](https://pydantic.dev/docs/ai/harness/) | 별도 패키지 경계 |
| P03 | [_agent_graph.py v2.61.0](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_agent_graph.py) | 노드·EndStrategy·예외 |
| P04 | [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/) | deps/RunContext |
| P05 | [Function Tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/) | decorator·schema |
| P06 | [Messages and chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/) | history/conversation·usage |
| P07 | [OpenAI models](https://pydantic.dev/docs/ai/models/openai/) | 명시 Chat Model·Provider |
| P08 | [tool_manager.py v2.61.0](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/tool_manager.py) | validation/execute 분리 |
| P09 | [Toolsets](https://pydantic.dev/docs/ai/tools-toolsets/toolsets/) | Function/Filtered/Combined |
| P10 | [_tool_execution.py v2.61.0](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_tool_execution.py) | 세 정책·barrier·retry-wins |
| P11 | [Output](https://pydantic.dev/docs/ai/core-concepts/output/) | Tool/Native/Prompted/Text |
| P12 | [Retries](https://pydantic.dev/docs/ai/core-concepts/retries/) | 검증/Provider/예산 층 |
| P13 | [Hooks](https://pydantic.dev/docs/ai/core-concepts/hooks/) | 실제 Hook API·wrap |
| P14 | [Building custom capabilities](https://pydantic.dev/docs/ai/capabilities/custom/) | 합성·순서·Run 수명 |
| P15 | [Capabilities overview](https://pydantic.dev/docs/ai/capabilities/overview/) | persistence/확장 제공 범위 |
| P16 | [Compaction strategies](https://pydantic.dev/docs/ai/harness/compaction/) | 이력 변경·전략 |
| P17 | [Memory](https://pydantic.dev/docs/ai/harness/memory/) | store·namespace·주입/검색 |
| P18 | [Skills](https://pydantic.dev/docs/ai/harness/skills/) | load_capability·코드 구성 |
| P19 | [MCP Client](https://pydantic.dev/docs/ai/mcp/client/) | 실제 MCPToolset |
| P20 | [Multi-agent applications](https://pydantic.dev/docs/ai/guides/multi-agent-applications/) | 위임·코드 라우팅 |
| P21 | [Harness Subagents](https://pydantic.dev/docs/ai/harness/subagents/) | 선택 위임 기능 |
| P22 | [Advisor](https://pydantic.dev/docs/ai/harness/advisor/) | 조언 요청 경계 |
| P24 | [Capabilities overview](https://pydantic.dev/docs/ai/capabilities/overview/) | 관찰·평가 연동 경계 |
| P23 | [Deferred Tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/) | 승인·inline/후속 재개 |
| V01 | [vLLM APC](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) | prefix caching 원리·조건 |
| V02 | [vLLM Online Serving](https://docs.vllm.ai/en/latest/serving/online_serving/) | HTTP 공통 계약과 모델별 지원 |

## F-3. 원문에서 보완·정정한 사항만

| 원문의 질문/표현 | 이번 처리 | 영향·근거 |
|---|---|---|
| graceful: 최종 출력 이전 Function 처리 후 종료 | 후행 Function도 실행될 수 있음. 이후 Output Tool 생략과 구별 | S28/C-5, 고정 executor의 flush_pending과 _run_output 대조 [P10] |
| ToolOutput은 그냥 받은 것을 tool call로 해석? | 출력용 schema를 Tool로 제시해 생성 유도 | S27 [P11] |
| Memory·compaction은 직접 전부 구현? | Core/별도 Harness 제공 기능과 업무 정책을 분리 | S31–S33 [P02][P16][P17] |
| 승인 UI 없으면 계속 멈춤? | 호스트 해결 경로, inline 또는 보류 반환/후속 Run | S36/C-10 [P23] |
| 모든 Tool은 곧 Toolset? | Function Toolset과 Provider-native 기능의 실행 경계 구별 | S25 [P05][P09] |
| Hermes Tool 일괄 ThreadPool 병렬 | planner/barrier/충돌 조건을 반영 | S14 [H13] |
| Skill 인덱스는 확실히 Volatile | 현행 Prompt Assembly의 세 계층 목록은 volatile로, 바로 아래 문장은 skills를 stable로 설명해 문서 내 충돌. 위치 단정 제외, snapshot/호출별 정보만 확정 설명 | S07 [H03]. 설치 소스의 실제 prompt로 판별 |
| 압축 50%/85%, 최근 20개는 항상 동일 | 기본 설명과 실효 설정/보정 조건을 구별 | S09 [H04] |
| Cron은 명령 실행이 아니라 무조건 Agent 기동 | Agent 세션 실행 모드 외 no-agent script 모드도 문서화됨. 발표는 Agent 작업 모드로 한정 | S15 [H16] |
| run_steam_evnets, 줄 번호/‘21.2’ | 실제 이름 run_stream_events, 고정 파일·심볼로 교체 | C-3/C-4 [P01][P08] |
| 일반 openai 문자열로 모델 연결 | Demo는 OpenAIChatModel을 명시해 공통 Chat Completions로 고정 | C-2 [P07] |
| 기존 MCP 코드 이름을 그대로 재사용 | 현행 문서·v2.61.0 mcp.py는 MCPToolset을 제공하므로 해당 이름으로 작성 | C-8 [P19]. 설치 버전과 API 세대 대조 |

## F-4. 추가 코멘트·보강 질문 반영표

| 원문 요구 묶음 | 반영 위치 | 상태 |
|---|---|---|
| 각 기술 큰 조직도 먼저, 부분 확대 | S04/S16/S20–S21, A-1 | 명세 완료 |
| Hermes 폴더·Profile·공식 Turn·실제 종료 | S04–S06/S11 | 문서 근거, 설치값 미검증 |
| 캐시/Prompt 3계층/SOUL·프로젝트 지시 | S07/S08/F-3 | 충돌 표시·설명 한정 |
| 기억 snapshot/FTS/Skill Curator | S10–S12/S19 | 문서·고정 소스 확인 |
| Tool/MCP/Plugin·특수 Tool·병렬/Child·Cron/승인 | S13–S15/C-4 | 구현 경계 반영 |
| Claude Memory/지시·Subagent 예시·격리·Teams·명령 | S16–S19 | 공식 공개 범위 |
| Pydantic·Core·Graph·Harness·이점 | S20–S23/S37 | 계층 구분 |
| 모든 코드 실제 문법·스트리밍 선택 | C-2/C-3/C-6/C-8 | 이번 예제 정적 확인, 실행 미검증 |
| instructions/system/deps·Provider 차이 | S24/C-2 | 자동 전송 오해 방지 |
| tool/tool_plain·Toolset·인자 검증·sync/async/병렬 | S25/S26/C-4 | 실제 API/고정 executor |
| 출력 방식·ModelRetry·Retry 종류·EndStrategy | S27–S29/C-5 | 중요 정정 포함 |
| Hook·Capability·여러 개 합성·도메인 활용 | S30/C-6 | 실제 Hook·순서·Run 수명 |
| 대화 자동 유지 여부·영속 저장·Memory/압축 직접 구현? | S31–S33/C-7 | 제공 경계 답변 |
| Skill/MCP 추상화·개발자 코드 | S34/C-8 | 코드 조각 포함 |
| agent-as-a-tool/handoff/Graph/Subagents/Advisor | S35/C-9 | 반환·제어·상태 구분 |
| Harness 핵심 내부 동작 | S32–S35/S37 | 주입/변환/도구 경로 중심 |
| 승인 UI/주체/위임 방지/재개 재검사 | S36/C-10 | 호스트 계약과 SDK 구별 |
| 설치 Demo 가능? 고정 output_type의 범용성? | D5/D6/C-5 | 명시 답변 |
| 실제 로그·별도 웹·이관 후 상세 지시서 | E-1–E-7 | 제작 요구 완성, 실행 전 |
| 중앙/로컬 운영·자원·업데이트 | S43/S44 | 설계 질문, 실측 전 |
| Codex 10000 / Antigravity 10001·OpenAI 감싸기 | 개정 FLOW/E-6/E-7 | 두 프레임워크 공통 계약 |

---