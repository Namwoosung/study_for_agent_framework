# Agent Framework 세미나 2차 — 실제 실행 구조와 개발 책임

> 발표의 도달점은 실행 구조를 읽고 도구 권한, 상태 저장, 업무 검증과 복구를 설계하는 것입니다. 끝의 S44·S45는 현재 발표에서 검증 체크포인트와 개발 질문으로 구성합니다.

> **현행 발표 순서**
> Hermes 루프는 호출 조건과 요청 준비(HLOOP), 응답 처리와 다음 실행(HTRACE), 중단·예산·오류(HEXIT)로 나눕니다. Prefix 재사용은 모델 입력 다음, 압축은 세션 검색 다음, 병렬 Tool은 Tool 오류 처리 다음에 설명합니다. PydanticAI는 Core 구성 → 앱 코드 → Graph → 모델 입력과 대화 → Tool 검증·병렬 실행 → 출력 정책 → Capability·승인 → 선택 Harness 순으로 진행합니다. 선언 변환과 3회 응답 예시는 각각 코드와 Graph 장에 통합했습니다. 아래 S 번호는 원 설계의 식별자이며, 현재 발표 페이지는 manifest의 순서를 따릅니다.


> **용도:** 1차 blueprint의 문서 구조·디자인을 유지한 HTML 슬라이드 제작 지시서 및 발표자 해설·대본·Q&A.  
> **기준일:** 2026-11-03. Markdown 설계 완성본. HTML·Demo·프록시 서비스·실제 Trace는 아직 제작하거나 실행하지 않았다.  
> **내용 기준:** [2차 발표 흐름](flow.md). 그 안의 추가 질문·검증 요청을 공식 문서/소스로 보강했다. 종합 비교 문서나 이전 2차 안을 내용 원본으로 승격하지 않았다.  
> **형식·디자인 기준:** [1차 slide blueprint](../../../archive/presentations/seminar-1/blueprint.md). 원본은 보존한다.  
> **실행 계획:** [작업 순서](../../../archive/presentations/seminar-2/planning/execution-plan.md). 본 문서가 이번 요청의 최종 blueprint다. 기존 2차 설계안들과 혼합하지 않는다.  
> **전제:** 청중은 1차 Introduction/Core/Tools/Orchestration을 이수했다. 일반 Agent 정의나 범용 Tool Loop 강의를 반복하지 않는다.

---

# A. Claude를 위한 구현 지침 — 가장 먼저 읽을 것

## A-1. 결과물 형태

1. 단일 웹앱, 16:9, **한 화면=한 슬라이드**. 마우스·`←/→`·`Space`·번호 점프로 탐색. 스크롤로 다음 장이 노출되지 않는다. 1920×1080 stage를 비례 축소한다.
2. `S00`–`S45` 안정 ID를 사용한다. S39–S42는 네 SDK의 이전 ID이며 빌드에서 각각 새 주제 첫 장으로 연결한다. 현재 본편은 172장이다. 안정 ID와 표시 번호는 분리한다.
3. `title`, `onScreen`, `visual`, `buildSteps`, `speakerNotes`, `sourceRefs`를 분리한다. 아래 ‘화면’과 도식 레이블만 청중 화면에 넣는다. 대본·긴 해설·구현 지시는 노트로 보낸다. 핵심 조건을 숨겨 주장이 달라지게 하지 않는다.
4. **A~G 문서 구조와 타이틀·인사·로드맵·전체 지도·확대도·시퀀스·코드 비교·종합의 레이아웃 문법을 유지**한다. 장수·기술 순서·세부 내용은 2차 원문에 맞춘다.
5. 도식은 SVG/CSS+텍스트. 기술별 master architecture를 먼저 보여준 뒤 동일 node ID·좌표를 확대한다. 실제 구현의 단순화 지도와 설계 예시를 구별한다.
6. `→`/`Space`는 남은 build부터 진행하고 마지막 이후 다음 장. `←`는 역순. 작은 `k/n`은 유지한다. 비교 모드 토글·학습용 드롭다운·hover 정의·자동 시뮬레이터 버튼은 제거하고 **동시 표시+순차 강조**로 바꾼다.
7. `N` 노트·`Escape` 닫기·번호 점프·Reduced motion은 발표 제어이므로 유지한다. 노트 기본 비공개. 별도 발표자 창/노트 파일을 제공하여 청중 공유 창에 대본이 노출되지 않게 한다.
8. 슬라이드는 API key 없이 로컬 자산과 설명용 고정 도식으로 동작한다. 실제 Hermes/PydanticAI 실행은 **별도 Demo 페이지**다. Space로 기록을 살피는 동작과 Agent 실행 정지를 구별한다.
9. 코드 복사·구문 강조·Sources·페이지/섹션 footer·키보드 접근성을 유지한다. 긴 코드는 노트로 분리하고 작은 글자로 압축하지 않는다.
10. 실제 기록·고정 응답 시험·설계 예시를 구분한다. 기록되지 않은 압축·기억·위임을 실제처럼 채우지 않는다. 숨겨진 추론을 로그로 창작하지 않는다.

## A-2. 디자인 시스템 — 1차 원형 유지

| 요소 | 유지할 값·문법 |
|---|---|
| 분위기 | Tech conference / clear systems thinking. 어두운 배경, 도식 가독성 우선 |
| 배경·본문·보조·선 | `#0B1020` / `#EFF4FF` / `#9EACC8` / `#33415D` |
| 의미색 | Model 파랑 `#60A5FA`, Runtime 보라 `#B794F4`, Tool 녹색 `#34D399`, Context/Memory 주황 `#FDBA74`, Risk 빨강 `#FB7185`, Success 민트 `#5EEAD4` |
| 여백·글자 | 가로 7%, 세로 6%. 1920×1080 기준 label 14–18px, 제목 38–54px, 핵심 22–30px, 보조 17–22px, 코드 18–22px |
| footer | `01 / 172` + 현재 섹션. Sources 전체 URL은 노트 |
| 화면 밀도 | 결론형 제목, 한 장 한 주장, 핵심 1–3문구. 비교표는 4–5행 수준. 카드·배지 남발 금지 |
| 도식 | 역할별 색·코드 패널·레이어·루프·시퀀스 유지. 호출/반환/저장/제어 이전은 화살표에 명시 |
| 모션 | 기존 0.25–0.45초 ease-out. 키 입력 강조 약 0.3초, Reduced motion 시 즉시 표시 |
| 접근성 | 색+텍스트+단계 번호, 충분한 대비, 포커스, 최종 정적 화면 제공 |

**변경 허용 범위:** 토글→좌우 비교, 실행/초기화 버튼→순차 build, 툴팁 정의→짧은 고정 레이블, 반복적인 제작 안내→노트. 디자인 교체 근거로 쓰지 않는다. 모바일은 발표용 16:9 stage 비례 축소로 통일하며 작은 화면의 재배치로 도식을 바꾸지 않는다.

## A-3. 통일 예시 — 합성 BIN-X 분석

질문은 `LOT-DEMO의 BIN-X 비율을 확인해줘` → `왜 달라졌는지 다른 측정과 비교해줘` → `다른 기간 데이터로 다음 기간을 예측해줘`로 이어간다.

- BIN-X·LOT·장비·데이터는 가상/합성이다. 분자·분모·기간·단위·`snapshot_id`를 함께 표시한다. 실제 제조 데이터는 외부 API에 보내지 않는다.
- 비율은 도구로 계산한다. 예측은 별도 시간 분할·기준 모형·평가 도구가 준비된 경우에만 실행한다. 조회·관측·원인 가설·예측을 구분한다.
- `get_bin_summary`, `get_measurement_summary`, `forecast_bin`, `record_demo_note`는 **후속 Demo에서 작성할 앱 함수명**이다. 프레임워크 내장 API가 아니다.
- 마지막 기록 Tool은 임시 영역에만 기록하거나 호출 여부만 남기는 Mock이다. 실제 게시·설비 제어는 하지 않는다.
- 같은 데이터/질문으로 실행 구조를 비교한다. 코드 길이·Tool 수·서로 다른 모델 결과를 성능 순위로 바꾸지 않는다.
- Codex용 두 Demo는 `http://127.0.0.1:10000/v1`, Antigravity용 두 Demo는 `http://127.0.0.1:10001/v1`. 모델 별칭은 `demo-model`. 프록시의 실제 OpenAI upstream/모델/key는 Demo 코드에서 모른다. E-6 참조.

## A-4. 전체 세미나 경계

| 범위 | 처리 |
|---|---|
| 1차 | 개념은 전제. 해당 제품 설명에 필요한 연결 한 문장만 사용 |
| 집중 순서 | Hermes → Claude Code → PydanticAI. Hermes/PydanticAI만 실제 Demo 설계 |
| 후속 비교 순서 | Claude Agent SDK → Google ADK → Microsoft Agent Framework → OpenAI Agents SDK |
| 후속 비교 근거 | [SDK 비교 계획](../reviews/sdk-comparison-plan.md)의 고정 소스 태그, 공식 가이드와 학습 문서 |
| 다른 담당자 | LangChain/LangGraph, Mistral AI Studio, vLLM/SGLang 내부는 다루지 않음 |
| 3차 | 업무 적용·부하/자원 실측·운영 검증. 이번에는 운영 선택과 확인 질문까지 |

Harness/SDK는 엄격한 배타적 제품 계급이 아니라 **개발 출발점**을 설명하는 관점이다. SDK도 실행 루프를 제공하며 선택적 Harness로 확장될 수 있다.

## A-5. 사실·근거 규칙

