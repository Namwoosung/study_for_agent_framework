# Hermes Agent 학습 교재

메인 페이지는 이 폴더의 `index.html`입니다. 브라우저에서 직접 열면 설치나 서버 없이 읽을 수 있습니다. 공식 출처 링크를 열 때만 인터넷 연결이 필요합니다.

## 폴더 구조

```text
hermes/
├── Hermes_Agent.md       # 학습 원문
└── html/                # 웹페이지 코드 및 관련 파일
    ├── index.html
    ├── *.html           # 단원별 페이지
    ├── style.css
    ├── site.js
    ├── editorial.mjs
    ├── build.mjs
    ├── validate.mjs
    ├── content-map.json
    └── assets/
```

원문은 상위 폴더의 `Hermes_Agent.md`입니다. 웹페이지에서 원문을 여는 상대 경로는 `../Hermes_Agent.md`입니다.

## 교재 구성

학습 안내와 10개 단원, 용어 사전, 출처·검증 범위를 담은 13개 정적 페이지입니다. 원문의 0–22장과 부록 2개를 보존하고, 단원 도입에는 개념을 연결하는 설명을 더했습니다. 원문의 Mermaid 도식 7개를 로컬 SVG로 표시합니다.

루트 `AGENTS.md`를 따라 17px 본문, 최대 76ch 읽기 폭, 1.8 줄 간격과 단순한 목차를 사용합니다. JavaScript는 좁은 화면에서 목차를 여닫는 용도로만 사용합니다. 브라우저 저장소나 별도 서버 API는 사용하지 않습니다.

## 재생성과 검증

이미 생성된 페이지를 읽는 데에는 의존성이 필요 없습니다. 원문을 수정한 뒤 다시 생성할 때만 Node.js와 `marked`, `@viz-js/viz`가 필요합니다. 로컬 패키지 또는 Codex 번들 런타임을 사용합니다.

이 `html/` 폴더에서 실행합니다.

```powershell
node build.mjs
node validate.mjs
```

`editorial.mjs`는 단원별 편집 안내, `build.mjs`는 HTML·도식 생성, `validate.mjs`는 원문 섹션 포함 여부와 로컬 링크·제목 ID 검사를 담당합니다. `content-map.json`에는 원문 SHA256과 페이지 대응 관계를 기록합니다.

## 로컬 서버 미리보기

Python이 설치된 환경에서 이 `html/` 폴더에서 실행합니다. 학습 원문 링크도 열리도록 상위 `hermes/`를 서버 루트로 사용합니다.

```powershell
python -m http.server 8766 --bind 127.0.0.1 --directory ..
```

브라우저에서 `http://127.0.0.1:8766/html/`을 엽니다. 서버 종료는 Ctrl+C입니다.

교재는 원문 기준의 문헌·공개 소스 검토이며, Hermes의 실제 설치·실행·벤치마크나 최신 구현의 추가 검증을 뜻하지 않습니다.
