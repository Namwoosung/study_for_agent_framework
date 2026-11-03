# 반도체 Agent 실습

합성 검사 데이터 FAB-DEMO-r3에서 A17(1,000개 중 42개 불량)과 B04(800개 중 12개 불량)를 조회합니다. 모델은 조회, 최근 추세 해석, 다음 검사의 가설을 제안합니다. 분모와 집계값은 업무 Tool이 제공합니다.

| 시스템 | 발표용 웹 | 모델 API |
|---|---|---|
| Hermes v0.22.5 | http://127.0.0.1:18000 | http://127.0.0.1:10000/v1 |
| PydanticAI Core 2.61.0 / Harness 0.61.0 | http://127.0.0.1:18001 | http://127.0.0.1:10001/v1 |

## Windows에서 실행

Python 3.14와 3.11이 설치된 상태에서 프로젝트 루트에서 실행합니다.

```powershell
./demos/setup.ps1
```

Hermes 소스는 [공식 v0.22.5 ZIP](https://github.com/NousResearch/hermes-agent/tree/v0.22.5)을 내려받아 `demos/hermes/.runtime/source/`에 풉니다. Python 의존성은 각 가상환경에 설치합니다. Hermes의 브라우저 패키지는 Pillow 버전 제약이 충돌하고 시연 도구에 포함되지 않아 설치 대상에서 제외했습니다.

모델 포트가 준비된 뒤 터미널을 각각 열어 실행합니다.

```powershell
./demos/start.ps1 -Service hermes
./demos/start.ps1 -Service pydanticai
```

웹에서 시나리오를 고른 뒤 미리 입력된 문장을 그대로 실행하거나 고쳐 보낼 수 있습니다. 요청 본문과 결과 JSON은 실행 중 순서대로 표시됩니다. `전체 이벤트`에서 필터에 가려진 호출을 볼 수 있습니다.

## 모델 연결

두 앱은 OpenAI 호환 Chat Completions API를 호출합니다. 기본 모델 이름은 `seminar-model`이며 대상 vLLM 모델 이름에 맞게 `DEMO_HERMES_MODEL`, `DEMO_PYDANTIC_MODEL`을 지정할 수 있습니다. 이관 환경에서 해당 포트에 호환 vLLM 서비스를 띄우면 됩니다.

현재 PC의 별도 전환 서버는 `demos/.local/openai_bridge.py`에 있습니다. 같은 폴더의 `openai.json`에 실제 OpenAI 키와 사용할 모델 ID를 기록합니다. 설정 파일은 각 요청에서 읽습니다.

```json
{
  "api_key": "여기에 로컬에서 설정",
  "model": "이 프로젝트에서 사용할 수 있는 모델 ID"
}
```

또는 전환 서버 프로세스에 `OPENAI_API_KEY`와 `DEMO_OPENAI_MODEL`을 설정합니다. 실행은 `./demos/start.ps1 -Service bridge`입니다. 한 포트만 시작할 때는 `py -3.14 demos/.local/openai_bridge.py --port 10001`을 사용합니다.

현재 PC에서는 기존 정적 서버가 `127.0.0.1:10000`을 사용하므로 Hermes 전환 서버를 같은 포트의 다른 루프백 주소에 실행합니다.

```powershell
py -3.14 demos/.local/openai_bridge.py --host 127.0.0.2 --port 10000
# Hermes를 실행하는 별도 터미널
$env:DEMO_HERMES_MODEL_HOST = '127.0.0.2'
./demos/start.ps1 -Service hermes
```

전환 서버, 인증정보, 실행 상태, 가상환경, Hermes ZIP은 Git에서 제외됩니다. 다른 PC에선 해당 포트의 모델 API를 별도로 준비합니다. NativeOutput 비교는 연결한 모델이 JSON Schema 응답을 지원해야 합니다.

## 관찰 지점

- **Hermes** — 공식 AIAgent, SQLite SessionDB와 session_search, Tool Registry, pre_tool_call, 실제 승인 게이트, skill_manage, delegate_task를 사용합니다. 합성 보고서 발행은 승인 뒤 데모 로그에만 기록합니다. 일반 셸·파일 Tool은 시나리오에 등록하지 않습니다.
- **PydanticAI** — 공식 Agent.iter와 Graph, RunContext, ConversationTypeAdapter, 4개 Output 모드, 3개 EndStrategy, Harness Memory와 SubAgents를 사용합니다. 종료 정책 비교는 첫 번째 실행에서 실제로 받은 모델 응답을 후속 실행의 첫 응답으로 재사용합니다. 요청한 두 Tool이 같은 응답에 안 들어오면 화면에 표시합니다.
- **공통** — SDK가 HTTP로 보내기 직전의 JSON 본문, 지정된 Python 호출·반환, 업무 함수의 결과를 수집합니다. 실행기·검색기·Tool 검증은 프레임워크가 처리합니다. 합성 데이터, 업무 Tool, Hook 정책, UI와 관찰 어댑터는 데모 코드입니다. 세션 검색의 과거 기록은 데모용으로 실제 SQLite에 삽입합니다.

## 검증 범위

격리된 테스트 모델 endpoint에서 실제 프레임워크의 HTTP·Tool 실행을 검증했습니다. Hermes의 검색 결과, 인자 수정·차단, 승인 후 발행, Skill 파일 생성, 자식 실행 2개를 확인했습니다. PydanticAI는 Graph, Deps, 대화 저장·로드, 출력 4종, 종료 정책 3종, Core 검증, Memory 주입, Subagents를 확인했습니다. 이 테스트 응답은 웹 데모에 연결되어 있지 않습니다.

양쪽 웹 페이지는 데스크톱·휴대폰 화면과 시나리오 이동을 확인했습니다. OpenAI 전환 서버는 로컬 HTTP 경로까지 확인했으며 실모델 검증에는 실제 키와 모델 설정이 필요합니다. 함수 추적의 call/return은 비동기 함수 재개·중단도 포함하므로 모델 요청 횟수와 구별해서 읽습니다.