- **SRC:** 고정 소스. **DOC:** 2026-11-03 열람한 현행 공식 문서. **설계 예시:** 발표/데모 설계. **미실행:** 설치·실동작 전. Sources와 노트에서 관리하며 화면에 배지를 반복하지 않는다.
- Hermes 내부 설명 기준 v0.22.5, PydanticAI v2.61.0. **설치 버전은 아직 없다.** Harness는 후속 구현 시 호환 버전을 별도로 고정한다. 현행 문서가 모든 고정 소스와 일치한다고 하지 않는다.
- Prefix cache는 Context 길이 감소가 아니다. Memory 저장은 현재 system snapshot 교체가 아니다. 도구 노출 필터는 인가가 아니다. 독립 Context는 OS/DB 격리가 아니다.
- 출력 타입 검증은 업무 정확성·인과·예측 정확성의 증명이 아니다. 승인 플래그는 UI·인증·인가·영속 복구를 자동 완성하지 않는다.
- **graceful에서도 유효 Output 뒤 Function Tool이 실행될 수 있다.** 종료 정책을 부작용 승인 대신 쓰지 않는다. 불일치는 F-3에 모은다.

## A-6. 본편 목차 및 생략 가능성

발표 시간이 미정이므로 본편 설명 약 55–70분, Demo 합계 12–18분은 **리허설 가정**이다. ‘확장’ 장은 노트로 돌릴 수 있다. 필요 조건을 지워 시간에 맞추지 않는다.

| ID | 제목 | 우선순위 |
|---|---|---|
| S00 | 다시 반갑습니다 | 필수 |
| S01 | 이제 실제 구현을 들여다봅니다 | 필수 |
| S02 | 2차에서 맡는 범위 | 필수 |
| S03 | 완성된 실행환경과 개발용 구성요소 | 필수 |
| S04 | Hermes 전체 아키텍처 | 필수 |
| S05 | 한 Turn을 실제 요청으로 만드는 경로 | 필수 |
| S06 | 응답 분기가 루프와 종료를 결정한다 | 필수 |
| S07 | 고정 Prompt와 호출별 정보는 따로 움직인다 | 필수 |
| S08 | Prefix 재사용은 서빙 계층의 일이다 | 확장 |
| S09 | 압축은 실행 이력의 정합성도 지켜야 한다 | 필수 |
| S10 | Memory 파일과 지금 보는 기억은 다르다 | 필수 |
| S11 | Session 검색은 전체 Memory의 대체물이 아니다 | 필수 |
| S12 | Skill은 필요할 때 읽고 유지 관리한다 | 필수 |
| S13 | 도구 등록·외부 연결·확장 Hook은 다른 접점이다 | 필수 |
| S14 | 병렬 Tool과 Child Agent는 실행 단위가 다르다 | 필수 |
| S15 | 정책 경계를 확인하고 Hermes Demo로 간다 | 필수·Demo 1 |
| S16 | Claude Code도 Harness에서 출발한다 | 필수 |
| S17 | 프로젝트 지시와 Auto Memory를 분리한다 | 필수 |
| S18 | Subagent 반환과 Team 협업은 다르다 | 필수 |
| S19 | Slash command는 실행 상태를 조작하는 입구다 | 확장 |
| S20 | Pydantic → PydanticAI → 선택적 Harness | 필수 |
| S21 | PydanticAI 전체 아키텍처 | 필수 |
| S22 | 개발자는 업무 계약과 Tool을 작성한다 | 필수 |
| S23 | 세 Graph 노드가 다음 실행을 정한다 | 필수 |
| S24 | 지시·History·Deps는 같은 입력이 아니다 | 필수 |
| S25 | Tool은 스키마 준비·검증·실행을 거친다 | 필수 |
| S26 | 병렬 실행은 의존성 없는 구간을 겹친다 | 필수 |
| S27 | 출력 형식과 결과의 정확성은 따로 검증한다 | 필수 |
| S28 | EndStrategy는 실제 실행 범위를 바꾼다 | 필수 |
| S29 | Retry를 발생 위치별로 나눈다 | 필수 |
| S30 | Hook을 기능 단위 Capability로 합성한다 | 필수 |
| S31 | 여러 Run의 대화는 명시적으로 이어 붙인다 | 필수 |
| S32 | 압축 전략은 제공되지만 보존 정책은 설계한다 | 필수 |
| S33 | Harness Memory는 저장·주입·검색을 묶는다 | 필수 |
| S34 | Skill 로딩과 MCP 호출을 따로 연결한다 | 확장 |
| S35 | 위임·라우팅·Graph·Advisor의 제어권 | 필수 |
| S36 | 승인은 보류 Call을 해결하고 재개하는 계약이다 | 필수 |
| S37 | Core에 Harness를 더해도 업무 책임은 남는다 | 필수 |
| S38 | 코드와 내부 전이를 PydanticAI Demo에서 잇는다 | 필수·Demo 2 |
| S39–S42 | 네 SDK 비교 | 본편 · SDKMAP 이후 |
| S43 | 중앙 실행과 로컬 실행은 책임 배치가 다르다 | 필수 |
| S44 | 분석에 필요한 검증 기준을 정한다 | 확장 |
| S45 | 제공받는 실행과 직접 만드는 계약 | 필수 |

---

# B. 슬라이드별 상세 명세

‘화면’은 실제 청중 문구, ‘설명/대본’은 노트다. 도식 관계는 처음부터 보이고 build는 **강조를 이동**한다. 명시되지 않은 핵심 내용을 숨기는 인터랙션을 추가하지 않는다.

## S00 — 다시 반갑습니다

- **섹션·우선순위:** Opening · 필수.
- **핵심/화면:** `다시 반갑습니다.` / `Agent Framework 세미나 · 2차` / 작은 부제 `실행 구조와 개발 책임`.
- **구성·단계:** 1차 S00 중앙 상단 1/3 문구, 우하단 연결 노드 3개 유지. 짧은 fade-in 후 다음 장. 개인정보 임의 생성 금지.
- **설명/대본:** “지난번에는 Agent를 이루는 개념을 맞췄습니다. 오늘은 각 기술 안에서 실제로 어떤 구조가 작동하는지 보겠습니다.”
- **연결·근거:** 인사→S01. [FLOW] 도입.

## S01 — 이제 실제 구현을 들여다봅니다

- **섹션·우선순위:** Opening · 필수.
- **핵심/화면:** `AGENT FRAMEWORK` / `Inside the Implementations` / `같은 구성요소, 서로 다른 실행 책임` / `Seminar 02`.
- **구성·단계:** 1차 S01의 좌측 58% 타이틀, 우측 42% 원형 루프 유지. 전체→Runtime 강조→`무엇을 제공받고, 무엇을 직접 만드는가?`.
- **설명/대본:** “일반 루프 정의 대신 Hermes가 Context를 언제 고정하고 PydanticAI가 어떤 분기로 Tool을 실행하는지처럼 구체적인 구현 선택을 보겠습니다.”
- **연결·근거:** 목적→범위. [FLOW] 구성 원칙.

## S02 — 2차에서 맡는 범위

- **섹션·우선순위:** Opening · 필수.
- **핵심/화면:** `1차 · 공통 개념 → 2차 · 기술별 실제 구조 → 3차 · 직접 개발·적용`; `이 파트: Hermes · Claude Code · PydanticAI`.
- **구성·단계:** 1차 S02 3열 타임라인. 2차만 밝게, 다른 발표자 `LangChain/LangGraph`, `Mistral AI Studio · vLLM/SGLang`은 작은 점선 영역. 전체→2차→내 파트.
- **설명/대본:** “두 기술은 내부 동작과 실행 관찰까지 다룹니다. 서빙 엔진 내부는 다른 발표에서 이어지고 실제 업무 적용과 운영 실측은 3차로 연결합니다.”
- **연결·근거:** 범위→기술 지도. [FLOW] 도입.

## S03 — 완성된 실행환경과 개발용 구성요소

- **섹션·우선순위:** Landscape · 필수.
- **핵심/화면:** `Harness에서 출발: Hermes · Claude Code` / `코드로 구성: PydanticAI` / `실행 루프는 양쪽 모두에 있다`.
- **구성·단계:** 1차 S03 지도+S24 레이어 문법. 두 갈래 아래 공통 Model API/추론 서비스/모델. 전체 책임 지도→Hermes/PydanticAI 강조. PydanticAI 이후 SDKMAP에서 네 SDK의 후속 순서를 소개한다.
- **설명/대본:** “계층을 엄격히 나누는 표준이 아니라 시작점의 차이입니다. Hermes는 갖춰진 실행환경에 기능을 붙이고 PydanticAI는 앱 코드로 업무 계약을 구성합니다. 후자도 루프는 내장합니다.”
- **연결·근거:** 분류→Hermes 전체. [FLOW][P01].

## S04 — Hermes 전체 아키텍처

- **섹션·우선순위:** Hermes · 필수.
- **핵심/화면:** `입력 경로 → AIAgent → 모델·도구·저장소`; `반복 실행을 중심으로 기능을 묶은 Harness`.
- **구성:** `h-entry` CLI/Gateway/API/ACP 위, `h-loop` AIAgent 보라 경계 안에 `h-prompt` Prompt/Compression, `h-provider` Provider adapter, `h-dispatch` Tool dispatch. 밖에 `h-model`, `h-tools`, `h-session` SQLite/FTS5, `h-memory` 파일, `h-skills` 절차. 정책/Trace는 실행 접점의 경계.
- **단계:** 전체 노드→Prompt/Tool/State 세 확대 영역.
- **설명/대본:** “기능 하나가 아니라 모델 호출과 도구 실행을 반복하고 상태를 보존하는 환경입니다. 이 지도에서 한 부분씩 확대하겠습니다.” CLI/TUI/Desktop/메신저·Cron·Hooks·Plugins 목록은 노트.
- **연결·근거:** 전체→Turn. 실제 구현 단순화 [H01][H02].

