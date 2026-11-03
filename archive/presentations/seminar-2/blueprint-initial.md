# Agent Framework 세미나 2차 — 실행 구조의 차이에서 개발·운영 판단까지

> **문서 성격:** 최종 HTML 슬라이드 제작용 블루프린트. 화면 콘텐츠·시각 구성·단계 전개·발표자 설명·근거·검수 기준을 포함한다. 이 문서를 읽는 구현자가 다시 발표 내용을 기획할 필요가 없도록 한다.  
> **작성일:** 2026-11-03. 기술 분석 기준은 아래 C 문서의 2026-10-31 조사와 고정 버전이다. 작성일의 최신 기능을 조사했다는 뜻은 아니다.  
> **내용 원본 C:** `Agent_Framework_7종_최종_종합_비교_분석.md`  
> **디자인 원본 D:** `agent_framework_seminar_1_slide_blueprint.md`  
> **프로젝트 루트:** `C:\Users\namws\OneDrive\Desktop\study_for_agent_framework`  
> **편집 원칙:** C의 기술적 의미·조건·한계를 유지한다. D에서는 디자인과 설명 방식만 가져온다. 1차의 Agent/Core/Tools/Orchestration 기초 설명은 이미 청중이 안다고 가정한다.  
> **산출 범위:** 이번 산출물은 Markdown 한 개다. 발표 앱·PPT·데모를 제작하거나 실행한 결과가 아니다.

# A. 제작자와 발표자가 먼저 공유할 기준

## A-1. 발표 목적과 최종 메시지

이번 발표는 일곱 제품의 기능 소개가 아니라 **이미 배운 구성요소가 각 실행 시스템에서 어떻게 구현되고, 개발자의 책임을 어떻게 바꾸는지 비교하는 발표**다.

청중이 발표 후 다음 질문에 답할 수 있어야 한다.

1. 다음 행동과 반복을 누가 통제하는가?
2. 모델 요청·도구 실행·정책 검사는 어디에서 만나는가?
3. 대화·실행 상태·기억·외부 변경은 어디에 남는가?
4. 실패·중단·재개 시 무엇이 다시 실행되는가?
5. 공개 소스로 확인한 것과 공식 동작 계약만 알려진 것은 무엇인가?

마지막에 남길 문장: **“프레임워크를 선택한다는 것은 어떤 실행 책임을 맡기고 어떤 계약을 우리 애플리케이션에 남길지 결정하는 일이다.”** 근거: C 독자 안내, §§1–3, 30, 34–39.

Hermes와 PydanticAI는 깊게 설명한다. 나머지는 두 기준점에 대한 차별점을 설명한다. 순서는 **Hermes → Claude Code → PydanticAI → OpenAI Agents SDK → Claude Agent SDK → Google ADK → Microsoft Agent Framework**다. 이 순서는 우수성 순위가 아니다. 일곱 기술은 동일 층위의 경쟁 제품도 아니다.

## A-2. 내용·근거의 사용 규칙

- 이 문서의 `C §n`은 내용 원본의 번호 붙은 절이다. `D A-2` 등은 디자인 원본의 절이다. 아래 G의 경로·공식 링크 인덱스와 함께 사용한다.
- **[SRC]** 고정 버전 공개 소스, **[DOC]** 공식 동작 계약, **[INF]** 설계 해석·권고, **[UNV]** 추가 확인 필요, **[PSEUDO]** 의사코드라는 원문의 구분을 유지한다. 원문이 [DOC]로 설명한 내용을 [SRC]로 승격하지 않는다.
- 슬라이드 하단 Sources에는 짧은 `C §4.1 · v0.22.5 · SRC`처럼 표시하고 전체 파일·URL은 노트에 둔다. [INF] 사례는 화면에 `설계 예시`라고 표시한다. 원문 안에서도 근거 수준이 혼합된 경우 문장별로 연결한다.
- 이번에는 외부 조사로 내용을 갱신하지 않았다. C에 있는 링크를 계승한다. “실행 검증”, “최신”, “가장 빠름”, “정확도 1위” 등 원문에 없는 사실을 추가하지 않는다.
- 의사코드·호출 경로·설명용 숫자·가상 사례는 실제 API 실행 로그와 구분한다. 공개된 함수명은 유지하되 축약된 연결은 `대표 경로`라고 표시한다.
- Claude Code의 비공개 엔진과 공개 Claude SDK 래퍼를 하나의 공개 Python 런타임처럼 그리지 않는다. SDK와 CLI를 두 독립 엔진으로 집계하지 않는다.
- 반도체 사례는 도메인 설계 질문을 구체화하는 예시다. 검증된 공정 성과·인과·예측 정확도를 주장하지 않는다.

## A-3. 결과물 형태와 정보 밀도

1. **한 화면=한 슬라이드**, 16:9. 본문 `S00`–`S40` 41장, 상세 부록 `X01`–`X10` 10장. 부록은 기본 발표 순회에서 제외한다.
2. 각 슬라이드 데이터는 `id`, `section`, `priority`, `title`, `onScreen`, `visual`, `buildSteps`, `speakerNotes`, `sourceRefs`, `appendixLinks`를 분리한다. 화면에는 아래 **화면** 항목과 도식 레이블만 넣는다.
3. 발표자 대본·기술 설명·검증 한계를 본문 카드에 몰아넣지 않는다. `N`으로 여는 노트와 별도 발표자 보기로 제공하되 일반 청중 화면에서는 숨긴다.
4. 한 화면은 중심 주장 하나, 본문 문구 3–5개, 도식의 주 경로 하나를 기본으로 한다. 긴 표는 작은 글자로 압축하지 말고 비교 행을 단계적으로 강조하거나 부록으로 보낸다.
5. 일곱 기술 각각 **전체 아키텍처 → 해당 영역 확대** 순서를 지킨다. 구조도는 구성 관계, 시퀀스는 시간 순서, 상태도는 전이 조건을 나타낸다. 세 종류를 같은 화살표 의미로 섞지 않는다.
6. 슬라이드 앱의 모든 설명용 인터랙션은 로컬 고정 데이터로 동작한다. 실제 Agent 호출은 별도 데모 페이지의 책임이다. 발표 앱 자체는 API key 없이 실행 가능해야 한다.
7. 본문 41장 전체는 설명량이 많다. **약 70–85분, 선택 데모 10–15분 별도**를 리허설 전 편집 가정으로 둔다. 시간 제한이 주어진 사실은 아니다. 분량 축소는 A-7 경로로 수행하고 원문의 조건을 삭제하여 맞추지 않는다.

## A-4. 디자인 시스템 — 1차와 이어지는 시각 언어

| 요소 | 확정 지시 |
|---|---|
| 톤 | Tech conference / clear systems thinking. 깔끔한 어두운 배경, 도식 중심. 네온·유리 카드·장식적 3D 금지. |
| 배경·본문 | 배경 `#0B1020`, 본문 `#EFF4FF`, 보조 `#9EACC8`, 선 `#33415D`. |
| 의미색 | Model 파랑 `#60A5FA`, Runtime 보라 `#B794F4`, Tool 초록 `#34D399`, Context/Memory 주황 `#FDBA74`, Risk 빨강 `#FB7185`, Success 민트 `#5EEAD4`. |
| 색의 사용 | 제품마다 브랜드 색을 부여하지 않는다. 어느 제품에서도 같은 역할은 같은 색이다. 상태는 텍스트·아이콘으로도 구분한다. |
| 여백 | 가로 7%, 세로 6%. 상단 작은 section label, 하단 페이지·섹션·Sources. |
| 글자 | 1920×1080 기준 제목 38–54px, 핵심 문구 22–30px, 보조 17–22px, 코드 18–22px. 1280×720에서 실제 읽기와 겹침을 검수한다. |
| 제목 | 결론형 한국어 중심. 기술 이름·식별자는 영어 유지. 각 장 제목은 아래 명세대로 사용한다. |
| 도식 | SVG/CSS+실제 텍스트로 편집 가능하게 구현한다. 노드 ID·위치를 재사용하고 확대 영역만 바꾼다. 스크린샷 속 작은 글자로 도식을 대체하지 않는다. |
| 경계 | 실선=실행/명시적 전송, 점선=설정·관찰·선택적 연결. 프로세스/저장소/외부 시스템은 컨테이너로 구분하고 범례를 둔다. 점선 자체가 보안 격리를 뜻하지 않는다. |
| 전환 | 기본 0.25–0.45초 ease-out, 연속 전환의 체감 대기는 짧게. 자동 재생은 Pause/Reset, Reduced motion과 비애니메이션 최종 상태 제공. |

아키텍처 확대 시 비활성 영역은 대비를 낮추되 텍스트 판독이 불가능할 정도로 흐리게 하지 않는다. 핵심 경로는 밝은 선+단계 번호로 강조한다. 연결이 끊기거나 역할 주체가 바뀌는 이동 효과를 사용하지 않는다. 근거: D A-1/A-2, E.

## A-5. 통일된 도메인 예시 — 제품 사실과 분리

**[INF] 발표용 설계 예시**로 “Lot A의 지정 BIN 비율을 조회 → 이전 기간·측정 근거를 비교해 설명 → 다른 데이터 구간으로 예측”을 사용한다. 실제 데이터·수치·예측 모델은 아직 정해지지 않았다.

- 고정 식별자: `LOT-A`, `BIN-X`, `snapshot-v1`, `SOP-r3`, 사용자 `analyst-A`.
- 개념 도구: `lookup_bin_rate`, `compare_measurements`, `predict_bin_rate`, `publish_report`. **전부 발표용 가상 함수명이며 어느 제품의 내장 API도 아니다.**
- 조회 출력은 비율 자체와 함께 분모·기간·Snapshot ID가 필요하다고 설명한다. 수치는 넣지 않는다. 예측 품질도 임의로 표시하지 않는다.
- 정책 사례: 조회는 허용된 범위만, 보고서 발행은 정확한 보고서 버전·대상·승인과 연결한다. 발표의 고정 인터랙션은 실제 발행 API를 호출하지 않는다.
- 동일 Lot이라도 Snapshot·SOP·기간이 다르면 같은 근거라고 볼 수 없다. 이 질문을 Memory·병렬·승인·복구·평가에서 필요한 경우만 회수한다.

이 예시는 원문의 일반적 데이터·정책·재현성 논점을 일관된 상황으로 표현하기 위한 재구성이다. 제품별 동작을 이 예시에 맞추려고 바꾸지 않는다. 근거: C §§6–8, 13–18, 22, 31–36 및 기존 발표의 도메인 적용 의도.

## A-6. 조작·노트·별도 데모 연결

- `→/Space`: 남은 build step을 먼저 진행하고 마지막 단계 이후 다음 장으로 간다. `←`는 역순이며 이전 장 복귀 시 마지막 단계로 이동한다.
- 목차 점프는 안정적인 slide ID를 사용한다. `N` 노트, `R` 현재 그림 초기화, `Esc` 최상위 오버레이 닫기를 제공한다. 입력창·노트 텍스트 편집 중에는 발표 키가 가로채지 않는다.
- 단계 카운터 `k/n`과 본문 페이지 `n/41`은 분리한다. X 부록은 별도 번호이며 발표 순회와 페이지 분모에 끼워 넣지 않는다.
- 부록으로 이동할 때 원래 slide ID·build step을 기억하고 `발표로 돌아가기`를 제공한다.
- `S11`은 Demo 1(Hermes), `S21`은 Demo 2(PydanticAI)의 연결 장이다. 슬라이드에는 관찰 질문과 이동·복귀만 둔다. 실제 런타임을 슬라이드에 내장하지 않는다.
- 데모가 준비되지 않았으면 해당 장의 **설명용 경로도**만 제시하고 “실제 실행 기록 미연결”로 표시한다. 준비되지 않은 링크를 클릭 가능하게 두거나 가상 Trace를 실제 기록으로 바꾸지 않는다.

## A-7. 전체 목차와 발표 경로

`핵심`은 축약 발표에도 유지, `확장`은 시간에 따라 부록으로 보내도 되는 본문, `연결`은 준비 상태에 따라 설명/별도 데모로 운용한다.

