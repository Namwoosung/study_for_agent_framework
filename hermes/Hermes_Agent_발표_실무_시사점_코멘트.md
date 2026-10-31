# Hermes Agent — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 집중 설명. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. Memory 스냅샷의 안정성을 업무 자료의 최신성과 분리하기

**발표 핵심:** 같은 분석 안에서는 근거를 고정하고, 새 분석에서는 유효한 버전을 다시 선택한다.

**연결할 원문:** 8.2 핵심: 세션 중 기록해도 System Prompt는 즉시 바뀌지 않는다 — 원문 497행, [교재의 추가 코멘트](html/deep/unit-07.html#seminar-hermes-memory-revision)

가상의 공정 이상 조사에서 개인 선호나 보고서 형식은 Memory 재사용 대상으로 볼 수 있지만, 적용 SOP의 유효 리비전과 현재 Lot의 측정값은 분석 요청별로 선택할 근거다. Frozen Snapshot의 장점인 문맥·Prefix 안정성을 업무 지식의 최신성 보장으로 해석하면 두 요구가 뒤섞인다.

업무 설계에서는 분석 시작 시 데이터 스냅샷과 SOP 리비전을 기록하는 방안을 검토할 수 있다. 조사 도중 SOP가 바뀌면 조용히 새 문장을 섞기보다, 기존 분석을 유지할지 중단하고 새 근거로 시작할지 결정한다. 이렇게 하면 재현성을 설명하기 쉬워지는 대신, 자료 변경을 감지하고 새 분석과 연결하는 책임이 생긴다.

**3차 확인 질문:** 같은 질문에서 SOP 리비전만 바꿨을 때, 답변이 사용한 버전과 분석 이력을 구분해 남길 수 있는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-07.html#line-497) · [S12](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/memory_tool.py) · [D03](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly) · [D10](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)

## 2. FTS의 적합성은 도메인 질의로 판단하기

**발표 핵심:** 검색 기술 이름보다 필요한 근거를 찾는 질의의 성격을 먼저 비교한다.

**연결할 원문:** 9.2 FTS5는 어느 수준의 검색인가? — 원문 595행, [교재의 추가 코멘트](html/deep/unit-08.html#seminar-hermes-retrieval-evaluation)

가상의 설비 로그 검색에는 정확한 장비 식별자·알람 코드로 찾는 질의와, “진공이 불안정했던 비슷한 사례”처럼 표현이 달라지는 질의가 함께 있을 수 있다. Hermes의 기본 세션 검색을 평가할 때 두 질의 집합을 나누면, 로컬 대화 검색의 단순함을 활용할 범위와 별도 도메인 검색이 필요한 범위를 설명하기 쉽다.

발표에서는 FTS와 벡터 검색의 일반 정의를 다시 설명하기보다, 동일한 근거를 정확 코드와 자연어 표현으로 각각 찾아보는 비교 과제를 제시할 수 있다. 코드가 같아도 다른 설비·다른 기간의 기록이면 업무상 정답이 아닐 수 있으므로 검색 성공은 근거의 대상·시점 일치까지 포함해 판단한다. 검색 방식 추가 여부는 이 과제의 누락·오탐을 확인한 뒤 검토할 선택이다.

**3차 확인 질문:** 합성 로그에서 코드가 정확한 질의와 표현이 바뀐 질의의 근거 누락은 어디에서 발생하는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-08.html#line-595) · [S14](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_state_fts.py) · [D05](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage)

## 3. Agent 운영 자원을 모델 서버 자원과 별도로 보기

**발표 핵심:** 완성형 Harness를 사용해도 실행·세션·모델의 자원 수명은 따로 관찰해야 한다.

**연결할 원문:** 15.3 Hermes의 세션 쓰기 소유권 — 원문 1191행, [교재의 추가 코멘트](html/deep/unit-14.html#seminar-hermes-runtime-resources)

여러 엔지니어가 가상의 로그 분석을 동시에 요청하는 상황에서는 모델 호출 대기, Tool 실행, 승인 대기, Session 기록이 서로 다른 시간과 자원을 점유할 수 있다. Gateway의 세션 소유권을 학습하는 이유는 API 주소를 외우기보다, 같은 분석에 두 요청이 들어왔을 때 누가 순서를 결정하는지 설명하기 위해서다.

2차 발표에서는 “클라이언트 → Gateway/Agent 실행 → Tool·저장소 / 모델 엔드포인트”의 책임 배치까지만 제시해도 운영 시사점이 생긴다. 필요한 GPU 수나 Worker 수를 이 구조만 보고 정할 수는 없다. 3차에서는 활성 실행·도구 실행·승인 대기를 나눠 관찰해, 어떤 대기를 실행 슬롯에서 분리할지와 취소 후 남는 작업을 판단하는 과제로 확장할 수 있다.

**3차 확인 질문:** 동일 Session에 추가 요청을 보내거나 승인 대기를 섞으면, 대기열·실행 시간·모델 호출량이 각각 어떻게 달라지는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-14.html#line-1191) · [D05](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage) · [D08](https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration)