## S05 — 한 Turn을 실제 요청으로 만드는 경로

- **섹션·우선순위:** Hermes / Execution · 필수.
- **핵심/화면:** `입력·Task → Prompt/History 준비 → 압축 판단 → Provider 변환 → 모델 요청`; `API 직전 입력을 관찰한다`.
- **구성·단계:** 1차 S11 시퀀스의 Entry/AIAgent/Provider/Model 4레인. Task+user append→prompt 재사용/구성→일시 정보→payload. History와 tools schema는 별도 합류.
- **설명/대본:** “Context는 화면 대화만이 아닙니다. snapshot·이력·도구 정의·호출 시점 정보가 adapter를 거칩니다. 관찰에서도 변환 전 객체와 최종 JSON을 나눠 봅니다.” cache marker는 지원 Provider에만 적용.
- **연결·근거:** 요청→응답 분기. [H02][H03].

## S06 — 응답 분기가 루프와 종료를 결정한다

- **섹션·우선순위:** Hermes / Execution · 필수.
- **핵심/화면:** `Tool Call → 실행·결과 추가 → 다음 호출` / `최종 답변 → 저장·종료` / `오류·중단·예산 → 복구 또는 종료`.
- **구성·단계:** 1차 S10/S15 루프의 분기에 `tool_calls?` 레이블. 정상 Tool 경로→최종 답변→Tool error/API retry/interrupt/예산. Tool error는 결과로, API error는 통신 복구로 별도 연결.
- **설명/대본:** “목표 달성을 판정하는 공통 성공 센서가 있는 게 아닙니다. 응답·실행 예산·오류·취소 조건으로 분기합니다. 도구 오류를 모델에 알려 수정 기회를 주는 것과 API 장애 재시도는 다릅니다.”
- **연결·근거:** 실행→입력 구성. [H02]. 예산 소진의 실제 마무리 경로는 설치 버전에서 관찰.

## S07 — 고정 Prompt와 호출별 정보는 따로 움직인다

- **섹션·우선순위:** Hermes / Context · 필수.
- **핵심/화면:** `Stable → Context → Volatile` / `세션 snapshot + 이력 + 이번 호출 정보` / `Volatile ≠ 매 호출 재작성`.
- **구성·단계:** 1차 S18 Context 패널을 세 층으로. Stable=SOUL/기본 행동, Context=프로젝트/호출자 지침, Volatile=Memory/USER/런타임 snapshot. 별도 History·일시 정보→모델 요청. 계층→snapshot 고정→일시 정보 이동.
- **설명/대본:** “Volatile도 세션 내 고정된 prompt 일부일 수 있습니다. SOUL은 정체성, AGENTS 계열은 프로젝트 규칙입니다. 실제 파일 로더 우선순위는 따로 확인합니다.” Skill 계층은 현행 문서 자체의 불일치가 있어 고정 위치를 단정하지 않는다.
- **연결·근거:** 고정 prefix→캐시. [H03], F-3.

## S08 — Prefix 재사용은 서빙 계층의 일이다

- **섹션·우선순위:** Hermes / Cache · 확장.
- **핵심/화면:** `같은 앞부분 → 기존 KV 계산 재사용` / `Hermes: 입력 배치` / `추론 서비스: 캐시 판단`.
- **구성·단계:** 두 토큰 막대에 공통 prefix·변경 suffix. `10,000 중 8,000 동일 — 설명용` 표시. Hermes→endpoint→Serving Engine→Model. 동일 prefix→뒤 변경→담당 계층.
- **설명/대본:** “Python 조립 시간보다 추론 계산을 줄이는 원리입니다. 입력은 여전히 전송되고 Context 길이도 같습니다. 적중은 prefix·퇴거·부하에 좌우됩니다. 로컬 OpenAI 프록시 기록을 vLLM 캐시 실측으로 보여주지 않습니다.”
- **연결·근거:** 재사용→한도 관리. [H04][V01]. 속도·절감 수치 미측정.

## S09 — 압축은 실행 이력의 정합성도 지켜야 한다

- **섹션·우선순위:** Hermes / Context · 필수.
- **핵심/화면:** `상태·기억 보존 → 오래된 내용 축약 → 최근 문맥·Tool 쌍 유지` / `in-loop 압축 ≠ Gateway 위생 처리`.
- **구성·단계:** 1차 S21 Before/After. Tool Call/Result를 한 괄호로 묶고 오래된 이력→요약, 최근 문맥 유지. 누적→발동 위치→보존 대상.
- **설명/대본:** “앞 문장을 자르는 기능으로 이해하면 호출·반환 대응이 깨질 수 있습니다. 문서의 50%/85%는 기본 설명이며 모델 크기·출력 예약·설정 보정으로 실효 임계값이 달라질 수 있습니다. 무조건 절반에서 압축한다고 말하지 않습니다.” 최근 20개도 설정 예로만 노트.
- **연결·근거:** 보존할 기억→저장소. [H04].

## S10 — Memory 파일과 지금 보는 기억은 다르다

- **섹션·우선순위:** Hermes / Memory · 필수.
- **핵심/화면:** `파일 저장 / 현재 세션 snapshot / 다음 세션 반영`; `저장 성공 ≠ 현재 system prompt 교체`.
- **구성·단계:** MEMORY.md/USER.md와 세션 A/B. A 시작 snapshot→A 중간 write는 파일로→B 시작 새 snapshot. A system으로 즉시 되돌아가는 화살표 금지.
- **설명/대본:** “현재 Tool 결과로 저장 내용을 알아도 처음 고정한 system snapshot과는 다릅니다. add/patch/remove로 관리하며 용량 초과는 오류로 돌려 정리를 유도합니다.” 노트: 2,200/1,375자 기준·자율/사용자/백그라운드 write·write_approval.
- **시사점:** 선호는 재사용해도 SOP·측정 근거는 분석 시작 시 버전 고정. 설계 예시.
- **연결·근거:** 기억→기록 검색. [H05][H06].

## S11 — Session 검색은 전체 Memory의 대체물이 아니다

- **섹션·우선순위:** Hermes / Session · 필수.
- **핵심/화면:** `Memory: 소수의 지속 사실` / `state.db + FTS5: 과거 대화 검색` / `외부 Provider: 별도 확장`.
- **구성·단계:** 1차 S18 저장 역할 비교. `session_search→선택 결과→Context`. 저장 경로→정확 코드 질의→선택 주입. 전체 DB 자동 주입 금지.
- **설명/대본:** “기본 대화 검색은 임베딩 검색과 다릅니다. 정확 장비 ID 질의와 표현만 비슷한 사례 질의를 나눠 평가하고 대상·기간도 확인합니다.” Profile은 config/DB/memory 운영 분리이며 독립 보안 테넌트 보장은 아님.
- **노트:** HERMES_HOME 아래 config.yaml/.env/state.db/memories/skills/plugins 트리. Windows 기본 경로까지 무조건 ~/.hermes로 단정하지 않는다.
- **연결·근거:** 사건 검색→절차 지식. [H07][H08].

## S12 — Skill은 필요할 때 읽고 유지 관리한다

- **섹션·우선순위:** Hermes / Skills · 필수.
- **핵심/화면:** `인덱스 → SKILL.md → 필요한 참고 파일` / `skill_manage로 갱신` / `Curator: active → stale → archived`.
- **구성·단계:** 1차 S22/S23 문서→Context 관계. 폴더 SKILL.md/references/scripts와 아래 별도 Curator 유지관리 경로. 목록→본문→지원 자료→정리.
- **설명/대본:** “Skill은 언제 어떻게 도구를 쓸지 알려주는 절차입니다. 실행은 Tool이 합니다. Curator는 Agent가 만든 Skill의 사용 이력을 관리합니다. 오래 안 썼다고 모든 사용자 Skill을 삭제하는 것으로 말하지 않습니다.”
- **시사점:** 잘못된 분석 절차도 재사용될 수 있으므로 검토·버전·근거 필요. 가중치 학습과 다름.
- **연결·근거:** 지침→기능 연결. [H09][H10].

## S13 — 도구 등록·외부 연결·확장 Hook은 다른 접점이다

- **섹션·우선순위:** Hermes / Tools · 필수.
- **핵심/화면:** `Registry → 활성 스키마 → 이름으로 dispatch` / `MCP: 외부 호출 경로` / `Plugin: Tool·Hook·명령 확장`.
- **구성·단계:** 1차 S23 확대. 모델 schema와 handler 별도 칸. 로컬·MCP 경로 동시 표시, Plugin은 등록/Hook에 점선. 등록→Toolset/check→dispatch→관찰.
- **설명/대본:** “모든 등록 도구가 매번 노출되지는 않습니다. 환경과 활성화 검사를 통과한 schema를 보냅니다. memory/delegate_task 같은 Agent 상태 도구는 일반 dispatch 앞에서 처리할 수 있어 중앙 Hook 하나로 전부 봤다고 단정할 수 없습니다.”
- **노트:** 실제 registry.register(name, toolset, schema, handler, check_fn), Plugin register(ctx)/ctx.register_tool·register_hook. 인수는 설치 버전 대조. 자체 Tool 추가에 Core fork가 항상 필수라는 주장은 삭제.
- **연결·근거:** dispatch→동시 실행. [H11][H12].

## S14 — 병렬 Tool과 Child Agent는 실행 단위가 다르다

