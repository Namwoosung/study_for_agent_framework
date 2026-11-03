# 2차 세미나 — 발표자 전용 노트

## S00 — Agent Framework 세부 구조

## Agent Framework 세부 구조

### 주요 개념

**Agent Framework**: 모델 호출, 도구 실행, 상태 관리 등 Agent를 구성하고 실행하는 기능을 제공하는 소프트웨어입니다.

### 설명

이번 세미나는 공통 개념을 배운 1차에 이어 실제 기술의 세부 구조를 살펴봅니다. 이 발표에서는 Hermes와 PydanticAI를 중심으로 실행 흐름과 상태 관리 방법을 설명하고 Claude Code와도 비교합니다.

### 발표 포인트

Hermes · Claude Code · PydanticAI

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

## S03 — Agent Harness와 SDK

## Agent Harness와 SDK

### 주요 개념

**Agent Harness**: CLI, 도구, 세션 등 갖춰진 Agent 실행환경에서 시작합니다. 여기서는 Hermes와 Claude Code를 묶었습니다.

**Agent SDK**: 개발자가 Agent, Tool, 실행 조건을 코드로 정의하고 애플리케이션에 연결하는 출발점입니다.

### 설명

Harness와 SDK는 배타적인 제품 분류가 아닙니다. Hermes의 프로그래밍 통합이나 PydanticAI의 선택적 Harness처럼 기능이 겹칠 수 있습니다. 이 장은 발표를 위한 두 출발점을 보여주며, Hermes와 PydanticAI를 각 행의 주요 설명 대상으로 강조합니다. 다른 SDK는 이름과 편집 위치만 표시하며 기능 비교가 완료됐다는 뜻은 아닙니다.

### 발표 포인트

Hermes와 PydanticAI를 중심으로 살펴봅니다.

## S03H — Hermes

## Hermes

### 주요 개념

**AIAgent**: 모델 요청과 Tool 실행을 이어가는 Hermes의 Agent Runtime입니다.

**Session / Memory / Skills**: 대화 기록, 지속 사실, 재사용 절차를 서로 다른 방식으로 보관하고 사용합니다.

### 설명

CLI나 Gateway 등에서 들어온 요청은 AIAgent로 이어집니다. Prompt를 구성해 모델을 호출하고, 필요한 Tool을 실행한 뒤 결과를 다시 모델에 전달합니다. 이 과정에서 세션, Memory, Skills를 사용합니다. 왼쪽은 대표 관계를 단순화한 전체 구조도이며 이후 장표에서 각 부분을 나누어 설명합니다.

### 발표 포인트

전체 구조를 먼저 보고, 각 기능의 동작을 살펴봅니다.

## S04 — Hermes는 범용 Agent Harness입니다

## Hermes는 범용 Agent Harness입니다

### 주요 개념

**범용 Agent Harness**: 특정 업무 하나에 고정하지 않고 여러 도구와 모델을 연결해 작업할 수 있는 실행환경입니다.

**기본 제공 기능**: Loop·입출력·Tool 확장·기억/검색·Skills·운영 기능이 포함되지만 실제 가용성은 설치 방식, 플랫폼, 인증, 활성 Toolset과 설정에 따라 다릅니다.

### 설명

Hermes는 Agent Loop와 Tool Calling, 취소·중단·대체 모델 경로를 제공합니다. CLI/TUI/Desktop, 메신저 Gateway, HTTP API, ACP 등으로 접근할 수 있습니다. 터미널·파일·웹·브라우저·코드 실행, Toolsets·MCP·Plugins로 기능을 연결합니다. SQLite 세션과 FTS5 검색, Memory 파일과 외부 Memory Plugin을 구분하며, Skills 작성/관리와 Curator, Subagent·Cron·Hooks·승인·격리·파일 복구 등의 운영 기능도 포함합니다. 모든 기능이 기본 활성화되거나 모든 환경에서 동일하게 동작한다는 의미는 아닙니다.

### 발표 포인트

실제 사용 가능한 기능은 설치 환경과 설정에 따라 달라집니다.

## S05 — 사용자 입력에서 모델 요청까지

## 사용자 입력에서 모델 요청까지

### 주요 개념

**Turn**: 사용자 입력 한 건을 처리하는 단위이며, 여러 모델 호출과 Tool 실행을 포함할 수 있습니다.

**Provider Adapter**: 내부 메시지와 도구 정의를 선택한 모델 API 형식으로 변환합니다.

### 설명

Task와 사용자 메시지를 준비한 뒤 Prompt와 History, Tool schema를 모읍니다. 압축 필요 여부와 호출 시점 정보를 반영하고 Provider 형식으로 바꾸어 요청합니다. 지원 Provider에만 cache marker를 적용합니다. 프레임워크 내부 객체와 실제 전송 JSON은 구분해서 관찰합니다.

