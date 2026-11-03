# 2차 세미나 — 도식 중심 5장 예시

[발표자료 열기](index.html) · [정적 PDF](five-slide-examples.pdf)

`index.html`을 브라우저에서 열면 됩니다. 설치나 API key가 필요 없으며 폰트·CSS·SVG·JavaScript가 모두 내장되어 오프라인에서도 동작합니다. 기존 교재/blueprint와 분리한 예시입니다.

| 예시 | 원본 ID | 표현 |
|---|---|---|
| 1 | S04 | Hermes 전체 아키텍처와 실행·저장 경계 |
| 2 | S07 | 고정 Prompt snapshot과 호출별 정보 합류 |
| 3 | S14 | 병렬 Tool / 독립 Child Agent의 좌우 비교 |
| 4 | S23 | PydanticAI 노드와 Tool/Output/Retry 흐름 |
| 5 | S28 | 같은 응답에 대한 EndStrategy 실행 비교 |

기준: 루트 `2_2차_세미나_최종_slide_blueprint.md`. 1차의 다크 배경·역할 색·16:9 stage·여백·제목/본문 위계를 유지했습니다. 실동작 Demo가 아닌 발표용 구조도/조건부 예시입니다.

## 조작

- `←` / `→` / `Space`: 설명 경로 단계별 강조. 마지막 단계 이후 다음 장.
- `PageUp` / `PageDown`: 장 단위 이동.
- `1`–`5`: 해당 장으로 바로 이동. 아래 번호 버튼도 동일.
- `N` / `Sources`: 별도 발표자 노트·출처 창. 공유하는 청중 화면에는 노트를 표시하지 않습니다.
- `F`: 전체 화면. `Escape`: 전체 화면/발표자 노트 닫기.
- 터치 좌우 스와이프와 마우스 휠도 단계 이동을 지원합니다.

도식 전체는 처음부터 보이고 단계는 강조만 바꿉니다. PDF는 강조/키보드 조작이 없는 5장 정적 버전입니다. 모바일에서는 같은 16:9 stage를 비례 축소합니다.

## 검증·수정

1920×1080 고정 stage, 1280×720/390×844에서 overflow·텍스트 겹침, 방향키 build·번호 jump·장 이동·노트 분리·Reduced motion·PDF를 확인했습니다. 결과는 `validation.json`, 화면은 `screenshots/`입니다. 실제 Agent나 모델 API는 호출하지 않습니다.

수정 원본은 `build.py`입니다. `python html/seminar-2-examples/build.py`로 HTML/manifest를 다시 생성합니다. 폰트 자산이 없으면 최초 생성 시 Google Fonts 저장소에서 내려받습니다. `qa.cjs`는 현재 PC의 번들 Playwright/Chrome 경로를 사용하는 검수 스크립트입니다.

폰트: Nanum Gothic (Google Fonts), SIL Open Font License. `assets/OFL.txt`와 HTML 내부에도 라이선스를 포함했습니다.