- **섹션·우선순위:** Hermes / Orchestration · 필수.
- **핵심/화면:** `Tool: 한 Loop의 여러 실행` / `delegate_task: 자식의 별도 Loop·Context` / `자식 결과 → 부모 판단`.
- **구성·단계:** 좌 한 응답→여러 Tool→합류, 우 부모→자식 두 Loop→요약 반환. 공통 파일/서비스는 바깥 공유 영역. Tool→자식→격리 경계.
- **설명/대본:** “스레드는 실행 수단입니다. 별도 Agent인지 보려면 자체 모델 호출과 Context가 있는지 봐야 합니다. 독립 Goal/Context를 주고 결과를 부모로 돌려주므로 대화의 영구 handoff와 다릅니다.” 모든 Tool 무조건 병렬이라는 설명은 삭제, barrier/충돌 조건 적용.
- **시사점:** 같은 snapshot의 독립 조회를 합친다. Context 분리가 OS/DB 격리는 아니다.
- **연결·근거:** 동시성→정책. [H13][H14].

## S15 — 정책 경계를 확인하고 Hermes Demo로 간다

- **섹션·우선순위:** Hermes / Guardrails · 필수·Demo 1.
- **핵심/화면:** `입력 경계 → 명령·파일 정책 → 승인 → 실행환경` / `패턴 탐지 + 실제 권한` / `Demo 1: Context → Tool → 저장`.
- **구성·단계:** 1차 S26 Gate. 위험 패턴 승인과 DB/컨테이너 권한은 다른 문, checkpoint는 복구 옆 가지. Gate→무인 정책→Demo 경로.
- **설명/대본:** “smart/manual/off와 무인 deny 정책의 조합이 통제 수준을 바꿉니다. 패턴 탐지는 실제 권한을 대신하지 않고 opt-in checkpoint도 모든 외부 변경을 되돌리지는 못합니다.” Cron은 새 Agent 작업의 실행 입구이며 무인 승인·중복·전달 정책 필요.
- **Demo 진입·복귀:** 별도 Hermes 뷰어, 조회→분석→실제 Context/Tool/저장, 가능하면 기억/위임 한 경로. 기본 6–8분. 이 장 master로 복귀→S16.
- **근거:** [H15][H16]. Demo는 미실행 설계.

## S16 — Claude Code도 Harness에서 출발한다

- **섹션·우선순위:** Claude Code · 필수.
- **핵심/화면:** `Gather ↔ Act ↔ Verify` / `도구·권한·Context를 갖춘 실행환경`.
- **구성·단계:** 먼저 c-entry→c-runtime↔c-model, c-tools/c-project/c-memory/c-policy/c-children 전체 지도. Runtime 안은 공개 계약 경계, 비공개 함수 그래프 금지. 전체→세 동작→Hermes 공통 관심사.
- **설명/대본:** “갖춰진 Harness를 사용하는 출발점입니다. 맥락 수집·행동·검증으로 설명되며 공개 인터페이스는 비교할 수 있지만 엔진 전체 소스를 분석한 것처럼 말하지 않습니다.”
- **연결·근거:** 실행환경→기억. [C01].

## S17 — 프로젝트 지시와 Auto Memory를 분리한다

- **섹션·우선순위:** Claude Code / Context · 필수.
- **핵심/화면:** `CLAUDE.md: 사람이 작성한 규칙` / `Auto Memory: 경험·교정 기록` / `지시 ≠ 실제 권한`.
- **구성·단계:** Hermes MEMORY/USER와 Claude 지시/Auto Memory를 2×2 비교. 사람 작성→Agent 작성→실제 정책. 이름이 같아도 저장/로드 정책을 합치지 않는다.
- **설명/대본:** “공통 규칙을 AGENTS.md에 두고 CLAUDE.md에서 @AGENTS.md로 import할 수 있습니다. 두 파일이 항상 같은 방식으로 자동 로드된다고 말하지 않습니다. Auto Memory는 인덱스를 먼저 읽고 상세 파일을 필요시 읽습니다.”
- **노트:** 현행 문서: 처음 200줄 또는 25KB, worktree 공유. 내부 검색 순위 전체는 비공개.
- **연결·근거:** Context→자식 Context. [C02].

## S18 — Subagent 반환과 Team 협업은 다르다

- **섹션·우선순위:** Claude Code / Orchestration · 필수.
- **핵심/화면:** `Subagent: 부모 위임·결과 반환` / `Teams: 독립 세션·공유 작업·직접 메시지` / `Teams: 실험적 기능`.
- **구성·단계:** 좌 별형 트리, 우 팀원 메시지+공유 작업. 온도 검토 자식→부모 보고→팀 가설 교차 검토. 원문 read-only reviewer 설정은 노트.
- **설명/대본:** “분업보다 결과 통신과 다음 행동의 주체가 다릅니다. 팀은 충돌 조정·비용과 실험적 제약을 동반합니다. tools 축소가 파일·DB 계정 격리를 자동 생성하지는 않습니다.”
- **연결·근거:** 협업→실행 제어 입구. [C03][C04].

## S19 — Slash command는 실행 상태를 조작하는 입구다

- **섹션·우선순위:** Harness 비교 · 확장.
- **핵심/화면:** `기록 이어가기 / Context 관리 / 기억 검토`; `명령 이름보다 바뀌는 상태를 본다`.
- **구성·단계:** 명령/대상 상태 3행 비교. Hermes CLI `hermes sessions refresh-prompts --session SESSION_ID`, slash `/memory pending`; Claude `/resume`, `/compact`. CLI와 slash 구분. 세션→Prompt→Memory 강조.
- **설명/대본:** “이 명령은 저장 상태와 실행 정책의 인터페이스입니다. 재개가 팀원 복원까지 보장하지 않고 prompt 갱신도 기록 삭제와 다릅니다. 실제 실행 전 해당 버전 help로 확인합니다.” 실제 명령 실행 버튼 금지.
- **연결·근거:** Harness 사용→Python 구성. [H05][H08][C05].

## S20 — Pydantic → PydanticAI → 선택적 Harness

- **섹션·우선순위:** PydanticAI · 필수.
- **핵심/화면:** `Pydantic: 값의 계약` / `PydanticAI Core: Agent 실행` / `Harness: 재사용할 동작 조합`.
- **구성·단계:** 1차 S25 계단 세 층, pydantic-graph/Evals/Logfire는 별도 연결. Provider/모델 바깥. 타입→엔진→선택 확장.
- **설명/대본:** “JSON 검증만 붙인 API 래퍼가 아닙니다. Tool·출력·Retry 실행 엔진을 갖고 필요하면 별도 Harness로 기억·Skills를 조합합니다. Core만으로도 Agent를 만들 수 있습니다.”
- **연결·근거:** 패키지→전체 지도. [P01][P02].

## S21 — PydanticAI 전체 아키텍처

- **섹션·우선순위:** PydanticAI / Architecture · 필수.
- **핵심/화면:** `개발자 정의 → 내부 Graph → Model/Tools → 결과 검증`; `저장·권한·업무 검증은 앱과 연결`.
- **구성:** p-app/p-agent/p-deps 위, p-input UserPromptNode→p-request ModelRequestNode→p-calls CallToolsNode→요청 또는 End. 밖에 p-model/p-tools/p-output/p-history. Capability는 실행 접점, Harness는 선택적 제공자로 표시.
- **단계:** 전체 지도→개발자 영역→SDK 실행 영역.
- **설명/대본:** “개발자는 업무 지침·도구·의존성·결과 계약을 정합니다. SDK가 요청·응답을 실행/출력 경로로 분류합니다. 내부 Graph는 pydantic-graph이고 LangGraph가 아닙니다.”
- **연결·근거:** 전체→코드. [P01][P03].

## S22 — 개발자는 업무 계약과 Tool을 작성한다

- **섹션·우선순위:** PydanticAI / Code · 필수.
- **핵심/화면:** `Agent 정의 + Tool 구현 + 실행 시 Deps`; `루프를 다시 작성하지 않는다`.
- **구성:** 좌 62% 코드, 우 38% S21 축소도. 아래 실제 API 축약만 화면에. import·앱 정의·Provider 전체는 C-2.

```python
agent = Agent(model, deps_type=DemoDeps,
              instructions='도구 근거로만 답하라.')

@agent.tool
async def get_bin_summary(ctx: RunContext[DemoDeps], lot_id: str) -> dict:
    return await ctx.deps.query(lot_id)

result = await agent.run('LOT-DEMO의 BIN-X를 조회해줘', deps=deps)
```

- **단계:** Agent→Tool→deps→SDK 실행.
- **설명/대본:** “query와 DemoDeps는 앱 코드, Agent/tool/run은 실제 SDK API입니다. 허용 LOT와 권한은 query 서비스에서 검사합니다.” 실행 완제품이 아닌 실제 API 축약으로 명시.
- **연결·근거:** 표면 코드→내부 실행. [P01][P04][P05].

## S23 — 세 Graph 노드가 다음 실행을 정한다

- **섹션·우선순위:** PydanticAI / Graph · 필수.
- **핵심/화면:** `UserPromptNode: 입력·이력 준비` / `ModelRequestNode: 모델 호출` / `CallToolsNode: Tool·Output 분류`.
- **구성·단계:** S21 노드 확대. Tool→ToolReturn→다음 요청, Output 검증→End, 실패 feedback→재요청. 아래 history/usage/retry/step 상태. 입력→요청→갈림길.
- **설명/대본:** “다음 단계의 근거가 런타임 분기로 남습니다. 도구는 검증·실행, 유효 결과는 종료, 수정은 피드백 요청입니다. 사용자 정의 Workflow와 내부 Agent Graph는 다릅니다.”
- **연결·근거:** 노드→입력 경계. [P03].

## S24 — 지시·History·Deps는 같은 입력이 아니다