### 발표 포인트

최종 요청에는 지침, 대화 이력, 도구 정의가 함께 담깁니다.

## S06 — Tool을 실행할 때와 답변을 마칠 때

## Tool을 실행할 때와 답변을 마칠 때

### 주요 개념

**Agent Loop**: 모델 응답을 해석하고 도구 결과를 추가하며 다음 호출 또는 종료를 결정합니다.

**Tool 오류 / API 오류**: 실행 오류를 모델에게 알려주는 경로와 모델 API 통신을 복구하는 경로는 다릅니다.

### 설명

Tool Call이 있으면 Runtime이 실행하고 결과를 대화에 추가해 모델을 다시 호출합니다. 최종 텍스트라면 응답과 세션을 정리합니다. 사용자 중단, 예산 소진, Context 문제, API 오류는 각각 별도 경로로 처리합니다. 모델이 답변을 마쳤다는 사실만으로 업무 목표의 달성을 보장하지는 않습니다.

### 발표 포인트

Tool 오류와 모델 API 오류는 복구 방법이 다릅니다.

## S07 — 고정된 Prompt와 매번 달라지는 정보

## 고정된 Prompt와 매번 달라지는 정보

### 주요 개념

**Stable / Context / Volatile**: 정체성·기본 행동, 프로젝트·호출자 지침, Memory·런타임 snapshot을 나눈 논리적 계층입니다.

**Frozen Snapshot**: 세션 동안 재사용하는 system prompt의 기준 내용입니다.

### 설명

SOUL은 정체성과 기본 행동을, AGENTS 계열 파일은 프로젝트 규칙을 안내합니다. 세션이 재사용하는 Prompt에 대화 이력과 이번 호출의 정보를 더합니다. Volatile이라는 이름이 매번 재작성을 뜻하지는 않습니다. 현행 문서의 Skill 계층 설명에는 불일치가 있어 여기서는 위치를 단정하지 않습니다.

### 발표 포인트

Volatile 계층도 세션 안에서는 같은 snapshot을 사용할 수 있습니다.

## S08 — 같은 Prefix의 계산을 재사용하기

## 같은 Prefix의 계산을 재사용하기

### 주요 개념

**Prefix Cache**: 반복되는 입력 앞부분의 계산을 추론 서비스가 재사용하는 방식입니다.

**입력 길이와 계산량**: 입력을 다시 전송해도 일부 계산이 재사용될 수 있으며 Context 길이 자체가 줄어드는 것은 아닙니다.

### 설명

예시의 8,000/2,000 tokens는 원리 설명용 수치입니다. Hermes는 입력 내용과 순서를 구성하고, 실제 캐시 적중은 Provider나 서빙 엔진이 판단합니다. Prefix 일치, 캐시 퇴거, 부하, 모델과 API 지원 조건이 영향을 줍니다. 로컬 OpenAI 프록시 실행을 vLLM 캐시 실측으로 해석하지 않습니다.

### 발표 포인트

입력은 다시 보내지만, 일부 계산은 재사용할 수 있습니다.

## S09 — 긴 대화에서 남길 것과 줄일 것

## 긴 대화에서 남길 것과 줄일 것

### 주요 개념

**Context Compression**: 긴 이력을 줄여 다음 요청에 필요한 공간을 확보합니다.

**Tool Call / Result 쌍**: 호출 ID에 맞는 결과와 순서를 보존해야 모델 API가 대화를 올바르게 해석할 수 있습니다.

### 설명

오래된 내용을 축약하면서 최근 문맥과 미해결 작업, 호출·결과 관계를 보존합니다. Tool Loop 안의 압축과 Gateway의 세션 위생 처리는 다릅니다. 문서의 50%/85% 및 최근 20개는 조건과 설정에 따른 기본 설명입니다. 수치·단위·원본 근거는 별도 artifact로 남기는 업무 설계를 검토할 수 있습니다.

### 발표 포인트

압축 후에도 호출과 결과가 서로 대응해야 합니다.

## S10 — 저장한 Memory는 언제 반영될까?

## 저장한 Memory는 언제 반영될까?

### 주요 개념

**Built-in Memory**: MEMORY.md와 USER.md에 다음 세션에서도 필요한 짧은 사실을 남깁니다.

**파일 저장과 Prompt 반영**: Memory Tool로 파일을 바꾸는 것과 이미 고정된 system snapshot을 바꾸는 것은 다른 동작입니다.

### 설명

