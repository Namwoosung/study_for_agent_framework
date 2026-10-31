# Google ADK — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 차별점 비교. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. 분석가의 답변 완료와 업무 완료를 구분하기

**발표 핵심:** 중간 결과를 먼저 보여 주려면 최종 보고 가능한 상태를 별도로 정의해야 한다.

**연결할 원문:** 15. Event.is_final_response()의 정밀한 정의 — 원문 489행, [교재의 추가 코멘트](html/deep/unit-07.html#seminar-google-adk-business-completion)

가상의 설비 로그 분석 Agent가 원인 후보를 답했어도, 다른 분석의 계산 검증이나 SOP 근거 확인은 남아 있을 수 있다. 원문의 final Event 범위를 이런 업무에 대입하면 “담당자의 응답이 끝남”과 “보고서가 검토 가능한 상태임”을 같은 완료 표시로 처리할지 질문하게 된다.

Event 중심 구조는 단계별 결과를 관찰하고 사용자에게 진행 상태를 나눠 보여 줄 설계 여지를 제공한다. 그 대신 근거·계산·검토 중 어떤 조건이 충족돼야 최종 보고서를 만들지 애플리케이션이 정해야 한다. 발표에서는 일반 Streaming 정의 대신 이 완료 계약을 비교 지점으로 삼을 수 있다.

**3차 확인 질문:** 원인 후보가 먼저 도착하고 계산 검증이 늦게 끝나면, 화면의 중간 상태와 최종 보고 상태를 어떻게 구분할 것인가?

**기술 근거:** [원문의 해당 절](html/deep/unit-07.html#line-489) · [S07](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/events/event.py)

## 2. 대화 기록과 분석 근거를 연결하되 같은 저장물로 취급하지 않기

**발표 핵심:** 대화를 다시 읽는 능력과 당시 자료로 결론을 재검토하는 능력은 다르다.

**연결할 원문:** 17. State / Memory / Artifact / Context의 정확한 차이 — 원문 544행, [교재의 추가 코멘트](html/deep/unit-07.html#seminar-google-adk-evidence-contract)

가상의 수율 이상 분석에서 Session/Event에는 실행 연결 정보를, 입력 데이터 스냅샷·통계 산출물·참고 SOP에는 식별 가능한 Artifact 또는 외부 자료 참조를 두는 설계를 생각할 수 있다. ADK가 구분한 서비스 경계를 업무 자료의 수명에 대응시켜 보는 해석이다.

이렇게 나누면 대화 Context를 모든 원본 파일로 채우지 않고 필요한 자료를 연결하며, 같은 분석의 근거를 다시 찾기 쉬운 구조를 검토할 수 있다. 다만 Artifact 사용 자체가 재현성을 보장하지는 않는다. 자료 버전·보존·접근권한과 Event의 참조가 일치해야 하며, 그 계약은 도메인 앱에서 정한다.

**3차 확인 질문:** 같은 보고서를 재검토할 때 당시 데이터 스냅샷·SOP 리비전·계산 결과를 어떤 ID 조합으로 되찾을 수 있는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-07.html#line-544) · [S08](https://github.com/google/adk-python/blob/v2.13.0/src/google/adk/sessions/base_session_service.py) · [D03](https://adk.dev/sessions/state/) · [D04](https://adk.dev/sessions/memory/)