- **섹션·우선순위:** PydanticAI / Context · 필수.
- **핵심/화면:** `Instructions/System Prompt/History → Provider → 모델` / `Deps → Python Tool·Hook` / `Deps 전체 자동 전송 아님`.
- **구성·단계:** 모델 입력 레인과 Python 객체 레인. dynamic instruction/Tool return을 거친 선택값만 모델로. 지시→Deps→명시 전달. DB client/key는 Python 레인.
- **설명/대본:** “instructions와 system_prompt는 이력 보존·재사용 규칙이 다릅니다. 동적 지침은 RunContext를 읽을 수 있습니다. 최종 system/developer/content 매핑은 adapter별로 달라 동일 Python Part를 동일 JSON으로 단정하지 않습니다.”
- **시사점:** 인증 tenant와 DB를 deps에 넣고 실제 Tool에서 인가한다. 비전송 객체라도 Tool 결과 유출은 별도 문제.
- **연결·근거:** 입력→Tool. [P04][P06][P07].

## S25 — Tool은 스키마 준비·검증·실행을 거친다

- **섹션·우선순위:** PydanticAI / Tools · 필수.
- **핵심/화면:** `함수·타입 → Schema → 인자 검증 → 정책·승인 → 실행 → 반환`; `tool: RunContext / tool_plain: 일반 인자`.
- **구성·단계:** 1차 S11 시퀀스. schema 공개와 실행 허가는 분리, Toolset은 집합/필터/접두어/결합 공급. 두 decorator→schema→검증→실행.
- **설명/대본:** “ctx는 모델이 채울 인자가 아닌 Python 문맥입니다. tool_plain은 순수 계산에 간단합니다. ToolManager가 준비·검증·실행·보류를 연결하고 FilteredToolset은 노출 후보를 줄입니다. 실제 인가와는 다릅니다.” Native Tool의 공급자 실행과 로컬 함수를 동일시하지 않는다.
- **연결·근거:** 하나→여러 호출. [P05][P08][P09].

## S26 — 병렬 실행은 의존성 없는 구간을 겹친다

- **섹션·우선순위:** PydanticAI / Concurrency · 필수.
- **핵심/화면:** `독립 A·B → Barrier → C·D`; `async task / sync worker thread`; `동시 완료 ≠ 같은 데이터 시점`.
- **구성·단계:** 시간축 A/B 동시→sequential 단독→C/D 동시. emission 순서와 완료 시각 별도. 호출→동시 구간→barrier→snapshot.
- **설명/대본:** “여러 호출은 asyncio task로 스케줄하고 sync는 worker thread에 올립니다. sequential=True는 앞 구간을 기다리고 혼자 실행한 뒤 다음을 엽니다. CPU 계산의 다중 코어 가속이나 DB 트랜잭션을 자동 제공하는 것은 아닙니다.”
- **연결·근거:** 실행→Output. [P08][P10].

## S27 — 출력 형식과 결과의 정확성은 따로 검증한다

- **섹션·우선순위:** PydanticAI / Output · 필수.
- **핵심/화면:** `ToolOutput: 출력용 Tool Schema` / `NativeOutput: Provider 구조화 기능` / `PromptedOutput: 지시+파싱·검증`; `형식 통과 ≠ 내용 검증`.
- **구성·단계:** 3열 원리 비교→하단 Pydantic/업무 validator/실데이터 재계산. 형식 제시→반환 해석→정답 기준. TextOutput은 노트.
- **설명/대본:** “ToolOutput은 임의 텍스트를 Tool Call로 우겨 넣는 게 아니라 출력 schema를 Tool로 제시합니다. Native는 공급자 지원, Prompted도 파싱·검증이 필요합니다. output_type은 최종 계약이고 개별 Tool return type과 다릅니다.”
- **연결·근거:** 유효 출력→혼합 응답. [P11].

## S28 — EndStrategy는 실제 실행 범위를 바꾼다

- **섹션·우선순위:** PydanticAI / Finalization · 필수.
- **핵심/화면:** 동일 응답 `조회 A → Output O1 → 게시 Mock B → Output O2`, 세 레인 `early / graceful / exhaustive`. 조건 `O1/O2 유효 · Retry 없음 · 비스트리밍`.
- **구성·단계:** early=O1만; graceful=A→O1→B, O2 생략; exhaustive=A/O1/B/O2 모두, emission상 첫 유효 O1 선택. barrier 없는 exhaustive는 병렬 표시. 같은 응답→세 레인 순차 강조, 토글 없음.
- **설명/대본:** “graceful은 최종 결과 뒤 Function Tool을 모두 취소하지 않습니다. 첫 성공 뒤 다른 Output Tool은 건너뛰지만 Function Tool은 실행할 수 있습니다. 게시·변경은 별도 정책으로 통제합니다.” Function ModelRetry·Native/Prompted·plain text·stream 예외는 C-5.
- **연결·근거:** 최종화→Retry. [P03][P10], v2.61.0.

## S29 — Retry를 발생 위치별로 나눈다

- **섹션·우선순위:** PydanticAI / Failure · 필수.
- **핵심/화면:** `인자·출력 실패 → 모델 수정 피드백` / `Provider 장애 → 통신 재시도` / `업무 실패 → 재검증·판단`.
- **구성·단계:** 1차 S27 실패 루프를 세 레인으로. ModelRetry와 429의 반환 위치 구분. 검증→수정→통신→누적 예산.
- **설명/대본:** “retries=2가 모든 장애의 전체 한도가 아닙니다. SDK·HTTP·프록시 재시도가 겹치면 wire 요청이 증폭됩니다. 수정 가능한 오류·권한 거절·일시 장애를 나누고 UsageLimits와 시간·부작용 중복 방지도 별도 관리합니다.”
- **연결·근거:** 실패→확장 접점. [P12].

## S30 — Hook을 기능 단위 Capability로 합성한다

- **섹션·우선순위:** PydanticAI / Extension · 필수.
- **핵심/화면:** `Hook: 실행 지점 개입` / `Capability: Tool·지시·Hook·설정 묶음` / `합성 순서도 실행 의미다`.
- **구성·단계:** S21 실행 접점 확대. 감사 A/정책 B wrapper와 `A.enter→B.enter→core→B.exit→A.exit`. 단일 Hook→기능 묶음→순서→우회 주의.
- **설명/대본:** “문서 Skill과 달리 Python 동작을 합성합니다. 기능을 여러 Agent에 재사용할 수 있습니다. wrapper가 handler를 호출하지 않으면 안쪽 Hook도 생략될 수 있어 필수 인가를 우회하지 않게 배치해야 합니다.”
- **시사점:** 단위 표준화·snapshot 기록·권한 검사를 적절한 접점으로 나눈다. 구조 재사용의 이점이지 업계 유일 개념은 아니다.
- **연결·근거:** 확장→상태 수명. [P13][P14]. 코드 C-6.

## S31 — 여러 Run의 대화는 명시적으로 이어 붙인다

- **섹션·우선순위:** PydanticAI / History · 필수.
- **핵심/화면:** `Run 1 → 저장 → Run 2` / `message_history 또는 conversation` / `객체 재사용 ≠ 사용자 대화 자동 복원`.
- **구성·단계:** 1차 S19 두 턴, typed Parts→bytes→로드→다음 Run. usage/ID 동반 표시. 새 Run→history→conversation→저장 책임.
- **설명/대본:** “앱이 이전 이력을 전달합니다. 현행 conversation은 이력·사용량·ID 등을 함께 넘기는 길입니다. 저장 위치와 사용자별 로드는 앱/추가 persistence 책임입니다. 이력만 넘기고 usage를 초기화하면 대화 누적 예산과 달라집니다.”
- **연결·근거:** 전체 이력→요청에 쓸 범위. [P06][P15]. 현행 편의 API는 설치 버전 대조.

## S32 — 압축 전략은 제공되지만 보존 정책은 설계한다

- **섹션·우선순위:** PydanticAI / Compaction · 필수.
- **핵심/화면:** `Core: Provider-native compaction` / `Harness: clear·window·summarize` / `원본 보관과 요청 축약은 별도`.
- **구성·단계:** 원본 보관/Run history 두 레인. 압축→축약 history→요청. 요청만 바꾸는 변환과 이후 history에 유지되는 변경을 구분. 계층→변경→보관.
- **설명/대본:** “전략을 전부 직접 구현할 필요는 없습니다. 그러나 Harness trim/clear/summary는 Run 이력에 이어질 수 있어 원본 보관이 별도입니다. Tool 쌍·정확 수치·근거 경로를 검증해야 합니다.” vLLM 이관 기본 데모에 Provider 전용 compaction을 필수로 넣지 않는다.
- **연결·근거:** 이력 축약→지속 기억. [P02][P16].

## S33 — Harness Memory는 저장·주입·검색을 묶는다

- **섹션·우선순위:** PydanticAI / Memory · 필수.
- **핵심/화면:** `저장소 + namespace + 제한된 주입 + 검색`; `대화 History와 다른 수명`.
- **구성·단계:** store→Memory→Context, 모델 Tool→store. namespace는 앱 deps에서 공급하며 모델 인자에서 고르지 않는다. 저장→범위→주입→정책.
- **설명/대본:** “기능·저장소를 선택할 수 있지만 기억할 사실·읽기/갱신 권한·SOP 만료는 설계해야 합니다. namespace는 주소 범위이며 인증과 공유 DB 권한을 대신하지 않습니다.” Hermes snapshot과 같은 구현으로 단정하지 않는다.
- **연결·근거:** 사실→절차/외부 기능. [P17].

## S34 — Skill 로딩과 MCP 호출을 따로 연결한다