세션 A가 시작할 때 파일을 읽어 snapshot을 만듭니다. A 도중 memory Tool이 파일을 갱신해도 기존 system snapshot은 자동 교체되지 않으며, 새 Tool 결과로 내용을 아는 것과도 구분합니다. 다음 세션은 갱신된 파일을 읽습니다. add/patch/remove, 용량 초과 처리와 write_approval 조건을 확인해야 합니다. SOP와 분석 근거는 별도로 버전을 고정하는 설계가 필요합니다.

### 발표 포인트

현재 세션의 system snapshot은 파일 저장만으로 바뀌지 않습니다.

## S11 — 기억할 사실과 다시 찾을 대화

## 기억할 사실과 다시 찾을 대화

### 주요 개념

**Session History**: SQLite state.db에 보관한 대화와 Tool 실행 기록입니다.

**FTS5 session_search**: 과거 대화를 문자열 중심으로 검색하고 선택한 결과를 Context에 넣습니다.

**External Provider**: 별도 저장소나 Plugin으로 추가하는 기억·검색 기능이며 기본 파일 Memory와 구분합니다.

### 설명

소수의 지속 사실, 과거 대화의 상세 기록, 외부 확장은 용도와 수명이 다릅니다. 정확한 장비 ID 질의와 표현이 달라진 질의를 나누어 검색 품질을 평가하고 대상과 기간도 확인합니다. Profile은 config/DB/memory 운영 분리이며 독립 보안 테넌트 보장은 아닙니다. 실제 경로는 HERMES_HOME과 환경에 따라 달라집니다.

### 발표 포인트

과거 대화는 필요한 기록을 검색해 현재 Context에 넣습니다.

## S12 — Skill을 읽고 다시 사용하는 과정

## Skill을 읽고 다시 사용하는 과정

### 주요 개념

**Skill**: 언제 어떤 도구를 어떤 순서로 사용할지 적은 문서형 절차입니다.

**Progressive Disclosure**: 목록, 선택한 SKILL.md 본문, 필요한 참고 파일 순으로 내용을 불러옵니다.

**Curator**: Agent 생성 Skill의 사용 이력을 보고 active/stale/archived 상태로 관리합니다.

### 설명

실제 실행은 Tool이 하고 Skill은 절차와 자료를 제공합니다. skill_manage로 생성·수정·삭제할 수 있지만, 이것은 기반 모델 가중치의 학습과 다릅니다. 잘못된 절차도 재사용될 수 있으므로 검토와 버전 관리가 필요합니다. Curator가 사용되지 않는 모든 사용자 Skill을 무조건 삭제하는 것은 아닙니다.

### 발표 포인트

저장한 절차를 다시 쓰기 전에 근거와 버전을 확인합니다.

## S13 — Tool 등록과 MCP·Plugin 연결

## Tool 등록과 MCP·Plugin 연결

### 주요 개념

**Tool Registry**: 이름, 모델용 schema, 실행 handler, 가용성 조건을 연결합니다.

**MCP**: 외부 서버가 제공하는 도구를 Client로 발견하고 호출하는 연결 방식입니다.

**Plugin / Hook**: Hermes 실행환경에 Tool·명령·실행 전후 처리를 추가하는 확장 접점입니다.

### 설명

등록된 모든 도구가 모델에 노출되는 것은 아닙니다. Toolset과 환경, check_fn 등을 통과한 schema를 제공합니다. memory/delegate_task 등 Agent 상태를 사용하는 도구는 일반 Registry dispatch 전에 별도 처리될 수 있습니다. 중앙 Hook 하나로 모든 내부 실행을 관찰했다고 판단하지 않습니다.

### 발표 포인트

도구에 따라 실행 경로와 관찰 가능한 지점이 달라집니다.

## S14 — Tool 병렬 실행과 Subagent 위임

## Tool 병렬 실행과 Subagent 위임

### 주요 개념

**병렬 Tool**: 한 모델 응답의 여러 호출을 같은 Agent Loop에서 실행합니다.

**Subagent**: 별도 AIAgent가 독립 Goal·Context·Loop로 작업하고 결과를 부모에게 돌려줍니다.

### 설명

thread는 실행 수단이며 Agent의 개수가 아닙니다. Hermes는 상호작용이나 파일 충돌 조건에 따라 barrier로 실행 구간을 나눌 수 있습니다. 같은 snapshot의 독립 조회를 합치는 것과 별도 Agent에게 분석을 위임하는 것은 비용과 상태 관리가 다릅니다. Context 분리가 OS·DB·파일 권한의 격리를 자동으로 만들지는 않습니다.

### 발표 포인트

Subagent의 결과를 받은 부모가 다음 작업을 이어갑니다.

