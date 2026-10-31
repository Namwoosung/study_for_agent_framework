# Microsoft Agent Framework — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 차별점 비교. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. 승인된 분석 범위와 최종 실행 범위를 같은 계약으로 묶기

**발표 핵심:** 입력 가공을 재사용할수록 어떤 인자에 정책을 적용했는지 추적해야 한다.

**연결할 원문:** 11.2 인자 변경과 Guardrail 우회 — 원문 409행, [교재의 추가 코멘트](html/deep/unit-05.html#seminar-microsoft-agent-framework-final-arguments)

가상의 조회 범위가 특정 라인·Lot·기간으로 승인됐더라도, 이후 Middleware의 정규화·보정이 범위를 넓히면 형식이 올바른 쿼리도 업무 계약과 어긋날 수 있다. 원문의 정책 이후 인자 변경 문제는 “검사를 붙였는가”보다 “실제로 실행할 값에 검사를 했는가”라는 비교 기준으로 연결된다.

계층별 Middleware는 공통 가공과 정책을 재사용하는 데 유용한 구성이지만 순서와 최종 인자를 이해해야 하는 비용이 있다. 반도체 사례에서는 범위 보정 결과를 승인 화면·실행 기록·실제 Tool 인자와 연결하는 설계를 검토할 수 있다. 이는 별도 적용 제안이며 모든 경로의 안전성이 자동 보장된다는 뜻은 아니다.

**3차 확인 질문:** 라인·Lot·기간의 보정 전후 범위가 달라지면, 어느 값을 검사하고 무엇을 차단하거나 다시 승인받아야 하는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-05.html#line-409) · [S03](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_tools.py) · [S04](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_middleware.py)

## 2. 병렬 분석 결과를 도착 순서보다 업무 키로 합치기

**발표 핵심:** 명시적 Graph가 설명하는 실행 경로와 도메인 근거의 올바른 결합은 별도 계약이다.

**연결할 원문:** 18.3 Superstep 병렬성의 정확한 계약 — 원문 692행, [교재의 추가 코멘트](html/deep/unit-08.html#seminar-microsoft-agent-framework-join-business-key)

가상의 두 Lot을 동시에 조사하면서 계측 요약·설비 이력·SOP 근거를 다른 분기에서 받는다면, 먼저 도착한 결과끼리 묶어서는 분석 대상이 섞일 수 있다. 원문의 Edge별 순서 보존과 서로 다른 Source의 도착순 차이는, 합류에 분석 대상·조회 시점·자료 버전 같은 업무 키가 필요한 이유를 보여 준다.

Executor/Edge를 명시하는 장점은 어떤 근거를 기다리고 어느 지점에서 검증할지 설명하기 쉽다는 데 있다. 반면 어떤 결과 조합이 업무상 유효한지는 Join 쪽의 계약으로 작성해야 한다. 발표에서는 순수 Agent 자유 탐색과의 일반 비교를 반복하기보다, 완료 순서를 바꿔도 같은 Lot의 근거만 합쳐지는 설계가 가능한지에 초점을 둘 수 있다.

**3차 확인 질문:** 분기 완료 순서를 바꾸거나 한 분기를 실패시켜도, 각 보고서에 같은 Lot·시점·버전의 근거만 결합되는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-08.html#line-692) · [S09](https://github.com/microsoft/agent-framework/blob/python-1.24.0/python/packages/core/agent_framework/_workflows/_runner.py)
