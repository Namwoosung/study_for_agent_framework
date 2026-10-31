# Agent Framework 세미나 1차 — Introduction & Core Concepts

**이 1차 세미나는 과거에 이미 진행한 세미나로서, 세미나의 내용은 이미 발표가 완료된 상황**
**추가로 아래 다른 사람의 범위라고 기술되어 있던, tool과 orchestration도 발표가 완료된 상황**
**현재 프로젝트의 내용들은 후속 세미나인 2차 세미나에 관한 내용**
**2차 세미나는, 해당 문서의 1차 세미나 내용은 모두 청중이 알고있다고 가정할 것이며, 중복된 내용 없이 2차 세미나에 해당되는 내용의 핵심을 담아야 함**
**발표자료 자체는 현재 문서인 1차 세미나 blue print 기반으로 제작한 것과 유사한 디자인과 구조를 가질 것. 하지만 내용은 2차 세미나에 맞춰서 준비할 필요가 있음**

> **용도:** Claude(또는 다른 프론트엔드 구현 모델)에 전달할 **HTML 슬라이드 제작 지시서**이자 발표자용 **기술 해설·대본·Q&A 문서**.  
> **기준일:** 2026-10-26  
> **언어:** 청중용 화면은 한국어 중심, 중요한 전문 용어는 영어 병기.  
> **담당 범위:** 1차 세미나 Introduction + Core Concepts. 다른 발표자가 담당하는 Tools·Orchestration의 상세 구현, 2차 프레임워크 비교, 3차 실습·데모는 다루지 않음.  
> **권장 분량:** 본편 30장(00~29). 전체를 충분히 설명하면 약 40~50분. 발표 시간에 따라 `우선순위: 선택` 슬라이드는 통째로 생략 가능.  
> **기술 상태:** 모든 예시 코드/로그/벤치마크 수치는 별도 표기가 없는 한 **개념 설명을 위해 작성한 예시**이며 실측 데모가 아님.

---

# A. Claude를 위한 구현 지침 — 가장 먼저 읽을 것

## A-1. 결과물 형태

1. 단일 웹앱으로 실행되는 16:9 **한 화면 = 한 슬라이드** 방식. 마우스, `←/→`, `Space`, 페이지 번호 점프로 전환 가능. 스크롤로 다음 페이지가 노출되지 않도록 할 것.
2. `slideId`는 아래 `S00`~`S29`를 그대로 사용. 각 슬라이드는 `title`, `onScreen`, `visual`, `buildSteps`, `speakerNotes`, `sourceRefs`가 분리된 데이터 구조로 구현 권장.
3. 슬라이드 본문에 **발표자 개념 해설·대본을 통째로 넣지 말 것**. 해당 내용은 발표자 노트 패널(`N` 키) 또는 별도 `notes` JSON에 저장한다. 브라우저 상 발표자 노트는 일반 청중 화면에 노출되지 않아야 한다.
4. 정적인 그림을 붙이는 대신, 핵심 구조도(S07/S09/S11/S12/S17/S21/S23/S26/S27)는 가능하면 **SVG/CSS 도형 + 텍스트**로 직접 구현한다. 복잡한 이미지 생성 없이도 재구성·편집 가능해야 한다.
5. `buildSteps`는 **슬라이드 내부 단계**다. `→` 누르면 남은 빌드 스텝부터 재생하고, 해당 슬라이드의 마지막 스텝 이후에만 다음 페이지로 이동. `←`는 반대. 현재 단계 `k/n`을 작은 영역에 표시한다.
6. 모든 도식의 노드·화살표는 연결 관계가 분명해야 한다. 도구 실행, 모델 추론, 메모리 로드의 주체를 혼동하게 표현하지 말 것.
7. 실제 LLM API 호출·네트워크 요청·임의 코드 실행을 요구하지 않는다. 설명용 인터랙션은 **사전에 고정된 시뮬레이션 데이터**만 사용해 동일하게 재현한다.
8. 등장하는 코드는 복사 가능한 텍스트와 구문 강조로 구현. 모바일에서는 레이아웃을 세로로 재배치하되 내용이 잘리지 않도록 한다.
9. 발표 중 네트워크 장애를 고려해 폰트·아이콘·도형은 가능한 로컬 자산 사용. 외부 링크는 슬라이드 끝의 작은 `Sources` 아이콘 또는 노트에서만 열리도록 한다.
10. 접근성: 애니메이션 끄기(`Reduced motion`) 지원, 모든 인터랙션의 비애니메이션 최종 상태 제공, 색상 외에 텍스트/아이콘으로 상태 구별.

## A-2. 디자인 시스템

- 분위기: **Tech conference / clear systems thinking**. 과도한 네온·글래스모피즘보다 깔끔한 어두운 배경과 도식 가독성 우선.
- 배경 `#0B1020`, 기본 텍스트 `#EFF4FF`, 보조 `#9EACC8`, 구분선 `#33415D`.
- 의미색 **LLM/Reasoning = 파랑 `#60A5FA`**, **Runtime/Harness = 보라 `#B794F4`**, **Tool/External Action = 녹색 `#34D399`**, **Context/Memory = 주황 `#FDBA74`**, **Risk/Failure = 빨강 `#FB7185`**, **Success = 민트 `#5EEAD4`**.
- 슬라이드 가로 여백 7%, 세로 6%, 상단 section label 14~18px, 제목 38~54px, 핵심 설명 22~30px, 보조 텍스트 17~22px, 코드 18~22px 권장(1920x1080 기준); 과밀 슬라이드만 조절.
- 제목은 가능한 **결론형 문장**. 일반적인 정의는 따로 `Key takeaway` 한 줄로 강조하되 색상 큰 카드 남발 금지.
- 슬라이드 하단에 `01 / 30` 형식의 번호와 현재 섹션만 작게 표시.
- 사용자 요청 예시와 에이전트 실행 Trace는 같은 인물·동일한 도구/상태/파일 이름을 계속 사용하여 일관성 유지.
- 기본적으로 0.25~0.45초 Ease-out 전환. `Enter` 또는 슬라이드의 별도 실행 버튼으로 인터랙션 재생 가능. 모든 모션은 Pause/Reset 가능.

## A-3. 통일 예시: 고장 난 테스트를 고치는 코딩 Agent

> 사용자의 한 가지 요청을 슬라이드 전체에서 발전시킨다. 실제 실행 내용처럼 속이지 말고 `가상 실행 시나리오`라고 명시.

**User Goal**: `로그인 테스트가 실패해. 원인을 찾아 수정하고, 다시 테스트해서 검증해줘.`

**가상 환경**:
- 파일: `tests/test_login.py`, `src/auth.py`
- 읽기 도구: `read_file(path)`
- 테스트 도구: `run_tests(target)`
- 수정 도구: `apply_patch(path, diff)`
- 결과 검증: 테스트 통과 + 변경 diff + 사용자가 승인한 범위 내 수정
- 초기 증상: `test_login_expired_token FAILED` (expired token 처리 분기가 잘못되어 있다고 가정)
- 도구 출력: 예제 로그와 예제 JSON을 사전 정의. 현실의 인증 로직 버그를 재현하거나 보안 취약점을 유도하려는 목적이 아님.

**표준 Trace (`trace_v1`)**:
```
T0 User        로그인 테스트가 실패해. 원인 찾아 고쳐줘.
T1 Model       tool_call run_tests({"target":"tests/test_login.py"})
T2 Runtime     run_tests 실행 -> FAILED, assertion mismatch
T3 Model       tool_call read_file({"path":"src/auth.py"})
T4 Runtime     파일 내용 반환 -> expired token 분기 오류 확인
T5 Model       tool_call apply_patch({"path":"src/auth.py","diff":"..."})
T6 Runtime     허용 경로 검증 후 패치 적용 -> OK
T7 Model       tool_call run_tests({"target":"tests/test_login.py"})
T8 Runtime     테스트 실행 -> PASSED
T9 Model       변경 요약 + 검증 결과 보고
```
**실패/복구 분기 (`trace_failure`)**: 첫 번째 패치 뒤 테스트 여전히 FAIL -> 실패 로그 관찰 -> 이전 가설 재검토 -> 허용된 횟수 내 재시도 -> PASS 또는 사용자에게 불확실성 보고. **모델 파라미터 자체가 업데이트된 것은 아님**.

## A-4. 전체 세미나 경계

| 세미나 | 주제 | 이 문서와의 관계 |
|---|---|---|
| 1차 | Introduction / Core Concepts → Tools → Orchestration | **이 문서는 앞의 파트만**. Tool/MCP/Skill, Orchestration은 개념·연결 관계까지만 소개 |
| 2차 | Hermes, PydanticAI, Deep Agents, LangChain/LangGraph, LLM Serving(vLLM/SGLang) 등 비교 | 특정 구현의 상세 API, 벤치마크, 장단점 비교는 **보류** |
| 3차 | 직접 Agent 개발·실습·시연 | 실제 프로젝트 구현·데모는 **보류** |

## A-5. 핵심 사실 검증 체크리스트

- `LLM = Agent` 아님. Agent는 모델 주변에 도구·상태·실행 제어가 결합된 **시스템**.
- 모든 Agent가 장기 메모리, 독립 계획기, MCP, 멀티 에이전트를 필수로 갖추는 것은 아님.
- Tool Calling = 모델이 **도구 호출 요청을 출력**하는 것. **도구 실행 주체는 Runtime/호스팅 실행 환경**. MCP는 연결 프로토콜.
- `Workflow vs Agent`는 **완전한 이분법이 아니라 제어권의 정도**를 구분하기 위한 아키텍처 관점.
- `State`(실행 상태), `Context`(이번 모델 호출에 전달된 정보), `Memory`(보존/검색 가능한 정보)는 같은 것이 아님.
- Context Window가 커져도 **모든 기억이 자동으로 유지되거나 품질이 선형 개선되는 것은 아님**.
- Self-correction(현재 실행에서 실패 관찰 후 수정) ≠ Continuous learning(세션 간 보존된 능력/지식 업데이트) ≠ Fine-tuning(모델 가중치 업데이트).
- Guardrails를 `시스템 프롬프트 한 줄`로만 표현하지 말고 권한·입력 검증·샌드박스·승인·테스트 등 코드 수준의 집행을 포함.
- 추론 모델의 비공개 chain-of-thought를 실제로 노출하는 UI로 묘사하지 말 것. 화면의 `Decision/Plan`은 **구현이 기록한 외부 행동/요약**이지 내부 숨겨진 추론 기록이 아님.
- 정확한 최신 벤치마크 점수·비용·모델 순위는 이 자료에 넣지 않음. 수시로 바뀌며 2차 세미나의 범위.

## A-6. 본편 목차 및 생략 가능성

| Slide | 제목 | 우선순위 | 예상 소요 |
|---|---|---|---|
| S00 | 시작 인사와 감사 | 필수 | 0.3분 |
| S01 | Agent Framework: Inside the Loop | 필수 | 0.4분 |
| S02 | 세미나 3회 로드맵과 오늘의 목적 | 필수 | 1.5분 |
| S03 | Today's Map | 필수 | 0.5분 |
| S04 | 서로 다른 Agent 정의 | 필수 | 2분 |
| S05 | 오늘 사용할 Agent의 작업 정의 | 필수 | 1분 |
| S06 | LLM Call vs Agent (코드/구조 비교) | 필수 | 2분 |
| S07 | Workflow vs Agent: 누가 다음 단계를 결정하는가? | 필수 | 2분 |
| S08 | 자율성은 스펙트럼 | 선택 | 1분 |
| S09 | Anatomy of an Agent | 필수 | 2분 |
| S10 | Agent Loop — 한눈에 | 필수 | 1.5분 |
| S11 | LLM은 도구를 직접 실행하지 않는다 | 필수 | 2분 |
| S12 | Tool Call 메시지의 왕복 | 필수 | 1.5분 |
| S13 | 하나의 작업을 끝내는 Execution Trace | 필수 | 2분 |
| S14 | Agent Loop: 최소 의사코드 | 필수 | 2분 |
| S15 | 언제 멈추는가? Stop Conditions | 선택 | 1.3분 |
| S16 | Agent의 두뇌: 모델 선택과 추론 | 필수 | 1.5분 |
| S17 | Reasoning과 Planning은 무엇을 바꾸는가? | 선택 | 1분 |
| S18 | State / Context / Memory | 필수 | 2.5분 |
| S19 | 멀티턴 세션은 어떻게 이어지는가? | 필수 | 1.5분 |
| S20 | 장기 메모리는 어떻게 관리되는가? | 선택 | 1.7분 |
| S21 | Context Engineering | 필수 | 2분 |
| S22 | Tool / MCP / Skill의 역할 | 필수 | 2분 |
| S23 | 확대하여 보는 Tool–MCP–Skill | 필수 | 1.7분 |
| S24 | Framework / SDK vs Harness | 필수 | 1.8분 |
| S25 | Prompt → Context → Harness Engineering | 필수 | 2분 |
| S26 | Guardrails & Human-in-the-loop | 필수 | 1.5분 |
| S27 | 실패에서 회복하는 Agent | 필수 | 2분 |
| S28 | Trace / Observability / Evaluation | 필수 | 1.6분 |
| S29 | 핵심 3가지 + 다음 발표 연결 | 필수 | 1분 |

> **편집 참고:** 예상 소요는 실제 리허설 전의 대략적인 가이드일 뿐. 모든 슬라이드를 설명할 경우 약 45분 전후가 될 수 있다. 30분 제한이 있으면 S08, S15, S17, S20을 제외하고 S12, S23을 빠르게 전환한다.

---

# B. 슬라이드별 상세 명세

## S00 — Opening: 감사 인사

- **섹션:** Opening · **우선순위:** 필수
- **설명 목적:** 차분한 시작, 감사, 발표 분위기 설정. 학술적 설명은 여기서 시작하지 않는다.
- **화면에 실제 넣을 텍스트**
  - 메인: `감사합니다. 그리고, 반갑습니다.`
  - 서브: `Agent Framework 세미나 · 1차` 
  - 하단 아주 작게: `Introduction & Core Concepts`
- **화면 구성:** 어두운 배경 중앙 상단 1/3에 큰 한글 문장, 아래 짧은 영문. 오른쪽 하단에 추상적 연결 노드 3개만. 인물 사진, 억지 3D AI 이미지 불필요.
- **인터랙션:** 등장 시 문구 0.4초 fade-in, 다음 키로 S01. 환영 슬라이드에 과한 모션 금지.
- **발표자용 설명/대본:**
  > 발표 기회를 주셔서 감사합니다. 이번에는 Agent Framework라는 주제로 세미나를 준비했습니다. 이미 다들 Agent와 LLM을 많이 접하셨기 때문에, 기본 용어를 나열하기보다는 내부 구조와 개념을 한 번 더 정확히 맞춰보는 시간이 되었으면 합니다.
