# Claude Agent SDK — 발표·실무 시사점 코멘트

> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.
> 발표 위치: 차별점 비교. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.

[2차 발표 흐름](../2%EC%B0%A8_%EC%84%B8%EB%AF%B8%EB%82%98_%EB%B0%9C%ED%91%9C_%ED%9D%90%EB%A6%84.md) · [1차 발표 범위](../agent_framework_seminar_1_slide_blueprint.md)

## 1. 도메인 함수를 어느 실행기에 연결하는지 비교하기

**발표 핵심:** 같은 Python 업무 함수라도 호출·오류·자원 정리가 지나가는 경계는 다를 수 있다.

**연결할 원문:** 14.1 외부 MCP와 SDK-hosted MCP — 원문 332행, [교재의 추가 코멘트](html/deep/unit-05.html#seminar-claude-agent-sdk-domain-tool-boundary)

기존의 합성 수율 집계 함수를 연결한다고 가정하면, PydanticAI의 Python 실행 흐름에서 Tool을 호출하는 방식과 Claude Agent SDK의 CLI가 SDK-hosted MCP를 통해 Python Handler에 요청하는 방식은 다른 통합 경로다. 후자는 Claude Code 실행 능력을 앱에서 재사용하면서 도메인 기능을 붙이는 관점으로 설명할 수 있다.

장점은 업무 기능의 Python 구현을 유지하면서 Harness의 작업 능력을 활용할 여지가 있다는 점이다. 대신 메시지 직렬화·콜백 수명·연결 종료라는 경계를 고려해야 한다. 비교의 기준을 예제 코드 줄 수에서 입력·결과·오류가 어느 프로세스와 프로토콜을 거치는지로 바꾸면 두 SDK의 성격이 분명해진다.

**3차 확인 질문:** 같은 합성 집계 함수의 성공·인자 오류·취소 결과가 두 통합 방식에서 어떤 실행 경로로 전달되는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-05.html#line-332) · [C05](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/query.py) · [D07](https://code.claude.com/docs/en/agent-sdk/custom-tools)

## 2. 대화 이동성과 분석 파일의 재현성을 나눠 설계하기

**발표 핵심:** 다른 Worker에서 대화를 이어가는 것과 같은 분석 자료를 되찾는 것은 별도 요구다.

**연결할 원문:** 21.3 File Checkpointing과 외부 SessionStore의 충돌 — 원문 584행, [교재의 추가 코멘트](html/deep/unit-07.html#seminar-claude-agent-sdk-analysis-portability)

가상의 분석 작업에서 Transcript와 생성 CSV·그래프·중간 통계 파일을 하나의 Session 저장 기능으로 생각하면 복원 범위를 오해하기 쉽다. 원문의 로컬 기록 후 외부 mirror, 임시 materialization, File Checkpointing 조합 제약은 이 차이를 설명하는 제품별 사례다.

외부 SessionStore는 대화 기록을 다른 실행 환경에 연결하는 기능으로 검토할 수 있다. 분석을 재검토하려면 입력 데이터·코드 버전·산출물 위치와 무결성 정보를 어떤 작업 ID로 묶을지도 별도로 정해야 한다. 이 식별자 설계는 제안이며 SDK가 같은 필드를 기본 제공한다는 뜻은 아니다. 2차에는 보관 범위의 차이만 짚고 실제 복원은 3차 과제로 남긴다.

**3차 확인 질문:** 다른 실행 환경에서 대화를 복원했을 때 원본 데이터·중간 파일·최종 보고서 중 무엇을 별도로 제공해야 분석을 이어갈 수 있는가?

**기술 근거:** [원문의 해당 절](html/deep/unit-07.html#line-584) · [D06](https://code.claude.com/docs/en/agent-sdk/session-storage) · [C09](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/session_resume.py) · [C10](https://github.com/anthropics/claude-agent-sdk-python/blob/v0.2.176/src/claude_agent_sdk/_internal/session_store_validation.py)
