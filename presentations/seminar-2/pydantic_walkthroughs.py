"""Source-checked explanations for the PydanticAI portion of the seminar."""


def apply_pydantic(slides, env, walkthrough, update):
    text, box, group, arrow = (env[n] for n in ('text', 'box', 'group', 'arrow'))

    def cards(key, title, subtitle, rows, take):
        diagram = ''
        for i, (heading, body) in enumerate(rows):
            x, y = (i % 2) * 835, 65 + (i // 2) * 235
            diagram += group(i+1, box(x, y, 800, 190, heading, body, ('context','runtime','tool','model')[i], 31))
        old = slides[key]['explanation']
        update(key, title, subtitle, diagram, take, [a for a,_ in rows],
               '\n\n'.join(a+' — '+b.replace('|',' ') for a,b in rows)+'\n\n'+old)

    def walk(n, title, sub, caption, rows, take):
        key = f'PA{n:02}'
        walkthrough(key, title, sub, caption, rows, take, slides[key]['explanation'])

    cards('PA01','Pydantic과 PydanticAI, 어디까지 맡을까?', '같은 불량률 보고서를 만드는 코드에서 역할을 나눠 봅니다.', [
        ('Pydantic · 데이터 검증','Report에서 bin_id와 defect_rate 타입 확인|문자열·숫자 등 입력을 선언된 계약으로 검증'),
        ('PydanticAI Core · 실행','모델 호출 → 도구 인자 검증 → Python 실행|결과를 다음 메시지로 넣거나 최종 타입으로 반환'),
        ('Harness · 선택 기능','Memory, Skills, Subagents를 연결|저장소나 호출 범위는 앱 설정으로 선택'),
        ('업무 앱 · 실제 기준','조회 가능한 BIN인지, 42/1000이 맞는지|데이터를 다시 조회하고 승인·저장을 관리'),
        ], '형식이 맞는 보고서와 수치가 맞는 보고서를 각각 확인해야 합니다.')
    rows = [('Agent 설정','모델 · 지시 · Deps · 도구 · 출력 타입'),
            ('Graph 실행','입력 → 모델 요청 → 응답 처리'),
            ('실행 경계','Model Adapter · ToolManager · 출력 검증'),
            ('상태와 운영','Conversation · 사용량 · Capability/Hooks')]
    diagram = ''.join(group(i+1,box((i%2)*855,60+(i//2)*265,790,175,a,b,('context','runtime','tool','model')[i],31))
                      for i,(a,b) in enumerate(rows))
    diagram += arrow('M790 145 H845','context') + arrow('M1250 235 V275 H400 V314','runtime') + arrow('M790 410 H845','tool')
    update('PA02','PydanticAI Core의 네 부분','Agent 선언을 시작으로 실행, 모델·도구, 대화와 확장을 순서대로 봅니다.',
           diagram,'Harness는 Core의 Capability 경계에 필요한 기능을 연결합니다.',
           [a for a,_ in rows], '\n\n'.join(a+' — '+b for a,b in rows))

    walk(4,'조회 도구와 보고서 타입을 붙이기','앱에서 선언한 세 가지가 실행 중 어디에 쓰이는지 봅니다.',
        'Python 앱 코드 발췌 · Repo와 모델 연결 정의 생략', [
        ('① 결과 타입','class YieldReport(BaseModel):\n    lot_id: str\n    yield_pct: float','최종 결과의 형태를 정함.|수치가 실제 조회값과 같은지는 별도 검사.'),
        ('② Agent 설정','agent = Agent(model, deps_type=Repo,\n              output_type=YieldReport)','Repo는 앱에서 넣을 의존성 타입.|YieldReport는 모델 출력 계약.'),
        ('③ 조회 함수 등록','@agent.tool\ndef read_counts(ctx: RunContext[Repo], lot_id: str):\n    return ctx.deps.read_counts(lot_id)','모델에는 lot_id 인자만 공개.|함수는 서버에서 ctx.deps로 조회.'),
        ('④ 실행','result = agent.run_sync("LOT-A 조회", deps=repo)\nreport = result.output','조회와 출력 검증을 마치면|앱이 YieldReport 객체를 받음.'),
        ], '개발자는 데이터 접근과 출력 계약을 쓰고, Core는 호출 순서를 실행합니다.')
    walk(6,'run()이 Graph를 여는 과정','한 번의 Run마다 상태와 리소스가 따로 준비됩니다.',
        'agent/abstract.py · agent/__init__.py · 내부 호출 경로 축약',[
        ('① 앱의 진입점','await agent.run(prompt, deps=repo)','run은 노드들을 끝까지 진행해|AgentRunResult를 반환.'),
        ('② 실행 준비','Agent.iter(...)\n# _prepare_run(...)','모델, 상태, 도구와 Capability 등|이 실행에서 사용할 구성을 준비.'),
        ('③ 리소스 열기','_PreparedAgentRun.open(...)\n# self.graph.iter(...)','실행 범위 안에서 리소스를 열고|첫 UserPromptNode를 Graph에 전달.'),
        ('④ 순회와 정리','async for node in agent_run:\n    ...','노드가 다음 작업을 돌려줌.|실행 컨텍스트를 빠져나오며 리소스 정리.'),
        ], '중간 노드를 직접 보고 싶다면 async with agent.iter(...)를 씁니다.')
    walk(7,'pydantic-graph가 Agent 루프를 돌리는 방법','GraphBuilder가 구조를 만들고, 각 노드가 다음 실행을 선택합니다.',
        '_agent_graph.py · GraphBuilder 등록과 노드 역할 축약',[
        ('① GraphBuilder','g = GraphBuilder(state_type=GraphAgentState,\n                 deps_type=GraphAgentDeps, ...)\ng.add(g.edge_from(g.start_node).to(UserPromptNode), ...)','Graph 타입과 시작점을 정의.|GraphRun이 노드의 실행 결과를 받아 진행.'),
        ('② UserPromptNode','UserPromptNode.run(ctx)','이력을 불러오고 새 사용자 요청을 구성.|승인 재개라면 보류 결과도 처리.'),
        ('③ ModelRequestNode','ModelRequestNode._prepare_request(...)\nModelRequestNode._make_request(...)','요청용 메시지·옵션을 준비하고 모델 호출.|응답을 이력에 넣어 CallToolsNode로 전달.'),
        ('④ CallToolsNode','CallToolsNode._handle_tool_calls(...)\n# ModelRequestNode / SetFinalResult 경로','도구 반환이나 수정 요청은 다음 모델 입력.|최종 결과는 SetFinalResult에서 End로 넘김.'),
        ], 'Graph는 실행 순서를 관리하고, Agent 노드는 모델 응답의 의미를 판단합니다.')
    walk(9,'Graph 상태와 앱 데이터가 만나는 곳','LOT-A를 조회하는 도구에는 무엇이 전달될까요?',
        '_agent_graph.py · 런타임 객체의 역할 발췌',[
        ('실행 중 누적 상태','GraphAgentState\n# message_history, usage, run_step','모델과 주고받은 이력, 사용량,|진행 단계를 현재 실행에서 누적.'),
        ('실행 구성','GraphAgentDeps\n# model, end_strategy, usage_limits','어떤 모델과 한도, 종료 정책을|현재 Graph 실행에서 사용할지 보관.'),
        ('도구가 읽는 값','ctx.deps.allowed_lots  # 앱 예시\nctx.deps.snapshot_id','도구는 앱이 넣은 권한과 데이터 기준을 읽음.|모델에는 도구가 반환한 값이 전달될 수 있음.'),
        ], '모델의 lot_id 제안과 앱의 조회 권한을 분리합니다.')
    walk(10,'모델 응답을 어느 경로로 보낼까?', '응답의 내용과 앱의 출력 계약을 함께 확인합니다.',
        'CallToolsNode · 실제 처리 메서드와 결과 예시',[
        ('업무 도구 요청','_handle_tool_calls(...)\n# read_counts({"lot_id": "LOT-A"})','도구 반환을 메시지에 추가.|다음 ModelRequestNode에서 모델이 읽음.'),
        ('최종 출력 후보','_process_response_output(...)\n# text / file output path','텍스트·파일은 출력 계약에 맞춰 검사.|출력용 Tool은 Tool 호출 처리 경로에서 검사.'),
        ('수정 또는 보류','RetryPromptPart(...)\nDeferredToolRequests(...)','수정 요청은 다음 모델 호출에 전달.|승인 대기는 앱에 넘겨 후속 실행에서 해결.'),
        ], '도구와 출력 후보가 함께 오면 EndStrategy가 실행 범위를 결정합니다.')
    walk(11,'다음 모델 요청이 막히는 지점','사용량 제한, 출력 재시도, 실행 취소의 효과가 다릅니다.',
        'usage.py · _agent_graph.py · 실제 검사 이름',[
        ('모델 요청 횟수','UsageLimits(request_limit=50)\ncheck_before_request(usage)','기본 요청 한도 50회. 한도에 도달하면|다음 모델 요청 전에 UsageLimitExceeded.'),
        ('출력 재시도','consume_output_retry(...)','출력 검증 실패는 해당 재시도 예산을 사용.|모델 요청 횟수 한도와 별개.'),
        ('실행 취소','run_cancelled_snapshot(...)','취소 시점에 기록 가능한 실행 상태를 정리.|이미 외부에 저장한 결과의 복구는 앱 책임.'),
        ], '실행이 중단돼도 이미 끝난 작업은 남을 수 있습니다.')
    walk(12,'실행 API 다섯 가지','앱이 어느 시점에 무엇을 받아야 하는지에 따라 고릅니다.',
        'PydanticAI 공개 API · Python 사용 형태',[
        ('run_sync','result = agent.run_sync(prompt)','동기 함수에서 최종 결과를 기다림.'),
        ('run','result = await agent.run(prompt)','비동기 서버에서 최종 결과와 이력을 받음.'),
        ('run_stream','async with agent.run_stream(prompt) as stream:\n    async for part in stream.stream_output(): ...','출력을 점진적으로 표시.|최종 출력 확정 시점에 유의.'),
        ('run_stream_events','async for event in agent.run_stream_events(prompt): ...','모델 응답과 도구 실행 이벤트를|같은 스트림에서 소비.'),
        ('iter','async with agent.iter(prompt) as run:\n    async for node in run: ...','현재 Graph 노드를 보며 실행.|run.result에서 최종 결과 확인.'),
        ], '출력 UI는 stream, 실행 경계 관찰은 events 또는 iter가 적합합니다.')
    cards('PA13','LOT-A 요청에서 모델이 실제로 받는 값','같은 실행을 API 요청과 Python 서버로 나눠 봅니다.',[
        ('① 메시지','예: “LOT-A 수율을 알려줘”|이전 조회 결과가 있다면 이력으로 함께 전송'),
        ('② 도구·출력 계약','read_counts의 lot_id는 문자열|YieldReport 필드는 출력 모드에 맞게 전송'),
        ('③ Python 실행 환경','ctx.deps에 허용 LOT와 DB 연결|도구가 실행될 때 이 객체로 접근 권한 검사'),
        ('④ 다음 모델 요청','도구가 반환한 good=920, total=1000|ToolReturnPart가 이력에 합쳐져 모델에 전달'),
        ], '모델이 읽는 값은 Python 객체가 아니라 그 실행에서 조립된 요청입니다.')
    walk(14,'새 Run에서 어떤 지시가 남을까?','첫 Run 뒤 모델 설정을 교체하는 예시로 비교합니다.',
        'Python 호출 예시 · result.all_messages()를 다음 Run에 전달',[
        ('첫 실행의 두 지시','a = Agent(model, instructions="단위를 표시",\n          system_prompt="반도체 검사 담당자")','Instructions는 현재 실행의 지시로 계산.|System prompt는 메시지 Part로 기록 가능.'),
        ('다른 Agent로 계속 실행','b = Agent(model, instructions="표로 작성")\nawait b.run("다시 보여줘",\n            message_history=result.all_messages())','새 instructions는 “표로 작성”.|기존 SystemPromptPart는 넘긴 이력에 남음.'),
        ('동적 System Prompt','_reevaluate_dynamic_prompts(...)','현재 Agent가 해당 동적 프롬프트를|인식하는 경로에서 다시 평가.'),
        ], '지시를 교체할 때는 현재 Agent 설정과 전달한 메시지 이력을 함께 확인합니다.')
    walk(17,'대화 불러오기 → 실행 → 새 버전 저장','합성 LOT-A 대화를 새 프로세스에서도 이어 가는 코드입니다.',
        '앱 저장소 예시 · ConversationTypeAdapter는 공개 API',[
        ('① 불러오기','old = store.read(user_id, session_id)\nconversation = ConversationTypeAdapter.validate_json(old.data)','사용자와 세션을 확인한 뒤 저장된 JSON을|메시지·실행 상태가 있는 Conversation으로 복원.'),
        ('② 이어서 실행','result = await agent.run("그 LOT 다시 조회",\n                         conversation=conversation)','이전 요청·응답을 참고해 새 메시지 추가.|빈 세션은 conversation=None으로 시작.'),
        ('③ 갱신','data = ConversationTypeAdapter.dump_json(result.conversation)\nstore.save_if_version(session_id, old.version, data)','갱신한 상태를 다시 저장.|버전 확인과 충돌 처리는 앱 예시.'),
        ], '대화 상태는 Core에서 직렬화하고, 저장 범위와 동시 갱신은 앱이 결정합니다.')
    walk(21,'Tool 인자가 틀리면 어디에서 멈출까?', '같은 read_counts 호출에 대해 실패와 성공을 비교합니다.',
        'tool_manager.py · 호출 경계와 모델 인자 예시',[
        ('① 도구 찾기','validate_tool_call(...)\n# _resolve_tool(...) / _build_tool_context(...)','도구 이름을 현재 실행에서 공개한 목록과 대조.|도구가 없으면 함수에 진입하지 않음.'),
        ('② 인자 검증','_validate_tool_args(...)\nvalidator.validate_json(...)  # 또는 validate_python','{}는 필수 lot_id 누락.|검증 오류는 RetryPromptPart로 돌려보냄.'),
        ('③ 정책 Hook과 실행','_run_validate_hooks(...)\nexecute_tool_call(...)','{"lot_id": "LOT-A"}가 검증을 통과한 뒤|서버에서 업무 권한을 확인하고 조회.'),
        ], '스키마 검증은 인자 형식을 확인하고, 업무 인가는 도구 또는 정책 경계에서 수행합니다.')
    walk(23,'병렬 조회 사이에 단독 작업을 넣기','같은 모델 응답의 A/B 조회, C 저장, D/E 조회를 예로 봅니다.',
        '_tool_execution.py · 실행기 로직 축약',[
        ('① 도구에 단독 실행 표시','@agent.tool(sequential=True)\ndef save_report(ctx: RunContext[Repo], ...): ...','C 앞의 조회가 끝나야 C를 시작.|C가 끝나기 전에는 D/E를 시작하지 않음.'),
        ('② 실행 묶음 계산','_segment_by_barriers(indices, is_barrier=...)\n# [A, B] → [C] → [D, E]','실행기는 모델이 낸 호출 순서에서|단독 도구를 기준으로 묶음을 분할.'),
        ('③ 독립 호출을 동시에 시작','for segment in segments:\n    tasks = [asyncio.create_task(call_tool(i))\n             for i in segment]\n    # 완료/버퍼 이벤트 소비 후 다음 묶음','독립 I/O는 대기 시간을 겹칠 수 있음.|공유 상태 쓰기나 호출량 폭주는 앱에서 제어.'),
        ], 'sequential은 실행 순서를 정합니다. 앞 도구 결과를 뒷 도구 인자로 자동 전달하지 않습니다.')
    walk(28,'같은 모델 응답에서 무엇을 실행할까?', '모델 응답에 조회 A → 유효한 출력 O1 → 기록 B → 출력 O2가 왔다고 가정합니다.',
        '_tool_execution.py · process_tool_calls · 정책별 처리 요약',[
        ('early','Agent(..., end_strategy="early")\n# O1 채택 / A, B, O2 생략','출력 도구를 먼저 검사.|유효한 출력이 있으면 업무 함수는 생략.'),
        ('graceful · 기본','Agent(..., end_strategy="graceful")\n# A 실행 → O1 채택 → B 실행 / O2 생략','모델이 낸 순서에 따라 함수 묶음을 처리.|O1을 얻어도 뒤의 업무 함수는 실행 가능.'),
        ('exhaustive','Agent(..., end_strategy="exhaustive")\n# A, O1, B, O2 모두 처리 / O1 채택','단독 실행 경계를 제외하면 함께 시작.|유효한 출력 선택은 응답에 나온 순서 기준.'),
        ], '기록·발행을 막아야 할 때는 종료 정책과 별도로 도구 자체에 승인 경계를 둡니다.')
    walk(34,'가드레일을 어느 경계에 걸까?', '요청과 도구 인자, 최종 수치는 서로 다른 시점에 확인할 수 있습니다.',
        'Guardrail Capability · A17 보고서 예시',[
        ('입력 검사','InputGuardrail.wrap_model_request(...)','예: 생산 데이터 반출 요청 차단.|병렬 모드는 모델 요청이 이미 시작될 수 있음.'),
        ('도구 검사','ToolGuardrail.before_tool_execute(...)','예: publish 호출을 승인 대기로 전환.|allow / block / retry / approve / replace.'),
        ('출력 검사','OutputGuardrail.after_output_process(...)','예: 최종 불량률이 원본과 맞는지 확인.|partial 출력은 이 검사에서 건너뜀.'),
        ], '부작용을 막는 검사는 실행 앞에 두고, 수치 검증은 최종 출력 경계에서 합니다.')
    walk(39,'Harness Memory에 메모 한 줄 쓰기','모델이 파일 이름을 제안하고, 저장 범위는 앱이 결정합니다.',
        'Harness memory/_capability.py · memory/_toolset.py',[
        ('앱에서 연결','Memory(store=store, namespace="fab-seminar")','실행에서 사용할 저장소와 scope를 결정.|기본 InMemoryStore는 프로세스 수명.'),
        ('모델의 쓰기 요청','write_memory(...)\n# 예: 다음 검사에서 진공 경보 확인','Toolset이 인자를 검사하고 scope 내에서|메모 저장 또는 수정 처리.'),
        ('다시 조회','read_memory(...) / search_memory(...)','정확한 파일을 읽거나 검색어로 노트를 찾음.|원본 대화 전체와는 별도의 저장 대상.'),
        ], '스토어를 바꾸면 메모의 수명과 공유 범위가 달라집니다.')
    walk(40,'저장한 Memory가 다음 모델 입력에 들어가는 곳','메모 파일이 모델이 읽을 수 있는 메시지로 바뀌는 경계입니다.',
        'memory/_capability.py · 실제 메서드',[
        ('실행 범위 정하기','Memory.for_run(ctx)\nMemory.resolve_scope(ctx)','현재 실행에서 쓸 저장소와 scope를|결정해 다른 실행의 메모와 구분.'),
        ('요청 전에 읽기','Memory.before_model_request(...)\nMemory._load_snapshot(...)','메모를 읽고 줄 수와 토큰 예산 안에서|현재 요청에 붙일 문맥을 준비.'),
        ('메시지로 넣기','Memory._remove_previous_injection(...)','중복 주입을 정리하고 사용자 입력 근처에|기억 문맥을 추가하는 경로.'),
        ], '저장된 메모 전체를 보내는 대신, 주입 범위와 예산을 설정합니다.')
    walk(42,'대화 압축 전후를 메시지로 보기','오래된 검토 이력 뒤에 A17 조회가 이어진 예시입니다.',
        'SlidingWindowCompaction · 메시지 예시는 설명용',[
        ('압축 전','[오래된 검토 1, 오래된 검토 2, A17 질문,\n read_fab_bin(A17), ToolReturn(42/1000)]','전체를 보내면 오래된 요청과 결과도|모델 입력에 들어가 토큰을 사용.'),
        ('임계조건에서 처리','SlidingWindowCompaction.before_model_request(...)\nSlidingWindowCompaction.compact(...)','크기와 보존 조건을 검사한 뒤|남길 최근 턴을 선택.'),
        ('압축 후 예','[A17 질문, read_fab_bin(A17), ToolReturn(42/1000)]','현재 질문을 뒷받침하는 최근 도구 호출과|반환을 함께 유지하는 예.'),
        ], '정확한 오래된 수치가 필요하면 저장소에서 다시 조회합니다.')
    walk(43,'Harness Skill이 실행에 들어오는 과정','목록에서 이름을 고르는 단계와 본문이 로딩되는 단계를 구분합니다.',
        'skills/_capability.py · _loader.py · Skill 연결 예',[
        ('목록 준비','Skills.for_run(...)\n# SKILL.md → 이름·설명','실행에 연결된 Skill을 발견하고|메타데이터로 사용할 절차를 안내.'),
        ('필요한 것 선택','load_capability(...)\n# 예: fab-bin-review','모델이 절차를 선택하면 해당 Capability의|본문이나 연결 기능을 활성화.'),
        ('참고파일 접근','SKILL.md → references/...','세부 절차가 필요할 때 파일 접근.|경로와 실행 권한은 연결한 환경에 따름.'),
        ], '발견된 목록, 실제로 로딩된 본문, 도구 실행 권한을 구분합니다.')
    walk(47,'위임 요청을 자식 Run으로 실행하기','예를 들어 통계 검토자에게 A17의 42/1000을 넘깁니다.',
        'subagents/_toolset.py · 실행 경계와 업무 예시',[
        ('부모에서 업무 구성','delegate_task(...)\n# “A17 42/1000의 불확실성 검토”','자식에게 필요한 데이터와 목표를 명시.|부모의 전체 이력을 공유한다고 가정하지 않음.'),
        ('자식 실행','SubAgentToolset._run_delegation(...)','선택된 자식의 Agent 실행.|Deps 전달과 사용량 추적은 설정을 확인.'),
        ('부모에 결과 반환','ToolReturnPart(...)\n# “42/1000 = 4.2%”','부모가 도구 결과를 읽고 답변을 종합.|위임과 별도 앱 Handoff의 차이.'),
        ], '부모는 결과를 받은 뒤 다음 결정을 내립니다.')
    walk(18,'함수 한 개에서 스키마와 검증기가 만들어지는 과정','read_counts의 Python 선언을 모델이 읽을 수 있게 바꿉니다.',
        '_function_schema.py · 모델 요청 필드 예시', [
        ('함수 선언','def read_counts(ctx: RunContext[Repo], lot_id: str):\n    """지정한 LOT의 검사 수량을 읽는다."""','함수 이름과 설명을 읽음.|lot_id는 모델이 넘길 입력.'),
        ('Core 내부 준비','function_schema(...)','함수 서명과 타입을 바탕으로|JSON Schema와 입력 검증기를 준비.'),
        ('모델에 공개하는 값','{"properties": {"lot_id": {"type": "string"}},\n "required": ["lot_id"]}','모델은 이름·설명·인자 계약을 받음.|함수 본문과 Repo는 Python에 남음.'),
        ], '같은 선언으로 모델에 공개할 계약과 호출할 때 사용할 검증기를 만듭니다.')
    walk(20,'다음 모델 요청에서 도구 목록을 바꾸기','사용자 권한에 따라 발행 도구의 노출을 제어하는 예입니다.',
        'tool_manager.py · toolsets/function.py · 실제 메서드', [
        ('요청 단계마다 목록 준비','ToolManager.for_run_step(ctx)\nFunctionToolset.get_tools(ctx)','현재 RunContext에 맞게|모델에 공개할 도구 정의를 준비.'),
        ('prepare 콜백으로 숨기기','async def prepare_publish(ctx, definition):\n    return definition if ctx.deps.can_publish else None','권한이 없으면 None을 반환해|그 요청의 공개 목록에서 제외.'),
        ('실행할 때 다시 확인','FunctionToolset.call_tool(...)','공개 목록에 있었다고 해서 실제 작업이|지금도 허용된다는 뜻은 아님.'),
        ], '노출 시점에는 선택지를 줄이고, 실행 시점에는 변경된 권한을 확인합니다.')
    walk(37,'승인한 호출 ID로 실행 이어가기','보고서 발행 요청을 저장하고, 앱의 승인 화면에서 결정하는 경우입니다.',
        'Core 공개 API · 승인 결과를 전달하는 Python 예시', [
        ('보류된 호출 저장','pending = result.output  # DeferredToolRequests\ncall = pending.approvals[0]','호출 ID와 원래 인자를 보관.|실행한 결과 대신 승인 요청이 앱에 도착.'),
        ('사람이 결정','decision = DeferredToolResults(\n    approvals={call.tool_call_id: True})','원래 호출 ID에 승인 또는 거절을 연결.|승인 권한과 유효기간은 앱에서 검사.'),
        ('새 Run으로 재개','await agent.run(conversation=result.conversation,\n                deferred_tool_results=decision)','Core는 보류했던 호출과 결정을 연결.|승인 결과를 처리한 뒤 실행을 이어감.'),
        ], '버전이 바뀐 초안에는 이전 승인을 재사용하지 않도록 앱에서 관리합니다.')
    cards('PA45','서버가 멈췄을 때 무엇부터 복구할까?', '같은 발행 작업에서 복구 단위를 비교합니다.', [
        ('Conversation','사용자 요청·도구 호출·결과와 보류 상태|앱이 이 상태를 다음 Run에 전달'),
        ('StepPersistence','완료한 단계와 효과를 checkpoint에 기록|복구 시 어디까지 했는지 결정하는 데 사용'),
        ('Durable 실행','실행기가 정한 경계에서 replay 또는 재개|공급자 호출과 도구 효과를 구분해 설정'),
        ('앱의 중복 방지','보고서 ID·버전으로 멱등 키 지정|발행 성공 후 응답을 잃어도 중복 발행 차단'),
        ], '대화가 저장됐다는 사실만으로 외부 작업의 중복 실행을 막을 수는 없습니다.')