- **주의:** 여기서 발표자의 이름이나 소속 등 개인정보를 임의 생성하지 않는다.

## S01 — Agent Framework: Inside the Loop

- **섹션:** Opening · **우선순위:** 필수
- **핵심:** 오늘은 프레임워크 제품을 나열하기 전에 **그 안의 실행 메커니즘**을 들여다본다.
- **화면 텍스트**
  - 영문 헤드라인: `AGENT FRAMEWORK`
  - 메인: `Inside the Agent Loop`
  - 부제: `개념의 합의에서 실제 동작 원리까지`
  - 푸터: `Seminar 01 · Introduction + Core Concepts`
- **화면 구성:** 좌측 58% 제목, 우측 42%에 작은 원형 루프(`Decide → Act → Observe → Decide`)를 추상화해 표현. 중앙 점은 파란 Model, 궤도 바깥에는 녹색 Tool, 보라 Runtime.
- **인터랙션:** 궤도 한 바퀴 순환은 2초 후 정지. 발표자의 클릭으로 `Model ≠ Agent` 문구 등장.
- **발표자 대본:**
  > 제목이 Agent Framework이지만, 제 파트에서는 특정 프레임워크의 장단점을 비교하지 않겠습니다. 먼저 어떤 프레임워크라도 공통적으로 해결해야 하는 Agent의 실행 구조를 살펴보겠습니다.

## S02 — 3회 세미나 로드맵 / 왜 이 순서인가?

- **섹션:** Opening · **우선순위:** 필수
- **핵심:** 오늘의 역할은 **정의 재정립, 용어 합의, 후속 세미나를 위한 전초**.
- **화면 텍스트**
  - 제목: `세미나의 목표는 '기초 암기'가 아닙니다`
  - 상단 세 가지 키워드: `① 개념 재정립` `② 용어 Consensus` `③ 후속 심화의 공통 기반`
  - 하단 타임라인:
    - `1차 · Foundation` / `Introduction · Core Concepts · Tools · Orchestration`
    - `2차 · Landscape` / `Framework별 특성 · 벤치마크 · LLM Serving`
    - `3차 · Build & Share` / `Agent 개발 · 실제 시연 · 회고`
  - 매우 작은 문구: `현재 파트: Introduction + Core Concepts`
- **레이아웃:** 타임라인 3개 수평 열. 1차만 선명하게, 2·3차는 절반 명도. 1차 내에서 현재 파트만 파란 실선 박스, 다른 발표자 파트는 점선 구역.
- **인터랙션:** 단계1 전체 세미나 노출 → 단계2 현재 파트 강조 → 단계3 `오늘 하지 않을 것: 특정 프레임워크 승부 / 실제 개발 데모` 표시.
- **대본:**
  > 청중분들께서는 Agent를 이미 익숙하게 사용하거나 구현해 보신 분들도 많으실 겁니다. 이번 세미나는 서로 다른 용어 사용을 맞추고, 뒤의 Tools·Orchestration, 그리고 2·3차의 비교와 개발을 똑같은 관점에서 이해하기 위한 자리입니다.
- **개념 보충:** OpenAI 교육 트랙도 Introduction → Core concepts → Tools → Orchestration → Examples → Best practices 순서이며, 그중 우리 발표 범위만 선택한다. [R01]

## S03 — Today's Map: 오늘 답할 5가지 질문

- **섹션:** Opening · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `오늘의 질문 5가지`
  - `1. Agent는 LLM 호출과 무엇이 다른가?`
  - `2. Workflow와 Agent의 경계는 어디인가?`
  - `3. Agent Loop는 실제로 어떻게 실행되는가?`
  - `4. State · Context · Memory · Tool · MCP · Skill은 어떻게 연결되는가?`
  - `5. 좋은 Agent는 모델 외에 무엇이 결정하는가?`
- **레이아웃:** 좌측 5개 번호형 텍스트, 우측에는 S09에서 사용할 Agent 전체 구조도의 비활성 실루엣. 진행될수록 해당 부분이 밝혀지는 느낌.
- **인터랙션:** 키 입력마다 질문 1개 강조, 마지막에는 모두 활성화. 시간 제한 시 한 번에 표시 가능.
- **대본:**
  > 이 다섯 질문을 설명할 수 있다면, 개별 프레임워크의 내부 구조나 설계 선택을 훨씬 쉽게 비교할 수 있습니다.

## S04 — 기관마다 조금 다른 Agent의 정의

- **섹션:** Definition · **우선순위:** 필수
- **핵심:** 하나의 표준 정의를 강요하기보다 **공통 요소와 강조점**을 분리한다.
- **화면 텍스트**
  - 제목: `What is an Agent? — 정의의 공통분모`
  - 카드 ① **OpenAI**: `Instructions + Guardrails + Tools → 사용자를 대신한 Action`
  - 카드 ② **Anthropic**: `LLM이 프로세스와 Tool 사용을 동적으로 제어`
  - 카드 ③ **ACM From-Scratch 관점**: `Tool Abstraction + Agent Loop + MCP/Skills 등 내부 구성요소`
  - 하단 요약: `공통분모: 목표 · 의사결정 · 행동 · 피드백`
- **레이아웃:** 상단 3개 균형 카드. 가운데 해당 키워드만 의미색 강조. 하단에 4개 원(`Goal`, `Decision`, `Action`, `Feedback`) 수평 연결. 
- **인터랙션:** 1/2/3 카드를 순서대로 활성화 후, 하단 공통분모를 도출하는 짧은 애니메이션.
- **발표자용 개념:**
  - OpenAI Building Agents는 지시사항·가드레일·도구를 통해 사용자를 대신해 행동하는 시스템을 소개한다. [R01]
  - Anthropic Building Effective Agents는 `agentic systems`라는 넓은 표현 안에서 **코드가 미리 흐름을 결정하는 Workflow**와 **모델이 자신의 행동 흐름을 동적으로 결정하는 Agent**를 구분한다. [R02]
  - ACM TechTalks는 엄밀한 새 정의의 인용 출처라기보다 **프레임워크를 벗겨낸 내부 구성요소의 학습 관점**이다. 따라서 카드 ③은 `ACM 발표의 설명 관점`이라고 표기하고 "ACM은 agent를 이렇게 정의했다"라는 직접 인용으로 쓰지 말 것. [R03]
- **대본:**
  > Agent라는 단어의 정의가 회사와 연구자마다 완전히 같지는 않습니다. OpenAI는 '행동할 수 있는 시스템'을, Anthropic은 '누가 실행 경로를 결정하느냐'를 강조합니다. ACM 강의는 이 개념을 실제 프로그램으로 어떻게 구성하는지 보여줍니다. 이 공통분모를 오늘의 기준으로 삼겠습니다.
- **출처 표시:** `[R01] [R02] [R03]`

## S05 — 이번 발표에서 사용할 실용적 정의

- **섹션:** Definition · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Agent = 모델을 포함한 실행 시스템`
  - 주 문장(큰 글씨): `LLM이 목표 달성을 위한 다음 행동을 선택하고, 실행 결과를 관찰하며 작업을 이어갈 수 있도록 설계된 시스템`
  - 네 가지 강조 표현: `Goal` / `Decision` / `Action` / `Feedback`
  - 하단: `Agent는 특정 모델명이나 프레임워크명이 아니다.`
- **레이아웃:** 중앙 커다란 정의. 동사 `선택하고`, `관찰하며`, `이어갈`은 파랑/녹색으로 강조. 아래 네 가지 토큰을 이어 연결.
- **인터랙션:** 문장에 등장하는 각각의 표현을 클릭하면 아주 짧은 설명 툴팁:
  - Goal: 완수할 목표·성공 기준
  - Decision: 답변 또는 도구 사용 등 다음 단계 결정
  - Action: 허용된 도구를 통한 실제 외부 동작
  - Feedback: 관찰한 실행 결과를 다음 판단에 반영
- **발표자 개념:** 이 문장은 **발표용 작업 정의**이지 모든 조직이 공유하는 단일 공식 정의가 아니다. Agent가 도구를 한 번만 사용하고 종료하는 것도 가능하므로 반드시 다회 호출을 요구하지 않는다.
- **대본:**
  > 저는 오늘 Agent를 'LLM을 중심으로 목표를 달성하기 위한 행동을 결정하고, 그 결과에 따라 계속 작업할 수 있도록 구성된 시스템'이라고 부르겠습니다. 이 정의에서 중요한 단어는 모델이 아니라 시스템, 그리고 행동과 피드백입니다.

## S06 — LLM Call vs Agent: 코드로 비교

- **섹션:** Definition · **우선순위:** 필수
- **핵심:** 차이는 `LLM 호출 횟수`만이 아니라 **의사결정과 외부 실행 제어의 결합**.
- **화면 텍스트**
  - 제목: `LLM 호출과 Agent는 같은 코드가 아닙니다`
  - 좌측 헤더: `One-shot LLM Call`
  - 좌측 코드:
    ```python
    answer = llm(
        "로그인 테스트가 왜 실패할까?"
    )
    print(answer)  # 가능성 설명
    ```
  - 우측 헤더: `Agentic Execution (개념 코드)`
  - 우측 코드:
    ```python
    state = init(goal)
    while not done(state):
        step = llm(make_context(state))
        if step.tool_call:
            result = run_tool(step.tool_call)
            state.observe(result)
        else:
            return step.answer
    ```
  - 하단: `답변 생성` `vs` `도구 실행 + 결과 피드백 + 조건부 반복`
- **레이아웃:** 정확히 절반 코드 패널 2개. 좌측은 `User → LLM → Text`, 우측은 `User → Model ↔ Runtime/Tools → Verified result` 도식. *좌측도 검색된 문서를 프롬프트에 넣을 수 있으며, 우측도 외부 도구 없이 바로 종료할 수 있음*을 노트에 표시.
- **인터랙션:** Step1 좌측 코드 실행 결과 `추측·설명` 노출 → Step2 우측 루프의 `run_tool` 강조 → Step3 테스트 결과가 다시 `make_context`에 들어가는 화살표.
- **대본:**
  > 단일 LLM 호출도 매우 유용하지만, 로그를 읽고 코드를 수정하고 실제 테스트를 실행했다는 보장이 없습니다. Agent에서는 모델의 출력이 다음 행동의 입력이 되고, 실행 결과가 다시 판단에 들어옵니다. 이제 모델만 설명하는 것이 아니라 실행을 포함한 시스템을 말하게 됩니다.
- **개념 주의:** 위 코드의 `llm`, `run_tool`, `init`은 가상 함수. **LLM 모델 자체가 Tool을 실행하지 않음**은 다음 장에서 설명.

## S07 — Workflow vs Agent: Who controls the next step?

- **섹션:** Definition · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `누가 다음 단계를 결정하는가?`
  - 좌측: `Workflow` / `코드가 경로를 정의` / `예측 가능 · 테스트 용이`
  - 우측: `Agent` / `모델이 경로를 동적으로 선택` / `유연성 · 변동성 관리 필요`
  - 아래 한 줄: `Workflow도 LLM을 쓸 수 있고, Agent도 정해진 제약 안에서 동작합니다.`
- **핵심 도형:** 좌측 `사용자 요청 → 검색 → 분석 → 문서 생성 → 검토` 고정 DAG. 우측 `사용자 요청 → Model decision ◇`에서 `run_tests`, `read_file`, `ask_user`, `final`을 동적으로 선택하고 결과가 모델로 되돌아오는 directed graph.
- **인터랙션(중요):** 상단 토글 `정상 입력` / `예상 못한 오류`.
  - 정상 입력: 좌측은 고정 4단계 그대로, 우측은 모델이 `run_tests → read_file → fix → run_tests` 선택.
  - 예상 못한 오류: 좌측은 정의된 오류 분기만 사용(없는 경우 실패로 표시), 우측은 도구 결과를 보고 `read_file` 또는 `ask_user` 등 새 경로 선택(항상 성공 보장 X).
  - 이동하는 빛줄기는 순차 재생, 한 화면에는 경로가 명확히 보이도록 함.
- **발표자 개념:** Anthropic은 'Agentic system' 안에 Workflow와 Agent를 모두 포함하는 넓은 의미를 사용한다. 실무상 혼합형이 많아 '완전히 별개 제품'처럼 묘사하면 안 된다. 예측 가능한 작업은 단일 호출/Workflow가 오히려 적절할 수 있고, Agent는 비용·지연·비결정성이 늘 수 있다. [R02]
- **대본:**
  > Workflow와 Agent를 구별할 때 핵심은 LLM을 몇 번 쓰느냐가 아닙니다. 다음 단계가 사전에 정한 코드 경로인지, 현재 관찰 결과를 본 모델의 판단인지입니다. 그래서 항상 Agent가 정답은 아닙니다. 고정 경로로 충분하다면 단순한 Workflow가 더 싸고 검증하기 쉬울 수 있습니다.
- **재사용:** `Workflow/Agent` 도형 색상·노드는 S08, S09에서 동일하게 유지.

## S08 — Agent는 자율성의 스펙트럼 위에 있다

- **섹션:** Definition · **우선순위:** 선택
- **화면 텍스트**
  - 제목: `Agentic ≠ Fully Autonomous`
  - 수평 스펙트럼 항목: `Single LLM Call` → `Tool-assisted` → `Bounded Agent` → `High-autonomy Agent`
  - 하단: `더 높은 자율성 = 더 큰 권한·실패 영향·관측 필요성`
- **레이아웃:** 하나의 수평 선 위에 4개 스테이지. 아래 각각 `결정권`, `행동 범위`, `사람의 승인 필요성` 비교. 점수나 정확한 정량 척도는 쓰지 않는다.
- **인터랙션:** 스테이지를 클릭하면 우측 설명 바뀜. 예를 들어 `Bounded Agent`: `코드 읽기·테스트는 자동 / 파일 수정은 승인 후`.
- **발표자 개념:** 모델이 일정한 판단을 하더라도 Runtime에서 행동/권한을 제한할 수 있다. 에이전트의 자율성을 높이는 것이 항상 성능이나 안전성 개선을 보장하지 않는다.
- **대본:**
  > 실제 제품에서는 완전히 자율적인지 아닌지보다는, 어떤 행동을 모델에 위임했고 어떤 결정은 코드 또는 사람이 보유하는지가 중요합니다. 이를 자율성의 정도라고 볼 수 있습니다.

## S09 — Anatomy of an Agent: 최종 구조

- **섹션:** Architecture · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Agent는 하나의 모델이 아니라 시스템입니다`
  - 도형 레이블: `User Goal`, `Instructions`, `LLM / Model`, `Context Builder`, `State`, `Memory Store`, `Runtime / Harness`, `Tools`, `Environment`, `Guardrails`, `Trace`
  - 하단 핵심: `Model decides. Runtime executes. State persists. Tools act.`