| ID | 제목 | 역할 |
|---|---|---|
| S00 | 같은 Agent 구성요소, 다른 실행 책임 | 핵심·Opening |
| S01 | 일곱 기술은 같은 층위의 경쟁 제품이 아닙니다 | 핵심·지도 |
| S02 | 비교 기준은 기능 개수가 아니라 다섯 가지 소유권입니다 | 핵심·질문 |
| S03 | Hermes는 작업 실행에 필요한 환경을 함께 제공합니다 | 핵심·전체 구조 |
| S04 | Hermes의 Tool 요청은 저장·실행·결과 기록으로 이어집니다 | 핵심·실행 |
| S05 | Hermes의 Prompt는 세션·도구·기억과 함께 구성됩니다 | 핵심·입력 |
| S06 | 캐시는 계산을 재사용하고, 압축은 입력을 다시 편집합니다 | 핵심·Context |
| S07 | Hermes의 Memory와 대화 검색은 다른 경로입니다 | 핵심·상태 |
| S08 | Skill·Tool·MCP·Plugin은 서로 다른 확장 책임입니다 | 확장·확장점 |
| S09 | Hermes의 병렬 Tool과 Subagent는 다른 실행 단위입니다 | 핵심·병렬/위임 |
| S10 | Hermes를 활용해도 권한과 운영 정책은 확인해야 합니다 | 확장·정책/플랫폼 |
| S11 | Demo 1: Hermes의 실제 요청과 실행을 연결해 봅니다 | 연결 |
| S12 | Claude Code는 공개된 Harness 계약을 중심으로 비교합니다 | 핵심·전체 구조 |
| S13 | Claude Code의 협업과 권한은 사용 계약으로 읽어야 합니다 | 핵심·차이 |
| S14 | PydanticAI는 실행 경로에 검증 계약을 결합합니다 | 핵심·전체 구조 |
| S15 | 내부 Graph는 모델 요청과 Tool 처리의 경계를 드러냅니다 | 핵심·실행 |
| S16 | Tool Schema·Deps·실행 인가는 같은 계약이 아닙니다 | 핵심·입력/도구 |
| S17 | 최종 출력과 Tool이 함께 나오면 종료 정책이 중요해집니다 | 핵심·종료 |
| S18 | 검증 Retry와 병렬 장벽은 실행 비용과 부작용을 바꿉니다 | 핵심·실행 정책 |
| S19 | Core·Capabilities·Harness와 앱의 책임을 구분합니다 | 핵심·개발 범위 |
| S20 | Deferred 승인은 중단된 요청을 다시 연결하는 계약입니다 | 핵심·재개 |
| S21 | Demo 2: 개발 코드와 내부 실행 경계를 함께 봅니다 | 연결 |
| S22 | OpenAI SDK는 다음 실행을 NextStep으로 나눕니다 | 핵심·전체 구조 |
| S23 | Agent-as-Tool은 결과를 돌려주고 Handoff는 제어권을 넘깁니다 | 핵심·위임 |
| S24 | OpenAI Guardrail과 RunState는 적용 범위를 구분해야 합니다 | 핵심·정책/상태 |
| S25 | Claude Agent SDK는 Python과 CLI Runtime 사이를 연결합니다 | 핵심·전체 구조 |
| S26 | SDK가 소유하는 것은 프로세스·스트림·콜백의 수명입니다 | 확장·경계 |
| S27 | ADK는 Flow의 실행과 Runner의 이벤트 관리를 나눕니다 | 핵심·전체 구조 |
| S28 | ADK의 Final Event는 업무 전체 완료와 다를 수 있습니다 | 핵심·상태/Workflow |
| S29 | Microsoft에는 Tool·Harness·Workflow 반복이 겹쳐 있습니다 | 핵심·전체 구조 |
| S30 | Middleware는 어느 단계에서 정책을 강제하는지가 중요합니다 | 핵심·정책 |
| S31 | Superstep과 Checkpoint는 외부 트랜잭션이 아닙니다 | 확장·Workflow |
| S32 | 같은 ‘저장’이라도 다시 답할 수 있는 질문이 다릅니다 | 핵심·종합 |
| S33 | 복구 후 같은 Tool을 실행해도 되는지는 별도 판단입니다 | 핵심·실패 사례 |
| S34 | Cron·Background·Queue·Resume는 다른 실행 계약입니다 | 확장·운영 |
| S35 | 응답 전달과 Agent 실행 상태는 분리해야 합니다 | 핵심·Serving |
| S36 | 모델 교체는 URL보다 기능 계약을 먼저 확인해야 합니다 | 핵심·호환 |
| S37 | Trace로 경로를 설명하고 네 층의 평가로 검증합니다 | 핵심·평가 |
| S38 | 직접 만든다면 제품보다 책임 인터페이스를 가져옵니다 | 핵심·설계 |
| S39 | 선택은 요구조건과 반대급부의 조합입니다 | 핵심·판단 |
| S40 | 맡길 책임과 우리가 지킬 계약을 결정합시다 | 핵심·Closing |

**전체 경로:** S00–S40, 데모 별도. **축약 경로:** S08/S10/S26/S31/S34를 부록으로 이동하고 S11/S21은 관찰 질문만 짧게 회수한다. **45–55분 수준의 압축이 필요하면** S02를 S01 노트, S05–S07을 핵심 화면만, S18은 S17 노트, S24는 S22 노트, S32–S33을 연속 사례로 축약한다. 모든 일곱 기술의 전체 아키텍처와 차이·한계는 유지한다. 시간 수치는 리허설 가정이며 실제 소요 측정값이 아니다.

# B. 슬라이드별 상세 명세

각 장의 **화면**은 청중용 확정 문구다. **그림·단계**는 제작 명세, **노트·연결**은 발표자용이다. 도식의 실제 API 세부를 원문 이상으로 추가하지 않는다.

## S00 — 같은 Agent 구성요소, 다른 실행 책임

- **화면:** `Agent Framework · Inside the Runtime` / `7개 기술의 실행 구조와 개발·운영 판단` / `누가 판단하고, 실행하고, 저장하고, 복구하는가?`
- **그림·단계:** 중앙 제목, 아래 일곱 기술명을 작고 동등한 크기로 배치. ① 제목 ② 다섯 동사 ③ Hermes·PydanticAI만 밑줄 강조. 로고·기능 카드 벽은 사용하지 않는다.
- **노트·연결:** “기초와 Tool·Orchestration은 이미 배웠습니다. 오늘은 같은 이름의 기능이 실제 제품에서 어떤 책임으로 구현되는지 보겠습니다.” 다음 장에서 일곱 기술의 위치를 먼저 구분한다.
- **근거:** C 독자 안내, §§1–3, 39. 디자인 D S01/A-2만 참고.

## S01 — 일곱 기술은 같은 층위의 경쟁 제품이 아닙니다

- **화면:** `완성형 Harness: Hermes · Claude Code` / `실행 Framework/SDK: PydanticAI · OpenAI · ADK · Microsoft` / `Claude Agent SDK → Claude Code Runtime` / `제품명보다 실제 제어권을 비교합니다`
- **그림·단계:** 2개 묶음+SDK→CLI 연결의 위치도. 아래 Model/Provider/Environment를 공통 의존 영역으로 배치. ① Harness 묶음 ② 조립형 묶음 ③ Claude SDK 연결 ④ 상호 배타적 분류가 아니라는 작은 설명. 성숙도·성능 축처럼 보이는 좌표축을 넣지 않는다.
- **노트·연결:** “SDK 안에도 Runner가 있고 Framework 안에도 Harness가 있습니다. 특히 Claude Code와 Claude SDK는 독립 엔진 두 개가 아닙니다.” 네 제품을 완전히 같은 개발 인터페이스라고 단정하지 않는다. PydanticAI Harness 등 선택적 계층은 뒤에서 별도 설명한다.
- **근거:** C §§1, 1.1, 2, 24–29.

## S02 — 비교 기준은 기능 개수가 아니라 다섯 가지 소유권입니다

- **화면:** `행동: 누가 다음 단계를 결정하나?` / `상태: 무엇을 어디에 남기나?` / `권한: 누가 실행을 허가하나?` / `복구: 실패하면 무엇을 다시 하나?` / `근거: 어디까지 코드로 보이나?`
- **그림·단계:** 왼쪽 질문 5개, 오른쪽 이후 구조도의 작은 기준 축. ① 행동/상태 ② 권한/복구 ③ 근거. 구석에 `SRC · DOC · INF · UNV` 범례만 둔다.
- **노트·연결:** 일반 Agent 구조를 다시 강의하지 않는다. “이 질문을 일곱 기술에 반복해 적용하면 무엇을 기본으로 받고 무엇을 직접 만들어야 하는지 보입니다.” 근거 수준은 판단의 범위이며 제품 점수가 아니다.
- **근거:** C 독자 안내, §§2–3, 37.1.

## S03 — Hermes는 작업 실행에 필요한 환경을 함께 제공합니다

- **화면:** `AIAgent Loop` / `Prompt · Tools · Memory · Session` / `Gateway · Cron · 실행 Backend` / `완성형 Harness의 공개 구현을 읽습니다`
- **그림·단계:** `arch-hermes` 전체도. 위 Host(CLI/Gateway/Cron) → 중앙 AIAgent → 오른쪽 Provider/Model 및 Tool Executor/Backend, 왼쪽 Prompt Builder·Memory·Skills, 아래 SQLite Session/FTS5. Registry/MCP/Plugin은 Tool 확장 영역에 둔다. ① 입력/Loop ② 모델/도구 ③ Context/저장 ④ Gateway/Cron·정책 경계. Context와 저장소를 같은 박스로 합치지 않는다.
- **노트·연결:** “작은 Agent 클래스만 제공하는 접근과 달리 일상 작업의 실행 환경을 묶습니다. 그래서 빠르게 연결할 수 있는 기능이 많지만 정책·설정·영속성의 이해 부담도 커집니다.” 다음은 중앙 Loop 확대다.
- **근거:** C §§1–2, 4.1, 23; 공식 링크 G-H.

## S04 — Hermes의 Tool 요청은 저장·실행·결과 기록으로 이어집니다

- **화면:** `run_conversation → 요청 준비 → Provider 호출` / `응답 분류 → Tool Intent 저장 → Handler 실행` / `Tool Result 기록 → 다음 호출 / 종료` / `기록과 외부 실행의 연결을 확인합니다`
- **그림·단계:** S03 Loop를 확대하여 Model/Runtime/Store/Tool 4레인 시퀀스. ① 모델 요청·응답 ② Intent 저장 ③ Handler 실행·결과 저장 ④ 다음 반복·최종 분기. 별도 작은 Stop 가지에 예산/취소/정책/오류를 배치한다. Intent 기록만으로 외부 실행과 원자적 트랜잭션이 완성된 것처럼 그리지 않는다.
- **노트·연결:** `conversation_loop.py`, `turn_*.py`, `turn_tool_round.py`는 실제 소스 식별자다. 이 그림은 축약 대표 경로다. “모델이 말한 것, 실제 실행한 것, 저장된 것은 다른 사건입니다. 중간에 장애가 나면 어느 사건까지 완료됐는지 알아야 합니다.” 복구의 일반 문제는 S33으로 회수한다.
- **근거:** C §§4.1, 5, 23, 33; G-H.

## S05 — Hermes의 Prompt는 세션·도구·기억과 함께 구성됩니다

- **화면:** `stable → context → volatile` / `지침 · Tool Schema · Skill · History · 검색 결과` / `저장된 정보 전체가 매번 전송되지는 않습니다`
- **그림·단계:** `arch-hermes`의 Prompt Builder 확대. 상단에 논리 계층, 하단 Provider Request 상자. ① 안정 지침 ② 프로젝트/사용자 맥락 ③ 선택된 정보·최근 이력 ④ Provider별 표현 변환. 물리적인 API 필드 순서를 확정하는 도식으로 그리지 않는다. `stable/context/volatile`과 A–I 분석 항목은 서로 다른 분해 관점이라고 노트에 둔다.
- **노트·연결:** “다음 모델 호출에 무엇이 들어가는지 보려면 Prompt Builder뿐 아니라 History와 Tool 목록, Provider 변환도 함께 봐야 합니다.” 모든 구성 요소가 매번 로드된다는 연출을 피한다. SOP가 바뀌면 갱신 시점이 어디인지 질문하고 S06으로 연결한다.
- **근거:** C §§10–10.1, 11.1, 23; G-H prompt_builder.py.

## S06 — 캐시는 계산을 재사용하고, 압축은 입력을 다시 편집합니다

- **화면:** `Prefix Cache: 동일 Prefix의 계산 재사용` / `Compaction: 현재 입력의 선택·요약·축약` / `캐시 효율과 정보 신선도를 함께 봅니다`
- **그림·단계:** 좌우 55:45. 왼쪽 동일 Prefix와 새로운 suffix의 두 요청, 오른쪽 긴 History→요약+최근 결과+원문 참조. ① 같은 Prefix의 재전송 ② 제공자 hit일 때 재사용 ③ 앞부분 변경 시 영향 ④ 압축 전후와 신선도 질문. 설명 숫자는 C의 `10k+2k → 10k reuse+3k`만 사용하고 `개념 예시·실측 아님`을 붙인다. 장식용 속도 그래프는 금지한다.
- **노트·연결:** 캐시는 입력 전송 생략과 다르며 TTL·가격·집계·지원은 Provider에 종속된다. 압축과 영구 삭제는 다른 행위다. 보존 정책·Tool Call/Result 쌍·원문 ID를 확인해야 한다. “SOP-r3를 고정해 캐시가 잘 맞아도 지금 r4를 써야 한다면 올바른 운영이 아닙니다.” 이는 설계 예시다.
- **근거:** C §§11–11.2, 14–14.1, 31 F13/F16. 상세 기법 X04.

## S07 — Hermes의 Memory와 대화 검색은 다른 경로입니다

- **화면:** `SQLite Session: 이전 대화와 실행 기록` / `FTS5: 단어·구문 중심 검색` / `MEMORY.md / USER.md: 선별된 지속 정보` / `FTS5 ≠ Vector Search · RAG는 검색 활용 패턴`
- **그림·단계:** Store를 Session DB, Fact Files, Skills로 분리하고 현재 Context에 대한 별도 읽기 화살표를 둔다. ① 대화 저장 ② FTS 검색 ③ 선별 기억 주입 ④ Vector/Hybrid가 필요한 질문. FTS를 RAG 바깥의 반대편으로 배치하지 않는다.
- **노트·연결:** “장비·Alarm ID의 정확한 용어 검색과 다른 표현으로 적힌 설명 검색은 평가 조건이 다릅니다.” 이는 선택 질문이며 특정 검색 방식의 우승을 의미하지 않는다. 대규모 전문 Corpus 요구가 개인 세션 회상으로 자동 해결되지는 않는다. 데이터·Tokenizer·인덱스와 원문 추적을 함께 본다.
- **근거:** C §§12–13.1, 23, 31 F14/F15. 여섯 저장 범주 X04.

## S08 — Skill·Tool·MCP·Plugin은 서로 다른 확장 책임입니다

- **화면:** `Skill: 절차와 참고 자료` / `Tool: 실행 기능` / `MCP: 기능을 연결하는 프로토콜` / `Plugin: 호스트 Runtime의 확장 규약` / `자동 생성한 절차도 검증은 필요합니다`
- **그림·단계:** `Skill → Context → Model → Tool 요청 → Runtime` 경로에 Local Handler와 MCP Server 두 실행 경로를 둔다. Plugin은 별도 테두리로 Registry/Hook 확장을 연결한다. ① 절차 입력 ② Tool 실행 ③ MCP 경계 ④ Plugin 개입. 한 기능이 두 경로로 등록될 수 있다는 충돌 질문은 노트에만 둔다.
- **노트·연결:** 일반 용어 정의를 재강의하지 말고 Hermes가 통합한 확장점으로 연결한다. Skill 생성→품질 검증→승인·버전→배포는 C의 설계 권고이며 제품 기본 자동 파이프라인이 아니다. 모델 가중치 재학습으로 설명하지 않는다.
- **근거:** C §§15–15.2, 23. Skill 품질 파이프라인 X05.