## S15 — 실행 권한과 Hermes Demo

## 실행 권한과 Hermes Demo

### 주요 개념

**승인과 실행 권한**: 명령·파일 검사, 사용자 승인, OS·DB·Sandbox 권한은 서로 다른 통제입니다.

**Checkpoint**: 지원 범위 안에서 파일 복구를 돕는 opt-in 기능이며 외부 변경 전체의 rollback은 아닙니다.

### 설명

smart/manual/off 승인 모드와 무인 실행 deny 정책을 함께 확인합니다. 위험 패턴 탐지뿐 아니라 실제 실행 계정과 데이터 접근 권한도 제한해야 합니다. Cron의 Agent 작업 모드는 새 실행을 시작하는 입구입니다. Demo에서는 Context, Tool, 저장 상태를 관찰할 계획이며 현재 연결 페이지는 실제 서비스가 없는 안내 화면입니다.

### 발표 포인트

Demo에서는 모델 요청, Tool 결과, 저장된 상태를 살펴봅니다.

## S16 — Claude Code의 실행 구조

## Claude Code의 실행 구조

### 주요 개념

**Claude Code Harness**: 모델, 도구, Context, 권한과 위임 설정을 연결한 실행환경입니다.

**Gather / Act / Verify**: 정보 수집, 행동, 결과 확인이 반복되는 공개 동작 설명입니다.

### 설명

사용자 요청과 프로젝트 파일을 바탕으로 Context를 수집하고 도구를 실행하며 결과를 확인합니다. 이 장은 공개 인터페이스와 동작을 설명합니다. 비공개 엔진의 함수나 내부 구조를 확인한 것처럼 세부 구현을 추정하지 않습니다.

### 발표 포인트

도구와 지침, 권한 설정이 하나의 실행환경에 연결됩니다.

## S17 — 프로젝트 지침과 Auto Memory

## 프로젝트 지침과 Auto Memory

### 주요 개념

**프로젝트 지침**: 사람이 작업 규칙과 제약을 적은 파일입니다.

**Auto Memory**: Claude Code가 관리하는 기억으로 인덱스와 필요한 세부 파일을 로드합니다.

### 설명

Hermes는 SOUL·프로젝트 지침과 MEMORY/USER 파일을 구분하고 세션 snapshot을 사용합니다. Claude Code는 CLAUDE.md와 Auto Memory의 읽기 정책이 다릅니다. AGENTS.md를 같은 방식으로 자동 로딩한다고 합치지 않으며 필요 시 import 관계를 확인합니다. 두 제품 모두 지침이 실제 권한 통제를 대신하지는 않습니다.

### 발표 포인트

접근 권한은 지침 파일과 별도로 관리합니다.

## S18 — Subagent와 Agent Teams

## Subagent와 Agent Teams

### 주요 개념

**Subagent**: 부모의 하위 과제를 수행한 뒤 결과를 부모에게 반환합니다.

**Agent Teams**: 독립 세션의 팀원들이 공유 작업과 직접 메시지로 협업하는 방식입니다.

### 설명

위임과 협업은 결과 전달 경로와 제어 주체가 다릅니다. Teams의 지원 조건과 실험적 제약을 확인해야 하며, Context가 분리되어도 파일 충돌과 공통 자원 권한, 조정 비용은 남습니다.

### 발표 포인트

독립 Context를 써도 공유 파일과 자원의 충돌은 확인해야 합니다.

## S19 — 명령으로 세션과 기억 관리하기

## 명령으로 세션과 기억 관리하기

### 주요 개념

**Prompt refresh**: Hermes의 저장된 Prompt를 명시적으로 갱신하는 관리 경로입니다.

**Pending Memory**: 보류된 기억 쓰기를 검토하는 기능입니다.

**Resume / Compact**: Claude Code에서 대화를 다시 열거나 Context를 축약하는 서로 다른 동작입니다.

### 설명

명령 이름보다 어떤 상태를 바꾸는지에 주목합니다. hermes sessions refresh-prompts --session, /memory pending, Claude Code의 /resume·/compact는 목적과 적용 시점이 다릅니다. 화면의 명령은 설명용이며 이 발표에서 실제 실행한 기록은 아닙니다.

### 발표 포인트

명령마다 바꾸는 상태와 적용 시점이 다릅니다.

## S20 — Pydantic에서 PydanticAI로

## Pydantic에서 PydanticAI로

### 주요 개념

**Pydantic**: Python 값과 schema를 검증하는 기반 라이브러리입니다.

**PydanticAI Core**: Agent·Tool·Output과 내부 실행 Graph를 제공합니다.

**선택적 Harness**: Memory·Skills 등 필요한 실행 기능을 추가하는 별도 구성입니다.

