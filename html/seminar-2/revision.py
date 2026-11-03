"""2026-11-03 editorial revision. Stable slide IDs, updated audience copy and study notes."""
from html import escape

# title, subtitle, short closing line. Technical detail belongs in Sources.
COPY = {
'S00': ('Agent Framework 세부 구조', '2차 세미나', 'Hermes · Claude Code · PydanticAI'),
'S01': ('Agent Framework의 구성', '목표가 모델 호출과 도구 실행으로 이어지는 과정', '각 기술이 이 구조를 어떻게 구현하는지 살펴봅니다.'),
'S02': ('2차 세미나 진행 계획', '1차 세미나의 내용을 기반으로 실제 기술별 세부 사항을 살펴봅니다.', '3차에서는 직접 개발하고, 결과를 검증하며 회고합니다.'),
'S03': ('Agent Harness와 SDK', '완성된 Agent를 확장하거나, 코드로 필요한 기능을 구성합니다.', 'Hermes와 PydanticAI를 중심으로 살펴봅니다.'),
'S03H': ('Hermes', '범용 Agent Harness', '전체 구조를 먼저 보고, 각 기능의 동작을 살펴봅니다.'),
'S04': ('Hermes는 범용 Agent Harness입니다', '모델 호출부터 도구 실행과 상태 관리까지 기본 실행환경을 제공합니다.', '실제 사용 가능한 기능은 설치 환경과 설정에 따라 달라집니다.'),
'S05': ('사용자 입력에서 모델 요청까지', '한 Turn을 시작할 때 준비하는 정보', '최종 요청에는 지침, 대화 이력, 도구 정의가 함께 담깁니다.'),
'S06': ('Tool을 실행할 때와 답변을 마칠 때', '모델 응답에 따라 반복하거나 종료합니다.', 'Tool 오류와 모델 API 오류는 복구 방법이 다릅니다.'),
'S07': ('고정된 Prompt와 매번 달라지는 정보', '세션의 지침에 대화 이력과 호출 시점 정보를 더합니다.', 'Volatile 계층도 세션 안에서는 같은 snapshot을 사용할 수 있습니다.'),
'S08': ('같은 Prefix의 계산을 재사용하기', '반복되는 입력 앞부분은 추론 서비스가 캐시로 처리할 수 있습니다.', '입력은 다시 보내지만, 일부 계산은 재사용할 수 있습니다.'),
'S09': ('긴 대화에서 남길 것과 줄일 것', '과거 내용을 줄이면서 최근 문맥과 Tool 호출 관계를 보존합니다.', '압축 후에도 호출과 결과가 서로 대응해야 합니다.'),
'S10': ('저장한 Memory는 언제 반영될까?', '파일을 바꾸는 시점과 세션이 읽는 시점은 다릅니다.', '현재 세션의 system snapshot은 파일 저장만으로 바뀌지 않습니다.'),
'S11': ('기억할 사실과 다시 찾을 대화', 'Memory, Session History, 외부 Provider의 역할', '과거 대화는 필요한 기록을 검색해 현재 Context에 넣습니다.'),
'S12': ('Skill을 읽고 다시 사용하는 과정', '목록에서 절차를 고르고, 필요한 자료를 불러옵니다.', '저장한 절차를 다시 쓰기 전에 근거와 버전을 확인합니다.'),
'S13': ('Tool 등록과 MCP·Plugin 연결', '실행 함수, 외부 서버, 런타임 확장을 연결하는 방법', '도구에 따라 실행 경로와 관찰 가능한 지점이 달라집니다.'),
'S14': ('Tool 병렬 실행과 Subagent 위임', '함수를 함께 실행하는 경우와 별도 Agent에게 맡기는 경우', 'Subagent의 결과를 받은 부모가 다음 작업을 이어갑니다.'),
'S15': ('실행 권한과 Hermes Demo', '입력 검사, 승인, 실행환경, 복구 기능을 확인합니다.', 'Demo에서는 모델 요청, Tool 결과, 저장된 상태를 살펴봅니다.'),
'S16': ('Claude Code의 실행 구조', 'Context를 모으고, 도구를 실행하고, 결과를 확인합니다.', '도구와 지침, 권한 설정이 하나의 실행환경에 연결됩니다.'),
'S17': ('프로젝트 지침과 Auto Memory', '사람이 정한 규칙과 Agent가 남긴 기억', '접근 권한은 지침 파일과 별도로 관리합니다.'),
'S18': ('Subagent와 Agent Teams', '부모에게 결과를 돌려주거나, 팀원끼리 협업합니다.', '독립 Context를 써도 공유 파일과 자원의 충돌은 확인해야 합니다.'),
'S19': ('명령으로 세션과 기억 관리하기', '대화 재개, Prompt 갱신, 보류된 Memory 검토', '명령마다 바꾸는 상태와 적용 시점이 다릅니다.'),
'S20': ('Pydantic에서 PydanticAI로', '값의 검증에서 Agent 실행과 선택적 Harness까지', 'Core로 시작하고, 필요한 Harness 기능을 추가할 수 있습니다.'),
'S21': ('PydanticAI 전체 구조', '개발자가 정의한 Agent를 내부 Graph가 실행합니다.', '모델·Tool·저장소를 애플리케이션에 맞게 연결합니다.'),
'S22': ('Agent와 Tool을 코드로 정의하기', '지침, 실행 함수, 의존성을 연결하는 기본 코드', '업무 데이터 조회와 권한 확인은 애플리케이션에서 구현합니다.'),
'S23': ('세 노드로 보는 Agent 실행', '입력 준비, 모델 요청, Tool과 최종 출력 처리', 'Tool 결과와 수정 피드백은 다음 모델 요청으로 이어집니다.'),
'S24': ('모델 입력과 Python 실행 자원', '지시·History와 Deps가 전달되는 경로', 'Deps에서 사용한 정보도 Tool 결과로 반환하면 모델에 전달됩니다.'),
'S25': ('함수 정의에서 Tool 실행까지', '스키마를 공개하고, 인자를 검증한 뒤 실행합니다.', '모델에 도구를 보여주는 것과 실행을 허가하는 것은 별개입니다.'),
'S26': ('함께 실행할 작업과 기다릴 작업', '독립 작업은 병렬로, 순서가 필요한 작업은 barrier로 처리합니다.', '여러 조회 결과를 합칠 때는 대상과 기준 시점도 맞춰야 합니다.'),
'S27': ('출력 형식과 업무 정확성 검증', '타입 검사 이후에도 계산과 근거를 확인합니다.', '형식이 맞는 답변도 내용은 틀릴 수 있습니다.'),
'S28': ('EndStrategy에 따른 Tool 실행', '같은 응답을 받아도 종료 정책에 따라 실행 범위가 달라집니다.', 'graceful에서는 최종 출력 뒤의 Function Tool도 실행될 수 있습니다.'),
'S29': ('무엇을 다시 시도할까?', '인자·출력 수정, API 장애 복구, 업무 판단 오류', '재시도가 여러 계층에 있으면 실제 요청 횟수가 늘어날 수 있습니다.'),
'S30': ('Hook과 Capability 구성', '실행 시점에 개입하고, 관련 기능을 묶어 재사용합니다.', 'wrapper 순서에 따라 안쪽 Hook의 실행 여부가 달라집니다.'),
'S31': ('이전 대화를 다음 Run으로 이어가기', '이력을 저장하고 필요한 대화에 다시 전달합니다.', '대화 저장, 사용자 구분, 누적 사용량을 함께 관리합니다.'),
'S32': ('Context 압축과 원본 보관', 'Core와 Harness가 제공하는 압축 방법', '모델에 보낼 이력과 감사용 원본은 따로 관리합니다.'),
'S33': ('Harness의 Memory 기능', '대화가 끝난 뒤에도 필요한 사실을 저장하고 불러옵니다.', '저장 범위뿐 아니라 읽기·수정 권한과 유효기간도 정합니다.'),
'S34': ('Skill 로딩과 MCP 연결', '절차 문서를 읽는 경로와 외부 도구를 호출하는 경로', '사용할 절차와 서버, 인증 설정을 준비해야 합니다.'),
'S35': ('Agent 사이의 작업 전달', '위임, 라우팅, Graph, Advisor의 실행 방식', '누가 다음 작업을 정하고 어디로 결과를 돌려주는지 확인합니다.'),
'S36': ('승인을 기다렸다가 실행 재개하기', '보류된 호출을 검토하고, 승인 결과를 전달합니다.', '검토한 호출과 인자를 실행 시점에 다시 확인합니다.'),
'S37': ('Core와 Harness로 구성하는 Agent', '실행 기능을 조합하고 업무에 필요한 코드를 연결합니다.', '데이터, 권한, 결과 검증은 업무에 맞게 설계합니다.'),
'S38': ('PydanticAI Demo', '정의 코드에서 모델 요청과 Tool 결과까지 따라갑니다.', 'Core 실행을 먼저 확인한 뒤 Harness 기능을 추가합니다.'),
'S43': ('Agent를 어디에서 실행할까?', '중앙 서버와 사용자 PC에 배치했을 때의 차이', 'Agent 실행 자원과 모델 서버 자원을 나누어 살펴봅니다.'),
'S44': ('실행 기록과 업무 결과 검증', '무엇을 실행했는지, 요구한 결과가 맞는지 확인합니다.', '데이터 범위, 계산, 근거, 승인 내용을 함께 확인합니다.'),
'S45': ('구조를 이해하고 실제 개발로', 'Hermes와 PydanticAI에서 살펴본 내용', '3차에서는 Agent를 개발하고 검증 결과와 시행착오를 공유합니다.'),
}

