# Claude Code — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 차별점 비교. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. 반복 분석의 캐시 효율과 근거 최신성을 별도 축으로 보기

**발표 핵심:** 고정 절차를 재사용하는 경제성과 매 작업의 근거를 갱신하는 정확성은 다른 평가 축이다.

**연결할 원문:** 7.3 캐시 저장 위치도 설계 요소다 — 원문 266행, [교재의 추가 코멘트](html/deep/unit-04.html#seminar-claude-code-procedure-freshness)

여러 Lot에 같은 분석 절차를 적용하더라도 대상 기간·Lot 데이터·적용 SOP 리비전은 달라질 수 있다. Claude Code의 Prefix·Tool Search·압축 조건은 “계속 같은 지침을 사용하는 부분”과 “이번 작업에 필요한 자료를 확인하는 부분”을 나눠 설명할 구체적인 사례다. 캐시 적중을 최신 자료를 확인했다는 증거로 사용하지 않는다.

반도체 분석 저장소에서 고정된 계산·검토 절차를 재사용하는 설계는 반복 설명의 부담을 줄일 여지가 있다. 동시에 결과에 데이터·SOP 버전을 남겨야 재검토가 가능하다. 발표에서는 캐시 통계와 근거 버전의 정확도를 별도로 비교할 질문을 제시하고, Provider별 조건이나 실제 절감량은 원문의 제한을 넘어 단정하지 않는다.

**3차 확인 질문:** 모델·도구·절차를 고정하고 Lot 입력이나 SOP 리비전만 바꾸면, 캐시 통계와 답변의 리비전 인용은 각각 어떻게 달라지는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-04.html#line-266) · [R03](https://code.claude.com/docs/en/prompt-caching)

## 2. 업무 코드를 만드는 일과 실행기를 바꾸는 일을 구별하기

**발표 핵심:** 완성된 코딩 환경의 재사용과 공개 Runtime 내부의 변경 가능성은 서로 다른 장점이다.

**연결할 원문:** 45. Claude Code vs Hermes — 두 완성형 Harness — 원문 1253행, [교재의 추가 코멘트](html/deep/unit-14.html#seminar-claude-code-control-surface)

가상의 반도체 분석용 Python 저장소에서 파서 수정·통계 스크립트 작성·테스트 반복을 맡기는 경우에는 Claude Code가 이미 갖춘 작업 환경을 활용하는 관점으로 볼 수 있다. 반면 “Tool 결과가 특정 형식이면 다음 반복의 분기를 내부에서 바꾸자”는 요구는 실행기 자체를 연구하는 문제다.

Hermes 심층 설명 뒤에는 어느 제품이 더 우수한지보다, 필요한 변경이 업무 코드·지침·Hook·Tool 연결에서 끝나는지, 공개 코어의 수정까지 요구하는지를 대비하면 된다. 이 비교는 Claude Code의 비공개 내부를 확인했다고 주장하지 않으면서도, 재사용 범위와 제어 자유도의 Trade-off를 전달한다.

**3차 확인 질문:** 같은 합성 데이터 분석 과제에서 필요한 변경을 공개 설정·Hook·Tool로 표현할 수 있는가? 내부 Loop 변경을 전제하는 요구는 무엇인가?

**기술 근거:** [원문의 해당 절](html/deep/unit-14.html#line-1253) · [R02](https://code.claude.com/docs/en/how-claude-code-works) · [R24](https://github.com/anthropics/claude-code/blob/v2.1.314/README.md) · [R25](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.174/src/claude_agent_sdk/query.py) · [R27](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.174/src/claude_agent_sdk/_internal/transport/subprocess_cli.py) · [R28](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.174/src/claude_agent_sdk/_internal/query.py)
