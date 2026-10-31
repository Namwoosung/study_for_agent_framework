# OpenAI Agents SDK — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 차별점 비교. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. 정형 조회 결과에 후속 모델 해석이 필요한지 판단하기

**발표 핵심:** Tool 결과를 그대로 최종화할지, 여러 근거를 모델이 종합할지에 따라 실행 정책을 고른다.

**연결할 원문:** 15. Tool 결과로 종료할 수도 있다: tool_use_behavior — 원문 432행, [교재의 추가 코멘트](html/deep/unit-05.html#seminar-openai-agents-sdk-tool-finalization)

가상의 수율 조회에서 승인된 계산 Tool이 요청한 정형 결과를 이미 반환했다면, 다시 모델에 문장으로 바꾸게 하는 단계가 필요한지 물을 수 있다. tool_use_behavior는 이런 최종화 선택을 설명할 구체적인 비교 지점이다. 모델의 재서술 과정 없이 계산 결과를 전달하는 경로를 검토할 수 있지만, 실제 비용·지연 개선량을 측정한 것은 아니다.

반대로 원인 가설, 서로 다른 문서의 근거, 불확실성을 함께 설명해야 하는 분석 보고서라면 정형 결과 한 개만 돌려주는 정책은 요구를 충족하지 못할 수 있다. “조회 API형 업무”와 “근거 종합형 업무”를 구분하면 경량 Runner를 어떤 역할에 활용할지 설명하기 쉽다. 결과의 도메인 검증과 오류 처리는 어느 경로에서도 별도 계약이다.

**3차 확인 질문:** 계산 결과 조회와 해석 보고서 생성을 서로 다른 과제로 두면, 후속 모델 호출이 실제로 가치를 더하는 경우는 어디인가?

**기술 근거:** [원문의 해당 절](html/deep/unit-05.html#line-432) · [D09](https://openai.github.io/openai-agents-python/tools/) · [S15](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/agent.py)

## 2. 전문가에게 묻는 것과 답변 책임을 넘기는 것을 나누기

**발표 핵심:** 협업 방식의 선택 기준은 Agent 수보다 최종 답변과 후속 질의의 책임이다.

**연결할 원문:** 22. Handoff와 Agent as Tool은 근본적으로 다르다 — 원문 575행, [교재의 추가 코멘트](html/deep/unit-07.html#seminar-openai-agents-sdk-answer-ownership)

가상의 설비 이상 조사에서 주 담당 Agent가 통계 전문가의 결과를 받아 최종 보고서를 작성한다면 Agent-as-Tool과 연결해 설명할 수 있다. 이후의 질문도 특정 전문가가 맡도록 담당을 바꾸려는 목적이라면 Handoff가 비교 대상이 된다. 같은 “전문가 연결” 요구도 원하는 대화 구조에 따라 달라진다.

이 구분은 보고서 한 장의 책임을 모으려는 업무와 전문가 상담을 이어가려는 업무를 나누는 데 유용하다. 다만 역할 분리가 필요 없는 고정 계산이라면 별도 Agent 대신 일반 Tool로 표현할 수 있는지도 확인한다. 역할을 늘리는 장점과 근거를 다시 합치는 비용을 함께 설명해야 한다.

**3차 확인 질문:** 통계 결과만 돌아와야 하는 경우와 통계 담당이 대화를 이어가야 하는 경우에, History 전달 범위와 최종 보고 책임이 어떻게 달라지는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-07.html#line-575) · [D06](https://openai.github.io/openai-agents-python/multi_agent/) · [D07](https://openai.github.io/openai-agents-python/handoffs/) · [S14](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/handoffs.py) · [S15](https://github.com/openai/openai-agents-python/blob/v0.24.0/src/agents/agent.py)