- **레이아웃 구체 지시:**
  - 화면 중앙에 가로 70%·세로 66% 크기의 점선 큰 보라색 `Agent Runtime / Harness` 컨테이너.
  - 컨테이너 중앙 상단 파란 `LLM / Model` 카드, 좌측 하단 주황 `Context Builder`와 `State`, 좌측 바깥 `Memory Store`.
  - 컨테이너 우측에는 녹색 `Tool Router / Executor`; 오른쪽 바깥에 `File System`, `Test Runner`, `External API` 3가지 환경 노드.
  - 사용자 입력은 위 → Runtime → Context Builder → LLM으로 흐른다. LLM의 Tool Call은 → Runtime Tool Executor → External Tool, Observation은 역방향 → State → Context Builder → LLM.
  - `Guardrails`는 Tool Executor 전단의 **실행 게이트**, `Trace`는 Runtime 하단 전체를 관찰하는 **관측 레이어**. Guardrails를 단순히 모델 앞쪽 하나에 놓지 않는다.
  - 선은 색상 구분: 모델 요청 파랑, 도구 호출 녹색, 상태/검색 주황.
- **인터랙션:**
  1. User Goal 도착
  2. Context Builder + State 강조
  3. LLM 결정 강조
  4. Tool Executor → Environment 왕복
  5. Observation과 Memory 연결
  6. Guardrails/Trace 레이어 출현
  7. 'Tool·MCP·Orchestration의 세부 내용은 뒤 발표에서' 작은 문구 노출
- **발표자 개념:** 표준 고정 아키텍처가 아니라 **개념적 참조 아키텍처**. 메모리·툴 실행이 외부 서비스에 있을 수도 있다. Harness와 Runtime은 용어가 사용되는 범위에 차이가 있다. Tool·Memory·Orchestration 모두 필수 요소는 아니고 필요 시 추가하는 구성임. [R01][R04][R14]
- **대본:**
  > 이 그림에서 모델은 판단의 중심입니다. 하지만 모델은 외부 파일에 손을 대거나 실행 이력을 관리하는 프로그램 자체가 아닙니다. 맥락과 상태를 준비하고, 모델이 요청한 행동을 검증·실행하며, 결과를 다음 호출에 반영하는 실행 구조가 필요합니다. 여기서 Tools와 Orchestration의 구체적인 패턴은 다른 발표에서 자세히 다룰 예정이니, 지금은 전체 속에서의 역할을 중심으로 보겠습니다.
- **중요 재사용 지시:** 이 도형의 노드 ID를 `agent-architecture-*`로 지정해 S10, S18, S22~S26의 포커스 줌에서 동일 컴포넌트를 재사용. 각각 새 디자인으로 바꿔 그리지 않는다.

## S10 — Agent Loop: Decide → Act → Observe → Repeat

- **섹션:** Mechanism · **우선순위:** 필수
- **핵심:** 자율 행동의 최소 메커니즘은 **행동 결과를 다시 입력으로 받는 제어 루프**.
- **화면 텍스트**
  - 제목: `Agent의 핵심은 Loop입니다`
  - 큰 원형 도식: `1. Context 구성` → `2. Model 판단` → `3. Tool 실행` → `4. 결과 관찰` → 다시 1
  - 별도 종료 가지: `Final Answer / Escalate / Stop`
  - 아래: `Perceive → Decide → Act → Observe` (이해를 위한 간략화)
- **레이아웃:** S09 도식에서 중앙 루프만 확대 전환. 네 개의 원형/둥근 사각형을 다이아몬드/원형 배치. `Model 판단` 파랑, `Tool 실행` 녹색, `Context` 주황, `Runtime` 가장 바깥 보라 링.
- **인터랙션 핵심:**
  - `▶ 실행` / `⏸ 일시정지` / `↺ 초기화` / `다음 단계` 제공.
  - 실행 시 목표 텍스트가 들어오고, LLM이 `run_tests` 호출을 요청, Runtime에서 실행, FAIL이 관찰로 돌아옴. 2회차 LLM이 `read_file`을 선택하도록 애니메이션.
  - 각 단계 hover/click 시 하단에 `어떤 데이터가 이동하는가?` 1문장 제시.
  - `Final Answer`가 선택되면 루프 선에서 빠져나감. **무조건 무한 루프가 되지 않도록 종료 분기 눈에 띄게 구성**.
- **발표자 기술 해설:**
  - Loop는 `while True` 문법이 본질이 아니라 `모델 판단 → 외부 실행/관찰 → 다음 판단`이라는 **피드백 제어**가 본질. 실제 SDK에는 단일 모델 호출 내부에 호스팅된 도구 사용을 처리하는 동작도 존재하며, 앱 개발자가 모든 왕복을 직접 코딩하지 않을 수 있음.
  - ReAct를 소개할 경우 **Reasoning + Acting** 패턴으로 단락 하나만. 원문 논문의 상세 수식이나 숨겨진 Chain-of-Thought 원문을 보여줄 필요 없음.
  - 최종 답변, 에러, 사람 승인, 횟수/시간/비용 제한은 별도 분기(S15).
- **대본:**
  > Agent가 복잡하게 느껴져도 반복되는 최소 단위는 단순합니다. 모델이 다음 행동을 고르고, 시스템이 수행하고, 그 결과를 다시 모델이 판단할 수 있는 형태로 제공합니다. '실패했다'라는 관찰이 다시 들어가면 다른 행동을 선택할 수 있습니다. 여기서부터 Agent가 단순 자동화와 다르게 느껴지는 부분이 시작됩니다.
- **출처:** [R01][R03][R06][R07]

## S11 — LLM은 Tool을 직접 실행하지 않는다

- **섹션:** Mechanism · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Tool Calling은 '실행'이 아니라 '실행 요청'입니다`
  - 5단계 라벨: `Tool Schema 전달` → `Model이 Tool Call 생성` → `Runtime 검증·실행` → `Tool Result 반환` → `Model이 후속 판단`
  - 중앙 크게: `Model output ≠ Side effect`
  - 하단 경고: `권한 검사와 실제 I/O는 실행 환경의 책임`
- **레이아웃:** 좌에서 우로 순차적인 Sequence Diagram: `App/Runtime | Model | Tool Executor | File/Test Environment` 4개 수직 레인.
- **인터랙션:** `run_tests(target)`를 요청하는 파란 메시지 객체가 Model에서 Runtime으로 이동. Runtime이 `authorized?` 검사. 통과하면 녹색 도구 아이콘이 실제 실행 결과 `FAILED`를 돌려준다. 결과가 Context에 들어가 다시 모델에 전달된다.
- **발표자 기술 해설:**
  - `Tool definition/schema`는 모델에게 호출 가능한 이름·설명·인수 형식을 전달해 적절한 구조화 출력을 유도한다. 실제 도구 함수/API 실행은 호스트 앱 또는 관리형 도구 인프라가 담당. [R05]
  - 모델이 도구 호출을 **선택할 확률**, 도구 실행 **허가 여부**, 실행의 **성공 여부**는 다른 문제. 유효한 JSON이어도 승인되지 않은 호출일 수 있다.
  - 호스팅 Tool은 서비스에서 실행될 수 있으므로 '반드시 우리 백엔드의 Python 함수가 실행한다'라고 단정하지 않음.
- **대본:**
  > 가장 중요한 오해 중 하나가 'LLM이 파일을 열었다'는 표현입니다. 실제로는 LLM이 어떤 기능을 어떤 인수로 사용하고 싶은지 Tool Call을 생성하고, 실행 환경이 그 요청을 검증하고 수행합니다. 모델이 말하는 것과 시스템이 실제로 바꾸는 것은 구분해야 합니다.
- **출처:** [R05]

## S12 — 메시지 수준에서 보는 Tool Calling 왕복

- **섹션:** Mechanism · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Tool Call은 결국 구조화된 메시지 교환입니다`
  - 왼쪽: `Model output: function_call`
  - 중앙 코드(설명용이며 OpenAI Responses API 형태를 본뜬 **축약 예시**):
    ```json
    {
      "type": "function_call",
      "name": "run_tests",
      "arguments": "{\"target\":\"tests/test_login.py\"}",
      "call_id": "call_01"
    }
    ```
  - 오른쪽: `Tool output → Model input`
    ```json
    {
      "type": "function_call_output",
      "call_id": "call_01",
      "output": "FAILED: assertion mismatch"
    }
    ```
  - 하단: `call_id가 요청과 결과를 연결합니다`
- **레이아웃:** 좌/우 코드 블록 2개, 가운데 `Runtime executes` 녹색 화살표. `call_id`에 동일 강조색을 적용. 스크린 전체에서 JSON이 읽히도록 최소 한 줄 폰트 20px.
- **인터랙션:** 단계1 왼쪽 `name / arguments` 강조 → 단계2 인수가 Runtime 내부 함수로 매핑 → 단계3 Tool Result 등장 → 단계4 두 `call_id` 강조 및 `Context`로 반입.
- **발표자 기술 해설:**
  - 실제 API 구현과 SDK에 따라 메시지 타입과 필드가 다르므로 **이 예시는 개념형**. API의 특정 버전을 구현하는 코드를 그대로 복사한 완제품 아님.
  - `arguments`는 JSON 오브젝트가 아니라 **직렬화된 JSON 문자열** 형식으로 전달되는 사례가 있음. 서버에서 파싱/검증이 필요.
  - `function_call`과 `function_call_output`은 별도의 항목. 예시에서 `output` 문자열로 단순화했지만 도구 결과에 이미지/파일 참조/구조화 데이터가 들어갈 수 있다.
  - 여러 Tool Call이 한 번에 나올 수 있으며, 실행 순서/병렬성은 Runtime 책임. 깊이 있는 이야기는 Tools 발표로 넘길 것.
- **대본:**
  > 실제 통신으로 보면 더 명확합니다. 모델은 함수 이름과 인수를 담은 요청 항목을 반환합니다. Runtime이 함수를 호출해 결과를 얻고, 같은 call ID로 이 결과를 다시 모델 호출에 연결합니다. Loop의 중심은 어떤 마법 같은 객체가 아니라 이런 메시지의 왕복입니다.
- **출처:** [R05]

## S13 — 하나의 작업을 끝내는 Execution Trace

- **섹션:** Mechanism · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `한 번의 사용자 요청이 5번의 행동이 되는 과정`
  - 사용자 배너: `“로그인 테스트가 실패해. 원인을 찾아 수정하고 검증해줘.”`
  - 카드 순서:
    1. `run_tests → FAILED`
    2. `read_file → 원인 후보 발견`
    3. `apply_patch → 변경 성공`
    4. `run_tests → PASSED`
    5. `final → 근거와 함께 보고`
  - 오른쪽 작은 상태 표시: `tool_calls: 4` / `test: PASSED` / `status: completed`
- **레이아웃:** 세로 타임라인 5칸 또는 화면이 넓으면 가로 5칸. 각 타임라인에 모델(파랑) → 실행기(보라) → 도구(녹색) 아이콘을 작게 고정 표시.
- **인터랙션:** 하단 `▶ Trace 재생` 클릭 시 한 칸씩 카드 열림. 실패 카드에서는 빨간 테두리, 성공 카드에서 민트. 우측에 `Current context`가 늘어나는 시각 표현. **실제 제품 로그가 아닌 가상 Trace** 레이블 고정.
- **발표자 해설:**
  - 하나의 User turn 안에 여러 번의 모델 호출과 다수 도구 실행이 일어날 수 있음.
  - 목표는 테스트 PASS이지만 그것만으로 전체 프로젝트 품질이 보장되지는 않음. `test_passed`는 **관측 가능한 성공 기준 중 하나**.
  - 결과 리포트에는 실제 실행 여부를 Trace에 근거해 말해야 하며, 실행하지 않은 테스트를 통과했다고 보고하면 실패.
- **대본:**
  > 사용자가 한 줄 요청했더라도 내부적으로는 테스트 실행, 파일 읽기, 패치, 재테스트 같은 사건이 발생합니다. 중요한 것은 모델이 행동을 지시하는 순간과 실제 환경에서 행동이 완료되는 순간을 분리해 관찰할 수 있다는 점입니다.
- **출처:** [R03][R07][R11]

## S14 — Agent Loop의 최소 의사코드

- **섹션:** Mechanism · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `프레임워크를 걷어내면 남는 것은 이 Loop`
  - 코드:
    ```python
    def run_agent(goal, tools, max_steps=8):
        state = init_state(goal)

        for _ in range(max_steps):
            context = build_context(state, tools)
            response = llm(context, tool_schemas=tools.schemas)

            if response.is_final:
                return response.output

            for call in response.tool_calls:
                if not authorized(call):
                    return request_approval(call, state)
                result = execute_tool(call)
                state.add_tool_result(call, result)

        return {"status": "stopped", "reason": "max_steps"}
    ```
  - 하단: `Model decision + Runtime execution + State update + Stopping rule`
- **레이아웃:** 좌측 62% 코드 패널 / 우측 38% S10 Loop 도식 작은 버전. 코드 라인 번호 표시. 위험한 요청을 `request_approval`로 가로채는 위치를 보라색 강조.
- **인터랙션:** Step1 `build_context` 강조와 오른쪽 Context 노드 반짝임 → Step2 `llm`과 Model → Step3 `execute_tool`과 Tool → Step4 `state.add_tool_result`와 Observation → Step5 `max_steps`와 Stop.
- **발표자 기술 해설:**
  - 이 코드는 **실행 가능한 완성품이 아닌 의사코드**. 예외/동시 도구/승인 후 재개/Tool timeout/스키마 검증/트랜잭션 등 생략.
  - `is_final`과 `tool_calls`가 **동시에** 존재하는 응답을 처리하는 방식, 병렬 호출, 스트리밍 등 API 종속 요소가 다름.
  - 사용자 승인 요청 시 현 상태를 유지·저장할 필요가 있을 수 있다. 그래서 `return request_approval`은 개념상 일시 중단을 표현한다.
  - 코드 수준에서 프레임워크의 역할은 이런 반복되는 공통 로직을 추상화하고, 개발자가 비즈니스 정책에 집중하게 돕는 것(S24).
