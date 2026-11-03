"""SDK comparison chapters following the PydanticAI walkthrough."""

TOPICS = {
    'CAS': ('Claude Agent SDK', '0.2.177', 'anthropics/claude-agent-sdk-python', 'v0.2.177',
            'src/claude_agent_sdk/', 'Claude_Agent_SDK', 'Claude_Agent_SDK',
            'https://platform.claude.com/cookbook/claude-agent-sdk-01-the-chief-of-staff-agent'),
    'ADK': ('Google ADK', '2.13.0', 'google/adk-python', 'v2.13.0',
            'src/google/adk/', 'Google_ADK', 'Google_ADK', 'https://adk.dev/runtime/'),
    'MAF': ('Microsoft Agent Framework', '1.24.0', 'microsoft/agent-framework', 'python-1.24.0',
            'python/packages/core/agent_framework/', 'Microsoft Agent_Framework', 'Microsoft_Agent_Framework',
            'https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/checkpoints?pivots=programming-language-python'),
    'OAI': ('OpenAI Agents SDK', '0.24.0', 'openai/openai-agents-python', 'v0.24.0',
            'src/agents/', 'OpenAI_Agents_SDK', 'OpenAI_Agents_SDK',
            'https://openai.github.io/openai-agents-python/running_agents/'),
}

