# Claude Agent SDK 학습 페이지

`index.html`을 브라우저에서 열어 읽습니다. 생성된 페이지는 설치·서버·인터넷 없이 본문·표·코드·도식을 표시합니다. 공식 출처 링크에는 인터넷 연결이 필요합니다.

원문은 상위 폴더의 `Claude_Agent_SDK.md`입니다. 원문 기준은 2026-10-29, Python SDK v0.2.174 / 번들 CLI v2.1.310입니다. 공개 Python SDK의 통신·제어 코드와 별도 Claude Code CLI 내부 실행의 공개 범위를 구분합니다.

학습 안내, 9개 단원, 복습·용어·Auto Memory, 출처로 구성합니다. 원문의 30개 장과 도입부·부록을 보존하고 각 단원 앞에 개념을 연결하는 편집 설명을 더했습니다. `allowed_tools`의 자동 승인 의미, `can_use_tool`의 적용 조건, Session·RAG·Auto Memory·Skill과 File Rewind·외부 부작용의 차이를 유지합니다.

루트 `AGENTS.md`에 맞춰 17px 본문·제한된 읽기 폭과 단순한 목차를 사용합니다. 원문 복습과 체크리스트는 읽기용이며 진도·채점·계정·브라우저 저장소는 없습니다. 흐름도는 로컬 SVG로, 호출 순서는 반복·분기를 보존한 표 형태로 표시합니다. Mermaid 원문을 보존합니다.

## 재생성과 검증

`site.config.mjs`는 편집 안내와 원문 대응, `build.mjs`는 HTML·도식 생성, `validate.mjs`는 섹션·코드·도식·내부 링크 검사를 담당합니다. `content-map.json`에 원문 해시와 대응 관계를 기록합니다.

이 폴더에서 실행합니다. 재생성에만 Node.js와 `marked`, `@viz-js/viz`가 필요하며 로컬 패키지 또는 Codex 번들 런타임을 사용합니다.

```powershell
node build.mjs
node validate.mjs
```

Python이 설치된 환경에서는 선택적으로 미리 볼 수 있습니다.

```powershell
python -m http.server 8767 --bind 127.0.0.1 --directory ..
```

`http://127.0.0.1:8767/html/`을 엽니다. 종료는 Ctrl+C입니다.

이번 웹페이지 제작은 사용자의 원문 편집·표시입니다. 최신 SDK·CLI 동작을 새로 조사하거나 설치·모델 실행·보안 차단율·벤치마크를 검증한 것은 아닙니다.

## 이번 제작의 검증 범위

12개 페이지, 33개 원문 섹션, 26개 코드 블록, 9개 도식의 포함 여부와 로컬 파일·섹션 링크, 제목 ID, 원문 SHA256을 확인했습니다. 좁은 브라우저 화면에서 본문 배치·목차 개폐·단원 이동을 점검했습니다. 별도 데스크톱 해상도나 실제 모바일 기기는 확인하지 않았습니다.