- **대본:**
  > 겉으로는 거대한 Agent Framework가 있어도 그 안에는 이런 반복되는 기본 아이디어가 있습니다. 컨텍스트를 만들고, 모델을 호출하고, 모델이 요청한 행동을 실행하고, 그 결과를 상태에 적습니다. 이를 이해하면 나중에 프레임워크마다 어떤 부분을 추상화했는지 비교할 수 있습니다.
- **출처:** [R01][R03][R05]

## S15 — Agent가 무한히 돌지 않도록: Stop Conditions

- **섹션:** Mechanism · **우선순위:** 선택
- **화면 텍스트**
  - 제목: `Agent에게 필요한 것은 Loop뿐 아니라 Stop입니다`
  - 5개 종료/보류 조건:
    - `Goal achieved` : 성공 조건 확인
    - `Need approval` : 위험 행동 보류
    - `Max steps / Time / Budget` : 비용·자원 제한
    - `Terminal failure` : 복구 불가 오류
    - `Uncertainty / Escalation` : 사람에게 이관
  - 하단: `계속 실행하는 능력과 멈출 수 있는 능력은 같이 설계해야 한다.`
- **레이아웃:** 중앙 Loop에서 종료 분기 5개가 바깥으로 뻗어 나가는 방사형 구조. 성공은 민트, 승인은 주황, 장애는 빨강.
- **인터랙션:** 사용자가 드롭다운 `테스트 PASS / 승인 필요 / 8회 초과 / 권한 오류` 선택 → Loop 바깥에서 해당 종료 분기가 강조됨. 단순 설명용 결정 규칙이라 외부 API 불필요.
- **발표자 개념:** 예산, 반복, 시간, 실패 조건이 없으면 무한 재시도·비용 폭증·반복 부작용 위험. 승인은 **멈춤 후 재개**의 한 유형이지 꼭 최종 실패가 아님. 조건 구체화는 Orchestration/Production engineering과 겹치므로 확장 자제.
- **대본:**
  > 피드백을 받으면 계속할 수 있다는 점이 장점이지만, 끝없이 반복해도 된다는 의미는 아닙니다. 성공 여부를 판단하고, 위험 작업은 멈추고, 한계를 넘으면 사람에게 돌려주는 것도 Agent 실행 구조의 일부입니다.

## S16 — Agent의 두뇌: 어떤 LLM을 쓰느냐도 중요하다

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `좋은 Harness도 좋은 판단을 대체하지는 못합니다`
  - 4개 축: `Task Success` / `Tool Use Reliability` / `Latency` / `Cost`
  - 하단: `모델 선택은 Agent의 작업 특성에 따라 달라집니다.`
  - 보조 키워드: `Reasoning vs Non-reasoning` · `Tool Calling` · `Context Window` · `Structured Output`
- **레이아웃:** 왼쪽 Agent Brain 파란 모델 아이콘, 오른쪽 네 축을 십자형 Trade-off로 표현. 실제 모델명을 비교하거나 임의 벤치마크 수치 쓰지 않음.
- **인터랙션:** `간단한 분류` 클릭 시 빠른/저비용 쪽이 강조, `복잡한 디버깅` 클릭 시 추론/도구 신뢰성 쪽이 강조. 비용·성능은 정량 숫자 아닌 **설계 고려 요인**만 표시.
- **발표자 기술 해설:**
  - OpenAI Building Agents는 **Reasoning / Non-reasoning**의 선택을 Core Concepts로 둔다. 어려운 문제를 위한 추가적인 추론 작업은 지연과 비용을 더 요구할 수 있다. [R01]
  - Agent에서는 일반 문장 품질 외에도 **정확한 도구 선택, 스키마 준수, 다단계 오류 복구, 긴 컨텍스트 처리**가 중요.
  - 실제 멀티 모델 구성은 단일 Task를 빠르게 처리하는 모델과 심화 추론 모델을 라우팅하는 구조로 확장 가능하지만, 모델 라우팅/서빙 상세는 2차 또는 Orchestration 파트로 넘긴다.
  - 강한 모델이 항상 비례해서 전체 Task Success를 높이는 것은 아님. 실행기·도구 품질·테스트 전략이 병목일 수도 있음.
- **대본:**
  > 지금까지 모델 주변의 구조를 강조했지만, 당연히 백본 LLM도 중요합니다. Agent에서는 특히 사용 가능한 도구를 정확히 이해하고, 오류 상황에서 올바른 행동을 선택하며, 긴 작업을 유지하는 능력을 봐야 합니다. 결국 어떤 모델이 좋은지는 우리의 작업 목표와 비용·지연 제약을 함께 보고 결정해야 합니다.
- **출처:** [R01][R14]

## S17 — Reasoning · Planning · Acting의 관계

- **섹션:** Components · **우선순위:** 선택
- **화면 텍스트**
  - 제목: `추론을 오래 한다고 더 자율적인 Agent가 되는 것은 아닙니다`
  - 세 구역:
    - `Reasoning` — 현재 정보에서 판단/가설 형성
    - `Planning` — 앞으로 수행할 작업 단계 구성
    - `Acting` — 외부 환경에 영향을 주는 행동
  - 하단: `Plan은 바뀔 수 있고, Action은 검증 가능해야 한다.`
- **레이아웃:** 중앙에 원 3개가 일부 겹치는 구조가 아니라, `Reasoning → (optional) Plan → Action → Observation ↺` 실행 순환. Planning을 선택적 노드로 표시.
- **인터랙션:** `가설 A가 틀림` 버튼 → `Plan v1`이 회색으로 바뀌고 `Plan v2` 생성 → 새 도구 선택 경로 표시.
- **발표자 기술 해설:**
  - 추론 모델의 내부 CoT와 앱이 사용자에게 보여주는 계획·행동 로그는 다르다. 내적 추론 과정을 임의로 실제 API의 원문처럼 화면에 나타내지 않는다.
  - 모든 Agent가 명시적 단계별 Plan을 먼저 만들 필요 없음. 반응형(ReAct 계열) 접근과 미리 계획 후 재계획하는 접근은 상황에 따라 선택됨.
  - Planning 오류·사실 오류는 관찰과 검증으로 줄일 수 있지만 완전히 사라지는 것은 아님.
- **대본:**
  > Reasoning은 지금 무엇을 할지 판단하는 능력이고, Planning은 여러 행동을 미리 조직하는 전략입니다. 하지만 현실의 결과가 달라지면 Plan은 바뀌어야 합니다. 행동과 검증이 분리되어야 하는 이유가 여기에 있습니다.

## S18 — State, Context, Memory: 같은 것이 아니다

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `State ≠ Context ≠ Memory`
  - 왼쪽 `STATE` — `실행이 지금 어디까지 왔는가?` / `step=4 · test=FAILED · approval=pending`
  - 가운데 `CONTEXT` — `모델이 이번 호출에서 무엇을 보는가?` / `지시사항 + 최근 이력 + 도구 결과 + 검색 정보`
  - 오른쪽 `MEMORY` — `이후에도 무엇을 보존·다시 찾는가?` / `선호 · 사건 · 업무 지식`
  - 하단: `Memory에 있다고 자동으로 Context에 들어가는 것은 아닙니다.`
- **레이아웃(중요):**
  - S09 `Agent Runtime`의 State 패널을 좌측 아래로 확장, `Context Window`를 중앙 모델 앞의 넓고 길쭉한 박스로 표시, `Memory Store`는 화면 오른쪽 바깥 DB/파일 아이콘으로 표시.
  - Memory → Retrieval 화살표 → Context Window. State → Context Builder → Context Window. Context → LLM. State/Memory/Context 영역 겹쳐 그리지 말고 데이터 이동을 보여준다.
  - 작은 예시 값은 실제로 모델에 들어간 내용과 저장된 내용의 차이가 보이게 구성.
- **인터랙션:**
  1. State `test_failed` 값을 강조
  2. Memory `이전에 성공한 인증 테스트 패턴`을 불러올지 결정
  3. 관련 메모리 하나만 Context에 삽입(나머지는 Store에 남음)
  4. Context가 LLM으로 전달
- **발표자용 개념:**
  - State = 실행 컨트롤 및 데이터 상태(프로그램 변수, 체크포인트, 히스토리). Session은 State의 한 종류/경계로 다뤄질 수 있음.
  - Context = **특정 모델 추론 호출에 실질적으로 공급되는 입력**(텍스트 외 multimodal 요소 포함 가능). 앱 설계에서는 context 정보 집합으로도 느슨하게 부르지만 여기서는 '호출 시 컨텍스트'로 통일.
  - Memory = 장기/단기 정보를 저장·검색·갱신하는 메커니즘. 세션 히스토리를 memory라고 부르는 라이브러리도 많지만, 'State/Context/Memory는 관리 책임이 다르다'는 관점을 유지.
  - 임베딩/벡터DB는 Memory의 선택적 구현 기술일 뿐 필수가 아니다.
- **대본:**
  > 현재 몇 번째 단계인지, 테스트가 실패했는지는 State입니다. 그 내용을 모델에게 전달하도록 편집한 입력이 Context입니다. 지난주에 사용자에게 배운 코드 컨벤션을 저장해두고 나중에 검색한다면 Memory입니다. 실제로는 세 부분이 연결되지만 서로 같은 데이터 구조를 의미하지는 않습니다.
- **출처:** [R01][R08][R09][R10]

## S19 — 멀티턴 세션과 대화 기록은 어떻게 유지되는가?

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `모델이 기억하는 것처럼 보여도, 상태는 시스템이 관리합니다`
  - 좌측 예시 대화:
    - `User: 테스트가 왜 실패하지?`
    - `Agent: 만료 토큰 분기가 문제인 듯합니다.`
    - `User: 그럼 그 부분만 고쳐줘.`
  - 오른쪽 흐름: `Turn 1 → History / State Save → Turn 2 Context Assemble → Model`
  - 하단: `Session continuity ≠ 모델 가중치 변경`
- **레이아웃:** 두 턴을 나란히 카드로 놓고 가운데 `history/state` 저장박스. 아래 `API replay`와 `provider-managed conversation state`를 작은 가지로 표시.
- **인터랙션:** 클릭으로 Turn 1 완료 시 히스토리 저장 → Turn 2 도착 → `그 부분`이 무엇인지 이전 맥락이 Context에 추가되어 해결되는 애니메이션.
- **발표자 기술 해설:**
  - 기본 모델 호출은 이전 앱 요청을 자동으로 전부 알지 못한다. 이전 메시지를 앱이 다시 전달하거나 API가 제공하는 상태/대화 연결 기능을 사용할 수 있다. 예: OpenAI Responses의 `previous_response_id`나 Conversations API 관련 기능(버전별 세부 구현은 문서 확인). [R08]
  - '상태를 서버에서 유지한다'는 것과 '모델 자체의 파라미터에 학습된다'는 것은 다른 개념.
  - 보안·비용·컨텍스트 제한상 이전 대화를 무조건 전부 실어 보내는 것은 비효율적.
- **대본:**
  > 우리가 채팅을 이어갈 때 모델이 기억하는 것처럼 보입니다. 사실 많은 경우 앞선 대화나 상태를 애플리케이션이 저장하고 다음 호출의 Context에 다시 넣는 구조입니다. 이 과정이 대화를 지속시키지만, 방금 한 대화만으로 백본 모델이 자동으로 Fine-tuning되는 것은 아닙니다.
- **출처:** [R08]

## S20 — 장기 메모리: 저장, 검색, 갱신의 3단계

- **섹션:** Components · **우선순위:** 선택
- **화면 텍스트**
  - 제목: `기억하려면 저장해야 하고, 쓰려면 찾아야 합니다`
  - 상단 파이프라인: `Observe` → `Extract` → `Store` → `Retrieve` → `Inject into Context`
  - 세 가지 Memory 예시:
    - `Episodic`: `지난번 실패한 로그인 테스트의 원인`
    - `Semantic`: `프로젝트의 인증 정책`
    - `Procedural`: `이 저장소의 테스트·검증 절차`
  - 하단: `Stored ≠ Retrieved ≠ Trusted`
- **레이아웃:** Memory Store 3개의 서랍을 우측에 두고, 중앙에는 `Relevance filter`가 1개 선택해 Context로 옮기는 모습.
- **인터랙션:** `관련 없는 기억` 버튼 클릭 → 메모리는 Store에 남지만 Context에는 미포함. `오래된 정책` 클릭 → `last_verified`가 오래되었다는 경고와 함께 검증 후 참조하도록 유도.
- **발표자 기술 해설:**
  - 단기 메모리는 대화 히스토리·현재 Context와 겹쳐 사용되는 느슨한 표현. 장기 메모리는 세션을 넘어 저장/검색 가능한 데이터나 지식으로 구분 가능.
  - 저장 구현: 문자열/Markdown 파일, 관계형 DB, KV, Vector DB, 그래프 등. **Vector DB = Memory**는 아님.
  - 쓰기 정책: 누가 무엇을 언제 저장하는지, 근거, 유효기간, 업데이트/충돌, 민감정보 필터링, 삭제 권한.
  - 잘못된 Memory를 재주입하면 오히려 성능이 하락할 수 있음. 복구/가치 검증은 S21·S28로 연결.
- **대본:**
  > Agent에 기억을 붙인다는 것은 DB만 연결한다는 뜻이 아닙니다. 어떤 사실을 저장할지, 언제 찾아올지, 오래되거나 틀린 기억을 어떻게 버릴지도 설계해야 합니다. 특히 장기 메모리는 모델 컨텍스트와 별개의 저장소라고 보는 것이 이해하기 쉽습니다.
- **출처:** [R09][R10]

## S21 — Context Engineering: 더 많이 넣는 것이 답은 아니다

