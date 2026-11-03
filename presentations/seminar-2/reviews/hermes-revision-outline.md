# Hermes 코드 대조 개정 목차

2026-11-03 사용자 요청 반영. 전체 81장, Hermes 본편 6~53페이지(48장). 범주별 메뉴를 없애고 전환 장표로 구분했다. Hermes 소개는 5페이지, Claude Code 시작은 54페이지, PydanticAI 시작은 59페이지다.

| 화면 번호 | ID | 범주 | 제목 |
|---|---|---|---|
| 6 | S04 | Hermes / 전체 흐름 | Hermes 내부 구성과 설명 순서 |
| 7 | S05 | Hermes / 요청 처리 | 사용자 요청 한 건의 실행 과정 |
| 8 | HLOOP | Hermes / 실행 루프 | 루프 한 번이 지나는 실제 함수들 |
| 9 | HTRACE | Hermes / 실행 루프 | 한 요청에서 루프가 세 번 도는 예 |
| 10 | HEXIT | Hermes / 실행 루프 | 중단·예산 소진·오류의 종료 경로 |
| 11 | HCTX | Hermes / 구분 | Context와 기억 |
| 12 | S07 | Hermes / Context와 기억 | 모델 입력과 Session·Memory의 관계 |
| 13 | S10 | Hermes / Context와 기억 | memory Tool은 무엇을 어떻게 저장할까? |
| 14 | HMEM | Hermes / Context와 기억 | Memory 쓰기 승인은 기본으로 켜져 있을까? |
| 15 | S11 | Hermes / Context와 기억 | session_search는 인자에 따라 다르게 동작합니다 |
| 16 | HSEARCH | Hermes / Context와 기억 | 검색어 정리와 범위 확인은 누가 할까? |
| 17 | HTOOL | Hermes / 구분 | Tools와 Skills |
| 18 | S13 | Hermes / Tools와 Skills | Hermes Tool은 이렇게 등록됩니다 |
| 19 | HSCHEMA | Hermes / Tools와 Skills | 모델에게 공개되는 Tool의 실제 수준 |
| 20 | HCONNECT | Hermes / Tools와 Skills | Local Tool·MCP·Plugin은 Hermes 어디에 붙을까? |
| 21 | HVALID | Hermes / Tools와 Skills | validate_tool_calls가 검사하는 순서 |
| 22 | S13A | Hermes / Tools와 Skills | Tool 요청이 실제 실행으로 이어지는 과정 |
| 23 | S13B | Hermes / Tools와 Skills | 실행 전 검사는 실제로 어떤 순서일까? |
| 24 | HHUMAN | Hermes / Tools와 Skills | 어떤 경우에 실제 사용자 승인을 요청할까? |
| 25 | HFAIL | Hermes / Tools와 Skills | 오류·취소가 실제 작업에 남기는 것 |
| 26 | S12 | Hermes / Tools와 Skills | Skills를 찾고 읽는 Hermes의 경로 |
| 27 | HLEARN | Hermes / Tools와 Skills | Hermes는 언제 새 Skill을 만들까? |
| 28 | HWRITE | Hermes / Tools와 Skills | skill_manage의 변경은 어떻게 반영될까? |
| 29 | HCURATOR | Hermes / Tools와 Skills | Curator는 언제 무엇을 정리할까? |
| 30 | HCONSOLIDATE | Hermes / Tools와 Skills | Curator의 LLM 통합은 별도 선택입니다 |
| 31 | HSAFE | Hermes / 구분 | 안전장치와 실행 기록 |
| 32 | HGUARD | Hermes / 안전장치와 실행 기록 | Hermes의 기본 안전장치는 어디에 있을까? |
| 33 | HGUARDFLOW | Hermes / 안전장치와 실행 기록 | 반복되는 Tool 호출을 코드에서 감지하기 |
| 34 | HGUARDCONFIG | Hermes / 안전장치와 실행 기록 | 기본 경고와 강제 중단의 차이 |
| 35 | HHOOK | Hermes / 안전장치와 실행 기록 | 필요한 실행 정책을 Hook으로 추가하기 |
| 36 | HTRACEBASE | Hermes / 안전장치와 실행 기록 | Hermes에 기본으로 남는 기록은 무엇일까? |
| 37 | HOBSERVER | Hermes / 안전장치와 실행 기록 | Observer Hook으로 실행 경계를 연결하기 |
| 38 | HTRACECODE | Hermes / 안전장치와 실행 기록 | 짧은 Plugin으로 API 관측을 시작하기 |
| 39 | HTRACEUSE | Hermes / 안전장치와 실행 기록 | Trace로 무엇을 확인하고 개선할까? |
| 40 | HTRACESHARE | Hermes / 안전장치와 실행 기록 | 실행 대화를 Trace Viewer로 공유하는 경로 |
| 41 | HLONG | Hermes / 구분 | 긴 작업과 위임 |
| 42 | S08 | Hermes / 긴 작업과 위임 | System Prompt를 고정해 Prefix를 재사용하기 |
| 43 | S09 | Hermes / 긴 작업과 위임 | 예시 Context가 압축되는 과정 |
| 44 | S14 | Hermes / 긴 작업과 위임 | Hermes의 병렬 Tool 실행 코드 |
| 45 | S14A | Hermes / 긴 작업과 위임 | delegate_task는 자식을 어떻게 만들까? |
| 46 | HCHILD | Hermes / 긴 작업과 위임 | 자식 실행과 결과 전달의 세부 경로 |
| 47 | HMULTI | Hermes / 긴 작업과 위임 | Hermes는 delegate_task만 사용할까? |
| 48 | HCRON | Hermes / 구분 | 예약 실행과 활용 |
| 49 | S14C | Hermes / 예약 실행과 활용 | Cron으로 예약 작업 실행하기 |
| 50 | HCRONUSE | Hermes / 예약 실행과 활용 | Cron 작업을 만들고 관리하기 |
| 51 | HCRONTRADE | Hermes / 예약 실행과 활용 | Cron은 언제 유용하고 무엇을 주의할까? |
| 52 | HCOMMAND | Hermes / 예약 실행과 활용 | 구조를 알고 쓰면 유용한 Hermes 명령 |
| 53 | S15 | Hermes / Demo | Hermes Demo |

