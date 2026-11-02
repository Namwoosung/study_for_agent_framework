# 2차 세미나 발표 기획 및 자료 인계 문서

작성일: 2026-11-03 / 로컬 자료 검토 기준: 2026-11-02부터 이어진 작업  
프로젝트 루트: `C:\Users\namws\OneDrive\Desktop\study_for_agent_framework`  
이번 산출물의 단계: **로컬 자료 분석과 발표 기획 인계**. 최종 슬라이드 블루프린트, 발표자료, 데모 구현물은 아직 아니다.

## 1. 작업 목적 및 최종 지향점

### 1.1 발표가 해결해야 할 질문

청중은 1차 세미나에서 Agent, Core, Tool, Orchestration의 기본 개념을 이미 학습했다. 2차의 질문은 “Agent란 무엇인가?”가 아니라 **“이 기술에서는 누가 반복 실행을 담당하고, 모델 입력과 도구 실행을 어떻게 구성하며, 개발자가 어디까지 구현·통제해야 하는가?”**이다. Hermes와 PydanticAI를 깊이 이해한 뒤 다른 다섯 기술을 같은 질문으로 비교하여, 3차의 실제 도메인 Agent 개발로 이어간다. 근거: [FLOW], [REF1].

핵심 메시지는 다음과 같다.

- **완성된 실행 환경을 활용할 것인지, SDK로 애플리케이션의 실행 계약을 조립할 것인지**가 개발 범위와 운영 책임을 바꾼다. 제품명이나 기능 개수만으로 선택하지 않는다.
- 동일한 Tool·Memory·Guardrail·Multi-agent라는 이름 아래에도 실행 시점, 저장 범위, 제어권, 실패 처리의 차이가 있다. 그 차이를 실제 구조와 관찰 가능한 데이터로 설명한다.
- 반도체 도메인에 적용할 때는 잘 만들어진 문장보다 **어떤 Lot·시점·SOP 버전의 근거로 어떤 도구를 실행했는지**, 그리고 승인·재개·재실행이 어떤 결과를 남기는지가 중요하다. 이 내용은 제품의 검증된 도입 성과가 아니라 기존 자료에 근거한 설계 시사점이다. 근거: [CMP] §§4–22, [COMMENTS], 각 주제의 실무 코멘트.

### 1.2 대상과 발표 범위

대상은 Agent의 기초를 알고 실제 개발·활용을 고민하는 동료다. 구체적인 청중 직무 분포, Python 숙련도, 발표·질의응답·데모 시간은 **미확정**이다. 1차 자료의 시간과 장수를 2차의 제약으로 가져오지 않는다.

다룰 순서는 **Hermes → Claude Code → PydanticAI → OpenAI Agents SDK → Claude Agent SDK → Google ADK → Microsoft Agent Framework**로 고정한다. Hermes와 PydanticAI에 설명과 데모의 중심을 둔다. LangChain/LangGraph, Mistral AI Studio, vLLM/SGLang 자체의 상세 설명은 다른 발표자의 영역이다. vLLM은 이번 발표에서 연결·호환·배포 경계상 필요한 범위만 다룬다. 근거: [FLOW] 작성 원칙·도입.

### 1.3 최종 결과물과 단계별 책임

| 단계 | 담당 | 결과와 완료 조건 |
|---|---|---|
| 이번 단계 | Codex | 이 인계 문서 한 개. 로컬 근거, 내용 구성, 조사 질문, 두 데모의 요구사항을 연결한다. |
| 다음 단계 | GPT/조사 AI | 필요한 외부 확인을 수행하고 최종 2차 세미나 블루프린트를 작성한다. 슬라이드별 콘텐츠·시각 구성·발표자 설명·데모 연결·근거를 확정한다. |
| 제작 단계 | Codex/구현 에이전트 | 블루프린트 기반 발표자료 제작 → Demo 1 구현 → Demo 2 구현 → 설치·실행·검증 → 검증 결과에 맞춘 발표자 실행·이관 가이드 작성. 구현에 필요한 환경 점검·설치는 해당 단계에서 자동 수행한다. |
| 최종 지향점 | 발표자 | 발표자료 전체, 두 데모의 실행 가능한 코드, 재현 가능한 환경 구성, 다른 PC의 vLLM 연결 절차, 발표·시연 가이드를 확보한다. |

이번에는 웹 검색, 새 기술 조사, 외부 자료 수집, 소스 다운로드, 패키지 설치, Agent 실행, 발표용 HTML/PPT 제작을 수행하지 않았다. 조사 문서의 정적 분석 결과를 인계했으며 실행 검증을 대신하지 않는다.

## 2. 발표 의도·작성 원칙

### 2.1 우선순위와 상태 표기

판단 우선순위는 **현재 [FLOW]의 명시적 의도 > 최신 프로젝트 조사 자료 > [REF1]의 형식 참고**다. 기술 사실의 충돌은 우선순위만으로 진위를 결정하지 않고 §8에 남긴다. 동일 문서의 초기 고민과 상단의 명시적 규칙이 다르면 명시적 규칙을 적용한다.

| 표기 | 이 문서에서의 의미 |
|---|---|
| 기존 자료 확인됨 | 로컬 문서에 설명과 근거가 있다. 문서에 수록된 소스 분석·공식 문서 주장을 확인했다는 뜻이며, 이번 PC에서 실행하여 입증했다는 뜻은 아니다. |
| 추가 조사 필요 | 버전별 실제 API, 지원 조건, 공개 소스와의 일치 여부 등을 다음 조사 AI가 확인해야 한다. |
| 미확정 | 발표자 결정, 대상 환경 정보, 데이터, 구현 선택이 아직 정해지지 않았다. 기술 조사만으로 확정할 수 없는 경우도 포함한다. |
| 기획 제안 | 기존 의도를 실현하기 위한 구성·예시·테스트 설계다. 제품의 기본 기능이나 이미 구현된 결과로 소개하지 않는다. |

### 2.2 반드시 보존할 발표 규칙

| 원칙 | 블루프린트에 적용할 방식 |
|---|---|
| 기술별 전체 아키텍처를 먼저 제시 | 일곱 기술 모두 큰 구조를 먼저 보여주고, 같은 그림의 해당 영역을 강조하며 세부를 설명한다. 각 기술을 공통 Loop 그림 한 장으로 대체하지 않는다. |
| 단계적으로 이해시키기 | Pydantic → PydanticAI Core → 별도 Harness의 관계를 짧게 안내한 뒤 전체 구조로 들어간다. 다른 기술도 필요 용어만 보충한다. |
| 1차 개념 반복 최소화 | Agent·Tool·Orchestration 정의는 재강의하지 않는다. 실제 분기·상태·정책 시점을 설명하기 위한 짧은 연결만 허용한다. |
| 중심과 비교 대상의 깊이 구분 | Hermes·PydanticAI는 실제 흐름과 개발 예시까지 깊게 다룬다. 나머지는 제공 범위, 개발자 책임, 내부 차이, 장단점에 집중한다. |
| 종료·정책을 구체적으로 설명 | “끝나면 종료”, “Guardrail이 검사”로 끝내지 않는다. 응답 분류, 유효 출력, Tool 결과, 승인 대기, 예산, 실패가 어떤 분기를 만드는지 보여준다. |
| 메서드 이름보다 목적과 구조 | 실제 이름은 가능한 한 유지하되, 대표 경로만 본문에 제시한다. 축약·의사코드·실행 검증된 코드를 구분한다. 흐름 문서의 예시 코드를 그대로 실행 가능하다고 선언하지 않는다. |
| Orchestration 특별 설명 | Agent-as-Tool, Handoff, Subagent, Workflow를 제어권·반환 위치·컨텍스트·상태 공유 기준으로 구별한다. “여러 Agent”만으로 동일시하지 않는다. |
| 실무 시사점은 필요한 곳에 | 각 개념에 장식적인 코멘트를 붙이지 않는다. 데이터 신선도, 승인할 인자, 부작용, 도메인 근거처럼 설계 선택을 바꾸는 지점에만 연결한다. |
| Hermes·Claude Code의 유용한 명령 | 기능 목록 대신 세션 재개·컨텍스트·메모리 등 실행 구조와 연결되는 명령을 선별한다. 정확한 slash/CLI 구문은 후속 버전 확인 후 사용한다. |
| 두 데모만 별도 웹페이지로 구성 | Demo 1=Hermes, Demo 2=PydanticAI. 슬라이드 HTML에 내장하지 않고 설명한 부품과 데모 화면을 연결한다. |
| 실제 내부 데이터 관찰 | 실제 LLM 요청 직전 데이터, 도구 실행, 메시지 누적, 분기와 상태 변화를 보여준다. 큰 데이터는 화면에서 분해하여 읽힌다. |
| Hermes 기존 로직 보존 | 계속 사용할 실제 Hermes의 구조와 기능을 유지한다. 가능하면 무수정 관찰, 필요하면 제거 가능한 Hook·Wrapper 등을 검토한다. |
| 이관 가능한 결과 | 현재 PC의 외부 API 검증 후 다른 PC의 로컬 vLLM에 적용할 수 있도록 실제 코드와 실행 결과에서 상세 가이드를 추출한다. |
| 검증 요청의 처리 | [FLOW]의 “추가 검증” 요청은 이번 단계에서는 과제로 정리한다. 다음 단계에서 맞는 내용은 자연스럽게 반영하고 문제·변경점만 보고하되, 근거 이력은 유지한다. |
| 마지막 운영 관점 | 중앙 Agent 서버와 로컬 Agent+중앙 LLM의 가능성을 비교할 수 있다. 확정 구축안이나 필수 세 번째 데모로 확대하지 않는다. |

### 2.3 1차 자료에서 재사용할 형식적 장점

[REF1]의 장점은 **한 화면의 중심 주장, 설명 단계별 강조, 짧은 화면 문구와 충분한 발표자 노트의 분리, 의미가 일관된 색상, 편집 가능한 도식**이다. 16:9, 충분한 여백, 큰 글자, 짧은 코드, 출처와 Q&A의 노트 배치도 참고할 만하다.

디자인 톤의 후보는 어두운 배경 `#0B1020`, 밝은 본문 `#EFF4FF`, 보조 텍스트 `#9EACC8`이며 Model=파랑, Runtime=보라, Tool=초록, Context=주황의 의미 색상을 유지할 수 있다. 정확한 픽셀·장면 배치·슬라이드 수는 다음 GPT가 최종 결정한다. 구성요소·제어 흐름·시간 흐름이 다른 그림은 선과 화살표의 의미도 구분한다.

단계 전환은 키보드와 정지 상태에서도 읽혀야 한다. 애니메이션이 설명을 대신하지 않도록 하고, 발표자 노트·현재 단계·복귀 위치를 설계한다. 1차의 목차, 30장 구성, 기초 설명, 고정 모의 예제, 시간 배분을 복제하지 않는다. 특히 **2차 데모는 실제 실행 데이터**라는 현재 요구가 우선이다. 기존 학습 사이트의 화면과 SVG는 원문 관계를 이해하는 참고 자산이며, 1차 슬라이드의 실제 렌더링 증거로 취급하지 않는다.

## 3. 기존 자료 분석 요약

### 3.1 근거 파일 목록과 인용 규칙

아래 경로는 모두 위의 프로젝트 루트를 기준으로 한다. `[H2]` 같은 표기는 해당 **실제 로컬 파일 경로의 약칭**이다. 절 번호는 문서의 번호 붙은 장을 뜻한다. 후속 GPT가 외부 파일을 함께 받지 않더라도 핵심 내용은 §4–7에서 이해할 수 있도록 정리했다.