- **섹션:** Engineering · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Context Engineering = 무엇을, 언제, 얼마나 보여줄 것인가`
  - 비교: `Before: 모든 문서/로그/대화 투입` → `After: 필요한 정보 선택 + 요약 + 필요 시 검색`
  - 실행 전략 태그: `Select` `Retrieve` `Summarize/Compact` `Order` `Refresh`
  - 하단: `Context is a finite resource — relevance > volume`
- **레이아웃:** 화면 왼쪽에 토큰 블록이 Context Window에 무차별 쌓이는 그림(붉은 `irrelevant logs`, `duplicate context`). 오른쪽은 색상별로 `Instructions`, `Recent State`, `Relevant Files`, `Tool Results`만 채운 Context Window. 정확한 토큰 수·성능 % 등 근거 없는 정량값 사용 금지.
- **인터랙션:**
  1. `무차별 투입` 버튼 → 유사한 로그 20개가 쌓이고 중요한 오류 메시지가 희미해짐.
  2. `선택/압축` 버튼 → 20개 로그가 `요약 + 원본 경로`로 압축되고, 핵심 실패 1건과 관련 소스만 진하게 남음.
  3. `Just-in-time retrieval` 버튼 → 모델이 특정 파일을 요청했을 때만 내용이 들어옴.
- **발표자 기술 해설:**
  - Prompt Engineering이 '지시를 어떻게 쓰는가'라면 Context Engineering은 '모델이 지금 볼 수 있는 **전체 입력 상태**를 어떻게 설계하는가'.
  - Anthropic은 길어진 입력에서 관련 정보의 품질이 저하될 수 있는 `context rot`와 필요한 자료를 적시에 가져오는 전략을 강조한다. 이는 모든 모델/작업에 일정하게 적용되는 정량 법칙이 아니라 관리상 고려할 위험임. [R10]
  - Compaction은 긴 이력에서 핵심 사실·결정·미해결 항목을 보존해 요약하는 방식. 단, 요약에 중요한 정보가 누락될 수 있어 원본 참조 경로를 유지하는 것이 유리.
  - Prompt caching은 중복 입력 비용/지연 최적화에 도움이 될 수 있지만 **Context를 잘 선택하는 것과 다른 기술**임.
  - 긴 Context Window도 신뢰할 만한 장기 기억 저장소와 동일하지 않음.
- **대본:**
  > Agent가 여러 단계 실행되면 대화, 파일, 로그, 도구 결과가 계속 늘어납니다. 모든 내용을 그냥 넣으면 비용이 커지는 것뿐 아니라 정작 중요한 오류가 묻힐 수 있습니다. 그래서 중요한 정보를 고르고, 요약하고, 필요한 순간 다시 가져오는 것이 Context Engineering입니다.
- **출처:** [R10][R17]

## S22 — Tool, MCP, Skill: 서로 같은 이름이 아니다

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Tool · MCP · Skill — 세 가지 다른 층위`
  - `TOOL` — `모델이 요청할 수 있는 구체적인 기능` / 예: `run_tests(target)`
  - `MCP` — `외부 기능·데이터를 연결하는 표준 프로토콜` / 예: `MCP Server의 tools/list → tools/call`
  - `SKILL` — `특정 작업을 수행하는 재사용 가능한 절차·자료 패키지` / 예: `test-debugging/SKILL.md`
  - 하단: `Tool = Capability / MCP = Connection / Skill = Know-how`
- **레이아웃:** 3열 카드가 아니라 의미 관계 그림을 우선. 왼쪽 Skill(종이 아이콘)에서 모델의 행동 전략을 알려주고, 모델은 Tool을 요청한다. 그 Tool의 **일부가 MCP Client↔Server를 통해 공급**될 수 있다. `Skill ≠ MCP Server ≠ Tool`을 하단에 텍스트로 명시.
- **인터랙션:** S09 참조 아키텍처 위에 세 가지 버튼 `Tool`, `MCP`, `Skill`.
  - Tool 클릭: `run_tests` 함수 인터페이스만 강조.
  - MCP 클릭: Host→Client→Server 연결선을 강조하며 Tool Discovery/Call 예시 노출.
  - Skill 클릭: `SKILL.md` 문서→Context Builder→Model로 불러오는 흐름 강조.
- **발표자 심화 개념:**
  - MCP는 모델/프레임워크 자체가 아니라 애플리케이션(Host)이 MCP Client를 통해 MCP Server와 기능·자료를 교환하는 표준. 핵심 공개 프리미티브에 Tools, Resources, Prompts가 있으며, 이것들이 모두 Tool과 동일한 것은 아님. MCP는 JSON-RPC를 사용하는 프로토콜 계층을 포함한다. [R12]
  - Agent Skills 스펙은 폴더 안 필수 `SKILL.md` 파일, 선택적 `scripts/`, `references/`, `assets/` 등을 정의한다. Skill은 종종 `name`,`description` 메타데이터로 먼저 탐색되고 필요한 시점에 본문을 로드한다. [R13]
  - 특정 제품에서는 'Skill'이나 'Tool'이라는 단어를 더 넓게 쓰기도 한다. 본 발표에서는 위 세 분류로 용어를 합의한다.
- **대본:**
  > 이 세 용어를 구분하는 것이 오늘의 중요한 목표 중 하나입니다. Tool은 사용할 기능이고, MCP는 외부 기능이나 데이터를 연결하는 규약이며, Skill은 어떤 작업을 잘하기 위한 매뉴얼이나 재사용 가능한 작업 패키지입니다. 서로 결합할 수 있지만 같은 계층은 아닙니다.
- **발표 범위 경계 멘트:**
  > MCP의 프로토콜 메시지와 Tool 구현 패턴은 뒤의 Tools 담당자 발표에서 더 자세히 확인하겠습니다.
- **출처:** [R12][R13]

## S23 — 확대해서 보는 Tool Call / MCP / Skill의 관계

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `하나의 행동, 서로 다른 역할`
  - 시나리오: `Agent가 테스트를 수행하려고 한다.`
  - 노드 레이블: `Skill: 디버깅 절차`, `Model: run_tests 선택`, `Runtime: 호출 검증`, `MCP Client`, `MCP Server`, `Test Runner`, `Observation`
  - 하단: `Skill은 어떻게 할지 돕고, Tool은 무엇을 할 수 있는지 제공하며, Runtime은 실제 실행을 책임집니다.`
- **레이아웃:** S09 아키텍처 확대:
  - ① 왼쪽 위 `SKILL.md`: `실패 재현 → 원인 파악 → 최소 수정 → 재검증`.
  - ② 가운데 파랑 Model.
  - ③ 오른쪽 보라 Runtime/Host + MCP Client.
  - ④ 가장 오른쪽 녹색 MCP Server → Test Runner.
  - ⑤ 아래 주황 Observation을 Context로 되돌림.
  - **MCP는 예시일 뿐**. 작은 스위치 `Local Function` / `Via MCP`를 추가하여 같은 `run_tests`가 MCP 없이 로컬 함수로 실행될 수도 있음을 보여줌.
- **인터랙션:**
  1. Skill 내용 일부 Context로 로드(전체 파일이 자동으로 항상 들어가는 연출 X).
  2. Model이 `run_tests` 호출을 구성.
  3. `Via MCP` 모드에서 Host가 연결된 Client를 통해 Server Tool을 호출.
  4. Test Runner 결과가 Server→Client→Runtime→Context를 거쳐 Model로 복귀.
  5. `Local Function` 모드로 바꿔 MCP 경로가 없어도 동일한 Tool Call 개념 성립함을 보여줌.
- **발표자 개념:**
  - 모든 Tool이 MCP를 써야 하는 것은 아니다. MCP는 연결/상호운용성을 표준화하는 선택지 중 하나.
  - 모든 Skill이 반드시 자동 실행 스크립트를 포함하거나 내부에 모든 Tool을 정의하는 것은 아니다.
  - 실제 시스템에서 Tool의 discovery/selection/execution은 구현 방식에 따라 다를 수 있음.
  - MCP Host/Client/Server 3요소는 공식 아키텍처에 따른 용어. [R12]
- **대본:**
  > '테스트 실패 원인을 해결하는 Skill'은 디버깅 절차를 알려줄 수 있습니다. 모델은 그 절차와 현재 상황을 참고해서 `run_tests`를 선택합니다. 그 실제 실행 통로가 로컬 Python 함수일 수도 있고 MCP로 연결된 외부 서버일 수도 있습니다. 이 구조를 구분해 두면 프레임워크별 기능 설명이 훨씬 선명해집니다.
- **출처:** [R03][R12][R13]

## S24 — Framework / SDK와 Harness는 어떤 관계인가?