## S09 — Hermes의 병렬 Tool과 Subagent는 다른 실행 단위입니다

- **화면:** `Tool Round: 순차·병렬 구간과 충돌 장벽` / `Subagent: 별도 Loop·Context·권한·예산` / `결과 순서 고정만으로 공유 파일 충돌은 해결되지 않습니다`
- **그림·단계:** 위쪽 한 모델 응답의 A/B/C Tool 구간, 아래 부모→자식 Loop→부모 반환. ① 여러 호출 제안 ② 실행 구간·충돌 장벽 ③ Child ID/Parent Link ④ 공유 파일·비용·취소의 경계. 독립 Context를 OS 격리 컨테이너로 표현하지 않는다.
- **노트·연결:** C는 ThreadPoolExecutor 계열과 세그먼트/배리어를 설명한다. 정확한 하위 실행기 이름·Worker 수를 새로 만들지 않는다. “같은 Snapshot의 독립 조회는 병렬 후보지만, 같은 파일을 고치는 두 도구는 다른 문제입니다.” Parent가 Child 결과를 받아 통합·재검증할 책임을 설명한다.
- **근거:** C §§7–8.2, 23, 31 F04/F19/F20. 전체 병렬성 표 X03.

## S10 — Hermes를 활용해도 권한과 운영 정책은 확인해야 합니다

- **화면:** `Tool Policy / Approval ≠ OS·DB 권한` / `Gateway: 사용자·세션·결과 전달` / `Cron: 미래의 Agent Run 기동` / `통합 기능은 운영 책임의 출발점입니다`
- **그림·단계:** S03 전체도 재등장. ① Tool 게이트·Backend 권한 ② Gateway 사용자/세션 라우팅 ③ Cron→새 Run→결과 전달 ④ 무인 실행 시 정책 질문. Cron을 현재 모델 Loop 안의 반복 화살표로 넣지 않는다.
- **노트·연결:** “조회 도구라고 해도 어느 사용자의 어떤 Lot까지 조회 가능한지는 따로 강제해야 합니다. 예약 실행에서 사람이 없을 때 승인을 어떻게 처리할지도 정책입니다.” 멀티테넌트 격리·중복 Job·배송 보장은 확인할 문제이지 기본 완전 보장이 아니다.
- **근거:** C §§16–17, 19, 20.2, 23. 운영 비교는 S34–S35.

## S11 — Demo 1: Hermes의 실제 요청과 실행을 연결해 봅니다

- **화면:** `① 모델에 실제 전달된 내용` / `② Tool 선택·정책·실행·결과` / `③ 다음 Context와 저장 상태` / `관찰 질문: 어느 사건이 다음 반복을 만들었나?`
- **그림·단계:** 왼쪽 `arch-hermes` 축소판, 오른쪽 관찰 포인트 3개. ① 요청 ② Tool 왕복 ③ 저장/다음 호출 ④ `별도 Demo 1` 버튼(설정된 경우만 활성). Trace 자체는 슬라이드에 내장하지 않는다.
- **노트·연결:** C는 실험·반도체 데모 구현을 제외한다. 따라서 이 장은 기존 발표 요구를 위한 연결 명세이며 C에 실측 결과가 있다는 뜻이 아니다. 별도 구현 후 실제 run ID·모델·버전이 있는 기록을 관찰한다. 없으면 설명용 도식만 사용한다. 복귀 후 “완성형 Harness의 다른 선택”으로 Claude Code에 연결한다.
- **근거:** C §§4.1, 10, 22–23, Appendix B1. 데모 제작 계약 F.

## S12 — Claude Code는 공개된 Harness 계약을 중심으로 비교합니다

- **화면:** `CLI Harness → Model · Tools · Subagents` / `Project Instructions · Auto Memory · Skills · Session` / `Permissions · Hooks · Sandbox` / `핵심 엔진 내부 전체는 공개 소스로 확인되지 않습니다`
- **그림·단계:** `arch-claude-code` 전체도. Host→CLI Runtime 경계 안에 Context·Tool·Session·Permission 논리 영역, 바깥에 Model/Workspace/MCP. ① 전체 관계 ② 지침·기억 ③ 권한·도구 ④ 비공개 경계. `공식 동작 계약` 레이블을 고정한다. 가상의 내부 함수명을 붙이지 않는다.
- **노트·연결:** Hermes와 비교할 것은 완성형 Harness의 통합 범위다. 차이는 공개 소스로 추적 가능한 깊이와 저수준 변경 범위에 있다. `CLAUDE.md`, 설정에 따른 `AGENTS.md`, Auto Memory, Skills는 같은 저장물로 합치지 않는다.
- **근거:** C §§4.6, 10.1, 12.1, 28; G-C.

## S13 — Claude Code의 협업과 권한은 사용 계약으로 읽어야 합니다

- **화면:** `Subagent ↔ Agent Teams: 협업 계약을 구분` / `Permission Rule · PreToolUse · Sandbox: 다른 경계` / `지침·절차 재사용의 편의와 내부 변경 제약을 함께 봅니다`
- **그림·단계:** 좌측 Parent→Child→Parent와 팀 관계를 개념 비교, 우측 Tool 앞 Hook·Permission과 실행 Backend의 경계를 배치. ① 위임 구조 ② 팀 구조 ③ 권한 위치. Teams의 자세한 메시지 순서·스레드·보장·명령을 C에 없는 수준으로 확정하지 않는다.
- **노트·연결:** “정해진 작업 환경을 재사용하는 장점이 있습니다. 다만 Hook에 기록이 찍힌 것과 Backend에서 실제 차단한 것은 다릅니다.” 실용 명령은 버전별 확인 후 보조 노트에 추가할 수 있지만, 이 원문에 없는 slash command 목록을 제작자가 임의 보강하지 않는다. 다음은 직접 Agent를 구성하는 Python Framework다.
- **근거:** C §§7.1, 8.1, 16.1, 28. 공개 계약 경계 X01/G-C.

## S14 — PydanticAI는 실행 경로에 검증 계약을 결합합니다

- **화면:** `Python 타입·검증 → Agent 실행 계약` / `Agent → 내부 Graph → Model / ToolManager / Output` / `Core · Capabilities · 별도 Harness를 구분합니다`
- **그림·단계:** `arch-pydantic` 전체도. Agent 설정/Dependencies → Core 내부 Graph, 오른쪽 Model/Provider와 ToolManager→Tools, 아래 History/Output Validator, 바깥 Capabilities/별도 Harness·외부 저장/Host. ① 타입·검증 기반 짧은 안내 ② Core 전체 ③ 확장 계층 ④ 개발자 책임. 독립 사용자 Workflow Graph는 별도 영역으로 둔다.
- **노트·연결:** Pydantic의 긴 기초 수업은 하지 않는다. “잘못된 구조의 출력을 어떻게 수정할지, 도구와 출력을 어떤 순서로 처리할지까지 실행 계약과 연결합니다.” Core 버전과 Harness 버전을 같게 가정하지 않는다.
- **근거:** C §§1, 4.2, 24, 35 각주, Appendix A3; G-P.

## S15 — 내부 Graph는 모델 요청과 Tool 처리의 경계를 드러냅니다

- **화면:** `UserPromptNode → ModelRequestNode → CallToolsNode` / `Tool Result / Retry → 다음 ModelRequestNode` / `유효한 최종 결과 → End` / `내부 Graph ≠ 사용자 Workflow Graph`
- **그림·단계:** 위 실제 Node 이름을 가진 3노드+End 상태도. ① 입력 준비 ② Model 요청 ③ Tool/Output 분류·검증 ④ 반복/종료. 각 Edge에 원문의 분기 의미를 적는다. `Agent.run / Agent.iter`는 진입 API로 별도 표시한다.
- **노트·연결:** Graph라는 단어만으로 LangGraph나 분산 내구성 Workflow라고 설명하지 않는다. “이 내부 구조는 모델 요청과 도구 처리의 경계를 읽기 좋게 드러냅니다. 업무 Graph의 설계와는 별개입니다.” 모든 Node 세부 필드·5개 실행 API 등 원문이 상세히 다루지 않은 내용은 이번 본문에 새 사실로 추가하지 않는다.
- **근거:** C §§4.2, 9, 24. 실제 소스 G-P `_agent_graph.py`.

## S16 — Tool Schema·Deps·실행 인가는 같은 계약이 아닙니다

- **화면:** `타입 기반 Schema → 모델의 호출 요청` / `ToolManager → 인자 검증·실행 경로` / `Dependencies → 실행 자원·테스트 대체` / `형식에 맞는 DB ID도 비인가일 수 있습니다`
- **그림·단계:** Model/ToolManager/App Policy/Tool Backend 레인. ① Schema 노출 ② 모델 Call ③ 검증+정책 경계 ④ 실행 결과. Dependencies는 Python 실행 경계에서 필요한 객체로 그리며 자동으로 Prompt 전체에 복사하는 선을 넣지 않는다. 최종 요청 포함 여부의 상세는 Adapter/사용 코드 확인 사항으로 노트에 둔다.
- **노트·연결:** C의 Pydantic 기반 Tool·Output 계약과 Dependencies를 중심으로 설명한다. “형식 검증은 입력을 해석할 수 있는지를, 인가는 이 사용자가 그 자원에 접근해도 되는지를 다룹니다.” Lot 접근 통제는 [INF] 앱 설계 예시다. 원문의 인자·결과 형식 검증 설명을 모든 도구 반환값의 자동 Pydantic 사실 검증으로 넓히지 않는다.
- **근거:** C §§6–6.2, 16.1, 24, 31 F02; G-P tool_manager.py/tools.py.

## S17 — 최종 출력과 Tool이 함께 나오면 종료 정책이 중요해집니다

- **화면:** `한 응답에 Final 후보 + Function Tool` / `early · graceful · exhaustive` / `출력 처리와 Tool 실행 정책이 달라집니다` / `타입 통과는 수치의 진실성을 보장하지 않습니다`
- **그림·단계:** 한 모델 응답에서 최종 후보와 Tool A/B가 나오는 갈림길. ① 공존 상황 ② 세 정책 이름 ③ “무엇이 이미 실행됐나?” 질문 ④ 출력 형식과 내용 정확성 분리. C는 전략별 세부 순서표를 제공하지 않으므로 이름만 보고 실행 순서를 임의로 애니메이션하지 않는다. X02에 확인할 조건을 둔다.
- **노트·연결:** “EndStrategy는 단순 화면 옵션이 아니라 Final과 도구 처리가 만나는 지점의 정책입니다. 실제 부작용이 발생하는 경로를 봐야 합니다.” 원문 이상의 기본값·전략별 정확한 취소 시점은 주장하지 않는다. 세부 시연은 고정 버전 구현 확인 후 별도 기록에 근거해 채운다.
- **근거:** C §§4.2, 5, 24, 31 F05/F06; G-P `_agent_graph.py`/`_tool_execution.py`/`_output.py`.

## S18 — 검증 Retry와 병렬 장벽은 실행 비용과 부작용을 바꿉니다

- **화면:** `Validation Retry: 수정된 요청을 다시 생성` / `Transport / Tool / Node Retry는 다른 범위` / `sequential 장벽: 순서 제약을 표현` / `이미 시작한 외부 작업은 별도로 확인합니다`
- **그림·단계:** 위 4종 Retry의 재실행 범위, 아래 병렬 조회 A/B→장벽→의존 작업 C. ① 검증 실패→모델 피드백 ② 네트워크/Tool/Node와 차이 ③ 장벽 ④ 취소와 부작용. 고정 지연·비용 수치는 넣지 않는다.
- **노트·연결:** “비동기로 실행한다고 안전한 병렬 처리가 되는 것은 아닙니다. 결과가 같은 Snapshot인지, 앞 결과에 의존하는지부터 봐야 합니다.” Retry가 반복될수록 추가 호출·중복 작업이 생길 수 있으므로 예산·멱등성을 함께 설명한다. 특정 함수에 몇 회 재시도가 기본인지는 C 밖의 사실이다.
- **근거:** C §§5.1, 7–7.3, 24, 31 F03/F04/F06. 전체 비교 X03.

## S19 — Core·Capabilities·Harness와 앱의 책임을 구분합니다

- **화면:** `Core: 실행·도구·출력 계약` / `Capabilities / Hooks: 실행 개입 지점` / `Harness: 별도 계층·구성` / `Host · 장기 저장 · 도메인 권한은 설계가 필요합니다`
- **그림·단계:** S14 전체도 재등장. ① Core ② Capabilities ③ 별도 Harness ④ 앱의 외부 저장/Auth/Serving 경계. 표는 “원문에서 다룬 역할”만 기입하고 모든 Memory·Skill·Shell 기능을 기본 탑재로 체크하지 않는다.
- **노트·연결:** “개발자는 실행을 전부 처음부터 만드는 대신 계약과 개입 지점을 사용할 수 있습니다. 하지만 무엇을 보존하고 누가 승인하며 어떻게 서비스할지는 정해야 합니다.” Core만으로 모든 것이 자동 해결되거나 Memory를 무조건 전부 수동 구현한다는 결론을 피한다. Harness 구체 패키지 기능 목록·버전은 이번 C에서 확정되지 않은 범위다.
- **근거:** C §§10.1, 12.1, 16.1, 20.2, 24, 35 각주, Appendix A3.

## S20 — Deferred 승인은 중단된 요청을 다시 연결하는 계약입니다