# title / subtitle / three visible rows / takeaway / speaker detail / tagged sources
CONTENT = '''
CAS|Claude Agent SDK의 프로세스 경계|Claude Code 실행환경을 Python 업무 앱에 연결합니다.|Python 앱~query()와 설정·콜백 정의~SDK가 CLI 명령 구성|Claude CLI~작업 폴더에서 모델·도구 실행~CLI 내부 루프는 공개 계약으로 설명|메시지와 제어~stdout 메시지는 앱이 소비~권한·SDK MCP 요청은 Python으로 전달|CLI 버전과 작업 환경까지 배포 계약에 포함됩니다.|SDK 공개 범위에서 SubprocessCLITransport._build_command와 Query._handle_control_request를 읽는다. 실행 환경의 파일·셸을 활용하기 쉽지만 운영 격리와 CLI 버전의 영향을 받는다.|query.py _internal/transport/subprocess_cli.py#L570 _internal/query.py#L606
CAS|단발 요청과 대화형 클라이언트|같은 LOT 조회에서 입력과 연결 수명을 비교합니다.|query()~비동기 메시지 반복자~한 번의 실행 흐름을 소비|ClaudeSDKClient~connect → query → receive_response~연결을 유지하며 후속 입력 전달|결과 처리~ResultMessage와 오류 확인~연결 수명은 앱에서 관리|두 API 모두 결과 메시지를 끝까지 소비합니다.|SDK 클라이언트의 async with 범위 안에서 질문과 후속 질문을 전송할 수 있다. SDK 메시지 타입과 CLI 세션 수명은 별도로 추적한다.|query.py client.py types.py
CAS|Python 조회 함수를 SDK MCP로 연결|LOT-A 조회의 실제 실행 위치를 따라갑니다.|Python 등록~@tool + create_sdk_mcp_server~업무 함수는 호스트 프로세스에 존재|Claude CLI~mcp__lot__read_lot 호출 요청~SDK의 control 채널로 전달|Python 디스패치~_handle_sdk_mcp_request~함수 결과를 CLI로 반환|PydanticAI의 직접 함수 등록과 호출 경계가 다릅니다.|SDK MCP는 Python 프로세스 안에서 함수를 실행한다. 외부 stdio/HTTP MCP는 별도 서버 경계를 가진다. 샘플의 권한 있는 범위는 앱에서 주입하는 fixture다.|__init__.py _internal/query.py#L782
CAS|작업 환경과 도구 권한|CLI 정책과 LOT 데이터 인가를 구분합니다.|작업 환경~cwd와 setting_sources 지정~프로젝트 설정 로딩 범위 확인|호출 정책~도구 목록·permission mode~Hook과 can_use_tool 개입점 확인|데이터 인가~read_lot 내부에서 LOT 범위 검사~CLI 허용 이후에도 검증|권한 콜백에서 거절한 호출은 업무 함수 실행 0회를 기대합니다.|Python 기본값은 permission_mode=None, max_turns=None, setting_sources=None이다. 이는 옵션 값이며 실효 권한 모드나 CLI 턴 한도와 분리한다. 파일 설정 사용은 명시적으로 설정하고 런타임별 sandbox 조건을 확인한다. Subagent·Plugin은 Sources에서 읽는다.|types.py#L2393 _internal/transport/subprocess_cli.py#L570 _internal/query.py#L606
CAS|세션 재개와 산출물 버전|세션을 이어도 LOT 보고서의 근거는 별도로 확인합니다.|세션~session_id로 대화 재개~fork는 대화 분기|작업 환경~cwd와 실제 파일 상태 확인~실행 파일과 산출물을 따로 식별|업무 근거~LOT-A · snapshot r3 · 92/100~보고서 revision과 저장 위치 기록|대화 이력과 업무 근거의 식별자를 함께 기록합니다.|CLI에 전달하는 resume/fork 옵션과 앱의 파일 버전 계약을 따로 설명한다. 파일 checkpointing/rewind는 별도 지원 조건을 확인해야 한다.|types.py _internal/transport/subprocess_cli.py
CAS|스트림과 구조화 결과|앱은 메시지 스트림을 읽고 업무 결과를 검증합니다.|StreamEvent~부분 메시지는 기본 비활성~include_partial_messages=False|ResultMessage~종료 subtype과 structured_output~실행 결과와 JSON 결과 구분|앱 검증~허용 LOT·snapshot·수율 재확인~검증 후 저장 또는 실패 기록|구조화된 JSON에도 LOT와 원본 버전 검증이 필요합니다.|output_format의 JSON Schema와 앱 업무 규칙을 따로 둔다. 예시에는 조회 1건과 권한 거절 1건을 사용한다. CLI가 보고한 오류 subtype과 앱 검증 실패를 다른 로그로 남긴다.|types.py _internal/transport/subprocess_cli.py
ADK|Runner와 이벤트 스트림|한 invocation에서 응답과 상태 변경 이벤트를 함께 읽습니다.|호스트~Runner.run_async() 호출~user_id와 session_id 전달|Agent 실행~BaseLlmFlow가 모델·함수 처리~이벤트로 진행을 전달|세션 서비스~Runner가 저장 후보 이벤트 처리~클라이언트에도 이벤트 전달|이벤트는 진행 관찰과 상태 기록에 모두 쓰입니다.|런타임 진입점은 Runner다. 앱의 세션 식별자와 실행 invocation을 분리한다. 인메모리 서비스는 실습용으로 적합하며 저장 수명은 서비스 구현에 따라 달라진다.|runners.py flows/llm_flows/base_llm_flow.py
ADK|함수 응답과 상태 반영|Tool 응답이 모델과 세션에 전달되는 경로를 추적합니다.|모델~FunctionCall에 도구 이름·인자~LLM flow에서 실행으로 연결|Tool~FunctionResponse와 state_delta~응답 내용과 변경값을 분리|Runner → SessionService~부분 이벤트 등을 선별~append_event에서 상태 반영|부분 스트림과 저장된 이벤트는 서로 다른 목록입니다.|Runner._process_and_append_event는 partial 및 저장 조건을 검사한다. BaseSessionService.append_event에서 state delta를 적용하는 경로를 확인한다. fixture의 응답은 good=92, total=100이다.|flows/llm_flows/base_llm_flow.py runners.py#L1536 sessions/base_session_service.py#L166
ADK|Session·State·Memory·Artifact|하나의 분석에서 저장 대상을 나눕니다.|Session과 State~대화 이벤트와 업무 값~app: / user: / 세션 / temp: 구분|Memory~이전 정보의 검색 경로~세션 이력과 별도 서비스|Artifact~보고서 파일과 버전~상태에는 참조 식별자 기록|상태 스코프와 실제 저장 서비스가 데이터 수명을 결정합니다.|temp: 값은 invocation용으로 취급한다. 보고서 바이트와 저장된 이벤트를 동일 저장물로 간주하지 않는다. context compaction·prefix caching은 모델 입력 비용과 관련된 별도 기능이다.|sessions/base_session_service.py runners.py
ADK|Agent 전이와 고정 순서|다음 단계를 고르는 위치에 따라 실행을 선택합니다.|AgentTool~부모 Agent가 결과를 받아 계속 실행~도구로 하위 Agent 호출|Agent transfer~모델이 전이 요청~대상 Agent로 실행 흐름 연결|Workflow Agent~Sequential / Parallel / Loop~코드에서 단계 배치|모델에 맡기는 선택과 업무 순서를 코드에서 정하는 선택을 구분합니다.|조회·계산·승인의 순서가 업무 계약이면 실행 모델에 드러낸다. ADK 2.x Graph는 다음 장에서 별도 실행 경로로 설명한다.|agents/sequential_agent.py agents/parallel_agent.py flows/llm_flows/base_llm_flow.py
ADK|ADK 2.x Graph 스케줄러|업무 그래프에서 준비된 노드가 실행되는 지점을 읽습니다.|Node와 Edge~조회 → 병렬 분석 → 검증~입력 의존성과 시작 조건 선언|_schedule_ready_nodes()~준비 조건과 동시 실행 한도 확인~선택된 노드 작업 시작|_emit_node_checkpoint()~노드 진행 상태 기록 경로~재실행·복구 조건은 별도 확인|PydanticAI 내부 루프 Graph와 ADK 업무 Graph는 역할이 다릅니다.|Workflow._run_loop를 중심으로 준비된 노드 스케줄과 노드 체크포인트를 설명한다. 장표의 LOT 그래프는 업무 설계 예시다. 체크포인트를 전체 Python 프로세스 스냅샷으로 해석하지 않는다.|workflow/_workflow.py#L305
ADK|답변 완료와 발행 완료|보고서 저장에 실패하는 조건으로 업무 종료를 확인합니다.|응답 이벤트~모델이 수율 92%를 설명~is_final_response() 판정|저장 시도~Artifact 저장 실패 주입~발행 완료 상태 기록 보류|검수 기록~실제 남은 이벤트와 Artifact 조회~발행 횟수 0회 기대|최종 응답과 업무 완료를 서로 다른 조건으로 검사합니다.|고정 모델 응답에서 답변 이벤트는 수집하되 발행 상태는 앱에서 저장 성공 이후 기록하도록 설계한다. 예제의 실패 기대값이며 SDK 재시도나 원자성을 가정하지 않는다.|events/event.py runners.py#L1536
ADK|실행 설정과 이벤트 검증|LLM 호출 한도와 로컬 재현 조건을 함께 기록합니다.|RunConfig~streaming_mode=NONE~max_llm_calls 기본 500|환경·실행 경로~ADK_MAX_LLM_CALLS로 기본값 변경~Live 호출 한도는 별도 검토|이벤트 시험~모델 응답 고정 · 실제 Runner 사용~state_delta와 산출물 참조 검증|테스트는 고정 모델 응답과 실제 서비스 연동을 구분합니다.|Callback과 Plugin 개입은 어떤 이벤트 또는 호출을 변경하는지 함께 기록한다. Live, 평가, 관리형 배포는 공식 가이드의 지원 범위를 별도로 확인한다.|agents/run_config.py runners.py
MAF|Agent 실행과 업무 Workflow|조회 Agent 한 번의 run을 업무 그래프에 넣습니다.|Workflow~조회 → 분석 → 승인 → 발행~Executor와 Edge로 단계 제어|AgentExecutor~Agent를 한 Executor로 사용~내부 모델·도구 루프 실행|상태 경계~AgentSession은 대화 상태~Workflow는 메시지·복구 위치 관리|업무 순서와 복구 조건을 그래프에 드러낼 수 있습니다.|WorkflowBuilder와 Workflow.run이 바깥 실행이다. AgentSession과 Workflow checkpoint를 각각 저장할 이유가 있다. .NET과 Foundry 배포 기능은 Python 코드와 구분한다.|_workflows/_workflow_builder.py _workflows/_workflow.py
MAF|Executor와 Edge의 메시지 계약|업무 단계 사이에서 값의 타입과 의미를 검사합니다.|보내는 단계~Executor가 LOT 결과를 보냄~LOT-A · r3 · 측정 요약|Edge~다음 Executor로 라우팅~필요한 경우 분기 조건 적용|받는 단계~입력 타입 및 업무 계약 확인~snapshot 불일치 시 중단|타입이 맞아도 LOT와 snapshot이 일치하는지 확인합니다.|WorkflowBuilder에서 연결한 Edge는 워크플로의 연결 계약이다. SDK 실행 계약에 더해 앱이 최신 데이터와 업무 키를 검사한다.|_workflows/_workflow_builder.py _workflows/_workflow.py
MAF|AgentExecutor의 입력과 출력|워크플로 메시지가 Agent.run 인자로 바뀌는 경로입니다.|from_message()~Message를 핸들러가 받음~Agent 실행 입력으로 전달|_run_agent_and_emit()~Agent 응답 및 사용자 입력 요구 처리~대화 Session과 실행 연결|후속 Executor~AgentExecutorResponse 전달 경로~출력 이벤트를 업무 데이터와 구분|AgentExecutor는 워크플로와 Agent 실행 계약을 연결합니다.|str, Message 및 메시지 목록 등 입력 경로가 있다. Agent가 생성한 결과와 호출자가 소비하는 이벤트 및 다음 단계의 데이터 타입을 구별한다.|_workflows/_agent_executor.py#L447
MAF|병렬 결과를 결합하는 업무 키|온도·압력 분석의 도착 순서를 바꿔 검증합니다.|Fan-out~같은 LOT-A / r3 전달~온도와 압력 Executor에 분배|Fan-in~업무 키로 결과를 결합~LOT + snapshot + 분석 종류|검증~지연·중복·r4 혼입 시도~r3 결과만 보고서에 사용|도착 순서와 업무상 결합 기준을 분리합니다.|SDK가 제공하는 fan-in 경로와 결합 데이터의 업무 검증은 별개다. 같은 키의 중복, 서로 다른 snapshot 혼입, 한 결과 누락을 각각 검증한다.|_workflows/_workflow_builder.py _workflows/_workflow.py
MAF|승인 대기와 응답 연결|승인 요청 ID와 보고서 revision을 묶습니다.|요청~Workflow가 사용자 입력 대기~요청 ID와 LOT-A / r3 기록|응답~같은 요청 ID로 응답을 전달~승인 대상·권한 재확인|재개~r4를 발행하려는 경우 보류~새 보고서 버전으로 재승인|r3 승인으로 r4 발행이 0회인지 확인합니다.|Workflow의 일반 외부 요청과 AgentExecutor의 도구 승인 중계 경로를 구분한다. 업무 승인 범위와 만료, 요청 ID 대응은 호스트 계약이다.|_workflows/_workflow.py _workflows/_agent_executor.py#L473
MAF|체크포인트와 외부 발행 복구|어디에서 복구해도 발행이 한 번인지 검사합니다.|Entry checkpoint~초기 입력·응답 전달 시점~Python 1.13.0부터 추가|Superstep 완료~Executor 상태·다음 메시지 등~저장소 지정 시 복구 가능|외부 발행~멱등 키로 재실행 검증~업무 저장소에서 중복 확인|업무 발행의 중복 방지는 외부 저장소까지 포함합니다.|checkpoint_storage 기본 None. 인메모리는 프로세스 내 확인, 파일 저장은 재시작 확인에 사용한다. 체크포인트 스키마와 외부 부작용이 별개이므로 발행에 idempotency key를 둔다.|_workflows/_workflow.py#L712 _workflows/_checkpoint.py
MAF|Agent와 명시적 Executor의 배치|업무에서 판단을 위임할 곳과 검증을 고정할 곳을 나눕니다.|Agent~분석 근거 요약~불확실한 서술과 설명 생성|Executor~수율 재계산 · 승인 범위 검사~고정 업무 규칙 실행|저장·발행~보고서 revision과 키 기록~복구와 중복 처리 시험|명시적인 그래프에는 메시지와 저장소 관리 비용이 따릅니다.|빌더는 반복되는 orchestration의 시작점이다. Agent/Function middleware, context provider, Foundry 연동과 .NET은 기능별 지원 범위를 Sources에서 분리한다.|_workflows/_workflow_builder.py _workflows/_agent_executor.py
OAI|Runner가 한 턴을 해석하는 방식|PydanticAI의 내부 Graph와 비교해 다음 상태를 읽습니다.|모델 호출~활성 Agent와 입력으로 요청~Runner가 응답 분류|도구·handoff~도구 실행 또는 활성 Agent 교체~다음 입력과 상태 구성|종료~최종 출력 또는 한도·중단~기본 max_turns=10|한 턴은 모델 호출과 그 턴의 도구 처리를 포함합니다.|Runner.run의 진입과 turn_resolution의 후속 상태 결정 경로를 짚는다. max_turns=None은 턴 한도를 비활성화한다. 모델 호출과 Tool 횟수는 각각 기록한다.|run.py run_config.py run_internal/turn_resolution.py
OAI|도구 결과로 종료하는 정책|같은 조회 응답으로 후속 모델 호출 유무를 비교합니다.|run_llm_again~기본값 · Tool 결과를 모델에 전달~모델이 후속 출력 작성|stop_on_first_tool~함수 도구 결과를 최종값으로 선택~실행된 도구 목록은 별도 기록|StopAtTools / callable~특정 이름 또는 결과 조건 사용~종료 판단 위치 확인|최종값 선택과 실행된 Tool 수를 각각 측정합니다.|_maybe_finalize_from_tool_results와 도구 결과 선택 함수를 함께 읽는다. 함수 도구 결과의 종료 정책과 PydanticAI EndStrategy가 적용되는 출력 경로를 구분한다. 두 도구가 제안된 턴에서 최종값과 실제 실행 횟수를 함께 기록한다.|agent.py run_internal/turn_resolution.py#L785
OAI|Agent.as_tool과 handoff|전문가의 답변을 받는 경우와 실행 주체를 바꾸는 경우입니다.|Agent.as_tool()~하위 Agent가 실행되고 결과 반환~부모가 계속 응답|handoff()~Runner가 활성 Agent 변경~이후 Agent가 답변 책임을 가짐|입력 이력~handoff input_filter 적용 가능~모델 입력과 저장 이력 구분|누가 최종 응답을 생성하는지 추적으로 확인합니다.|Agent.as_tool의 중첩 실행과 execute_handoffs를 대비한다. 입력 필터와 다음 Agent에 전달되는 이력을 확인하고, 중첩 Agent 승인 전파는 보충 해설에 둔다.|agent.py run_internal/turn_resolution.py#L544
OAI|Session과 RunState의 저장 경계|이전 대화와 멈춘 실행을 이어받는 입력을 구분합니다.|Session~클라이언트가 관리하는 대화 이력~다음 Run의 입력 구성|RunState~중단된 Run의 진행 상태~승인 결정 후 Runner에 전달|Responses API 식별자~conversation_id / previous_response_id~공급자 쪽 대화 연결|다음 대화와 중단된 실행은 서로 다른 저장 계약을 가집니다.|업무 보고서·승인 이력은 앱이 별도로 보관한다. 관리되는 대화 기능에는 provider 전제가 있다. RunState는 멈춘 실행의 재개에 쓰고 중복 발행 제어는 업무 키로 처리한다.|run.py run_state.py
OAI|Guardrail과 Tool 승인|검사 지점과 실행 대기 지점을 분리합니다.|Agent 검사~첫 Agent 입력 · 최종 Agent 출력~병렬 입력 검사는 호출 시작 가능|Function Tool 검사~도구 입력·출력 경계~handoff 경로와 구분|Approval~보류 후 RunState 승인·재개~외부 발행 전 업무 범위 확인|승인 전후의 실제 Tool 실행 횟수를 확인합니다.|입력 guardrail의 선행 실행을 선택할 수 있다. Tool guardrail은 function-tool 경로에 적용되며 기본 승인 순서와 사전 검사 옵션을 구분한다. 전역 업무 인가를 별도로 검증한다.|run.py run_internal/tool_execution.py run_state.py
OAI|Trace에서 실행 주체 확인|동일 LOT 요청의 모델·도구·전이 기록을 연결합니다.|Trace~한 업무 실행의 관찰 단위~Agent 및 generation span|전이와 도구~handoff / function span~전이 전후 활성 Agent 확인|수집 설정~RunConfig에서 tracing 제어~민감 데이터 포함 여부 명시|Trace 설정과 업무 감사 기록의 저장 정책을 분리합니다.|tracing_disabled의 RunConfig 기본값은 False이며 전역 설정도 영향을 준다. trace_include_sensitive_data는 환경 기반 기본값을 읽는다. 화면에는 합성 데이터와 명시적 민감 데이터 제외 설정을 사용한다.|run_config.py run_internal/tool_execution.py
OAI|고정 모델 응답으로 실행 비교|SDK 규칙과 자연 모델의 선택을 분리해 검증합니다.|Tool 종료 비교~같은 응답으로 정책만 변경~모델 횟수·도구 횟수 비교|Agent 협업 비교~부모 반환과 handoff 비교~최종 Agent·전달 이력 확인|중단과 재개~승인 전후 RunState 추적~발행 중복 여부 별도 검증|작은 API로 조합할 수 있고, 이력과 저장소 선택이 실행 계약을 바꿉니다.|시연의 기준 입력은 LOT-A, snapshot r3, 92/100이다. Hosted tools, MCP, Realtime 및 sandbox·skills는 지원 API 및 provider 전제가 다른 별도 기능이다. 장표에는 실험 설계와 예상 관찰값을 제시한다.|run.py agent.py run_state.py
'''.strip()