| 약칭 | 실제 경로 | 용도 |
|---|---|---|
| FLOW | `2차_세미나_발표_흐름.md` | 최우선 발표 의도, 고정 순서, Hermes/PydanticAI 설명 구상, 두 데모와 PC 이관 요구. 약 1,014행. |
| REF1 | `agent_framework_seminar_1_slide_blueprint.md` | 이미 발표한 1차의 형식·밀도·도식·발표자 노트·조작 원칙 참고. 내용 구성의 원본이 아니다. |
| CMP | `Agent_Framework_7종_최종_종합_비교_분석.md` | 일곱 기술의 공통 비교 축, 실패 사례, 운영·보안·복구 질문, 고정 버전 소스 지도. 약 1,510행. |
| H1 / H2 / HC | `hermes/Hermes_Agent.md` / `hermes/Hermes_Agent_2차_심층_학습_분석.md` / `hermes/Hermes_Agent_발표_실무_시사점_코멘트.md` | Hermes 기초·전체 구조 / 실제 반복·도구·저장 경로 / 도메인 해석. |
| C1 / C2 / CC | `Claude_Code/Claude_Code.md` / `Claude_Code/Claude_Code_2차_심층_학습_분석.md` / `Claude_Code/Claude_Code_발표_실무_시사점_코멘트.md` | Claude Code 사용·구조 / 공개 계약과 내부 비공개 경계 / 도메인 해석. |
| P1 / P2 / PC | `PydanticAI/PydanticAI.md` / `PydanticAI/PydanticAI_2차_심층_학습_분석.md` / `PydanticAI/PydanticAI_발표_실무_시사점_코멘트.md` | PydanticAI 도입 / Core·내부 Graph·검증·Capability·별도 Harness / 도메인 해석. |
| O1 / O2 / OC | `OpenAI_Agents_SDK/OpenAI_Agents_SDK.md` / `OpenAI_Agents_SDK/OpenAI_Agents_SDK_2차_심층_학습_분석.md` / `OpenAI_Agents_SDK/OpenAI_Agents_SDK_발표_실무_시사점_코멘트.md` | Runner·Tools·Handoff·RunState / 실제 다음 단계와 승인 전파 / 도메인 해석. |
| S1 / S2 / SC | `Claude_Agent_SDK/Claude_Agent_SDK.md` / `Claude_Agent_SDK/Claude_Agent_SDK_2차_심층_학습_분석.md` / `Claude_Agent_SDK/Claude_Agent_SDK_발표_실무_시사점_코멘트.md` | Python SDK와 Claude Code CLI 연결 / 통신·권한·세션 경계 / 도메인 해석. |
| G1 / G2 / GC | `Google_ADK/Google_ADK.md` / `Google_ADK/Google_ADK_2차_심층_학습_분석.md` / `Google_ADK/Google_ADK_발표_실무_시사점_코멘트.md` | ADK Agent·Flow·Event·Session·Workflow / 실행·저장·복구 경계 / 도메인 해석. |
| M1 / M2 / MC | `Microsoft Agent_Framework/Microsoft_Agent_Framework.md` / `Microsoft Agent_Framework/Microsoft_Agent_Framework_2차_심층_학습_분석.md` / `Microsoft Agent_Framework/Microsoft_Agent_Framework_발표_실무_시사점_코멘트.md` | Agent Pipeline·Tools·Workflow / Middleware·승인·Superstep / 도메인 해석. 폴더명에 공백이 있다. |
| COMMENTS | `html/seminar-comments.json`, `html/seminar-comment-map.json`, `html/세미나_코멘트_안내.md` | 기존 17개 실무 코멘트의 원본과 삽입 위치. 위 일곱 코멘트 MD는 같은 내용의 동반 산출물이며 독립 근거 일곱 건으로 중복 집계하지 않는다. |
| HUB | `index.html`, `html/README.md` | 일곱 주제의 기본·심층 학습 페이지를 찾아가는 전체 목차. |
| RULES | `AGENTS.md` | 원문 충실성·가독성·실코드/의사코드 구분·디렉터리 규칙. 이번 사용자 요청의 문서 작성 범위가 웹사이트 제작 규칙보다 우선한다. |

### 3.2 코드·시각 자료·검증 자료의 해석

일곱 주제의 `html/`에는 기본 교재, `html/deep/`에는 심층 교재가 있다. `content-map.json`, `site.config.mjs`, `build.mjs`, `validate.mjs` 등은 원문-학습 페이지 연결, 편집 구성, 생성·검사에 쓰인다. SVG 도식·PNG 미리보기·브라우저 QA는 기존 설명의 표현 자산이다. 예를 들어 `hermes/html/editorial.mjs`도 실행 엔진이 아니라 학습 안내 편집 자료다.

탐색 시점에 Markdown 41개, HTML 228개, SVG 106개, PNG 16개가 있었고, HTML은 기본·심층·전체 홈을 포함한다. 이 수량은 자료 규모를 설명하며 발표 분량의 목표가 아니다. 프로젝트 내부에는 `.py`, `.ipynb`, `.zip`, `.pptx`, `.pdf`, `.docx` 파일이나 실행 가능한 두 데모의 구현 소스가 발견되지 않았다. 실제 프레임워크 소스 체크아웃이 있다는 증거도 없다. 다만 프로젝트 밖의 설치 환경은 이 결과만으로 판단할 수 없다.

`html/seminar-validation.json`, `html/seminar-baseline.json`, 각 사이트의 검증·QA 기록은 내용 보존·링크·표시 검사의 근거다. **SDK API 호환성, Agent 실제 실행, 모델 성능, 보안 보장, vLLM 연결 성공을 입증하지 않는다.** MD에 포함된 코드 역시 실행 완료 결과와 구분한다.

### 3.3 조사 문서의 기준 버전

| 기술 | 심층·종합 자료의 분석 기준 | 인계 시 주의점 |
|---|---|---|
| Hermes | `v0.22.5` | 현재 설치 버전과 일치하는지 미확인. 기본값·명령·폴더·Curator 등은 버전 확인 필요. |
| PydanticAI | Core `v2.61.0` | `pydantic-ai-harness`는 별도 제품·버전. Core와 같은 번호라고 추정하지 않는다. |
| OpenAI Agents SDK | Python `v0.24.0` | Python 분석을 다른 언어 SDK의 동작으로 일반화하지 않는다. |
| Google ADK | Python `v2.13.0` | 이전 실행 경로와 새로운 Graph Workflow의 차이를 섞지 않는다. |
| Microsoft Agent Framework | Python `python-1.24.0` | .NET/Go에 기능·구현이 동일하다고 주장하지 않는다. 실험 기능을 구분한다. |
| Claude Code | CLI `v2.1.314` | 핵심 내부 전체 소스가 공개된 것으로 설명하지 않는다. |
| Claude Agent SDK | Python `v0.2.176`, 번들 CLI `v2.1.316` | Claude Code 단독 조사 버전과 다르다. 초기 자료의 SDK `v0.2.174`와 혼합하지 않는다. |

근거: 각 2차 심층 문서의 조사 범위·버전·출처, [CMP] Appendix A. 이는 **로컬 조사 기준**이며 2026-11-02의 최신 버전이나 현재 설치 버전이라는 뜻이 아니다. [CMP] Appendix B가 가리키는 일부 1차 파일명은 실제 파일명과 다르므로 위 실제 경로 목록을 사용한다.

## 4. 2차 세미나 권장 발표 흐름

### 4.1 스토리라인과 구성 단위

**이미 아는 구성요소의 위치 확인 → 완성형 Harness의 실제 작동(Hermes) → 다른 Harness의 선택(Claude Code) → 직접 개발하는 SDK의 실제 계약(PydanticAI) → 다른 SDK·Framework의 차별적 책임 배분 → 도메인 개발·운영 판단**으로 연결한다.

아래 B01–B24는 **내용 묶음의 식별자**이며 최종 슬라이드 번호나 확정 장수가 아니다. 하나의 묶음을 몇 장으로 나눌지, 발표 시간, 화면별 정확한 문구와 시각 배치는 다음 GPT가 결정한다. 모든 묶음의 기본 상태는 `기존 자료 확인됨`이며, 보강 항목은 §6의 조사 요청과 연결한다.

### 4.2 도입

**B01. 1차에서 3차로 이어지는 위치**

- 메시지: 이번에는 실제 기술의 실행 구조와 개발 책임을 이해하여 다음 세미나의 도메인 Agent 제작에 사용할 판단 기준을 얻는다.
- 필수 설명: 1차 기초는 전제로 한다. Model, 추론 서버, SDK, Harness의 책임 위치만 짧게 재배치한다. 일곱 기술을 보여준 뒤 Hermes·PydanticAI를 중심으로 강조한다. SDK/Harness는 엄격히 배타적인 제품 분류가 아니라 이번 설명의 묶음이다.
- 표현: 계층 위치도와 고정 발표 순서. LangChain/LangGraph·서빙 발표와의 경계는 짧게 표시한다.
- 근거: [FLOW] 도입·작성 원칙, [CMP] §§1–3. 보강: 청중·시간 결정. 공통 Agent Loop를 다시 길게 설명하지 않는다.

### 4.3 Hermes: 실행 환경이 이미 제공될 때 무엇을 이해해야 하는가

**B02. 전체 아키텍처와 사용 경로**

- 메시지: Hermes는 모델 호출 라이브러리만이 아니라 반복 실행·도구·기억·세션·채널을 함께 제공하는 Harness다.
- 필수 설명: CLI/TUI 등 입력 채널 → Agent Core → Provider, Tool Registry·MCP·Plugin, Skills, Session/SQLite·FTS5, Memory, 승인·격리, Gateway·Cron의 관계. 채널 기능이 모두 데모에 필요하다는 뜻은 아니다.
- 표현: [H2] §2.1의 구조를 토대로 전체 조직도를 먼저 제시하고 이후 설명의 위치 지도로 계속 재사용한다. 데이터 저장과 실행 호출의 선을 구별한다.
- 근거: [FLOW] Hermes, [H1], [H2] §§1–3. 보강: R02의 버전·설치 구조 확인.

**B03. 한 요청의 실제 반복·도구·종료 분기**

- 메시지: 모델의 Tool 요청 이후에는 실행 엔진의 검증·기록·정책·실행·재호출이 있다.
- 필수 설명: 사용자 입력 기록, Prompt 준비, Provider 형식 변환, 모델 응답 분류, Tool Intent 기록과 실행, 결과 메시지, 다음 호출 또는 최종 저장. Intent 저장 실패를 무시하고 도구부터 실행하지 않는 경로를 설명한다. 정상 종료와 예산·취소·오류·Fallback의 분기를 구분한다. 모든 실패를 동일한 Retry로 설명하지 않는다.
- 표현: 대표 Loop 한 개와 Tool Round 확대도. 대표 함수·파일을 노트에 연결하고, 정상·실패 분기를 색상만이 아닌 레이블로 구분한다.
- 근거: [H2] §§3–4, 11–14, 17; [CMP] §§4–6. 보강: R02, R09. Tool Pool 예시는 단순 `ThreadPoolExecutor` 의사코드와 실제 실행기를 구분한다.

**B04. 모델이 보는 입력과 캐시·압축**

- 메시지: 저장된 데이터 전체와 지금 모델에 보내는 입력은 같지 않다. 안정적인 Prefix 재사용과 오래된 정보 갱신은 서로 다른 설계 문제다.
- 필수 설명: Stable/Context/Volatile의 논리적 계층과 세션 Prompt Snapshot. 매 호출마다 모든 지침을 새로 읽는 것으로 설명하지 않는다. Cache는 동일 Prefix의 계산 재사용이며 입력을 안 보내도 된다는 뜻이 아니다. Compaction은 문맥 길이·일관성 관리이고 Cache와 별개다. 요약할 때 Tool Call/Return 쌍과 최근 근거를 어떻게 유지하는지 다룬다.
- 표현: 실제 Demo 1의 요청을 지침·메모리·Skill 목록·History·Tools로 나눈 화면과 앞뒤 비교. “8천 토큰 재사용” 등 수치는 설명용일 경우 명확히 표시한다.
- 근거: [FLOW] Hermes Prompt/Cache/Compressor, [H2] §§5–8, [HC]. 보강: R02, R08. 압축 임계값·vLLM 캐시 기본값·성능 향상을 미검증 사실로 확정하지 않는다.

