# 2차 세미나 blueprint 재구성 실행 계획

기준일: 2026-11-03. 산출물은 발표 흐름 문서의 데모 개정과 최종 Markdown blueprint다. 슬라이드 앱과 데모 서비스 구현은 후속 작업이다.

1. **입력 확인**: `0_2차_세미나_발표_흐름.md` 전체와 `agent_framework_seminar_1_slide_blueprint.md` 전체를 읽는다. 내용 범위는 전자, 문서 구조·디자인은 후자를 기준으로 한다. 기존 2차 blueprint·인계서는 현황만 확인하며 내용 원본으로 승격하지 않는다.
2. **데모 계약 개정**: Hermes/PydanticAI 모두 Codex 지시에서는 10000, Antigravity 지시에서는 10001을 사용한다. Agent는 OpenAI-compatible vLLM 인터페이스만 알고, 로컬 별도 프록시만 실제 OpenAI upstream과 API key를 안다. 대상 PC에서도 같은 계약을 사용한다.
3. **추가 코멘트 조사**: 흐름의 질문·검증 요청을 묶어 Hermes의 실제 실행·Context·Memory·Skill·정책과 PydanticAI의 Graph·Tools·병렬·출력·Retry·Hook·Capability·History·Harness·승인·위임을 공식 문서 및 고정 소스로 확인한다. 현행 문서와 고정 버전을 섞지 않는다.
4. **발표 편집**: 도입 → Hermes 심층/데모 → Claude Code 비교 → PydanticAI Core/확장/데모 → 나머지 SDK 순서 → 운영 선택/다음 세미나. 원문에서 미작성인 네 SDK의 기능 설명은 새로 창작하지 않고 짧은 연결 자리만 둔다.
5. **최종 작성**: A 구현 지침, B 슬라이드 명세, C 발표자 해설, D Q&A, E 구현·데모 명세, F 근거, G 검수 구조를 유지한다. 색상·여백·텍스트 위계·도식·노트·키보드·단계 강조를 보존하고 토글·드롭다운·독자 학습용 조작은 순차 강조 또는 정적 병렬 비교로 치환한다.
6. **검수**: 모든 추가 질문을 슬라이드/해설/제작 요구에 매핑한다. 포트/인증 경계, 실제/예시/미검증 구분, 슬라이드 ID, 근거 참조, 문서 링크를 검사한다. 1차 원본과 사용자가 수정 중인 인계서는 보존한다.

완료 기록과 실제 조사 근거는 최종 blueprint F/G 및 `html/seminar-2-blueprint-validation.json`에 남긴다.

## 완료 기록

- 2026-11-03: 발표 흐름의 공통 Demo 계약과 PydanticAI Demo 연결 문구 개정.
- [최종 blueprint](../../../../presentations/seminar-2/docs/blueprint.md): A~G, 본편 42장, 미작성 기술 예약 4개, 질문 대응표·정정표·실제 API 예제·두 Demo/프록시/이관 명세 작성.
- 구조·슬라이드 ID·출처 ID·로컬 링크·Python 코드 문법은 `python html/validate-seminar-2-blueprint.py`로 검사. 실행·렌더링 검증은 이번 산출 범위 밖이며 미완료로 표시.
- 1차 blueprint와 사용자가 수정 중이던 인계서는 변경하지 않았다.