ORDER = ['SDKMAP']
for prefix in TOPICS:
    count = sum(row.startswith(prefix + '|') for row in CONTENT.splitlines())
    ORDER.extend(f'{prefix}{number:02}' for number in range(1, count + 1))

ALIASES = {'S39': 'OAI01', 'S40': 'CAS01', 'S41': 'ADK01', 'S42': 'MAF01'}

CODE = {
    'CAS02': """async for message in query(prompt=prompt, options=options):
    if isinstance(message, ResultMessage):
        print(message.subtype)

async with ClaudeSDKClient(options=options) as client:
    await client.query(prompt)
    async for message in client.receive_response():
        if isinstance(message, ResultMessage):
            print(message.subtype)""",
    'CAS03': """@tool("read_lot", "Read an allowed LOT", {"lot_id": str})
async def read_lot(args):
    report = read_allowed_lot(args["lot_id"])
    return {"content": [{"type": "text", "text": report}]}

server = create_sdk_mcp_server(name="lot", tools=[read_lot])
options = ClaudeAgentOptions(
    mcp_servers={"lot": server},
    allowed_tools=["mcp__lot__read_lot"],
)""",
    'ADK01': """runner = Runner(agent=agent, app_name="yield_demo",
                session_service=session_service)
await session_service.create_session(
    app_name="yield_demo", user_id="operator", session_id="r3")
async for event in runner.run_async(
    user_id="operator", session_id="r3", new_message=message
):
    print(event.author, event.actions.state_delta)""",
    'ADK07': """config = RunConfig(max_llm_calls=3)
async for event in runner.run_async(
    user_id="operator",
    session_id="r3",
    new_message=message,
    run_config=config,
):
    if event.is_final_response():
        print(event.author)""",
    'MAF02': """builder = WorkflowBuilder(start_executor=read_lot)
builder.add_edge(read_lot, analyze)
builder.add_edge(analyze, approve)
builder.add_edge(approve, publish)
workflow = builder.build()

async for event in workflow.run(request, stream=True):
    print(event.type)""",
    'MAF06': """storage = FileCheckpointStorage("./checkpoints")
builder = WorkflowBuilder(
    start_executor=read_lot, checkpoint_storage=storage
)
builder.add_edge(read_lot, analyze)
workflow = builder.build()
await workflow.run(request)
checkpoints = await storage.list_checkpoints(
    workflow_name=workflow.name
)""",
    'OAI02': """agent = Agent(
    name="Yield analyst",
    tools=[read_lot],
    tool_use_behavior="run_llm_again",
)
normal = await Runner.run(agent, prompt)
direct = await Runner.run(
    agent.clone(tool_use_behavior="stop_on_first_tool"), prompt
)""",
    'OAI03': """manager = Agent(
    name="Manager", tools=[expert.as_tool(
        tool_name="ask_expert", tool_description="Summarize LOT"
    )]
)
triage = Agent(
    name="Triage", handoffs=[handoff(expert, input_filter=filter_history)]
)
result = await Runner.run(triage, prompt)
print(result.last_agent.name)""",
    'OAI05': """@function_tool(needs_approval=True)
async def publish_report(lot: str, revision: str) -> str:
    return await publish_once(lot, revision)

result = await Runner.run(agent, prompt)
if result.interruptions:
    state = result.to_state()
    for item in result.interruptions:
        if approved_for_r3(item):
            state.approve(item)
    result = await Runner.run(agent, state)""",
}