- **섹션:** Components · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Framework는 개발을 돕고, Harness는 실행을 가능하게 합니다`
  - 비교:
    - `Raw Model API`: `모델 응답을 직접 받아 처리`
    - `Framework / SDK`: `Agent·Tool·상태·실행 흐름의 공통 추상화`
    - `Harness / Runtime`: `모델이 행동할 수 있도록 감싼 실행 환경·제어·피드백 구조`
  - 하단: `관계는 배타적이지 않습니다. SDK가 Harness의 일부를 구현할 수 있습니다.`
- **레이아웃:** 겹치는 투명 영역 표현 대신 레이어 3개. `Application`(최상위) 안에 `Framework/SDK helpers` + `Execution Runtime` + `Policy/Tools/Observability`가 배치되고 가운데 Model. `Harness`는 실행·컨텍스트·권한·도구·상태·피드백을 포괄하는 음영 경계로 설정.
- **인터랙션:** `Without Framework` 버튼을 누르면 Tool Loop를 직접 구성하는 S14 코드 확대, `With Framework` 버튼은 `agent.run(goal)` 형태로 추상화하되 내부의 Runner/State/Tool 단계를 반투명하게 유지하여 **마법처럼 사라진 것이 아니라 감춰진 것**임을 표시.
- **발표자 기술 해설:**
  - Framework는 Agent 구성/Tool 정의/흐름/통합을 위한 개발 추상화. Harness는 제품마다 쓰는 범위가 다르지만 대체로 **Agent를 실행시키고, 환경·권한·관측·반복·컨텍스트를 관리하는 프로그램 전체**에 가깝다. [R14][R15]
  - 예: OpenAI는 관리형 Agents API, 앱에 포함해 실행하는 Agents SDK, 더 낮은 수준의 Responses API 등을 제공한다(정확한 옵션/제품 현황은 [R14] 검토). 이는 누가 Loop와 환경을 운영하는지에 대한 선택 관점.
  - Anthropic의 Agent SDK는 도구, Loop, Context 관리 등의 기능을 제공한다. 다른 프레임워크 비교는 후속 세미나에 양보. [R15]
  - `Harness Engineering`은 특정 SDK를 쓰는 행위와 동일하지 않다. 실행 환경, 관측, 반복 검증 가능성 등을 어떻게 **설계·개선**하는가에 초점을 둔다.
- **대본:**
  > Framework는 구현을 편하게 해주는 추상화입니다. 하지만 그런 프레임워크를 사용하더라도 실행 권한, 컨텍스트, 테스트 환경, 로깅, 실패 처리를 어떻게 운영할지 결정해야 합니다. 이를 포함해 모델이 실제로 일을 하게 하는 환경을 Harness라고 볼 수 있습니다.
- **출처:** [R14][R15][R16]

## S25 — Prompt → Context → Harness Engineering

- **섹션:** Engineering · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `Agent Engineering은 Prompt 밖으로 확장됩니다`
  - 3계층:
    1. `Prompt Engineering` / `모델에게 어떻게 지시할 것인가?`
    2. `Context Engineering` / `어떤 정보를 언제 모델에 줄 것인가?`
    3. `Harness Engineering` / `모델이 행동하고 검증할 환경을 어떻게 만들 것인가?`
  - 하단: `좋은 지시 × 좋은 정보 × 좋은 실행 환경`
- **레이아웃:** 계단형 3층. `Prompt`는 모델 입력 일부, `Context`는 입력 전체, `Harness`는 상호작용과 도구 및 검증을 포함하는 시스템 바깥으로 확장. 상호 배타적인 시대 구분으로 표현하지 말 것.
- **인터랙션(중요):** 같은 모델/같은 요청으로 비교:
  - 버튼 `Prompt only`: '테스트를 신중하게 고쳐'라는 지시문만 강화. 검증 도구/정책 없음.
  - 버튼 `+ Context`: 실제 에러 로그와 관련 파일, 저장소 규칙을 전달.
  - 버튼 `+ Harness`: 격리된 테스트 환경, 자동 테스트, Diff Review, 실행 권한 제한, 피드백 루프 결합.
  - 우측 **정성적 설명**만 바뀜: `추정 중심` → `관련 정보 기반 판단` → `행동 결과를 검증할 수 있는 시스템`. 성공률이나 비용 절감 %를 임의로 기입하지 않는다.
- **발표자 기술 해설:**
  - 3개의 용어는 서로 대체 관계가 아닌 **설계 관심사의 층위**이다.
  - OpenAI의 Harness Engineering 사례는 모델을 더 강하게 만드는 대신 리포지토리 지식의 접근성과 실행 규칙, 자동 테스트, 관측, 피드백 루프 등을 개선해야 성과가 난다는 경험을 다룬다. 이는 특정 조건의 사례이므로 공식 실험 결과를 **일반화된 성능 보장**으로 해석하지 않는다. [R16]
  - `Agent = Model + Harness` 같은 표현은 비유/관점이지 모든 시스템을 빠짐없이 분해하는 보편 수식이라고 주장하지 않는다.
- **대본:**
  > 같은 모델에 '더 열심히 생각해'라고 쓰는 것만으로 해결되지 않는 문제가 많습니다. 어떤 오류 로그와 파일을 보여주는지, 어떤 환경에서 테스트할 수 있는지, 결과를 어떻게 검증할 수 있는지를 바꾸면 실제 작동 방식이 달라집니다. 그래서 Prompt뿐 아니라 Context와 Harness를 같이 설계해야 합니다.
- **출처:** [R10][R16]

## S26 — Guardrails & Human-in-the-loop: 행동의 경계

- **섹션:** Engineering · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `자율성에는 '허용된 행동'의 경계가 필요합니다`
  - 경계 그림:
    - `Read` — `자동 허용`
    - `Test in Sandbox` — `자동 허용`
    - `Edit Allowed Files` — `조건부 허용`
    - `Deploy / Delete / Send` — `사전 승인 필요`
  - 하단: `Validate → Authorize → Execute → Verify`
- **레이아웃:** 화면 중앙 Tool Execution Gate. 왼쪽 Model Tool Call, 가운데 보라 Runtime 게이트(`schema validation`, `path allowlist`, `approval`, `sandbox`), 오른쪽 도구 실행. 아래 별도 Human Approval 분기.
- **인터랙션:** 선택지 `read_file`은 녹색 통과; `apply_patch`는 허용 경로 검사 후 통과; `delete_production_db`와 같은 가상 호출은 **실행되지 않고** 빨간 거부/승인 요청 카드가 뜬다. 실제 삭제 액션/API는 절대 구현하지 않는다.
- **발표자 기술 해설:**
  - Guardrails는 모델에 금지 규칙을 적는 것에 그치지 않는다. 도구 스키마/인수 검증, 권한 확인, 파일/리소스 격리, rate limit, 위험 행동 승인, 결과 검증 등 **모델 바깥의 집행 로직**을 포함한다.
  - Prompt injection: 도구 결과/외부 문서의 문장이 시스템 지시를 덮어쓰도록 만들 수 있으므로, 도구로 수집된 텍스트를 **신뢰하지 않는 데이터**로 취급해야 한다.
  - HITL(Human-in-the-loop) = 사람이 모든 단계에 개입한다는 뜻이 아니라 위험·불확실성 등 특정 조건에서 **승인/수정/중단할 수 있는 설계**.
  - Guardrails가 있더라도 '완전한 보안' 보장 X. 권한 경계를 Runtime에서 집행해야 함.
- **대본:**
  > 모델이 패치를 추천하는 것과, 회사의 운영 DB를 삭제하거나 외부로 메일을 보내는 권한을 갖는 것은 전혀 다릅니다. 어떤 행동은 자동으로 허용하고 어떤 행동은 사람이 승인하도록 나누어야 합니다. 안전 장치는 모델이 아니라 실행 시스템이 실제로 집행할 수 있어야 합니다.
- **출처:** [R14][R15][R16]

## S27 — 실패한 Agent가 스스로 교정하는 과정

- **섹션:** Engineering · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `실패를 관찰하고 고치는 것 ≠ 모델이 학습한 것`
  - 왼쪽 `Naive Retry Loop`: `오류 → 같은 호출 → 같은 오류 → 반복`
  - 오른쪽 `Feedback-driven Recovery`: `오류 감지 → 원인 가설 수정 → 행동 변경 → 독립 검증 → 종료`
  - 아래 구분:
    - `Within-run self-correction` — 현재 State/Context에서 전략 변경
    - `Cross-run improvement` — 검증된 경험을 Memory/Skill/Code에 업데이트
    - `Model learning` — 별도의 훈련·파인튜닝으로 가중치 갱신
- **레이아웃:** 같은 실패에서 갈라지는 두 개의 Loop 도식. 왼쪽은 같은 붉은 화살표가 3회 회전하다 Stop. 오른쪽은 관찰 결과로 다른 녹색 Tool 선택 + 검증 완료. 맨 아래에 장기 개선 파이프라인을 **별도의 점선 박스**로 분리.
- **인터랙션:**
  - 초기 상태: `apply_patch` 뒤 여전히 FAILED.
  - `Naive` 선택: 같은 패치를 두 번 재시도 → `max_steps reached`.
  - `Feedback` 선택: 실패 로그 비교 → 가설 변경 → 다른 수정 후보 → `run_tests` → PASSED(가상 시나리오).
  - `Persist learning` 버튼은 클릭 시 `validated lesson`을 검토 후 Skill/Memory 후보에 반영하는 별도 **비실행 파이프라인**을 보여줌. 'Agent가 즉석에서 가중치를 다시 학습했다'는 장면 금지.
- **발표자 기술 해설:**
  - 한 번의 실행에서 Self-correction은 모델이 결과를 관찰하고 계획이나 도구를 달리 사용하는 것. *반복한다고 항상 더 정확해지는 것은 아님*.
  - 세션 간 재사용은 오류 궤적 기록→원인 분석→교훈/스킬 후보 생성→독립 테스트→승인→배포라는 별도 시스템이 필요.
  - Fine-tuning/사후학습은 가중치를 바꾸는 별도 과정이며 에이전트 반복 호출 중 기본적으로 자동 발생하지 않음.
  - AI Agent Book의 지속적 진화 장은 지식·지시·프로그램·파라미터 **서로 다른 업데이트 경로**를 구분하고, 회귀 검증/릴리스 게이트를 중요하게 본다. [R19]
- **대본:**
  > Agent가 실패를 보고 다음 행동을 바꾸는 것을 흔히 '스스로 학습한다'고 표현하는데, 엄밀히는 구분해야 합니다. 지금 실행 중에 다시 시도하는 것은 자기교정이고, 그 경험을 다음 세션에도 쓰려면 Memory나 Skill, 코드 변경 등 별도의 지속화 설계가 필요합니다. 모델 가중치 학습은 또 다른 과정입니다.
- **출처:** [R19][R11]

## S28 — Trace, Observability, Evaluation: 무엇이 잘못됐는가?

- **섹션:** Engineering · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `최종 답변만 보면 Agent를 디버깅할 수 없습니다`
  - Trace 샘플 레인: `Model Call` → `Tool Call` → `Tool Result` → `State Change` → `Final`
  - 관측 지표: `Task success`, `Tool-call validity`, `Retries`, `Latency`, `Token / Cost`, `Policy violations`
  - 하단: `Trace = 일어난 일의 기록 / Eval = 잘했는지 판단하는 기준`
- **레이아웃:** 가상 디버깅 대시보드. 좌측 이벤트 타임라인 5개, 오른쪽에 두 개의 다른 색 카드: `Observed: test PASSED`, `Needs validation: regression tests not run`. 아래 세 가지 평가 뱃지 `Outcome / Process / Safety`.
- **인터랙션:** 오류가 발생한 `apply_patch` 이벤트 클릭 → 관련 Tool Call 인수/결과/시간/실행 권한 판정이 확장. 다른 탭 `Success` / `Failure` 비교. 수치는 임의 데모임을 작은 워터마크로 표시.
- **발표자 기술 해설:**
  - Trace는 모델 호출, 도구 선택, 인수, 결과, 비용/지연 등을 기록하는 사건 시퀀스. 민감한 원문, 비밀키, 개인정보는 로그에 무조건 저장하지 말고 마스킹/최소화해야 한다.
  - Observability는 실제 실행을 관찰·진단할 수 있는 시스템적 능력. Tracing 외에도 로그·메트릭·알림을 포함.
  - Evaluation은 수행의 **성공 기준과 품질 척도**: 결과 검증(테스트 PASS 등), 경로 검증(권한·도구 사용), 품질 평가. LLM-as-a-Judge는 일부 질적 요소에 유용할 수 있으나, 파일 수정·테스트 성공 여부처럼 객관적 상태로 확인 가능한 것은 실제 검증을 우선.
  - 성공한 최종 답변만 남기고 실패 경로를 버리면 개선 포인트를 찾기 어렵다. 최신 공식 Anthropic 평가 가이드는 멀티턴 Agent 평가에서 환경 상태와 궤적의 중요성을 설명한다. [R11]
- **대본:**
  > Agent는 결과만 보면 왜 성공했는지, 왜 실패했는지 알기 어렵습니다. 어떤 Tool을 어떤 인수로 호출했고, 실행 환경이 무엇을 반환했는지 봐야 합니다. Trace로 실제 진행을 관찰하고, Eval로 그 과정과 결과가 목표를 만족했는지 판단할 수 있습니다.
- **출처:** [R11][R15][R19]

## S29 — Wrap-up: Model이 아니라 시스템을 설계한다

- **섹션:** Closing · **우선순위:** 필수
- **화면 텍스트**
  - 제목: `AI Agent를 이해하는 3가지 문장`
  - `01. Agent는 단일 LLM 호출이 아니라 행동과 피드백을 가진 시스템이다.`
  - `02. 핵심은 Model Decision ↔ Runtime Execution ↔ Observation Loop다.`
  - `03. 실용적인 Agent는 Context · Tools · State · Guardrails · Evaluation을 함께 설계한다.`
  - 하단 작은 멘트: `Next → Tools & Orchestration` 
- **레이아웃:** S09 전체 아키텍처가 선명하게 재등장. 이 위에 번호 01~03이 순서대로 점등되며 각 문장 옆 관련 노드 강조. 마지막에는 전체 구조가 한 번에 노출.
- **인터랙션:** 3단계 요약. 마지막 단계에서 `Tools` 영역과 `Orchestration` 경계가 은은하게 강조되고 다음 발표로 자연스럽게 넘기는 화살표.
- **발표자 대본:**
  > 오늘 제가 말씀드린 핵심은 세 가지입니다. 첫째, Agent를 모델 이름이 아니라 행동할 수 있는 시스템으로 볼 것. 둘째, 그 중심에는 판단·행동·관찰을 연결하는 Loop가 있다는 것. 셋째, 좋은 Agent를 만들려면 Model만이 아니라 Context, 실행 환경, 권한과 평가까지 설계해야 한다는 것입니다. 이어지는 발표에서 오늘의 Tool과 Orchestration 부분을 더 깊게 살펴보겠습니다. 감사합니다.
- **진행 참고:** 이 장에서 **3명 전체 Q&A를 시작하지 않음**. 다른 발표자들의 발표가 끝난 뒤 별도 Q&A 세션 진행. 아래 Q&A 부록을 참고.

---

# C. 발표자 개념 해설 — 슬라이드에 억지로 넣지 말 것

## C-1. 핵심 용어 한 장 정리

| 용어 | 발표에서 사용할 엄밀한 정의 | 흔한 혼동 / 주의 |
|---|---|---|
| LLM | 입력 토큰/멀티모달 정보에 따라 다음 출력과 구조화된 도구 호출 등을 생성하는 모델 | 모델 API 호출만으로 파일이 수정되지는 않음 |
| Agent | 모델이 도구·환경을 활용해 작업을 수행하도록 설계된 시스템 | LLM과 동일한 의미 아님. 행동 범위와 자율성은 구현별 차이 |
| Agentic Workflow | LLM/도구를 포함하면서 사전 정의된 코드 경로로 실행하는 흐름 | LLM을 포함했다고 자동으로 동적 Agent가 되지 않음 |
| Agent Loop | 판단/행동/관찰을 반복해 목표를 수행하는 제어 구조 | 무한 반복해야 한다는 뜻 아님 |
| Tool | 특정 조회 또는 행동 기능에 대한 호출 가능 인터페이스 | Tool Call 메시지와 실제 실행은 다름 |
| Function Calling | 모델이 함수 이름과 인수를 지정하는 구조화 요청을 생성하는 메커니즘 | 앱/호스팅 인프라가 실행 책임을 짐 |
| MCP | 외부 서버의 Tool/Resource/Prompt 등 기능을 연결하는 표준 프로토콜 | 모든 Tool이 MCP 서버를 요구하지는 않음 |
| Skill | 특정 종류의 작업을 수행하는 지시·자료·스크립트 등의 재사용 패키지 | `SKILL.md` 스펙과 제품별 '스킬' 용례 구분 |
| State | 실행 단계와 결과/상태를 나타내는 관리 정보 | Context에 자동으로 모두 들어가는 것이 아님 |
| Context | 특정 모델 호출의 입력으로 구성해 제공하는 정보 | Memory Store에 있는 모든 데이터와 동일하지 않음 |
| Memory | 유용한 정보를 보존·조회·갱신하는 메커니즘 | 반드시 벡터 DB여야 하는 것은 아님 |
| Session | 이어지는 상호작용/실행의 논리적 단위 | 장기 기억과 동일하지 않음 |
| Orchestration | 작업·도구 호출·모델/에이전트 간 흐름과 상태를 조정 | 단일 Agent 내부의 Loop부터 멀티 Agent까지 넓은 용례 |
| Framework/SDK | 반복되는 Agent 구현 기능을 추상화하고 개발 인터페이스 제공 | Harness의 전부라고 단정 X |
| Harness | 모델의 행동을 가능하게 하는 실행·환경·컨텍스트·정책·피드백 인프라 | 학계/제품별 범위가 달라 발표에서 작업 정의 필요 |
| Guardrails | 입력/행동/결과의 안전성·허용 범위를 강제하는 장치 | 시스템 프롬프트만으로 구현 X |
| HITL | 조건부로 사람의 승인·판단·수정을 개입시킴 | 모든 단계 수동 실행을 의미하지 않음 |
| Trace | 호출·결정된 행동·관찰 결과·실행 정보의 기록 | 모델의 비공개 내적 추론 과정을 의미하지 않음 |
| Evaluation | 결과·절차·제약 충족 여부를 측정 | 주관적 점수만으로 완료 여부 판정하면 안 됨 |
| Reasoning | 주어진 정보로 가설·선택 등을 형성하는 모델 능력 | 모델 내부 CoT의 원문을 볼 수 있다는 의미 X |
| Planning | 목표를 이루기 위한 계획/부분 작업 구성 | 모든 Agent에 전용 Planner가 필요한 것은 아님 |

## C-2. `LLM vs Workflow vs Agent`를 더 정확히 말하려면

- **LLM Call:** 주어진 Context에서 답을 생성하는 원자적 작업. 모델은 도구 호출을 제안할 수 있으나 이것만으로 자동적 다단계 실행은 성립하지 않는다.
- **RAG Application:** 검색→LLM이 한 번 작동하는 **고정 파이프라인**이라면 Workflow에 가깝다. 모델이 필요할 때 검색 쿼리를 다시 만들거나 다양한 자료를 선택해 반복 검색한다면 Agentic RAG라고 부를 수 있다.
- **Workflow:** 코드를 통해 선택/분기/병렬 처리할 수 있다. '조건문이 있으면 Agent'가 아님. 조건문의 결과를 누가/무엇이 결정하는지를 보자.
- **Agent:** 목표 해결 경로의 적어도 일부에서 모델의 판단이 실행 흐름에 영향을 준다. 그래도 정책/권한/제약은 코드가 결정할 수 있다.
- **Hybrid:** 현실의 제품에서는 `코드가 큰 Workflow 정의 → 중간 특정 단계에 Agent 삽입 → 다시 Workflow` 같은 혼합 형태가 흔하다.

## C-3. `Agent = LLM + Tools + Memory + Planning` 수식에 대한 주의

이것은 **학습용 구성요소 나열**에 가깝다. 일부 Tool만 가진 단순 Agent에도 유효한 자율 행동이 있고, 장기 Memory/명시적 Planner/MCP는 선택 요소다. 따라서 정의 슬라이드에는 '필수 수학 공식'처럼 두지 않고 `Model + Runtime/State + Optional Tools/Memory + Policy`의 **개념 구성**으로 설명한다.

## C-4. Memory 상세 개념

1. **Working / Short-term:** 현재 작업에 필요한 최근 메시지, 중간 도구 결과, 실행 상태.
2. **Episodic Memory:** 특정 작업에서 무엇이 일어났는지 (`지난번 테스트 수정 사건`).
3. **Semantic Memory:** 지속적인 사실, 저장소 구조/사용자 선호 등 (`CI는 특정 Python 버전 사용`).
4. **Procedural Memory:** 재사용할 절차 (`실패 테스트를 재현하고 수정 후 회귀 테스트`).
5. **Storage와 인지 유형은 독립:** 하나의 Markdown 문서에 의미 기억을 저장할 수도, RDB에 일화 기억을 저장할 수도 있다.
6. **Write path:** 후보 사실 추출→민감도/중복 확인→근거/타임스탬프 기록→저장.
7. **Read path:** 현재 작업과의 관련성 판단→검색→출처/신뢰성 확인→Context에 선별 주입.
8. **Maintenance:** 업데이트, 충돌 해결, 만료/삭제, 오래된 정책 검증, 비용 관리.

## C-5. Context Engineering 실무적 논점

- 많은 도구를 한번에 모델에 공개하면 선택이 혼란스러워질 수 있다. **Tool Description**과 검색/선택 전략도 Context의 일부다.
- `Context Window`와 `max output tokens`, `reasoning budget`, `API 캐싱 비용` 등은 서로 관련되지만 같지 않다.
- `Compaction`은 요약본으로 교체하고 원본 파일 위치를 보존. 요약 과정에서 사실이 손실되는 위험이 있으므로 중요한 결정/미해결 항목을 구조화 보관.
- `Just-in-time retrieval`: 파일 경로/키를 보유하고 실제로 필요할 때만 전체 내용을 읽기. 대규모 저장소/로그에서 특히 유용.
- `RAG`는 Context를 공급하는 방식이며, Agent가 어떤 검색을 할지 결정하는 구조와 결합 가능.

## C-6. Tool Schema, 실행 검증, 오류 분류

모델이 `run_tests({"target":"tests/test_login.py"})`를 제안하더라도 Runtime은 최소한 다음을 점검해야 한다.

```text
schema valid?
  ↓ yes