- **화면:** `DeferredToolRequests → 외부 승인/실행 → DeferredToolResults` / `Pending은 최종 실패가 아닙니다` / `요청 ID · 승인자 · 인자 · 버전 · 만료를 연결합니다`
- **그림·단계:** 모델 Tool 요청→Pending→외부 결정→재검증→결과 반영의 상태도. ① 요청 보관 ② 승인자 결정 ③ 변경 여부 검사 ④ Run 이어가기/거절. SDK 제공 수단은 보라, [INF] 앱 책임 항목은 중립 점선 영역으로 구분한다. 원문의 `execute once` 표기를 SDK의 Exactly-once 보장으로 옮기지 않는다.
- **노트·연결:** “보고서 v1을 승인한 뒤 내용이 v2로 바뀌었다면 같은 승인일까요?” 정확한 인자와 버전 결합은 설계 권고다. 승인 UI·내구 저장·프로세스 재시작을 모두 자동 제공한다고 주장하지 않는다. UI가 아니라 수명과 재개 계약이 핵심이다.
- **근거:** C §§17–17.1, 18.1, 24, 31 F08/F09. 상세 상태 계약 X06.

## S21 — Demo 2: 개발 코드와 내부 실행 경계를 함께 봅니다

- **화면:** `① Agent · Tool · 출력 계약` / `② 내부 Graph · 검증 · Retry` / `③ 승인 · History · 제어권` / `관찰 질문: SDK가 해준 일과 앱이 구현한 일은 무엇인가?`
- **그림·단계:** 좌측 개발자 작성 범위, 우측 S14의 Core 경계. ① Tool→Schema→Call ② Node 전이와 결과 ③ 관찰 가능한 실제 분기 ④ `별도 Demo 2` 링크. 아직 없는 로그·구현 화면을 완성된 것처럼 삽입하지 않는다.
- **노트·연결:** 동일 도메인 질문에 대해 Core 최소 실행을 먼저 관찰하고, 실제 검증한 경우에만 선택 Harness 확장으로 넘어간다. EndStrategy 재현은 자연 LLM 실행과 Scripted Runtime 시험을 구분해야 한다. 다음은 같은 조립형 접근에서도 명시적 NextStep을 중심으로 읽는 OpenAI SDK다.
- **근거:** C §§4.2, 22–24, Appendix B1. 데모 제작 계약 F.

## S22 — OpenAI SDK는 다음 실행을 NextStep으로 나눕니다

- **화면:** `Agent + Runner + Tools + Session / RunState` / `ProcessedResponse → NextStep` / `FinalOutput · RunAgain · Handoff · Interruption`
- **그림·단계:** `arch-openai` 전체도. Host→Runner, Model/Tools/Guardrails, 아래 Session/RunState/Tracing을 먼저 보여준 뒤 Turn Resolver 확대. ① 전체 구조 ② 응답 처리 ③ NextStep ④ 저장/반환. `Interruption`은 상태 의미이며 원문에 명시되지 않은 정확한 클래스명을 만들어 넣지 않는다.
- **노트·연결:** PydanticAI의 내부 Node 전이와 비교하여 “응답을 다음 실행의 자료형으로 분류하는 설계”를 강조한다. Tool 결과를 직접 최종 출력으로 채택하는 경우에는 후속 모델 해석을 생략하는 선택과 한계를 설명한다. 완성형 Gateway·Scheduler·Sandbox를 모두 주는 제품이라고 하지 않는다.
- **근거:** C §§4.3, 5, 25; G-O.

## S23 — Agent-as-Tool은 결과를 돌려주고 Handoff는 제어권을 넘깁니다

- **화면:** `as_tool: Specialist 결과 → Manager → Final` / `Handoff: Agent A → Agent B → Final / 다음 이관` / `Workflow: Scheduler가 다음 경로를 관리`
- **그림·단계:** 3개 수평 레인, 동일한 전문 Agent와 Manager 아이콘 사용. ① Manager 중심 ② 활성 담당자 변경 ③ 코드/Graph 경로. “최종 답변 책임” 표식을 각 레인에 다른 위치로 이동한다. 모든 Handoff를 새 OS 프로세스로 그리지 않는다.
- **노트·연결:** “공정 전문가의 분석 결과만 받아 종합할지, 사용자 후속 대화까지 그 전문가가 맡을지의 차이입니다.” 이 도메인 예시는 설계 해석이다. 다른 제품의 Delegation이라는 단어만 보고 native Handoff와 동일시하지 않는다. Context 전달 범위·Child 예산·취소는 각각 확인해야 한다.
- **근거:** C §§8–9, 25, 30. 추가 Subagent 책임 X03.

## S24 — OpenAI Guardrail과 RunState는 적용 범위를 구분해야 합니다

- **화면:** `Input Guardrail: 병행 실행 여부 확인` / `Output Guardrail: 이전 Tool 부작용을 되돌리지 않음` / `Function Tool Guardrail ≠ 모든 도구의 공통 게이트` / `RunState ≠ Conversation Session`
- **그림·단계:** 위 Guardrail과 모델/Tool의 병행 시간축, 아래 승인 Pending→RunState와 Session History 두 저장물. ① 검사 시점 ② 도구 유형 범위 ③ 승인·재개 상태. 검사 완료 전 진행 가능성을 보여주되 모든 구성에서 실제 위험 Tool이 실행된다고 단정하지 않는다.
- **노트·연결:** 정책 검사의 적용 대상·시점·실패 전파를 확인한다. `pre_approval_tool_input_guardrails`는 원문에 있는 구성 예시이며 정확한 인자 코드는 넣지 않는다. “검사 지원”을 사전 부작용 차단의 완전 보장으로 바꾸지 않는다.
- **근거:** C §§16.1–16.3, 17.1, 18, 25, 31 F07. G-O Guardrails/RunState.

## S25 — Claude Agent SDK는 Python과 CLI Runtime 사이를 연결합니다

- **화면:** `query / ClaudeSDKClient → InternalClient` / `SubprocessCLITransport ↔ Claude Code CLI` / `Control Protocol · Hooks · Permissions · SDK MCP` / `공개 SDK 코드와 CLI 내부 Loop는 다른 범위입니다`
- **그림·단계:** `arch-claude-sdk` 전체도. Python 프로세스/CLI 프로세스/외부 Model·Workspace를 세 경계로 배치. ① API→Transport ② CLI Runtime ③ Control Callback 반환 ④ 메시지 파서·ResultMessage. Python이 직접 모든 내장 Tool을 실행하는 선을 그리지 않는다.
- **노트·연결:** “애플리케이션에 완성된 Harness를 포함하는 접근입니다. 공개 코드는 통신과 프로세스 수명, 콜백 연결을 읽는 좋은 자료지만 내부 모델 Loop 전체의 공개 증거는 아닙니다.” S12와 같은 CLI Runtime 컴포넌트를 재사용한다.
- **근거:** C §§1, 4.7, 29; G-S.

## S26 — SDK가 소유하는 것은 프로세스·스트림·콜백의 수명입니다

- **화면:** `query ↔ 지속 연결 Client: 수명 비교` / `SDK-hosted MCP ↔ CLI 내장 Tool: 실행 위치 비교` / `SessionStore ↔ CLI Transcript: 저장 경계 비교` / `Host는 자원·취소·세션 격리를 관리합니다`
- **그림·단계:** S25 경계도에 lifecycle 막대와 MCP 왕복을 겹쳐 확대한다. ① 단발/연결 수명 ② Python Tool Callback ③ Session/Store ④ Host 책임. 호출당 프로세스 수 등 C에 없는 보장을 숫자로 쓰지 않는다.
- **노트·연결:** `allowed_tools`를 모든 실행의 완전한 whitelist로 취급하지 않는다. 콜백 호출 여부는 실제 정책 경로에 달린다. 대화 저장·파일·산출물·인증은 다른 이관 준비물이다. 실제 조합 제약은 코드 확인 후 추가할 수 있으나 이번 원문에 없는 세부를 확정하지 않는다.
- **근거:** C §§4.7, 12.1, 16.1, 20.2, 29; G-S query/client/transport/session_resume.

## S27 — ADK는 Flow의 실행과 Runner의 이벤트 관리를 나눕니다

- **화면:** `Runner: Session · Invocation · Event 관리` / `LlmAgent / BaseLlmFlow: 요청·모델·도구 반복` / `Session · Memory · Artifact Service는 별도 계약`
- **그림·단계:** `arch-adk` 전체도. Host→Runner→LlmAgent/BaseLlmFlow→Model·Tool Batch, Event가 Runner와 SessionService로 흐른다. MemoryService·ArtifactService는 Context/근거 공급 영역으로 분리한다. ① 전체 구조 ② Flow 반복 ③ Event 전달·저장 ④ 서비스 분리.
- **노트·연결:** C §4.4는 축약 대표 경로이므로 실제 최신 Node 함수가 모두 이 이름으로 직렬 호출된다고 설명하지 않는다. “실행을 만드는 층과 상태 변화를 이벤트로 전달·저장하는 층을 나눠 읽습니다.” 상세 Graph와 전통 Workflow는 다음 장에서 구분한다.
- **근거:** C §§4.4, 10.1, 12.1, 26; G-G.

## S28 — ADK의 Final Event는 업무 전체 완료와 다를 수 있습니다

- **화면:** `개별 Agent final ≠ 전체 Workflow 완료` / `Event · State Delta · Artifact를 연결` / `전통 Agent Tree/Workflow와 별도 Graph 구분` / `순서·중복·Resume의 범위를 확인합니다`
- **그림·단계:** 두 Agent의 시간축에서 Agent A final 뒤 B/Join이 남은 그림. ① 개별 final ② 전체 완료 조건 ③ Event/State와 Artifact ID ④ Workflow 경로 구분. 현재 구체 API가 구현된 것처럼 가상의 workflow-complete 이벤트 타입을 만들지 않는다.
- **노트·연결:** “BIN 분석 한 단계가 말을 마쳤다고 보고서가 준비된 것은 아닙니다. 어떤 Snapshot·Artifact를 모아 완료로 볼지 업무 기준이 필요합니다.” `temp:`와 영구 상태, Graph checkpoint의 세부 재개 범위는 코드 추적 대상으로 노트에 둔다. 보편적인 완전 복구 보장으로 표현하지 않는다.
- **근거:** C §§4.4, 9, 18.2–18.3, 26, 31 F10. G-G event/session/workflows.

## S29 — Microsoft에는 Tool·Harness·Workflow 반복이 겹쳐 있습니다

- **화면:** `Agent → RawAgent → Context Providers → ChatClient` / `① Function Invocation Tool Loop` / `② Harness의 Agent 재호출` / `③ Workflow의 Executor · Edge · Superstep`
- **그림·단계:** `arch-maf` 전체도. 중앙 Pipeline에 Tool Loop, 그 바깥 Harness Loop, 옆 별도 Workflow Scheduler를 둔다. ① 전체 Pipeline ② 모델↔Tool 반복 ③ 상위 Agent 재호출 ④ Workflow 반복. 동심원이 같은 매 실행마다 모두 활성화된다는 오해를 피하려고 선택 구성 선을 점선으로 표시한다.
- **노트·연결:** “한 개의 while 루프로 비교하면 반복의 위치와 종료 기준을 놓칩니다.” Agent·Chat·Function Middleware를 각 실제 계층에 표시한다. Python 분석을 다른 언어 구현의 동일 동작으로 일반화하지 않는다.
- **근거:** C §§4.5, 9, 27; G-M.

## S30 — Middleware는 어느 단계에서 정책을 강제하는지가 중요합니다

- **화면:** `Agent / Chat / Function: 개입 단위가 다릅니다` / `Tool 오류와 정책 거절의 전파를 구분합니다` / `최종 실행 인자를 기준으로 승인·인가합니다`
- **그림·단계:** 세 Middleware 층을 Pipeline 위에 표시. 오른쪽에 일반 Tool Error→결과/예외 정책과 `MiddlewareFailure`→중단/거절의 비교 경로. ① 위치 ② 오류 분류 ③ 승인한 인자와 실행 인자의 비교. 정책 인자 변경 사례는 [INF] 설계 예시로 둔다.
- **노트·연결:** “권한 거절을 모델이 수정해 다시 도전할 일반 오류로만 돌리면 정책 경계가 약해질 수 있습니다.” C가 설명한 전파 차이를 유지하며 모든 예외가 항상 하나의 경로로 처리된다고 단정하지 않는다. FIDES는 실험적이며 완전 보안의 근거가 아니다.
- **근거:** C §§16.1, 16.4, 17, 27, 31 F08/F24; G-M `_middleware.py`.

## S31 — Superstep과 Checkpoint는 외부 트랜잭션이 아닙니다

- **화면:** `Executor · Edge · Superstep · Checkpoint` / `Workflow 상태 복원 ≠ 외부 변경의 원자적 처리` / `병렬 결과는 업무 키와 버전으로 결합합니다`
- **그림·단계:** Source A/B→Join→다음 Superstep, 아래 Checkpoint와 별도 외부 DB. ① 분기/결합 ② 저장 경계 ③ 외부 성공과 checkpoint 사이 장애 틈. 같은 Executor 순서와 다른 분기 도착 순서를 혼동하지 않는다.
- **노트·연결:** 업무 키 예시는 `LOT-A + snapshot-v1 + SOP-r3`다. 이는 Join 설계 제안이며 MAF가 이 키를 자동 제공한다는 뜻이 아니다. Graph/Functional은 다른 구성 접근이며 세부 코드는 부록·소스에 둔다. 다음은 기술별 저장물을 같은 질문으로 비교한다.
- **근거:** C §§9, 18.1–18.3, 27, 34.1; G-M `_workflows/_runner.py`/`_checkpoint.py`.

## S32 — 같은 ‘저장’이라도 다시 답할 수 있는 질문이 다릅니다

