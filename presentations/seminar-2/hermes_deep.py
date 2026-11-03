"""Code-grounded Hermes teaching revision, including version-scoped corrections."""
from copy import deepcopy
from pathlib import Path
from html import escape
import base64
import json
from hermes_observability import IDS as OBSERVABILITY_IDS

ORDER=['S04','S05','HLOOP','HTRACE','HEXIT','HCTX','S07','S08','S10','HMEM','S11','HSEARCH','S09',
       'HTOOL','S13','HSCHEMA','HCONNECT','HVALID','S13A','S13B','HHUMAN','HFAIL','S14',
       'S12','HLEARN','HWRITE','HCURATOR','HCONSOLIDATE',
       'HLONG','S14A','HCHILD','HMULTI',
       'HCRON','S14C','HCRONUSE','HCRONTRADE','HCOMMAND','S15']
ORDER[ORDER.index('HLONG'):ORDER.index('HLONG')]=OBSERVABILITY_IDS

def apply_deep(slides,env):
    old=deepcopy(slides);root=env['ROOT'];text,box,arrow,group,rule=(env[n] for n in ('text','box','arrow','group','rule'))
    evidence=json.loads((root/'research/hermes-v0.22.5-evidence.json').read_text(encoding='utf-8'))['sources']
    for s in slides.values():s.pop('chapter',None)
    slides['S01']['steps']=['전체 구성']
    # This display change does not change the overview's content or topology.
    import re
    slides['S01']['diagram']=re.sub(r' data-focus="\d+"','',slides['S01']['diagram'])

    def image(name,x,y,w,h):
        data=base64.b64encode((root/'assets'/name).read_bytes()).decode()
        return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/svg+xml;base64,{data}" preserveAspectRatio="xMidYMid meet"/>'

    slides['S03H']['diagram']+=image('hermes-official.svg',1115,30,125,125)
    slides['S03H']['sources'].append(('ASSET','Hermes official icon','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/static/img/favicon.svg'))

    def put(ident,title,sub,take,section,diagram,steps,terms,explanation,keys,base='S04',kind='content-slide',code_kind=None):
        s=deepcopy(old.get(ident,old[base]))
        if ident not in old:s['originalSpec']=''
        sources=list(s['sources']) if ident in old else []
        for k in keys:
            e=evidence[k]
            sources.append(('R-'+k,e['path']+' · v0.22.5',e['url']))
        s.update(id=ident,title=title,sub=sub,take=take,section='Hermes / '+section,diagram=diagram,
                 kind=kind,steps=['전체 구성']+steps,demo='hermes' if ident=='S15' else None,
                 concepts=[{'term':a,'meaning':b} for a,b in terms],explanation=explanation,sources=list({r[0]:r for r in sources}.values()),
                 version='Hermes v0.22.5 · 공식 코드 대조',researchKeys=keys,
                 localEvidence=[{'path':'hermes/Hermes_Agent_2차_심층_학습_분석.md','sections':'관련 개념의 기초; 코드·기본값은 Sources의 고정 소스로 재대조'}],
                 editorialBasis='hermes_deep.py / user-requested code-level revision',codeKind=code_kind)
        s.pop('chapter',None)
        s['note']='## '+title+'\n\n### 주요 개념\n\n'+'\n\n'.join('**'+a+'**: '+b for a,b in terms)+'\n\n### 설명\n\n'+explanation+'\n\n### 발표 포인트\n\n'+take
        if code_kind:s['note']+='\n\n### 코드 표시\n\n'+code_kind
        slides[ident]=s;return s

    def code(x,y,w,h,lines,caption='공식 함수·분기 축약 · 실행 가능한 전체 코드 아님',size=23):
        out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#F0F4FA" stroke="#7E90A8"/>'
        out+=text(x+24,y+35,caption,20,'muted')+rule(x,y+58,x+w,y+58)
        for i,line in enumerate(lines.splitlines()):out+=env['code_line'](line,x+24,y+96+i*33,size)
        return out

    def notes(items,x=1120,y=55,w=530,h=135):
        return ''.join(group(i+1,box(x,y+i*(h+45),w,h,a,b,c,29)) for i,(a,b,c) in enumerate(items))

    def chain(items,y=95,w=480,gap=105,h=150,connect=True):
        d=''
        for i,(a,b,c) in enumerate(items):
            x=i*(w+gap);d+=group(i+1,box(x,y,w,h,a,b,c,29))
            if connect and i<len(items)-1:d+=group(i+1,arrow(f'M{x+w} {y+h/2} H{x+w+gap-12}',c))
        return d

    def divider(ident,name,sub,parts):
        d=text(0,210,name,77,'text',700)+text(5,285,sub,32,'muted')
        d+=rule(5,350,1645,350)
        for i,p in enumerate(parts):d+=text(5+i*550,450,p,30,'context',700)
        put(ident,name,sub,'','구분',d,[],[(name,sub)],'다음 범주를 시작하는 전환 장표입니다. '+ ' → '.join(parts)+' 순서로 살펴봅니다.',[],kind='topic-divider')

    # Page 6 now describes exactly the subjects in the following pages.
    d=''
    for i,(a,b) in enumerate([('실행 루프','반복 조건 · 중단 · 예산 · 오류'),('Context와 기억','System Prompt · Session · Memory · 검색'),('Tools와 Skills','등록 · 노출 · 검증 · 승인 · 자체 절차 수정'),('안전장치와 기록','Guardrail · 정책 확장 · Trace 수집·활용'),('긴 작업과 위임','Prefix Cache · 압축 · 병렬 Tool · Subagent'),('예약 실행과 활용','Cron · 사용 명령 · 실제 관찰 Demo')]):
        y=20+i*100;d+=group(i+1,text(0,y+36,a,33,'runtime',700)+text(490,y+36,b,29,'text')+rule(0,y+83,1652,y+83))
    put('S04','Hermes 내부 구성과 설명 순서','범용 Agent Harness에서 실제 작업이 이어지는 과정을 살펴봅니다.','실행 흐름을 먼저 보고, 입력·도구·상태·확장 기능을 차례로 확인합니다.','전체 흐름',d,
        ['실행 루프','Context와 기억','Tools와 Skills','안전장치와 기록','긴 작업과 위임','예약과 활용'],
        [('범용 Agent Harness','모델 호출뿐 아니라 도구 실행, 이력·지식 관리, 작업 제어를 제공하는 실행환경입니다.')],
        '제품 기능 전체를 다시 나열하는 장표가 아니라 이번 Hermes 본편의 설명 범위입니다. Gateway·API 운영 구조는 요청에 따라 제외했습니다. CLI/TUI/Desktop 등의 입력 표면이 있다는 사실과 상세 운영 아키텍처를 강의하는 것은 구분합니다.',['loop','prompt','registry','curator','cron'])

    # Outer iteration and inner retry are deliberately separate.
    d=code(0,40,1030,550,'while iteration_allowed:\n    begin_iteration(...)\n    prepare_iteration(...)\n    assemble_api_request(...)\n    run_preflight_gate(...)\n    announce_api_call(...)\n    _run_api_retry_loop(...)\n    apply_retry_restarts(...)\n    normalize_model_response(...)\n    # 응답에 따라 하나의 분기로 진행\n    run_tool_round(...)       # Tool\n    finish_text_response(...) # Text',size=22)
    d+=notes([('반복 조건','호출 상한 + remaining budget|또는 일회성 grace call','runtime'),('매 반복 진입','중단 확인 · 카운터 증가|예산 consume 후 호출 준비','context'),('안쪽 retry','한 모델 요청의 통신 복구|바깥 Tool 반복과 구분','model')])
    put('HLOOP','루프 한 번이 지나는 실제 함수들','conversation_loop.py → turn_iteration_prep.py → turn_*','Tool·Context의 세부 처리는 뒤에서 보고, 여기서는 반복 제어를 따라갑니다.','실행 루프',d,
        ['반복 조건','반복 진입','안쪽 retry'],
        [('바깥 반복','호출 횟수와 IterationBudget.remaining, _budget_grace_call로 진입을 결정합니다.'),('begin_iteration','pending redirect·interrupt·budget을 확인하고 논리 호출 카운터를 증가시킵니다.'),('API retry loop','build_api_request → perform_api_call → check_api_response를 오류 처리와 함께 반복합니다.')],
        'v0.22.5 conversation_loop.py 1724~1777을 추적한 호출 순서입니다. 실제 코드는 _run_phase(...)의 verdict.action에 따라 return/break/continue로 분기합니다. 화면의 iteration_allowed는 긴 원 조건을 대신한 설명용 이름이며 실제 함수가 아닙니다. 조건은 (s.api_call_count < agent.max_iterations and agent.iteration_budget.remaining > 0) or agent._budget_grace_call입니다.\n\nbegin_iteration은 interrupt를 먼저 확인하고 api_call_count를 증가시킨 뒤 예산을 소비합니다. prepare_iteration, assemble_api_request, preflight와 모델 요청을 거치고 정상화된 응답을 Tool 또는 최종 텍스트 경로로 넘깁니다. API retry는 이 바깥 반복 안에 따로 있습니다. 이 카운터를 실제 HTTP 요청 수로 동일시하면 SDK/프록시 재시도나 preflight 재시작을 놓칠 수 있습니다.',
        ['loop','prep','retry'],code_kind='공식 함수명과 제어 흐름을 유지한 축약 의사코드. _run_phase 래퍼와 일부 분기를 생략했으며 복사 실행용이 아니다.')

    d=text(0,35,'예시 · max_turns = 3, 통신 오류·압축·grace 없음',28,'muted')
    d+=chain([('반복 1','모델 → Tool A 요청|결과를 이력에 추가','model'),('반복 2','모델 → Tool B 요청|결과를 이력에 추가','tool'),('반복 3','모델 → 최종 텍스트|답변 정리 후 종료','success')],y=135,h=185)
    d+=group(4,box(0,450,1650,150,'항상 3번 실행되는 것은 아닙니다','첫 응답이 최종 답변이면 1회 · 설정된 상한/중단/오류에 따라 더 일찍 종료','runtime',31))
    put('HTRACE','한 요청에서 루프가 세 번 도는 예','호출 결과가 다음 반복의 입력이 되는 과정을 봅니다.','횟수는 모델의 응답과 실행 조건으로 정해지며 고정된 작업 수가 아닙니다.','실행 루프',d,
        ['첫 호출','두 번째 호출','최종 답변','기본값과 예외'],
        [('반복 예시','예산 3, Tool 두 번 뒤 답변 한 번을 가정한 교육용 사례입니다.'),('기본 제한값','v0.22.5 DEFAULT_CONFIG의 agent.max_turns는 null(무제한)이며 API retry 기본은 3입니다.')],
        '실제 Hermes를 실행한 Trace가 아닌 제어 흐름 예시입니다. 반복 1/2에서 Tool 결과를 넣고 반복 3에서 최종 텍스트를 받아 종료한다고 가정합니다. 과거 학습자료의 500/50을 모든 버전의 기본 반복 제한으로 쓰지 않습니다. 이번에 확인한 고정 소스에서 agent.max_turns는 None, constructor max_iterations는 sys.maxsize이며 명시 상한과 종료 조건이 실제 실행을 제한합니다. delegation.max_iterations 기본 250은 별도 자식 설정입니다.\n\n예산 카운터에는 execute_code refund, grace 등의 예외가 있어 단순 HTTP 횟수와 1:1이라는 주장도 피합니다. 화면의 3회는 오류·압축·grace가 없는 선택된 예입니다.',
        ['defaults','loop','prep'])

    d=code(0,50,1030,550,'# begin_iteration · 일부 분기 발췌\nif agent._interrupt_requested:\n    return _verdict("break")\nif agent._budget_grace_call:\n    agent._budget_grace_call = False\nelif not agent.iteration_budget.consume():\n    return _verdict("break")\n# API retry · _run_phase 래퍼 축약\ntry:\n    perform_api_call(...)\nexcept InterruptedError:\n    handle_api_interrupt(...)\nexcept Exception:\n    handle_api_error(...)',caption='두 함수의 핵심 분기 재구성 · 상태 대입/인자/phase 래퍼 생략',size=22)
    d+=notes([('중단','새 요청 전 interrupt 확인|호출 중 InterruptedError 처리','risk'),('예산 소진','remaining / 호출 상한 확인|조건부 toolless 정리 호출','context'),('오류','API retry 기본 3 · 원인별 처리|fallback·복구 또는 실패 정리','runtime')])
    put('HEXIT','중단·예산 소진·오류의 종료 경로','모두 같은 break 한 줄로 끝나는 처리가 아닙니다.','종료 원인과 완료·실패·부분 결과를 구분해 기록합니다.','실행 루프',d,
        ['중단','예산','오류와 정리'],
        [('Interrupt','반복 진입의 중단 플래그와 모델 호출 중 InterruptedError가 별도 처리됩니다.'),('Budget 종료','일반 반복을 멈추고 조건에 따라 도구 없는 grace 호출이나 보존된 부분 응답으로 정리합니다.'),('Finalizer','정상 루프 종료 후 transcript·상태·실패 정보를 정리합니다. 모든 early return이 이 함수만 통과하는 것은 아닙니다.')],
        'begin_iteration의 interrupt 경로는 _turn_exit_reason을 남기고 break합니다. 호출 중 interrupt는 handle_api_interrupt에서 redirect 재시작 여부와 취소 상태를 처리합니다. 이미 시작한 외부 Tool 효과를 되돌린다는 의미는 아닙니다.\n\n상한·IterationBudget 또는 run budget은 서로 다른 제약입니다. 소스는 조건부 _budget_grace_call을 소비해 도구 없는 정리 기회를 제공하고, finalizer는 budget_exhausted·interrupted·failed 등에 맞춰 결과를 만듭니다. API 예외는 handle_api_error에서 retry/fallback/복구/실패를 선택합니다. 인증·형식 오류와 일시 네트워크 장애를 같은 무한 재시도로 처리하지 않습니다. 직접 early result를 반환하는 경로도 있어 finalize_turn이 예외 없이 모든 경로를 덮는다고 말하지 않습니다.',
        ['prep','retry','final'])

    divider('HCTX','Context와 기억','모델 입력과 저장된 정보를 함께 살펴봅니다.',['System Prompt','Session·Memory','과거 대화 검색'])
    d=group(1,box(0,35,780,310,'System Prompt snapshot','SOUL / 기본 정체성 · 모델·Tool 지침|프로젝트·호출자·작업공간·운영 지침|Skills 인덱스 / auto-load · MEMORY / USER|외부 Provider · Plugin · 시간·환경 힌트','context',31))
    d+=group(2,box(0,410,780,180,'Session History','SQLite · sessions / messages · FTS5|user · assistant · tool + 연결 ID|미디어·reasoning은 모델/API 지원 조건에 따라','context',31))
    d+=group(3,box(980,35,670,145,'이번 호출의 추가 정보','예산·Context 압박 · steer 등|세션 snapshot과 별도 채널','runtime',31))
    d+=group(4,box(980,255,670,145,'tools 필드','이름 · description · parameters schema|실행 함수·인증 객체는 포함하지 않음','tool',31))
    d+=group(5,box(980,475,670,145,'Provider Adapter → API 요청','모델 · messages / system · tools · 호출 옵션','model',30)+arrow('M780 180 H860 V550 H968','context')+arrow('M780 485 H860','context')+arrow('M1315 400 V463','tool')+arrow('M980 105 H930 V550 H968','runtime'))
    put('S07','모델 입력과 Session·Memory의 관계','화면의 대화만으로 모델 입력 전체를 설명할 수는 없습니다.','구성 요소의 역할을 확인하고, 실제 payload는 Demo에서 살펴봅니다.','Context와 기억',d,
        ['System Prompt','Session History','호출별 정보','Tool schema','최종 요청'],
        [('System snapshot','정체성·지침·Skills·Memory·외부/Plugin·런타임 정보를 구성하며 조건에 따라 생략됩니다.'),('Session과 Memory','Session은 이력, Memory는 snapshot의 지속 사실을 공급합니다.'),('최종 payload','이력·호출별 정보·tools와 API 옵션을 Provider 형식으로 변환한 결과입니다.')],
        'system_prompt.py의 실제 assemble 계층을 대조했습니다. stable에는 identity, Tool/모델 안내, pinned auto-load와 coding 지침이 들어가고 context에는 system_message·프로젝트 파일·workspace snapshot·operator/platform 안내가 들어갑니다. volatile에는 Skills 인덱스와 built-in/외부 Memory, Plugin after_memory 섹션, profile/time/environment가 구성됩니다. 모든 블록이 항상 활성화되는 것은 아닙니다.\n\n공식 Prompt Assembly 문서에는 Skill 인덱스 위치가 서로 다르게 적힌 부분이 있으므로 이 도식은 논리 역할을 보여주고 순서는 고정 소스를 기준으로 설명합니다. 대화 메시지에는 텍스트 외에 미디어·추론·도구 메타데이터가 있을 수 있고 API 모드에 따라 표현이 다릅니다. 이 그림은 바이트 단위 전체 payload 명세가 아닙니다. 실제 조립 결과는 Demo에서 adapter 전후 JSON으로 확인합니다. 세션 중 Memory 파일 변경만으로 snapshot이 즉시 바뀌지 않지만, 새 세션·명시 갱신·압축 재빌드 경계에서 다시 읽는 경로는 존재합니다.',
        ['prompt','loop','memory','registry'])

    d=code(0,45,1030,520,'memory(\n  target="memory",\n  operations=[{\n    "action": "add",\n    "content": "보고서에는 단위를 표시"\n  }]\n)\n# 모델이 생성하는 Tool 인자 예시',caption='memory Tool 인자 예시 · 저장 실행은 Hermes가 처리',size=24)
    d+=notes([('대상 파일','MEMORY.md · USER.md|프로필의 memories/ 아래','context'),('Inline 처리','Agent의 MemoryStore 사용|크기·내용·변경 대상 검증','runtime'),('저장과 반영','파일 변경 + Tool 반환|현재 snapshot은 즉시 교체 안 됨','tool')])
    put('S10','memory Tool은 무엇을 어떻게 저장할까?','Tool 요청에서 MemoryStore와 파일 변경까지','“기억했다”는 문장보다 Tool 반환과 파일 변경을 확인합니다.','Context와 기억',d,
        ['파일 구조','Inline Store','저장과 반영'],
        [('memory','add/patch/remove와 operations batch를 받아 built-in Store에 적용하는 상태 의존 Tool입니다.'),('MemoryStore','기본 문자 한도와 내용·대상 검증 뒤 변경을 원자적으로 저장합니다.')],
        '표시는 모델의 memory Tool 인자 예시이며 Python 공개 SDK 함수 호출 예제가 아닙니다. 실제 schema는 대상 memory/user와 add/patch/remove, content/old_text/new_text 또는 operations를 사용합니다. 실행기는 Agent 상태의 MemoryStore를 전달하고 memory_tool_store.py가 한도·내용·대상과 파일 변경을 처리합니다. MEMORY.md 기본 2,200자, USER.md 기본 1,375자이며 설정 가능합니다.\n\n한도 초과는 기존 사실을 조용히 버리는 대신 오류를 반환해 모델이 축약·patch/remove를 선택하게 합니다. 파일에 쓴 사실을 Tool 결과로 보는 것과 System snapshot의 교체는 별개입니다. 새 세션 또는 재빌드 경계의 반영까지 나누어 확인합니다. 비밀값·raw 생산 데이터 보관소로 사용하는 것은 이 작은 Memory의 목적과 다릅니다.',
        ['memory','store','write','defaults'])
    d=code(0,45,910,525,'memory:\n  memory_enabled: true\n  user_profile_enabled: true\n  write_approval: false\n  memory_char_limit: 2200\n  user_char_limit: 1375\n\n# v0.22.5 DEFAULT_CONFIG',caption='고정 소스의 기본 설정 · 실행 환경의 config가 우선',size=26)
    d+=notes([('false · 기본','일반 쓰기 승인 Gate를 끔|검사까지 모두 끄는 설정은 아님','context'),('true · 대화형','지원 UI/callback에서 검토|승인 또는 거절','runtime'),('true · 무인/백그라운드','pending/memory/<id>.json|/memory pending·approve·reject','tool')],x=1030,w=620)
    put('HMEM','Memory 쓰기 승인은 기본으로 켜져 있을까?','기본 설정과 승인 활성화 이후의 경로를 나눠 봅니다.','write_approval과 Memory 기능의 활성화는 서로 다른 설정입니다.','Context와 기억',d,
        ['기본 설정','대화형 승인','보류된 쓰기'],
        [('write_approval 기본값','v0.22.5는 false이며 미설정·잘못된 값도 일반 Gate off로 해석하는 코드가 있습니다.'),('보류','지원 대화형 승인 통로가 없으면 pending 기록으로 검토를 남깁니다.')],
        'config_defaults.py와 write_approval.py를 대조했습니다. memory_enabled/user_profile_enabled는 기능을 켜는 설정이고 write_approval은 일반 쓰기 검토의 별도 boolean입니다. false가 모든 내용 검사나 특수 보호까지 해제한다는 뜻은 아닙니다. 코드에는 background destructive operation의 추가 보호와 모듈 로딩 실패 시 fail-open인 경로도 있어 전 경로의 fail-closed 보장으로 표현하지 않습니다.\n\ntrue일 때 foreground는 지원 callback/CLI 경로로 검토할 수 있고, 사용자 응답 통로가 없는 cron·background 등에서는 pending으로 남깁니다. 정확한 payload는 프로필 pending/memory/<id>.json에 보관됩니다. /memory pending, /memory approve <id>, /memory reject <id>로 관리하며 patch/remove의 target 변경을 검사해 오래된 승인 적용을 막는 경로가 있습니다. Store 크기·내용 검증과 사용자 승인을 구분합니다.',
        ['defaults','write','memory'])

    d=code(0,50,1010,500,'{\n  "query": "ALARM-17 OR vacuum",\n  "after": "7d",\n  "role_filter": "user,assistant",\n  "limit": 3\n}\n# session_search Tool 인자 예시',caption='검색어와 범위는 모델의 Tool Call 또는 명시 요청으로 선택',size=24)
    d+=notes([('Discovery','query로 FTS 검색|현재/숨김/계보 범위 처리','context'),('Read / Scroll','session_id로 읽기|around_message_id로 주변 탐색','runtime'),('Recent','query가 비어 있으면|최근 세션 목록 경로','tool')],x=1100,w=550)
    put('S11','session_search는 인자에 따라 다르게 동작합니다','검색·세션 읽기·주변 탐색·최근 목록의 네 가지 형태','검색 범위는 Tool 인자와 Runtime의 세션 가시성 규칙으로 결정됩니다.','Context와 기억',d,
        ['질의 검색','세션·주변 읽기','최근 목록'],
        [('query 작성자','모델이 사용자 질문을 보고 Tool의 query·after/before·쉼표 구분 문자열 role_filter 등을 선택하거나 사용자가 명시합니다.'),('Runtime 범위','DB 질의 필터, 현재 세션/lineage, 숨김 source 등 실행기의 조건을 추가 적용합니다.')],
        'session_search_tool.py의 _dispatch는 session_id+around_message_id이면 scroll, session_id만 있으면 read, 빈 query이면 recent, 그 외에는 discovery를 선택합니다. query는 이 Tool이 별도 LLM으로 다시 써 주는 검색어가 아닙니다. 모델이 생성한 Tool 인자를 Runtime이 검증·정규화합니다. after/before는 ISO 또는 7d/24h 등 상대 시각을 파싱합니다.\n\n현재 태그의 discovery는 기본 limit 3(1~10 clamp), user/assistant 중심 검색, 세션 계보 중복 제거와 adaptive hydration을 사용합니다. session_id는 discovery의 단순 필터가 아니라 읽기 모드를 고르는 인자라는 점이 중요합니다. 시간 필터는 이 코드의 세션 시작 시각 기준을 확인해야 하며 업무의 측정 데이터 기간과 동일시하지 않습니다. profile 인자는 운영 범위 선택이며 별도 인가를 대신하지 않습니다.',
        ['search','sql'])
    d=chain([('모델이 query 선택','사용자 질문 → Tool 인자','model'),('코드가 문법 정리','_sanitize_fts5_query','runtime'),('SQL과 결과 선택','MATCH · 필터 · 계보 정리','context')],y=55,h=160)
    d+=group(4,box(0,370,760,185,'검색어 정리 예','ALARM-17 → "ALARM-17"|따옴표 보존 · 특수 문자·끝 연산자 정리|의미를 새로 추론하는 단계가 아님','runtime',30)+box(890,370,760,185,'조회 범위와 반환','role/source/time 가시성 조건|FTS / CJK / LIKE 대체 경로|선택 메시지와 주변 문맥을 반환','context',30))
    put('HSEARCH','검색어 정리와 범위 확인은 누가 할까?','모델의 질의 선택과 Python의 문법·가시성 처리를 구분합니다.','문법상 검색 성공과 업무상 올바른 근거 검색은 따로 확인합니다.','Context와 기억',d,
        ['질의 선택','문법 정규화','DB 검색','구체 예와 반환'],
        [('Sanitizer','인용구를 보존하고 지원하지 않는 구문·끝 연산자·기호를 정리하며 점·하이픈 단어를 인용하는 문자열 처리입니다.'),('FTS/범위','SQL에 role/source/time 조건을 넣고 가시성과 계보를 고려해 세션과 메시지를 선택합니다.')],
        'hermes_state_search.py의 _sanitize_fts5_query는 인용 문구를 임시 보존하고 지원되지 않는 문자, 퍼센트·와일드카드·dangling boolean을 정리한 뒤 dotted/hyphenated/underscored 단어를 인용하고 문구를 복구합니다. 이는 결정적 Python 처리이며 LLM이 검색어 의미를 재해석하는 단계가 아닙니다. ALARM-17 인용은 이 코드 규칙을 보여주는 예입니다.\n\nDB는 MATCH와 rank/snippet, 공통 role/source/session-start 필터를 사용하고 환경·문자열에 따라 CJK 인덱스나 LIKE fallback을 택합니다. Tool은 현재 live context와 계보, 제외 세션, 제목 일치와 limit 등을 고려해 결과를 구성합니다. 검색된 코드가 맞더라도 다른 설비·기간이면 업무상 정답이 아닐 수 있습니다. 이 마지막 검증은 사용자 업무 평가 기준이며 Hermes가 측정 데이터의 도메인 정답을 자동 보장하는 기능은 아닙니다.',
        ['sql','search'])

    divider('HTOOL','Tools와 Skills','실행 능력과 재사용 절차를 연결합니다.',['도구 등록·검증','승인·실행','Skill 작성·관리'])
    d=code(0,45,1030,535,'registry.register(\n    name="skills_list",\n    toolset="skills",\n    schema=SKILLS_LIST_SCHEMA,\n    handler=...,  # 실제 lambda 본문 생략\n    check_fn=check_skills_requirements\n)',caption='tools/skills_tool.py 731~734의 등록 항목 재배치·축약',size=25)
    d+=notes([('Discovery','tools/*.py의 AST에서|최상위 registry.register 탐색','runtime'),('Import → Registry','모듈 import 시 등록 실행|schema와 handler를 따로 보관','tool'),('가용성','활성 Toolset·check_fn|선택한 schema만 모델에 공개','context')])
    put('S13','Hermes Tool은 이렇게 등록됩니다','실제 skills_list 등록 코드로 schema와 handler를 구분합니다.','Python 파일을 두는 것만으로 모든 함수가 Tool이 되지는 않습니다.','Tools와 Skills',d,
        ['AST 발견','등록','활성·가용성'],
        [('등록','ToolRegistry가 name/toolset/schema/handler/check_fn 등을 보관합니다.'),('Discovery','최상위 registry.register 호출을 찾은 모듈을 import해 등록 코드를 실행합니다.')],
        '표시 코드는 tools/skills_tool.py의 실제 registry.register 항목을 읽기 좋게 재배치한 축약이며 handler lambda 본문과 emoji 등을 생략했습니다. 실제 handler는 skills_list(category=args.get("category"), task_id=kw.get("task_id"))를 호출합니다. 모듈 discovery는 AST를 사용하며 helper 파일 전체를 임의 실행 가능한 Tool로 만드는 방식은 아닙니다.\n\n활성 Toolset과 가용성 검사를 거친 이름 집합으로 get_definitions를 구성합니다. 현재 소스의 check_fn probe에는 TTL·scope cache와 예외/last-known 처리 등 세부 로직이 있으므로 단순 매 요청 무조건 재검사라고 말하지 않습니다. ToolEntry.description은 Registry 메타데이터이고 모델 설명의 기준은 schema.description입니다.',
        ['native','registry'],code_kind='공식 등록 코드의 항목 재배치·handler 생략. 이름과 파라미터는 실제 코드에 존재한다.')
    d=code(0,40,1080,550,'{ "type": "function",\n  "function": {\n    "name": "skills_list",\n    "description": "...",\n    "parameters": {\n      "type": "object",\n      "properties": {"category": {"type":"string"}},\n      "required": []\n    }\n  }\n}',caption='실제 SKILLS_LIST_SCHEMA에서 description을 줄인 API 예시',size=23)
    d+=notes([('모델에 보이는 것','함수 이름 · 사용 설명|인자 JSON Schema','context'),('모델에 안 보내는 것','handler 함수 코드 · check_fn|Python 객체·환경변수 원문','runtime'),('실행할 때','모델은 name + arguments를 제안|Runtime이 handler로 연결','tool')],x=1140,w=510)
    put('HSCHEMA','모델에게 공개되는 Tool의 실제 수준','get_definitions()가 만드는 function schema','모델은 실행 코드를 받는 것이 아니라 호출 가능한 계약을 받습니다.','Tools와 Skills',d,
        ['공개 명세','서버에 남는 정보','반환된 호출'],
        [('모델용 schema','name·schema.description·parameters 등이 function definition으로 전달됩니다.'),('서버용 구현','handler/check_fn/credential은 모델 schema를 구성하는 실행 함수와 동일한 데이터가 아닙니다.')],
        'registry.py get_definitions는 entry.schema에 name을 결합하고 dynamic schema override를 반영한 뒤 {type:function,function:schema_with_name} 형식을 반환합니다. 실제 전송 형식은 Provider Adapter에서 바뀔 수 있습니다. skills_list의 category string과 required=[]는 공식 schema의 필드를 따른 예이며 description은 화면에서 줄였습니다.\n\n별도 description= 인자로 Registry 메타데이터만 채워도 모델 schema에 자동 복사되는 것은 아닙니다. 실제 인가와 데이터 범위는 handler/Backend에서 검사해야 합니다. handler 자체를 schema에 보내지 않는다는 설명이지 Tool의 반환 데이터에 비밀이 절대 포함되지 않는다는 보장은 아닙니다.',
        ['registry','native'],code_kind='실제 schema 기반 설명용 JSON. description 축약, 실제 wire capture 아님.')
    d=chain([('Local Tool','tools/*.py → registry.register|model_tools → registry.dispatch','tool'),('MCP Tool','mcp_tool_discovery → 발견·등록|Client → Transport → 외부 Server','tool'),('Plugin','register(ctx) → Tool / Hook|Context·Memory·명령 등 확장','runtime')],y=60,h=205,connect=False)
    d+=group(4,box(0,405,1650,160,'Hermes의 두 실행 경로','memory · session_search · delegate_task 등은 Agent 상태를 쓰는 Inline 경로|일반 Registry/MCP/Plugin 경로와 Hook 적용 범위를 구분','context',31))
    put('HCONNECT','Local Tool·MCP·Plugin은 Hermes 어디에 붙을까?','실제 모듈과 실행 위치로 연결 방법을 비교합니다.','중앙 Hook 하나가 모든 Inline·외부 실행을 감싼다고 가정하지 않습니다.','Tools와 Skills',d,
        ['Native','MCP','Plugin','Inline 예외'],
        [('Native','직접 등록된 schema/handler를 model_tools와 Registry가 연결합니다.'),('MCP','발견한 외부 명세를 Hermes Tool에 등록하고 transport를 통해 서버를 호출합니다.'),('Plugin','register(ctx)로 실행환경에 접점을 추가하는 코드 확장이며 신뢰·호환성을 관리해야 합니다.')],
        '공식 Tools Runtime과 v0.22.5 registry/model_tools를 대조한 역할도입니다. Native discovery 후 MCP discovery와 Plugin 로딩이 기능을 추가합니다. MCP 서버는 stdio subprocess 또는 네트워크 transport를 쓸 수 있으며 이름·schema·서버별 필터와 credential 전달을 확인해야 합니다. Plugin은 ctx.register_tool/register_hook뿐 아니라 MemoryProvider/ContextEngine 등 Hermes 내부 기능도 확장할 수 있습니다.\n\nAgent 상태를 사용하는 memory·session_search·delegate_task는 Inline 가로채기가 있습니다. 따라서 모든 Tool이 동일한 pre/post Hook, terminal guard를 지나간다는 그림은 부정확합니다. MCP 서버 권한과 Plugin 코드 권한도 별도이며 연결 표준이나 schema만으로 데이터 인가가 완성되지는 않습니다.',
        ['registry','memory','delegate'])
    d=chain([('Call ID 정리','중복 ID 고유화·정규화','runtime'),('이름 확인','valid_tool_names · 이름 repair','context'),('인자 확인','dict/빈 값 정규화 · JSON parse','runtime')],y=55,h=160)
    d+=group(4,box(0,390,760,190,'이름 오류','정상·무효 혼합 → 정상 호출 진행, 무효는 오류|모두 무효인 반복 → 3회 후 partial 종료','risk',30)+box(890,390,760,190,'JSON 오류','잘린 인자 → 실행 거부·partial 경로|일반 parse 실패 → 제한 retry 후 Tool 오류 복구','risk',30))
    put('HVALID','validate_tool_calls가 검사하는 순서','이름 오류와 JSON 오류는 서로 다르게 처리합니다.','여기서 하는 검사는 모든 Tool의 업무 의미·권한 검증을 대신하지 않습니다.','Tools와 Skills',d,
        ['ID','이름','JSON','실패 분기'],
        [('ID·이름','이미 사용된 ID와 충돌을 정리하고 허용 이름 및 repair 가능성을 확인합니다.'),('인자 정규화','dict/list를 JSON string으로, 빈 인자를 {}로 정리하고 json.loads를 시도합니다.')],
        'turn_tool_validation.py의 순서는 ID 고유화/Provider ID 정규화→이름 repair 및 valid_tool_names 비교→JSON 정규화와 parse입니다. 정상·unknown 이름이 섞이면 정상 호출을 살리고 unknown에 대응 오류 결과를 반환합니다. 유효 호출이 전혀 없는 이름 오류만 strike가 누적되며 3회 후 partial로 나가는 경로입니다.\n\nJSON은 잘림을 감지하면 실행을 거부하고 partial 종료합니다. 일반 JSON 오류는 제한 retry 뒤 호출/결과 관계를 맞춘 오류 결과를 넣어 모델 복구 기회를 줍니다. 이는 JSON 문법 검사이지 임의 Tool의 모든 business schema를 Pydantic처럼 검증한다는 뜻이 아닙니다. 실제 Tool handler와 별도 정책에서 타입·범위·권한을 추가로 확인합니다.',
        ['validation'])
    # Keep the persisted-call illustration, with more concrete notes already supplied.
    slides['S13A'].pop('chapter',None)
    slides['S13A']['section']='Hermes / Tools와 Skills'
    slides['S13A']['researchKeys']=['persist','validation','registry']
    for k in slides['S13A']['researchKeys']:slides['S13A']['sources'].append(('R-'+k,evidence[k]['path'],evidence[k]['url']))
    d=code(0,40,1080,550,'# check_all_command_guards: 분기 축약\nif isolated_without_host_access:\n    return user_deny_or_approve\nif floor_block(command): return deny\nif prepared_guard: return prepared_guard\nif yolo_or_mode_off: return approve\nif permanent_allowlist: return approve\nif no_human_surface: return context_policy\nif not dangerous or cached: return approve\nreturn human_decision(..., smart=smart_mode)',caption='tools/approval.py 1151~1194 · 실제 순서 기반 축약',size=22)
    d+=notes([('명령 실행 경로','terminal 등의 사전 guard|모든 Tool 공통 함수는 아님','runtime'),('모드보다 앞선 검사','host 접근·강제 floor|준비된 승인 확인','risk'),('사람에게 묻기 전','allowlist·cached 승인|무인 policy·위험 패턴 검사','context')],x=1140,w=510)
    put('S13B','실행 전 검사는 실제로 어떤 순서일까?','terminal 명령의 check_all_command_guards 경로','off·격리 실행도 모든 Tool·권한 정책을 전부 해제한다는 뜻은 아닙니다.','Tools와 Skills',d,
        ['적용 경로','앞선 강제 검사','승인 전 분기'],
        [('Command guard','격리/host 접근, floor, prepared guard, mode·allowlist, 무인 정책, 위험 패턴 등을 순서대로 판단합니다.'),('Tool별 검사','파일 경로 정책·Plugin 규칙·MCP 서버 인가는 해당 Tool 경로에서 별도로 적용됩니다.')],
        'v0.22.5 approval.py를 대조했습니다. host 접근 없는 충분히 격리된 backend는 별도 user-deny 확인 경로이고, 그 밖에는 _floor_block을 mode=off나 yolo보다 먼저 검사합니다. prepared guard 재사용, 영구 allowlist, UI 존재와 무인 문맥, 위험 패턴 및 세션 승인 cache를 거쳐 _human_decision에 도달합니다.\n\n이 그림은 terminal command guard의 순서를 축약한 것이며 파일/MCP/Inline Tool 전부의 단일 순서가 아닙니다. 다른 도구는 경로·인자·handler 검증, pre_tool_call 규칙과 request_tool_approval 등의 경로가 있습니다. 표시의 floor_block 등은 실제 private 함수명의 축약이며 그대로 실행하는 코드가 아닙니다. 승인 전후 최종 인자 일치와 OS/DB 권한도 별도로 확인합니다.',
        ['approval','smart'],code_kind='공식 command guard의 조건 순서를 재구성한 의사코드. 함수명/return shape를 짧게 표시.')
    d=chain([('위험 패턴 감지','명령·reason·pattern key 생성','risk'),('smart / manual','smart는 보조 판단 경로|manual은 사람 검토 경로','runtime'),('사용자 응답','once · session · always · deny|표면·정책에 따라 선택 제한','context')],y=60,h=190)
    d+=group(4,box(0,400,760,170,'smart 판단','APPROVE / DENY / ESCALATE|실패·불확실한 응답은 escalate','model',31)+box(890,400,760,170,'사람이 응답할 수 없을 때','Cron·single-query·unattended 별도 정책|기본 deny · 무한 승인 대기로 남기지 않음','runtime',31))
    put('HHUMAN','어떤 경우에 실제 사용자 승인을 요청할까?','위험 판정·기존 승인·실행 표면을 확인한 뒤 요청합니다.','smart가 모든 요청을 사람에게 묻는 모드인 것은 아닙니다.','Tools와 Skills',d,
        ['위험 감지','모드','사용자 응답','smart와 무인 처리'],
        [('smart','보조 guardian의 approve/deny/escalate 결과를 사용하는 경로가 있습니다.'),('사용자 승인','CLI callback·지원 transport 등에서 허용 범위를 검토하고 요청 결과를 기록합니다.')],
        'approval_smart.py는 보조 LLM verdict를 approve/deny/escalate로 정규화하고 실패·빈 응답·불확실한 값은 escalate합니다. 실제 human decision은 mode·surface·기존 승인·정책에 따라 보조 판단과 사용자 UI를 연결하므로 smart=항상 사람 질문도, smart=무조건 안전 승인도 아닙니다.\n\n사용자 선택은 once/session/always/deny 등이며 도구·표면·설정에 따라 영구/세션 승인이 제한될 수 있습니다. DEFAULT_CONFIG의 approvals.mode는 smart, cron_mode/single_query_mode/unattended_mode는 deny입니다. off·allowlist 등 앞선 승인 조건과 위험 패턴 검사를 먼저 거칩니다. 실제 사용자 응답이 불가능한 문맥은 해당 policy로 정리합니다. Memory/Skill write_approval은 이 명령 승인과 별도 Gate입니다.',
        ['approval','smart','defaults','write'])
    s=put('HFAIL','오류·취소가 실제 작업에 남기는 것','모델 요청 실패와 이미 실행한 Tool의 효과를 구분합니다.','기록 실패·중단·외부 효과 미상을 같은 성공 상태로 합치지 않습니다.','Tools와 Skills',old['S13B']['diagram'],old['S13B']['steps'][1:],
        [('실행 전 실패','Tool-call 정본 저장 실패는 해당 실행 시작을 막습니다.'),('실행 후 실패','외부 작업 뒤 결과 저장 실패는 효과가 남은 미상 상태가 될 수 있습니다.')],
        old['S13B']['explanation']+'\n\n이 장은 실제 Tool round와 command policy, interrupt/timeout의 서로 다른 상태를 연결합니다. Checkpoint는 opt-in 파일 복구 범위이며 외부 API·DB 전체 rollback이 아닙니다.',
        ['persist','approval','final'])

    # Skills: reading, authoring decision, mutation gate, deterministic and LLM maintenance.
    slides['S12'].update(title='Skills를 찾고 읽는 Hermes의 경로',sub='목록·본문·참고 자료와 명시·자동 로딩을 구분합니다.',take='Skill은 실행 함수가 아니라 도구 사용 절차를 담은 재사용 문서입니다.',section='Hermes / Tools와 Skills')
    slides['S12']['diagram']=chain([('skills_list','이름·description·category','context'),('skill_view(name)','SKILL.md + linked_files','context'),('skill_view + file_path','references · scripts · templates','tool')],y=70,h=180)+text(0,430,'명시 /skill-name · auto_load · 모델 선택 · Cron 첨부',31,'runtime',700)+text(0,510,'모든 설치 Skill이 매번 본문 전체로 들어가는 것은 아닙니다.',28,'muted')
    slides['S12']['steps']=['전체 구성','목록','본문','지원 자료']
    slides['S12']['sources'].append(('R-native',evidence['native']['path'],evidence['native']['url']))
    slides['S12']['researchKeys']=['native','skillsdoc','prompt']
    d=chain([('학습할 경험 발생','새 절차 · 반복 시행착오|사용자 수정·피드백','context'),('모델이 재사용 판단','System guidance · 사용자 /learn|주기적 nudge·review 유도','model'),('skill_manage 요청','실제 파일 변경 Tool 호출|지시만으로 자동 저장되는 것은 아님','tool')],y=85,h=210)
    d+=group(4,box(0,445,1650,145,'판단과 검증은 다른 단계','성공했다는 이유만으로 검증된 공식 절차가 되는 것은 아님 · 다음 장에서 쓰기 경로 확인','risk',31))
    put('HLEARN','Hermes는 언제 새 Skill을 만들까?','지침이 기록을 유도하고 모델이 실제 Tool Call을 선택합니다.','자기 개선은 재사용 절차의 갱신이며 모델 가중치 학습이 아닙니다.','Tools와 Skills',d,
        ['경험','모델 판단','쓰기 요청','검증과 구분'],
        [('생성 판단','작업 경험·피드백과 System guidance를 보고 모델이 재사용 가치를 판단합니다.'),('nudge / review','실행 중 주기적 안내와 백그라운드 검토가 저장을 유도할 수 있지만 결정적 성공 판정기는 아닙니다.')],
        'System Prompt의 Tool-aware guidance와 Skills 지침은 비사소한 절차·재사용 가능한 해결·사용자 수정 등을 Skill로 남기도록 유도합니다. prepare_iteration에는 skill_manage가 사용 가능할 때 _iters_since_skill을 증가시키는 nudge bookkeeping이 있습니다. 실제 생성은 모델이 skill_manage를 요청해야 일어납니다. 고정된 성공률 기준으로 Runtime이 최적 절차를 자동 증명하는 알고리즘이 아닙니다.\n\n명시적인 /learn도 자료를 읽고 절차를 저술하는 진입점입니다. background review의 모델·입력 budget·주기와 활성 기능에 따라 동작이 달라질 수 있습니다. 새 기록은 다음 로딩에서 영향을 주므로 틀린 절차도 확산될 수 있고 검토와 적용 범위가 필요합니다.',
        ['skillsdoc','prompt','prep'])
    d=code(0,40,1010,550,'skill_manage(\n  operations=[{\n    "action": "create",\n    "name": "alarm-review",\n    "content": "...SKILL.md 본문..."\n  }]\n)\n\nskills:\n  write_approval: false\n  guard_agent_created: false\n  ledger: true',caption='Tool 요청 예시와 v0.22.5 기본 설정은 구분해서 표시',size=24)
    d+=notes([('검증·변경','경로·동작·대상 확인|create / patch / write_file / delete','runtime'),('승인을 켜면','Skill 쓰기는 pending으로 stage|/skills diff → approve/reject','context'),('관리 기록','before/after hash ledger|Curator backup·rollback과 연결','tool')],x=1100,w=550)
    put('HWRITE','skill_manage의 변경은 어떻게 반영될까?','파일 검증·쓰기 승인·보안 검사·변경 이력을 구분합니다.','내용 검사와 사람의 승인, 업무 정확성 검증은 서로 다른 절차입니다.','Tools와 Skills',d,
        ['변경 처리','보류 승인','변경 이력'],
        [('Skill 변경','operations 배열의 action/name/content 또는 old_string/new_string 등으로 SKILL.md와 지원 파일을 변경합니다.'),('기본 정책','v0.22.5 write_approval=false, guard_agent_created=false, ledger=true를 확인했습니다.')],
        '표시 Tool 요청은 모델에게 공개되는 operations 배열 schema를 따른 예이며 함수 SDK 호출이나 실제 생성 기록이 아닙니다. 각 operation은 action별 anyOf/additionalProperties=false로 구분됩니다. patch는 old_string/new_string(부분 치환) 또는 content(본문 전체 교체)를 받습니다. write_file/remove_file은 지원 파일, delete는 단독 operation만 허용합니다. batch 실패는 변경 대상을 rollback하는 원자적 처리이며, 레거시 flat action/name 인자는 기존 이력 재생을 위해 수용하지만 모델에는 공개하지 않습니다. 경로·대상·동작 검증과 쓰기 Gate가 파일 변경을 처리합니다. write_approval=true이면 Skill 본문이 크므로 foreground도 항상 stage해 /skills pending, /skills diff <id>, /skills approve|reject <id>로 검토합니다. Memory foreground inline과 다릅니다.\n\nagent-created Skill 내용 scanner는 guard_agent_created 설정에 의존하며 이 태그 기본 false입니다. Hub 설치 scan과 Agent 작성 scan을 같은 기본값으로 합치지 않습니다. advisory linter도 보증 검사가 아닙니다. ledger는 변경 전후 hash를 기록하지만 감사 기록 실패를 모든 변경의 강제 차단으로 쓰는 것은 아닙니다. scope·SOP 버전·만료·검증은 업무 설계이고 자동 가중치 학습과 무관합니다.',
        ['skill','defaults','write','curator'],code_kind='공식 Tool schema 기반 인자 예시 + 실제 DEFAULT_CONFIG 발췌 항목. 생성 실행하지 않음.')
    d=chain([('실행 여부 확인','enabled=true · interval 168h|idle 2h 이상이 기본 조건','runtime'),('사용 이력 확인','view / use / patch 기록|pin·Cron 참조·대상 범위 확인','context'),('자동 상태 전이','14일 미사용 → stale|30일 미사용 → archive','tool')],y=70,h=210)
    d+=group(4,box(0,440,1650,155,'기본 Curator는 LLM 없는 결정적 정리','Agent 생성 대상 중심 · Hub 설치 제외 · 기본 자동 삭제 없음 · 첫 관찰은 실행 시각 초기화','runtime',31))
    put('HCURATOR','Curator는 언제 무엇을 정리할까?','일정·유휴 조건을 만족하면 사용 이력으로 상태를 바꿉니다.','active → stale → archived는 사용 이력 관리이며 품질 점수 판정이 아닙니다.','Tools와 Skills',d,
        ['발동 조건','관리 대상','상태 전이','기본 동작'],
        [('발동','기본 interval_hours=168, min_idle_hours=2이며 세션 시작·maintenance에서 조건을 확인합니다.'),('자동 정리','기본 stale 14일, archive 30일. pinned/예약 참조 등 보호 대상을 확인합니다.')],
        'v0.22.5 Curator 코드와 고정 문서의 기본값을 확인했습니다. cron job 자체가 아니라 inactivity 조건 점검으로 실행됩니다. 첫 관찰에는 last_run_at을 초기화하고 한 interval 뒤 실제 pass를 미루는 경로가 있습니다. 활성 turn·profile maintenance 주체·CLI/serve 등 표면별 실행 조건은 소스를 확인합니다.\n\n기본 대상은 Agent 생성 Skill이고 Hub 설치는 제외됩니다. pinned 및 Cron 참조 Skill은 자동 전이에서 보호하며 built-in 정리는 prune_builtins opt-in입니다. 미사용 14일 stale, 30일 archive, never-used grace 조건 등을 적용합니다. 자동 archive는 복구 가능한 이동이며 영구 자동 삭제로 설명하지 않습니다. 품질·정답을 검증한 상태값은 아닙니다.',
        ['curator','curatordoc','defaults'])
    d=code(0,45,900,515,'curator:\n  enabled: true\n  interval_hours: 168\n  min_idle_hours: 2\n  stale_after_days: 14\n  archive_after_days: 30\n  consolidate: false\n  prune_builtins: false',caption='v0.22.5 기본 설정',size=26)
    d+=notes([('선택적 LLM 검토','consolidate=true 또는 수동 실행|별도 AIAgent가 겹침·drift 검토','model'),('허용된 변경','keep · patch · 통합 · archive|지원 파일과 참조 관계도 유지','tool'),('직접 점검','hermes curator status|hermes curator run --dry-run','context')],x=1010,w=640)
    put('HCONSOLIDATE','Curator의 LLM 통합은 별도 선택입니다','기본 정리와 비용이 드는 절차 통합을 나누어 봅니다.','Skill을 합칠 때 본문뿐 아니라 references·scripts·템플릿도 함께 관리합니다.','Tools와 Skills',d,
        ['선택적 검토','변경 범위','수동 확인'],
        [('consolidate','기본 false. 활성화하면 보조 Agent가 겹침을 검토해 통합·수정을 제안/적용하는 경로입니다.'),('점검','status와 dry-run으로 상태·예상 결과를 확인할 수 있습니다.')],
        '고정 문서에서 기본 deterministic prune과 opt-in LLM consolidation을 구분합니다. LLM pass는 독립 prompt cache의 fork이며 현재 대화에 직접 문맥을 섞는 단계가 아닙니다. 지원 파일을 포함한 Skill package를 유지/이관하고 상대 참조를 고쳐야 하며 SKILL.md만 납작하게 복사하는 것으로 통합을 설명하지 않습니다.\n\n보조 모델 비용과 광범위 변경 때문에 consolidate 기본 false입니다. hermes curator run --dry-run은 변경 없는 점검, --consolidate는 수동 통합 선택입니다. ledger/backup/rollback은 실제 태그의 명령·제약을 확인해야 하며 pin이 모든 수정을 막는 lock과 동일하지 않습니다. 실제 실행 결과나 개선 성능을 측정한 것은 아닙니다.',
        ['curator','curatordoc','defaults'])

    from hermes_observability import extend
    extend(slides,env,put,code,notes,chain,divider)

    divider('HLONG','긴 작업과 위임','입력의 크기와 실행 단위를 확장합니다.',['System Prompt·압축','병렬 Tool','Subagent·다중 모델'])
    slides['S08'].update(title='System Prompt를 고정해 Prefix를 재사용하기',sub='같은 System Prompt와 이력의 앞부분을 다시 사용할 수 있습니다.',take='Hermes는 입력을 구성하고, 캐시 적중은 추론 서비스가 판단합니다.',section='Hermes / 긴 작업과 위임')
    slides['S08']['diagram']=slides['S08']['diagram'].replace('동일한 앞부분 · 8,000 tokens','동일 System Prompt + 이력 · 8,000').replace('입력 순서·내용 구성','System Prompt · 이력 구성')
    slides['S08']['sources'].append(('R-prompt',evidence['prompt']['path'],evidence['prompt']['url']))
    slides['S08']['researchKeys']=['prompt']
    d=''
    examples=[('압축 전','user: LOT-A의 이상값 확인|tool: 센서 원문 5,000행 ...|assistant: 기준선 검토 ...|최근 call_7 ↔ result_7','muted'),('큰 결과 축소','user: LOT-A의 이상값 확인|tool: [큰 과거 본문 축소]|assistant: 기준선 검토 ...|최근 call_7 ↔ result_7','context'),('요약 + 보호 구간','summary: LOT-A · UTC · SOP r3|원본: artifact://lot-a|최근 call_7 ↔ result_7|최신 사용자 요청 유지','tool')]
    for i,(a,b,c) in enumerate(examples):
        x=i*585;d+=group(i+1,box(x,70,480,325,a,b,c,31))
        if i<2:d+=group(i+1,arrow(f'M{x+480} 230 H{x+573}',c))
    d+=group(4,box(0,490,1650,130,'이 예시에서 보호할 정보','정확한 단위·대상·SOP 버전·원본 위치와 아직 사용하지 않은 최근 Tool 결과','runtime',31))
    put('S09','예시 Context가 압축되는 과정','큰 과거 결과를 줄이고, 요약과 최근 문맥을 합칩니다.','실제 문자열·행 수를 재현한 로그가 아닌 압축 원리의 예시입니다.','긴 작업과 위임',d,
        ['압축 전','Tool 본문 축소','요약과 합성','보호할 정보'],
        [('Prune','보호되지 않는 오래되고 큰 Tool 결과를 줄이는 처리입니다.'),('Summary + Tail','중간 이력 요약과 최근 메시지·호출/결과 쌍을 합쳐 요청을 구성합니다.')],
        '표시의 5,000행, call_7, LOT-A, artifact URI와 요약 문장은 설명용 가상 Context이며 실제 compressor 출력이나 실행 Trace가 아닙니다. 실제 기능은 필요 판단→오래된 큰 Tool 결과 prune→최근/미사용 결과·호출 쌍 보호→중간 이력 요약→합성·프로토콜 정합성 보정입니다.\n\n원문 계산 조건은 별도 artifact로 보존하고 Context에는 식별자·단위·리비전·요약을 두는 업무 설계를 보여줍니다. 압축은 내용 손실과 캐시 Prefix 변경을 수반할 수 있습니다. timeout/감소 실패·재로딩 마커·session lineage를 처리하는 경로와 압축 후 system snapshot 재빌드 경계도 존재합니다. 모든 임계값을 고정 50%/85%라고 단정하지 않습니다.',
        ['prompt','loop'],code_kind='가상 Context의 Before/Prune/Summary 예시. 실측·완전한 compressor 출력이 아님.')
    d=code(0,45,1050,540,'# _ConcurrentBatch.submit_all 실제 호출 형태\nf = executor.submit(\n    propagate_context_to_thread(self.run_worker),\n    i, submit_index\n)\n\n# 원본은 한 줄, 화면에서 줄바꿈 조정\n# self.results[index] = outcome\n# 결과 slot은 원래 호출 index를 유지',caption='agent/tool_executor.py · 공식 코드 발췌/줄바꿈 조정',size=22)
    d+=notes([('구간 계획','_plan_tool_batch_segments|경로 충돌·interactive barrier','runtime'),('Worker 실행','DaemonThreadPoolExecutor|Context·승인 callback 전달','tool'),('결과 정리','self.results[index]에 보관|완료 순서와 호출 순서를 분리','context')],x=1120,w=530)
    put('S14','Hermes의 병렬 Tool 실행 코드','계획한 구간 안에서 실제 worker를 스케줄링합니다.','thread 여러 개와 독립 Agent 여러 개는 다른 실행 방식입니다.','긴 작업과 위임',d,
        ['구간 계획','Worker','결과 순서'],
        [('Segment planner','read-only·대화형·파일 경로 충돌과 effect 가능성을 보고 구간을 나눕니다.'),('Concurrent batch','Context를 전파해 Worker를 제출하고 원래 index의 결과 slot을 채웁니다.')],
        'executor.submit(propagate_context_to_thread(self.run_worker), i, submit_index)는 v0.22.5의 실제 호출이며 화면은 줄바꿈만 조정했습니다. run_worker는 middleware·권한·시작 순서 gate를 사용하고 outcome을 self.results[index]에 저장합니다. deadline·interrupt 시 미상 효과와 abandoned 결과를 처리할 수 있습니다.\n\n모델이 호출을 여러 개 제안했다고 전부 즉시 병렬 수행하지 않습니다. _plan_tool_batch_segments는 Reader·write 경로 중첩·대화형 도구 등을 고려하고 unknown/Plugin/MCP는 기본 effect-capable로 보수적으로 다루는 경로가 있습니다. thread pool은 CPU 병렬 성능 보증이 아니며 외부 I/O·GIL·락에 좌우됩니다. 결과 call_id 정합성과 데이터 snapshot 검증은 별개입니다.',
        ['parallel','planner'],code_kind='executor.submit 실제 호출 발췌(줄바꿈 조정). 주석의 결과 대입은 인접 run_worker 소스의 실제 코드이다.')
    d=code(0,45,1030,540,'delegate_task(\n  tasks=[\n    {"goal": "측정값 검토",\n     "context": "합성 LOT-A / UTC / 기준 v3"},\n    {"goal": "SOP 근거 검토",\n     "context": "승인 문서 r3만 확인"}\n  ]\n)\n# 모델의 Tool 요청 예시',caption='실제 delegate_task schema를 따른 예시 · 실행 기록 아님',size=23)
    d+=notes([('인자 정규화','goal 또는 tasks를 작업 목록으로|할당량·권한·동시성 확인','runtime'),('자식 구성','독립 AIAgent·Messages·Task|부모 기반 Toolset·모델 설정','context'),('Parent 범위','goal/context로 필요한 근거 전달|부모 History 전체 자동 상속 아님','tool')])
    put('S14A','delegate_task는 자식을 어떻게 만들까?','작업 요청을 정규화하고 Child AIAgent를 구성합니다.','자식이 알아야 할 데이터·버전·작업 범위를 context에 명시합니다.','긴 작업과 위임',d,
        ['작업 목록','자식 설정','전달 범위'],
        [('Child 설정','부모 설정을 바탕으로 모델·허용 Toolset·별도 반복 예산과 Task를 구성합니다.'),('Context 격리','자식 메시지는 별도이며 goal/context와 허용된 프로젝트 지침 등을 전달합니다.')],
        '화면은 실제 Tool schema 기반의 가상 tasks 요청입니다. delegate_tool.py와 delegate_tool_child_run.py는 입력 정규화·할당량·도구 제한·자식 AIAgent 생성과 등록을 나누어 처리합니다. 자식은 새 대화를 가지며 부모의 과거 Tool 결과를 자동으로 전부 이해한다고 가정하지 않습니다. workspace 프로젝트 지침 등 명시적 로더 예외는 존재합니다.\n\n고정 DEFAULT_CONFIG의 자식 max_iterations 기본은 250이며 부모 상한과 별개입니다. MCP 상속·toolset 제한·worktree/credential 등은 설정과 Backend 조건을 확인해야 합니다. 파일·DB·secret 권한 격리는 Context 분리와 다르며 Task 분리만으로 운영 격리가 보장되지는 않습니다.',
        ['delegate','child','dispatch','defaults'],code_kind='공식 Tool schema에 맞춘 설명용 인자. 실제 호출 Trace 또는 공개 Python SDK 예제가 아님.')
    d=chain([('_run_batch','동기 / background 경로 선택','runtime'),('_run_children_parallel','Child 실행과 진행·중단 추적','tool'),('결과 전달','summary · status · schema 검사|Parent가 다음 판단 수행','context')],y=65,h=190)
    d+=group(4,box(0,420,760,165,'최상위 background 경로','즉시 handle / delegation_id 반환|완료 결과는 별도 전달로 도착','runtime',30)+box(890,420,760,165,'output_schema를 지정하면','JSON Schema 확인 → 1회 수정 기회|실패해도 미검증 표시와 원문 결과 유지','context',30))
    put('HCHILD','자식 실행과 결과 전달의 세부 경로','대기형 반환과 background handle을 구분합니다.','Child 완료와 결과의 구조·업무 정확성 통과는 별개입니다.','긴 작업과 위임',d,
        ['배치 경로','자식 실행','결과 통합','반환 형태'],
        [('실행','_run_batch와 _run_children_parallel 등이 자식 실행·상태·중단·정리를 관리합니다.'),('Background','최상위 요청은 handle을 먼저 반환하는 경로가 있으며 결과 전달은 실행 완료와 별도입니다.')],
        '확인한 고정 소스에서 _run_batch는 동기/백그라운드 실행 경로를 나누고 background 응답에는 dispatched 상태·delegation_id·자식 식별자 등이 담길 수 있습니다. orchestrator 자식이 worker를 기다리는 경로와 최상위 사용자 대화의 background 전달을 동일한 동기 반환 그림으로 합치지 않습니다.\n\noutput_schema 검증 실패 시 제한된 수정 turn을 주고 최종 실패는 원문 summary를 버리지 않고 schema_valid=false와 오류를 표시하는 경로입니다. 실제 필드는 버전·경로에 따라 확인합니다. 자식 background 프로세스의 수명도 자식 정리에 연결될 수 있어 서버를 띄우고 ID만 반환하면 부모 소유가 된다는 가정은 피합니다. 비용·partial·중단·전달 실패를 함께 관찰합니다.',
        ['dispatch','child','delegate'])
    d=chain([('delegate_task','하위 목표마다 별도 Loop|Task·도구·예산을 나눠 실행','runtime'),('Mixture of Agents','Provider의 reference + aggregator|acting model이 Tool Loop 수행','model'),('Kanban','Board·Task·Profile·Worker로 조정|지속 작업 상태와 협업','context')],y=85,h=225,connect=False)
    d+=group(4,box(0,455,1650,140,'선택 기준은 분리하려는 단위','독립 하위 작업 / 여러 모델의 관점 / 지속 작업 보드 · 서로 다른 구조와 수명','runtime',31))
    put('HMULTI','Hermes는 delegate_task만 사용할까?','공식 소스·문서에는 목적이 다른 다중 실행 방식이 있습니다.','작업 위임과 다중 모델 합성, 보드 기반 협업을 구분합니다.','긴 작업과 위임',d,
        ['Task 위임','모델 합성','보드 협업','선택 기준'],
        [('Delegation','목표를 쪼개 독립 Agent가 실행하고 부모가 결과를 사용하는 방식입니다.'),('MoA','여러 reference 모델 분석을 aggregator가 사용하며 acting model의 정상 Agent Loop를 유지합니다.'),('Kanban','Task/board와 profile worker를 활용하는 지속 작업 조정 기능입니다.')],
        'delegate_task만이 유일한 멀티에이전트 방식이라고 결론내릴 수 없습니다. 고정 태그의 Mixture of Agents는 moa 가상 Provider의 reference/aggregator 모델 구성이며, aggregator가 실제 응답·Tool Call을 내는 acting model입니다. 각 reference가 모두 별도의 업무 Tool Loop를 맡는 Subagent와 다릅니다. Kanban은 Board·Task·Profile·worker의 지속 작업 상태를 조정하는 다른 수준의 기능입니다.\n\ndelegate_task는 한 대화에서 하위 목표를 독립 Context·Toolset·예산으로 맡기고 반환받는 데 적합한 설계입니다. MoA는 여러 모델의 관점 합성, Kanban은 지속 작업 조정에 쓰는 선택지입니다. 이 비교는 확인한 대표 방식이며 Hermes의 모든 orchestration 확장을 전수 열거했다는 뜻은 아닙니다. 추가 기능의 배포/복구 구조는 이번 발표 범위에서 상세 설명하지 않습니다.',
        ['delegate','dispatch','moa','kanban'])

    divider('HCRON','예약 실행과 활용','반복 작업을 예약하고 실행 상태를 직접 다룹니다.',['Cron 구조','생성·관리 명령','Session·Skill 활용'])
    slides['S14C'].pop('chapter',None);slides['S14C']['section']='Hermes / 예약 실행과 활용';slides['S14C']['researchKeys']=['cron']
    slides['S14C']['sources'].append(('R-cron',evidence['cron']['path'],evidence['cron']['url']))
    d=code(0,40,1080,545,'# 대화 안의 slash command\n/cron add "every 2h" "합성 로그 요약"\n\n# 독립 CLI\nhermes cron create "every 2h" "합성 로그 요약"\nhermes cron list\n\n# 자연어로도 예약 요청 가능\n# 내부 Tool: cronjob_manage',caption='공식 문법을 따른 예시 · 실제 예약을 생성하지 않음',size=23)
    d+=notes([('생성','schedule + prompt|Skill·실행 환경·전달 대상 확인','runtime'),('관리','list · pause · resume · run|update · remove 등','context'),('실행 시','설정 검증 → 새 Session|첨부 Skill·prompt → Loop','tool')],x=1140,w=510)
    put('HCRONUSE','Cron 작업을 만들고 관리하기','자연어·slash command·독립 CLI가 같은 예약 기능으로 이어집니다.','schedule 표현과 prompt, 권한·전달 대상을 함께 확인합니다.','예약 실행과 활용',d,
        ['생성','관리','실행 구성'],
        [('예약 명령','/cron add와 hermes cron create는 서로 다른 입력 표면입니다.'),('cronjob_manage','모델이 create/list/update/pause/resume/run/remove 등의 action으로 관리하는 Tool입니다.')],
        '표시 예시는 공식 /cron add "every 2h" "..."와 standalone CLI의 positional schedule/prompt 문법을 따릅니다. 실제 예약을 생성한 것은 아닙니다. 5필드 cron·상대 지연·반복 간격·ISO 시각 등 지원 표현과 시간대를 확인합니다.\n\n자연어 요청도 내부적으로 cronjob_manage로 이어질 수 있습니다. 고정 문서의 일부 예제에는 cronjob이라는 옛 표기가 남아 있어 함수 이름을 그대로 복사하지 않고 현재 Tool 이름과 CLI 문법을 구분했습니다. 첨부 Skills, 실행 경로, 모델 선택·인증·무인 승인·전달 조건은 실제 환경에 맞게 검증해야 합니다. 생성/일시중지/재개/수동실행/삭제는 별도 동작입니다.',
        ['cron','slash'],code_kind='공식 command 문법 기반 예시. 실제 예약 생성/실행은 하지 않았다.')
    d=group(1,box(0,65,760,340,'장점','시간·주기 기반 작업 시작|Prompt + Skill로 절차 재사용|Fresh Session으로 이력 누적 완화|결과 저장·전달을 작업과 연결','tool',35))
    d+=group(2,box(890,65,760,340,'주의할 점','무인 승인·인증 만료·모델 비용|실행 성공과 전달 성공의 차이|외부 작업 중복 효과 별도 통제|중단 후 재실행·결과 확인 필요','risk',35))
    d+=group(3,text(0,540,'Agent 모드: LLM·Tools 실행 / no-agent 모드: Script 결과 전달',30,'context',700)+text(0,605,'Script의 실행 권한과 LLM Tool 승인 정책을 자동으로 동일시하지 않습니다.',26,'muted'))
    put('HCRONTRADE','Cron은 언제 유용하고 무엇을 주의할까?','정기 점검·요약·알림에 맞는 기능과 운영 비용을 함께 봅니다.','예약 회차 Claim이 외부 작업과 전달까지 exactly-once로 만들지는 않습니다.','예약 실행과 활용',d,
        ['장점','주의점','두 실행 모드'],
        [('적합한 활용','주기적 조회·점검·요약처럼 시간 조건이 명확하고 결과를 검토할 수 있는 작업입니다.'),('모드와 권한','Agent 모드와 no-agent Script 모드를 구분하고 외부 효과·무인 정책을 별도로 확인합니다.')],
        'Hermes Cron의 강점은 일정 표현, reusable Skill, fresh Agent session, 저장·전달이 제품 기능으로 연결된다는 점입니다. 반면 모델 호출비, 인증과 실패 알림, 재시도·중복 부작용·결과 누락을 운영해야 합니다. 새 Session도 지속 Memory/Skills를 읽을 수 있어 완전 stateless하지 않습니다.\n\n회차 Lock/Claim/receipt와 외부 대상 시스템의 멱등성, Delivery 보장은 다른 문제입니다. no-agent는 Script 실행과 stdout 전달 경로이며 비용·권한·오류 형태가 Agent 모드와 다릅니다. 사용자 코드의 권한과 Tool approval을 혼동하지 않습니다. 이벤트 기반·장기 복구 요구는 다른 trigger/workflow 설계와 비교할 사안입니다.',
        ['cron'])
    d=chain([('/new','새 세션 · 새 snapshot|작업/주제가 바뀔 때','context'),('/learn …','경험·자료를 Skill로 정리|생성 내용은 검토 후 재사용','tool'),('/skills diff <id>','보류된 변경을 확인|write_approval=true일 때 검토','runtime')],y=90,h=220,connect=False)
    d+=group(4,box(0,460,1650,135,'명령 뒤의 구조를 함께 보기','세션 경계 / 절차 파일 작성 / pending 검토 · 서로 다른 상태를 바꾸는 입구','context',31))
    put('HCOMMAND','구조를 알고 쓰면 유용한 Hermes 명령','세션 경계와 Skill 관리가 실제 사용 습관으로 이어집니다.','명령의 이름보다 무엇이 바뀌고 언제 반영되는지를 확인합니다.','예약 실행과 활용',d,
        ['세션 새로 시작','Skill 학습','변경 검토','상태 변화'],
        [('/new','새 Session ID·History로 작업 경계를 만들고 Memory snapshot을 다시 읽는 계기입니다.'),('/learn','자료·경험을 바탕으로 Skill을 저술하는 진입점이며 지식 검증을 자동 보장하지 않습니다.')],
        '새 작업·주제 전환에서 /new로 세션 경계를 만들면 지속 Memory를 다시 읽고 필요 시 과거 세션을 검색하는 사용 흐름을 설명하기 쉽습니다. /learn은 문서나 경험을 재사용 Skill로 만들도록 요청하는 기능이며 생성 절차·지원 파일을 검토해야 합니다.\n\n/skills diff <id>는 write_approval을 켜 보류된 변경이 있을 때 검토하는 명령이며 기본 false 환경에서 모든 쓰기가 반드시 pending이라고 설명하지 않습니다. /memory pending/approve/reject와 /skills pending/approve/reject도 관리하는 subsystem이 다릅니다. 설치된 Skill의 /skill-name은 built-in 명령과 충돌 시 fallback을 확인해야 합니다.',
        ['slash','skillsdoc','write','memory'])
    slides['S15'].pop('chapter',None);slides['S15']['section']='Hermes / Demo'
    slides.pop('S14B',None)  # Explicit user exclusion: no Gateway architecture slide.

    # Topic dividers before Claude Code and PydanticAI. Claude is typography-only.
    def topic(ident,name,sub,items,base,logo=None):
        d=text(0,185,name,90 if len(name)<13 else 77,'text',700)+text(5,270,sub,32,'muted')+rule(5,345,1650,345)
        if logo:d+=image(logo,1130,55,480,170)
        for i,item in enumerate(items):d+=text(5+i*550,455,item,31,'context',700)
        s=deepcopy(old[base]);s.update(id=ident,title=name,sub=sub,take='',diagram=d,kind='topic-divider',steps=['전체 구성'],demo=None,originalSpec='',
            concepts=[{'term':name,'meaning':sub}],explanation=name+'의 설명을 시작합니다. '+' → '.join(items)+' 순서로 실제 실행의 입력·처리·결과를 연결합니다. 각 기능은 실행환경이 제공하는 동작과 개발자가 구성하는 부분을 나누어 살펴봅니다.',note='## '+name+'\n\n'+sub,
            section=name,version='Topic',editorialBasis='explicit topic divider')
        s.pop('chapter',None);slides[ident]=s
    topic('CLAUDE','Claude Code','코딩 작업을 위한 Agent Harness',['실행 구조','지침과 기억','위임과 활용'],'S16')
    topic('PYDANTIC','PydanticAI','코드로 구성하는 Agent 실행과 검증',['Agent 정의','내부 실행 Graph','업무 검증과 확장'],'S20','pydanticai-official.svg')

    d=chain([('/context → /compact','사용 중인 Context를 확인|긴 대화의 축약을 직접 관리','context'),('/permissions','허용·승인 규칙을 확인|도구 실행 통제와 연결','runtime'),('/rewind','지원 Checkpoint로 복원|코드·대화 복원 범위를 선택','tool')],y=90,h=225,connect=False)
    d+=text(0,505,'긴 작업: Context 확인 / 실행 전: 권한 확인 / 수정 후: Diff·Checkpoint 확인',29,'text',700)
    s=deepcopy(old['S19']);s.update(title='Claude Code의 구조와 연결되는 활용 명령',sub='Context·도구 권한·작업 복구를 직접 관리합니다.',take='Checkpoint 복구 범위는 Shell·외부 서비스의 모든 부작용을 포함하지 않습니다.',diagram=d,
        steps=['전체 구성','Context','권한','복구'],section='Claude Code / 활용',
        concepts=[{'term':'/context · /compact','meaning':'Context 사용 상태를 확인하고 긴 대화를 축약합니다.'},{'term':'/permissions','meaning':'Tool의 허용·승인 규칙을 확인합니다.'},{'term':'/rewind','meaning':'Checkpoint의 코드·대화 복원/요약 옵션을 사용합니다.'}],
        explanation='공식 Claude Code Commands·Checkpointing 문서를 확인했습니다. /context로 입력 사용을 확인하고 /compact로 긴 대화를 축약합니다. /permissions는 실행 허용·승인 규칙을 다루며 지침 파일과 다른 통제입니다. /rewind는 지원하는 파일 편집과 대화의 Checkpoint 복원·요약을 선택하는 기능입니다.\n\nShell 명령으로 만든 파일 변경이나 외부 시스템의 효과를 전부 되돌리는 기능으로 설명하지 않습니다. /diff로 변경을 검토하고 /resume으로 세션을 잇는 활용도 있습니다. 이 명령은 공개 계약 기준이며 비공개 엔진 구현을 분석했다는 뜻은 아닙니다.',
        sources=[('CC-CMD','Claude Code Commands','https://code.claude.com/docs/en/commands'),('CC-CHK','Claude Code Checkpointing','https://code.claude.com/docs/en/checkpointing')],version='Claude Code · 공식 공개 문서')
    s['note']='## '+s['title']+'\n\n'+s['explanation'];slides['S19']=s

    slides['S12']['concepts']=[{'term':'skills_list','meaning':'이름·설명 목록으로 후보를 찾습니다.'},{'term':'skill_view','meaning':'SKILL.md를 읽고 linked_files에서 필요한 지원 파일을 추가로 읽습니다.'}]
    slides['S12']['explanation']='skills_list는 설치 Skill의 이름·설명·category를 보여주고, skill_view(name)는 본문과 linked_files를 반환합니다. 필요한 경우 file_path로 references/templates/scripts를 추가로 읽습니다. 목록 노출과 전체 본문 로딩은 다릅니다.\n\n명시 slash invocation, skills.auto_load, 모델의 Tool 호출, Cron 첨부라는 로딩 입구가 있습니다. auto_load는 pinned system 영역에 들어갈 수 있고 일반 인덱스와 동적 로딩은 다른 경로입니다. 내용 작성과 승인·Curator 관리는 다음 장들에서 따로 설명합니다.'
    for ident in ('S12','S08','S14C'):
        s=slides[ident]
        for k in s.get('researchKeys',[]):
            if not any(r[0]=='R-'+k for r in s['sources']):s['sources'].append(('R-'+k,evidence[k]['path'],evidence[k]['url']))
        s['note']='## '+s['title']+'\n\n'+s['sub']+'\n\n'+s['explanation']+'\n\n'+s['take']

    # Preserve old blueprint specs only as authoring evidence, not audience content.
    slides['S05']['originalSpec']=old['S05']['originalSpec']
    return ORDER
