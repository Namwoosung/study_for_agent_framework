# Claude Code 발표자료 개정 목차와 작성 계획

2026-11-03 작성. 이 개정안을 발표 54~82쪽에 반영했다. 기존 CLAUDE 및 S16~S19 구간을 29장으로 구성했다.

## 1. 발표의 중심

**Hermes에서 익힌 실행 흐름을 기준으로, Claude Code가 같은 문제를 어떤 설정·컨텍스트·실행 경계로 푸는지 설명한다.** 같은 이름의 기능이라도 저장 대상, 로딩 시점, 권한, 결과 전달, 수명주기가 다른 부분을 확대한다. 차별점은 제품 독점 기능을 뜻하지 않으며, 이번 Hermes 발표에서 설명한 구현과 비교했을 때 설명할 가치가 있는 차이를 뜻한다.

- 공통 흐름: 모델 → Tool → 관찰 → 재호출, 상태/기억의 구별, MCP의 기본 역할, 독립 Context의 일반적인 장점은 짧게 연결한다.
- 상세 설명: 지침 선택·지연 로딩, Auto Memory, Skills 호출/권한/별도 실행, Tool Search, Permission/Hook 실패 방식, Bash Sandbox, OTel, Subagent/fork/Teams, 작업 복구와 예약의 수명이다.
- 코드: 공식 설정 JSON, frontmatter, Hook 입력/출력과 짧은 사용자 handler를 우선한다. 공개 Sandbox Runtime과 SDK의 코드는 각각 공개된 부품·통합 경계라고 표시한다. 비공개 CLI 루프/스케줄러 함수를 만들지 않는다.

## 2. 기준 자료와 버전

다음 로컬 문서를 대조했다.

1. [기본 학습자료](../../../study/Claude_Code/Claude_Code.md): v2.1.310 기준 개념·도구·지침·메모리·안전·운영 범위.
2. [2차 심층 학습자료](../../../study/Claude_Code/Claude_Code_2%EC%B0%A8_%EC%8B%AC%EC%B8%B5_%ED%95%99%EC%8A%B5_%EB%B6%84%EC%84%9D.md): v2.1.314 기준 Part I~XII와 W01~W15. 이번 구성의 주된 기준이다.
3. [사용자 추가 코멘트](../../../study/Claude_Code/Claude_Code_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md): 캐시 효율과 근거 최신성의 분리, 업무 코드 수정과 실행기 수정의 차이를 반영한다.
4. 현재 `notes.json`의 CLAUDE/S16/S17/S18/S19와 Hermes 개정 목차·설명.

공식 자료는 아래 D/S 목록을 2026-11-03에 확인했다. **v2.1.314는 로컬 심층 교재의 비교 기준이며 최신 버전이라고 주장하지 않는다.** 현재 공식 문서는 이후 동작도 포함할 수 있다. 실제 장표 작성 시 예시의 대상 CLI 버전·설정·실험 플래그·플랫폼을 함께 적고, v2.1.314 릴리스와 현행 문서의 차이는 Sources에서 나눈다. SDK v0.2.174와 CLI v2.1.314는 다른 버전 체계다.

공식 설명과 공개 저장소만으로 핵심 비교가 가능하므로 비공식 역공학 글은 근거로 채택하지 않는다. Anthropic의 Sandbox 기술 글은 설계 배경에 사용하고, 현재 기본 동작은 제품 레퍼런스로 확인한다.

## 3. 전체 흐름과 권장 분량

**실행 개요 → Context·기억 → Tools·Skills → 안전장치·관측 → 긴 작업·위임 → 예약·활용 → Harness 비교**

권장안은 **총 29장: 대주제 구분 1장 + 설명 23장 + 범주 전환 5장**이다. Hermes 48장을 같은 비중으로 반복하지 않는다. 공통 루프는 도입 1장에서 연결하고 차이가 있는 주제에 장수를 배정한다. 시간 제약이 생기면 코드 예외표와 설정 전체를 Sources로 옮기고, 본문 글자를 줄여 넣는 방식은 피한다.