- **섹션·우선순위:** PydanticAI / Integrations · 확장.
- **핵심/화면:** `Skills: 목록 → load_capability → 본문` / `MCP: 연결 → Tool 발견 → 호출`.
- **구성·단계:** 1차 S23 로컬/MCP 동시 경로. Skill은 입력, MCP는 실행. 개발자 영역에는 library/서버/인증. scan→load→MCP→결과.
- **설명/대본:** “Harness가 유효 Skill을 찾아 목록과 선택 로딩을 제공합니다. MCP도 연결 추상화를 제공하지만 서버·인증·수명·도구별 권한은 준비해야 합니다. 기본 구현 제공과 업무 통합 완료를 구분합니다.”
- **연결·근거:** 기능 연결→Agent 연결. [P18][P19], C-8 코드.

## S35 — 위임·라우팅·Graph·Advisor의 제어권

- **섹션·우선순위:** PydanticAI / Orchestration · 필수.
- **핵심/화면:** `도구 위임: 부모 반환` / `코드 라우팅: 앱이 선택` / `Graph: 명시적 상태·분기` / `Harness: Subagents·Advisor`.
- **구성·단계:** 2×2 소형 시퀀스: A→tool(B.run)→A / user→router→B / node→조건→node / 주 Agent↔Advisor. 위임→라우팅→Graph→확장. 반환/제어 이전 레이블.
- **설명/대본:** “delegation은 agent-as-a-tool의 부모 반환 패턴에 대응합니다. programmatic handoff는 앱의 흐름 패턴이지 다른 SDK native handoff와 같은 함수가 아닙니다. Advisor는 조언을 구하는 역할이지 실행권 전체 이전이 아닙니다.” 상태·deps·usage·자식 권한 명시.
- **연결·근거:** 제어권→승인. [P20][P21][P22].

## S36 — 승인은 보류 Call을 해결하고 재개하는 계약이다

- **섹션·우선순위:** PydanticAI / Approval · 필수.
- **핵심/화면:** `requires_approval → DeferredToolRequests` / `호스트 승인·거절 → DeferredToolResults` / `같은 Call ID + 인자·버전`.
- **구성·단계:** SDK/호스트 두 swimlane에 pending→승인/거절→재개. 보류→검토→연결→실행 인가. 자동 UI 생성 연출 금지.
- **설명/대본:** “CLI·웹·정책 handler 중 해결 경로를 호스트가 제공합니다. inline으로 해결하거나 미해결 호출을 반환·저장해 다음 Run으로 잇습니다. thread를 영원히 잡아야 하는 방식만 있는 게 아닙니다.” 인자 변경 후 이전 승인 재사용 금지, 게시 Mock만 사용.
- **연결·근거:** 승인 책임→제공 범위. [P23].

## S37 — Core에 Harness를 더해도 업무 책임은 남는다

- **섹션·우선순위:** PydanticAI / Trade-offs · 필수.
- **핵심/화면:** `Core: 실행·Tools·Output` / `Harness: 기억·절차·동작 스택` / `우리 코드: 데이터·권한·검증·운영`.
- **구성·단계:** 1차 S24 레이어+3열 책임표. Logfire/Evals는 옆 관찰/평가 경로. Core→Harness→업무 계약.
- **설명/대본:** “이점은 타입 문법을 넘어 검증/실행 경계, 최종화, barrier, 보류/재개, 관찰 Hook을 같은 런타임 안에서 조합하는 데 있습니다. 그 경계를 이해하지 못하면 잘못된 종료·승인·상태 공유를 만들 수 있습니다.”
- **연결·근거:** 책임→Demo. [P01][P02][P24].

## S38 — 코드와 내부 전이를 PydanticAI Demo에서 잇는다

- **섹션·우선순위:** PydanticAI / Demo 2 · 필수.
- **핵심/화면:** `코드 → Graph → 최종 입력 → Tool 결과`; `Core 먼저, Harness는 선택 확장`.
- **구성·단계:** 좌 코드 정의 4블록, 중앙 S21, 우 request/tool/history/output. 진입 링크 하나. 조회→분기→확장 목표.
- **설명/대본:** “어느 정의가 모델 요청과 실행으로 연결되는지 보겠습니다. 종료 정책은 동일 고정 응답 시험으로 분리하며 live 모델 응답인 것처럼 보여주지 않습니다.”
- **Demo 진입·복귀:** 별도 뷰어, 기본 6–10분. 조회/후속 분석→노드/Deps→정책 시험→Harness 1개→이 장→SDKMAP. 압축·승인·위임 확장은 별도 기록 탐색.
- **근거:** [FLOW] Demo/보강. 실행 미검증.

## S39 — OpenAI Agents SDK

- **현재 장표:** OAI01–OAI07. Runner의 종료 분기, Agent.as_tool과 handoff, RunState 및 Guardrail을 비교한다.
- **발표 순서:** Microsoft Agent Framework 뒤.

## S40 — Claude Agent SDK

- **현재 장표:** CAS01–CAS06. Python SDK에서 CLI로 이어지는 호출, MCP 디스패치, 권한과 세션 재개를 설명한다.
- **발표 순서:** PydanticAI 뒤 SDKMAP을 지나 첫 번째.

## S41 — Google ADK

- **현재 장표:** ADK01–ADK07. Runner의 이벤트 저장, 상태 범위, ADK 2.x Graph를 설명한다.
- **발표 순서:** Claude Agent SDK 뒤.

## S42 — Microsoft Agent Framework

- **현재 장표:** MAF01–MAF07. Executor, 병렬 결과, 승인 응답과 체크포인트를 설명한다.
- **발표 순서:** Google ADK 뒤.

## S43 — 중앙 실행과 로컬 실행은 책임 배치가 다르다

- **섹션·우선순위:** Operations · 필수.
- **핵심/화면:** `중앙 Agent: 공통 운영·사용자 격리` / `로컬 Agent: 배포·업데이트·권한` / `모델 서비스: 부하·접근 제어`.
- **구성·단계:** 1차 레이어 문법 두 열. 중앙 client→API/queue→workers→Tools/DB·모델. 로컬 desktop→로컬 Tools/저장·중앙 모델 endpoint. 중앙→로컬→자원 경계.
- **설명/대본:** “중앙형은 인증·tenant·세션 순서·대기·격리, 로컬형은 설치·서명된 배포·업데이트·정책 버전이 필요합니다. 로컬 실행이어도 데이터가 모델 서버로 가므로 경로를 검토합니다.” CPU/메모리/Tool/모델 대기/GPU를 분리 측정, Worker/GPU 수 미정.
- **연결·근거:** 운영→업무 검증. [FLOW] 운영 질문. 설계 예시, 확정 구축안 아님.

## S44 — 분석에 필요한 검증 기준을 정한다

- **섹션·우선순위:** Application · 확장.
- **핵심/화면:** `같은 snapshot인가?` / `분모·기간·근거가 맞는가?` / `승인한 인자와 실행이 같은가?`.
- **구성·단계:** 1차 S28 Trace/Eval 두 패널. 실행/ID/결과 vs 계산 재현/인가/시간 분할. 증거→업무 검증→3차 질문. 수치 점수 없음.
- **설명/대본:** “실행이 보인다는 것과 분석이 옳다는 것은 다릅니다. 기간·snapshot이 바뀌면 같은 Tool이어도 근거가 달라집니다. 예측은 시간 누수 없이 기준 모형과 평가해야 합니다.”
- **연결·근거:** 검증→정리. [FLOW] BIN/타입/운영 질문. 설계 예시.

## S45 — 제공받는 실행과 직접 만드는 계약

- **섹션·우선순위:** Wrap-up · 필수.
- **핵심/화면:** `1. Hermes: 상태·기억·정책의 실제 동작` / `2. PydanticAI: 검증·실행·최종화·확장의 조합` / `3. 데이터·권한·업무 검증은 명시적 설계`.
- **구성·단계:** 1차 S29 핵심 3문장·다음 발표 연결. 작은 master 실루엣. 3문장→다음 담당자/3차, 청중용 Q&A 장 자동 추가 금지.
- **설명/대본:** “기본 제공 기능뿐 아니라 상태가 어디 남고 어느 분기에서 행동이 실행되는지를 비교해야 합니다. 다음에는 이 계약으로 실제 Agent를 만들고 검증하겠습니다.”
- **연결·근거:** 전체 발표 후 Q&A는 비공개 D. [FLOW] 목적.

---

# C. 발표자 개념 해설 — 슬라이드에 억지로 넣지 말 것

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

# D. 3명 전체 발표 후 Q&A 대비

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

# E. 실제 HTML 인터랙션 구현 명세 (구현자용)

## E-1. 파일·컴포넌트 권장 구조

이번에는 다음 파일을 구현하지 않는다. 후속 제작 시 웹 자산·실행/검증 스크립트·가이드는 루트 `html/` 아래에 둔다. 각 프레임워크의 기존 교재를 덮어쓰지 않는다.

```text
html/seminar-2/
  index.html                 # 발표용 stage, API key 불필요
  slides.js                  # S00–S45, reserved 제외 순회
  style.css                  # A-2 토큰
  notes.json                 # 청중 화면과 별도
  assets/                    # 로컬 폰트/도식
  demos/
    hermes/                  # 실제 런타임 관찰 backend + 별도 viewer
    pydanticai/              # Core부터 시작, Harness 확장 구분
    shared/                  # 데이터 계약·이벤트 schema·기록 뷰어 공통부
    fixtures/                # 합성 입력/정답/고정 모델 응답 시험
    traces/                  # 가림 처리된 실제 기록, 출처 manifest
  proxy/                     # Demo와 독립된 OpenAI 변환 서비스
  guides/
    run.md
    transfer-codex.md         # 10000 명시
    transfer-antigravity.md   # 10001 명시
  validation/
```

