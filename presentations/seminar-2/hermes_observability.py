"""Source-scoped guardrails and observability slides; no runtime instrumentation is installed."""
IDS=['HSAFE','HGUARD','HGUARDFLOW','HGUARDCONFIG','HHOOK','HTRACEBASE','HOBSERVER','HTRACECODE','HTRACEUSE','HTRACESHARE']

def extend(slides,env,put,code,notes,chain,divider):
    text,box,group,rule=(env[n] for n in ('text','box','group','rule'))
    divider('HSAFE','안전장치와 실행 기록','실행을 제한하는 판단과 실행을 설명하는 기록을 연결합니다.',['기본 보호 장치','반복·정책 제어','Trace 수집·활용'])
    section='안전장치와 실행 기록'

    d=chain([('실행 통제','명령의 floor·smart/manual 승인|Tool 범위·Hook·반복 감지','runtime'),('파일·입력 보호','민감 경로·지침 파일 쓰기 검사|URL 제한·비밀값 마스킹','context'),('격리와 복구','terminal.backend 기본 local|Checkpoint는 기본 off','tool')],y=60,h=230,connect=False)
    d+=group(4,box(0,455,1650,145,'하나의 만능 Guardrail이 있는 구조는 아닙니다','승인·파일 검사·OS 권한·반복 감지는 적용 위치와 실패 방식이 다릅니다.','risk',31))
    put('HGUARD','Hermes의 기본 안전장치는 어디에 있을까?','명령 승인 외에도 서로 다른 경계에서 실행을 제한합니다.','기본 local 실행의 권한과 격리 환경의 권한을 구분해 설정합니다.',section,d,
        ['실행 통제','파일·입력 보호','격리·복구','각 경계의 역할'],
        [('실행 승인','명령 패턴·hardline floor·기존 승인·smart/manual 경로를 처리합니다.'),('파일 보호','민감 경로와 config, 프로젝트 지침 파일에 대한 별도 검사입니다.'),('격리','backend 기본 local은 자동 컨테이너 격리가 아닙니다. Checkpoint 기본값도 false입니다.')],
        'DEFAULT_CONFIG를 대조하면 terminal.backend=local, approvals.mode=smart, security.allow_private_urls=false, security.redact_secrets=true, security.protected_instruction_files=true, checkpoints.enabled=false입니다. dangerous command approval은 이미 앞 장에서 본 별도 경로이며, 여기서는 전체 보호 지점을 묶어 봅니다.\n\nfile_tools_write_guards는 raw NT/device 경로와 정규화/실제 경로, 민감 시스템 경로·Hermes config를 검사합니다. 프로젝트의 AGENTS.md/CLAUDE.md/SOUL.md/.cursorrules와 .hermes 지침은 별도 일회 승인 경로이고, yolo와 무인 실행 예외도 구분합니다. HERMES_WRITE_SAFE_ROOT로 추가 쓰기 범위를 제한할 수 있지만 일반 파일 Tool 보호가 임의 Python·Shell·외부 MCP의 모든 쓰기를 동일하게 가두는 OS sandbox는 아닙니다.\n\n활용할 때는 필요한 backend와 파일/네트워크 범위, 승인 가능한 표면을 먼저 정하고, 업무 규칙은 Handler/Backend 또는 명시적인 정책 확장으로 더합니다. 지침 텍스트는 실행 권한 검사의 대체물이 아닙니다.',
        ['defaults','fileguard','approval','securitydoc'])

    d=code(0,40,1040,550,'# 실제 Controller 메서드를 연결한 축약\nd = agent._tool_guardrails.before_call(name, args)\nif d.allows_execution:\n    result = execute(args)\n    after = agent._tool_guardrails.after_call(\n        name, args, result\n    )\n    seen = agent._tool_guardrails.observe_call(...)\n# warn: 결과에 안내 추가\n# block/halt: Runtime이 실행/반복 중단 처리',caption='tool_guardrails.py + tool_executor.py · 변수/래퍼 축약',size=22)
    d+=notes([('호출 식별','Tool 이름 + canonical args → hash|턴마다 실패·반복 카운터 초기화','context'),('실행 전','before_call: cap·이전 실패 확인|허용 / 차단 결정','runtime'),('실행 후','after_call + observe_call|실패·동일 결과·순환 패턴 관찰','tool')],x=1120,w=530)
    put('HGUARDFLOW','반복되는 Tool 호출을 코드에서 감지하기','한도 검사와 실행 결과 관찰이 서로 다른 시점에 동작합니다.','실패를 몇 번 했는지뿐 아니라 그 사이에 진전이 있었는지를 봅니다.',section,d,
        ['호출 식별','실행 전','실행 후'],
        [('Signature','Tool 이름과 정규화 인자의 hash로 동일 호출을 식별합니다.'),('실행 전/후','before_call은 cap/반복 차단, after_call은 실패·진전 카운터, observe_call은 동일 streak·cycle을 관찰합니다.')],
        'ToolCallGuardrailController는 reset_for_turn으로 상태를 초기화합니다. before_call은 먼저 web_search/subagent cap을 검사하고, hard_stop_enabled일 때 변경 없는 동일 실패나 idempotent 결과 반복을 차단합니다. tool_executor의 policy 경로는 scope→Plugin pre-hook/modify→pruned argument 검사→before_call→실제 dispatch 순서를 가집니다.\n\nafter_call은 실패 분류, exact signature·같은 Tool 실패 누적, 성공한 수정 이후 진전 표시, idempotent result hash를 관리합니다. HTTP rate-limit은 정상 cooldown 재시도일 수 있어 exact-failure 증가를 건너뛰는 예외가 있고, terminal 등의 다양한 실패 명령은 진단 과정일 수 있어 failure-tolerant 예외를 둡니다. observe_call은 A,A,A와 A,B,A,B 같은 cycle을 따로 다루고 큰 동일 결과는 Context 참조 stub으로 줄일 수 있습니다. stub은 이미 실행된 결과의 표현 축소이며 실행 생략 cache가 아닙니다.\n\nController는 결정 객체를 반환하고 Runtime이 안내·합성 오류·halt를 소비합니다. 차단된 호출은 실제 실행 결과처럼 실패 카운터에 다시 넣지 않습니다. 이 판단은 반복/실패 제어이며 업무 결과의 진실을 검증하는 모델이 아닙니다.',
        ['guard','parallel'],code_kind='실제 Controller 메서드 기반 제어 흐름 예시. execute/name/args/after/seen은 설명용 변수이며 원문 전체 실행 코드가 아니다.')

    d=code(0,35,1010,570,'tool_loop_guardrails:\n  warnings_enabled: true\n  hard_stop_enabled: false\n  non_interactive_hard_stop_enabled: true\n  warn_after:\n    exact_failure: 2\n    same_tool_failure: 3\n    idempotent_no_progress: 2\n  hard_stop_after:\n    exact_failure: 5\n    same_tool_failure: 8\n    idempotent_no_progress: 5',caption='DEFAULT_CONFIG · v0.22.5',size=23)
    d+=notes([('대화형 기본','경고를 결과에 붙여 복구 유도|반복 감지 hard stop은 off','context'),('무인 표면','해당 platform에서 hard stop on|Cron 등 사람이 없는 반복 제어','runtime'),('항상 별도 적용','web_search 50 · subagent 50 / turn|loop_caps는 hard_stop과 별개','risk')],x=1100,w=550)
    put('HGUARDCONFIG','기본 경고와 강제 중단의 차이','대화형 세션과 무인 작업의 기본 정책이 다릅니다.','threshold는 실패 분류·진전·표면 조건과 함께 해석합니다.',section,d,
        ['대화형','무인 실행','별도 cap'],
        [('기본값','경고 true, interactive hard stop false, non-interactive hard stop true입니다.'),('한도','loop_caps의 web_search와 subagent 기본 한도는 각각 turn당 50이며 0은 해당 cap 해제입니다.')],
        'ToolCallGuardrailConfig.from_mapping은 nested warn_after/hard_stop_after를 읽고, 알려진 대화형 platform 이외의 비어 있지 않은 platform에서는 non_interactive_hard_stop_enabled에 따라 hard stop을 켭니다. 고정 소스의 attended 집합은 cli/tui/desktop/acp/subagent/api_server입니다. api_server를 무조건 무인으로 묶지 않습니다.\n\nExact failure는 같은 인자 실패가 2회 누적되면 안내, hard stop을 켰을 때 5회 누적 뒤 다음 before_call에서 차단합니다. 같은 Tool 실패는 3회 경고/8회 halt가 기본이지만 failure-tolerant 도구·진전·throttle 등 예외가 있습니다. 따라서 모든 여섯 번째 Tool이 차단된다는 예로 일반화하지 않습니다. loop_caps는 이 soft/hard switch와 독립적으로 적용합니다. 무인 점검에서는 cap·예산·종료 결과를 함께 관측하고, 대화형 진단에서는 의도된 반복을 오탐하는지 확인합니다.',
        ['guard','defaults'])

    d=code(0,45,1040,530,'# 로컬 Plugin의 정책 예시\ndef register(ctx):\n    ctx.register_hook("pre_tool_call", read_only)\n\ndef read_only(**event):\n    if event.get("tool_name") == "terminal":\n        return {\n            "action": "block",\n            "message": "조회 전용 세션"\n        }',caption='공식 Hook API 활용 예시 · terminal만 차단하는 제한된 예',size=23)
    d+=notes([('정책 Hook','block 또는 modify 인자 반환|효과를 바꾸는 확장 지점','runtime'),('실패 방식','pre_tool_call 오류·시간 초과 → 차단|일반 관측 Hook은 실패 시 건너뜀','risk'),('활용 범위','tool_request 수정 → 정책·승인|최종 인자로 downstream 검사','context')],x=1120,w=530)
    put('HHOOK','필요한 실행 정책을 Hook으로 추가하기','공식 pre_tool_call의 반환값과 실패 처리를 확인합니다.','이 예시는 terminal 차단이며 모든 파일·외부 쓰기를 막는 완전한 조회 모드는 아닙니다.',section,d,
        ['정책 반환','실패 처리','변경한 인자'],
        [('정책 반환','pre_tool_call은 block 또는 modify(args)로 실행에 개입할 수 있습니다.'),('실패 처리','고정 코드의 pre_tool_call은 예외/timeout/still-running에서 차단 directive를 생성합니다.')],
        'Plugin register(ctx)에서 register_hook을 쓰는 활용 예시이며 기본 내장 정책 코드 자체를 복사한 것은 아닙니다. Tool executor는 get_pre_tool_call_directive 계열의 결과를 검사해 block/modify를 적용합니다. 다른 write_file·MCP 도구를 허용한 상태에서는 terminal만 막아도 전체 read-only가 되지 않습니다. 필요한 전체 Toolset/Backend 권한도 따로 제한해야 합니다.\n\n중요한 코드 대조 결과: observer 문서의 일반적인 fail-open 설명을 모든 Hook에 적용하면 부정확합니다. plugins_dispatch.py의 _HOOK_TIMEOUT_FAIL_CLOSED_HOOKS={pre_tool_call}이며 timeout/이미 실행 중/예외에 block을 반환합니다. 기본 plugins.hook_callback_timeout은 30초, timeout<=0 등 설정 예외가 있습니다. 일반 pre/post API 관측 callback은 실패를 기록하고 건너뛰는 경로입니다.\n\nMiddleware의 tool_request는 인자를 먼저 바꾸고 그 유효 인자로 정책·guardrail·승인을 평가하게 합니다. middleware 자체의 실패는 fail-open 경로가 있으므로 반드시 차단해야 하는 정책을 단순 인자 수정 callback 하나에만 의존시키지 않습니다. Hook 종류와 Inline/Registry 적용 범위를 확인해야 합니다.',
        ['pluginreg','hookdispatch','parallel','middlewaredoc','defaults'],code_kind='공식 Plugin API를 사용한 제한된 사용자 정책 예시. 전체 보안 정책이나 설치된 Plugin이 아니다.')

    d=''
    rows=[('Session 기록','SQLite · messages · Tool Call/Result 연결','context'),('운영 로그','logs/agent.log INFO+ · errors.log WARNING+','runtime'),('Observer / Span','API·Tool·승인·자식 이벤트를 ID로 연결','tool'),('별도 내보내기','Trajectory / MoA trace / HF upload / OTLP는 설정·목적별 구분','model')]
    for i,(a,b,c) in enumerate(rows):
        y=40+i*140;d+=group(i+1,text(0,y+35,a,34,c,700)+text(460,y+35,b,29,'text')+rule(0,y+95,1650,y+95))
    put('HTRACEBASE','Hermes에 기본으로 남는 기록은 무엇일까?','대화 저장·운영 로그·이벤트 관측·외부 전송을 구분합니다.','Session 기록만으로 모든 API 시도의 지연·재시도를 복원할 수는 없습니다.',section,d,
        ['Session','로그','관측 Hook','내보내기'],
        [('Session / 로그','대화·호출 결과 보존과 실행 중 INFO/WARNING 진단은 다른 데이터입니다.'),('외부 관측','라이프사이클 소비자·Exporter를 연결해야 원하는 Span을 수집할 수 있습니다.')],
        'hermes_logging.setup_logging은 프로필 home/logs에 agent.log와 errors.log 등을 구성합니다. agent.log 기본 INFO, 5MB/backup 3이며 errors.log는 구현에서 WARNING, 2MB/backup 2로 별도 지정합니다. security.redact_secrets 기본 true의 formatter를 사용하지만 모든 PII의 완전 제거를 보장하지는 않습니다. Session SQLite 기록과 이 일반 로그를 상세 API payload capture로 혼동하지 않습니다.\n\nAIAgent의 save_trajectories 기본은 false이며 opt-in이면 ShareGPT 형식의 JSONL 기록을 저장하는 경로가 있습니다. moa.save_traces도 기본 false입니다. monitoring.gateway_health_export.enabled와 monitoring.export.otlp.enabled는 모두 기본 false입니다. 이 OTLP 경로는 내용 없는 서비스 건강·운영 진단용이며 대화/Tool args/results trajectory와 다릅니다.\n\nObserver는 built-in 소비자와 Plugin 소비자를 lifecycle에서 함께 호출합니다. 설정된 Relay 공유 metrics 등의 경로는 별도 계약입니다. 기본적으로 외부 전체 대화 Trace가 자동 생성/전송된다고 설명하지 않습니다. 목적에 맞춰 보존 기간·필드·Exporter를 선택합니다.',
        ['logging','defaults','lifecycle','agentinit','trajectory'])

    d=chain([('모델 요청 경계','pre_api_request|post_api_request / api_request_error','model'),('Tool 경계','pre_tool_call|post_tool_call: status·duration_ms','tool'),('사용자·자식 경계','approval request / response|subagent_start / stop','runtime')],y=55,h=215,connect=False)
    d+=group(4,box(0,425,1650,170,'이벤트를 연결하는 ID','session_id · turn_id · api_request_id · tool_call_id|parent/child_session_id · parent_turn_id로 위임 관계 연결','context',31))
    put('HOBSERVER','Observer Hook으로 실행 경계를 연결하기','이벤트 종류와 상관 ID가 Trace의 뼈대가 됩니다.','발생 순서만 보고 연결하지 않고 명시적인 ID와 시간 정보를 사용합니다.',section,d,
        ['API 경계','Tool 경계','승인·위임','상관 ID'],
        [('API 이벤트','요청 준비 뒤 pre, 성공 응답 post, 실패/복구 경로 api_request_error를 보냅니다.'),('Tool 이벤트','완료뿐 아니라 blocked/cancelled/error에도 terminal post 이벤트를 제공하는 경로입니다.'),('부모·자식','명시적인 session/turn 식별자로 위임 관계를 구성합니다.')],
        'turn_api_request._fire_pre_api_request_hook은 has_hook으로 소비자를 확인한 뒤 effective request를 전송합니다. turn_response_check 및 api_request_hooks의 성공/오류 경로에서 사용량·지연·종료 이유·에러 정보를 제공합니다. tool_executor는 호출의 한 terminal post_tool_call을 소유하며 block/cancelled도 닫히게 처리합니다. transform_tool_result는 post 이후 모델에 들어갈 표현을 바꾸는 별도 Hook입니다.\n\n주의: 코드의 api_request_id는 conversation_loop에서 바깥 논리 반복 번호로 생성하며 안쪽 retry에서 재사용될 수 있습니다. 문서의 per-attempt 설명만 보고 이를 고유 HTTP span ID로 쓰면 덮어쓸 수 있습니다. api_request_id를 opaque correlation key로 두고 timestamp/retry_count/수집 측 attempt index를 더해야 합니다. api_duration은 초, Tool duration_ms는 밀리초이므로 단위를 맞춥니다.\n\non_session_end는 run/turn 종료 이벤트이고 session identity의 최종 종료와 같지 않습니다. 장기 session 정리는 on_session_finalize/reset을 봅니다. approval 관측 Hook의 반환으로 승인을 대신 응답할 수는 없고 차단 정책은 pre_tool_call에서 수행합니다.',
        ['apirequest','apihooks','apiresponse','loop','parallel','observerdoc','lifecycle'])

    d=code(0,40,1080,550,'import logging\nlog = logging.getLogger("seminar.trace")\n\ndef register(ctx):\n    ctx.register_hook("post_api_request", observe)\n    ctx.register_hook("api_request_error", observe)\n\ndef observe(**e):\n    log.info("turn=%s request=%s duration=%s",\n        e.get("turn_id"), e.get("api_request_id"),\n        e.get("api_duration"))',caption='공식 등록 API를 이용한 최소 관측 Plugin 예시',size=22)
    d+=notes([('수집 시작','Plugin 발견·활성화 후 register|기본 내장 Exporter 코드가 아님','runtime'),('payload 가공','JSON 변환 · key redaction · 크기 제한|소비자가 있을 때 구성','context'),('수집 품질','빠른 callback·비동기/배치 Export|누락·닫히지 않은 Span 점검','tool')],x=1140,w=510)
    put('HTRACECODE','짧은 Plugin으로 API 관측을 시작하기','먼저 식별자와 지연을 수집하고 필요한 필드만 확장합니다.','관측 callback의 성공 여부가 작업 성공 여부와 같지는 않습니다.',section,d,
        ['등록·활성화','payload','수집 품질'],
        [('등록','register_hook으로 원하는 이벤트를 구독하고 Plugin을 활성화해야 합니다.'),('Sanitizer','JSON 호환 변환·민감 key 마스킹·문자열/시퀀스/전체 크기 제한을 적용합니다.')],
        '코드는 실제 공식 API를 사용하는 사용자 Plugin 예시이며 실행·설치하지 않았습니다. 기존 Hermes logging 설정이 적용된 환경에서 turn/request/duration만 INFO로 남기는 최소 형태입니다. Tool/approval/subagent는 해당 Hook과 callback을 추가하고 parent/child 관계 및 상태를 별도로 저장해야 합니다. 네트워크 Exporter는 queue/batch/retry를 구성하고 callback에서 긴 blocking IO를 피하는 편이 적절합니다.\n\napi_request_hooks._hook_jsonable 기본은 depth 8, string 8000자, sequence 200개이고 api_key/authorization/cookie 등의 key를 가립니다. 전체 payload 기본 cap은 HERMES_PLUGIN_PAYLOAD_MAX_CHARS=50000이며 줄인 cap 후에도 크면 preview로 축소합니다. 따라서 payload가 원문과 동일하다고 가정하지 않습니다. 이 key 기반 sanitizer는 프롬프트 문자열 속 모든 credential·개인정보를 의미적으로 탐지하는 보증도 아닙니다. legacy compatibility fields보다 sanitized request/response/error를 사용하고 Export 전 별도 마스킹·최소화를 검토합니다.',
        ['pluginreg','hookdispatch','apihooks','apirequest','logging'],code_kind='공식 Plugin 등록 API 기반 실행 가능한 형태의 최소 사용자 예시. Hermes 내장 Plugin 원문/실행 결과가 아니다.')

    d=code(0,45,1050,535,'# 가상 이벤트 · 성능 측정 결과 아님\nturn=T1 request=R1 error=429 retry_count=0\nturn=T1 request=R1 ok usage={...}\nturn=T1 tool=C1 status=blocked duration_ms=...\nparent_session=S1 child_session=S2\n\n# 같은 R1이라고 같은 HTTP 시도는 아님\n# 시간 + retry_count + 수집 측 attempt로 구분',caption='수집 데이터에서 확인할 관계의 예시',size=22)
    d+=notes([('실패 원인','모델/API 오류 vs 정책 차단|Tool 실패·취소·전달 실패 분리','risk'),('비용·지연','실제 usage·API duration 집계|승인 대기·Tool·자식 시간 구분','model'),('Demo 활용','질문 → 요청 → 승인/Tool → 저장|같은 ID로 Sources 설명과 연결','context')],x=1120,w=530)
    put('HTRACEUSE','Trace로 무엇을 확인하고 개선할까?','재시도·차단·사용량·위임을 한 작업의 기록으로 읽습니다.','실행 완료·정책 통과·업무 정답 여부를 별도의 기준으로 평가합니다.',section,d,
        ['원인 구분','비용·지연','Demo 연결'],
        [('진단','에러 타입·status·reason과 ID를 연결해 모델 장애/정책 차단/도구 실패를 분리합니다.'),('평가','Trace는 실행 근거이며 계산 정확성·근거 문서 버전·권한 적합성은 업무 평가 기준이 필요합니다.')],
        '표시는 가상 이벤트이며 요청·실행 또는 성능 실측을 한 것이 아닙니다. 같은 api_request_id에 실패/성공 이벤트가 이어질 수 있으므로 한 ID에 마지막 값을 덮어쓰는 저장 구조를 피합니다. 이벤트 시각과 retry_count/수집 순번을 보존하고 Tool Call ID 및 parent/child 관계를 연결합니다.\n\n사용량은 실제 응답 usage를 정규화해 집계하되 실패 시 usage 누락, 공급자 캐시/과금 방식, auxiliary model과 자식 비용을 구분해야 합니다. API duration과 전체 turn latency는 승인 대기·Tool·재시도·자식 시간 때문에 다릅니다. blocked status는 미실행일 수 있고 ok status도 업무 정답을 보증하지 않습니다. 앞서 설명한 Guardrail 경고/차단과 Memory/Skill 쓰기의 반환·파일 확인을 Demo 관찰 지점으로 연결합니다.',
        ['apihooks','loop','observerdoc','parallel'])

    d=chain([('명시적 내보내기','/upload-trace|Session 메시지 조회','context'),('JSONL 변환','system 제외 · tool_use/tool_result|uuid / parentUuid로 순서 연결','runtime'),('Hugging Face 업로드','기본 private=true · redact=true|토큰·패키지·명시 호출 필요','tool')],y=60,h=225)
    d+=group(4,box(0,445,1650,155,'Transcript Viewer와 실제 시간 Trace의 차이','현재 변환 코드는 내보내기 시각을 timestamp로 사용 · 실제 API span latency 복원용이 아님','risk',30))
    put('HTRACESHARE','실행 대화를 Trace Viewer로 공유하는 경로','저장된 대화를 재구성하는 기능과 실시간 계측을 구분합니다.','내보내기 전 원문·비밀값·공유 범위를 검토합니다.',section,d,
        ['명시 호출','변환','업로드','시간의 의미'],
        [('변환','build_trace_jsonl은 system을 제외하고 Tool Call/Result를 Viewer용 메시지로 바꿉니다.'),('기본 옵션','upload_session_trace의 redact/private 기본값은 모두 true이며 자동 업로드가 아닙니다.')],
        'agent/trace_upload.py는 SessionDB에서 messages/meta를 읽고 build_trace_jsonl로 Claude Code JSONL shape을 만듭니다. assistant tool_calls는 tool_use, Tool 결과는 user 형태의 tool_result로 바꾸며 uuid/parentUuid로 순서를 연결합니다. 포맷 이름은 Hermes가 Claude Code 내부 Runtime을 사용한다는 의미가 아닙니다.\n\n코드는 base_ts=_now_iso()를 export 시 한 번 정하고 각 행에 넣습니다. 따라서 이 Viewer의 timestamp 차이로 원래 API 지연을 계산하면 안 됩니다. 실제 latency는 앞의 Observer 이벤트에서 수집해야 합니다. 토큰과 huggingface_hub 의존성을 확인한 뒤 private dataset의 sessions/<id>.jsonl에 명시 업로드합니다. redact=true는 force=True로 redactor를 적용하고 마스킹 실패/변환 JSON 오류 시 업로드를 거부합니다.\n\n실제 외부 업로드는 하지 않았습니다. 일반 로그 redaction과 이 export redaction, Observer key sanitizer는 적용 범위가 다릅니다. 업무상 민감 데이터·경로·사용자 메시지는 공유 전에 직접 검토할 대상입니다.',
        ['traceshare','apihooks'],code_kind='실제 내보내기 경로의 도식. 외부 업로드나 인증 요청을 실행하지 않음.')