**B05. Memory·FTS·Skills와 세션 관리**

- 메시지: 짧은 기억, 과거 대화의 검색, 절차 재사용은 저장·주입·갱신 시점이 다르다.
- 필수 설명: Memory 파일의 세션 Snapshot, SQLite 대화 이력과 FTS5 검색, 필요 시 읽는 Skills 본문·참고 자료, Skill 생성과 품질 검증의 구별. FTS는 어휘 검색이며 벡터가 아니라는 이유로 RAG 전체와 대립시키지 않는다. Profiles/세션 재개/Prompt 갱신 관련 명령을 구조와 연결한다. External Memory Provider는 발표자의 범위 선택에 따라 깊게 다루지 않는다.
- 표현: “무엇을 저장 / 언제 읽음 / 무엇이 다음 요청에 반영됨” 표. 동일 Lot라도 SOP 버전이 바뀌면 이전 Snapshot을 그대로 써도 되는지 질문한다.
- 근거: [H2] §§8–10, 15–16, [HC], [FLOW] Memory·Skills. 보강: R02. Curator와 명령의 정확한 지원 범위는 확인 후 포함한다.

**B06. 확장·Subagent·실행 권한**

- 메시지: Tool·MCP·Plugin은 확장 경계가 다르고, 독립 대화의 Subagent도 자동으로 OS·파일·테넌트 격리가 되지는 않는다.
- 필수 설명: 등록된 함수·특수 처리 도구·MCP 연결·Plugin 확장점의 차이, 부모가 자식 결과를 받아 다시 판단하는 흐름, 도구 범위·반복 예산·공유 자원. 병렬 Tool, Subagent, Gateway 동시 요청을 분리한다. Cron은 새 Agent 작업을 기동하고 결과를 전달하는 경로이며 현재 대화의 Loop 반복과 다르다. 승인·위험 작업 검사와 실제 백엔드 권한의 경계를 다룬다. File checkpoint는 모든 외부 변경을 되돌리는 장치가 아니다.
- 표현: 부모/자식 호출·결과 반환도, 컨텍스트와 파일 자원의 공유 범위, 정책이 개입하는 Tool 경로.
- 근거: [H2] §§11–16, [CMP] §§7–8, 16–19. 보강: R02, R09. 도구 직접 추가는 항상 Core 수정이라는 단정을 피한다.

**B07. Demo 1: 관찰한 실행을 다시 읽기**

- 메시지: B02–B06에서 설명한 부품이 실제 BIN 분석 요청에서 어떤 데이터를 주고받았는지 확인한다.
- 필수 설명: 실제 실행의 모델 요청·응답·Tool·분기·상태 변화를 구분한다. Space는 실제 기록을 단계별로 읽는 조작으로 우선 설계한다. 라이브 Agent를 강제로 단계 정지시키는 설계는 별도 검토한다.
- 표현: 별도 Demo 1 웹페이지로 이동하여 실제 Trace 재생, 슬라이드로 복귀. 상세 요구는 §7.2.
- 근거: [FLOW] 공통 데모·Hermes 데모, [HC], [PC]의 관찰 원칙. 보강: R08–R10.

### 4.4 Claude Code: 다른 완성형 Harness의 선택

**B08. 전체 구조 → 작업 루프·지침·명령 비교**

- 메시지: Claude Code는 코딩 작업 환경과 실행 계약을 제공한다. Hermes와 같은 큰 묶음에서도 컨텍스트·권한·기억의 계약은 다르다.
- 필수 설명: CLI Harness, Gather–Act–Verify의 논리적 흐름, 파일·Shell·검증 도구, Project Instructions·Auto Memory·Skills·세션의 관계. `CLAUDE.md`와 `AGENTS.md` fallback/import 조건을 구분한다. `/context`의 입력 상태 관찰, `/compact`의 문맥 관리, `claude -c`·`--resume`·`/resume`의 재개를 명령 후보로 삼아 원리와 연결한다. 정확한 구문·가용성은 R07로 확인한다. 프로젝트에 코딩 도구를 제공받는 장점과 런타임 내부 변경의 제약을 설명한다.
- 표현: 전체 구조 후 Hermes와 “설정·현재 입력·장기 절차·권한” 비교. 내부 비공개 엔진은 공개 계약 영역과 시각적으로 경계를 둔다.
- 근거: [C1], [C2]의 Context·Memory·Permissions·Sessions, [CC], [CMP] §28. 보강: R07. 공개 문서상의 동작을 비공개 내부 함수의 소스 증명처럼 표현하지 않는다.

**B09. Subagent와 Agent Teams, 권한의 실제 범위**

- 메시지: 자식에게 맡겨 결과를 받는 구조와 독립 세션들이 협업하는 구조는 제어·상태·비용이 다르다.
- 필수 설명: Subagent의 별도 컨텍스트와 부모 반환, Agent Teams의 독립 세션·공유 작업·직접 메시지. Teams는 [FLOW]가 중요하게 다루길 요청했으므로 본문 비교에 포함하되 실험 기능·활성화·제약을 구분한다. Read 도구 Hook만으로 모든 파일 유입 경로가 통제되지 않는다는 권한 범위 예시를 선별한다.
- 표현: 같은 역할 분담의 부모-자식도와 팀 통신도를 나란히 비교한다. 병렬 처리량 우수성은 실측 없이 주장하지 않는다.
- 근거: [FLOW] Claude Code, [C2] Subagents·Agent Teams·Hooks·Permissions. 보강: R07.

### 4.5 PydanticAI: 개발자가 만드는 Agent의 계약과 내부 실행

**B10. Pydantic → Core → 선택적 Harness 전체 구조**

- 메시지: Pydantic은 데이터 계약을 다루는 기반이며 PydanticAI는 실행·모델·도구·출력 계약을 묶는다. Core와 별도 Harness는 구분해야 한다.
- 필수 설명: Agent 설정, Model/Provider/Profile, 내부 Graph, Tools/Toolsets, 출력 검증, Deps, Capabilities, History와 관찰 경로. 독립 `pydantic_graph`와 내부 Agent Graph, 별도 Harness, Logfire/Evals의 위치를 나눈다. PydanticAI 내부 Graph를 LangGraph라고 부르지 않는다.
- 표현: 제품 관계를 짧게 보여준 뒤 Core 전체 아키텍처, 바깥에 선택적 Harness와 관찰·평가 영역 배치.
- 근거: [FLOW] PydanticAI, [P2] §§1–8, 18–22. 보강: R01, R05.

**B11. 실행 API와 Graph의 실제 분기**

- 메시지: Agent 정의와 개별 Run의 상태는 다르고, 실행 API는 결과를 관찰·제어하는 방식이 다르다.
- 필수 설명: `run_sync`, `run`, `run_stream`, `run_stream_events`, `iter`의 용도와 수명. `UserPromptNode → ModelRequestNode → CallToolsNode → 다음 모델 요청/종료`의 대표 경로에서 메시지 준비·출력/Tool 분류·Retry·Deferred를 설명한다. Run/Step/Session이라는 일반 용어를 자동 영속화 기능으로 오해하지 않게 한다.
- 표현: 동일 요청을 실행 API별 “받는 것/제어하는 것/닫아야 하는 것”으로 비교하고 Graph를 단계 강조한다. 핵심 상태와 실제 타입 이름은 최종 버전 확인 후 노트에 배치한다.
- 근거: [P2] §§4–6, 10–13, [FLOW] 실행 API·내부 Graph. 보강: R01, R03.

**B12. Instructions·Deps·Toolsets에서 실제 모델 요청까지**

- 메시지: Python 실행에 전달한 정보가 모두 LLM에게 자동 노출되지는 않는다. 도구 노출과 실행 권한도 별개다.
- 필수 설명: instructions/system prompt/dynamic instructions의 역할, Deps/RunContext의 실행 시 접근, `tool`과 `tool_plain`, 함수 도구의 Schema, Provider-hosted/native 도구와의 차이, Toolsets의 필터·결합·Prefix와 수명. 모델에 보인 Tool Schema → 선택된 Call → 인자 검증 → 정책·Hook → 실행 → 결과 메시지를 연결한다.
- 표현: 같은 사용자 요청에 대한 Python Deps·History·최종 Provider 요청을 나란히 보여준다. 사용자별 허용 Lot은 서버 권한 확인으로 강제해야 하며 Prompt에 쓰는 것만으로 해결되지 않는다.
- 근거: [P2] §§7–10, 14–15, 19, [FLOW] instructions·ToolManager·toolsets. 보강: R01, R03, R05.

**B13. 출력 계약·Retry·EndStrategy·병렬 실행**

- 메시지: 타입을 만족한 결과, 사실적으로 맞는 결과, 부작용이 안전하게 완료된 상태는 다르다.
- 필수 설명: ToolOutput은 최종 출력용 도구의 인자를 검증하는 방식이며 일반 텍스트를 임의로 도구로 바꾸는 것이 아니다. NativeOutput은 모델/Provider 지원, PromptedOutput은 파싱·검증 조건, TextOutput은 텍스트 처리 계약과 연결한다. 최종 `output_type`과 개별 Tool 반환 타입을 분리한다. `ModelRetry`, 출력 검증, 네트워크 재시도, 실행 예산을 구분한다. 자료 기준 기본 `graceful`과 `early/graceful/exhaustive`가 최종 출력·다른 Tool이 같은 응답에 섞일 때 만드는 차이, 병렬 Barrier와 이미 시작한 작업을 설명한다.
- 표현: 한 모델 응답에 출력 후보+도구 호출이 있는 경우의 세 전략 분기표와 실제 Trace 비교. 출력 타입을 통과한 잘못된 근거 사례를 설명용으로 추가할 수 있다.
- 근거: [P2] §§10–13, [PC], [FLOW] Output·Retry·EndStrategy·Q&A. 보강: R01, R04. 전략 차이를 확실히 재현할 입력·실제 호출 순서는 구현 검증 전 확정하지 않는다.

**B14. Hooks·Capabilities·History·Memory·Compaction**

- 메시지: Core가 제공하는 개입·합성 지점과 애플리케이션의 정책·저장 책임을 구분하면 “전부 직접 구현”도 “전부 기본 제공”도 피할 수 있다.
- 필수 설명: before/wrap/after 등 Hook 위치, Capability의 지침·도구·Hook 묶음과 활성화·합성 순서, 실행 간 History를 명시적으로 전달하거나 저장하는 경로. Session metadata와 대화 이력, 장기 Memory는 같은 것이 아니다. 압축의 입력 변환과 저장 이력에 대한 영향을 구분한다. 선택적 Harness의 Memory·Skills·Planning·Shell·Sandbox·Subagents·Guardrails가 어디까지 제공되는지 설명한다.
- 표현: “Core 제공 / Harness 추가 / 개발자가 정할 정책·저장소” 책임표. Lot 분석의 오래된 요약을 새 데이터처럼 사용하는 실패와 갱신 위치를 예로 든다.
- 근거: [P2] §§14–19, 21–22, [FLOW] Hooks·Capabilities·Memory·Harness. 보강: R03, R05. 예시 Capability 생성자가 실제 API라는 가정은 금지한다.

**B15. Orchestration·승인·평가와 Demo 2**

- 메시지: Agent 호출을 도구로 감싸는 것, 답변 책임을 넘기는 것, 코드·Graph로 순서를 통제하는 것은 다른 선택이다.
- 필수 설명: Tool 내부 위임, 프로그램 라우팅, 명시적 Graph, Harness의 Subagents/Advisor를 제어권 기준으로 비교한다. Deferred 승인 요청→외부 결정→재개는 승인자·인자·데이터 버전과 결합한다. Logfire/OTel 관찰과 Pydantic Evals의 Case·Evaluator는 실행 성공과 분석 품질을 별도로 평가하는 도구로 설명한다.
- 표현: 부모에게 결과 반환 / 다음 담당자가 답변 / 정해진 Graph의 세 구조, 승인 대기·재개 상태도. 별도 Demo 2 페이지에서 Core 실행을 먼저 관찰하고 가능한 Harness 확장으로 연결한다.
- 근거: [P2] §§16, 20–24, [P1] §25의 관찰·Evals, [PC], [FLOW] orchestration·approval·데모. 보강: R04–R06, R09–R10. 세부 데모는 §7.3.