### 설명

Core만으로도 Agent를 만들 수 있습니다. pydantic-graph, Evals/Logfire, Provider/Model과 연결되는 범위를 구분하며 모든 기능을 한 패키지가 자동으로 구성한다고 보지 않습니다. Harness는 설치·버전을 별도로 확인합니다.

### 발표 포인트

Core로 시작하고, 필요한 Harness 기능을 추가할 수 있습니다.

## S21 — PydanticAI 전체 구조

## PydanticAI 전체 구조

### 주요 개념

**내부 Graph**: UserPromptNode, ModelRequestNode, CallToolsNode가 입력과 응답을 처리합니다.

**Capabilities**: Run·Model·Tool·Output 실행 지점에 개입하는 기능을 구성합니다.

### 설명

개발자는 지침, 도구, output_type과 의존성을 정의합니다. SDK는 pydantic-graph로 모델 요청과 Tool/출력 분기를 처리합니다. 데이터 저장, 업무 권한, 실제 Tool 서비스는 앱에 연결하며 LangGraph를 사용한다는 뜻은 아닙니다.

### 발표 포인트

모델·Tool·저장소를 애플리케이션에 맞게 연결합니다.

## S22 — Agent와 Tool을 코드로 정의하기

## Agent와 Tool을 코드로 정의하기

### 주요 개념

**Agent 정의**: 모델, 지침, Deps와 출력 계약을 설정합니다.

**RunContext**: Tool이 실행될 때 앱이 주입한 자원과 상태에 접근하는 문맥입니다.

### 설명

예시의 get_bin_summary는 앱에서 구현하는 Tool이고 DemoDeps/query 역시 사용자 코드입니다. SDK Loop를 다시 구현할 필요는 없지만 실제 데이터 조회와 인가를 Tool 또는 서비스에서 검사해야 합니다. 이 코드는 연결 구조를 보여주는 축약 예시입니다.

### 발표 포인트

업무 데이터 조회와 권한 확인은 애플리케이션에서 구현합니다.

## S23 — 세 노드로 보는 Agent 실행

## 세 노드로 보는 Agent 실행

### 주요 개념

**UserPromptNode**: 입력과 이전 이력을 준비합니다.

**ModelRequestNode**: 모델 요청을 구성하고 호출합니다.

**CallToolsNode**: Function Tool과 최종 Output을 분류하고 검증·실행합니다.

### 설명

Function Tool의 결과는 다음 모델 요청으로 돌아갑니다. 최종 출력이 유효하면 End로 종료하고, 검증이 실패하면 모델 수정 피드백으로 이어집니다. history, usage, retry 등 실행 상태를 함께 추적합니다.

### 발표 포인트

Tool 결과와 수정 피드백은 다음 모델 요청으로 이어집니다.

## S24 — 모델 입력과 Python 실행 자원

## 모델 입력과 Python 실행 자원

### 주요 개념

**모델 입력**: Instructions/System Prompt, History, Tool schema와 반환 결과 등 실제로 전송하는 정보입니다.

**Deps**: DB client나 인증 문맥처럼 Python에서 사용하는 앱 자원입니다.

### 설명

Deps 전체가 자동으로 모델에 전송되는 것은 아닙니다. 하지만 지침 생성이나 Tool 반환에 선택한 정보가 포함되면 모델 입력으로 전달됩니다. 객체 주입의 안전성과 Tool 결과의 정보 노출은 따로 확인해야 합니다.

### 발표 포인트

Deps에서 사용한 정보도 Tool 결과로 반환하면 모델에 전달됩니다.

## S25 — 함수 정의에서 Tool 실행까지

## 함수 정의에서 Tool 실행까지

### 주요 개념

**Schema**: 모델이 생성할 Tool 이름과 인자의 형식을 설명합니다.

**tool / tool_plain**: RunContext를 사용하는 Tool과 일반 인자만 받는 Tool의 등록 방식입니다.

### 설명

함수와 타입으로 schema를 만들고 모델에 노출한 뒤 응답 인자를 검증해 실행합니다. 허용 범위와 사용자 인가는 서버 측에서 확인해야 합니다. 노출 필터가 곧 실행 권한 검사가 되는 것은 아닙니다.

### 발표 포인트

모델에 도구를 보여주는 것과 실행을 허가하는 것은 별개입니다.

## S26 — 함께 실행할 작업과 기다릴 작업

## 함께 실행할 작업과 기다릴 작업

### 주요 개념

**동시 실행**: 독립적인 Tool을 함께 스케줄링해 대기를 겹칩니다.

**sequential barrier**: 앞 구간이 완료된 후 해당 Tool을 단독 실행하고 다음 구간을 시작합니다.

