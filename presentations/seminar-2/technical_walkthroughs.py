"""Focused source walkthroughs for the seminar's Hermes and PydanticAI chapters."""
from code_artwork import code_line


def apply(slides, env):
    text, box, group, rule = (env[name] for name in ('text', 'box', 'group', 'rule'))

    def update(key, title, sub, diagram, take, steps, explanation):
        slide = slides[key]
        slide.update(title=title, sub=sub, diagram=diagram, take=take,
                     steps=['전체 보기', *steps], explanation=explanation,
                     note='## ' + title + '\n\n' + explanation)
        slide['concepts'] = [{'term': label, 'meaning': detail} for label, detail in
                             zip(steps, explanation.split('\n\n'))] or slide['concepts']

    def walkthrough(key, title, sub, caption, rows, take, detail='', recap=()):
        height = 590
        diagram = '<rect x="0" y="20" width="1015" height="590" rx="12" fill="#111c2d" stroke="#64768e"/>'
        diagram += text(22, 58, caption, 21, 'muted') + rule(0, 76, 1015, 76)
        line_count = sum(len(code.splitlines()) for _, code, _ in rows)
        pitch = min(42, 505 / line_count)
        y = 86
        note_height = min(142, (height - 18) / len(rows))
        for i, (label, code, description) in enumerate(rows, 1):
            lines = code.splitlines()
            code_group = f'<rect class="node" x="12" y="{y}" width="988" height="{pitch*len(lines)-3}" rx="5" fill="#26364d" stroke="#42556c"/>'
            for j, line in enumerate(lines):
                code_group += code_line(line, 26, y + pitch * (j + .72), min(23, pitch * .69))
            tone = ('context', 'runtime', 'tool', 'model', 'success', 'risk')[(i-1)%6]
            top = 20 + (i-1)*note_height
            note = box(1050, top, 600, note_height - 9, '', '', tone)
            note += text(1074, top+32, label, 25, tone, 700)
            note += ''.join(text(1074, top+60+j*25, line, 21, 'muted')
                            for j, line in enumerate(description.split('|')))
            focus = f'{i} {len(rows)+1}' if i in recap else str(i)
            diagram += group(focus, code_group + note)
            y += pitch * len(lines)
        steps = [label for label, _, _ in rows]
        if recap:
            steps.append('핵심 다시 보기')
        explanation = '\n\n'.join(f'**{label}** — {desc.replace("|", " ")}' for label, _, desc in rows)
        update(key, title, sub, diagram, take, steps, explanation + ('\n\n' + detail if detail else ''))

    walkthrough('HLOOP', 'Hermes는 언제 다시 모델을 부를까?', '바깥 루프 한 번을 위에서 아래로 읽습니다.',
        'conversation_loop.py · v0.22.5 · 실제 조건 및 호출 축약', [
        ('① 들어갈 조건 확인', 'while prelude_ok and (\n    (calls < max_iterations and remaining > 0)\n    or grace_call\n):', '준비 단계가 중단되지 않았고|횟수와 예산이 남거나 정리 호출이 허용됨'),
        ('② begin_iteration', '    _run_phase(begin_iteration, agent, s)', '중단 플래그를 확인한 뒤 호출 번호를|올리고 예산 한 회를 사용'),
        ('③ prepare_iteration', '    _run_phase(prepare_iteration, agent, s)', '이번 반복의 메시지와 상태를 준비'),
        ('④ assemble_api_request', '    _run_phase(assemble_api_request, agent, s)', '메시지와 도구를 공급자 요청 형식으로 조립'),
        ('⑤ run_preflight_gate', '    _run_phase(run_preflight_gate, agent, s)', '보내기 직전 검사. 결과에 따라|전송 전 종료하거나 다음 반복으로 이동'),
        ('⑥ announce_api_call', '    _run_phase(announce_api_call, agent, s)', '모델을 호출하기 전에 진행 상황을 알림'),
        ], '먼저 호출할 수 있는지 확인하고, 실제로 보낼 요청을 준비합니다.',
        'prelude_ok, calls, remaining, grace_call은 지면용 이름입니다. 원래 조건은 _prelude_action != "break" and ((s.api_call_count < agent.max_iterations and agent.iteration_budget.remaining > 0) or agent._budget_grace_call)입니다. phase 결과 분기는 생략했습니다.', (1, 2, 4, 5))
    walkthrough('HTRACE', '모델 응답을 받고 루프를 잇는 코드', '앞 장의 전송 준비 직후부터 도구 실행 또는 답변까지 따라갑니다.',
        'conversation_loop.py · v0.22.5 · 실제 함수 호출 축약', [
        ('① _run_api_retry_loop', '_run_api_retry_loop(agent, s)', '모델 응답을 얻는 구간. 통신 재시도는|이 호출 내부에서 처리'),
        ('② apply_retry_restarts', '_run_phase(apply_retry_restarts, agent, s)', '모델 전환 등으로 요청을 다시 준비해야|하면 바깥 루프로 돌아감'),
        ('③ normalize_model_response', '_run_phase(normalize_model_response, agent, s)', '받은 응답을 공통 메시지로 정리해|도구 호출 목록을 읽을 수 있게 함'),
        ('④ run_tool_round', 'if s.assistant_message.tool_calls:\n    _run_phase(run_tool_round, agent, s)', '예: A17 조회 → 반환값을 이력에 추가 →|다음 모델 요청이 그 값을 읽음'),
        ('⑤ finish_text_response', 'else:\n    _run_phase(finish_text_response, agent, s)', '도구 호출이 없으면 텍스트 종료 경로.||응답 상태에 따른 예외 분기는 Sources 참고'.replace('||','|')),
        ], 'Hermes는 응답을 읽고 도구 결과를 다음 요청에 넣거나, 답변을 정리합니다.',
        '원본은 두 handler를 조건식으로 골라 _run_phase에 넘깁니다. Tool 분기도 승인 대기나 종료 같은 상태를 반환할 수 있고 텍스트 분기에도 복구·연장 조건이 있습니다. SDK의 네트워크 재시도는 외부 반복 카운터와 별개입니다.', (1, 3, 4, 5))
    walkthrough('HEXIT', '루프가 멈추는 세 가지 이유', '어디에서 멈추는지와 실행 뒤에 남는 결과를 나눠 봅니다.',
        'Hermes v0.22.5 · 실제 분기 위치를 묶은 의사코드', [
        ('중단', 'if agent._interrupt_requested:\n    return _verdict("break")\n# 호출 중: handle_api_interrupt(...)', '새 호출 전에는 중단 표시를 확인.|호출 중 InterruptedError는 별도로 처리.'),
        ('호출 예산 소진', 'if agent._budget_grace_call:\n    agent._budget_grace_call = False\nelif not agent.iteration_budget.consume():\n    return _verdict("break")', 'max_turns 기본 null. 설정된 상한을|소진하면 조건부 정리 호출만 허용.'),
        ('모델 요청 오류', 'while s.retry_count < s.max_retries:\n    # 실패 원인에 따라 분기\n    handle_api_error(...)', 'api_max_retries 기본 3.|원인에 따라 재시도·대체 모델·실패 처리.'),
        ], '중단 뒤에도 이미 실행된 도구의 외부 효과는 남을 수 있습니다.',
        '기본값은 hermes_cli/config_defaults.py 기준입니다. 3은 Hermes 내부 재시도 루프의 상한이며 최초 호출 외에 항상 세 번 더 요청한다는 뜻이 아닙니다. SDK 재시도는 별도입니다. finalize_turn은 루프 종료 후 정리하며 일부 조기 반환 경로는 따로 있습니다.')
    slides['HEXIT']['sources'] += [ref for ref in slides['HLOOP']['sources'] if ref[0] == 'R-loop']

    parts = [('기본 지시','SOUL · 모델/도구 안내 · 고정 Skill'),
             ('작업 환경','프로젝트 규칙 · workspace · 호출자 지시'),
             ('기억과 확장','Skills 목록 · MEMORY/USER · 외부 Memory'),
             ('환경에 따른 정보','Plugin · 프로필 · 시간 · 실행 환경')]
    diagram = ''.join(group(i+1, box((i%2)*835, 70+(i//2)*235, 805, 190, a,b,'context',31))
                      for i,(a,b) in enumerate(parts))
    update('HCTX','시스템 프롬프트에는 무엇이 들어갈까?','세션을 시작할 때 조립하는 지시를 역할별로 봅니다.',
           diagram,'다음 장에서 이 지시가 대화 이력·도구 목록과 어떻게 합쳐지는지 봅니다.',
           [a for a,_ in parts],
           '\n\n'.join(a+' — '+b for a,b in parts)+'\n\n환경과 설정에 따라 블록은 생략됩니다. 소스의 stable/context/volatile 조립 순서와 역할별 분류는 별개입니다.')
    slides['HCTX']['sources'] = slides['S07']['sources'].copy()
    from html import escape
    slides['S07']['diagram'] = slides['S07']['diagram'].replace(
        escape('SOUL / 기본 정체성 · 모델·Tool 지침'), escape('기본 지시와 작업 환경'))
    for line in ('프로젝트·호출자·작업공간·운영 지침', 'Skills 인덱스 / auto-load · MEMORY / USER',
                 '외부 Provider · Plugin · 시간·환경 힌트'):
        slides['S07']['diagram'] = slides['S07']['diagram'].replace(escape(line), '')
    hermes_src = 'https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/'
    for slide_id, paths in {
        'HLOOP': ['turn_request_assembly.py', 'turn_preflight_gate.py'],
        'HTRACE': ['turn_response_intake.py', 'turn_tool_round.py', 'turn_final_response.py'],
    }.items():
        slides[slide_id]['sources'] += [('R-'+path, path+' · v0.22.5', hermes_src+path) for path in paths]

    walkthrough('S10','memory 도구에 무엇을 보낼까?', '저장할 대상과 수정할 문장을 지정합니다.',
        '모델이 생성하는 Tool 인자 예시 · Python 공개 API 아님', [
        ('파일 선택', '"target": "memory"  # 또는 "user"', 'MEMORY.md 2,200자 / USER.md 1,375자.|프로필 설정에서 변경 가능.'),
        ('저장할 작업 지정', '"action": "add", "content": "단위를 표시"\n"action": "patch", "old_text": "...",\n    "new_text": "..."\n"action": "remove", "old_text": "..."', 'add는 추가, patch는 찾아서 수정,|remove는 지정한 내용을 삭제.'),
        ('여러 변경을 함께 요청', '"operations": [{"action": "add", ...}]', '여러 작업은 operations 배열로 전달.|한도 초과 시 오류를 반환하고 쓰지 않음.'),
        ('현재 대화에서 알 수 있는 값', '{"success": true, "done": true, "target": "memory"}', '모델은 자신의 호출 인자와 Tool 응답을|이력으로 봄. 시스템 프롬프트는 그대로.'),
        ], '다음 세션이나 프롬프트를 다시 만드는 시점에 저장된 내용을 읽습니다.',
        '성공 응답 예시는 필드 일부입니다. 기본 성공 결과는 기억 전체를 반환하지 않습니다. 따라서 현재 대화의 모델은 방금 입력한 문장과 저장 성공을 알 수 있지만, 변경된 MEMORY.md 전체가 자동으로 다시 주입되지는 않습니다.')
    diagram = ''
    for i,(a,b) in enumerate([('기본 설정','모델이 기억 저장을 요청하면|내용 검사 후 바로 저장'),
                               ('승인을 켰고 사람이 접속 중','지원되는 화면에서|저장할 내용을 보여주고 결정 요청'),
                               ('승인을 켰지만 사람이 없음','예: Cron 실행. 변경 요청을 남겨|나중에 /memory pending에서 확인')]):
        diagram += group(i+1,box(i*555,170,530,220,a,b,('context','runtime','tool')[i],28))
    update('HMEM','기억을 쓰기 전에 사람에게 물어볼까?', '기본은 바로 저장입니다. 승인 설정을 켜면 실행 환경에 따라 달라집니다.',
           diagram,'write_approval 기본값은 false입니다.', ['기본','대화형 승인','나중에 검토'],
           '기본: write_approval: false. 파일 크기, 내용, 수정 대상 검사는 별도입니다.\n\n대화형: true이고 승인 통로가 있으면 변경을 보여주고 결정받습니다.\n\n무인 실행: 검토 요청을 보류 파일에 남길 수 있습니다. /memory approve <id>와 /memory reject <id>로 처리합니다. 백그라운드 삭제에는 별도 보호가 적용될 수 있습니다.')
    walkthrough('S11','session_search에 무엇을 보낼까?', '같은 도구가 인자에 따라 네 가지 동작을 고릅니다.',
        'session_search_tool.py · 실제 인자와 _dispatch 우선순위', [
        ('① 특정 메시지 주변 보기','{"session_id": "abc", "around_message_id": 42,\n "window": 5}', '세션과 메시지 번호가 있으면 주변 조회.|window 기본 5.'),
        ('② 세션 열기','{"session_id": "abc"}','세션 ID만 있으면 해당 세션을 읽음.'),
        ('③ 최근 세션 목록','{"query": "", "limit": 3}','세션 ID 없이 검색어가 비면 최근 목록.|limit 기본 3, 허용 범위 1~10.'),
        ('④ 검색어로 찾기','{"query": "ALARM-17 OR vacuum", "after": "7d",\n "role_filter": "user,assistant", "limit": 3}','검색어가 있으면 DB에서 검색.|after/before는 세션 시작 시각 기준.'),
        ], 'session_id를 보내면 검색어보다 세션 읽기 경로가 먼저 선택됩니다.',
        'sort는 newest/oldest, detail은 adaptive/full을 받습니다. 검색 범위는 profile 및 제외 세션 등 런타임 필터에도 영향을 받습니다. 예시 ID와 내용은 설명용입니다.')
    for key in ('S14A','HCHILD','HMULTI'):
        slides[key]['section'] = 'Hermes / 위임'
    divider = slides['HLONG']
    divider.update(title='위임', sub='한 Agent가 다른 Agent에게 일을 나누는 과정을 봅니다.')
    divider['diagram'] = text(0, 210, '위임', 77, 'text', 700) + rule(5, 350, 1645, 350) + text(5, 450, '부모의 요청 → 자식 실행 → 결과 회수', 34, 'context', 700)

    from pydantic_walkthroughs import apply_pydantic
    apply_pydantic(slides, env, walkthrough, update)