function allowed for this user/session?
  ↓ yes
arguments safe and path in allowlist?
  ↓ yes
side effect needs approval?
  ↓ no
execute with timeout / resource limit
  ↓
observe stdout / error / duration
  ↓
record result + return to model
```

- **Retryable error:** 네트워크 일시 오류, rate limit 등 정책상 재시도 가능한 실패 → 제한된 백오프.
- **Non-retryable error:** 스키마 오류, 권한 거부, 존재하지 않는 리소스처럼 재시도로 해결되지 않는 실패 → 인수 수정/정책 안내/사람에게 이관.
- **Task failure:** 도구 호출 자체는 성공했지만 목표는 실패 (`run_tests`가 정상 실행되었으나 테스트 FAIL).
- **False success:** 모델은 '완료'라고 말했지만 실제 환경상 상태가 바뀌지 않았음 → 실제 환경 상태 검증 필요.

## C-7. Harness Engineering이 실제로 바꾸는 것

- **Legibility:** 모델이 구조/규칙/문서/오류를 읽고 이해할 수 있게 노출.
- **Actionability:** 실행 가능한 도구와 샌드박스 제공.
- **Verifiability:** 테스트, 린트, 스키마 검사, diff 및 승인 절차.
- **Boundaries:** 네트워크, 파일, 권한, 예산·횟수, 위험 행동 제약.
- **Feedback:** 결과를 안정적으로 수집·정규화해 다음 호출에 제공.
- **Debuggability:** Trace와 평가로 어느 단계가 병목인지 파악.

OpenAI Harness Engineering 글의 중심 사례는 실제 팀이 작업 환경과 규칙·테스트·지식 접근 방식을 정비해 Agent의 생산성을 높인 경험이다. 글에 등장하는 코드 라인 수, PR 수 등은 **그 팀·그 기간의 관찰치**로만 제시할 수 있으며 다른 조직의 기대 성능으로 일반화해서는 안 된다. [R16]

## C-8. 자기교정 vs 자기개선 vs 모델 학습 비교

| 구분 | 변경되는 것 | 유효 범위 | 검증 방법 |
|---|---|---|---|
| Self-correction | 이번 실행의 가설/계획/행동 | 현재 실행 | 재실행 결과·Tool 결과 |
| Memory update | 저장소에 보관할 사실/경험 | 다음 세션에도 사용 가능 | 근거·수명·재검색 정확성 |
| Skill/Prompt update | 재사용 규칙·절차 | 새 배포 또는 다음 실행 | 회귀 테스트·사람 승인 |
| Tool/Harness code update | 실행 프로그램/정책 | 배포된 런타임 | 코드 리뷰·테스트·릴리스 게이트 |
| Fine-tuning/Post-training | 모델의 파라미터 | 새로운 모델 버전 | 별도 학습·독립 평가 |

'스스로 발전했다'라는 표현이 나오면 반드시 **어느 계층이 갱신되었는가?**라는 질문으로 구체화한다. [R19]

---

# D. 3명 전체 발표 후 Q&A 대비

> 이 섹션은 **발표 슬라이드에 포함하지 말고** 발표자 노트 또는 비공개 부록으로 유지. 특정 프레임워크 비교/Serving에 관한 질문은 담당 발표자와 연결한다.

### Q01. LLM이 여러 번 호출되면 모두 Agent인가?

아니다. 여러 호출을 고정 코드 순서로 잇는 것은 Workflow일 수 있다. 모델이 관찰에 따라 다음 행동·도구를 동적으로 선택하는 정도가 구분 포인트다. 다만 실무에서는 혼합형이 많다.

### Q02. Tools를 한 번만 쓰는 것도 Agent인가?

가능하다. 다회 Tool Call이나 영구 루프가 필요조건은 아니다. 다만 Tool을 자동으로 호출해 준다는 사실만으로 자율 Agent라고 단정할 수도 없다. **동적 선택, 행동, 환경 피드백의 통합**이 핵심이다.

### Q03. RAG는 Agent가 아닌가?

고정된 검색→답변 생성 구조는 Workflow/LLM 앱에 가깝다. 모델이 필요할 때 검색·재검색·다른 데이터 소스 선택을 스스로 결정한다면 Agentic RAG로 설계할 수 있다.

### Q04. MCP와 Function Calling의 가장 큰 차이는?

Function Calling은 **모델이 구조화된 도구 호출을 생성하는 메커니즘**, MCP는 **호스트 애플리케이션과 외부 서버 간의 도구/리소스/프롬프트 발견 및 호출 규약**이다. Function Calling만으로 로컬 도구를 쓸 수 있고, MCP Server가 제공한 Tool을 모델의 호출 가능 목록에 연결할 수도 있다.

### Q05. Skill과 Tool은 어떻게 다른가?

Tool은 실행 가능한 기능 인터페이스, Skill은 특정 업무 수행 방법과 필요 자료를 담는 재사용 패키지다. Skill 내부의 스크립트를 Tool로 실행할 수 있으나 둘은 동일 개념이 아니다.

### Q06. Framework와 Harness는 서로 대체재인가?

아니다. Framework는 구현 추상화이고, Harness는 모델이 도구·환경·피드백과 상호작용하도록 감싸는 실행·운영 체계다. SDK가 일부 Harness를 제공할 수 있고, 조직이 나머지 정책/검증/배포 구조를 추가할 수 있다.

### Q07. Agent가 대화 내용을 기억하는 원리는?

대화/State 저장 후 다음 모델 호출 Context에 관련 부분을 포함한다. 어떤 API는 이전 응답 연결/세션 기능을 제공한다. 모델 가중치가 실시간 업데이트되는 것과는 다르다.

### Q08. Context 길이가 충분하면 장기 Memory는 필요 없나?

둘은 목적이 다르다. 긴 Context도 일정 제한과 비용이 있고, 오래되거나 중요한 정보를 세션 간 지속적으로 관리·검색·업데이트하는 일은 별도 저장/Memory 설계가 필요하다.

### Q09. Reasoning Model만 쓰면 더 좋은 Agent인가?

모델의 판단 능력이 중요하지만 단일 기준은 아니다. 도구 스키마, 권한, 검색 품질, 검증 환경, 지연·비용, 실패 복구 등을 함께 평가해야 한다. 모델 선택은 작업 유형마다 달라진다.

### Q10. 모델이 Tool 실행을 직접 하는 것 아닌가?

일반적인 Tool Call 구조에서는 모델이 이름·인수 등 **실행 요청**을 출력하고, 호스트/관리형 Runtime이 검증·실행한다. UI에서 'Agent가 실행했다'는 말은 시스템 전체에 대한 편의 표현이다.

### Q11. Agent가 테스트 실패 후 패치를 다시 고쳤다면 학습한 것인가?

현재 실행의 로그를 참고해 행동을 바꿨다면 자기교정이다. 다음 세션에도 남는 개선은 Memory/Skill/코드 등에 지속화하고 독립적으로 검증해야 한다. 모델 가중치 학습은 별도 과정.

### Q12. Agent가 진짜로 성공했다고 어떻게 판단하나?

가능하면 **외부 환경에서 검증 가능한 상태**를 확인한다. 코드면 테스트 및 diff, API면 실제 변경된 데이터, 사용자 의도와 정책 준수 등. 최종 문장만 보고 성공 처리하지 않는다.

### Q13. Human-in-the-loop를 넣으면 자율 Agent가 아닌가?

아니다. 승인·권한은 Agent의 **자율성 범위**를 정하는 요소다. 위험한 행동만 승인받고 나머지는 자동 수행하는 형태도 일반적이다.

### Q14. Agent가 Prompt Injection에 취약한 이유와 방어는?

외부 문서·Tool Result 같은 비신뢰 데이터를 모델 Context에서 읽기 때문이다. 신뢰 경계 구분, 도구 권한 최소화, 출력 검증, Sandbox, 사용자 승인, 예외 탐지가 필요하다. 모델에게 '무시하라'고 지시하는 것만으로 충분하지 않다.

### Q15. Loop가 오히려 비용만 늘리는 것은 아닌가?

가능하다. 불필요한 Agent 대신 단일 호출/Workflow를 쓸 수 있고, 모델 호출·재시도·컨텍스트·도구 비용을 관리해야 한다. 성공률 대비 비용/시간이 좋아지는지 평가하는 것이 중요하다.

### Q16. Trace가 있는데 Evaluation도 필요하나?

Trace는 '무슨 일이 있었나'의 기록이고 Evaluation은 '목표에 비추어 잘했나'의 판단이다. 기록만으로 성공 판단 규칙이 생기지 않으며, Eval만 있으면 원인 분석이 어렵다.

### Q17. ReAct, Plan-and-Execute, Reflection을 설명하지 않는 이유는?

오늘은 실행 메커니즘의 공통 최소 단위와 용어 합의를 목표로 한다. Planning/Reflection 패턴은 그 위에 얹히는 전략이며, 상세한 패턴 비교는 Orchestration 파트에서 다루는 편이 자연스럽다.

### Q18. 어떤 프레임워크부터 배우는 게 좋나?

이 세미나에서는 특정 프레임워크 추천·우열은 판단하지 않는다. 먼저 Raw API로 Tool Loop/상태/종료 조건이 무엇인지 이해한 후, 각 프레임워크가 무엇을 감추고 무엇을 제공하는지 평가하는 것이 좋다. 실제 비교는 2차 세미나 범위.

### Q19. 멀티 에이전트가 단일 Agent보다 강력한가?

작업 분해/전문성/병렬성 장점이 있을 수 있지만 통신 비용·오류 전파·상태 관리 부담도 늘어난다. 항상 우수하다고 주장할 수 없다. Orchestration 담당 파트에서 비교하면 좋다.

### Q20. vLLM/SGLang 같은 Serving Framework와 Agent Framework의 차이는?

Serving Framework는 모델 추론 요청을 효율적으로 제공/스케줄링하는 데 초점을 두고, Agent Framework는 모델을 중심으로 Tool/State/실행 흐름을 구성한다. 시스템에서 서로 연결될 수 있지만 해결 문제가 다르며, 서빙 내부 최적화는 2차 세미나 범위.

### Q21. 가장 먼저 평가해야 할 지표 3개는?

업무 완수율(Task Success), 허용된 방식으로 완수했는지(Process/Policy Validity), 비용/지연(Operational Efficiency)이다. 고위험 도메인은 안전 위반율을 별도 핵심 지표로 둔다.

### Q22. 지금까지 정리한 개념에서 Agent의 핵심 1개만 고르면?

**관찰을 토대로 다음 행동이 달라지는 제어 구조**. 모델의 판단만 강조하면 외부 실행을 놓치고, Tool만 강조하면 동적인 의사결정을 놓친다. 둘의 왕복이 중요한 공통 메커니즘이다.

---

# E. 실제 HTML 인터랙션 구현 명세 (구현자용)

## E-1. 파일·컴포넌트 권장 구조

```text
seminar-slides/
  index.html
  src/
    app.tsx                    # 또는 동등한 JS 엔트리
    data/slides.ts             # S00~S29 메타데이터
    data/traceScenario.ts      # trace_v1 / trace_failure 고정 샘플
    components/SlideFrame.tsx
    components/SpeakerNotes.tsx
    components/AgentArchitecture.tsx
    components/LoopSimulator.tsx
    components/SequenceDiagram.tsx
    components/CodeCompare.tsx
    styles/tokens.css
  public/
    (필요 시 로컬 아이콘/이미지)
```

프레임워크는 구현자 판단(React·Vue·Vanilla JS 등)으로 선택. **HTML 결과물 자체가 최종 목표**이며, 별도 백엔드나 API Key 없이 발표 기능이 모두 동작해야 한다.

## E-2. 전역 상태 예시

```ts
type PresentationState = {
  currentSlide: number;        // 0..29
  buildStep: number;           // 0..slide.buildSteps.length
  notesOpen: boolean;
  reducedMotion: boolean;
  activeExample: 'success' | 'failure';
  simulatorPlaying: boolean;
  simulatorIndex: number;
};
```

## E-3. 시뮬레이터 이벤트 모델

```ts
type TraceEvent = {
  id: string;
  index: number;
  actor: 'user' | 'model' | 'runtime' | 'tool';
  action: string;
  payloadPreview: string;
  result?: 'success' | 'failure' | 'pending';
  highlightNodeIds: string[];
};
```

같은 `trace_v1` 이벤트 데이터를 S10/S11/S13/S27/S28에서 재사용한다. 예를 들어 T1을 표시할 때 **어느 슬라이드에서든** Model→Runtime 호출이 강조되어야 한다. S27에서만 `trace_failure`로 갈라지는 것은 명시적 스위치로 관리한다.

## E-4. 인터랙션 상태 전이

```text
NORMAL SLIDE
  Next: if buildStep < maxStep -> advanceBuild
        else -> navigateToNextSlide
  Prev: if buildStep > 0 -> rewindBuild
        else -> navigateToPreviousSlideAtLastBuild