### 설명

async Tool은 task, sync Tool은 worker thread로 실행될 수 있습니다. sequential=True는 실행 순서의 장벽이며 데이터 snapshot이나 트랜잭션을 자동으로 만들지 않습니다. 같은 Lot·시간대·기준 시점을 사용했는지는 앱이 확인합니다.

### 발표 포인트

여러 조회 결과를 합칠 때는 대상과 기준 시점도 맞춰야 합니다.

## S27 — 출력 형식과 업무 정확성 검증

## 출력 형식과 업무 정확성 검증

### 주요 개념

**ToolOutput / NativeOutput / PromptedOutput**: 출력용 Tool, Provider의 구조화 출력, 형식 지시와 파싱을 사용하는 서로 다른 출력 방식입니다.

**output_type**: 최종 결과의 계약이며 개별 Tool 반환 타입과 목적이 다릅니다.

### 설명

Pydantic으로 타입과 필드를 검증한 뒤 업무 Validator와 실제 데이터 검증을 연결합니다. 단위, 계산, 분모, 기간, 출처가 맞는지는 schema 통과만으로 알 수 없습니다. 모델과 Provider에 따라 지원 가능한 방식도 다릅니다.

### 발표 포인트

형식이 맞는 답변도 내용은 틀릴 수 있습니다.

## S28 — EndStrategy에 따른 Tool 실행

## EndStrategy에 따른 Tool 실행

### 주요 개념

**EndStrategy**: 최종 출력이 제안된 응답에서 Function Tool을 어디까지 실행할지 정하는 정책입니다.

**Emission 순서**: 모델이 제안한 순서이며 실제 완료 시간 순서와 다릅니다.

### 설명

같은 A/O1/B/O2 응답을 정책별로 비교하는 예시입니다. 최종 결과 선택과 Tool 실행 여부를 분리해서 봅니다. graceful에서도 최종 출력 뒤 Function Tool이 실행될 수 있으므로 부작용이 있는 도구는 승인과 업무 단계 분리가 필요합니다. 정확한 정책별 동작은 표와 고정 응답 시험 기준을 따릅니다.

### 발표 포인트

graceful에서는 최종 출력 뒤의 Function Tool도 실행될 수 있습니다.

## S29 — 무엇을 다시 시도할까?

## 무엇을 다시 시도할까?

### 주요 개념

**ModelRetry**: 잘못된 인자나 출력에 대해 모델이 수정하도록 피드백하는 경로입니다.

**통신 retry**: 429·5xx·연결 장애를 timeout과 backoff 정책으로 복구합니다.

### 설명

유효한 형식의 잘못된 업무 판단은 통신 retry로 해결되지 않습니다. SDK와 HTTP·프록시 재시도가 중첩되면 실제 요청과 비용이 늘어날 수 있습니다. UsageLimits, 시간 제한, Tool 중복 부작용 방지를 별도로 관리합니다.

### 발표 포인트

재시도가 여러 계층에 있으면 실제 요청 횟수가 늘어날 수 있습니다.

## S30 — Hook과 Capability 구성

## Hook과 Capability 구성

### 주요 개념

**Hook**: Run·모델 요청·Tool 등 특정 실행 시점에 개입합니다.

**Capability**: 지시·도구·Hook·설정을 기능 단위로 묶어 재사용합니다.

### 설명

wrapper는 A.enter→B.enter→core→B.exit→A.exit 순서처럼 중첩됩니다. 바깥 wrapper가 handler를 호출하지 않으면 안쪽 검사도 실행되지 않을 수 있습니다. 실행 순서와 Run별 상태 수명을 확인해야 합니다.

### 발표 포인트

wrapper 순서에 따라 안쪽 Hook의 실행 여부가 달라집니다.

## S31 — 이전 대화를 다음 Run으로 이어가기

## 이전 대화를 다음 Run으로 이어가기

### 주요 개념

**message_history**: 이전 Run의 typed messages를 다음 실행에 전달하는 경로입니다.

**Conversation**: 현행 API에서 이력·사용량·ID 등을 이어가는 기능이며 저장소 자체와 구분합니다.

### 설명

Agent 객체를 계속 사용하는 것만으로 사용자 대화가 자동 복원되지는 않습니다. 앱이 인증된 사용자에 맞는 이력을 저장하고 불러와야 합니다. usage를 초기화하면 대화 전체의 누적 예산과 달라질 수 있어 동시 갱신·TTL·누적 한도도 함께 고려합니다.

### 발표 포인트

대화 저장, 사용자 구분, 누적 사용량을 함께 관리합니다.

## S32 — Context 압축과 원본 보관