- **화면:** `Transcript: 무엇을 대화했나?` / `RunState: 어디서 멈췄나?` / `Event / Checkpoint: 무엇이 바뀌고 어디서 재개하나?` / `Memory: 다음에도 무엇을 기억하나?` / `Side-effect Journal: 실제 외부 변경은 무엇인가?`
- **그림·단계:** 5개 질문과 저장물, 각 행의 대표 기술 예시만 표시. ① 대화/기억 ② 실행 중단 ③ Event/Checkpoint ④ 외부 변경. 제품별 7열 체크표는 넣지 않는다.
- **노트·연결:** “Session을 DB에 저장했다고 승인 대기 위치까지 복원되는 것은 아니고, Checkpoint가 있다고 외부 보고서 발행 이력까지 자동 일치하지도 않습니다.” 저장물끼리 연결할 ID와 source of truth는 앱 계약이다. 여섯 범주의 정확한 표는 X04/X06.
- **근거:** C §§12, 17–18, 22.

## S33 — 복구 후 같은 Tool을 실행해도 되는지는 별도 판단입니다

- **화면:** `외부 Tool 성공 → 응답 기록 전 Crash` / `Checkpoint 복원 → Tool 재호출?` / `멱등 키 · 완료 조회 · 조정/보상` / `Resume ≠ Exactly-once`
- **그림·단계:** C의 이체 예를 A-5의 가상 `publish_report`로 치환한 시퀀스. ① Intent 저장 ② 외부 성공 ③ Crash ④ 복원과 중복 후보 ⑤ 멱등/조회 경로. 고정 애니메이션은 설명 사례이며 실제 장애 재현 로그로 표시하지 않는다.
- **노트·연결:** “안전한 복구는 저장 위치만이 아니라 외부 시스템의 계약에 달립니다.” Outbox/Inbox·멱등성·Reconciliation은 C의 설계 대안이며 일곱 제품이 동일하게 기본 제공하는 기능이 아니다. Intent 저장도 외부 API와 원자적으로 묶이는 것은 아니다.
- **근거:** C §§18.1–18.2, 31 F09/F11, 33.

## S34 — Cron·Background·Queue·Resume는 다른 실행 계약입니다

- **화면:** `Cron: 언제 시작할까?` / `Background: 누가 계속 소유할까?` / `Queue: 어떻게 전달·재시도할까?` / `Resume: 어디서 이어갈까?` / `무인 실행 정책과 중복·누락을 확인합니다`
- **그림·단계:** Trigger→Job→Run→State→Delivery의 수명선, 각 개념이 관여하는 위치만 강조. ① 예약 ② 분리 작업 ③ 전달/Retry ④ 재개. 단일 원형 “자동화” 아이콘으로 합치지 않는다.
- **노트·연결:** Hermes는 스케줄·Agent Run·전달을 통합한다. 다른 SDK의 외부 Scheduler 조합은 예약 불가능과 다르다. `(job_id, scheduled_for)`, 이전 작업 overlap 정책, Catch-up, DLQ, Interactive Approval 부재는 [INF] 선택 질문이다.
- **근거:** C §§19–19.1, 23, 34.

## S35 — 응답 전달과 Agent 실행 상태는 분리해야 합니다

- **화면:** `부분 Token → Agent Final → 정책·저장 → Client 수신` / `동기 HTTP / Streaming / Job API` / `연결 단절이 Tool 취소를 뜻하지는 않습니다`
- **그림·단계:** 위 4개 완료 시점, 아래 Client→Auth/Session Router→Worker→Model/Tool/Store 구조. ① token ② final ③ commit ④ delivery. 작은 inset으로 중앙 Agent vs 로컬 Agent+중앙 LLM의 배치를 비교한다. 후자는 [INF] 배치 대안이며 특정 제품의 완성 기능으로 표시하지 않는다.
- **노트·연결:** 중앙형은 인증·Tenant·Session, 예산·Worker/Tool 동시성, 영속 상태·취소·감사를 설계한다. 로컬형은 설치·업데이트·자격증명·파일 권한·정책 버전 동기화 책임을 검토한다. 사용자 수·GPU 수·프로세스 수를 근거 없이 추정하지 않는다. 상세 비교는 X09.
- **근거:** C §§20–20.4, 21–22, 36. 배치 대안은 원문의 Host 책임을 적용한 [INF].

## S36 — 모델 교체는 URL보다 기능 계약을 먼저 확인해야 합니다

- **화면:** `Tool Calling · Schema / Structured Output` / `Streaming · Cancellation · Error / Retry` / `Token Accounting · Cache · Parallel Calls` / `OpenAI-compatible ≠ 모든 기능 동일`
- **그림·단계:** Runtime→Provider Adapter/Profile/Client→모델 Gateway의 경계. ① 요청 형식 ② 도구/출력 ③ Stream/취소 ④ 비용·Cache. 일곱 제품의 상세 Provider 목록 대신 기능 호환 질문을 표시한다.
- **노트·연결:** Hermes Provider Resolver, PydanticAI Model/Profile, OpenAI Responses/Chat 경로, ADK Adapter, MAF ChatClient, Claude CLI 지원 옵션처럼 평가 경계가 다르다. “로컬 vLLM 연결도 해당 서버·모델·템플릿의 기능을 별도 확인해야 합니다.” 엔진 내부 최적화 강의로 확대하지 않는다.
- **근거:** C §21, Appendix B1. 기능 점검 표 X09.

## S37 — Trace로 경로를 설명하고 네 층의 평가로 검증합니다

- **화면:** `Contract → Scripted Runtime → Integration → Task Eval` / `Model · Tool · Turn · Context · Policy · Workflow · Host` / `형식·경로·연결·업무 품질을 분리합니다`
- **그림·단계:** 왼쪽 연결 ID를 가진 이벤트 타임라인, 오른쪽 네 평가 층. ① Schema/Serializer ② Scripted 분기 ③ 실제 Provider/DB/MCP ④ 정답·근거·비용·정책. 네 층을 자동으로 모두 통과한 것처럼 체크하지 않는다.
- **노트·연결:** “Trace는 원인을 찾는 기록이고 Eval은 성공 기준입니다. 타입을 통과해도 수치가 틀릴 수 있고 Scripted 모델로 분기를 재현해도 실제 LLM의 과제 성공률이 입증되지는 않습니다.” 로그에는 Tool 인자·근거·정책 버전을 연결하되 비밀정보를 가린다. 비공개 추론 원문을 요구하지 않는다.
- **근거:** C §§22–22.1, Appendix B1.

## S38 — 직접 만든다면 제품보다 책임 인터페이스를 가져옵니다

- **화면:** `RunCoordinator · ModelGateway · ContextBuilder` / `ToolCatalog · PolicyEngine · ToolExecutor · StateStore` / `principal · deadline · expected_version · idempotency_key`
- **그림·단계:** C §32 참조 아키텍처를 상위 7개 책임으로 축약. Host→Coordinator→Context/Model, Resolver→Catalog/Policy/Executor, Coordinator↔Store, Trace 관찰선. ① 입력/실행 조율 ② 모델/Context ③ 정책/Tool ④ 상태/감사. 상단에 `INF · 참조 설계`를 고정한다.
- **노트·연결:** “프레임워크를 새로 전부 만들자는 결론은 아닙니다. 기존 기술을 사용하더라도 누가 이 책임을 수행하는지 적어보자는 뜻입니다.” optimistic concurrency, 멱등성, 실행 주체, deadline이 Tool 호출 함수만으로 해결되지 않는 문제를 드러낸다. 전체 Protocol과 의사코드는 X08.
- **근거:** C §§32–33. 실제 제품 아키텍처와 구분한다.

## S39 — 선택은 요구조건과 반대급부의 조합입니다

- **화면:** `통합 실행 환경 ↔ 조립 가능한 실행 계약` / `자율 Tool 선택 ↔ 명시적 Workflow` / `Event 이력 ↔ 빠른 Snapshot 복원` / `자율 Memory ↔ 승인된 지식·버전 관리`
- **그림·단계:** 성능 순위 대신 4개 선택 행. 각 행 오른쪽에 `얻는 것 / 추가 책임`을 한 쌍으로 둔다. ① 작업 조건 ② 비교할 쌍 ③ 필수 검증 ④ 선택 보류 조건. 제품별 ◎ 점수는 본문에 쓰지 않는다.
- **노트·연결:** C §34 요구사항 표를 사용한다. 예: 완성형 작업 환경은 Hermes/Claude Code, 명시적 Runner/Typed 계약은 OpenAI/PydanticAI, Event/Workflow는 ADK/MAF, CLI 삽입은 Claude SDK가 비교 기준이 된다. 이는 후보 검토 지점이며 산업용 선정 결과가 아니다. 전체 연구 적합성 표는 X09에서 원문 범례와 함께만 공개한다.
- **근거:** C §§30, 34–36.

## S40 — 맡길 책임과 우리가 지킬 계약을 결정합시다

- **화면:** `① Loop와 제어권의 소유자를 확인한다` / `② 상태·권한·복구의 경계를 확인한다` / `③ 우리 데이터·정책·평가로 검증한다` / `Next: 실제 도메인 Agent의 설계와 재현`
- **그림·단계:** S01 기술 지도가 작게 재등장하고 중앙에 3개 결론. ① 실행 책임 ② 운영 계약 ③ 검증. 마지막에는 제품명보다 책임 경계를 밝게 남긴다.
- **노트·연결:** “누가 더 많은 기능을 갖췄는지보다, 우리 요구에서 맡길 수 있는 책임과 남는 책임을 설명할 수 있어야 합니다. 다음 단계에서는 데이터·권한·성공 기준을 고정한 Agent로 이 선택을 검증하겠습니다.” 1차의 “다음은 Tools/Orchestration” 멘트를 재사용하지 않는다. Q&A 운영은 실제 세미나 진행 방식에 맞추며 일반 청중용 빈 Q&A 장을 자동 추가하지 않는다.
- **근거:** C §§36, 39, 최종 메시지.

# C. 상세 부록 명세 — 본문을 작게 압축하지 않기 위한 참조 화면

부록도 한 장 한 화면을 지키되 탭/행 선택으로 세부를 읽는다. 화면의 모든 탭 내용은 로컬 데이터에 포함하고, 현재 선택 내용을 인쇄/최종 상태로 확인할 수 있게 한다. 아래 표 전문을 한 화면에 모두 노출하라는 뜻은 아니다.

## X01 — 7개 실행 경로와 공개 경계

**화면:** `Loop를 누가 소유하는가?`와 기술 선택 탭. **그림:** 왼쪽 전체 구조 축소, 오른쪽 아래 경로, 하단 공개 범위. **조작:** 기술 선택→경로 단계 강조→출처 열기. 복귀는 호출한 장으로 돌아간다.

| 기술 | 표시할 대표 경로 | 경계 |
|---|---|---|
| Hermes | run_conversation → preflight/request → Provider → response validation → intent → tool round → result → continue/final | 공개 Harness 대표 경로 [SRC] |
| PydanticAI | Agent.run/iter → UserPromptNode → ModelRequestNode → CallToolsNode → next request/End | 내부 Agent Graph와 사용자 Graph 구분 [SRC] |
| OpenAI | Runner/_run_impl → model → ProcessedResponse → tool/side effects → NextStep | 명시적 분기 [SRC] |
| ADK | Runner/Session → LlmAgent/Flow → processors/model/tools → Events → Runner 저장 | 축약 경로, 구체 버전 구현은 링크 확인 [SRC] |
| MAF | Agent→RawAgent/Context→ChatClient FunctionInvocation; 별도 Harness/Workflow | 세 반복이 항상 함께 동작한다는 뜻 아님 [SRC/DOC] |
| Claude Code | CLI→Context→Model/tool/subagent/final→permissions/session/result | 공식 계약의 논리 모델, 내부 함수 추정 금지 [DOC/UNV] |
| Claude SDK | query/Client→InternalClient→Transport→CLI↔Control→typed messages | 공개 Python 경계와 비공개 CLI 구분 [SRC/UNV] |

**노트:** 기술별 대표 소스 파일은 G. 모든 함수명이 한 호출 스택에 그대로 존재한다는 뜻이 아니다. **근거:** C §§2, 4.1–4.7, 37.1, Appendix A.

## X02 — Tool의 7단계·4종 실패·종료 정책 질문

**화면/그림:** `정의→Schema→선택→Parse/Validate→Policy/Approval→실행→Result 기록`의 7단계를 고정한다. 다른 탭에는 다음 두 표를 둔다.

| 실패 | 사례 | 판단 질문 |
|---|---|---|
| 형식 | 누락 인자·잘못된 JSON | 모델에 수정 요청할 것인가? |
| 실행 | 파일 없음·DB Timeout | 제한 Retry/실패 반환이 가능한가? |
| 정책 | 비인가 자원·금지 Tool | 강제 거절/중단이 필요한가? |
| 부분 부작용 | 외부 성공 후 응답 유실 | 조회·멱등성·조정 없이 재실행해도 되는가? |

| 종료/중단 | 추가 확인 |
|---|---|
| 모델 Final | Output 검증·후처리·저장은 완료됐나? |
| Tool 결과 Final | 모델 재해석을 생략해도 되는가? |
| Handoff | 후속 실행 주체와 Context는? |
| Max steps/예산 | 진행된 작업·저장 상태·알림은? |
| Guardrail | 이미 발생한 부작용은? |
| 승인 대기 | 요청 ID·인자·재개 상태는? |
| 취소 | Task와 실제 외부 실행 모두 중단됐나? |
| Workflow 수렴 | 남은 메시지·외부 작업은? |

**EndStrategy 탭:** early/graceful/exhaustive를 표시하고 “Final 후보+Function Tool, 검증 실패, 이미 실행 중인 Tool, Streaming일 때의 실제 분기를 고정 버전 소스로 확인”이라는 추적 질문만 둔다. 원문에 없는 상세 결과표를 만들어 채우지 않는다. **근거:** C §§5–6.2, 24, 31 F05.

## X03 — 병렬성 다섯 종류와 위임의 공유 범위

**화면/그림:** 모델 응답, Tool Task, Child Loop, Workflow, Server의 다섯 레인을 클릭하여 관련 표 행만 보여준다.