SIMULATOR (S10/S13/S27)
  Idle --Play--> Playing --Pause--> Paused --Play--> Playing
  Playing --End--> Finished --Reset--> Idle
  Any --Step--> PausedAtNextEvent
```

- 방향키가 Simulator 이벤트를 다음으로 넘기는 중에도 슬라이드 전체를 곧바로 넘겨버리지 않게 이벤트 우선순위 관리.
- `Escape`는 오버레이/노트/전체화면 닫기, `N`은 노트 열기, `R`은 현재 인터랙션 초기화.
- 시각 효과는 결과 이해를 돕는 경우만 사용. 슬라이드 전환 0.3초를 넘겨 발표자를 기다리게 하지 않는다.

## E-5. 반드시 검사할 테스트 항목

1. 모든 슬라이드 번호·목차·다음/이전 이동 일치.
2. 오프라인으로 실행해도 주요 애니메이션/도식 보임.
3. S11에서 Tool Call은 **모델 출력**, 실제 실행은 **Runtime/Tool Executor**로 나타남.
4. S18에서 Memory Store의 전체 데이터가 Context에 자동으로 복사되는 연출이 없음.
5. S23에서 MCP 없이 로컬 Tool을 쓰는 모드를 정상 표시.
6. S27의 수정·재시도는 모델 자체의 파라미터 학습으로 표현되지 않음.
7. 시뮬레이션에서 위험한 삭제/배포 등의 실제 실행 없음.
8. 코드 블록 가독성, 발표 화면 16:9, 1280x720에서도 텍스트 겹침 없음.
9. 스피커 노트가 청중 일반 화면에 자동 표시되지 않음.
10. S00~S29 모든 슬라이드 제목/레이아웃/메시지를 MD와 대조 검수.

---

# F. 조사·참고자료와 적용 범위

> 아래는 외부 문헌에 기반한 슬라이드 개념을 검증할 수 있도록 붙인 원문 출처다. 자료 내용을 장황하게 복사하지 않고, 정의·설계 포인트를 **발표자가 설명할 수 있도록 재구성**했다.  
> **검증 범위 고지:** OpenAI/Anthropic/MCP/Skills 공식 웹문서와 공개된 AI Agent Book의 관련 장은 직접 확인했다. YouTube 3편은 공식 공개 소개, 챕터/타임스탬프, 공개 강의 설명 및 일부 외부 요약을 근거로 핵심 학습 포인트를 반영했으나, **전체 영상의 음성과 전체 자막을 전부 직접 시청·대조한 것은 아니다**. 따라서 영상에 '이 문장을 직접 말했다'는 식의 확인되지 않은 인용은 사용하지 않았고, 시간 정보도 확인 가능한 공개 챕터만 사용한다. 로그인/동적 콘텐츠인 Claude Academy 내부 강의 전편도 직접 열람한 것으로 취급하지 않는다.

## F-1. 1차 공식 자료 · 최우선

- **[R01] OpenAI — Building agents (교육 트랙)**  
  URL: https://developers.openai.com/tracks/building-agents  
  활용: Introduction 정의, Core concepts(모델/도구/상태·메모리/오케스트레이션), Reasoning 모델 선택, Responses API와 Agents SDK의 차이. S02, S04, S09, S14, S16.
- **[R02] Anthropic — Building effective agents (2024-12-19; 웹 내용 최신 수정 가능)**  
  URL: https://www.anthropic.com/research/building-effective-agents  
  활용: Workflow/Agent 아키텍처 구분, 가장 단순한 구조 우선, 유연성과 예측 가능성/비용의 Trade-off. S04, S07.
- **[R03] ACM TechTalks — Inside an LLM Agent: A From-Scratch Walkthrough (2026-06-04)**  
  소개: https://on.acm.org/t/inside-an-llm-agent-a-from-scratch-walkthrough/3528  
  동영상: https://www.youtube.com/watch?v=QwJnUkA8uIU  
  공개 강의 설명에 근거한 구성: Tool abstraction, Processing Loop, MCP integration, Agent Skills, Memory 예고. S04, S10, S13, S14, S23.
- **[R04] Tech With Tim — How AI Agents Actually Work (Every Piece Explained & Built) (2026-09-03)**  
  URL: https://www.youtube.com/watch?v=HzGOWq5UyjY  
  공개 챕터: `01:07 AI Model vs AI Agent`, `02:27 Harness`, `03:40 MCP Servers`, `04:45 Skills`, `05:36 Sandbox`, `06:41 Production Layer`, `08:03 Building Agents`, `16:55 Deploying`, `17:52 Benchmarks`.  
  활용: LLM과 실행 환경의 차이, Harness·Skill·MCP·Sandbox 관계. S09, S24, S26. 설명에 나오는 '모델이 전체의 n%' 같은 수치는 **임의 정량 사실로 인용하지 않음**.
- **[R05] OpenAI — Function calling 공식 문서**  
  URL: https://developers.openai.com/api/docs/guides/function-calling  
  활용: Tool Schema 전달 → Tool Call 수신 → App-side 실행 → Tool Output 반환 → 후속 모델 응답. S11, S12, S14.
- **[R06] freeCodeCamp / KodeKloud — AI Agents for Beginners, OpenClaw Case Study (2026-07-07)**  
  URL: https://www.youtube.com/watch?v=AZDSpS5v57w  
  공개 챕터 기준: `00:17:54 Token Economics & Context`, `00:45:01 Multi-turn History`, `00:51:08 Tool Schemas & Execution Loops`, `00:58:20 Workflows vs Agents`, `01:08:16 Perceive–Reason–Act`, `01:13:15 While Loop`, `01:21:13 Guardrails`, `01:26:19 Memory Managers`, `01:43:08 Production Failures`, `02:30:44 Evals`, `02:39:30 Observability`, `02:51:55 Security`.  
  활용: S10, S13, S18, S20, S26~S28. 전체 OpenClaw 코드베이스 분석/실습 시연은 3차 범위라서 제외.

## F-2. 개념·엔지니어링 심화

- **[R07] Anthropic — Building effective agents (Loop/Feedback 관련 부분)**  
  URL: https://www.anthropic.com/research/building-effective-agents  
  활용: Agent/Workflow의 단순한 구성과 피드백 구조. S10, S13.
- **[R08] OpenAI — Conversation state 공식 문서**  
  URL: https://developers.openai.com/api/docs/guides/conversation-state  
  활용: 다회차 문맥의 저장·연결 방식을 모델 가중치 학습과 구분. S18, S19.
- **[R09] AI Agent Book (한국어판) — 사용자 메모리와 지식 베이스**  
  URL: https://github.com/bojieli/ai-agent-book/blob/main/book-ko/chapter3.ko.md  
  활용: 세션/사용자 메모리/비즈니스 상태, 일화/의미/절차 메모리, 저장/검색의 구분. S18, S20.
- **[R10] Anthropic — Effective context engineering for AI agents**  
  URL: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents  
  활용: Context rot, 유효 Context 선택, Just-in-time retrieval, 압축. S18, S21, S25.
- **[R11] Anthropic — Demystifying evals for AI agents (2026-01-09)**  
  URL: https://www.anthropic.com/research/demystifying-evals-for-ai-agents  
  활용: Agent 평가, Multi-turn 환경 상태, Grader와 실제 Task 결과 구분. S13, S27, S28.
- **[R12] Model Context Protocol — Architecture overview (2026 문서)**  
  URL: https://modelcontextprotocol.io/docs/learn/architecture  
  활용: Host–Client–Server, Tools/Resources/Prompts, Protocol 범위. S22, S23.
- **[R13] Agent Skills — Specification**  
  URL: https://agentskills.io/specification  
  활용: `SKILL.md`, 선택적 스크립트/레퍼런스/자산 구조. S22, S23.
- **[R14] OpenAI — Agents and Runtime options**  
  URL: https://developers.openai.com/api/docs/guides/agents  
  활용: Responses API / Agents SDK / 관리형 Agents API의 역할 분담, 관리형 Harness. S09, S16, S24, S26.
- **[R15] Anthropic — Agent SDK overview**  
  URL: https://code.claude.com/docs/en/agent-sdk/overview  
  활용: Agent Loop, Tool, Session, Sandbox, Permission, Observability 등 SDK의 범위. S24, S26, S28.
- **[R16] OpenAI — Harness engineering: leveraging Codex in an agent-first world (2026-02-11)**  
  URL: https://openai.com/index/harness-engineering/  
  활용: Repo Knowledge Legibility, 자동 검사, 피드백 루프, 환경 설계. S24, S25, S26.
- **[R17] Claude Code — Best practices**  
  URL: https://code.claude.com/docs/en/best-practices  
  활용: 컨텍스트 관리, 검증 가능 환경, 행동 권한 및 세션 관리 관점. S21.
- **[R18] AI Agent Book 한국어판 — 구성 및 장별 안내**  
  URL: https://github.com/bojieli/ai-agent-book/blob/main/docs/ko/README.md  
  1장: https://github.com/bojieli/ai-agent-book/blob/main/book-ko/chapter1.ko.md  
  2장: https://github.com/bojieli/ai-agent-book/blob/main/book-ko/chapter2.ko.md  
  활용: 하네스 요소, 컨텍스트 설계, Tool·Memory·평가로 확장되는 개념의 전체 지도. S09, S21, S24.
- **[R19] AI Agent Book 한국어판 — 에이전트 지속적 진화**  
  URL: https://github.com/bojieli/ai-agent-book/blob/main/book-ko/chapter8.ko.md  
  활용: 실행 내 자기교정 vs 경험 영속화 vs 모델/프로그램 업데이트, 테스트·승인·릴리스 게이트. S27, S28. **저장소가 갱신되면 장 번호가 바뀔 수 있으니 제목과 경로로 식별.**

## F-3. 사용자가 제공한 추가 교육 과정

- **Claude Academy — Claude Platform 101**  
  https://academy.claude.com/ko/courses/claude-platform-101  
  공개 강좌 목록: https://academy.claude.com/courses  
  공개 소개: 모델/API 사용에서 시작해 플랫폼의 기반을 소개하는 입문 강좌. 학습 플랫폼의 로그인·동적 강의 본문이 브라우징 환경에서 완전히 펼쳐지지 않아 **내부의 모든 레슨을 읽었다고 주장하지 않음**. 발표 개념의 1차 검증은 OpenAI/Anthropic 공식 개발 문서로 수행.
- **Claude Academy — Build with Claude 컬렉션**  
  https://academy.claude.com/collections/build-with-claude  
  사용자 제공 `academy.openai.com/collections/build-with-claude`는 제공 주체와 도메인이 불일치하므로 위 Anthropic 강좌 링크를 참고할 것. 공개 강좌 페이지에서 Claude Code, API, MCP, Skills 교육 범위를 확인.
- **AI Agent Book 프로젝트**  
  위 [R18] 링크. 사용자가 적은 `ai-agnet-book`은 철자 오기이고 확인된 저장소 이름은 **`ai-agent-book`**.

## F-4. 특정 자료에서 발표로 직접 가져온 아이디어 출처 매핑

| 발표 요소 | 참고 근거 |
|---|---|
| Agent 정의의 차이 | OpenAI [R01] + Anthropic [R02] |
| Workflow/Agent 제어권 대비 | Anthropic [R02], freeCodeCamp 공개 챕터 [R06] |
| Raw Tool Loop와 의사코드 | ACM 강의 소개 [R03], OpenAI Function Calling [R05] |
| Agent 구성요소에 Harness/Sandbox 결합 | Tech With Tim 공개 챕터 [R04], 공식 Runtime 문서 [R14][R15] |
| State/Session/Memory 차이 | OpenAI Conversation state [R08], AI Agent Book [R09] |
| Context Rot/Compaction/JIT | Anthropic [R10] |
| Tool/MCP/Skill 구별 | MCP [R12], Agent Skills [R13] |
| Context → Harness Engineering | Anthropic [R10], OpenAI [R16] |
| Guardrail/권한/환경 검증 | OpenAI [R16], Anthropic SDK [R15] |
| 자기교정 vs 지속적 진화 | AI Agent Book [R19] |
| Trace와 Eval의 상보성 | Anthropic Eval Guide [R11] |

---

# G. 최종 제작 전 발표자·구현자 공동 체크

- [ ] 화면에 보이는 모든 주요 주장은 위 자료로 확인되거나 **예시/견해**라고 구별되어 있는가?
- [ ] `Agent`를 무조건 더 나은 선택으로 추천하지 않았는가?
- [ ] Loop가 어떻게 구성되고 동작하는지 **S10 → S11 → S12 → S13 → S14**에서 점진적으로 이해되는가?
- [ ] S09의 아키텍처 도형이 S18/S22/S23/S24에서도 색과 노드 이름이 일관되게 재사용되는가?
- [ ] State/Context/Memory에 서로 다른 용어와 데이터 흐름이 사용되는가?
- [ ] Tool/Skill/MCP가 잘못된 포함 관계로 표현되지 않았는가?
- [ ] 모델의 비공개 추론 과정을 실제 기록처럼 표현하지 않았는가?
- [ ] S26 위험한 행동은 절대 실제 API/시스템에 연결되지 않는가?
- [ ] S27 자기교정을 모델 학습이라고 부르지 않는가?
- [ ] 숫자가 등장하는 로그/사례는 `가상 시나리오`임을 표시하는가?
- [ ] 첫 번째 세미나의 다른 발표자 범위(Tools/Orchestration)와 2·3차의 상세 구현을 침범하지 않는가?
- [ ] S29 이후 일반 청중용 별도 Q&A 슬라이드를 임의로 끼우지 않고, 3명의 발표가 끝난 뒤 Q&A를 진행하도록 안내하는가?
- [ ] Q&A 부록과 참고자료는 발표자만 접근 가능한가?
- [ ] 발표 시간에 따라 선택 슬라이드를 삭제하더라도 논리 흐름과 링크가 유지되는가?

**이 문서의 최종 역할:** 특정 Framework의 사용법 튜토리얼이 아니라, Agent의 정의와 실행 메커니즘을 기술적으로 정확하고 시각적으로 이해하기 쉽게 제시할 **슬라이드 설계 원본**이다. 구현자는 화면만 예쁘게 그리는 것이 아니라, 위 메시지와 주체·흐름의 정확성을 유지하는 것을 최우선으로 할 것.