PydanticAI의 활용 가치는 “타입 검증을 더 잘한다”에서 끝내지 않는다. **도구 검증과 재시도 경로를 분리하여 오류를 어디로 돌려보낼지 설계하고, 실행 Node와 메시지를 관찰하며, EndStrategy·Barrier로 완료와 부작용의 관계를 정하고, Hook/Capability에 반복되는 정책을 모을 수 있다는 구조적 선택지**를 설명한다. Deps로 실행 자원과 사용자 맥락을 주입하고 History·승인을 애플리케이션 저장·권한과 결합하는 책임도 함께 보인다. 이로써 활용 이점과 개발 비용을 동시에 판단하게 한다. 근거: [P2] §§4–18, 20–24. 구체 API·합성 계약은 R01–R05 확인 대상이다.

### 4.6 나머지 네 기술: PydanticAI와 비교할 실제 차이

**B16. OpenAI Agents SDK: 전체 구조 → 명시적 Runner와 제어권**

- 메시지: Runner의 다음 단계 판정과 Agent-as-Tool/Handoff의 구분으로 실행 소유권이 비교적 직접 드러난다.
- 필수 설명: 전체 Agent/Runner/Model/Tools/Session/RunState/Tracing 구조를 먼저 제시한다. 응답 처리 후 Final·RunAgain·Handoff·Interruption의 분기, Tool 결과로 후속 모델 호출 없이 종료하는 설정, 매니저에게 돌아오는 as-tool과 활성 Agent가 바뀌는 Handoff를 비교한다. PydanticAI의 이름이 다른 패턴과 API를 억지로 일대일 대응시키지 않는다.
- 표현: 전체 구조 후 두 가지 제어 흐름과 실제 NextStep 분기. 도메인 전문가에게 분석만 요청할지 이후 사용자 질의까지 맡길지 예를 든다.
- 근거: [O2] Runner·Turn Resolution·Tools·Handoffs, [OC], [CMP] §§4–8, 25. 보강: R06.

**B17. OpenAI의 Guardrail·승인·History·Stream 경계**

- 메시지: “Guardrail 있음”, “세션 저장”, “스트리밍 완료”만으로 실행 안전성과 복구를 판단할 수 없다.
- 필수 설명: 입력 Guardrail의 병행 실행 조건, Function Tool Guardrail과 다른 도구 유형의 범위, RunState 승인·재개와 Session History의 차이. nested Agent-as-Tool 승인은 최상위 상태·시작 Agent와 연결되는 경로를 설명한다. 마지막 토큰/루프 중단/명시적 취소가 같은 사건이 아님을 필요한 만큼만 다룬다.
- 표현: 검사와 도구 실행의 시간축, 승인된 RunState와 저장 대화의 두 저장물. 유사 개념을 PydanticAI와 짧게 대조한다.
- 근거: [O2] Guardrails·RunState·nested approval·Session·Streaming, [CMP] §§16–18, 22. 보강: R06. Guardrail의 선행 차단을 모든 설정에 보장하지 않는다.

**B18. Claude Agent SDK: 전체 구조 → 공개 Python과 CLI의 경계**

- 메시지: Python에서 코딩 Harness를 재사용하되, 실행 루프 전체를 Python 애플리케이션이 소유하는 구조와 다르다.
- 필수 설명: `query`/`ClaudeSDKClient` → Transport/CLI Process → Claude Code Runtime → Model/Tools의 전체도. 단발 호출과 연결 수명, 메시지·Control Protocol, SDK MCP 도구의 CLI↔Python 왕복 경로. `allowed_tools`의 자동 승인과 도구 카탈로그 제한을 혼동하지 않는다. `can_use_tool`이 모든 호출에서 반드시 실행되는 단일 권한 게이트라고 가정하지 않는다.
- 표현: 프로세스 경계 시퀀스와 공개/비공개 영역. 동일한 Python 함수도 일반 SDK 호출과 SDK MCP 경유일 때 어떤 수명·권한 경계를 지나는지 비교한다.
- 근거: [S2] API·Transport·Query·Permissions·SDK MCP, [SC], [CMP] §29. 보강: R07. CLI의 최종 모델 요청 전체가 공개 Python 객체로 관찰된다고 주장하지 않는다.

**B19. Claude SDK의 상태 이관과 재현성**

- 메시지: 대화 복원과 작업 환경 복원은 별개의 준비다.
- 필수 설명: CLI 로컬 Session, 외부 Session Store 미러·재개 경로, 파일·도구 의존성·산출물의 독립 수명. `enable_file_checkpointing`과 외부 Store 조합 제약을 확인하여, 이력만 옮기면 다른 PC에서도 같은 분석이 재현된다는 오해를 막는다.
- 표현: transcript, workspace, artifact, credential을 분리한 이관 체크 그림.
- 근거: [S2] Session Resume·External Store·File Checkpoint, [SC]. 보강: R07. 세 번째 실행 데모를 추가하지 않는다.

**B20. Google ADK: 전체 구조 → Event와 최종 완료의 범위**

- 메시지: Agent의 이벤트와 업무 전체의 완료를 구분하는 구조가 다단계 분석과 연결된다.
- 필수 설명: Runner·Agent/LlmFlow·Tool Callback·SessionService·MemoryService·ArtifactService·Workflow 전체도. v2.13 기준 LlmAgent 실행 경로와 BaseLlmFlow의 반복, 이벤트 append와 state delta, partial/final의 범위를 설명한다. 특정 Agent의 final Event가 전체 보고서 완료를 뜻하지 않는다. `temp:` 상태와 영속 상태를 구분한다.
- 표현: Agent별 이벤트 시간축과 Session/Event·Artifact 저장 분리. 최종 보고서에는 데이터 Snapshot·분석 결과 Artifact ID를 결합하는 도메인 예시.
- 근거: [G2] Runner·LlmAgent·BaseLlmFlow·Events·Sessions·Artifacts, [GC], [CMP] §26. 보강: R06.

**B21. ADK Workflow·병렬·복구의 경계**

- 메시지: Callback·Task·Graph·Checkpoint 각각이 통제하는 범위를 봐야 한다.
- 필수 설명: 도구 batch 병렬과 취소·부분 성공, 기존 Workflow Agent와 Graph Workflow의 차이, deprecated 경로와 새 경로의 관계. Checkpoint 존재만으로 모든 실행 위치에서 완전한 재개가 된다고 주장하지 않는다. 조사 소스의 resume TODO 등 한계를 함께 인계한다.
- 표현: Event 기반 경로와 Graph Scheduler 경로를 분리한 축약도. 자세한 API는 노트/부록 후보로 둔다.
- 근거: [G2] Tool Batch·Graph Workflow·Checkpoint, [CMP] §§7, 9, 18. 보강: R06.

**B22. Microsoft Agent Framework: 전체 구조 → 정책 위치·Superstep**

- 메시지: Agent/Chat/Function Middleware, 모델-도구 반복, 상위 Harness와 Workflow는 개입 단위가 다르다.
- 필수 설명: Agent/RawAgent → Context/History → ChatClient/Function Invocation → Tool의 전체 경로, 별도 Harness 반복과 Workflow. 도구 인자 변환 후 최종 실행 인자를 다시 승인·검사해야 하는 이유. MiddlewareFailure와 제어된 종료, 일반 Tool 예외의 차이를 선별한다. Workflow Superstep의 내부 commit을 외부 DB의 원자적 트랜잭션과 동일시하지 않는다.
- 표현: 정책이 위치한 세 Middleware 층, 두 입력 결과를 Lot·날짜·Revision 키로 결합하는 Workflow. 다른 Source의 도착 순서에 의존하지 않는 설계 시사점을 연결한다.
- 근거: [M2] Agent Pipeline·Middleware·Approval·Harness·Workflow/Superstep·Checkpoint, [MC], [CMP] §27. 보강: R06. Functional Workflow·FIDES 등은 실험 상태를 구분하고 주제와 무관하면 부록으로 내린다.

### 4.7 종합과 도메인 적용

**B23. 도메인 Agent를 만들 때 남는 개발 책임**

- 메시지: 각 기술에서 이미 제공되는 실행 메커니즘을 활용하되, 데이터·정책·부작용·품질의 계약은 별도로 설계한다.
- 필수 설명: 한 장의 비교 축은 Loop 소유자 / 모델 입력 구성 / Tool 정책 지점 / 상태·재개 / 위임의 제어권 / 개발자 구현 범위로 제한한다. 타이핑·Guardrail·Checkpoint·Subagent가 각각 보장하지 않는 것을 같은 말로 섞지 않는다. 제품 우승표나 미실측 성능 순위는 만들지 않는다.
- 표현: 일곱 기술 책임표와 “BIN 오류율 조회→근거 분석→다른 데이터 기반 예측”의 단계별 설계 질문. 어떤 시점의 데이터인지, 승인 대상은 무엇인지, 재실행할 수 있는 읽기와 중복 위험 쓰기를 어떻게 구분할지 묻는다.
- 근거: [CMP] §§23–36, 39, [COMMENTS]. 보강: R10–R11. 모든 실패 사례를 본문에 넣기보다 대표 사례를 선정한다.

**B24. 운영 형태의 선택과 3차 연결**

- 메시지: Agent 실행 위치와 LLM 서빙 위치를 분리해서 선택할 수 있으며, 선택마다 상태·권한·배포 책임이 달라진다.
- 필수 설명: ① 중앙 Agent 서버+요청 전용 클라이언트, ② 사용자 PC Agent+중앙 LLM, ③ 필요한 경우 혼합 구조. 중앙형의 Session 소유권·작업 큐·동시성·취소·감사와 로컬형의 설치·업데이트·자격증명·파일 접근·Trace 수집을 비교한다. Runtime worker 수와 모델 서버 GPU 자원은 별개로 계산한다. 실제 용량 수치는 측정 전 제시하지 않는다.
- 표현: 두 배치도와 결정 질문. “다음에는 우리 데이터·권한·운영 조건으로 최소 Agent를 만든다”로 3차와 연결한다.
- 근거: [FLOW] 작성 원칙의 마지막 운영 제안, [H2] Gateway, [P2] Serving, [CMP] §§19–22, 32–36, [HC]. 보강: R11. 시간이 부족하면 상세 배포안은 부록으로 이동하되 핵심 선택 질문은 유지한다.

## 5. 이미 조사됐지만 추가 반영할 내용

다음은 새로 외부 조사한 내용이 아니라 **흐름 문서의 빈 부분·질문을 기존 완료 자료로 메울 수 있는 항목**이다. 기술별 후반부가 “추후 정리”라고 되어 있어도 해당 주제의 심층 조사가 없는 것은 아니다.

