# Agent Framework 2차 세미나 — 전체 발표자료

[발표용 HTML](index.html) · [81페이지 PDF](agent-framework-seminar-2.pdf) · [발표자 노트](presenter-notes.md)

기준 blueprint와 로컬 학습자료를 바탕으로 기존 청회색 테마를 유지했습니다. 후속 요청에 따라 Hermes를 공식 `v0.22.5` 코드와 대조해 확장했습니다. 본편은 **81장**, Hermes는 **6~53페이지 48장**입니다. S39~S42의 미작성 SDK 예약 항목은 청중 목차·PDF에서 제외합니다.

## 이번 개정

- 반복 범주 메뉴를 없애고 Context·기억 / Tools·Skills / 안전장치·실행 기록 / 긴 작업·위임 / 예약·활용 전환 장표를 넣었습니다.
- Hermes·Claude Code·PydanticAI 시작을 명시적으로 구분했습니다. Hermes·PydanticAI는 공식 SVG를 내장했고, Claude Code는 글자 중심 구분 장표입니다.
- 루프 함수·반복/종료, 입력 구성·Memory 쓰기/승인·Session 검색, Tool 등록/노출/검증/승인, Skill 작성/승인/Curator, 병렬 실행·위임·다중 실행, Cron 사용법과 활용 명령을 설명합니다.
- 2페이지는 단계 진행을 없앴고, Gateway 상세 장표는 삭제했습니다. Claude Code 마지막 장은 구조와 연결되는 명령 활용으로 개정했습니다.
- 본문의 짧은 코드와 가상 예시는 축약·예시임을 표시하고 각 장의 Sources에 상세 분기·기본값·출처를 정리했습니다.

[현재 목차](reviews/hermes-revision-outline.md) · [요청 반영·근거 검토](reviews/hermes-code-review.md) · [공식 코드 대조 기록](research/hermes-v0.22.5-evidence.json)

## 실행

`index.html`을 브라우저로 열면 됩니다. HTML 하나에 폰트·CSS·SVG·JavaScript·발표자 자료가 내장되어 있어 설치·인터넷·API key 없이 실행됩니다. 공유할 때 HTML 한 파일만 전달해도 발표 기능이 동작합니다. 별도 Demo 안내 페이지도 함께 쓸 경우 이 폴더를 통째로 전달합니다.

| 조작 | 동작 |
|---|---|
| `→` / `Space` | 강조 단계 진행, 마지막 단계 뒤 다음 장 |
| `←` | 단계 역순, 첫 단계에서 이전 장 마지막 단계 |
| `PageDown` / `PageUp` | 장 단위 이동 |
| `G` | 하단 번호 입력에 포커스. 1–81 입력 후 Enter |
| `T` / 목차 | 전체 본편 목록에서 바로 이동 |
| `Home` / `End` | 첫 장 / 마지막 장 |
| Sources | 현재 장의 개념·설명·참고 자료 |
| `N` | 별도 발표자 노트 창 |
| `F` / `Escape` | 전체 화면 / 닫기 |
| 터치 스와이프 / 휠 | 단계 이동 |

전체 도식은 처음부터 보이며 조작은 설명할 경로를 강조합니다. 3장의 발표자 이름은 Space로 위에서부터 차례로 나타나고, 4장은 Space 한 번으로 Hermes와 PydanticAI를 동시에 강조합니다. Sources에서는 81장 각각의 개념 정의와 설명을 읽고 Escape로 돌아올 수 있습니다. 노트 창은 화면 공유 대상에서 제외하세요. 노트 창에는 현재 슬라이드 대본·상세 해설·Q&A·근거/정정·데모 명세·SDK 예약 내용을 넣었으며 그 창에서도 발표 단계를 제어할 수 있습니다.

16:9 1920×1080 stage를 통째로 비례 축소합니다. 모바일에서도 도식 배치를 바꾸지 않습니다. PDF는 강조 조작·별도 노트·Demo 링크 UI가 없는 정적 81장 버전입니다.

