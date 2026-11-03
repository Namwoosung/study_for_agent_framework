# Hermes 상세 개선 — 요청 반영과 코드 대조

2026-11-03. 화면 번호는 이번 개정 이후이며, 사용자가 지칭한 페이지는 이전 47장 버전 기준이다. 최종 발표자료는 81장이고 Hermes 본편은 6~53페이지다.

## 요청별 반영

| 요청 | 반영 위치 / 처리 |
|---|---|
| 매 장의 여섯 범주 메뉴 제거 | 메뉴 DOM/CSS 삭제. HCTX·HTOOL·HSAFE·HLONG·HCRON 전환 장표와 작은 상단 section label 사용 |
| 대주제 구분·공식 이미지 | 5페이지 Hermes(S03H), 54페이지 Claude Code, 59페이지 PydanticAI. Hermes/PydanticAI 공식 SVG 내장. Claude는 타이포그래피 사용 |
| 이전 2페이지 step 제거 | S01의 build 수 0. Space는 다음 장으로 이동 |
| 이전 6페이지와 이후 내용 정합성 | S04를 실제 뒤의 다섯 설명 범주와 일치하는 목차로 교체 |
| 루프 내부·반복 예·종료 처리 | S05 → HLOOP → HTRACE → HEXIT. 실제 함수, 논리 반복/내부 retry 구별, 3회 예시, 중단·grace·consume·예외 handler 제시 |
| Context와 기억을 Tools 앞으로 | HCTX → S07 → S10 → HMEM → S11 → HSEARCH. System/History/호출별 정보/tools/Provider, Memory 파일·쓰기 정책·세션 검색 |
| Hermes 특화 Tool 등록·공개·연결·검증 | S13/HSCHEMA/HCONNECT/HVALID. 실제 skills_list 등록·schema, Native/MCP/Plugin/Inline 차이, ID·이름·JSON 검사 |
| 실행 전 검사·사용자 승인 | S13A/S13B/HHUMAN/HFAIL. 정본 기록, terminal guard의 조건 순서, smart/manual·무인 정책, 실행 후 실패 |
| Memory 쓰기·기본값·검색어 정리와 범위 | S10/HMEM/S11/HSEARCH. MemoryStore, 두 파일·문자 한도·write_approval, 검색 모드·FTS 문법 정리·role/source/session-start 필터 |
| Skill을 Tools와 묶고 자체 수정 확대 | S12/HLEARN/HWRITE/HCURATOR/HCONSOLIDATE. 읽기, 모델 판단과 nudge, operations 기반 파일 변경·승인·ledger, 결정적 Curator와 opt-in LLM 통합 |
| Prefix에 System Prompt 명시 | S08. 예시 수치 표기 유지, 추론 서비스의 cache 판단과 구분 |
| 압축을 예시 Context로 설명 | S09. 가상 Before → 큰 과거 Tool 본문 축소 → Summary+보호 Tail. 실측 아님 명시 |
| 병렬 실행 실제 코드 | S14. executor.submit + context 전파, segment planner, 원래 index 결과 저장 |
| delegate_task 세부 로직·다른 방식 여부 | S14A/HCHILD/HMULTI. 인자·자식 구성·배치 dispatch·결과 schema, background handle, MoA/ Kanban 비교 |
| 이전 19페이지 제외 | S14B Gateway 장표 삭제 |
| Cron 사용법·장단점 | S14C/HCRONUSE/HCRONTRADE. slash/CLI/Tool 구분, fresh session·실행 Claim·외부 효과·전달, 무인 정책과 비용 |
| 구조와 연결되는 활용 명령 | HCOMMAND와 S19. Hermes /new·/learn·/skills diff, Claude /context·/compact·/permissions·/rewind |

| 추가 요청: 가드레일·트레이스의 기본 구성·로직·활용 | HSAFE/HGUARD/HGUARDFLOW/HGUARDCONFIG/HHOOK/HTRACEBASE/HOBSERVER/HTRACECODE/HTRACEUSE/HTRACESHARE. 총 10장 추가 |

## 확인한 사실과 기존 자료의 정정