| 내용과 실질적 보강 | 포함 이유·삽입 위치 | 근거·남은 확인 |
|---|---|---|
| Hermes는 Tool Intent의 영속화와 실행을 구별한다. 저장 실패를 실행 후 경고로만 처리하는 그림을 피한다. | 단순 Loop 설명을 실제 런타임의 실패 경계로 구체화. B03. | [H2] §§3–4, [CMP] §4. 실행 버전 추적은 R02. |
| Hermes의 도구 병렬 실행은 세그먼트·장벽·컨텍스트·권한 조건과 연결된다. 자식 Agent와 Gateway 동시성은 다른 층이다. | “비동기니까 동시에 안전”을 피하고 데이터 의존성·공유 상태를 보게 한다. B06. | [H2] §§13–15, [CMP] §7. |
| 세션 시작 시 Memory Snapshot과 FTS 검색은 다른 갱신 경로다. Skill 생성도 절차 품질의 보증은 아니다. | SOP 개정·장비 코드·과거 분석 근거의 신선도와 연결. B04–B05. | [H2] §§8–10, [HC]. Curator 상세는 R02. |
| PydanticAI의 내부 Graph는 LangGraph가 아니며 사용자 정의 `pydantic_graph`와도 층이 다르다. | 흐름 문서의 질문을 이미 있는 조사로 해소. B10–B11. | [P2] §§4–6, 20, [CMP] §9. 실제 내부 타입은 R01. |
| Core/별도 Harness/애플리케이션 정책을 분리하면 Memory·Skills·Compaction을 전부 수작업으로 만든다는 결론을 피할 수 있다. | 제공 기능과 개발자 설계를 정확히 비교. B14–B15. | [P2] §§15–20. 설치 조합·지원 범위는 R05. |
| Deps는 실행 시 Python 데이터이고, 도구 노출 필터와 권한 검증은 별개다. | 다중 사용자에서 허용 Lot·사용자 식별자를 Prompt에 넣는 것만으로 통제했다고 오해하지 않게 한다. B12. | [P2] §§9–10, 14, 22. |
| EndStrategy와 Barrier는 최종 답변의 모양뿐 아니라 이미 시작된 도구·외부 부작용과 연결된다. | PydanticAI의 구체적 차별점과 깊은 실무 의미. B13, Demo 2. | [P2] §§11–13, [PC]. 정확한 재현 조건은 R04. |
| Deferred 승인은 단순히 사람이 오래 기다리는 기능이 아니라 요청 ID·원래 인자·승인자·데이터 버전과 연결된 재개 계약이다. | 잘못된 리포트·변경된 인자에 대한 승인 재사용 방지. B15/B17/B22. | [P2] §16, [O2] RunState, [M2] Approval, [PC], [CMP] §17. |
| OpenAI의 NextStep·Tool 결과 직접 종료·as-tool/Handoff·nested 승인 상태가 이미 조사되어 있다. | 흐름 문서가 미완성인 OpenAI 파트를 특징 중심으로 보강. B16–B17. | [O2], [OC]. 최신 동작 확인만 R06. |
| Claude Code의 AGENTS fallback, 권한·Hook의 적용 범위, Teams와 Subagent의 차이가 정리되어 있다. | “같은 Harness” 이상의 비교점 확보. Teams는 발표자 명시 관심사. B08–B09. | [C2], [CC]. 버전별 활성화·정확한 구문은 R07. |
| Claude SDK의 공개 영역은 Python API·Transport·Control·SDK MCP까지이며, 세션 이동과 작업 파일 복원은 다르다. | 다른 SDK와 제어권의 차이, 향후 데모 이관 시 사고 방식 제공. B18–B19. | [S2], [SC]. |
| ADK final Event의 범위, Session/Artifact 분리, Graph의 복구 한계가 조사되어 있다. | 분석 한 단계 완료와 업무 전체 완료를 구분. B20–B21. | [G2], [GC]. 구형 경로·과도한 durable 표현은 §8. |
| MAF의 Middleware 위치, 승인 후 인자 변경, Superstep과 Join 순서가 조사되어 있다. | 정책의 실제 강제 위치와 데이터 결합 정확성 설명. B22. | [M2], [MC]. |
| 실행 상태·대화·Checkpoint·Artifact·외부 부작용은 서로 다르며 Resume는 Exactly-once를 자동 보장하지 않는다. | 단순한 “저장/복구 지원” 비교를 운영 계약 비교로 바꾼다. B17/B19/B21–B24. | [CMP] §§18–22, 각 심층 문서. |
| 캐시 효율과 데이터 신선도, 로그 관찰과 분석 품질 평가를 분리한다. | “응답이 빨랐다/타입이 맞았다”를 도메인 정답으로 오인하지 않게 한다. B04/B15/B23. | [HC], [CC], [P1] §25 Evals, [CMP] §§11, 22. |

### 5.1 통합·축소·제외 후보

- **통합:** 공통 비교 축은 B23에서 한 번 회수한다. 각 기술에서는 해당 기술의 차이를 설명하는 데 필요한 축만 꺼낸다. 동일한 보안 일반론과 Memory 정의를 일곱 번 반복하지 않는다.
- **부록 후보:** 모든 함수 추적 워크북, 전체 API 목록, 24개 실패 사례 전부, 모든 Hook 이름, 모든 실험 기능·지원 채널, 큰 설정 파일 전문. 후속 GPT가 발표 시간에 따라 선별한다.
- **제외 후보:** 제품 홍보성 우열, 출처 없는 성능·정확도 순위, 다른 발표자의 LLM 엔진 상세, 도메인 근거 없는 자동 제어/공정 변경 시연, 1차 기초 강의 반복.
- **범위 유지:** External Memory Provider를 실제로 활용할 수 없다는 기술적 결론을 만들지 않는다. [FLOW]가 깊게 다루지 않겠다는 선택을 따른다. 캐시 속도 측정은 선택 실험이며 데모 성공의 필수 조건으로 만들지 않는다.

## 6. 추가 조사 요청사항

### 6.1 다른 조사 AI에게 전달할 공통 요청

> 아래 R01–R11을 우선순위에 따라 조사하라. 기존 로컬 분석은 조사 기준 버전의 정적 분석으로 존중하되, 미검증 API·새로운 구상·실행 요구를 사실로 바꾸지 말라. 공식 문서, 고정 릴리스 소스, 릴리스 노트를 우선 사용하고 **제품/언어/패키지/버전/파일·함수/URL/확인일**을 남겨라. 답변은 `로컬 자료와 일치 / 수정 필요 / 확인 불가 / 실행 검증 필요`로 구분하라. 개념도·의사코드·실행 가능한 코드를 명확히 표시하라. 출처가 없는 내부 동작은 추정하지 말라. 다음 질문의 답을 얻더라도 실제 성능·대상 PC 호환 성공은 실행 검증 전 확정하지 말라.

우선순위: **P0**=블루프린트/데모 범위를 결정하기 전에 필요, **P1**=주요 비교·설명 보강, **P2**=선택 실험·부록. 아래 질문은 이번 단계에서 외부 조사하지 않았다.

### R01. 버전 고정과 PydanticAI 코드·타입 감사 — P0

- 필요성: [FLOW]에는 이해용 코드, 철자 오류, 출처 없는 줄 번호, 확인이 필요한 타입명이 섞여 있다. 문법이 틀린 예제가 발표·구현에 전파되면 안 된다.
- 구체 질문: Core `v2.61.0`에서 다섯 실행 API의 정확한 반환 타입·호출·종료 방식은? `InstructionPart`, Graph 상태 필드, Capability 구성 예시가 실제 API인가? `ToolOutput/NativeOutput/PromptedOutput/TextOutput`의 정확한 import·지원 조건·validator 경로는? `output_type`은 최종 Run 결과의 계약인가, Tool별 반환 타입과 어떻게 다른가? 여러 최종 출력 형태를 허용하는 경우의 정확한 범위는? `run_steam_evnets`는 오타로 정리하고 임의 API로 남기지 말라.
- 요청 결과: 잘못된 예시→수정 예시→근거 표, 짧은 버전 고정 코드, 내부 타입과 공개 API 구분, [FLOW]의 불명확한 “21.2” 참조의 실제 출처 또는 확인 불가 표시. 패키지 전체 버전 매트릭스도 제시하라.
- 반영: B10–B14, Demo 2. 근거 출발점: [P2], [CMP] Appendix A, [FLOW] 추가 정리 목록.

### R02. Hermes 공개 확장·명령·메모리·관찰 경계 — P0

- 필요성: Hermes 기본 흐름을 보존하면서 실제 요청과 상태를 관찰해야 한다. 흐름 문서에 새로 적힌 기능은 고정 심층 자료만으로 확정하기 어렵다.
- 구체 질문: 대상 릴리스의 Windows/기타 OS `HERMES_HOME`·Profile·DB·Memory 경로는? memory 연산이 `add/patch/remove`인지 `add/replace/remove`인지? `hermes sessions refresh-prompts --session SESSION_ID`의 실제 존재·효과·이력 보존 조건은? Curator의 active/stale/archived, idle/주기 조건·설정이 실제 어느 버전에 있는가? Slash/CLI 명령을 어떻게 구분할까? 실제 Provider 요청 직전·Tool·Subagent·저장·압축을 Core 무수정으로 볼 수 있는 Hook/로그/Wrapper는? Registry 직접 도구·Plugin·MCP의 권장 확장 방식은? 압축 50%/85%, 최근 20개, Memory 문자 한도, Shadow Git의 기본값·적용 범위는 해당 버전에서 무엇인가?
- 요청 결과: 버전별 기능/명령 표, 폴더 그림, 최소 침습 관찰 설계와 관찰 불가 영역, 정확한 소스 함수. 기본값과 기획상 조정값을 구분하라.
- 반영: B02–B07, Demo 1. 출발점: [H2], [FLOW] Hermes. 캐시 측정은 R08과 분리한다.

### R03. PydanticAI 실행 수명·입력·History·병렬의 실제 계약 — P0

- 필요성: “개발자는 무엇을 전달하고 무엇을 관리하는가”를 정확히 설명하고 Trace 지점을 선정해야 한다.
- 구체 질문: Instructions/system prompt/dynamic instructions·Deps·History·Tool Schema가 Provider 요청에 반영되는 시점은? Deps가 모델에 노출되는 조건은? `tool`/`tool_plain`, sync/async 함수의 스레드·Task·Barrier·동시성 제어는? Streaming/iter 중단과 자원 정리는? 실행 간 자동 History 재사용/Conversation API/명시적 history 전달은 각각 어떤 조건인가? 저장된 History와 Compaction 적용 입력·저장본은 어떻게 달라지는가? before/wrap/after Hook 합성·예외·취소의 실제 순서는?
- 요청 결과: 1회 Run 시퀀스, 2회 Run의 입력·저장 비교, API별 수명 표, sync/async 실행 표, 비밀정보를 가린 최종 요청 예시와 공개 관찰 지점. 실제 실행이 필요한 부분은 별도 테스트 계획으로 제시하라.
- 반영: B11–B14, Demo 2. 출발점: [P2] §§4–18, [FLOW]의 실행·병렬·Memory 질문.

### R04. EndStrategy·Retry·Deferred 승인 재현 조건 — P0

- 필요성: 같은 입력만 넣으면 세 전략이 반드시 다른 동작을 보인다고 가정할 수 없다. 안전한 읽기와 승인 대상 쓰기도 분리해야 한다.
- 구체 질문: `early/graceful/exhaustive`는 유효 출력 후보와 다른 Tool·Retry가 섞일 때 어떤 순서로 작동하는가? Streaming에서 출력 확정 시점의 예외는? 이미 시작한 Tool·취소·동시 실행은? ModelRetry·출력 Retry·HTTP Retry·UsageLimits는 어떻게 중첩되는가? Deferred 승인·거절·만료·중복 응답의 Run/Call ID·이력 재전달 조건은? UI가 없으면 어떤 상태로 반환하며 누가 재개해야 하는가? 바뀐 인자나 데이터로 재개할 때 재승인 지점은?
- 요청 결과: 조건별 분기표, 실제 LLM 실험과 통제된 런타임 시험의 구분, 최소 재현 테스트 설계, 관찰할 Trace 항목, 승인 UI/API 상태도. 강제로 만든 모델 응답을 실제 모델의 자율 선택처럼 표시하지 말라.
- 반영: B13/B15, Demo 2. 출발점: [P2] §§11–13, 16, [PC].

### R05. 별도 Harness와 Capabilities·Skills·MCP의 제공 범위 — P0