| 종류 | 단위 | 확인할 공유/충돌 |
|---|---|---|
| Multiple Tool Calls | 한 모델 응답의 여러 요청 | 아직 동시 실행이 아님 |
| Parallel Tool Execution | 여러 Tool 함수 | 파일·DB·API·Connection Pool |
| Subagent Parallelism | 독립 모델 Loop | Context 복제·권한·비용·취소 |
| Workflow Fan-out/in | Node/Executor | 메시지·State·Join·장벽 |
| Server Concurrency | 사용자/세션 요청 | Tenant·Lock·Rate Limit·Worker |

**기술 비교 탭:** Hermes=스레드 계열+구간/장벽, PydanticAI=async Task+sequential 장벽, OpenAI=async Tool+상한 설정, ADK=Tool batch와 별도 ParallelAgent/TaskGroup, MAF=Function invocation과 Workflow Superstep, Claude Code=문서화된 동시 작업 계약, Claude SDK=CLI의 스케줄 결과 수신. Provider의 다중 호출 허용과 런타임 동시성 상한을 분리한다.

**Subagent 노트:** Child ID·Parent Link, Context·Tool·예산·종료, 반환 계약, 실패·취소 전파, 부모의 결과 재검증, 부모 종료 시 detach/cancel/background 정책을 묻는다. 독립 Context는 강한 OS·테넌트 격리 증거가 아니다. **근거:** C §§7–8.2, 31 F03/F04/F19/F20.

## X04 — Memory 여섯 범주와 Context 변환 다섯 방식

**화면/그림:** “저장물” 탭과 “현재 요청 변환” 탭을 분리한다.

| 범주 | 저장 내용·목적 |
|---|---|
| Working Context | 현재 모델 입력과 Tool 응답 |
| Message History | User/Assistant/Tool 대화 |
| Semantic/Fact Memory | 선별 사실·선호 |
| Procedural/Skills | 재사용 절차 |
| Retrieval Index | 원문을 찾는 검색 인덱스 |
| Durable State/Checkpoint | 중단된 실행의 Node·대기·Queue |

| 변환 | 이점 | 위험/추가 책임 |
|---|---|---|
| Sliding Window | 단순한 입력 관리 | 오래된 제약 손실 |
| Tool Output Pruning | 큰 결과의 중복 축소 | 원문 재검증 경로 |
| Summarization | 맥락과 길이 절충 | 누락·왜곡 |
| Structured State | 목적·제약 명시 | Schema·갱신 비용 |
| Retrieve-on-demand | 필요한 순간 로드 | 검색 품질·지연 |

**노트:** 압축은 삭제 정책이 아니다. 실제 저장 History도 변환될 수 있는지는 구현별 확인이 필요하다. Prompt Cache와 앱 결과 캐시는 별도다. C §11.2의 네 경우(Provider cache, cache control, Prefix 안정화, 앱 캐시)를 구분한다. **근거:** C §§10–14.1.

## X05 — Skill 품질과 Tool/MCP/Plugin 신뢰 경계

**화면:** `생성 → 검증 → 평가 → 승인·버전 → 로딩 → 로그 회수·수정`과 `INF · 품질 설계 권고`. **그림:** 절차 문서가 Context에 들어가는 선과, Tool이 외부에 영향을 미치는 선을 분리한다. **조작:** Skill 후보 생성/배포/폐기 단계 강조.

**노트:** Candidate 식별→초안→Schema·경로·권한 검증→샘플 Dry-run/Eval→검토→버전·서명 등록→점진 로딩→오류 회수라는 원문 권고를 설명한다. 모든 제품 기본 자동 기능으로 소개하지 않는다. MCP Server는 프로토콜 노출, Plugin은 호스트 규약 확장이다. 같은 Tool의 중복 등록·이름·정책·감사 경로 충돌을 질문한다. **근거:** C §§15–15.2, 31 F17/F18.

## X06 — 승인·상태 저장·재개를 묶는 앱 계약

**화면/그림:** `Running→Pending→Authorized→Revalidate→Running/Completed`, 거절·만료·실패 가지를 둔다. `설계 참조 상태도`로 표시한다.

| 결합할 정보 | 목적 |
|---|---|
| Request ID | 승인 대상 식별 |
| User/Role/Scope | 승인 권한 |
| Arguments·Tool Version Hash | 승인·실행 대상 일치 |
| Expiry | 오래된 승인 재사용 방지 |
| Pending State | 재시작 후 대기 복원 |
| Tool-side Idempotency | 중복 부작용 제한 |
| Revalidation | 정책·데이터 변경 재검사 |

**제품 수단 탭:** Hermes Approval/Tool Policy, PydanticAI Deferred requests/results, OpenAI RunState, ADK Event/Confirmation/Workflow, MAF Approval/HITL RequestPort/Checkpoint, Claude CLI Prompt/Hook, Claude SDK Permission/callback. 동일 내구성·저장형식 보장으로 읽지 않는다. **근거:** C §§17–18.3.

## X07 — 실패·경계 사례 24개: 테스트 결과가 아닌 질문

**화면:** 4개 탭 `호출/실행`, `정책/복구`, `Context/지식`, `운영/변경`. 한 번에 6행만 보인다. 각 행 클릭 시 `입장→최초 검사 코드→분기→저장→재실행 위험→설계 선택`의 빈 분석 틀을 연다. **검증 완료 체크 표시는 두지 않는다.**

| ID | 상황 | 확인할 판단 |
|---|---|---|
| F01 | 없는 Tool | 오류 반환/중단 |
| F02 | 형식상 유효한 비인가 DB ID | 업무 인가 위치 |
| F03 | 2초와 5분 Tool | Timeout·부분 결과 |
| F04 | 같은 파일 동시 쓰기 | 충돌·장벽 |
| F05 | Final+Tool 동시 요청 | 출력·도구 정책 |
| F06 | Validator 연속 실패 | 예산·예외·비용 |
| F07 | 늦은 Input Guardrail | 이미 발생한 부작용 |
| F08 | 승인 대상 인자 변경 | 무효화·재검증 |
| F09 | 승인 뒤 Crash | Replay·멱등성 |
| F10 | Event 중복 저장 | State Delta 중복 |
| F11 | Checkpoint 직전 외부 성공 | 완료 조회·중복 실행 |
| F12 | 복원 중 Tool Schema 변경 | Migration·호환 |
| F13 | 앞 Timestamp 변경 | Prefix Cache 영향 |
| F14 | Memory 동시 수정 | Lock·버전·Merge |
| F15 | FTS에 없는 동의어 | Recall 보완 |
| F16 | 요약에서 제약 탈락 | 보존 필드·원문 |
| F17 | 악성 Skill | 신뢰 등급·실행 권한 |
| F18 | 악성 MCP 응답 | 비신뢰 입력·정제 |
| F19 | 부모 취소 후 Child 지속 | 소유권·취소·비용 |
| F20 | 병렬 Agent 사실 충돌 | 근거 대조·병합 |
| F21 | Stream 단절 | 전송/실행 상태 분리 |
| F22 | Scheduler 중단·재시작 | 누락·중복·Catch-up |
| F23 | Provider 변경 | Schema·Context·Cache·Session |
| F24 | Guardrail 서비스 장애 | Fail closed/open·오류 전달 |

**노트:** 특정 제품이 취약하다는 판정이 아니다. 원문의 F01–F24를 보존한 후속 검증 질문이다. 세 대표 비교 시퀀스(위험 Tool 차단, 병렬 하나 실패, Resume 중 부작용)는 S24/S09/S33에서 회수한다. **근거:** C §§31–31.2.

## X08 — 참조 인터페이스와 최소 Runtime 의사코드

**화면:** 인터페이스 선택 탭과 짧은 코드. **조작:** 코드의 1단계와 S38 책임 노드를 연결하여 강조한다. 아래는 C §32.1/§33을 발표용으로 축약한 **[PSEUDO]**다. 실제 SDK에 존재하는 API로 제시하지 않는다.

```text
ModelGateway.generate(request, deadline, trace_ctx)
ContextBuilder.assemble(run_state, token_budget)
ToolCatalog.get_schema(agent_id, permissions) / lookup(name)
PolicyEngine.authorize_tool(principal, tool_call, context)
ToolExecutor.execute(tool_call, idempotency_key, timeout)
StateStore.load(run_id) / commit_transition(expected_version, transition)
RunCoordinator.run(...) / resume(...) / cancel(...)
```

```text
start_run
repeat within limits:
  cancellation/deadline → context → model request → classify response
  final: validate → commit completion → return
  handoff: authorize → commit transfer → continue
  tools: validate → policy → persist pending approval OR proceed
         partition conflicts → record intent → execute with limits
         record results → continue
  fatal/refusal: record stop → terminate
limit reached: record stop → terminate
```

**노트:** 핵심 식별자는 `principal`, `deadline`, `expected_version`, `idempotency_key`다. State commit과 외부 변경의 원자성은 여전히 별개이며 Outbox·조회·조정이 필요할 수 있다. 오류/분산/마이그레이션의 모든 코드를 이 의사코드가 해결한다는 뜻이 아니다. **근거:** C §§32–33.

## X09 — 선택 매트릭스·운영·호환 체크

**화면:** `설계 선택`, `연구 적합성`, `Host/Provider 점검` 3개 탭. 본문에서 처음부터 7열 전체 표를 노출하지 않는다.

**설계 선택 탭의 데이터:**

| 요구 | 검토할 설계·원문의 비교 대상 |
|---|---|
| Loop 학습/변경 | 명시적 상태 머신: OpenAI/PydanticAI |
| 정형 결과·검증 | Typed Tool/Output: PydanticAI |
| 단기 경량 실행 | SDK+최소 Tool: OpenAI |
| 통합 Runtime | Hermes/Claude Code |
| Context 합성 | ADK Processors/MAF Providers |
| Event 중심 기록 | ADK |
| 장기 분기·재개 | MAF/ADK Graph, 실제 지원 범위 검증 |
| 정책 경로 분리 | MAF Middleware+독립 인가/Backend |
| CLI를 앱에 삽입 | Claude Agent SDK |
| 통합 예약 | Hermes Scheduler/Gateway |

**연구 적합성 탭의 데이터:** C §35를 그대로 사용한다. 범례 `◎ 대표 연구 사례 / ○ 기능·코드 존재 / △ 별도 보완 고려 / — 직접 연구 기준 제한`를 표보다 먼저 표시한다. **성능 점수·미지원 표가 아니다.**

| 연구 영역 | Hermes | PydanticAI | OpenAI | ADK | MAF | Claude Code | Claude SDK |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 공개 자체 Loop | ◎ | ◎ | ◎ | ◎ | ◎ | △ | △ |
| 완성형 Harness | ◎ | ○ | ○ | ○ | ◎ | ◎ | ○ |
| Typed Validator/Retry | ○ | ◎ | ○ | ○ | ○ | △ | △ |
| Event/Session | ◎ | ○ | ◎ | ◎ | ◎ | ○ | ○ |
| 명시적 Graph Workflow | △ | ○* | △ | ◎ | ◎ | △ | △ |
| Tool 병렬 구현 | ◎ | ◎ | ◎ | ◎ | ◎ | △ | △ |
| Tool 권한/승인 | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ |
| 파일 Memory/Skill 통합 | ◎ | ○** | ○** | ○** | ◎ | ◎ | ○ |
| CLI SDK 통신 | — | — | — | — | — | ○ | ◎ |
| Scheduler/Gateway | ◎ | △ | △ | ○ | ○ | ○ | △ |

`*` 내부 Agent Graph와 별도 Pydantic Graph 구분. `**` 별도 Tool/Harness/앱 구성을 포함하며 기본 자율 Memory·Skill 루프가 Hermes와 같다는 뜻이 아니다.

**Host/Provider 점검 탭:** Auth/Tenant/Session, Credential 분리, Worker·Tool·LLM 동시성, deadline·취소, 영속 상태, 로그 보존; Tool arguments·Structured Output·Stream chunk·취소·토큰·Cache·Retry·병렬 호출. 중앙 Agent와 로컬 Agent+중앙 LLM의 차이는 이 책임이 어느 위치로 이동하는지로 비교하고 용량·속도 숫자는 비워 둔다. **근거:** C §§20–21, 30, 34–36.

## X10 — 발표자 Q&A와 소스 추적 안내

청중 기본 순회에는 넣지 않고 질문 검색/번호 점프로 연다. C §38의 30개 질문을 다음 답변 기준으로 보존한다. 답변은 원문에서 지지되는 범위로 제한한다.

