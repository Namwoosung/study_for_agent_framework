# OpenAI Agents SDK 학습 페이지

`index.html`을 브라우저에서 열어 읽습니다. 본문·표·코드·도식은 설치·서버·인터넷 없이 표시하며 공식 출처 링크에는 인터넷 연결이 필요합니다.

원문은 상위 폴더의 `OpenAI_Agents_SDK.md`입니다. 원문 기준은 2026-10-29, Python openai-agents v0.24.0입니다. 학습 안내, 10개 단원, 복습·용어, 출처로 구성합니다. 일반 Agent와 Sandbox 확장, 로컬 Context와 모델 Context, Handoff와 Agent-as-Tool, Session과 RunState를 구분하며 원문의 제약·미검증 조건을 보존합니다.

루트 `AGENTS.md`에 맞춰 읽기 폭과 17px 본문, 목차 탐색을 우선했습니다. 원문의 복습 질문은 읽기용이며 채점·진도·계정·수집·저장 기능을 추가하지 않았습니다. 도식은 연결 관계와 그룹 경계를 보존한 로컬 SVG, 호출 순서는 분기·반복을 보존한 표 형태 순서도로 표시합니다. Mermaid 원문도 보존합니다.

## 파일과 재생성

`site.config.mjs`는 편집 안내와 원문 대응, `build.mjs`는 페이지·도식 생성, `validate.mjs`는 원문 섹션·코드·도식·내부 링크 검사를 담당합니다. 원문 해시와 대응 관계는 `content-map.json`에 기록합니다.

이 폴더에서 실행합니다. 재생성에만 Node.js와 `marked`, `@viz-js/viz`가 필요하며 로컬 패키지 또는 Codex 번들 런타임을 사용합니다.

```powershell
node build.mjs
node validate.mjs
```

선택적으로 Python 서버를 이용할 수 있습니다.

```powershell
python -m http.server 8767 --bind 127.0.0.1 --directory ..
```

`http://127.0.0.1:8767/html/`을 엽니다. 종료는 Ctrl+C입니다.

이번 작업은 원문 편집·표시입니다. 최신 SDK·모델 지원·사내 Gateway 호환성을 새로 조사하거나 실제 설치·모델 호출·벤치마크를 수행한 것은 아닙니다.

## 이번 제작의 검증 범위

13개 페이지, 32개 원문 섹션, 36개 코드 블록, 11개 도식의 포함 여부와 로컬 파일·섹션 링크, 제목 ID, 원문 SHA256을 확인했습니다. 좁은 브라우저 화면에서 본문 배치·목차 개폐·단원 이동을 점검했습니다. 별도 데스크톱 해상도나 실제 모바일 기기는 확인하지 않았습니다.


<!-- deep-study-guide -->
## 2차 심층 교재

[2차 심층 학습 시작](deep/index.html) · [구성과 검증 안내](deep/README.md)

2차 원문 전체를 별도 심층 과정으로 추가했습니다. 기본 교재 본문은 유지하며 각 페이지의 과정 링크로 이동할 수 있습니다. 기본 빌드와 심층 빌드는 독립적입니다.