폴더는 제작 계획이다. 아직 실행 코드·설치 lock·명령은 없으므로 `python start_demo.py` 같은 존재하지 않는 실행법을 완료 보고에 적지 않는다. 기존 프로젝트 스택을 확인한 뒤 필요한 최소 의존성만 추가한다.

## E-2. 전역 상태·탐색

```ts
type PresentationState = {
  currentSlideId: string;
  buildStep: number;
  notesOpen: boolean;
  reducedMotion: boolean;
};
```

Next=현재 build 진행→다음 표시 슬라이드. Prev=역 build→이전 표시 슬라이드 마지막 build. reserved는 순회/목차/인쇄에서 제외. S38 다음 표시 슬라이드는 S43이다. Demo는 별도 탭의 고정된 returnSlideId로 복귀한다. 뷰어의 Space는 기록 cursor만 이동하며 실행을 다시 시작하거나 Tool을 재호출하지 않는다.

## E-3. Trace 이벤트·원본 경계

다음은 **관찰기용 설계 타입**이며 SDK 내장 클래스가 아니다.

```ts
type ObservationEvent = {
  id: string;
  sequence: number;
  time: string;
  runId: string;
  parentRunId?: string;
  requestId?: string;
  toolCallId?: string;
  layer: 'runtime' | 'provider' | 'tool' | 'storage';
  kind: string;
  payloadRef?: string;
  highlightNodeIds: string[];
  origin: 'live' | 'recorded' | 'fixture';
};
```

각 요청은 **프레임워크 객체→adapter 직후 JSON→프록시 수신 JSON**을 구분한다. requestId로 연결하되 retry attempt는 별도 식별한다. 인증 헤더는 기록 전에 제거하고 비밀값이 든 객체를 `repr`로 덤프하지 않는다. 프록시 upstream 모델 매핑은 운영 manifest에만 기록한다. viewer 요약을 ‘원문’이라고 부르지 않는다. Tool 시작/완료·검증 실패·승인 보류/재개·history/Memory 변경은 해당 런타임 관찰에서 채운다. 모델 프록시만으로 Python Deps/Graph/DB write를 안다고 가정하지 않는다.

관찰기 우선순위는 기존 callback/event/log→공개 Hook→adapter/transport wrapper다. 인수·반환·예외·취소를 그대로 전달한다. global monkey patch/Core fork는 최후의 수단이며 해당 버전 diff·동작 영향·해제 절차를 제공한다. 관찰을 위해 Tool 순서·승인·정책을 바꾸지 않는다.

## E-4. Demo 1 — Hermes

**목적:** 일반 Agent loop 재현이 아니라 실제 Hermes 요청·도구·세션·기억의 경계를 확인한다. 기존 ZIP 설치는 사용자 진술이므로 제작 시작 시 경로/OS/버전/Profile을 읽기 점검한다. 원래 Hermes는 계속 사용할 것이므로 별도 데모 Profile/합성 데이터·임시 도구를 사용하고 기존 DB/Memory/Skills를 덮어쓰지 않는다.

| 순서 | 입력·행동 | 볼 화면·실제 증거 | 복귀 연결 |
|---|---|---|---|
| 1 | 설치 버전·Profile·연결 점검 | 버전 manifest, schema 목록, endpoint 계약 | S04 |
| 2 | BIN-X 조회 | user append→최종 request의 system/history/tools→response | S05/S07 |
| 3 | Tool 처리 | call ID·인자·실행·반환·다음 request, 반복 횟수 | S06/S13 |
| 4 | 후속 근거 질문 | 누적 Context와 같은 snapshot 사용 여부 | S11 |
| 5 | 기억 요청 1개 | 실제 memory Tool·파일 diff·현재 snapshot/다음 세션 비교 | S10 |
| 6 | 필요한 확장 한 경로 | 위임 트리 또는 Skill/MCP 경로. 실제 발생한 것만 | S12/S14 |
| 7 | 종료 후 저장 확인 | 응답·세션 기록과 종료 원인 | S15 복귀 |

기본 6–8분은 조회/후속 분석/상태 경계로 완결한다. 압축·Subagent·MCP·Plugin·승인을 한 자연 실행에서 모두 강제하지 않는다. 각 확장은 별도의 이름 있는 시나리오와 사전 실제 기록을 준비한다. 압축이 안 일어나면 ‘이번 실행 미발생’. 캐시 속도/GPU 실험은 본 Demo 필수가 아니다.

뷰어는 좌 master 현재 영역, 중간 이벤트/요청별 payload, 오른쪽 Tool/저장 변화로 구성한다. 긴 payload는 요소별 보기와 가림 처리된 원문으로 나눈다. [H11][H12]의 관찰 접점이 특수 Tool을 놓치는지 점검한다.

**인수 기준:** 관찰 전후 같은 설정의 핵심 경로 유지, request-call-result 연결, Memory snapshot 구분, 중단·오류 표기, 실제 데이터/비밀정보 없음, recorder 해제 후 원래 Hermes 실행 가능. 모델 비결정성 때문에 완전 같은 문장을 요구하지 않는다. target PC 재현 여부는 별도 기록.

## E-5. Demo 2 — PydanticAI

**목적:** 개발 코드와 SDK의 추상화가 실제 노드·스키마·검증·실행으로 연결되는 것을 확인한다. Core 최소 실행을 먼저 완성하고 별도 Harness는 필요한 기능만 추가한다.

| 순서 | 입력·행동 | 볼 증거 | 연결 |
|---|---|---|---|
| 1 | Agent/Tool/Deps 코드 | 앱 정의와 SDK 영역 | S22 |
| 2 | 동일 BIN-X 조회·후속 질문 | Graph 노드, 최종 JSON, Tool schema, Python deps 비전송 | S23–S25 |
| 3 | 독립 조회 두 개 | task 시작/완료, emission/완료 순서, barrier | S26 |
| 4 | 별도 고정 응답 시험 | S28의 A/O1/B/O2에서 정책별 호출 여부 | S28 |
| 5 | 수정 가능한 잘못된 인자/Output | 검증 오류·ModelRetry·예산 한도 | S27/S29 |
| 6 | Hook 두 개와 History | 실제 합성 순서, 다음 Run 전달 범위 | S30/S31 |
| 7 | 선택 Harness 확장 | Memory 또는 compaction 전후 request/history. 필요시 Skill/MCP | S32–S34 |
| 8 | 승인/위임 확장 | pending ID/인자/결과, 부모-자식 경계 | S35/S36 |

기본 6–10분에서는 1/2/4/6 + Harness 한 경로를 선별한다. 나머지는 준비한 별도 확장 기록에서 볼 수 있게 한다. EndStrategy를 자연 모델에 매번 같은 순서로 출력하라고 강요하지 말고 고정 응답 시험으로 검증한다. 실제 SDK executor가 고정 모델 응답을 처리한 시험은 실제 런타임 시험이지만 **live LLM 응답**은 아니다.

예측은 `forecast_bin`의 방법·분할·평가가 구현·검증된 후만 포함한다. 조회 성공만으로 예측·원인 분석까지 성공한 것으로 표시하지 않는다. API 실패 시 사용한 실제 기록의 replay로 전환하고 origin/모델/버전/일시를 표시한다.

**인수 기준:** Graph/Provider/Tool ID 연결, 모델 입력에 key/DB 객체가 없음, graceful 후행 Function 동작과 retry 예외 시험, async/sync/barrier 구분, 인자 변경/승인 거절/재개, history와 압축 원본 보관 구분, 부모/자식 공유 상태 명시. Hook 관찰이 정책을 우회하지 않아야 한다.

## E-6. 모델 endpoint와 별도 프록시 계약 — 두 지시서 공통

### 역할·포트

| 지시 대상 | Hermes Demo | PydanticAI Demo | 현재 PC의 별도 서비스 | 이관 PC |
|---|---|---|---|---|
| Codex | `http://127.0.0.1:10000/v1` | 같은 10000 | 수신→OpenAI API | 같은 10000→vLLM |
| Antigravity | `http://127.0.0.1:10001/v1` | 같은 10001 | 수신→OpenAI API | 같은 10001→vLLM |

**포트는 프레임워크별이 아니라 구현 지시 대상별이다.** 두 포트는 별도 프로세스 또는 단일 서비스의 별도 listener로 구현 가능하나 외부 계약은 동일해야 한다. Demo viewer/Tool/MCP 서버 포트로 이 두 포트를 사용하지 않는다.

```text
Demo backend (Hermes 또는 PydanticAI)
    -- OpenAI-compatible Chat Completions --> 127.0.0.1:10000 또는 :10001

현재 PC의 별도 프록시
    -- 서버 측 실제 OpenAI key + 실제 model 매핑 --> OpenAI API

이관 PC의 같은 주소/경로
    -- 대상 환경 설정 --> 실제 vLLM 또는 그 앞 프록시
```

Demo는 `SEMINAR_MODEL_BASE_URL`, `SEMINAR_MODEL_ID=demo-model`, `SEMINAR_PROXY_TOKEN`만 받는다. Hermes 실제 설정 필드는 설치 버전의 custom/OpenAI-compatible provider 설정에 매핑하고 `api_mode=chat_completions` 지원을 점검한다. PydanticAI는 C-2의 명시 OpenAIChatModel을 쓴다. 한쪽 코드에 `if openai / else vllm` 분기를 만들지 않는다.

### 현재 PC에서 별도 서비스가 할 일