FLOWS = {
    'CAS01': [('Python 앱', 'query() · 설정', 'context'),
              ('SDK transport', 'CLI 인자 · 연결', 'runtime'),
              ('Claude CLI', '모델 · 도구 실행', 'model'),
              ('Python 앱', '이벤트 · 결과 소비', 'tool')],
    'ADK02': [('모델', 'FunctionCall', 'model'),
              ('Tool', '응답 · state_delta', 'tool'),
              ('Runner', '저장 조건 검사', 'runtime'),
              ('SessionService', 'append_event()', 'context')],
    'ADK05': [('조회', 'LOT-A / r3', 'context'),
              ('분석 노드', '준비된 작업 실행', 'runtime'),
              ('검증', '결과 · 상태 확인', 'tool')],
    'MAF01': [('조회 Agent', '내부 Tool loop', 'model'),
              ('분석 Executor', '측정 데이터 검증', 'runtime'),
              ('승인 Executor', '입력 대기', 'context'),
              ('발행 Executor', '업무 저장소', 'tool')],
    'MAF05': [('승인 요청', '요청 ID · r3', 'runtime'),
              ('응답 대기', '실행 보류', 'context'),
              ('응답 연결', '권한 · revision 검사', 'tool'),
              ('재개', 'r4면 재승인', 'risk')],
    'OAI01': [('활성 Agent', '모델에 요청', 'model'),
              ('Runner', '응답 분류', 'runtime'),
              ('후속 상태', 'Tool / handoff / 종료', 'context')],
}