## Context 압축과 원본 보관

### 주요 개념

**Provider-native compaction**: 지원하는 모델 API에서 제공하는 압축 경로입니다.

**Harness 압축**: clear·sliding window·summarize 등 별도로 선택하는 이력 축약 전략입니다.

### 설명

Core와 Harness의 제공 범위를 구분하고 원본 저장 정책을 따로 정합니다. 축약이 Run History에 유지될 수 있으며 원본 복원이 자동 보장되는 것은 아닙니다. vLLM 이관 기본 경로는 Provider 전용 compaction을 필수로 두지 않습니다.

### 발표 포인트

모델에 보낼 이력과 감사용 원본은 따로 관리합니다.

## S33 — Harness의 Memory 기능

## Harness의 Memory 기능

### 주요 개념

**Memory capability**: 지속 사실을 제한적으로 주입하거나 필요 시 검색하고 기록하는 기능입니다.

**Namespace**: 저장 범위를 구분하는 이름이며 인증과 DB 권한을 대신하지 않습니다.

### 설명

파일·메모리·DB 등 Store를 선택하고 앱이 인증된 사용자/Agent 범위를 연결합니다. 무엇을 기억할지, 누가 읽거나 바꿀지, SOP가 언제 만료되는지 정해야 합니다. Hermes의 frozen snapshot과 동일한 구현이라고 가정하지 않습니다.

### 발표 포인트

저장 범위뿐 아니라 읽기·수정 권한과 유효기간도 정합니다.

## S34 — Skill 로딩과 MCP 연결

## Skill 로딩과 MCP 연결

### 주요 개념

**Skill library**: 절차 문서를 검증·등록하고 목록과 본문을 제공하는 기능입니다.

**MCP Client**: 외부 서버에 접속해 도구를 발견하고 호출합니다.

### 설명

Skill은 모델에게 절차를 알려주고 MCP는 외부 기능을 연결합니다. 사용할 문서와 supporting files, 서버와 인증 설정은 앱이 준비합니다. Skill을 실행 함수로, MCP를 필수 저장소로 취급하지 않습니다.

### 발표 포인트

사용할 절차와 서버, 인증 설정을 준비해야 합니다.

## S35 — Agent 사이의 작업 전달

## Agent 사이의 작업 전달

### 주요 개념

**Delegation**: 부모가 자식에게 작업을 맡기고 결과를 받아 계속 진행합니다.

**Routing / Graph / Advisor**: 역할 선택, 명시적 단계, 자문 호출 등 제어 방식을 달리 구성합니다.

### 설명

다음 행동을 누가 결정하는지, 결과가 어디로 돌아오는지, 어떤 상태를 공유하는지 비교합니다. 부모 반환 패턴을 다른 SDK의 native handoff API와 동일시하지 않습니다. 실제 데이터·Tool 권한과 비용은 별도 설계 대상입니다.

### 발표 포인트

누가 다음 작업을 정하고 어디로 결과를 돌려주는지 확인합니다.

## S36 — 승인을 기다렸다가 실행 재개하기

## 승인을 기다렸다가 실행 재개하기

### 주요 개념

**Deferred Tool Call**: 즉시 실행하지 않고 승인이나 외부 결과를 기다리는 호출입니다.

**재개**: 호출 ID와 승인/결과를 연결해 다음 실행으로 이어가는 과정입니다.

### 설명

검토한 인자와 실제 실행 인자가 일치하는지 확인하고 데이터 버전과 사용자 권한을 실행 시점에 다시 검사합니다. 승인 UI, 인증, 영속 저장과 재시작 복구는 호스트 앱이 연결해야 합니다. UI가 없을 때 사용할 CLI·handler·보류 결과 경로도 정해야 합니다.

### 발표 포인트

검토한 호출과 인자를 실행 시점에 다시 확인합니다.

## S37 — Core와 Harness로 구성하는 Agent

## Core와 Harness로 구성하는 Agent

### 주요 개념

**Core + Harness**: 내부 실행 Graph에 선택적 Memory·Skills·동작 기능을 연결하는 구성입니다.

**업무 구현**: 인증·DB 접근·검증·저장 등 서비스에 맞게 만드는 코드입니다.

### 설명

제공 기능을 사용해도 업무 요구가 자동으로 충족되는 것은 아닙니다. 반대로 모든 기능을 직접 구현해야 하는 것도 아닙니다. 검증·Tool 실행·최종화·재개를 연결하면서 필요한 업무 규칙을 각 지점에 넣습니다.

### 발표 포인트

데이터, 권한, 결과 검증은 업무에 맞게 설계합니다.

## S38 — PydanticAI Demo