1. 기본은 loopback 두 listener. 수신 토큰은 실제 OpenAI key와 다른 로컬 토큰이다. OpenAI key는 **프록시 프로세스 환경 `OPENAI_API_KEY`**에만 주입한다. 브라우저 JS·Agent prompt·repo·Trace·샘플 설정에 실제 값을 넣지 않는다.
2. `POST /v1/chat/completions`를 같은 API 형식의 OpenAI upstream으로 전달한다. 수신 Authorization은 검증 후 제거하고 upstream Authorization을 서버에서 새로 만든다. upstream URL·실제 model ID 매핑·인증은 프록시 소유다.
3. `GET /v1/models`는 허용한 별칭만 제공한다. 프록시 설정에 별칭↔실제 모델 매핑을 둔다. 응답의 model 필드 정규화가 필요하면 이를 유일한 공개 매핑으로 문서화하고 Tool 결과·내용·ID는 바꾸지 않는다.
4. messages/tools/tool_choice/Tool call ID/finish_reason/stream/usage/오류 의미를 보존한다. 미지원 필드는 조용히 삭제하지 말고 명시 오류 또는 검증된 변환 정책을 기록한다. `max_tokens` 계열 등 모델별 차이는 해당 upstream으로 실제 시험한다.
5. SSE를 모아서 최종 JSON으로 바꾸지 않는다. delta·Tool 인자 조각·종료·사용량을 검증한다. 연결 종료·취소·타임아웃·429/5xx 의미를 유지하며 독자적 무한 retry를 넣지 않는다. 중간 실패 후 stream을 처음부터 재생하지 않는다.
6. 프록시는 Agent loop·Tool 실행·Memory 저장을 대신하지 않는다. 인증·민감 헤더는 log 전에 제거한다. actual upstream/provider/모델은 운영 manifest에서 확인 가능해야 한다. 청중에게 현재 PC의 실행을 ‘실제 vLLM 실행’이라고 설명하지 않는다.

### 이관 계약과 호환성 경계

같은 endpoint·별칭·수신 인증 계약을 대상 PC의 vLLM/앞단 프록시에서 제공하면 Demo 코드는 유지한다. 호스트가 다르거나 별칭/인증이 달라지는 환경은 해당 설정 필드만 변경하고 전후 값을 가이드에 명시한다. 현재 PC용 OpenAI key·프록시 비밀 설정은 이관하지 않는다.

Chat Completions/Tool calling/대화 replay를 기본 공통 부분으로 사용한다. OpenAI 호스팅 Tool·Provider 전용 conversation ID·native compaction을 기본 경로의 필수로 하지 않는다. vLLM의 모든 버전이 다른 API를 지원하지 않는다는 뜻은 아니다. 이번 이관의 공통 계약을 좁혀 검증하는 결정이다. [P07][V02]

같은 HTTP 인터페이스여도 모델의 Tool 선택·JSON Schema 준수·chat template/parser·병렬 요청·스트림·Context 한도는 다를 수 있다. 모델 답변·예측 정확도·캐시 성능까지 동일하다고 보장하지 않는다.

### 구현 후 필수 계약 시험

| 시험 | 통과 기준 |
|---|---|
| 두 listener | 각각 models/기본 호출, 지정 토큰, 별칭 정상. 10000/10001 혼동 없음 |
| 기본/멀티턴 | messages 내용/순서 유지, 앱 이력으로 후속 질문 정상 |
| Tool 왕복 | schema→모델 call→실제 Tool→동일 call ID result→후속 응답 |
| 병렬/구조화 | 지원 모델에서 다중 call·schema 출력, 미지원은 명시 실패 |
| SSE/취소 | 즉시 delta, Tool args 조합, terminal/usage, 연결 중단 후 정리 |
| 오류·재시도 | 인증/별칭/429/5xx/timeout 보존, 중복 실행/무한 retry 없음 |
| 비밀 경계 | 브라우저·Demo 설정·Trace·오류 본문에 실제 OpenAI key 없음 |
| vLLM 이관 | 같은 계약으로 기본/Tool/stream 재시험. 미접근이면 미검증 표기 |

## E-7. 실제 결과로 추출할 실행·이관 문서

후속 제작자는 **실제로 구현·검증한 뒤** run.md와 두 transfer 문서를 완성한다. 이번 설계가 이미 실행 가능한 명령집이라고 표현하지 않는다.

- 시작: cwd·OS/Python·패키지/소스 버전·설치/ZIP 경로·포트 점유·기존 Profile 확인. 자동 설치는 격리 가상환경, 기존 사용자 데이터 보존.
- 실행: 각 명령의 정확한 cwd/파일·환경변수 **이름과 placeholder**·실행 순서(프록시→backend→viewer)·정상 로그/화면·종료·원복. 숨김 helper로 실행하며 사용자 창을 임의 다수 열지 않는다.
- 시연: S15/S38 진입·질문·Space 단계·관찰 패널·예상 분기·기록 선택·슬라이드 복귀·데이터 reset.
- 이관: 이동할 코드/lock/합성 데이터/가림 Trace/manifest, 이동하지 않을 secrets/Profile/기존 DB, 수정할 파일/필드/전후 형식, 실패 판단·원복.
- 검증: 현재 PC의 실제 upstream, 모델·설정·오류·관찰기 영향과 target PC 검증 여부를 분리. ‘qwen 3.8 수준’은 정확 모델이 미확정이므로 적용 역량을 단정하지 않고 작은 단계와 검사 명령을 제공.

### Codex에 전달할 핵심 지시

> 두 Demo의 모델 base URL은 `http://127.0.0.1:10000/v1`, model은 `demo-model`이다. 그 뒤에는 vLLM-compatible 서비스가 있다고만 가정하라. Demo는 실제 upstream/key를 몰라야 한다. 현재 PC OpenAI 변환 서비스는 별도 proxy 모듈로 두고 서버 측 환경으로 인증한다. 목표 PC에서도 같은 10000 계약을 유지한다. 실제 실행 뒤 검증 결과와 이관 절차를 추출하라.

### Antigravity에 전달할 핵심 지시

> 두 Demo의 모델 base URL은 `http://127.0.0.1:10001/v1`, model은 `demo-model`이다. 그 뒤에는 vLLM-compatible 서비스가 있다고만 가정하라. Demo는 실제 upstream/key를 몰라야 한다. 현재 PC OpenAI 변환 서비스는 별도 proxy 모듈로 두고 서버 측 환경으로 인증한다. 목표 PC에서도 같은 10001 계약을 유지한다. 실제 실행 뒤 검증 결과와 이관 절차를 추출하라.

---

# F. 조사·참고자료와 적용 범위

## F-1. 내용 원본과 조사 범위

- **[FLOW]** [0_2차_세미나_발표_흐름.md](flow.md): 전체 발표 순서·질문·추가 검증 요청·Demo 요구. 이번 데모 계약을 먼저 개정했다.
- **[DESIGN]** [1차 blueprint](../../../archive/presentations/seminar-1/blueprint.md): A~G 구조·정보 위계·색·도식·노트 분리·탐색의 기준.
- [Hermes 추가 코멘트](../../../study/hermes/Hermes_Agent_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md)와 [PydanticAI 추가 코멘트](../../../study/PydanticAI/PydanticAI_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md)는 원문의 보강 의도와 관련된 snapshot/검색/병렬/최종화/승인 설계 해석을 확인했다. 이를 공식 제품 보장이나 실측 결과로 취급하지 않는다.
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

# G. 최종 제작 전 발표자·구현자 공동 체크

## G-1. 이번 Markdown 산출물 검수

- [x] 내용 원본은 2차 흐름이며 기존 종합 비교를 임의로 합치지 않았다.
- [x] 1차 A~G 문서 구조·의미색·여백·텍스트 위계·레이아웃/도식 문법·노트/키보드를 유지했다.
- [x] 토글/드롭다운/불필요한 청중 텍스트를 순차 강조·노트로 치환했다.
- [x] Hermes·PydanticAI를 중심으로 설명하고 네 SDK는 실행 경계와 차별점 위주로 비교한다.
- [x] 추가 보강 질문을 F-4에 매핑하고 중요한 정정/충돌을 F-3에 남겼다.
- [x] SDK 비교 장표를 본편에 넣고 기존 Demo 진입·복귀를 유지했다.
- [x] 포트는 지시 대상별이고 실제 key/upstream은 별도 프록시에만 둔다.
- [x] 실제 실행·그림 예시·fixture·미검증을 구별했다.

## G-2. 후속 제작 후에만 체크할 항목

- [ ] 1920×1080/1280×720/휴대폰 viewport에서 16:9·텍스트 겹침·도식/코드 overflow 검수.
- [ ] 모든 표시 번호/목차/Next/Prev/build/노트 비공개·복귀 링크·Sources 검수.
- [ ] 실제 설치 버전/OS/Profile·Harness 호환 조합 고정 및 API import/실행 확인.
- [ ] 실제 Hermes/PydanticAI Trace와 관찰기 비간섭·오류·취소·복구 검증.
- [ ] 두 프록시 포트 계약·SSE·인증 분리·비밀 로그 검사.
- [ ] target PC의 vLLM Tool/parser·schema·stream·한도 실험. 미접근이면 미검증 유지.
- [ ] 합성 BIN 정의·분모/기간·예측 평가·안전한 승인 Mock 확인.
- [ ] 실제 결과 기반 run/transfer 두 가이드, reset·원복·실패 replay 준비.

**남은 확인 사항:** 발표 시간, 실제 사용할 패키지/Harness 버전, 대상 PC 설치/모델 기능, 합성 예측 데이터·정답, 실제 서비스 포트 점유 상태다. 이 답이 없어도 이번 발표 설계는 읽고 제작할 수 있지만 실행 성공으로 표시할 수는 없다.