## 실제 Demo 상태

S15/S38의 링크는 `demo-handoff.html`로 이동합니다. **실제 Hermes/PydanticAI 실행 서비스는 연결되어 있지 않습니다.** 안내 페이지는 이를 명시하고 관찰할 지점과 원래 슬라이드 복귀 링크를 제공합니다. 가짜 Trace나 모델 결과를 생성하지 않습니다.

이 발표 HTML은 모델 프록시 포트에 요청하지 않습니다. 실동작 Demo/프록시는 blueprint E에 따라 별도 제작해야 합니다. Codex 지시의 두 Demo는 10000, Antigravity 지시의 두 Demo는 10001이라는 계약을 유지합니다.

## 수정·재생성

```powershell
# 프로젝트 루트에서
python presentations/seminar-2/build.py
```

- `build.py`: 81장 화면·도식과 blueprint의 발표자 내용 매핑.
- `artwork.py`: 5장 예시에서 확정한 도형·스타일과 재사용 도식. 이 폴더 자체 자산만 사용합니다.
- `revision.py`: 문구·도입/소개 도식·개념 해설. 원 blueprint의 노트는 originalSpec으로 보관.
- `hermes_revision.py`: 이전 16장 개정의 기본 도식·자료 매핑.
- `hermes_deep.py`: 최종 48장 Hermes 구성·코드 대조·상세 해설·대주제 구분 장표.
- `research/`: 고정 소스 URL·해시·발췌·MIT 라이선스와 공식 이미지 출처.
- `hermes_observability.py`: 가드레일·기본 설정·정책 Hook·관측 이벤트·Trace 활용과 내보내기.
- `design.py`: 청회색 테마·도식 재배치·연결선·강조 디자인. 내용은 유지.
- `assets/Pretendard-*`: 내장 글꼴과 SIL OFL 라이선스.
- `controller.js`: 단계 이동·목차·발표자 창·고정 stage 제어.
- `assets/`: 로컬 폰트·SIL OFL·viewport base CSS.
- `notes.json` / `presenter-notes.md`: 생성된 발표자 자료.
- `manifest.json`: 원본 blueprint hash, 본편 ID·출처·build 수, 예약·Demo 상태.

외부 라이브러리는 발표 실행에 필요하지 않습니다. 브라우저 검수 스크립트 `validate.cjs`는 이 PC의 번들 Playwright/Chrome 경로를 사용하며, 다른 PC에서는 해당 경로를 맞춰야 합니다.

## 확인한 범위

- 본편 81장 및 S38→S43 연결, blueprint SHA-256·원문 명세 보존, Claude 활용 명령 개정의 출처 교체.
- 1920×1080, 1280×720, 390×844의 stage 비율·viewport 범위·텍스트 넘침/겹침.
- 모든 build 정방향·역방향, 번호 이동·목차·예약 제외·노트 분리/제어.
- 두 Demo 안내의 미연결 표기·복귀 링크, 원격 자동 요청 없음.
- 모든 장 렌더링 화면 검토, PDF 81페이지 확인.

결과는 `validation/report.json`, 화면은 `validation/revision-screenshots/`에 있습니다. 내용 검증은 blueprint·로컬 학습자료와 공식 고정 소스 대조입니다. 실제 Hermes/PydanticAI 패키지·모델·프록시 실행이나 성능 측정은 포함하지 않습니다.

## 정리된 경로

발표 HTML·PDF·생성 코드는 이 폴더에 있습니다. 현재 기준 문서는 `docs/blueprint.md`, 발표 흐름은 `docs/flow.md`, 데모 계획은 `docs/demo-plan.md`입니다. 이전 계획과 예시는 `../../archive/presentations/`에 보관합니다. 학습 원문은 `../../study/`에서 확인합니다.