## PydanticAI Demo

### 주요 개념

**Runtime 관찰**: 정의 코드, 내부 노드, 실제 요청, Tool 인자와 반환을 연결해 확인합니다.

**고정 응답 시험**: 정해진 모델 응답을 실제 executor가 처리하는 시험이며 live LLM 응답과 구분합니다.

### 설명

Core 최소 실행을 먼저 보고 Memory 등 Harness 한 경로를 추가해 차이를 확인하는 Demo 계획입니다. 종료 정책은 자연 모델이 같은 응답을 반복한다고 가정하지 않고 별도 시험으로 비교합니다. 현재 발표의 Demo 링크는 실제 서비스가 연결되지 않은 안내 화면입니다.

### 발표 포인트

Core 실행을 먼저 확인한 뒤 Harness 기능을 추가합니다.

## S43 — Agent를 어디에서 실행할까?

## Agent를 어디에서 실행할까?

### 주요 개념

**중앙 실행**: 서버가 Agent·작업·사용자 격리·공통 운영을 관리합니다.

**로컬 실행**: 사용자 PC에 설치·업데이트·실행 권한 관리가 필요합니다.

### 설명

Agent의 CPU/메모리, Tool I/O, 승인·모델 대기와 모델 서버 GPU 자원은 수명이 다릅니다. 로컬 Agent도 모델 요청으로 정보를 보낼 수 있어 데이터 경로를 확인해야 합니다. Worker/GPU 수는 모델, 부하, Context와 실제 대기를 측정한 뒤 정합니다.

### 발표 포인트

Agent 실행 자원과 모델 서버 자원을 나누어 살펴봅니다.

## S44 — 실행 기록과 업무 결과 검증

## 실행 기록과 업무 결과 검증

### 주요 개념

**Trace**: 요청·Tool·승인·오류·결과와 사용 데이터의 실행 기록입니다.

**Evaluation**: 요구한 계산·근거·권한·업무 목표를 만족했는지 평가합니다.

### 설명

같은 Tool을 호출했어도 데이터 snapshot이나 기간·분모가 다르면 다른 분석입니다. 근거/SOP 버전, 승인 인자와 실제 실행, 예측의 시간 분할과 누수를 확인합니다. 조회 성공, 원인 가설, 예측 성능을 구분하며 실행 기록만으로 정확성을 판정하지 않습니다.

### 발표 포인트

데이터 범위, 계산, 근거, 승인 내용을 함께 확인합니다.

## S45 — 구조를 이해하고 실제 개발로

## 구조를 이해하고 실제 개발로

### 주요 개념

**Hermes**: 갖춰진 Harness에서 상태·기억·도구·정책의 동작을 살펴봤습니다.

**PydanticAI**: 코드 정의와 내부 Graph, 검증·실행·확장의 연결을 살펴봤습니다.

### 설명

프레임워크가 제공하는 기능을 이해한 뒤 실제 업무의 데이터·권한·검증을 연결해야 합니다. 3차에서는 직접 Agent를 개발하고 같은 기준으로 결과와 시행착오를 검토합니다.

### 발표 포인트

3차에서는 Agent를 개발하고 검증 결과와 시행착오를 공유합니다.

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
17. **네 SDK 비교가 왜 비어 있나?** 사용자가 이번에 내용 원본으로 한 흐름 문서에서 미작성 상태다. 원문 밖 기능을 채우지 않고 순서와 편집 자리만 유지했다. A-4/S39–S42.
18. **GPU/Worker는 몇 개가 필요한가?** 모델·동시 실행·Tool I/O·Context·승인 대기·하드웨어 실측 없이는 정할 수 없다. 책임 배치를 먼저 고른다. S43.

---

# 근거와 정정

조사·참고자료와 적용 범위

## F-1. 내용 원본과 조사 범위

- **[FLOW]** [0_2차_세미나_발표_흐름.md](0_2차_세미나_발표_흐름.md): 전체 발표 순서·질문·추가 검증 요청·Demo 요구. 이번 데모 계약을 먼저 개정했다.
- **[DESIGN]** [1차 blueprint](agent_framework_seminar_1_slide_blueprint.md): A~G 구조·정보 위계·색·도식·노트 분리·탐색의 기준.
- [Hermes 추가 코멘트](hermes/Hermes_Agent_발표_실무_시사점_코멘트.md)와 [PydanticAI 추가 코멘트](PydanticAI/PydanticAI_발표_실무_시사점_코멘트.md)는 원문의 보강 의도와 관련된 snapshot/검색/병렬/최종화/승인 설계 해석을 확인했다. 이를 공식 제품 보장이나 실측 결과로 취급하지 않는다.
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