- 필요성: Core와 Harness를 혼합하면 과장된 기본 기능이나 불필요한 전면 자체 구현을 제안하게 된다.
- 구체 질문: 재현 가능한 Core/Harness/Graph 버전·Python 요구사항·설치 extras 조합은? Memory·Compaction·Skills·Planning·Shell·Sandbox·Subagents·Advisor·Guardrails 각각의 실제 기본 제공 경로와 개발자 구현 책임은? Capability 활성화·합성 순서·중복 도구·Schema Cache 갱신·실패 전파는? `load_capability` 및 MCP 연결의 실제 API·수명은? Harness 없이 Core만으로 가능한 최소 관찰 데모와 선택적 확장 데모를 어떻게 나눌까?
- 요청 결과: 제공 범위 책임표, 고정 패키지 조합, 모듈 구조도, 최소 확장 예제와 미지원/실험 표시. “전부 수동” 또는 “전부 자동” 결론을 피하라.
- 반영: B10/B12/B14–B15, Demo 2 확장. 출발점: [P2] §§15–20, [FLOW] Harness 질문.

### R06. 다른 Framework의 핵심 비교 사실 감사 — P1

- 필요성: [FLOW]에서 아직 작성되지 않은 비교 부분을 기존 완료 연구로 채우되 과도한 요약을 바로잡아야 한다.
- 구체 질문: OpenAI Python `v0.24.0`의 NextStep·Tool 직접 종료·입력 Guardrail 병행·nested 승인/RunState 경로는? ADK `v2.13.0`의 새 LlmAgent 경로, Event final 범위, temp 상태, 구형 ParallelAgent와 Graph 관계, checkpoint resume TODO의 구체 범위는? MAF `python-1.24.0`의 Middleware 실패 처리·최종 인자 승인·상위 Harness·Superstep commit·다중 Source 순서·실험 Functional/FIDES의 범위는? 이후 버전을 사용할 경우 어떤 설명을 바꿔야 하는가?
- 요청 결과: 기술별 “PydanticAI와 비교할 차이 3개 / 개발자 책임 / 근거 / 한계” 표, 실제 실행·저장 경로 1개씩, 수정 사항만 별도 목록. 성능 순위를 만들지 말라.
- 반영: B16–B17/B20–B22. 출발점: [O2], [G2], [M2], [CMP].

### R07. Claude Code·SDK의 공개 계약과 Teams — P1

- 필요성: 버전별 사용 계약과 비공개 런타임 구현을 구별해야 한다. Teams는 발표자의 명시 관심사다.
- 구체 질문: `CLAUDE.md`/`AGENTS.md` fallback과 import의 조건, Auto Memory 한도·공유 범위, 세션 재개·컨텍스트 관련 명령은? Agent Teams의 실험 상태·활성화·작업 공유·통신·제약과 Subagent 차이는? `allowed_tools`·`can_use_tool`·Hooks의 실제 적용/우회 경로는? SDK Python/번들 CLI 버전 조합에서 Session Store와 File Checkpoint의 조합 제약은? 모델 요청 전체를 공개 API로 관찰할 수 있는 범위는 어디까지인가?
- 요청 결과: 버전·명령 표, 팀/자식 비교도, 공개 계약과 비공개 구현 경계, SDK↔CLI↔MCP 시퀀스. 내부 스케줄러·스레드 방식을 추정하지 말라.
- 반영: B08–B09/B18–B19. 출발점: [C2], [S2]. 두 데모에 Claude를 추가할 필요는 없다.

### R08. 외부 API → 대상 PC vLLM의 기능 호환 — P0, 캐시 실험은 P2

- 필요성: base URL과 모델명만 바꾸면 모든 기능이 그대로 된다고 보장할 수 없다.
- 구체 질문: 현재 PC·대상 PC의 실제 OS/Python, Hermes 설치 방식·버전, vLLM 버전·endpoint·인증·served model ID·context limit·tool parser·chat template·지원 API는? Tool calling/다중 Tool/stream/structured output/schema 제약/사용량 통계/취소의 지원은? PydanticAI Provider·Profile과 Hermes Provider 설정은 어떻게 달라지는가? [FLOW]의 “qwen 3.8 수준”이 가리키는 정확한 구현 지원 모델은 무엇인가? 캐시를 보여준다면 대상 vLLM의 활성화 설정·통계·warm/cold 비교·데이터 신선도 통제는 어떻게 할 것인가?
- 요청 결과: **먼저 필요한 환경 정보 질문지**, 기능 호환 매트릭스, 설정 전환표, 최소 사전 점검 계획, 미지원 시 축소 대안. 민감한 실제 key는 요구하지 말고 환경변수 이름만 명시하라. 캐시 기본 활성화·속도 향상을 버전 확인 없이 주장하지 말라.
- 반영: B04/B24, 두 데모·이관 가이드. 출발점: [FLOW] 데모, [CMP] §21. 다른 발표자의 엔진 상세 조사로 확대하지 않는다.

### R09. 실제 Trace를 의미 변화 없이 수집·표시하는 방법 — P0

- 필요성: 교육용 시각화가 런타임 동작을 바꾸거나 모델에 전달되지 않은 객체를 “최종 요청”이라고 보이면 안 된다.
- 구체 질문: 공개 Hook/Provider Wrapper/Transport 관찰 중 각 프레임워크에서 가능한 위치는? SDK 내부 모델 객체, Provider 변환 후 payload, 실제 전송 데이터 중 어디까지 확인 가능한가? Tool 시작·종료·기록 순서·부모자식 ID·압축·저장을 어떤 이벤트로 수집할까? 가림 처리를 어디서 하고, 순서·Retry·동시성·취소·예외를 바꾸지 않았음을 어떻게 검증할까? 실제 실행 기록의 재생과 라이브 실행 조작을 어떻게 분리할까?
- 요청 결과: 관찰 범위표, 이벤트 필드 초안, 대표 기록 예시, 미관찰 영역, 무관찰 기준 실행 대비 점검 계획. 비공개 Chain-of-thought를 수집·표시 대상으로 삼지 말라.
- 반영: Demo 1·2 전체, B07/B15. 출발점: [FLOW] 실제 내부 데이터 요구, [H2], [P2], [PC].

### R10. BIN 분석 시나리오·데이터·예측의 검증 가능한 범위 — P0

- 필요성: 현재는 공통 예시의 방향만 있고 데이터·오류율 정의·예측 목표·정답이 없다. 수치와 원인을 꾸며낼 수 없다.
- 구체 질문: “빈 오류율”은 어떤 분모·기간·집계 단위의 값인가? 예측 대상이 Bin 분류, Bin 비율, 다음 시점의 값 중 무엇인가? 다른 데이터의 범위와 기준 시점은? 발표자가 제공할 익명/합성 데이터·데이터 사전·알려진 정답은? 이유 설명은 관측 상관·가설·확인된 원인을 어떻게 구분할까? 예측 Tool은 어떤 방법·학습/평가 분할·baseline·metric을 사용할까? 시간 누수·Lot 혼합·SOP Revision 불일치를 어떻게 확인할까?
- 요청 결과: 발표자 결정 목록, 작은 데이터 명세·시나리오 카드, 기대 결과와 근거 필드, 예측 최소 구현 대안과 선택 기준. 합성 데이터 결과를 실제 공정 정확도·인과관계 증거로 제시하지 말라.
- 반영: B07/B13/B15/B23, 두 데모의 공유 입력·출력. 출발점: [FLOW] 공통 데모, [COMMENTS].

### R11. 운영 형태·권한·실행 품질 평가 — P1

- 필요성: 마지막 시사점을 추상적인 “보안을 잘하자”가 아니라 실행·배포 선택으로 연결한다.
- 구체 질문: 중앙 Agent와 로컬 Agent+중앙 LLM 각각에서 Session/사용자/파일/자격증명/정책/Queue/취소/Trace의 소유자는? Worker·Subagent·Tool·모델 동시성을 어떻게 각각 제한할까? 변경·발행의 중복 실행은 어떤 애플리케이션 멱등성 키와 기록으로 막을까? 로컬 설치·업데이트·원복과 중앙 정책 적용의 한계는? 도메인 평가를 Schema/런타임/통합/업무 품질로 어떻게 나눌까?
- 요청 결과: 배치도 두 개, 책임·장단점 표, 측정해야 할 항목, 단계별 최소 운영안. 사용자 수·GPU 수·처리량·응답시간은 환경과 실측 없이 숫자를 만들지 말라.
- 반영: B23–B24, 미래 3차. 출발점: [CMP] §§18–22, 31–36, [HC]. 상세 구현은 이번 발표 필수 범위로 자동 승격하지 않는다.

## 7. Demo 1·Demo 2 기획 및 준비 요구사항

### 7.1 공통 확정 요구와 설계 원칙

| 항목 | 현재 확정 또는 상태 |
|---|---|
| 매핑 | **Demo 1=Hermes / Demo 2=PydanticAI**. [FLOW]가 명시한다. 다른 기술 데모를 추가하지 않는다. |
| 형태 | 슬라이드와 분리된 웹페이지. 발표에서 설명한 구조·부품과 실제 기록을 대응시킨다. 웹 기술·서버·실시간 전송 방식은 미확정이다. |
| 내용 | 한 공통 시나리오의 조회→이유 분석→다른 데이터 기반 예측. 정확한 데이터·예측 정의·Tool 이름·출력 Schema는 미확정이다. |
| 실제성 | 실제 Hermes/PydanticAI 실행을 관찰한다. 가짜 로그·정적 애니메이션을 실제 실행처럼 제시하지 않는다. 실제 기록 재생, 라이브, Mock 시험은 구분한다. |
| 현재/대상 PC | 현재 PC는 OpenAI key 등 외부 API 활용 예정. 대상 PC는 로컬 vLLM 연결이 되어 있다고 [FLOW]가 서술한다. 이번에 접속·실행 확인하지 않았다. |
| 환경 처리 | 실제 구현 단계에서 OS·Python·도구·설치 상태·모델 연결을 자동 점검하고, 필요한 Hermes 소스 ZIP·PydanticAI·Python 패키지 등을 다운로드·설치한다. 기존 설치가 있으면 버전과 경로를 확인하여 재사용부터 검토한다. |
| 가이드 작성 시점 | 실제 구현·설치·실행·검증 후, 검증한 코드·설정·출력에서 명시적인 실행·이관 절차를 추출한다. 지금은 요구사항만 정리한다. |

**공통 학습 효과:** 청중이 “LLM에게 무엇이 전달되었는가”, “누가 도구를 실행했는가”, “다음 실행을 결정한 조건은 무엇인가”, “어떤 정보가 저장되어 다음 요청에 영향을 주었는가”를 실제 한 실행에서 찾을 수 있어야 한다.

**표시할 Trace의 기획안:** run/session/model call/tool call/parent ID, 순서·시간, 실행 버전·설정 식별자, 입력 Snapshot, 모델 요청·응답, Tool 인자·정책·시작/완료·결과, Retry·종료 이유, Memory/History/압축 변화. 실제 API의 이름과 수집 가능 범위는 R02/R03/R09로 확정한다. 병렬 작업의 시작·완료·기록 순서를 같게 그리지 않는다.

“실제 최종 요청” 화면은 **Provider 변환 후 어떤 계층을 관찰했는지** 명시한다. 비밀 key·인증 헤더·민감한 제조 데이터는 저장 전에 가리고, 화면에 가림 표시를 남긴다. 전송 전체를 확인하지 못했다면 내부 모델 객체를 wire payload라고 부르지 않는다. 추론의 비공개 사고 과정을 보여주는 것이 아니라 관찰 가능한 요청·응답·행동을 보여준다.

**조작 방식의 기획 제안:** 실제 실행을 먼저 기록하고 Space로 기록을 순서대로 읽는다. 이는 [FLOW]의 단계 관찰 의도를 유지하면서 실제 실행 순서·동시성을 훼손하지 않는 우선안이다. 라이브 실행과 재생 모드를 분리하고 run ID·기록 시점·사용 모델을 표시한다. 라이브가 필요한 구간은 별도 결정한다. 네트워크 실패에 대비한 실제 기록 재생은 허용할 수 있으나 “지금 실행 중”으로 표시하지 않는다.

**대표 입력 예시(문구·데이터는 기획 제안):**

1. “지정 Lot·기간의 BIN-X 오류율과 기준값을 조회해줘.”
2. “변화의 근거를 다른 측정 데이터와 비교해서 설명해줘. 확인된 사실과 가설을 구분해줘.”
3. “별도 데이터 구간으로 지정 BIN 값을 예측하고 사용 데이터·방법·한계를 알려줘.”