# Each entry contains real concept definitions and a short explanation, rather
# than a dump of authoring instructions. These are available on every Sources.
DETAIL = {
'S00': ([('Agent Framework', '모델 호출, 도구 실행, 상태 관리 등 Agent를 구성하고 실행하는 기능을 제공하는 소프트웨어입니다.')], '이번 세미나는 공통 개념을 배운 1차에 이어 실제 기술의 세부 구조를 살펴봅니다. 이 발표에서는 Hermes와 PydanticAI를 중심으로 실행 흐름과 상태 관리 방법을 설명하고 Claude Code와도 비교합니다.'),
'S01': ([('Runtime / Harness', '모델 호출과 Tool 실행을 반복하면서 상태, 종료 조건, 권한을 관리합니다.'), ('Context Builder', '지침, 현재 상태, 대화 이력, 필요한 기억을 모아 모델 입력을 구성합니다.'), ('Guardrails / Trace', '실행 전후의 검사·승인과 실행 기록을 뜻합니다. 각 기능이 적용되는 지점은 구현에 따라 다릅니다.')], '사용자 목표와 지침을 바탕으로 Runtime이 Context를 준비하고 모델을 호출합니다. 모델이 Tool을 요청하면 Runtime이 실행 조건을 확인하고 도구를 통해 환경에 접근합니다. 결과는 상태와 다음 Context에 반영됩니다. 도식은 특정 제품의 호출 순서를 복제한 것이 아니라 이번 발표의 공통 구성도입니다.'),
'S02': ([('모델 개발·서빙', 'AI Studio, vLLM, SGLang을 다루는 파트입니다.'), ('Agent 개발·워크플로', 'DeepAgents, LangChain, LangGraph를 다루는 파트입니다.'), ('Agent Harness·SDK', 'Hermes, PydanticAI, OpenAI, Claude 관련 기술을 다루는 파트입니다.')], '1차 세미나의 개념을 바탕으로 세 파트가 각 기술의 세부 사항을 설명합니다. 담당자는 위에서부터 강준혁, 박건, 남우성입니다. 이번 발표는 세 번째 파트이며 실제 개발, 검증과 회고는 3차에서 진행합니다.'),
'S03': ([('Agent Harness', 'CLI, 도구, 세션 등 갖춰진 Agent 실행환경에서 시작합니다. 여기서는 Hermes와 Claude Code를 묶었습니다.'), ('Agent SDK', '개발자가 Agent, Tool, 실행 조건을 코드로 정의하고 애플리케이션에 연결하는 출발점입니다.')], 'Harness와 SDK는 배타적인 제품 분류가 아닙니다. Hermes의 프로그래밍 통합이나 PydanticAI의 선택적 Harness처럼 기능이 겹칠 수 있습니다. 이 장은 발표를 위한 두 출발점을 보여주며, Hermes와 PydanticAI를 각 행의 주요 설명 대상으로 강조합니다. 다른 SDK는 이름과 편집 위치만 표시하며 기능 비교가 완료됐다는 뜻은 아닙니다.'),
'S03H': ([('AIAgent', '모델 요청과 Tool 실행을 이어가는 Hermes의 Agent Runtime입니다.'), ('Session / Memory / Skills', '대화 기록, 지속 사실, 재사용 절차를 서로 다른 방식으로 보관하고 사용합니다.')], 'CLI나 Gateway 등에서 들어온 요청은 AIAgent로 이어집니다. Prompt를 구성해 모델을 호출하고, 필요한 Tool을 실행한 뒤 결과를 다시 모델에 전달합니다. 이 과정에서 세션, Memory, Skills를 사용합니다. 왼쪽은 대표 관계를 단순화한 전체 구조도이며 이후 장표에서 각 부분을 나누어 설명합니다.'),
'S04': ([('범용 Agent Harness', '특정 업무 하나에 고정하지 않고 여러 도구와 모델을 연결해 작업할 수 있는 실행환경입니다.'), ('기본 제공 기능', 'Loop·입출력·Tool 확장·기억/검색·Skills·운영 기능이 포함되지만 실제 가용성은 설치 방식, 플랫폼, 인증, 활성 Toolset과 설정에 따라 다릅니다.')], 'Hermes는 Agent Loop와 Tool Calling, 취소·중단·대체 모델 경로를 제공합니다. CLI/TUI/Desktop, 메신저 Gateway, HTTP API, ACP 등으로 접근할 수 있습니다. 터미널·파일·웹·브라우저·코드 실행, Toolsets·MCP·Plugins로 기능을 연결합니다. SQLite 세션과 FTS5 검색, Memory 파일과 외부 Memory Plugin을 구분하며, Skills 작성/관리와 Curator, Subagent·Cron·Hooks·승인·격리·파일 복구 등의 운영 기능도 포함합니다. 모든 기능이 기본 활성화되거나 모든 환경에서 동일하게 동작한다는 의미는 아닙니다.'),
'S05': ([('Turn', '사용자 입력 한 건을 처리하는 단위이며, 여러 모델 호출과 Tool 실행을 포함할 수 있습니다.'), ('Provider Adapter', '내부 메시지와 도구 정의를 선택한 모델 API 형식으로 변환합니다.')], 'Task와 사용자 메시지를 준비한 뒤 Prompt와 History, Tool schema를 모읍니다. 압축 필요 여부와 호출 시점 정보를 반영하고 Provider 형식으로 바꾸어 요청합니다. 지원 Provider에만 cache marker를 적용합니다. 프레임워크 내부 객체와 실제 전송 JSON은 구분해서 관찰합니다.'),
'S06': ([('Agent Loop', '모델 응답을 해석하고 도구 결과를 추가하며 다음 호출 또는 종료를 결정합니다.'), ('Tool 오류 / API 오류', '실행 오류를 모델에게 알려주는 경로와 모델 API 통신을 복구하는 경로는 다릅니다.')], 'Tool Call이 있으면 Runtime이 실행하고 결과를 대화에 추가해 모델을 다시 호출합니다. 최종 텍스트라면 응답과 세션을 정리합니다. 사용자 중단, 예산 소진, Context 문제, API 오류는 각각 별도 경로로 처리합니다. 모델이 답변을 마쳤다는 사실만으로 업무 목표의 달성을 보장하지는 않습니다.'),
'S07': ([('Stable / Context / Volatile', '정체성·기본 행동, 프로젝트·호출자 지침, Memory·런타임 snapshot을 나눈 논리적 계층입니다.'), ('Frozen Snapshot', '세션 동안 재사용하는 system prompt의 기준 내용입니다.')], 'SOUL은 정체성과 기본 행동을, AGENTS 계열 파일은 프로젝트 규칙을 안내합니다. 세션이 재사용하는 Prompt에 대화 이력과 이번 호출의 정보를 더합니다. Volatile이라는 이름이 매번 재작성을 뜻하지는 않습니다. 현행 문서의 Skill 계층 설명에는 불일치가 있어 여기서는 위치를 단정하지 않습니다.'),
'S08': ([('Prefix Cache', '반복되는 입력 앞부분의 계산을 추론 서비스가 재사용하는 방식입니다.'), ('입력 길이와 계산량', '입력을 다시 전송해도 일부 계산이 재사용될 수 있으며 Context 길이 자체가 줄어드는 것은 아닙니다.')], '예시의 8,000/2,000 tokens는 원리 설명용 수치입니다. Hermes는 입력 내용과 순서를 구성하고, 실제 캐시 적중은 Provider나 서빙 엔진이 판단합니다. Prefix 일치, 캐시 퇴거, 부하, 모델과 API 지원 조건이 영향을 줍니다. 로컬 OpenAI 프록시 실행을 vLLM 캐시 실측으로 해석하지 않습니다.'),
'S09': ([('Context Compression', '긴 이력을 줄여 다음 요청에 필요한 공간을 확보합니다.'), ('Tool Call / Result 쌍', '호출 ID에 맞는 결과와 순서를 보존해야 모델 API가 대화를 올바르게 해석할 수 있습니다.')], '오래된 내용을 축약하면서 최근 문맥과 미해결 작업, 호출·결과 관계를 보존합니다. Tool Loop 안의 압축과 Gateway의 세션 위생 처리는 다릅니다. 문서의 50%/85% 및 최근 20개는 조건과 설정에 따른 기본 설명입니다. 수치·단위·원본 근거는 별도 artifact로 남기는 업무 설계를 검토할 수 있습니다.'),
'S10': ([('Built-in Memory', 'MEMORY.md와 USER.md에 다음 세션에서도 필요한 짧은 사실을 남깁니다.'), ('파일 저장과 Prompt 반영', 'Memory Tool로 파일을 바꾸는 것과 이미 고정된 system snapshot을 바꾸는 것은 다른 동작입니다.')], '세션 A가 시작할 때 파일을 읽어 snapshot을 만듭니다. A 도중 memory Tool이 파일을 갱신해도 기존 system snapshot은 자동 교체되지 않으며, 새 Tool 결과로 내용을 아는 것과도 구분합니다. 다음 세션은 갱신된 파일을 읽습니다. add/patch/remove, 용량 초과 처리와 write_approval 조건을 확인해야 합니다. SOP와 분석 근거는 별도로 버전을 고정하는 설계가 필요합니다.'),
'S11': ([('Session History', 'SQLite state.db에 보관한 대화와 Tool 실행 기록입니다.'), ('FTS5 session_search', '과거 대화를 문자열 중심으로 검색하고 선택한 결과를 Context에 넣습니다.'), ('External Provider', '별도 저장소나 Plugin으로 추가하는 기억·검색 기능이며 기본 파일 Memory와 구분합니다.')], '소수의 지속 사실, 과거 대화의 상세 기록, 외부 확장은 용도와 수명이 다릅니다. 정확한 장비 ID 질의와 표현이 달라진 질의를 나누어 검색 품질을 평가하고 대상과 기간도 확인합니다. Profile은 config/DB/memory 운영 분리이며 독립 보안 테넌트 보장은 아닙니다. 실제 경로는 HERMES_HOME과 환경에 따라 달라집니다.'),
'S12': ([('Skill', '언제 어떤 도구를 어떤 순서로 사용할지 적은 문서형 절차입니다.'), ('Progressive Disclosure', '목록, 선택한 SKILL.md 본문, 필요한 참고 파일 순으로 내용을 불러옵니다.'), ('Curator', 'Agent 생성 Skill의 사용 이력을 보고 active/stale/archived 상태로 관리합니다.')], '실제 실행은 Tool이 하고 Skill은 절차와 자료를 제공합니다. skill_manage로 생성·수정·삭제할 수 있지만, 이것은 기반 모델 가중치의 학습과 다릅니다. 잘못된 절차도 재사용될 수 있으므로 검토와 버전 관리가 필요합니다. Curator가 사용되지 않는 모든 사용자 Skill을 무조건 삭제하는 것은 아닙니다.'),
'S13': ([('Tool Registry', '이름, 모델용 schema, 실행 handler, 가용성 조건을 연결합니다.'), ('MCP', '외부 서버가 제공하는 도구를 Client로 발견하고 호출하는 연결 방식입니다.'), ('Plugin / Hook', 'Hermes 실행환경에 Tool·명령·실행 전후 처리를 추가하는 확장 접점입니다.')], '등록된 모든 도구가 모델에 노출되는 것은 아닙니다. Toolset과 환경, check_fn 등을 통과한 schema를 제공합니다. memory/delegate_task 등 Agent 상태를 사용하는 도구는 일반 Registry dispatch 전에 별도 처리될 수 있습니다. 중앙 Hook 하나로 모든 내부 실행을 관찰했다고 판단하지 않습니다.'),
'S14': ([('병렬 Tool', '한 모델 응답의 여러 호출을 같은 Agent Loop에서 실행합니다.'), ('Subagent', '별도 AIAgent가 독립 Goal·Context·Loop로 작업하고 결과를 부모에게 돌려줍니다.')], 'thread는 실행 수단이며 Agent의 개수가 아닙니다. Hermes는 상호작용이나 파일 충돌 조건에 따라 barrier로 실행 구간을 나눌 수 있습니다. 같은 snapshot의 독립 조회를 합치는 것과 별도 Agent에게 분석을 위임하는 것은 비용과 상태 관리가 다릅니다. Context 분리가 OS·DB·파일 권한의 격리를 자동으로 만들지는 않습니다.'),
'S15': ([('승인과 실행 권한', '명령·파일 검사, 사용자 승인, OS·DB·Sandbox 권한은 서로 다른 통제입니다.'), ('Checkpoint', '지원 범위 안에서 파일 복구를 돕는 opt-in 기능이며 외부 변경 전체의 rollback은 아닙니다.')], 'smart/manual/off 승인 모드와 무인 실행 deny 정책을 함께 확인합니다. 위험 패턴 탐지뿐 아니라 실제 실행 계정과 데이터 접근 권한도 제한해야 합니다. Cron의 Agent 작업 모드는 새 실행을 시작하는 입구입니다. Demo에서는 Context, Tool, 저장 상태를 관찰할 계획이며 현재 연결 페이지는 실제 서비스가 없는 안내 화면입니다.'),
'S16': ([('Claude Code Harness', '모델, 도구, Context, 권한과 위임 설정을 연결한 실행환경입니다.'), ('Gather / Act / Verify', '정보 수집, 행동, 결과 확인이 반복되는 공개 동작 설명입니다.')], '사용자 요청과 프로젝트 파일을 바탕으로 Context를 수집하고 도구를 실행하며 결과를 확인합니다. 이 장은 공개 인터페이스와 동작을 설명합니다. 비공개 엔진의 함수나 내부 구조를 확인한 것처럼 세부 구현을 추정하지 않습니다.'),
'S17': ([('프로젝트 지침', '사람이 작업 규칙과 제약을 적은 파일입니다.'), ('Auto Memory', 'Claude Code가 관리하는 기억으로 인덱스와 필요한 세부 파일을 로드합니다.')], 'Hermes는 SOUL·프로젝트 지침과 MEMORY/USER 파일을 구분하고 세션 snapshot을 사용합니다. Claude Code는 CLAUDE.md와 Auto Memory의 읽기 정책이 다릅니다. AGENTS.md를 같은 방식으로 자동 로딩한다고 합치지 않으며 필요 시 import 관계를 확인합니다. 두 제품 모두 지침이 실제 권한 통제를 대신하지는 않습니다.'),
'S18': ([('Subagent', '부모의 하위 과제를 수행한 뒤 결과를 부모에게 반환합니다.'), ('Agent Teams', '독립 세션의 팀원들이 공유 작업과 직접 메시지로 협업하는 방식입니다.')], '위임과 협업은 결과 전달 경로와 제어 주체가 다릅니다. Teams의 지원 조건과 실험적 제약을 확인해야 하며, Context가 분리되어도 파일 충돌과 공통 자원 권한, 조정 비용은 남습니다.'),
'S19': ([('Prompt refresh', 'Hermes의 저장된 Prompt를 명시적으로 갱신하는 관리 경로입니다.'), ('Pending Memory', '보류된 기억 쓰기를 검토하는 기능입니다.'), ('Resume / Compact', 'Claude Code에서 대화를 다시 열거나 Context를 축약하는 서로 다른 동작입니다.')], '명령 이름보다 어떤 상태를 바꾸는지에 주목합니다. hermes sessions refresh-prompts --session, /memory pending, Claude Code의 /resume·/compact는 목적과 적용 시점이 다릅니다. 화면의 명령은 설명용이며 이 발표에서 실제 실행한 기록은 아닙니다.'),
'S20': ([('Pydantic', 'Python 값과 schema를 검증하는 기반 라이브러리입니다.'), ('PydanticAI Core', 'Agent·Tool·Output과 내부 실행 Graph를 제공합니다.'), ('선택적 Harness', 'Memory·Skills 등 필요한 실행 기능을 추가하는 별도 구성입니다.')], 'Core만으로도 Agent를 만들 수 있습니다. pydantic-graph, Evals/Logfire, Provider/Model과 연결되는 범위를 구분하며 모든 기능을 한 패키지가 자동으로 구성한다고 보지 않습니다. Harness는 설치·버전을 별도로 확인합니다.'),
'S21': ([('내부 Graph', 'UserPromptNode, ModelRequestNode, CallToolsNode가 입력과 응답을 처리합니다.'), ('Capabilities', 'Run·Model·Tool·Output 실행 지점에 개입하는 기능을 구성합니다.')], '개발자는 지침, 도구, output_type과 의존성을 정의합니다. SDK는 pydantic-graph로 모델 요청과 Tool/출력 분기를 처리합니다. 데이터 저장, 업무 권한, 실제 Tool 서비스는 앱에 연결하며 LangGraph를 사용한다는 뜻은 아닙니다.'),
'S22': ([('Agent 정의', '모델, 지침, Deps와 출력 계약을 설정합니다.'), ('RunContext', 'Tool이 실행될 때 앱이 주입한 자원과 상태에 접근하는 문맥입니다.')], '예시의 get_bin_summary는 앱에서 구현하는 Tool이고 DemoDeps/query 역시 사용자 코드입니다. SDK Loop를 다시 구현할 필요는 없지만 실제 데이터 조회와 인가를 Tool 또는 서비스에서 검사해야 합니다. 이 코드는 연결 구조를 보여주는 축약 예시입니다.'),
'S23': ([('UserPromptNode', '입력과 이전 이력을 준비합니다.'), ('ModelRequestNode', '모델 요청을 구성하고 호출합니다.'), ('CallToolsNode', 'Function Tool과 최종 Output을 분류하고 검증·실행합니다.')], 'Function Tool의 결과는 다음 모델 요청으로 돌아갑니다. 최종 출력이 유효하면 End로 종료하고, 검증이 실패하면 모델 수정 피드백으로 이어집니다. history, usage, retry 등 실행 상태를 함께 추적합니다.'),
'S24': ([('모델 입력', 'Instructions/System Prompt, History, Tool schema와 반환 결과 등 실제로 전송하는 정보입니다.'), ('Deps', 'DB client나 인증 문맥처럼 Python에서 사용하는 앱 자원입니다.')], 'Deps 전체가 자동으로 모델에 전송되는 것은 아닙니다. 하지만 지침 생성이나 Tool 반환에 선택한 정보가 포함되면 모델 입력으로 전달됩니다. 객체 주입의 안전성과 Tool 결과의 정보 노출은 따로 확인해야 합니다.'),
'S25': ([('Schema', '모델이 생성할 Tool 이름과 인자의 형식을 설명합니다.'), ('tool / tool_plain', 'RunContext를 사용하는 Tool과 일반 인자만 받는 Tool의 등록 방식입니다.')], '함수와 타입으로 schema를 만들고 모델에 노출한 뒤 응답 인자를 검증해 실행합니다. 허용 범위와 사용자 인가는 서버 측에서 확인해야 합니다. 노출 필터가 곧 실행 권한 검사가 되는 것은 아닙니다.'),
'S26': ([('동시 실행', '독립적인 Tool을 함께 스케줄링해 대기를 겹칩니다.'), ('sequential barrier', '앞 구간이 완료된 후 해당 Tool을 단독 실행하고 다음 구간을 시작합니다.')], 'async Tool은 task, sync Tool은 worker thread로 실행될 수 있습니다. sequential=True는 실행 순서의 장벽이며 데이터 snapshot이나 트랜잭션을 자동으로 만들지 않습니다. 같은 Lot·시간대·기준 시점을 사용했는지는 앱이 확인합니다.'),
'S27': ([('ToolOutput / NativeOutput / PromptedOutput', '출력용 Tool, Provider의 구조화 출력, 형식 지시와 파싱을 사용하는 서로 다른 출력 방식입니다.'), ('output_type', '최종 결과의 계약이며 개별 Tool 반환 타입과 목적이 다릅니다.')], 'Pydantic으로 타입과 필드를 검증한 뒤 업무 Validator와 실제 데이터 검증을 연결합니다. 단위, 계산, 분모, 기간, 출처가 맞는지는 schema 통과만으로 알 수 없습니다. 모델과 Provider에 따라 지원 가능한 방식도 다릅니다.'),
'S28': ([('EndStrategy', '최종 출력이 제안된 응답에서 Function Tool을 어디까지 실행할지 정하는 정책입니다.'), ('Emission 순서', '모델이 제안한 순서이며 실제 완료 시간 순서와 다릅니다.')], '같은 A/O1/B/O2 응답을 정책별로 비교하는 예시입니다. 최종 결과 선택과 Tool 실행 여부를 분리해서 봅니다. graceful에서도 최종 출력 뒤 Function Tool이 실행될 수 있으므로 부작용이 있는 도구는 승인과 업무 단계 분리가 필요합니다. 정확한 정책별 동작은 표와 고정 응답 시험 기준을 따릅니다.'),
'S29': ([('ModelRetry', '잘못된 인자나 출력에 대해 모델이 수정하도록 피드백하는 경로입니다.'), ('통신 retry', '429·5xx·연결 장애를 timeout과 backoff 정책으로 복구합니다.')], '유효한 형식의 잘못된 업무 판단은 통신 retry로 해결되지 않습니다. SDK와 HTTP·프록시 재시도가 중첩되면 실제 요청과 비용이 늘어날 수 있습니다. UsageLimits, 시간 제한, Tool 중복 부작용 방지를 별도로 관리합니다.'),
'S30': ([('Hook', 'Run·모델 요청·Tool 등 특정 실행 시점에 개입합니다.'), ('Capability', '지시·도구·Hook·설정을 기능 단위로 묶어 재사용합니다.')], 'wrapper는 A.enter→B.enter→core→B.exit→A.exit 순서처럼 중첩됩니다. 바깥 wrapper가 handler를 호출하지 않으면 안쪽 검사도 실행되지 않을 수 있습니다. 실행 순서와 Run별 상태 수명을 확인해야 합니다.'),
'S31': ([('message_history', '이전 Run의 typed messages를 다음 실행에 전달하는 경로입니다.'), ('Conversation', '현행 API에서 이력·사용량·ID 등을 이어가는 기능이며 저장소 자체와 구분합니다.')], 'Agent 객체를 계속 사용하는 것만으로 사용자 대화가 자동 복원되지는 않습니다. 앱이 인증된 사용자에 맞는 이력을 저장하고 불러와야 합니다. usage를 초기화하면 대화 전체의 누적 예산과 달라질 수 있어 동시 갱신·TTL·누적 한도도 함께 고려합니다.'),
'S32': ([('Provider-native compaction', '지원하는 모델 API에서 제공하는 압축 경로입니다.'), ('Harness 압축', 'clear·sliding window·summarize 등 별도로 선택하는 이력 축약 전략입니다.')], 'Core와 Harness의 제공 범위를 구분하고 원본 저장 정책을 따로 정합니다. 축약이 Run History에 유지될 수 있으며 원본 복원이 자동 보장되는 것은 아닙니다. vLLM 이관 기본 경로는 Provider 전용 compaction을 필수로 두지 않습니다.'),
'S33': ([('Memory capability', '지속 사실을 제한적으로 주입하거나 필요 시 검색하고 기록하는 기능입니다.'), ('Namespace', '저장 범위를 구분하는 이름이며 인증과 DB 권한을 대신하지 않습니다.')], '파일·메모리·DB 등 Store를 선택하고 앱이 인증된 사용자/Agent 범위를 연결합니다. 무엇을 기억할지, 누가 읽거나 바꿀지, SOP가 언제 만료되는지 정해야 합니다. Hermes의 frozen snapshot과 동일한 구현이라고 가정하지 않습니다.'),
'S34': ([('Skill library', '절차 문서를 검증·등록하고 목록과 본문을 제공하는 기능입니다.'), ('MCP Client', '외부 서버에 접속해 도구를 발견하고 호출합니다.')], 'Skill은 모델에게 절차를 알려주고 MCP는 외부 기능을 연결합니다. 사용할 문서와 supporting files, 서버와 인증 설정은 앱이 준비합니다. Skill을 실행 함수로, MCP를 필수 저장소로 취급하지 않습니다.'),
'S35': ([('Delegation', '부모가 자식에게 작업을 맡기고 결과를 받아 계속 진행합니다.'), ('Routing / Graph / Advisor', '역할 선택, 명시적 단계, 자문 호출 등 제어 방식을 달리 구성합니다.')], '다음 행동을 누가 결정하는지, 결과가 어디로 돌아오는지, 어떤 상태를 공유하는지 비교합니다. 부모 반환 패턴을 다른 SDK의 native handoff API와 동일시하지 않습니다. 실제 데이터·Tool 권한과 비용은 별도 설계 대상입니다.'),
'S36': ([('Deferred Tool Call', '즉시 실행하지 않고 승인이나 외부 결과를 기다리는 호출입니다.'), ('재개', '호출 ID와 승인/결과를 연결해 다음 실행으로 이어가는 과정입니다.')], '검토한 인자와 실제 실행 인자가 일치하는지 확인하고 데이터 버전과 사용자 권한을 실행 시점에 다시 검사합니다. 승인 UI, 인증, 영속 저장과 재시작 복구는 호스트 앱이 연결해야 합니다. UI가 없을 때 사용할 CLI·handler·보류 결과 경로도 정해야 합니다.'),
'S37': ([('Core + Harness', '내부 실행 Graph에 선택적 Memory·Skills·동작 기능을 연결하는 구성입니다.'), ('업무 구현', '인증·DB 접근·검증·저장 등 서비스에 맞게 만드는 코드입니다.')], '제공 기능을 사용해도 업무 요구가 자동으로 충족되는 것은 아닙니다. 반대로 모든 기능을 직접 구현해야 하는 것도 아닙니다. 검증·Tool 실행·최종화·재개를 연결하면서 필요한 업무 규칙을 각 지점에 넣습니다.'),
'S38': ([('Runtime 관찰', '정의 코드, 내부 노드, 실제 요청, Tool 인자와 반환을 연결해 확인합니다.'), ('고정 응답 시험', '정해진 모델 응답을 실제 executor가 처리하는 시험이며 live LLM 응답과 구분합니다.')], 'Core 최소 실행을 먼저 보고 Memory 등 Harness 한 경로를 추가해 차이를 확인하는 Demo 계획입니다. 종료 정책은 자연 모델이 같은 응답을 반복한다고 가정하지 않고 별도 시험으로 비교합니다. 현재 발표의 Demo 링크는 실제 서비스가 연결되지 않은 안내 화면입니다.'),
'S43': ([('중앙 실행', '서버가 Agent·작업·사용자 격리·공통 운영을 관리합니다.'), ('로컬 실행', '사용자 PC에 설치·업데이트·실행 권한 관리가 필요합니다.')], 'Agent의 CPU/메모리, Tool I/O, 승인·모델 대기와 모델 서버 GPU 자원은 수명이 다릅니다. 로컬 Agent도 모델 요청으로 정보를 보낼 수 있어 데이터 경로를 확인해야 합니다. Worker/GPU 수는 모델, 부하, Context와 실제 대기를 측정한 뒤 정합니다.'),
'S44': ([('Trace', '요청·Tool·승인·오류·결과와 사용 데이터의 실행 기록입니다.'), ('Evaluation', '요구한 계산·근거·권한·업무 목표를 만족했는지 평가합니다.')], '같은 Tool을 호출했어도 데이터 snapshot이나 기간·분모가 다르면 다른 분석입니다. 근거/SOP 버전, 승인 인자와 실제 실행, 예측의 시간 분할과 누수를 확인합니다. 조회 성공, 원인 가설, 예측 성능을 구분하며 실행 기록만으로 정확성을 판정하지 않습니다.'),
'S45': ([('Hermes', '갖춰진 Harness에서 상태·기억·도구·정책의 동작을 살펴봤습니다.'), ('PydanticAI', '코드 정의와 내부 Graph, 검증·실행·확장의 연결을 살펴봤습니다.')], '프레임워크가 제공하는 기능을 이해한 뒤 실제 업무의 데이터·권한·검증을 연결해야 합니다. 3차에서는 직접 Agent를 개발하고 같은 기준으로 결과와 시행착오를 검토합니다.'),
}