def revise(slides, drawing):
    table, text, code_panel, rule, chain = (
        drawing[key] for key in ('table', 'text', 'code_panel', 'rule', 'chain')
    )

    def add(ident, title, subtitle, rows, takeaway, detail, refs, evidence, section, version):
        snippet = CODE.get(ident)
        if snippet:
            diagram = code_panel(0, 48, 1050, 517, snippet,
                                 caption='Python API 발췌 · import와 업무 정의 생략', size=19)
            for index, (name, first, second) in enumerate(rows):
                y = 106 + index * 155
                diagram += text(1090, y, name, 27, 'context', 700)
                diagram += text(1090, y + 45, first, 22, 'text')
                diagram += text(1090, y + 80, second, 22, 'muted')
                if index < 2:
                    diagram += rule(1090, y + 112, 1652, y + 112)
            detail += '\n\nPython API 발췌입니다. 앱 정의와 import를 생략했습니다.\n\n```python\n' + snippet + '\n```'
        elif ident in FLOWS:
            flow = FLOWS[ident]
            width = 340 if len(flow) == 4 else 440
            diagram = chain(flow, y=45, w=width, gap=75, h=142,
                            start=(1652 - len(flow) * width - (len(flow) - 1) * 75) // 2)
            diagram += table(('실행 지점', '관찰할 동작', '확인할 조건'), rows,
                             [465, 590, 597], y=247, row_h=108)
        else:
            diagram = table(('실행 지점', '관찰할 동작', '확인할 조건'), rows, [465, 590, 597], y=90, row_h=140)
        slides[ident] = dict(
            id=ident, title=title, sub=subtitle, diagram=diagram, take=takeaway,
            steps=['전체 구성'], section=section, version=version, kind='content-slide',
            note=detail, explanation=detail, sources=refs, localEvidence=evidence,
            concepts=[dict(term=name, meaning=f'{action} · {condition}')
                      for name, action, condition in rows],
        )

    add('SDKMAP', 'SDK 실행 경계 비교', 'PydanticAI의 LOT-A 조회를 네 SDK에서 이어갑니다.',
        [('실행 주체', 'Claude CLI · ADK Runner', '호스트와 Agent 런타임의 경계'),
         ('업무 제어', 'ADK Graph · Microsoft Workflow', '이벤트 반영과 단계 복구'),
         ('한 턴의 분기', 'OpenAI Runner', '도구 결과 · 종료 · 활성 Agent')],
        '공통 입력은 LOT-A, snapshot r3, 양품 92 / 전체 100입니다.',
        'PydanticAI의 Agent 선언·Tool 실행·출력 정책을 기준으로 Claude Agent SDK, Google ADK, Microsoft Agent Framework, OpenAI Agents SDK를 차례로 비교합니다. 네 편의 실패 장면은 합성 입력을 사용한 설명이며 라이브 실행 결과는 아닙니다.',
        [(prefix, name, docs) for prefix, (name, _, _, _, _, _, _, docs) in TOPICS.items()],
        [], 'SDK 비교', 'Python')

    for ident, row in zip(ORDER[1:], CONTENT.splitlines(), strict=True):
        prefix, title, subtitle, *fields = row.split('|')
        *rows, takeaway, detail, paths = fields
        name, version, repo, tag, base, folder, stem, docs = TOPICS[prefix]
        refs = [(f'{ident}-{index}', path, f'https://github.com/{repo}/blob/{tag}/{base}{path}')
                for index, path in enumerate(paths.split(), 1)]
        refs.append((f'{ident}-DOC', f'{name} 공식 가이드', docs))
        evidence = [dict(path=f'study/{folder}/{stem}{suffix}.md', sections=section)
                    for suffix, section in (('', '기본 학습 문서'),
                                            ('_2차_심층_학습_분석', '심층 소스 분석'),
                                            ('_발표_실무_시사점_코멘트', '발표 실무 시사점'))]
        add(ident, title, subtitle, [tuple(item.split('~')) for item in rows],
            takeaway, detail, refs, evidence, name, f'Python {version}')