기대 출력은 원천 조회값·분모/기간·데이터 ID, 분석에 쓴 근거와 불확실성, 예측 대상·결과·평가 조건이다. 실제 숫자·인과 결론·예측 정확도는 아직 없다. 도구는 조회·계산·분석 등 필요한 최소 범위를 실제 코드로 구현하되, 공정 변경·실제 발행 등의 부작용은 별도의 Mock 대상과 승인 흐름으로 분리하는 안을 권장한다.

### 7.2 Demo 1 — Hermes의 실제 실행을 보존하며 관찰

**목적과 학습 효과:** 이미 제공되는 Harness에서 Prompt·Memory·Skill·Tool·상태·Subagent가 어떻게 연결되는지 확인한다. 설치된 Agent를 뜯어고쳐 자체 프레임워크처럼 만드는 데모가 아니다. [FLOW]는 대상 PC에서 ZIP 설치된 Hermes를 이후에도 계속 사용할 것이라고 설명한다.

**권장 시연 순서:**

1. 실제 사용 버전·Profile·모델 연결·데모 데이터와 관찰기를 확인한다. 원래 사용자 Profile과 구분되는 데모 작업 범위를 보여준다.
2. 첫 조회 요청을 실행한다. 사용자 입력 기록, 지침/Memory/Skill 목록·History·Tool Schema가 구성된 모델 요청을 연다.
3. 실제 모델 응답에서 선택된 Tool Call과 Runtime 분기를 본다. Tool Intent·정책·실행·결과 기록 및 다음 모델 호출을 연결한다. 최종 응답까지의 실제 반복 횟수를 표시한다.
4. 이어지는 분석 요청에서 이전 대화가 어떤 형식으로 재사용되는지 보고, 근거 조회 결과와 추측을 구분한다. 가능한 경우 Skill 본문을 읽는 시점과 일반 Tool/MCP/Plugin 확장 경로 중 설명에 유효한 사례를 관찰한다.
5. 예측 요청에서 실제 선택된 분석 도구·입력 데이터·결과를 보여준다. Subagent가 실제 호출되는 경우 부모가 전달한 작업·자식 컨텍스트·반환 결과의 범위를 확대한다.
6. 저장된 History/Memory와 현재 요청에 주입된 내용을 비교한다. 압축이 실제 발생했다면 전후 Context·보존 근거·Tool 쌍을 본다. 발생하지 않았다면 “이번 실행에서는 미발생”으로 남긴다.
7. 실제 종료 분기와 저장 결과를 회수하고 슬라이드의 전체 구조로 돌아간다.

**예상 화면/로그:** 전체 아키텍처의 현재 영역, Loop 반복 카운터, 모델 요청의 요소별 패널, 응답/Tool Call ID와 인자·결과, Runtime 분기, History/Memory 변화, 자식 호출 트리. 각 화면은 실제 기록에 존재하는 항목만 채운다. 긴 payload는 요소별 탐색과 가림 처리된 원문 보기로 나누고 단순 요약을 원문이라고 부르지 않는다.

**구현 범위·환경:** 실제 Hermes 설치/소스와 해당 버전이 요구하는 Python·시스템 도구·선택 도구 의존성, Provider 연결, 데모 데이터, 최소 확장 도구, 관찰기, 별도 뷰어. 정확한 의존성·설치 명령은 미확정이다. 대상 PC의 기존 ZIP 설치는 작성자 진술이므로 경로·내용·버전을 먼저 점검한다. 새로운 버전으로 덮어쓰거나 기존 Memory·DB·Skills를 임의 변경하지 않는다. Core 수정 없이 가능한 Hook·Wrapper·로그를 우선 검토하고, 불가피한 변경은 동작 영향·적용 diff·해제 절차를 명시한다.

**관찰 비간섭 검증 요구:** 관찰기를 붙이기 전후에 모델/도구/상태의 핵심 경로가 유지되는지 점검한다. 관찰 때문에 Tool 순서·승인·Retry·오류 전파가 바뀌지 않아야 한다. 성능 오버헤드가 생길 수는 있으므로 무관찰 실행과 관찰 실행을 같은 벤치마크처럼 섞지 않는다.

**선택 범위:** 캐시 속도·토큰 절감 실측은 P2다. 주 데모는 요청과 실행 구조 관찰로 완결되어야 한다. MCP·Plugin·Subagent·압축을 모든 요청에 억지로 발생시키지 않는다. 자연 실행에 나오지 않는 경로는 별도 명시된 재현 시나리오로 다루거나 부록으로 남긴다. Skill/Memory를 실제 저장하도록 할 경우 임시 데모 영역에서 수행하고 원복 방법을 준비한다.

**확정:** Hermes 사용, 기본 구조 보존, 실제 데이터 관찰, 별도 웹페이지, 단계별 탐색, 후속 PC 이관.  
**미확정:** 실제 설치 위치·버전·OS, 관찰 Hook, 데이터, Tools/MCP/Plugin 조합, Subagent 유도·검증 방법, 압축 재현 조건, live/replay 비중, 캐시 실험 여부. 근거: [FLOW] 공통·Hermes 데모, [H2], [HC].

### 7.3 Demo 2 — PydanticAI로 개발하는 범위와 내부 실행의 연결

**목적과 학습 효과:** 개발자가 작성한 Agent 설정·Tools·Deps·출력 계약과 SDK가 담당하는 Graph·Tool Manager·검증·실행을 구분한다. 타입이 주는 구조적 장점을 넘어 종료·병렬·승인·상태 설계에 미치는 영향을 보여준다. **Core 최소 Agent를 먼저**, 선택적 Harness 확장은 그다음에 제시한다.

**권장 시연 순서:**

1. 고정한 Python/Core/선택 Harness 버전과 Provider를 확인한다. 최소 Agent, 데이터 조회 Tool, 실행 시 Deps, 최종 출력 계약을 짧은 코드로 보여준다.
2. Hermes와 같은 조회 요청을 실행한다. Python에만 있는 Deps와 모델 요청의 지침·History·Tool Schema를 비교한다. Tool 등록→모델 노출→호출 선택→인자 검증→실행→Tool Return→다음 요청을 추적한다.
3. 분석 요청에서 내부 Graph 노드와 Run 상태의 전이를 보여준다. 유효성 실패/ModelRetry는 준비된 별도 시험에서 발생 이유와 수정 메시지를 보여주고 통제된 시험임을 밝힌다.
4. 최종 출력과 다른 Tool 호출이 섞이는 검증된 사례로 EndStrategy 차이를 비교한다. 자연 LLM 실행에서 재현이 불안정하면 별도의 명시적 런타임 시험으로 분리한다. 실제 LLM이 내놓지 않은 응답을 실제 응답처럼 표시하지 않는다.
5. Hook/Capability를 켠 경우 어떤 지침·Schema·실행 전후 동작이 달라졌는지 확인한다. 여러 Capability의 합성과 정책 위치를 실제 지원 범위 안에서 보여준다.
6. 이어지는 요청에서 History 전달·저장과 Compaction을 구분한다. 별도 Harness 확장을 사용할 경우 설치·제공 계층이 달라졌음을 표시하고 Memory/Skills 중 가치가 큰 최소 사례를 추가한다.
7. Orchestration의 대표 경로를 실행한다. 부모에게 결과를 돌려주는 도구 위임, 개발자 코드/Graph의 라우팅, Harness Subagent/Advisor 중 실제 지원·시나리오에 맞는 것을 선별한다. 모든 패턴을 한 실행에 강제로 넣지 않는다.
8. 승인 대기 예제가 필요하면 안전한 Mock 변경 요청으로 pending→승인/거절→재개를 보여준다. 승인 요청 ID·정확한 인자·데이터 버전을 확인한다. 결과 구조가 유효함과 분석이 맞음을 별도로 평가하고 슬라이드로 복귀한다.

**예상 화면/로그:** 개발자 코드와 SDK 내부 실행의 구분, Graph 현재 Node, 최종 Provider 요청, Tool Schema·검증 오류·Retry, 병렬 시작/완료와 Barrier, EndStrategy 분기, Hook/Capability 순서, History/Compaction 비교, Deferred 승인 상태, 위임의 부모/자식 경계. 기능이 실제 기록되지 않았다면 성공한 것처럼 채우지 않는다.

**구현 범위·환경:** 실제 PydanticAI Core, 모델 Provider 관련 패키지, 데이터·분석 Tools, 관찰기, 뷰어. Harness·MCP·Logfire/Evals 등은 실제 필요한 부분만 선택하고 독립 버전·설치 옵션·외부 통신·인증 요구를 확인한다. 관찰용 단순 Logger로 충분한데 평가 플랫폼을 의무 설치하는 식으로 범위를 키우지 않는다. `output_type`은 해당 데모 역할의 최종 출력 계약으로 설계하며, 범용 Agent의 모든 대화에 한 분석 Schema를 강요해야 한다는 일반 결론을 만들지 않는다.

**확정:** 실제 PydanticAI, 개발자 작성 범위와 SDK 추상화 구분, Tool 등록·실행·Context·EndStrategy·Hook/Capability·Memory/Compaction·Orchestration을 설명할 관찰 요구, Core 우선 후 Harness 확장, vLLM 이관.  
**미확정:** 정확한 패키지 조합, 출력 Schema, History 저장소, 실행 API, 동시성 설정, EndStrategy 재현 방법, Hook/Capability 실제 API, Harness 제공 기능 중 시연할 범위, 승인 UI·재개 방식, 위임/Graph/Advisor의 선별 범위. 근거: [FLOW] PydanticAI 데모·추가 목록, [P2], [PC].

### 7.4 발표자가 준비할 자료와 실행·이관 가이드 요구

**발표자 제공/결정 필요:** 발표 시간과 시연 비중, 대상 PC 접근 조건·OS, Hermes 기존 설치 경로/버전, vLLM의 비밀정보를 제외한 endpoint·model ID·기능 정보, 데이터 반출/외부 API 허용 범위, 익명/합성 데이터와 정답·분모·기간·예측 대상, 승인 역할, 온라인/오프라인 시연 조건. API key 자체는 문서에 넣지 않는다.

**후속 구현 에이전트가 실제 결과로 작성할 가이드의 필수 내용:**

| 범주 | 반드시 포함할 사항 |
|---|---|
| 환경 자동 점검 | OS/아키텍처/Python/패키지 관리 도구/기존 설치·ZIP·가상환경/네트워크·포트/모델 연결을 점검하고, 충족·미충족·조치 결과를 구분한다. 설치 전 기존 작업 영역과 Profile을 식별한다. |
| 설치·소스 확보 | 고정 버전·공식 소스 위치·ZIP 또는 패키지 취득 경로·필요 시스템 의존성·작업 디렉터리·실행 명령을 기록한다. 구현에 필요한 의존성은 자동 설치하되 기존 Hermes를 임의 교체하지 않는다. 설치가 제한되는 환경의 수동 조치와 중단 조건도 기록한다. |
| 실행 | 파일 트리, 각 명령의 정확한 cwd, 환경변수 이름과 예시 placeholder, Backend/Viewer의 시작 순서·포트·종료·로그 위치·정상 화면을 적는다. 구현하지 않은 명령을 미리 확정하지 않는다. |
| 시연 | 슬라이드에서 이동할 시점, 각 입력, 관찰할 패널·분기, 다음 단계 키, 예상 실제 로그/화면, 복귀 위치, 데이터 초기화·재실행 방법을 기록한다. |
| 검증 | 설치·기본 호출·Tool/Context/상태 관찰·주요 분기·오류·승인·재개·기록 재생을 확인한다. 무엇을 실제 실행했는지, 사용 모델·버전·환경과 미검증 경로를 남긴다. Schema 통과만으로 예측 정확도를 검증했다고 쓰지 않는다. |
| 다른 PC 이관 | 현재 PC 외부 API 설정과 대상 vLLM 설정의 대응표, 정확히 수정할 파일·필드·전후 값 형식·설정 조건, Provider/Profile·Tool parser 등 차이, 데이터·Trace·의존 파일 목록, 이동 후 검사·실패 시 원복을 제시한다. 다른 PC 미접근이면 검증 완료라고 표시하지 않는다. |
| 낮은 구현 역량의 모델을 위한 지시 | [FLOW]의 “qwen 3.8 수준” 표현은 정확한 제품명이 미확정이다. 작은 단위의 적용 순서·전제·허용 변경·예상 diff·검사 명령·정상/실패 판단·원복을 적어 모호한 “환경에 맞게 수정”을 없앤다. 실측하지 않은 대상 모델 능력은 단정하지 않는다. |
| 실패 대비 | API/네트워크/Tool 선택·출력 형식·승인 UI 실패별 대처와 실제 사전 기록의 재생 경로를 준비한다. Mock/과거 기록/live 상태를 식별한다. 원본 Profile·DB·Memory를 보호하고 관찰기 해제 방법을 제공한다. |