공식 저장소 태그 **v0.22.5**, tree SHA **bf0203a794a07aac3ff764972ab9087baa4e4f4e**를 확인했다. [근거 JSON](../research/hermes-v0.22.5-evidence.json)에 원본 경로·라인·URL·SHA-256·발췌를 보관했다. 코드의 배포 라이선스는 [MIT](../research/Hermes-source-LICENSE.txt)다.

- 부모 기본 반복 제한을 500, 자식을 50으로 고정하지 않았다. 확인한 DEFAULT_CONFIG의 agent.max_turns는 null, delegation.max_iterations는 250이다. 논리 반복 카운터와 실제 HTTP 요청 수는 retry/preflight 등의 이유로 다르다.
- Memory와 Skills의 write_approval 기본은 false다. true인 경우에도 Memory 대화형 inline 승인과 Skill의 pending stage는 다르다. 기능 활성화·내용 검증·사용자 승인을 구분했다.
- session_search의 role_filter는 쉼표 구분 문자열이며, session_id는 단순 discovery 필터가 아니라 read/scroll 경로를 선택한다. 검색어 의미는 모델이 선택하고 Python sanitizer는 FTS 문법을 정리한다.
- skill_manage의 모델 공개 인자는 operations 배열이다. patch의 부분 치환 인자는 old_string/new_string이며, 레거시 flat action/name 지원을 현재 공개 계약처럼 제시하지 않았다. batch의 원자적 rollback, 지원 파일과 delete 단독 operation 제약을 Sources에 설명했다.
- 기본 Curator는 LLM 없는 미사용 정리다. enabled=true, interval=168h, idle=2h, stale=14일, archive=30일이며 consolidate=false, prune_builtins=false다. 최초 관찰 시각 초기화와 pin/Cron 참조·Hub 제외 조건을 구분했다.
- System snapshot은 파일 쓰기 즉시 교체되는 것은 아니지만 새 세션뿐 아니라 명시 갱신·압축 재빌드 경계에서 다시 읽힐 수 있다. pinned auto_load·프로젝트/호출자 지침·Memory·Plugin 등 조건부 입력도 포함했다.
- 모든 Tool이 terminal approval의 단일 경로를 지나는 것은 아니다. Inline 도구·파일·MCP·Plugin의 별도 경로와 명령의 smart guardian을 구분했다.
- delegate_task 외에도 고정 공식 문서에서 MoA와 Kanban을 확인했다. 세 방식을 한 연속 실행 파이프라인으로 그리지 않고 비교했다.

추가 대조에서 pre_tool_call 정책 Hook은 예외·timeout에 fail-closed, 일반 관측 Hook은 실패 시 건너뛰는 차이를 확인했다. 문서의 일반 fail-open 문구를 일괄 적용하지 않았다. api_request_id는 논리 반복에서 생성되어 내부 retry가 재사용할 수 있다. Trace export JSONL의 timestamp는 내보내기 시각이며 실제 API span 지연의 근거가 아니다. Session/로그/Observer/외부 export와 내용 없는 Gateway health OTLP를 구분했다.

Claude Code 활용 명령은 [Commands](https://code.claude.com/docs/en/commands)와 [Checkpointing](https://code.claude.com/docs/en/checkpointing) 공개 문서를 확인했다. 비공개 내부 엔진 코드를 분석했다는 의미는 아니다.

## 검증 범위

- 81장 × 세 화면 크기: 1920×1080, 1280×720, 390×844. 고정 16:9·넘침·텍스트 겹침·헤더 침범 확인.
- 모든 build의 정방향/역방향, 목차·번호 이동·Sources·발표자 창·예약 장 제외·Demo 복귀 확인.
- 본문 코드의 공식 발췌/축약/의사코드/가상 Tool 인자/가상 Context를 구분. source hash와 URL로 재확인 가능.
- PDF 81페이지·빈 페이지 없음, 원 blueprint 명세 보존과 개정 대상 외 본문 대조.

실제 Hermes/PydanticAI 실행, 모델·프록시 호출, Memory/Skill 파일 변경, Cron 예약, 병렬 성능 측정은 하지 않았다. Demo 링크는 기존의 미연결 안내 상태다. 발표자료의 가상 예시는 실행 Trace로 표시하지 않았다.