| 묶음 | 설명 장표 | 전환 장표 | 설명할 핵심 |
|---|---:|---:|---|
| 시작·공통 실행 흐름 | 2 | 0 | 대주제 시작, Hermes와 공유하는 루프·공개 코드 범위 |
| Context·기억 | 3 | 1 | 요청 계층, 지침 로딩, Auto Memory와 Session |
| Tools·Skills | 4 | 1 | 지연 Tool 명세, Skill 호출과 권한, Plugin 배포 |
| 안전장치·관측 | 6 | 1 | 정책·Hook 분기, Sandbox, OTel·Trace |
| 긴 작업·위임 | 6 | 1 | 캐시·압축, Subagent·fork·Teams·복구 |
| 예약·활용·비교 | 3 | 1 | 예약 작업 수명, 명령 사용, 두 Harness의 선택 기준 |
| 합계 | 24 | 5 | 29장 |

CCxx는 작성 계획용 ID이며 최종 전역 화면 번호는 실제 작성 시 정한다. 범주 전환 페이지에는 다음에 설명할 항목만 보여주고, 반복 범주 메뉴는 사용하지 않는다.

## 4. 장표별 작성안

| ID | 제목 후보 | 전달할 내용 / Hermes 연결 | 권장 표현·근거 |
|---|---|---|---|
| CC00 | Claude Code | 코딩 작업에 맞춰 구성된 Harness를 설명한다는 시작. 모델·SDK·CLI 관계는 작게 표시 | 대주제 구분 + 전체 역할도. D01/S01 |
| CC01 | 실행 루프는 같고, 살펴볼 지점은 다릅니다 | Gather/Act/Verify는 Hermes와 같은 반복 원리. 이후에는 Context·정책·위임의 다른 동작에 집중. 소스 확인 범위 명시 | 기존 Hermes 루프에서 공통 경로를 흐리게, Claude의 확장 접점을 강조. D01/S01 |
| 전환 A | Context와 기억 | 지금 모델이 읽는 정보와 세션 밖에 남는 정보를 설명 | 한 줄 흐름 |
| CC02 | 모델 입력의 세 계층 | System / Project / Conversation의 역할과 로딩 시점. 전체 payload 바이트 명세로 오해하지 않게 함 | 세 계층 누적도. D02/D03 |
| CC03 | 어떤 지침을 언제 읽을까? | 사용자·프로젝트·하위 폴더·path-scoped Rules, CLAUDE.md/AGENTS.md의 조건부 선택. 파일 존재와 실제 로딩을 구별 | 작은 디렉터리 트리 + 로딩 분기. D04 |
| CC04 | Auto Memory는 색인에서 필요한 기억을 찾습니다 | MEMORY.md와 Topic 파일, 시작 로딩 한도, 모델의 선택적 기록. Hermes의 MEMORY/USER와 Session FTS 검색을 같은 기능끼리 비교 | 파일 구조 + 시작/필요 시 로딩. Session은 보조 비교 상자. D04/D05 |
| 전환 B | Tools와 Skills | 호출 가능한 기능과 작업 절차가 연결되는 방식 | 한 줄 흐름 |
| CC05 | 필요한 Tool 명세를 나중에 불러오기 | 내장 Tool의 일반 기능은 생략. MCP 이름·서버 지침 → ToolSearch → 필요한 명세의 흐름과 fallback 조건 설명 | 단계형 명세 노출도. Hermes의 Registry 공개와 비교하되 독점 기능이라고 주장하지 않음. D06 |
| CC06 | Skill은 누가 호출하고 어디까지 유지될까? | 사용자/모델 호출, 본문 지속과 턴별 권한 지속의 차이. allowed-tools는 단순한 도구 제한 목록이 아님 | frontmatter 일부 + 두 수명선. D07 |
| CC07 | Skill의 fork와 대화의 fork는 다릅니다 | context: fork는 Skill을 별도 Subagent의 작업으로 전달. 현재 대화 전체를 계승하는 fork와 구별. agent/skills 조합의 방향도 제시 | 부모 History·Skill 본문 전달 비교. D07/D08 |
| CC08 | Plugin으로 작업 환경을 묶어 배포하기 | Hermes의 register(ctx) 확장과 Claude Plugin의 manifest·Skills·Agents·Hooks·MCP 패키징을 대비. Mods는 별도 코드 확장으로 명명 | 작은 파일 트리와 Plugin 구성도. Mods 상세는 권한 장의 Sources로 연결. D09 |
| 전환 C | 안전장치와 실행 기록 | 실행 판단과 실행 관측을 함께 확인 | 한 줄 흐름 |
| CC09 | 지침과 실행 권한은 다른 설정입니다 | settings 범위·deny/ask/allow와 모드. Plan/Auto 등은 이름을 나열하기보다 같은 호출의 판단 차이로 설명. Hook/Mod·관리형 설정 예외 포함 | 최소 settings.json + 분기표. D10/D11 |
| CC10 | PreToolUse에서 무엇을 결정할 수 있을까? | matcher → 입력 JSON → permissionDecision/updatedInput → 실행 판단. PostToolUse와 Stop은 다른 시점의 제어 | 실제 공식 이벤트 형식 + 짧은 handler. 이벤트 전체 목록은 Sources. D11 |
| CC11 | Hook이 실패하면 실행은 계속될까? | 명시 deny, 종료 코드 2, 일반 오류, timeout, onFailure를 나누고 Command/HTTP와 SDK callback을 구별 | 4가지 실패 사례 표. Hermes의 pre_tool_call 실패 차단과 직접 비교. D11 |
| CC12 | Bash Sandbox가 제한하는 범위 | 권한 판정과 OS 파일·네트워크 격리의 차이. 파일 Tool/MCP/Hook은 동일 Sandbox 안이라고 그리지 않음. 공개 Sandbox Runtime의 API로 코드 설명 가능 | 경계도 + 공개 initialize/wrapWithSandbox 사용 예시. CLI 본체 코드로 표시하지 않음. D12/S02/S03 |
| CC13 | Claude Code의 지표·이벤트·Trace | Session 기록, 사용량 지표, 이벤트, beta span의 목적과 기본 활성화 조건. Hermes Observer/Exporter와 비교 | 수집 경로와 작은 opt-in 설정 예시. D13 |
| CC14 | 승인 대기와 실제 실행 시간을 나눠 보기 | interaction→LLM/Tool→승인 대기·실행, 자식 span 연결. API 오류·정책 거부·실행 실패 구별, payload 상세 수집은 별도 gate | 공식 span 계층과 가상 이벤트. 실제 계측 결과로 표시하지 않음. D13 |
| 전환 D | 긴 작업과 위임 | 입력 재사용, 대화 축약, 작업 분할을 연결 | 한 줄 흐름 |
| CC15 | 어떤 변경이 캐시의 어느 부분에 영향을 줄까? | Prefix 원리는 Hermes 설명을 참조. 모델/Tool 정의 변화와 파일·Skill 변경, 압축의 영향 범위를 비교 | 세 계층의 변경 전/후 비교. 캐시 적중과 최신 SOP 조회를 별도 판단. D02/사용자 코멘트 1 |
| CC16 | 압축 뒤에는 무엇을 다시 읽을까? | 요약 원리 재설명보다 루트 지침·경로 규칙·사용한 Skill·파일의 재주입 차이와 budget을 설명 | 실제 규약 기반의 가상 Before→Summary→Reload. D03/D07 |
| CC17 | Subagent는 어떤 설정으로 시작할까? | 위임 원리는 Hermes와 같다고 연결. description·system prompt·tools/model/permissionMode/memory/skills 등으로 역할 구성. 부모/자식 전달 범위 | .claude/agents/*.md 일부 + 실행 생명주기. D08 |
| CC18 | 새 Context, 대화 fork, background의 차이 | 새 전문 Subagent와 대화 계승 fork, 반환 대기/알림의 차이. 중첩 위임과 동시성은 공개 조건을 확인해 설명 | 전달되는 입력과 결과 경로의 비교도. 내부 thread pool 구현 추정 금지. D08 |
| CC19 | Teams는 작업 목록과 메시지로 협업합니다 | 단순 자식 반환과 팀의 조정을 비교. 현재 Subagent의 메시징·중첩 기능도 반영하여 Teams만 통신 가능하다고 단정하지 않음 | Lead·Task·Teammate·Message 관계도, 실험적/default off 표시. D08/D14 |
| CC20 | 대화를 되돌리는 일과 파일을 되돌리는 일 | Worktree, Context 격리, resume, checkpoint/rewind의 목적을 분리. Hermes의 opt-in checkpoint와 비교 | 두 상태축과 복구 범위. Shell·외부 효과·background 예외를 Sources에 정리. D08/D15 |
| 전환 E | 예약과 활용 | 이해한 구조를 실제 사용 흐름으로 연결 | 한 줄 흐름 |
| CC21 | 예약 작업은 어디에 남고 어디서 실행될까? | Hermes Cron과 /loop·Session 예약·Desktop·Cloud의 실행 호스트·세션 의존·재개 범위를 비교 | 수명 비교표 + 짧은 /loop 예시. D16 |
| CC22 | 탐색·실행·검토에 맞춰 명령 사용하기 | /context·/memory, /permissions·/hooks, /compact·/resume·/rewind를 각각 해당 구조와 연결. 옵션으로 /btw·/subtask 활용 | 짧은 작업 시나리오에 필요한 명령만 연결. 별도 실제 Demo 신설은 이번 계획에 포함하지 않음. D03~D05/D08/D10/D11/D15 |
| CC23 | 두 Harness에서 어디까지 바꿀 수 있을까? | Hermes의 공개 코어 수정과 Claude Code의 설정·확장 접점을 비교. Agent SDK는 같은 능력을 앱에서 호출하는 연결로 짧게 설명하고 PydanticAI로 전환 | 변경 요구가 업무 코드/설정/Hook/내부 실행기 중 어디에 있는지 비교. 사용자 코멘트 2/S01/S04 |

## 5. 공통 설명을 줄이는 기준

| 주제 | 본문 처리 | 확대할 차이 |
|---|---|---|
| Agent Loop·Tool Calling 원리 | CC01에서 한 번 연결 | Claude에서 공개 확인 가능한 제어 접점 |
| Context/Session/Memory의 일반 정의 | 기존 설명 참조 | 파일 선택, Index·Topic, 재로딩 |
| Tool schema와 실행 코드의 구별 | 한 문장 연결 | 모델에게 명세가 언제 공개되는가 |
| MCP의 Client/Server 구조 | 기본 도식 재사용 안 함 | ToolSearch·가용성·명세 로딩 |
| Skill의 문서/참고 자료 구조 | 작은 트리로 회상 | 호출 제어·권한 수명·별도 Context |
| Skill 자체 수정·관리 | Hermes 내용을 다시 강의하지 않음 | Claude에서 문서 작성/배포와 Hermes skill_manage/Curator를 동일 기능으로 취급하지 않음 |
| 승인·Guardrail 필요성 | 일반 당위는 생략 | Rule/Hook/Mod 우선순위, 실패·timeout 정책 |
| Sandbox의 일반 개념 | 짧게 연결 | Bash 적용 범위와 공개 Runtime, 플랫폼 조건 |
| Trace가 필요한 이유 | 재설명 생략 | 문서화된 OTel 이벤트·beta span·기본 opt-in |
| Prefix Cache와 압축 원리 | 기존 원리 참조 | 세 계층 변화·재주입·Skill 유지 규약 |
| 병렬 Tool·Subagent 기본 차이 | 한 문장 연결 | 설정·fork·대기/알림·중첩·Teams |
| Cron의 기본 개념 | 생략 | Session/Desktop/Cloud의 수명 |
| 서비스 운영 일반 구조 | 부록/3차 | CLI와 Agent SDK의 경계만 본문 연결 |

## 6. 이번 조사에서 확인한 작성상 주의점

아래 항목은 장표 초안을 쓰기 전에 확인해야 할 중요한 비교 조건이다. 전부를 한 장에 몰아 넣지는 않는다.

1. **AGENTS.md:** 현재 공식 문서는 조건부 직접 로딩과 설정 선택을 제공한다. 미지원/비활성·이전 버전 예외가 있어 “CLAUDE.md만 지원”과 “항상 둘 다 로딩” 모두 피한다. 전용 AGENTS 로딩과 import의 InstructionsLoaded 차이는 Sources에 둔다. D04
2. **Skill 권한:** allowed-tools의 사전 승인은 호출 턴에 적용되고 본문은 이후 대화에 남을 수 있다. 도구 집합 제한과 같지 않으며, 현행 문서의 disallowed-tools 및 관리형 설정과 나누어 설명한다. D07
3. **두 fork:** context: fork Skill은 현재 History를 자동 계승하는 대화 fork가 아니다. Skill 본문이 자식의 작업 입력이 된다. 일반 Subagent/Explore·Plan의 시작 지침도 동일하다고 가정하지 않는다. D07/D08
4. **Tool Search:** 현행 공식 문서의 기본은 지연 로딩이며 auto는 임계값 모드다. 10% 임계값을 모든 버전의 기본값으로 적지 않는다. 공급자·Gateway fallback 조건을 함께 확인한다. D06
5. **Hook 실패:** command/http의 onFailure=block, 명시적인 정책 거부, exit code 2, timeout, SDK callback의 차이를 구분한다. 네이티브 Windows의 예외도 있어 “Hook 오류면 모두 통과/차단”이라는 단정은 피한다. D11
6. **Permission과 Mods:** 일반 Hook의 allow는 명시 deny/ask를 우회하지 않는다. Mod의 tool.check는 로그인/관리형 정책/모드 조건에 따른 예외가 있으므로 Plugin과 Hook을 한 개념으로 합치지 않는다. 상세 조건은 부록 매트릭스로 관리한다. D10
7. **Sandbox 플랫폼:** 현행 Claude Code 제품 문서는 네이티브 Windows에서 Shell Sandbox를 적용하지 않는다고 설명한다. 한편 공개 sandbox-runtime 저장소에는 Windows 기능도 있다. 독립 부품 main의 기능을 특정 Claude Code 배포본의 통합 기능으로 옮겨 주장하지 않는다. D12/S02
8. **Trace:** 현행 Monitoring에는 beta distributed trace가 있으며 기본 off다. 일반 telemetry와 beta gate 및 exporter를 구분하고, 지원 버전·민감 필드 수집 gate를 별도 표기한다. Hermes의 내용 없는 Gateway health OTLP와 같은 종류의 기록으로 비교하지 않는다. D13
9. **Subagents:** 현행 문서는 중첩 위임과 대화 fork, named-agent 메시징을 설명한다. 오래된 “자식은 자식을 만들 수 없다/반드시 부모에게만 보고”를 보편 규칙으로 쓰지 않는다. Teams는 여전히 실험적·기본 비활성으로 구분한다. D08/D14
10. **예약:** Session-scoped라고 해서 종료 뒤 무조건 소멸한다고 설명하지 않는다. 현재 문서는 미만료 작업의 resume 복원과 예외를 설명한다. 실행 호스트가 켜져 있어야 하는 조건과 저장의 수명을 나눈다. D16
11. **복구:** checkpoint는 파일 Tool의 편집 추적 기능이다. 대화·파일·외부 효과의 복원 범위가 다르며 background 실행의 변경을 main checkpoint와 합쳐 보장하지 않는다. D15/D07

## 7. 원문 범위의 배치

| 로컬 심층 교재 | 발표 반영 |
|---|---|
| Part I / W01 | CC00~01. 공통 루프는 축소 |
| Part II / W02~03 | CC02, CC15~16. 캐시와 재주입의 차이에 집중 |
| Part III / W04~05 | CC03~04 |
| Part IV / W06~08 | CC05~08, CC10 |
| Part V / W09~10 | CC09~12. 일반 보안 체크리스트는 Sources |
| Part VI / W11~12 | CC17~20 |
| Part VII / W13~15 | 관측·예약과 SDK 경계만 CC13~14/21/23. 전체 서버·Queue·Gateway 설계는 부록·3차 |
| Part IX 실패 사례 | F04~10은 Context/Hook, F13~16은 위임/복구, F21은 예약 장의 예외로 분산. 24개 실패 표를 본문에 복사하지 않음 |
| Part X | CC23. 다른 SDK와의 7종 비교는 후속 구간과 중복하므로 생략 |
| Part XI 기존 15장안 | 주제 선택의 참고. 이번에는 Hermes 이후 발표이므로 정의·일반 Loop·일반 Serving 설명을 줄이고 차이에 장수 배분 |
| Part XII | Sources·검증 기록의 기준 |
| 기본 교재 설치·인증·전체 용어·일반 반도체 도입 체크 | Sources/부록. 이번 2차의 차별적 실행 구조 설명과 직접 관계없는 본문 확장은 피함 |
| 사용자 코멘트 1·2 | CC15의 최신 근거 확인, CC23의 수정 가능한 계층 비교 |

## 8. 작성 순서와 검증 계획

1. **비교표 확정:** 각 장마다 공통 원리, 다른 공개 동작, 공개 코드/설정, 확인 불가한 내부를 나눈다. Hermes와 동등한 기능이 없는지 확인하지 않은 상태에서 기능 부재·독점을 주장하지 않는다.
2. **버전·출처 고정:** 실제 사용할 CLI/OS·실험 옵션을 기록하고 현행 문서·고정 릴리스·공개 부품의 tag/commit을 분리한다. 참고 문서 URL·확인일·로컬 원문의 절을 Sources에 연결한다.
3. **핵심 차이부터 초안 작성:** CC03~07, CC09~14, CC17~20을 먼저 작성한다. 이후 공통 루프 연결과 캐시·예약·종합 비교를 붙여 흐름을 맞춘다.
4. **도식 설계:** 로딩은 시점도, 권한은 분기표, Hook은 입력/결정 JSON, Sandbox는 경계도, Trace는 span 트리, 위임은 Context 전달/메시지 관계도로 표현한다. 비교 항목 사이에는 실행 순서로 보이는 화살표를 넣지 않는다.
5. **코드 예시:** 본문은 읽을 수 있는 짧은 발췌/설정만 싣고, handler 전체·예외표·기본값·출처는 Sources에 둔다. 공식 발췌/사용 예시/논리 의사코드를 표시한다. SDK Transport는 자체 Loop 코드로 소개하지 않는다.
6. **내용 대조:** 원문 Part/W 매핑, 최신 문서와의 차이, Prompt/권한·내용 지속/권한 지속·Context/파일 격리·resume/rollback·metrics/events/spans 구별을 점검한다.
7. **발표 통합:** 현재 어두운 슬레이트 톤과 주제 구분 방식을 유지해 Claude 구간만 교체하고 페이지 번호·목차·Sources·발표자 노트를 갱신한다. Hermes는 현재 내용으로 유지한다.
8. **화면·기능 검수:** 1920×1080, 1280×720, 휴대폰 비례 축소에서 넘침·코드 크기·연결 방향·강조·탐색·Sources를 확인한다. PDF와 전체 순서를 재검증한다.

실행 실험은 현재 하지 않았다. 다음 실제 작성에서 동작 예시 검증이 필요하면 작은 합성 프로젝트로 파일 로딩·Hook 차단/실패·fork 전달·복구 범위를 재현하고, 검증하지 않은 부분은 문서 기준으로 표시한다. 외부 collector 전송·실제 예약·새 Demo 서비스 구축은 자동으로 수행하는 범위가 아니다.

## 9. 공식 자료 목록

| ID | 자료 | 이번 확인 범위 |
|---|---|---|
| D01 | [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | 공통 loop·Tool·Harness 역할 |
| D02 | [Prompt caching](https://code.claude.com/docs/en/prompt-caching) | 계층·변경 영향·캐시/메모리 차이 |
| D03 | [Context window](https://code.claude.com/docs/en/context-window) | 시작 입력·압축 후 재주입 |
| D04 | [Memory](https://code.claude.com/docs/en/memory) | 지침 선택·Rules·Auto Memory |
| D05 | [Sessions](https://code.claude.com/docs/en/sessions) | Session 재개·분기와 외부 파일 상태의 구별 |
| D06 | [MCP](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search) | 지연 명세·기본값·fallback |
| D07 | [Skills](https://code.claude.com/docs/en/skills) | invocation·권한 수명·fork·compaction |
| D08 | [Subagents](https://code.claude.com/docs/en/sub-agents) | 시작 Context·설정·fork·중첩·반환 |
| D09 | [Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference) | 패키징·구성요소와 Mods 구별 |
| D10 | [Permissions](https://code.claude.com/docs/en/permissions) | Rules/Hook/Mod·Plan·관리형 정책 |
| D11 | [Hooks](https://code.claude.com/docs/en/hooks) | 이벤트 계약·결정·오류·onFailure·timeout |
| D12 | [Sandboxing](https://code.claude.com/docs/en/sandboxing) | Bash 적용 경계·제품의 OS 조건 |
| D13 | [Monitoring](https://code.claude.com/docs/en/monitoring-usage) | metrics/events·beta tracing·활성화·상관 ID |
| D14 | [Agent Teams](https://code.claude.com/docs/en/agent-teams) | 공유 작업·통신·기본 off·실험 상태 |
| D15 | [Checkpointing](https://code.claude.com/docs/en/checkpointing) | 파일 추적·rewind·대화/코드 복구 |
| D16 | [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) | Session/Desktop/Cloud·resume 복원 |
| S01 | [Claude Code README @v2.1.314](https://github.com/anthropics/claude-code/blob/v2.1.314/README.md) · [동일 릴리스](https://github.com/anthropics/claude-code/releases/tag/v2.1.314) | 공개 자료 범위·로컬 교재의 기준 릴리스 확인 |
| S02 | [Sandbox Runtime 공식 저장소](https://github.com/anthropics/sandbox-runtime) | 공개 API와 제품 통합 경계. 코드 발췌 전 commit 고정 필요 |
| S03 | [Anthropic Sandbox 기술 글](https://www.anthropic.com/research/claude-code-sandboxing) | 파일·네트워크 격리 설계의 배경. 과거 수치를 이번 환경의 성능으로 사용하지 않음 |
| S04 | [Python SDK subprocess transport @v0.2.174](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.174/src/claude_agent_sdk/_internal/transport/subprocess_cli.py) | 공개 SDK/CLI 경계. SDK 상세는 후속 범위와 분리 |

발표는 전체 105장이다. 시작 장표는 기존 링크를 위해 `CLAUDE`를 ID로 사용하며 `CC00`도 같은 위치로 연결된다. 범주 전환 ID는 `CCA`~`CCE`다. 개정 내용과 발표자 설명은 [생성 코드](../claude_revision.py)에서 관리한다.