def apply(slides, env):
    text, box, arrow, group, rule = (env[n] for n in ('text','box','arrow','group','rule'))

    def node(x,y,w,h,title,sub='',color='runtime',size=27):
        return box(x,y,w,h,title,sub,color,size)

    # Cover: a large title balanced by a compact execution loop, no greeting.
    d=text(0,105,'Agent',92,'text',700)+text(0,215,'Framework',92,'text',700)
    d+=text(5,306,'세부 구조를 살펴봅니다',39,'text',700)+text(5,379,'2차 세미나',29,'muted')
    d+=rule(5,440,680,440)+text(5,492,'Hermes',28,'runtime',700)+text(210,492,'Claude Code',28,'runtime',700)+text(495,492,'PydanticAI',28,'runtime',700)
    d+=node(945,90,600,115,'Model','판단과 응답 생성','model',34)
    d+=node(945,285,600,115,'Runtime / Harness','모델 호출 · 도구 실행 · 상태 관리','runtime',34)
    d+=node(945,480,600,115,'Tools & State','외부 작업과 실행 결과','tool',34)
    d+=arrow('M1080 205 V275','model')+arrow('M1080 400 V470','tool')
    d+=arrow('M1545 535 H1605 Q1620 535 1620 520 V162 Q1620 148 1605 148 H1557','context')
    slides['S00'].update(diagram=d,steps=['전체 구성'],kind='cover')

    # Common conceptual architecture, zoned around the execution loop.
    d=text(0,120,'Agent를 이루는',49,'text',700)+text(0,186,'주요 구성요소',49,'text',700)
    d+=text(0,280,'목표와 지침을 읽고',29,'muted')+text(0,327,'모델과 도구를 연결해',29,'muted')+text(0,374,'작업을 이어갑니다.',29,'muted')
    def n(x,y,w,h,t,s='',c='runtime'): return node(x,y,w,h,t,s,c,25)
    d+=group(1,n(545,0,285,93,'User Goal','','context')+n(880,0,350,93,'Instructions','','context')+arrow('M687 93 V143','context')+arrow('M1055 93 V110 Q1055 125 1040 125 H900 Q885 125 885 140 V143','context'))
    d+=group(2,n(545,155,430,120,'Context Builder','지침 · 이력 · 필요한 정보','context')+n(1130,155,410,120,'LLM / Model','판단 · Tool Call · 답변','model')+arrow('M975 200 H1118','model')+arrow('M1130 248 H987','model'))
    d+=group(3,n(545,365,430,120,'Runtime / Harness','반복 · 실행 · 종료','runtime')+n(1130,365,190,120,'Tools','','tool')+n(1415,365,215,120,'Environment','','tool')+arrow('M760 365 V287','context')+arrow('M975 410 H1118','tool')+arrow('M1130 457 H987','tool')+arrow('M1320 410 H1403','tool')+arrow('M1415 457 H1332','tool'))
    d+=group(4,n(545,555,190,88,'State','','context')+n(785,555,290,88,'Memory Store','','context')+arrow('M640 555 V497','context')+arrow('M930 555 V530 Q930 515 945 515 H1020 Q1035 515 1035 500 V310 Q1035 295 1020 295 H930 V287','context'))
    d+=group(5,n(1130,555,240,88,'Guardrails','','risk')+n(1420,555,210,88,'Trace','','muted')+arrow('M1250 555 V540 Q1250 525 1235 525 H1015 Q1000 525 1000 510 V475 H987','risk')+arrow('M1540 500 V543','muted')+text(1330,35,'개념 구성도',22,'muted'))
    # Trace observes the tool/environment lane; guarding is shown at execution.
    d=d.replace('M1540 500 V543','M1523 485 V543')
    slides['S01'].update(diagram=d,steps=['전체 구성','목표와 지침','Context와 모델','실행과 환경','상태와 기억','검사와 기록'])

    # Programme: same 1st/2nd/3rd sequence, three rows for the current seminar.
    d=node(0,0,440,105,'1차 · 공통 개념','','muted',30)+node(590,0,470,105,'2차 · 기술별 세부 구조','','runtime',30)+node(1210,0,440,105,'3차 · 개발·검증·회고','','muted',30)
    d+=arrow('M440 53 H578','line')+arrow('M1060 53 H1198','line')
    rows=[('모델 개발·서빙','AI Studio · vLLM · SGLang','강준혁'),('Agent 개발·워크플로','DeepAgents · LangChain · LangGraph','박건'),('Agent Harness·SDK','Hermes · PydanticAI · OpenAI · Claude','남우성')]
    for i,(category,names,host) in enumerate(rows):
        y=180+i*150
        d+=rule(0,y+120,1652,y+120)+text(20,y+38,category,31,'text',700)+text(20,y+86,names,29,'muted')
        d+=f'<g data-reveal="{i+1}">'+node(1340,y+8,290,92,host,'','runtime',31)+'</g>'
    slides['S02'].update(diagram=d,steps=['세 파트','강준혁','박건','남우성'],reveal=True)

    # Only Hermes and PydanticAI share focus 1; everything else is focus 0.
    d=text(0,35,'Agent Harness',35,'text',700)+text(0,85,'갖춰진 실행환경에서 시작',25,'muted')
    d+=group(1,node(490,0,520,145,'Hermes','범용 Agent Harness','runtime',38))
    d+=group(0,node(1130,0,520,145,'Claude Code','코딩 작업을 위한 Harness','runtime',38))
    d+=rule(0,205,1652,205)+text(0,280,'Agent SDK',35,'text',700)+text(0,330,'코드로 Agent 구성',25,'muted')
    sdk=[('PydanticAI','Pydantic 기반 Agent SDK'),('OpenAI Agents SDK',''),('Claude Agent SDK',''),('Google ADK',''),('Microsoft Agent Framework','')]
    for i,(name,sub) in enumerate(sdk):
        x=490+(i%2)*640;y=255+(i//2)*127
        d+=group(1 if i==0 else 0,node(x,y,520,105,name,sub,'runtime',27 if len(name)>24 else 30))
    slides['S03'].update(diagram=d,steps=['전체 구성','Hermes · PydanticAI'])

    # Hermes section opener: diagram left, section title right, matching request.
    d=node(0,40,1000,100,'입력 경로','CLI · TUI · Gateway · API · ACP','runtime',30)
    d+=node(0,235,600,230,'AIAgent','Prompt 구성 · Agent Loop|Provider 변환 · Tool 실행','runtime',36)
    d+=node(735,210,265,110,'Model','판단과 응답','model',30)+node(735,365,265,110,'Tools','파일 · DB · API','tool',30)
    d+=arrow('M300 140 V223','runtime')+arrow('M600 265 H723','model')+arrow('M735 305 H612','model')+arrow('M600 390 H723','tool')+arrow('M735 450 H612','tool')
    for x,t,sub in [(0,'Session','SQLite · FTS5'),(355,'Memory','MEMORY · USER'),(710,'Skills','절차 · 참고 자료')]:
        d+=node(x,555,290,95,t,sub,'context',29)
    d+=arrow('M145 465 V543','context')+arrow('M500 555 V477','context')+arrow('M855 555 V520 Q855 505 840 505 H650 Q635 505 635 490 V430 H612','context')
    d+=text(1110,240,'Hermes',90,'runtime',700)+text(1115,312,'범용 Agent Harness',33,'text',700)
    d+=rule(1115,365,1652,365)+text(1115,420,'모델과 도구를 연결하고',29,'muted')+text(1115,466,'대화와 작업을 이어가는',29,'muted')+text(1115,512,'실행환경',29,'muted')
    slides['S03H']=dict(slides['S04'],id='S03H',diagram=d,steps=['전체 구조'],kind='section-opening',section='Hermes',demo=None,note='')

    # Six compact capability groups; full feature inventory goes in Sources too.
    capabilities=[
      ('실행 루프','Agent Loop · Tool Calling','취소·중단 · 대체 모델 처리','runtime'),
      ('입력과 출력','CLI · TUI · Desktop','메신저 Gateway · HTTP API · ACP','runtime'),
      ('도구와 확장','터미널·파일·웹·브라우저·코드 실행','Toolsets · MCP · Plugins','tool'),
      ('기억과 검색','SQLite 세션 · FTS5 검색','Memory 파일 · 외부 Memory Plugin','context'),
      ('작업 절차','작업별 Skills · Agent 작성 Skills','Curator로 사용 이력 관리','context'),
      ('위임과 운영','Subagent · Cron · Hooks','승인·격리 · 파일 복구','runtime'),
    ]
    d=''
    for i,(name,a,b,color) in enumerate(capabilities):
        x=(i%2)*870;y=(i//2)*215
        d+=group(i+1,text(x,y+35,name,33,color,700)+text(x,y+92,a,27,'text')+text(x,y+138,b,26,'muted')+rule(x,y+178,x+780,y+178))
    slides['S04'].update(diagram=d,steps=['기본 제공 기능']+[c[0] for c in capabilities])

    # Concise phrasing within the diagrams; preserve code and technical labels.
    replacements={
      '실행 구조와 개발 책임':'Agent Framework 세부 구조',
      '모델의 완료 문장과 업무 성공은 별개':'최종 답변 후에도 업무 검증 필요',
      '지시·History·Deps는 같은 입력이 아닙니다':'모델 입력과 Python 자원',
      '우리의 계약':'업무 적용',
      '상태·기억·정책이 실제로 어떻게 움직이는가':'상태·기억·도구·정책의 동작',
      '검증·실행·최종화·확장을 어떻게 조합하는가':'코드 정의부터 실행과 검증까지',
      '데이터·권한·업무 검증을 어떻게 보장하는가':'데이터·권한·결과 검증',
      '실행 단위':'실행 방식',
      'Core 먼저 → 선택 Harness의 변화 관찰':'Core 실행 → Harness 기능 추가',
      '같은 Tool을 호출했다는 사실만으로 같은 근거·같은 결과를 보장하지 않는다.':'같은 Tool도 데이터와 기준 시점이 다르면 다른 결과를 냅니다.',
      'Python 자원과 모델에 전달하는 정보 사이의 경계를 명시합니다.':'Python 자원에서 모델에 전달할 정보만 선택합니다.',
      '주입':'전달',
      '단일 중앙 Hook이 모든 내부 실행을 관찰한다고 단정하지 않는다.':'Tool마다 관찰할 수 있는 지점이 다릅니다.',
      '실행·정보·정책 경계':'도구·기억·권한',
      '공통 모델 서비스 · 부하·접근 제어':'모델 서비스 · 부하·접근 제어',
      'Claude Code · 공개 동작 계약':'Claude Code · 공개된 실행 구조',
      '지침 파일은 행동을 안내하고, 실제 접근 권한은 실행 계층에서 집행한다.':'실제 접근 권한은 도구와 실행환경에서 확인합니다.',
      '공유 작업 목록 · 실험적 제약 · 조정 비용':'공유 작업 목록 · 실험적 기능 · 조정 비용',
      '지침·Tools·결과 계약':'지침·Tools·출력 형식',
      'sequential=True는 실행 장벽이며 데이터 snapshot·트랜잭션을 만들지는 않는다.':'sequential=True는 실행 순서를 정합니다. 데이터 snapshot은 별도로 관리합니다.',
      'output_type은 최종 결과 계약 · 개별 Tool return type과 목적이 다르다':'output_type은 최종 출력 형식 · Tool return type은 개별 도구의 반환 타입',
      'Tool 쌍·정확 수치·근거 경로를 보존하고 원본 복원을 자동 보장하지 않는다.':'호출 쌍과 수치·근거를 보존하고, 원본은 별도로 보관합니다.',
      'namespace는 저장 범위이며, 인증·DB 접근 권한을 대신하지 않는다.':'namespace로 저장 범위를 나누고, 인증과 DB 권한은 따로 확인합니다.',
      '데이터 계약·보존·삭제':'데이터 형식·보관·삭제',
      '우리 애플리케이션':'업무 애플리케이션',
      '최종 결과는 emission 순서의 첫 유효 Output · 완료가 빠른 순서가 아니다':'최종 결과는 모델이 제안한 순서에서 첫 유효 Output을 선택합니다.',
      '한쪽만 남기는 축약은 피한다':'호출 ID와 결과를 함께 보존',
      '정확한 장비 ID 질의와 표현이 달라진 사례 질의를 나눠 평가한다.':'정확한 장비 ID와 유사 사례 질문으로 검색 결과를 비교합니다.',
    }
    oldcolors={'#60A5FA':'#205BC7','#B794F4':'#6941B8','#34D399':'#087756','#FDBA74':'#9B4F0A','#FB7185':'#BD2845','#5EEAD4':'#087C74','#9EACC8':'#52647B','#33415D':'#7E90A8','#EFF4FF':'#172B46','#080d19':'#F0F4FA','#080D19':'#F0F4FA'}
    for ident,s in slides.items():
        s['originalSpec']=s['note']
        s['title'],s['sub'],s['take']=COPY[ident]
        for a,b in replacements.items(): s['diagram']=s['diagram'].replace(escape(a),escape(b))
        for a,b in oldcolors.items(): s['diagram']=s['diagram'].replace(a,b)
        concepts,explanation=DETAIL[ident]
        s['concepts']=[{'term':a,'meaning':b} for a,b in concepts]
        s['explanation']=explanation
        s['note']='## '+s['title']+'\n\n### 주요 개념\n\n'+'\n\n'.join('**'+a+'**: '+b for a,b in concepts)+'\n\n### 설명\n\n'+explanation+'\n\n### 발표 포인트\n\n'+s['take']
    # Intro programme is user-supplied. Hermes opener retains architecture refs.
    slides['S03H']['sources']=slides['S04']['sources'][:]
    for key in ('H05','H07','H09','H10','H11','H12','H14','H15','H16'):
        if key not in {r[0] for r in slides['S04']['sources']}:
            slides['S04']['sources'].append((key,*env['references'][key]))

LIGHT_STYLE=r'''
/* White stage, dark labels, distinct focus at a glance. */
:root{--stage-bg:#E9EEF5;--slide-bg:#FBFCFF;--text:#172B46;--muted:#52647B;--line:#B7C3D3;--runtime:#6941B8;--context:#9B4F0A;--model:#205BC7;--tool:#087756}
.slide{background:var(--slide-bg)}.section-label{margin-bottom:24px}.section-label:before{background:var(--model)}
h1{font-size:48px;letter-spacing:-1.2px}.subtitle{font-size:27px;margin-top:18px}.takeaway{font-size:26px;border-left-color:var(--model)}
.slide g.dim{opacity:.24}.slide g.highlight{opacity:1}.slide g.highlight .node{fill:#FFF0AD;fill-opacity:1;stroke:#205BC7;stroke-opacity:1;stroke-width:4.5}
.slide g.highlight text{font-weight:700}.slide g.highlight path{stroke-width:3.8}.slide g.highlight .node{filter:drop-shadow(0 3px 5px #1d4ed81c)}
.step-label{border-radius:5px;padding:6px 10px;background:#EDF2FA;color:#344969;min-width:160px}.slide.focus-on .step-label{background:#205BC7;color:white;font-weight:700}
.sources{color:#205BC7;font-weight:700}.controls button:hover{background:#E5EDFD;color:#172B46}.key-hint{color:#344969}
.menu-dialog{background:#FBFCFF;color:#172B46;border-color:#B7C3D3}.menu-dialog button{color:#172B46;border-color:#B7C3D3}.menu-dialog small{color:#52647B}.menu-dialog::backdrop{background:#172b4655}.progress{background:#205BC7}
.cover header,.cover .takeaway,.section-opening header{visibility:hidden}.cover .diagram{top:210px}.section-opening .diagram{top:180px;height:720px}
[data-reveal]{visibility:hidden;opacity:0;transition:opacity .18s}[data-reveal].revealed{visibility:visible;opacity:1}
.sources-dialog{width:min(1000px,92vw);max-height:86vh;border:1px solid #B7C3D3;border-radius:12px;background:#FBFCFF;color:#172B46;padding:0;box-shadow:0 20px 90px #172b4633;font:17px/1.8 'Seminar Korean',sans-serif;overflow:auto}
.sources-dialog::backdrop{background:#172b4666}.sources-dialog header{padding:24px 34px;background:#EFF4FD;border-bottom:1px solid #CBD5E4}.sources-dialog h2{font-size:27px;line-height:1.5;margin:5px 60px 4px 0}.sources-dialog .reader-meta{font-size:14px;color:#52647B}.sources-dialog .reader-close{position:absolute;right:20px;top:20px;border:1px solid #A8B7CE;background:white;color:#172B46;padding:7px 13px;border-radius:5px;cursor:pointer}.sources-dialog main{padding:8px 34px 30px}.sources-dialog h3{font-size:20px;margin-top:25px}.sources-dialog dt{font-weight:700;color:#205BC7;margin-top:16px}.sources-dialog dd{margin:4px 0 0}.sources-dialog p{margin:12px 0;overflow-wrap:anywhere}.sources-dialog a{color:#205BC7}.sources-dialog ul{padding-left:22px}.sources-dialog button:focus-visible,.sources-dialog a:focus-visible{outline:3px solid #205BC7;outline-offset:3px}
@media print{.sources-dialog{display:none!important}[data-reveal]{visibility:visible!important;opacity:1!important}.cover header,.cover .takeaway,.section-opening header{visibility:hidden!important}.slide g.dim{opacity:1!important}.slide g.highlight .node{filter:none;fill-opacity:.08;stroke-width:1.6}}
'''