## 근거와 정정

공식 Hermes `v0.22.5`의 코드·기본 설정·같은 태그의 문서를 대조했다. [근거 목록](../research/hermes-v0.22.5-evidence.json)에는 URL·라인·SHA-256·발췌가 있다. [검토 기록](hermes-code-review.md)을 함께 참고한다.

로컬 [기초 학습자료](../../../study/hermes/Hermes_Agent.md), [심층 학습자료](../../../study/hermes/Hermes_Agent_2%EC%B0%A8_%EC%8B%AC%EC%B8%B5_%ED%95%99%EC%8A%B5_%EB%B6%84%EC%84%9D.md), [추가 코멘트](../../../study/hermes/Hermes_Agent_%EB%B0%9C%ED%91%9C_%EC%8B%A4%EB%AC%B4_%EC%8B%9C%EC%82%AC%EC%A0%90_%EC%BD%94%EB%A9%98%ED%8A%B8.md), [이전 미포함 검토](../../../archive/presentations/seminar-2/reviews/hermes-coverage-audit.md)는 개념과 학습 범위의 기준으로 사용했다. 버전별 세부 동작은 이번 고정 소스 확인이 우선한다.

원 blueprint는 보존했고 `hermes_deep.py`가 최종 개정 순서와 내용을 생성한다. 기존 S06은 S05에 통합, Gateway 상세 S14B는 사용자 요청으로 제외했다. Sources와 발표자 노트는 현재 장표 기준이며 원 blueprint의 보존된 부록은 이전 ID를 사용할 수 있다.