| Q | 질문 | 답변의 핵심·근거 |
|---|---|---|
| 01 | SDK/Framework는 제품명으로 구분? | 실제 실행 소유권·범위를 봄. C §1.1. |
| 02 | Hermes Intent를 먼저 저장하는 이유? | 요청한 행동과 실행·결과를 연결. 외부 원자성 보장은 별개. §4.1/§33. |
| 03 | 내부 Graph와 업무 Graph는? | Agent Loop 구현과 사용자 경로 설계의 차이. §4.2/§9. |
| 04 | NextStep이 Boolean보다 주는 정보? | 종료·계속·제어권 이전 등 분기 의미. §4.3. |
| 05 | ADK Event 영속화는 누구 책임? | 대표 경로에서 Runner/SessionService, 반복은 Flow. §4.4/§18.3. |
| 06 | MAF Loop를 왜 나눔? | 모델-Tool, 상위 Agent 재호출, Workflow의 의미·종료가 다름. §4.5. |
| 07 | Claude SDK에서 비공개 경계는? | Transport/Control은 공개, CLI 핵심 Loop는 별개. §4.7/§29. |
| 08 | 여러 Tool 요청=병렬 실행? | 아님. 응답 표현과 Scheduler 실행이 다름. §7. |
| 09 | parallel_tool_calls와 실행 상한은? | Provider 허용과 Runtime 자원 정책. §7.1. |
| 10 | Hermes Pool과 ADK TaskGroup은 같은 층? | Tool 실행/Agent 실행 단위를 먼저 구분. §7. |
| 11 | EndStrategy와 부작용은? | Final/Tool 공존 처리·이미 진행된 실행을 확인. §24. |
| 12 | Handoff와 as-tool? | 다음 담당자로 이전 vs Manager 결과 반환. §8. |
| 13 | ADK final=전체 완료? | 개별 발화와 업무 완료 범위가 다를 수 있음. §4.4. |
| 14 | MAF Superstep은? | Executor/메시지/상태 전이의 Workflow 실행 단위. §4.5/§27. |
| 15 | Cache가 전송을 줄이나? | 동일 Prefix 계산 재사용, 전송 생략 아님. §11. |
| 16 | Memory 파일과 Transcript? | 선별 장기 정보와 대화 기록. §12. |
| 17 | FTS와 RAG가 반대인가? | FTS도 RAG 검색 수단이 될 수 있음. §13. |
| 18 | Skill 생성=검증? | 생성·평가·승인·배포는 별도. §15.1. |
| 19 | MCP와 Plugin은 대체재? | 프로토콜 경계와 호스트 확장 규약. §15.2. |
| 20 | 늦은 Guardrail은? | 부작용 선행 가능성·Backend 차단 검토. §16.3. |
| 21 | Pydantic 검증=인가? | 형식과 실행 권한은 다름. §16.1. |
| 22 | 승인 후 인자 변경은? | 승인 대상 일치·무효화·재검증. §17. |
| 23 | Session/RunState/Checkpoint는? | 대화/중단 위치/실행 복원 질문이 다름. §18. |
| 24 | 재개 후 중복 이체는 왜? | 외부 성공과 Runtime 저장의 장애 틈. §18.1. |
| 25 | Task 취소=외부 취소? | 외부 Transaction이 계속될 수 있음. §7.2. |
| 26 | Stream 종료=Run 종료? | 전송·실행·저장·수신은 다름. §20.3. |
| 27 | 내장 Cron과 외부 Cron? | 제공 경계·Job/Retry/전달 책임 차이. §19. |
| 28 | 사내 Gateway 호환은? | Tool/출력/Stream/Cache/취소 등 기능별 검증. §21. |
| 29 | 비공개 Loop 분석은 어디까지? | 공식 계약과 공개 SDK 경계, 내부 추정 금지. §4.6–4.7. |
| 30 | 첫 인터페이스는 무엇? | Coordinator/Model/Context/Policy/Tool/Store 등 책임에서 선택. §32. |

# D. 원문 보존과 재구성의 추적표

## D-1. 전체 내용의 배치

원문의 18장 권장안은 내용 체크리스트로 활용하고 장수·목차는 그대로 복제하지 않았다. 아래는 C 전체의 핵심 학습 내용을 어디에 보존했는지 보여준다. “본문” 배치는 발표 대상, “부록/노트”는 상세 참조다.

| C 절 | 보존할 내용 | 본문/부록 |
|---|---|---|
| 독자 안내 | 5대 질문·증거 등급·표 해석 | A-1/A-2, S02, X09 |
| 1–1.1 | 다른 제품 층위·용어 비배타성 | S01, S14, S25 |
| 2 | 공통 논리 지도·실행 소유권 | S01–S03, S38, X01 |
| 3 | 일곱 구조적 결론 | S02, S06, S09, S24, S29, S32–S40 |
| 4.1–4.7 | 일곱 실제/계약 실행 경로 | S04/S15/S22/S27/S29/S12/S25, X01 |
| 5–5.2 | 종료·Retry·종료 불변식 | S04/S17–S18/S24/S33, X02/X08 |
| 6–6.2 | Tool 7단계·제품별 경로·실패 4종 | S04/S08/S16/S24/S30, X02 |
| 7–7.3 | 병렬 5종·제품 구현·충돌·취소 | S09/S18/S31, X03 |
| 8–8.2 | 제어권·Subagent 책임 | S09/S13/S23/S26, X03 |
| 9 | Agent/Workflow/Hybrid·Graph 종류 | S15/S23/S28/S29/S31/S39 |
| 10–10.1 | 논리 입력 A–I·제품별 Context | S05/S12/S14/S19/S25/S27/S29, X04 |
| 11–11.2 | Prefix·무효화·4종 Cache 지원 의미 | S06/S36, X04 |
| 12–12.1 | 여섯 Memory·제품별 저장 | S07/S19/S24/S26/S28/S32, X04 |
| 13–13.1 | FTS/Vector/RAG·기억 품질 | S07, X04 |
| 14–14.1 | 압축 5종·보존 불변식 | S06, X04 |
| 15–15.2 | Skill/Tool/MCP/Plugin·품질 | S08, X05 |
| 16–16.4 | 강제 계층·Guardrail 범위·MiddlewareFailure | S10/S13/S16/S24/S30, X02/X06 |
| 17–17.1 | 승인 계약·제품 수단 | S20/S24/S30, X06 |
| 18–18.3 | 저장물·Exactly-once·Replay | S28/S31–S33, X06/X08 |
| 19–19.1 | Cron/Background/Queue/Resume | S10/S34, X07 |
| 20–20.4 | Host·응답 4시점·Tenant | S26/S35, X09 |
| 21 | Provider 기능 호환 | S36, X09 |
| 22–22.1 | Trace 단위·평가 4층 | S11/S21/S37, F |
| 23 | Hermes 설계·장단점·추적 | S03–S11 |
| 24 | PydanticAI 설계·장단점·추적 | S14–S21 |
| 25 | OpenAI 설계·장단점·추적 | S22–S24 |
| 26 | ADK 설계·장단점·추적 | S27–S28 |
| 27 | MAF 설계·장단점·추적 | S29–S31 |
| 28 | Claude Code 설계·장단점 | S12–S13 |
| 29 | Claude SDK 설계·장단점 | S25–S26 |
| 30 | 연구 질문별 비교 쌍 | S39, X09 |
| 31–31.2 | 24개 반례·분석 틀·3시퀀스 | S09/S24/S33, X07 |
| 32–32.1 | 참조 아키텍처·7인터페이스 | S38, X08 |
| 33 | 최소 Runtime 의사코드·원자성 한계 | S38, X08 |
| 34–34.1 | 요구 기반 선택·5가지 Trade-off | S39, X09 |
| 35 | 정성 연구 매트릭스·범례·각주 | X09 |
| 36 | 선정 전 검증 | S36–S40, X09, H |
| 37–37.1 | 발표 핵심·대표 코드·근거 구분 | A, B, D, H |
| 38 | 복습 질문 30개 | X10 |
| 39 | 열 가지 결론 | S40 노트, A-1, E |
| Appendix A | 버전·고정 소스·공개 경계 | G |
| Appendix B/B1 | 기존 연구 관계·검증 한계 | A-2, G/H |

## D-2. 내용을 바꾸지 않기 위한 편집 제한

- 제품별 장점과 한계는 대본에서 한 쌍으로 설명한다. 그림을 간단히 하려고 외부 인가·저장·Host 책임을 지우지 않는다.
- 같은 “Memory/Graph/Guardrail” 명칭을 같은 자료형·같은 구현으로 번역하지 않는다.
- EndStrategy 상세 순서, 기본값, Callback의 정확한 호출 조건 등 C가 상세히 확정하지 않은 부분은 임의로 채우지 않는다. 이번 블루프린트는 그 조건 없이도 전달 가능한 핵심 메시지와 후속 관찰 질문을 확정했다.
- C의 일부 축약 경로는 대표 경로로 표시한다. ADK 신·구 경로, Workflow Resume 범위, 실험 기능이 버전별로 달라질 수 있으므로 최종 구현자가 새로운 기능 보장으로 일반화하지 않는다.
- C §14의 제목을 “압축해도 원본이 반드시 영구 보존된다”로 바꾸지 않는다. Context 변환과 보존 정책은 구별하되 실제 저장본 처리도 확인해야 한다.
- C §17 상태도의 `execute once` 의도는 §18.1의 한계와 함께 읽는다. 단순 승인·Checkpoint로 Exactly-once가 해결된다고 말하지 않는다.
- C §35의 `—`는 미지원, `◎`는 성능 점수가 아니다. 더 강한 표현으로 바꾸지 않는다.
- C Appendix B의 일부 1차 문서명은 실제 로컬 파일명과 다르다. 그 목록을 경로 검증 없이 구현 데이터에 복사하지 않는다. 이번 발표의 내용 출처는 C로 충분하며, 개별 학습 MD는 추가 추적 시 실제 경로를 확인한다.

# E. 발표자 심층 설명 — 화면에 통째로 넣지 말 것

## E-1. 일곱 기술을 각각 한 문장으로 회수하기

| 기술 | 설계 교훈 | 반대급부·한계 |
|---|---|---|
| Hermes | 완성형 Harness가 Context·Tools·Memory·Session·채널·예약을 어떻게 통합하는지 읽는다. | 설정·영속성·정책·코드 범위의 이해 부담. 자율 Skill은 검증 필요. |
| Claude Code | 작업 환경·지침·권한·Skills를 통합한 제품 계약을 활용한다. | 핵심 엔진 비공개로 저수준 추적·수정 제약. |
| PydanticAI | 내부 Graph와 검증·Retry·종료·Dependencies의 계약을 함께 설계한다. | 타입이 사실을 보증하지 않음. 장기 저장·Host·외부 권한은 별도. |
| OpenAI | 명시적 Runner/NextStep으로 계속·종료·이관을 구분한다. | 완성형 플랫폼 전체가 아님. Guardrail 적용 범위 확인 필요. |
| Claude SDK | CLI Harness를 앱에 연결하고 공개 통신·수명을 관리한다. | 내부 Loop 소유권과 Host의 자원·격리 책임을 혼동하면 안 됨. |
| ADK | Event와 Session/State 변화로 실행을 관찰한다. | 순서·중복·Branch·Resume·완료 범위 이해 필요. |
| MAF | Pipeline·정책·모델-Tool·Harness·Workflow 책임을 합성한다. | 중첩 순서·예외 전파가 복잡. 외부 부작용은 별도 계약. |

근거: C §§23–30. 위 장단점은 원문의 [INF] 해석이며 도입 성과가 아니다.

## E-2. PydanticAI의 이점을 타입 검증 한 줄로 끝내지 않기

“검증을 잘한다” 대신 다음 연결을 설명한다. Node 경계로 모델 요청/도구 처리/종료를 추적하고, Validator 실패를 모델 피드백과 예산으로 연결하며, EndStrategy가 Final/Tool 공존 처리를 다르게 한다. `sequential` 장벽은 실행 순서 제약을 표현한다. Dependencies는 실행 자원과 테스트 대체를 분리하는 수단이다. Capabilities/Hooks는 개입 위치를 제공하되 도메인 정책·권한·저장은 앱이 설계해야 한다. 이 모든 선택을 “자동으로 도메인 정답을 보장한다”로 요약하지 않는다. 근거: C §§4.2, 5–7, 16, 24.

## E-3. 반도체 사례에서 선별할 시사점

- **데이터 기준:** 같은 Lot이라도 기간·분모·Snapshot이 다르면 조회값·예측 입력이 달라진다. 근거 ID를 Tool 결과와 보고서에 연결하는 설계를 검토한다.
- **절차 신선도:** SOP 개정은 안정 Prefix·Memory·Skill의 갱신 시점과 연결된다. 캐시 hit와 최신 절차 사용을 다른 평가 축으로 본다.
- **권한:** Schema상 유효한 Lot ID도 비인가일 수 있다. Tool Backend·DB 자격증명에서 실제 경계를 강제한다.
- **병렬:** 독립 조회의 속도보다 데이터 의존성·같은 시점·공유 자원 충돌 여부가 먼저다.
- **승인/재개:** 승인한 보고서 버전과 실행할 버전, 외부 발행 완료 여부를 확인한다. 같은 Tool을 다시 호출해도 되는지는 도구 계약이다.
- **품질:** 오류율 계산은 결정적 정답으로, 설명은 근거 충실도·가설 구분으로, 예측은 정의된 target/평가 조건으로 판단한다. 이번 문서는 실제 데이터·예측 방법·정확도를 확정하지 않는다.

이는 C의 원리를 적용한 [INF] 설계 질문이다. 일곱 장마다 반복하지 않고 S06/S09/S16/S20/S31/S33/S37에서 필요한 지점만 사용한다.

## E-4. 마지막에 설명할 열 가지 결론의 회수

Loop 소유권, 비배타적 SDK/Framework, 모델 제안과 인가의 차이, 병렬성의 층, 저장물의 차이, Prefix 계산 재사용, Guardrail의 범위, Resume와 Exactly-once 구분, 공개 SDK와 비공개 CLI 경계, 요구 기반 선택이라는 C §39의 열 가지 결론을 S40의 세 문장에 묶는다. 화면에 열 줄을 한꺼번에 추가하지 않는다.

# F. Demo 1·2 연결 계약 — 실제 제작은 후속 작업

## F-1. 슬라이드와 데모의 분리

C는 데모 구현·실측을 제외하므로 기술 내용의 증거로 존재하지 않는 데모를 인용하지 않는다. 이전 발표 구상에서 요청한 **Demo 1=Hermes, Demo 2=PydanticAI**는 별도 페이지 제작 명세로 유지한다. 본문 두 장은 실제 데모 없이도 관찰 목표를 설명할 수 있어야 한다. 데모 페이지 주소·Trace 경로는 후속 구현 후 설정하고, 지금 임의의 완료 파일 경로를 만들지 않는다.