최종 가이드는 실제 구현 뒤 작성한다. 지금 적은 항목은 완료된 설치·실행 절차가 아니라 **제작 요구사항**이다.

## 8. 미확정 사항 및 주의점

### 8.1 자료 간 충돌과 해석 경계

| 항목 | 충돌·오해 가능성 | 인계 처리 |
|---|---|---|
| 발표 순서 | [FLOW] 도입의 초기 고민, [CMP] Appendix B의 학습 순서, §37의 18장 구조가 서로 다르다. | [FLOW] 상단 명시 순서를 적용한다. 종합 문서의 목차·장수를 복사하지 않는다. |
| 검증 시점 | [FLOW]는 추가 검증을 요청하지만 현재 작업은 외부 조사·설치·실행 금지다. | 이번에는 질문을 추출했다. 후속 조사·제작 단계에서 검증한다. |
| 데모 실제성 | 1차 형식 자료의 고정 예제·모의 설명 방식이 2차의 실제 데이터 요구와 다르다. | 형식만 참고한다. 2차는 실제 기록을 근거로 하며 재생/Mock은 식별한다. |
| 분석 버전 | 기초·심층·Claude SDK 번들 CLI 버전이 다르고 온라인 문서는 갱신될 수 있다. | §3.3 기준을 명시하고 버전 혼합을 금지한다. 설치 버전·최신 버전은 미확인이다. |
| Hermes Memory API | [FLOW]의 `add/patch/remove`와 기존 심층 설명의 `add/replace/remove` 표기가 다르다. | R02에서 대상 버전의 실제 Tool Schema·연산을 확인한다. 임의 통일하지 않는다. |
| Hermes 새 구상 | Prompt refresh 명령·Curator 조건·폴더·숫자 기본값은 흐름 문서의 구상과 고정 연구 범위가 정확히 일치하는지 불명확하다. | 설명 후보와 확인된 근거를 분리한다. R02 결과 전 확정 기능·기본값으로 표현하지 않는다. |
| PydanticAI 코드 | 흐름 문서의 타입·Hook/Capability 생성자·줄 번호·실행 API 오타·“21.2” 참조는 검증된 실행 예제가 아니다. | R01/R03에서 실제 이름·수명·출처를 감사한다. 불명확한 내부 자료형을 새로 만들지 않는다. |
| PydanticAI Memory/Harness | “모두 직접 구현해야 하는가”라는 질문은 기존 조사에서 Core/별도 Harness 구분으로 일부 해소된다. | 질문을 사실로 받아 적지 않는다. 구체적 제공 범위·설치 조합은 R05. |
| Graph와 Handoff 명칭 | 내부 Graph를 LangGraph로 오인하거나 프로그램 라우팅을 OpenAI native Handoff와 동일시할 위험이 있다. | 구조·제어권으로 설명한다. 제품 API의 일대일 대응은 검증 후에만 사용한다. |
| Claude 지침 파일 | `@AGENTS.md` import 예시와 최신 조사 버전의 fallback은 다른 조건이다. | 항상 둘 다 자동 로드된다고 하지 않는다. R07 확인. |
| Claude 내부 관찰 | 공개 SDK 소스가 곧 비공개 CLI Loop 전체 소스는 아니다. | 공개 통신·계약까지만 주장한다. 두 실동작 데모는 Hermes·PydanticAI에 한정한다. |
| ADK 실행·복구 | 종합 자료의 축약 경로·durable 표현은 심층의 새 실행 경로·resume TODO보다 넓게 읽힐 수 있다. | [G2]의 구체 조건을 우선 설명하되 충돌을 R06에 전달한다. 무조건적인 복구 보장을 하지 않는다. |
| 압축과 보존 | 일반적 “압축은 원본 삭제가 아님” 표현이 PydanticAI의 변환된 History 저장 경로까지 설명하지는 못한다. | 현재 요청 변환·저장 이력·원본 보관 정책을 기술별로 구분한다. |
| vLLM Cache | [FLOW]의 APC 기본 활성화·속도 개선 설명은 대상 버전·설정·측정이 없다. | 원리와 실험 주장을 구분한다. 캐시 실측은 선택 과제이며 R08 필요. |
| 설치 상태 | 프로젝트에 ZIP/실행 코드가 없지만 [FLOW]는 대상 PC Hermes 설치·vLLM 연결을 서술한다. | 서로 다른 환경의 서술이다. 로컬 프로젝트 부재를 대상 PC 미설치로 결론내리지 않는다. |
| 도메인 사례·예측 | BIN 시나리오는 예시이며 데이터·원인·모델·정확도가 정해지지 않았다. | R10과 발표자 결정 전 숫자·성과·인과 결론을 만들지 않는다. |
| 실무 코멘트·평가표 | 코멘트는 설계 해석이며 종합 비교의 ◎/○/△는 정성 평가다. | 실제 도입 성과·공식 보장·성능 순위로 바꾸지 않는다. |

### 8.2 블루프린트 전 결정할 사항

우선 결정할 것은 **총 발표 시간과 청중 수준**, **BIN 조회·예측의 정확한 의미와 데이터**, **데모에 반드시 보여줄 경로와 부록으로 돌릴 경로**, **실제 사용할 패키지 버전**, **대상 PC 환경·모델 기능**, **데모 live/replay 비중**이다. 원문에서 요구한 관찰 범위는 보존하되 모든 기능을 하나의 실행에 넣어야 한다고 해석하지 않는다.

공개 문서상의 “지원”, 소스에 해당 코드가 “존재”, 해당 설정에서 “실제로 관찰”, 대상 PC에서 “재현 성공”은 서로 다른 상태다. 다음 단계 산출물에는 이 구분을 출처·검증 노트로 유지한다. 청중 화면에 무의미한 경고 배지를 반복할 필요는 없지만 조건과 한계를 지워서는 안 된다.

## 9. 다음 단계 AI에게 전달할 작업 지시

### 9.1 GPT: 최종 2차 세미나 블루프린트 작성 요청

> 이 문서는 현재 프로젝트의 의도·조사 자료·형식 참고를 통합한 입력이다. **Hermes → Claude Code → PydanticAI → OpenAI Agents SDK → Claude Agent SDK → Google ADK → Microsoft Agent Framework** 순서를 유지하고 Hermes·PydanticAI를 중심으로 구성하라. 청중의 1차 학습을 전제로 각 기술의 전체 아키텍처를 먼저 제시한 뒤 실제 동작·차이·개발 책임을 확대하라. 일반 Agent 개념 반복과 제품 기능 목록 나열을 피하라.
>
> 먼저 R01–R11 중 필요한 조사 결과와 발표자 결정 사항을 확보하라. 로컬에서 이미 설명된 개념을 불필요하게 처음부터 재조사하지 말고, 코드/API·버전·공개 범위·모델 호환 등 미해결 조건을 확인하라. 수정할 점이 발견되면 원래 주장·변경 근거·영향을 기록하라. 답이 없으면 미확정으로 두고, 그 답이 없어도 설명할 수 있는 내용과 데모 필수 조건을 나눠라.
>
> 그다음 **최종 2차 세미나 발표 블루프린트**를 작성하라. 각 슬라이드에 제목·한 문장의 핵심 주장·화면 콘텐츠·필수 설명·도식/비교/단계별 강조·발표자 노트·전후 연결·근거 경로/버전·데모 진입/복귀를 구체화하라. 장수와 시간은 새로 설계하고 1차 목차를 복제하지 말라. B01–B24는 내용 묶음일 뿐 확정 페이지 수가 아니다.
>
> 형식은 1차의 정보 위계·의미 색상·단계 강조·읽기 좋은 화면과 상세 노트 분리를 참고하라. 완성형 시각 자료 지시와 페이지별 상세 배치는 이 블루프린트에서 확정하라. Hermes·PydanticAI의 실제 실행 관찰을 본문 설명에 연결하되 별도 데모 웹페이지를 요구하라. 아직 생성되지 않은 Trace나 성능 수치를 완성된 결과처럼 작성하지 말라.
>
> Orchestration은 반환·제어권·상태·격리를 그림으로 명확히 설명하라. 반도체 시사점은 데이터 Snapshot/SOP 버전, 검증과 인가, 승인한 최종 인자, 재개·부작용, 평가 기준처럼 설계 선택에 영향을 주는 부분만 선별하라. 실제 데이터와 근거가 없는 공정 성과를 주장하지 말라. 마지막 운영 형태 비교는 확정 구축안이 아니라 3차의 선택 질문으로 연결하라.
>
> 블루프린트의 별도 제작 명세에는 Demo 1·2 각각의 관찰 목표·시나리오·데이터·환경·수집 이벤트·화면·제작 범위·검증 기준·실패 대안을 적어라. 구현 전 확정할 조건과 구현 후 실측으로 채울 내용을 구분하라. 이미 실행한 것처럼 명령·로그·화면을 꾸미지 말라.

### 9.2 이후 Codex/구현 에이전트에게 전달할 제작 범위

1. 확정 블루프린트를 읽고 원본 학습 자료를 보존하면서 발표자료를 제작한다. 화면 정보 밀도·도식 관계·키보드 조작·발표자 노트를 검증한다.
2. Demo 1 Hermes를 실제 설치 상태 점검부터 구현한다. 필요한 소스 ZIP·의존성을 확보하되 기존 설치·설정·Memory·DB를 보호한다. 원래 흐름을 유지하는 관찰 방법으로 실제 Trace와 별도 뷰어를 만든다.
3. Demo 2 PydanticAI를 고정 버전의 Core 최소 실행부터 구현한다. 선택 Harness 기능은 범위를 나누고 실제 제공 경계를 보여준다. Tools·Context·Graph·출력/Retry·EndStrategy·Hook/Capability·상태·위임 중 확정한 경로를 관찰한다.
4. 구현 과정의 필요한 환경 점검·설치를 자동 수행하고, 전체 실행·주요 분기·안전한 실패·승인/재개·데이터 품질·뷰어 표시를 확인한다. 현재 PC의 외부 API 검증과 대상 PC의 vLLM 검증 결과를 따로 기록한다. 다른 PC에서 확인할 수 없으면 이관용 점검 절차와 미검증 상태를 남긴다.
5. **실제로 검증한 결과로** 발표자 실행 가이드와 상세 이관 계획을 작성한다. 명령·경로·설정 차이·기대 화면/로그·실패 판단·원복을 명확히 적고, 다른 구현 모델이 작은 단계로 적용·검사할 수 있게 한다.
6. 최종 인계 시 발표자료, 데모별 실행 코드·고정 의존성, 데이터 설명, Trace의 출처와 가림 조건, 재현·실행·시연·이관 가이드, 검증 결과와 남은 한계를 함께 제공한다.

이번 단계의 완료 조건은 위 제작을 수행하는 것이 아니라, **이 문서 하나로 다음 GPT가 발표의 내용·이유·흐름·근거·부족한 조사·두 데모의 범위를 이해하고 최종 블루프린트를 설계할 수 있게 하는 것**이다.
