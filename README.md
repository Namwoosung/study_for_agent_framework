# Agent Framework 학습과 발표

- [학습 홈](study/index.html) — 기본·심층 교재와 Python 에이전트 실습
- [현재 발표자료](presentations/seminar-2/index.html) · 2차 세미나 146장
- [실제 실행 Demo](demos/README.md) · Hermes와 PydanticAI
- [발표 폴더 안내](presentations/README.md): 현재 설계·참고 자료와 다음 작업
- [아카이브](archive/README.md): 초기안·이전 버전·과거 검토와 검수 결과

```text
study/           공부할 원문과 교재, 학습용 생성·검증 스크립트
presentations/   현재 발표자료와 지금 사용하는 설계·참고 문서
archive/         과거 버전·예시·완료된 이전 계획과 검수 기록
```

루트의 `index.html`에서 학습과 발표로 이동할 수 있습니다. 폴더 전체를 그대로 옮기면 상대 링크를 유지할 수 있습니다.

## 현재 작업

Claude Code는 발표 54~82쪽, PydanticAI는 83~143쪽입니다. PydanticAI에서는 합성 LOT 조회 코드에서 시작해 내부 실행, 출력 검증, 승인과 선택 Harness까지 따라갑니다.

## 다시 생성하고 확인하기

프로젝트 루트에서 실행합니다.

```powershell
node study/html/build-home.mjs
node study/html/validate-home.mjs
node study/html/validate-seminar-comments.mjs
python study/html/validate-layout.py
python presentations/seminar-2/build.py
python presentations/seminar-2/validate-blueprint.py
node presentations/seminar-2/validate.cjs
```

발표의 내용·PDF 검증은 `presentations/seminar-2/verify-content.py`를 사용합니다. PDF 처리 라이브러리가 설치된 Python이 필요하며, 브라우저 검수는 스크립트에 지정된 Playwright/Chrome 경로를 사용합니다.

이전 경로와 이동 내역은 [정리 기록](archive/reorganization-map.json)에 있습니다.