| 항목 | Demo 1: Hermes | Demo 2: PydanticAI |
|---|---|---|
| 목적 | 통합 Harness 안에서 요청·도구·상태가 연결되는 모습을 관찰 | 개발자가 작성한 계약과 SDK 내부 Node/검증/실행을 대응 |
| 시나리오 | 조회→근거 분석→예측의 공유 시나리오 | 동일 입력·데이터 정의로 비교 |
| 우선 관찰 | 실제 모델 요청, Intent/Tool/결과, 다음 Context, 저장 | Schema/Deps 경계, Graph, Tool·Output/Retry, 실제 종료 분기 |
| 선택 관찰 | Skill 로딩·Subagent·Compaction, 실제 발생 시 | EndStrategy 시험·Deferred·Capability/Harness 확장, 검증 후 |
| 화면 | 전체 구조의 활성 영역+실제 Trace+payload 요소별 보기 | 작성 코드와 내부 경계+Node/메시지/분기+실제 Trace |
| 보존 조건 | 기본 Hermes 로직·기존 설치/Memory/DB를 보존하고 가역 관찰 우선 | Core 최소 실행부터, 별도 Harness 버전·기능을 분리 |
| 종료/복귀 | 기록의 종료 이유 확인→S11→S12 | 실제 검증 범위 확인→S21→S22 |

## F-2. 실제 기록과 설명용 재생을 구분

실제 Agent를 실행한 뒤 기록을 Space로 단계 탐색하는 방식을 우선 검토한다. Space가 실제 런타임을 매 단계 강제 정지시켜 순서·동시성을 바꾸는 기능이라고 전제하지 않는다. live/실제 사전 기록/Scripted Runtime 시험/설명용 고정 도식은 화면에서 식별한다.

각 기록은 사용 버전·모델·실행 시점·run/session/model/tool/parent ID를 연결한다. “최종 요청”은 Provider 변환 전 객체인지 변환 후 payload인지 관찰 지점을 적는다. 비밀 key·민감 데이터는 저장 전에 가린다. 비공개 Chain-of-thought를 표시하는 UI를 만들지 않는다. 관찰기 부착 전후의 핵심 동작·오류·취소·정책 경로가 유지되는지 확인한다.

원하는 Tool·Child·압축이 실제 발생하지 않았다면 해당 run에서 미발생으로 남긴다. 자연 모델이 내놓지 않은 응답을 삽입하여 실제 Trace로 표시하지 않는다. EndStrategy 같은 분기 확인은 고정 응답의 Runtime 시험과 실제 Provider 통합을 구분한다. 근거: C §22.1.

## F-3. 구현·이관 전제와 완료 조건

후속 구현 에이전트는 환경을 자동 점검하고 필요한 Hermes 소스 ZIP·Python·PydanticAI·선택 의존성을 확보·설치한다. 기존 설치가 있으면 경로·버전을 확인하고 보호한다. 현재 PC의 외부 API와 다른 PC의 vLLM 연결은 설정·기능 호환을 각각 검증한다. C §21의 API 호환을 단순 URL 교체로 축소하지 않는다.

데이터·오류율 분모·기간·예측 target·실제 패키지 조합·모델 ID·환경·Hook·출력 Schema·승인 UI·live 비중은 구현 전 확정 사항이다. 현재 자료만으로 실행 명령이나 성공 로그를 확정할 수 없다. 캐시 실측은 선택 범위이며 주 데모의 성공 조건으로 만들지 않는다.

실제 제작 순서는 **발표자료 → Demo 1 → Demo 2 → 설치·실행·검증 → 가이드**다. 최종 가이드는 검증한 코드에서 정확한 cwd·명령·환경변수·데이터·기대 화면/로그·복귀 위치·실패 대안·다른 PC 설정 차이·원복을 추출한다. 다른 PC 미검증이면 성공으로 기록하지 않는다. 이번 Markdown 작성에서 이 제작·설치를 수행하지 않는다.

# G. 근거·버전·고정 소스 인덱스

## G-1. 로컬 원본과 기술 버전

| ID | 경로·범위 |
|---|---|
| C | `C:\Users\namws\OneDrive\Desktop\study_for_agent_framework\Agent_Framework_7종_최종_종합_비교_분석.md` — 발표 내용의 기준. §§1–39, Appendix A/B. |
| D | `C:\Users\namws\OneDrive\Desktop\study_for_agent_framework\agent_framework_seminar_1_slide_blueprint.md` — 디자인·슬라이드/노트 분리·단계 조작·검수의 기준. |

| 기술 | 원문 분석 기준 | 범위 |
|---|---|---|
| Hermes | v0.22.5 | 공개 Core/Gateway/Tools/Session |
| PydanticAI | Core v2.61.0 | 별도 Harness는 별도 제품·버전 |
| OpenAI Agents SDK | Python v0.24.0 | Python Runner/Tools/RunState |
| Google ADK | Python v2.13.0 | Agent/Flow/Workflow |
| Microsoft Agent Framework | Python python-1.24.0 | Core/Workflow/Harness |
| Claude Code | CLI v2.1.314 | 공식 제품 계약, 핵심 Loop 비공개 |
| Claude Agent SDK | Python v0.2.176 / 번들 CLI v2.1.316 | 공개 SDK·CLI 통신 경계 |

Claude Code 단독 버전과 SDK 번들 CLI를 같은 버전으로 합치지 않는다. 아래 URL은 C에서 계승한 링크이며 이번 작업에서 외부 열람·실행 검증을 새로 수행한 것은 아니다.

## G-2. 제품별 출처 — Sources 패널에서 사용할 링크

### G-H. Hermes

- [고정 소스 트리](https://github.com/NousResearch/hermes-agent/tree/v0.22.5)
- [conversation_loop.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/conversation_loop.py), [turn_tool_round.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/turn_tool_round.py), [turn_tool_validation.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/turn_tool_validation.py)
- [tool_executor.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/tool_executor.py), [registry.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/registry.py)
- [prompt_builder.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/prompt_builder.py), [prompt_caching.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/prompt_caching.py), [context_compressor.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/context_compressor.py), [hermes_state.py](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_state.py)
- [Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture), [Agent Loop](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop), [Session Storage](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage), [Prompt Caching](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-caching)

### G-P. PydanticAI

- [Agent API 소스](https://github.com/pydantic/pydantic-ai/tree/v2.61.0/pydantic_ai_slim/pydantic_ai/agent), [_agent_graph.py](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_agent_graph.py)
- [tool_manager.py](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/tool_manager.py), [_tool_execution.py](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_tool_execution.py), [_output.py](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_output.py), [tools.py](https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/tools.py)
- [공식 문서](https://ai.pydantic.dev/), [Tools](https://ai.pydantic.dev/tools/), [Output](https://ai.pydantic.dev/output/)

### G-O. OpenAI Agents SDK

- [run.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run.py), [run_loop.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/run_loop.py), [run_steps.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/run_steps.py), [turn_resolution.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/turn_resolution.py)
- [tool_execution.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/tool_execution.py), [guardrails.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/guardrails.py), [run_state.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_state.py), [session_persistence.py](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/run_internal/session_persistence.py)
- [Running Agents](https://openai.github.io/openai-agents-python/running_agents/), [Guardrails](https://openai.github.io/openai-agents-python/guardrails/), [Handoffs](https://openai.github.io/openai-agents-python/handoffs/), [Testing](https://openai.github.io/openai-agents-python/testing/)

### G-G. Google ADK

- [runners.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/runners.py), [llm_agent.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/agents/llm_agent.py), [base_llm_flow.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/flows/llm_flows/base_llm_flow.py)
- [_caller.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/flows/llm_flows/tools/_caller.py), [_batch_executor.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/flows/llm_flows/tools/_batch_executor.py), [parallel_agent.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/agents/parallel_agent.py)
- [event.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/events/event.py), [base_session_service.py](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/sessions/base_session_service.py), [Workflow 소스](https://github.com/google/adk-python/tree/v2.13.0/src/google/adk/workflows), [공식 ADK](https://adk.dev/)

### G-M. Microsoft Agent Framework

- [_agents.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_agents.py), [_clients.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_clients.py), [_tools.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_tools.py), [_middleware.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_middleware.py), [_sessions.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_sessions.py)
- [_harness/_loop.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_harness/_loop.py), [_workflows/_workflow.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_workflow.py), [_runner.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_runner.py), [_checkpoint.py](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_checkpoint.py)
- [Agent Pipeline](https://learn.microsoft.com/en-us/agent-framework/agents/agent-pipeline), [Workflows](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/), [Checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)

### G-C. Claude Code

- [공식 개요](https://code.claude.com/docs/en/overview), [공개 저장소](https://github.com/anthropics/claude-code)
- [Memory](https://code.claude.com/docs/en/memory), [Skills](https://code.claude.com/docs/en/skills), [Permissions](https://code.claude.com/docs/en/permissions), [Hooks](https://code.claude.com/docs/en/hooks), [Subagents](https://code.claude.com/docs/en/sub-agents)
- 핵심 Loop·Scheduler 전체의 고정 소스 링크가 있다는 식으로 위 문서 링크를 사용하지 않는다.

### G-S. Claude Agent SDK

- [query.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/query.py), [client.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/client.py), [_internal/client.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/client.py)
- [subprocess_cli.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/transport/subprocess_cli.py), [_internal/query.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/query.py), [message_parser.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/message_parser.py), [types.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/types.py), [session_resume.py](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/session_resume.py)
- [SDK 공식 개요](https://code.claude.com/docs/en/agent-sdk/overview), [Python 릴리스](https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.176)

# H. 후속 구현 지시와 완료 검수

## H-1. 발표 앱 구조 권고

기존 프로젝트 학습 페이지는 수정·교체하지 않는다. 발표 앱은 별도 폴더로 구성하되 정확한 폴더명·프레임워크는 후속 구현 시 결정한다. 최소 구조는 `slides data`, `notes`, `sources`, `shared architecture components`, `tokens.css`, `navigation`, `appendix router`다. 기존 학습 웹사이트를 슬라이드로 단순 변환하지 않는다.

일곱 구조 컴포넌트의 안정 ID는 `arch-hermes`, `arch-claude-code`, `arch-pydantic`, `arch-openai`, `arch-claude-sdk`, `arch-adk`, `arch-maf`로 한다. 각 Node에는 역할과 근거를 연결한다. Claude SDK의 CLI 영역은 Claude Code와 같은 의미·색을 사용한다.

상태는 `slideId`, `buildStep`, `notesOpen`, `reducedMotion`, `appendixReturn`, `selectedComparison`, `demoLinks` 정도로 최소화한다. 발표 앱에서 실제 Agent 환경·인증·실행 상태를 관리하지 않는다. 라이브 데모의 상태와 로컬 설명용 build state는 분리한다.

## H-2. 내용·도식 검수 체크리스트

- [ ] S00–S40, X01–X10 ID가 유일하고 목차·번호·복귀가 일치한다.
- [ ] 일곱 기술이 각각 전체 구조부터 시작하며 세부 화면은 같은 구조의 확대다.
- [ ] 원문 §§1–39 및 Appendix의 핵심 내용이 D-1에 연결되어 있다.
- [ ] 기초 개념을 다시 길게 강의하지 않고 실제 제품의 차이를 설명한다.
- [ ] Hermes Intent·실행·결과 저장이 구분되고 외부 원자성 보장으로 표현되지 않는다.
- [ ] PydanticAI 내부 Graph·별도 사용자 Graph·선택 Harness가 분리되어 있다.
- [ ] EndStrategy의 원문에 없는 상세 순서·기본값을 새로 단정하지 않았다.
- [ ] as-tool의 부모 반환과 Handoff의 제어권 이전이 다르게 그려진다.
- [ ] Multiple Tool Calls·Tool 병렬·Child Loop·Workflow·서버 동시성이 혼합되지 않는다.
- [ ] Guardrail의 대상·시점·실패 전파·Backend 권한이 구분된다.
- [ ] Input Guardrail과 모델이 병행될 수 있는 그림이 완전 사전 차단으로 설명되지 않는다.
- [ ] MAF의 세 Loop와 Middleware 위치·정책 실패 경로가 구분된다.
- [ ] ADK Agent final과 전체 Workflow 완료, Event와 Artifact가 혼동되지 않는다.
- [ ] CLI 내부 비공개 영역을 공개 SDK 소스로 입증했다고 하지 않는다.
- [ ] Cache 재사용과 전송 생략·앱 캐시·압축·영구 삭제를 구분한다.
- [ ] Resume·승인·Checkpoint가 Exactly-once를 자동 보장한다고 하지 않는다.
- [ ] X09 범례·각주가 유지되고 제품 성능 순위로 바뀌지 않는다.
- [ ] 반도체 예시·가상 함수·설명 숫자·테스트 질문이 실제 결과로 제시되지 않는다.
- [ ] Sources·버전·증거 등급이 노트와 연결되고 외부 링크가 임의로 생성되지 않는다.

## H-3. 화면·조작 검수 체크리스트

- [ ] 1920×1080과 1280×720에서 제목·코드·선·표가 읽히고 겹치지 않는다.
- [ ] 모든 단계의 화살표 주체·방향·분기 조건이 올바르다. 이동 효과가 실행 순서를 바꾸지 않는다.
- [ ] Next/Prev는 build step을 우선 처리하고 목차 점프·부록 복귀도 안정적이다.
- [ ] N 노트가 일반 청중 화면에 자동 노출되지 않는다.
- [ ] Reduced motion·Pause·Reset·최종 정지 상태가 제공된다.
- [ ] 폰트·도식·설명용 고정 데이터는 오프라인에서도 동작한다.
- [ ] Sources는 명시적 조작으로만 열리고 발표 중 외부 창이 자동으로 뜨지 않는다.
- [ ] 미연결 데모 버튼은 비활성/미연결 표시이며 깨진 링크가 없다.
- [ ] 실제 기록·설명용 재생·Scripted 시험·live가 구분되고 비밀정보가 보이지 않는다.
- [ ] 축약 경로에서도 일곱 구조·핵심 차이·한계·선택 기준이 남는다.

**제작 완료의 기준:** 보기 좋은 화면뿐 아니라, 원문의 학습 의미와 근거 수준을 유지하면서 “그래서 우리 Agent에서는 무엇을 맡기고 무엇을 설계해야 하는가?”를 설명할 수 있는 발표자료를 만드는 것이다.
