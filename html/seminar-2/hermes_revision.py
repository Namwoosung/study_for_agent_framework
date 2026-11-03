"""Hermes: agreed 16-slide teaching sequence, grounded in the local study sources."""
from copy import deepcopy

HERMES_ORDER=['S04','S05','S07','S13','S13A','S13B','S10','S11','S12','S08','S09','S14','S14A','S14B','S14C','S15']
CHAPTERS=['요청 처리','Tool 실행','기억·재사용','긴 작업·위임','서비스 운영','Demo']

def revise(slides, env):
    text,box,arrow,group,rule=(env[n] for n in ('text','box','arrow','group','rule'))
    references=env['references']
    project=env['PROJECT']
    old=deepcopy(slides)
    deep=project/'hermes/Hermes_Agent_2차_심층_학습_분석.md'
    study=project/'hermes/Hermes_Agent.md'
    comments=project/'hermes/Hermes_Agent_발표_실무_시사점_코멘트.md'

    extra={
      'HX01':('Tool round · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/turn_tool_round.py'),
      'HX02':('Tool validation · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/turn_tool_validation.py'),
      'HX03':('Approval · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/approval.py'),
      'HX04':('Gateway / API integration','https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration'),
      'HX05':('Gateway inbound · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/gateway/run_inbound.py'),
      'HX06':('Cron internals','https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals'),
      'HX07':('Cron scheduler · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/cron/scheduler.py'),
      'HX08':('Tool executor · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/tool_executor.py'),
      'HX09':('Memory store · v0.22.5','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/memory_tool_store.py'),
    }

    def put(ident,title,sub,take,chapter,diagram,steps,terms,explanation,refs,sections,base=None,evidence='고정 소스·공식 문서 기준',talk=None):
        base=base or ident
        s=deepcopy(old[base])
        sources=list(s['sources']) if ident==base else []
        for k in refs:
            if k not in {r[0] for r in sources}:sources.append((k,*(extra[k] if k in extra else references[k])))
        s.update(id=ident,title=title,sub=sub,take=take,diagram=diagram,section='Hermes / '+CHAPTERS[chapter],
                 chapter=chapter,steps=['전체 구성']+steps,kind='content-slide',demo='hermes' if ident=='S15' else None,
                 concepts=[{'term':a,'meaning':b} for a,b in terms],explanation=explanation,sources=sources,
                 version='Hermes · '+evidence,
                 localEvidence=[{'path':str(deep.relative_to(project)).replace('\\','/'),'sections':sections}],
                 editorialBasis='합의한 Hermes 16장 구성 / hermes_revision.py')
        if ident!=base:s['originalSpec']=''
        s['note']='## '+title+'\n\n### 개념\n\n'+'\n\n'.join('**'+a+'**: '+b for a,b in terms)+'\n\n### 설명\n\n'+explanation+'\n\n### 발표 포인트\n\n'+take
        if talk:s['note']+='\n\n### 설명 순서\n\n'+talk
        s['note']+='\n\n### 학습자료 근거\n\n심층 학습 '+sections+'; 기초 학습자료 및 추가 코멘트와 대조. 구현 설명·문서 설명·업무 설계 제안을 구분한다.'
        slides[ident]=s
        return s

    def chain(items,y=80,w=480,gap=105,h=140,step=1):
        d=''
        for i,(name,desc,col) in enumerate(items):
            x=i*(w+gap);d+=group(step+i,box(x,y,w,h,name,desc,col))
            if i<len(items)-1:d+=group(step+i,arrow(f'M{x+w} {y+h/2} H{x+w+gap-12}',col))
        return d

    # 6. Existing feature overview, now the first anchor of the detailed module.
    s=slides['S04'];s['chapter']=0;s['section']='Hermes / 요청 처리'
    s['localEvidence']=[{'path':'hermes/Hermes_Agent.md','sections':'§1.3·2·4'}]
    s['editorialBasis']='합의한 Hermes 16장 구성 / hermes_revision.py'

    # 7. A complete turn, before zooming into its individual components.
    d=chain([('사용자 입력','Task와 세션 준비','runtime'),('Context 준비','지침 · 이력 · Tool schema','context'),('모델 호출','Provider Adapter를 거쳐 요청','model')],y=40,h=135)
    d+=group(4,box(1170,345,480,150,'Tool 요청','검증 · 실행 · 결과 추가','tool')+arrow('M1410 175 V333','tool')+arrow('M1170 420 H1080 V245 H825 V187','context',label='결과를 넣어 다시 호출',lx=400,ly=300))
    d+=group(5,box(0,345,760,150,'최종 답변','응답 · 세션 정리 후 종료','success')+arrow('M1410 175 V255 H380 V333','success',label='답변 완료',lx=410,ly=237))
    d+=group(6,text(0,600,'중단 · 예산 소진 · 오류',30,'risk',700)+text(480,600,'각 종료 원인에 맞춰 기록과 응답을 정리',27,'muted'))
    s=put('S05','사용자 요청 한 건의 실행 과정','한 Turn 안에서 모델 호출과 Tool 실행이 반복됩니다.','사용자 요청 수와 모델 호출 수는 다릅니다.',0,d,
        ['입력과 Task','Context 준비','모델 요청','Tool 반복','답변과 저장','다른 종료 원인'],
        [('Turn','사용자 입력 한 건을 처리하는 실행 단위입니다. 여러 모델·Tool 호출을 포함할 수 있습니다.'),('Agent Loop','모델 응답을 분류하고 Tool 실행, 다음 호출, 종료를 결정합니다.'),('Provider Adapter','내부 메시지·도구 정의를 선택한 API의 요청 형식으로 바꿉니다.')],
        '입력과 Task를 준비한 뒤 지침·대화 이력·Tool schema를 모아 모델을 호출합니다. Tool Call이 있으면 Runtime이 검증과 실행을 거쳐 결과를 이력에 추가하고 다음 모델 호출로 이어갑니다. 최종 답변이면 Turn을 정리하고 세션을 저장합니다.\n\n사용자 중단, 실행 예산, API 오류, 잘못된 응답 등은 각각 다른 분기입니다. Tool 결과를 보고 다음 행동을 고르는 정상 반복과 통신 retry를 구분합니다. 압축용 보조 호출이나 자식 Agent 호출도 사용자 요청 수와 별도로 세어야 합니다. 모델의 최종 답변이 업무의 정확성을 보장하지는 않습니다.',
        ['H01','H02'], '§3·4',talk='전체 흐름을 먼저 한 번 따라간다. 이후 장표는 이 흐름의 Context, Tool, 저장, 확장 부분을 차례로 확대한다.')
    s['originalSpec']+='\n\n'+old['S06']['originalSpec']
    for r in old['S06']['sources']:
        if r[0] not in {v[0] for v in s['sources']}:s['sources'].append(r)
    del slides['S06']

    # 8. Prompt composition keeps the accepted snapshot diagram.
    put('S07','모델에 전달할 Context 구성하기','세션의 지침에 대화 이력과 호출 시점 정보를 더합니다.','항상 필요한 지침과 필요할 때 읽는 정보를 나누어 구성합니다.',0,old['S07']['diagram'],
        old['S07']['steps'][1:],
        [('System snapshot','세션 안에서 재사용하는 정체성·프로젝트 지침·Memory 등 기준 정보입니다.'),('History와 호출별 정보','대화·Tool 결과와 현재 실행 상태처럼 다음 모델 요청에 더하는 정보입니다.'),('Provider Adapter','구성한 정보를 실제 모델 API의 messages와 tools 형식으로 변환합니다.')],
        'SOUL은 Agent의 정체성과 기본 행동을, AGENTS 계열 파일은 프로젝트 지침을 제공합니다. 논리적 Stable/Context/Volatile 계층을 세션 snapshot과 함께 이해해야 하며, Volatile이라는 이름이 매 호출 재작성을 뜻하지는 않습니다.\n\nMemory 파일을 매번 통째로 다시 읽거나 설치된 모든 Skill 본문을 항상 넣는 구조로 설명하지 않습니다. 짧은 지속 사실, 대화 이력, 필요 시 읽는 절차와 검색 결과가 각 경로를 통해 Context에 들어옵니다. 실제 최종 요청은 Provider Adapter 뒤에서 확인합니다. 현행 문서의 Skill 계층 위치에는 불일치가 있어 특정 층으로 단정하지 않습니다.',
        ['H03','H05','H09'],'§5·8.2·10.2')

    # 9. Definition, model-facing schema and execution extension are distinct.
    d=old['S13']['diagram']
    d+=group(5,text(0,645,'공통 도구를 여러 Client에서 사용 → MCP / Hermes 내부 동작 확장 → Plugin',26,'context',700))
    put('S13','Tool·MCP·Plugin으로 기능 연결하기','모델이 볼 도구와 실제 실행 함수를 연결합니다.','무엇을 확장할지에 따라 Registry·MCP·Plugin을 선택합니다.',1,d,
        ['도구 등록','모델 노출','실행 함수','연결과 확장','선택 기준'],
        [('Registry','이름, 모델용 schema, handler와 가용성 조건을 관리합니다.'),('MCP','외부 서버가 제공하는 기능을 Client/Server 프로토콜로 연결합니다.'),('Plugin','Tool·Hook·명령과 Context/Memory 관련 실행환경을 확장할 수 있습니다.')],
        '등록된 모든 도구가 모델에 공개되는 것은 아닙니다. Toolset, 환경, check_fn 등 가용성 조건을 통과한 schema를 전달합니다. schema는 호출 형식을 알려주며, handler와 서비스가 실제 동작과 권한을 처리합니다.\n\n여러 Client가 공통으로 사용할 도구는 MCP 서버로 연결하는 선택이 가능하고, Hermes 내부 Hook이나 실행 기능을 바꾸려면 Plugin이 적합할 수 있습니다. 이는 선택 기준이며 MCP가 항상 별도 원격 프로세스이거나 보안을 자동으로 제공한다는 뜻은 아닙니다. Memory·Session Search·Delegation 등은 Agent 상태와 연결된 Inline 경로가 있어 일반 Registry dispatch와 다를 수 있습니다.',
        ['H11','H12'],'§11',talk='등록→노출→실행을 먼저 설명한 다음 Local/MCP/Plugin 연결을 비교한다. 모든 Tool이 같은 중앙 Hook을 지난다고 말하지 않는다.')

    # 10. Persist before effects, and show failure at the precise boundary.
    d=chain([('호출 검증','이름 · JSON 인자 · Call ID','runtime'),('호출 기록','Session에 먼저 저장','context'),('정책·승인','해당 Tool의 실행 조건 확인','runtime')],y=35,h=140)
    d+=group(2,arrow('M825 175 V217','risk')+text(825,260,'기록 실패 → 실행하지 않고 중단',27,'risk',700,'middle'))
    for step,x,name,desc,col in [(4,1170,'Handler 실행','허용된 범위에서 실제 작업','tool'),(5,585,'결과 기록','결과·오류를 Call ID와 연결','context'),(6,0,'다음 모델 요청','Tool 결과를 Context에 추가','model')]:
        d+=group(step,box(x,355,480,145,name,desc,col))
    d+=group(4,arrow('M1410 175 V343','tool'))+group(5,arrow('M1170 428 H1077','context'))+group(6,arrow('M585 428 H492','model'))
    d+=text(0,615,'대표 실행 경로 · Inline Tool과 Backend별 세부 경로는 다를 수 있음',24,'muted')
    put('S13A','Tool 요청이 실제 실행으로 이어지는 과정','호출을 검증하고 기록한 뒤, 실행 결과를 다시 모델에 전달합니다.','Tool 실행 전 기록은 필요하지만 외부 작업의 중복 방지까지 보장하지는 않습니다.',1,d,
        ['호출 검증','실행 전 기록','정책과 승인','실제 실행','결과 기록','모델 재호출'],
        [('Persist-before-execute','부작용을 시작하기 전에 Tool Call 정본을 저장하고, 그 저장이 실패하면 실행을 중단합니다.'),('Call / Result 대응','유효하지 않은 호출과 실행 오류도 대응 결과로 처리하여 메시지 관계를 유지합니다.'),('실행 후 장애','외부 작업 완료 뒤 결과 저장 전에 중단되면 실제 효과를 별도로 확인해야 합니다.')],
        '학습자료의 v0.22.5 Tool round는 호출 이름·인자·ID를 검증하고 Tool Call을 먼저 기록한 뒤 실행기로 전달하는 경로를 설명합니다. 유효하지 않은 호출이 섞인 배치는 유효 호출 처리와 오류 결과 대응을 구분합니다. 검증을 통과했다고 모든 인자의 업무적 의미가 옳다는 뜻은 아닙니다.\n\n대표 흐름은 검증→호출 기록→해당 경로의 정책·승인→handler→결과 기록→다음 모델 요청입니다. Inline/Registry/MCP/Plugin에 같은 Hook 순서를 보장하는 도식은 아닙니다. 호출 정본 저장 실패는 부작용 실행 전 중단합니다. 반면 외부 효과 발생 후 결과 기록 전 crash는 여전히 가능하므로 재시도에는 대상 시스템의 멱등성이나 효과 확인이 필요합니다. 후자는 일반 설계 원칙이며 모든 Tool에 내장됐다고 주장하지 않습니다.',
        ['H02','H11','HX01','HX02'],'§3.1·4.3·11.3~11.4·17.2',base='S13',evidence='v0.22.5 · 대표 실행 경로')

    # 11. Policy layers and failure types, without a single universal safety gate.
    d=chain([('실행 전 검사','명령 · 경로 · 인자 확인','runtime'),('사용자 승인','smart / manual / off|강제 차단 규칙은 별도','context'),('실행환경 권한','OS · DB · Sandbox','tool')],y=40,h=160)
    d+=group(4,box(0,365,480,170,'모델 API 장애','통신 retry · 설정된 대체 모델','model'))
    d+=group(5,box(585,365,480,170,'Tool 오류','오류 결과 → 모델에 전달|재실행 전 중복 효과 확인','risk'))
    d+=group(6,box(1170,365,480,170,'중단·Timeout','대기를 멈춰도 외부 효과는 남을 수 있음','risk'))
    d+=text(0,615,'Checkpoint: opt-in 파일 복구 · 외부 API·DB 변경 전체의 rollback은 아님',25,'muted')
    put('S13B','승인·오류·취소가 발생하면 어떻게 될까?','실행을 허가하는 과정과 실패 뒤 처리 방법을 나누어 봅니다.','취소와 재시도는 이미 발생한 외부 작업을 확인한 뒤 판단합니다.',1,d,
        ['검사','승인','실제 권한','API 장애','Tool 오류','중단과 복구'],
        [('다층 정책','모델 지침, Tool 검사, 사람 승인, OS·DB 권한은 서로 다른 통제입니다.'),('API retry / Tool 재실행','통신을 다시 시도하는 것과 외부 동작을 다시 수행하는 것은 다릅니다.'),('취소 / Rollback','중단 신호나 Future 취소만으로 이미 발생한 외부 효과가 되돌아가지는 않습니다.')],
        '명령·경로·인자 검사와 사람 승인, 실행환경의 실제 권한을 구분합니다. 승인 모드 off가 모든 강제 차단까지 없앤다는 뜻은 아니며 무인 실행 정책도 별도로 적용됩니다. Tool Output이나 검색 문서는 데이터로 다루어야 하며, 그 안의 지시를 실행 권한으로 승격해서는 안 됩니다. 검사·Hook만으로 모든 공격을 차단한다고 주장하지 않습니다.\n\nAPI 장애는 통신 retry나 설정된 fallback, Tool 오류는 모델이 읽는 오류 결과와 수정 경로로 이어집니다. 외부 쓰기 작업의 재실행에는 중복 효과를 확인해야 합니다. Timeout·취소 뒤 결과가 미상일 수 있고 opt-in Checkpoint는 지원 범위의 파일 복구 기능입니다. 검토한 인자와 최종 실행 인자 일치, 멱등성과 보상은 추가 검증할 업무 설계이며 Hermes 전 경로의 안전성 보증은 아닙니다.',
        ['H15','HX03','HX08'],'§4.2·12·13.5·17',base='S15')

    # 12. Distinct stores and the complete write/read lifecycle.
    d=group(1,box(0,30,760,145,'Session · state.db','대화 · Tool Call / Result · 실행 이력','context')+box(890,30,760,145,'Memory · MEMORY.md / USER.md','다음 세션에도 필요한 짧은 사실','context'))
    d+=chain([('memory Tool','저장 요청','tool'),('검사·승인','설정에 따른 검토','runtime'),('파일 저장','MemoryStore 변경','context'),('Tool 결과','성공·보류·오류 확인','tool')],y=285,w=345,gap=90,h=120,step=2)
    d+=group(6,box(0,500,760,125,'현재 세션 A','처음 읽은 system snapshot 유지','context')+box(890,500,760,125,'다음 세션 B','갱신된 파일로 새 snapshot 구성','context'))
    put('S10','Session과 Memory는 무엇을 저장할까?','실행 이력을 보관하는 경로와 지속 사실을 기록하는 경로','파일 저장 성공과 현재 system snapshot의 교체는 다른 동작입니다.',2,d,
        ['두 저장소','저장 요청','검사·승인','실제 저장','반환 확인','현재와 다음 세션'],
        [('Session','SQLite에 대화와 Tool 실행 이력을 보관합니다. Profile별 운영 범위를 확인합니다.'),('Memory write','memory Tool이 검사·승인 조건을 거쳐 파일을 바꾸고 성공·보류·오류 결과를 반환합니다.'),('Frozen snapshot','세션 중 파일을 갱신해도 이미 고정한 system snapshot은 자동 교체되지 않습니다.')],
        'Session은 상세 대화와 실행 이력을, MEMORY.md/USER.md는 짧은 지속 사실과 사용자 선호를 보관합니다. memory Tool은 Agent 상태를 사용하는 Inline 경로이며 실제 변경은 MemoryStore의 검사와 저장으로 이어집니다. write_approval 설정에 따라 즉시 검토하거나 pending 상태로 남을 수 있습니다. 말로 기억했다고 응답한 것만으로 파일 저장을 확인할 수는 없습니다.\n\n현재 세션은 처음 구성한 system snapshot을 유지합니다. 새 Tool 결과로 갱신 내용을 알게 되는 것과 system snapshot 교체는 구분하며 다음 세션은 갱신된 파일을 읽습니다. 2,200/1,375자 등은 설정 가능한 문서 기준값입니다. HERMES_HOME과 Profile 경로를 확인하며 Profile 분리를 보안 테넌트 격리로 단정하지 않습니다. 업무적으로 SOP 리비전과 데이터 기준 시점을 고정하고, 분석 중 변경 시 유지/재시작을 결정하는 설계가 필요합니다.',
        ['H05','H06','H07','HX09'],'§2.2·8·9.1')

    # 13. Retrieval selects evidence; it does not inject the whole database.
    d=group(1,text(0,50,'정확한 코드로 찾기',32,'context',700)+text(0,105,'장비 ID · 알람 코드',29,'text')+text(890,50,'비슷한 사례로 찾기',32,'context',700)+text(890,105,'표현이 달라진 과거 상황',29,'text'))
    d+=chain([('검색어 정리','질의 준비','runtime'),('FTS5 검색','과거 대화 조회','context'),('범위 확인','세션 · 대상 · 기간','runtime'),('Context에 추가','선택한 메시지와 문맥','model')],y=245,w=345,gap=90,h=155,step=2)
    d+=group(6,box(0,510,1650,125,'검색 결과를 평가하는 기준','코드 일치뿐 아니라 같은 대상·시점의 근거인지 확인 · 업무 평가 예시','context'))
    put('S11','과거 대화를 찾아 현재 작업에 사용하기','session_search가 필요한 기록을 선택해 Context에 넣습니다.','기본 대화 검색과 도메인 문서 검색은 대상과 요구가 다릅니다.',2,d,
        ['질의의 차이','검색어 준비','과거 대화 검색','범위 확인','선택 주입','근거 평가'],
        [('FTS5','기본 Session 검색에 사용하는 문자열 중심 전문 검색입니다. Dense Vector 검색과 다릅니다.'),('session_search','검색어와 조건으로 메시지를 찾고 필요한 전후 문맥을 탐색하는 경로입니다.'),('도메인 검색','SOP·매뉴얼·설비 데이터의 별도 저장소·권한·색인 설계가 필요한 검색입니다.')],
        '검색어 처리 뒤 FTS MATCH 또는 환경에 따른 대체 경로를 사용하고, 세션·시간·역할 등 조건과 관련 메시지를 확인해 결과를 현재 Context에 넣습니다. DB 전체가 자동 주입되거나 검색할 때마다 이 Tool이 LLM 요약을 수행하는 것으로 설명하지 않습니다. FTS 기반 검색도 생성에 근거를 제공하면 넓은 의미의 RAG 패턴에 쓰일 수 있습니다.\n\n정확한 장비 ID·코드 질의와 표현이 달라진 유사 사례 질의를 나누어 누락·오탐을 평가합니다. 같은 코드라도 다른 대상·기간이면 업무 근거가 달라집니다. 도식의 평가 기준은 추가 코멘트의 업무 설계 예시입니다. 외부 Memory Provider는 별도 확장이며 내장 파일 Memory나 기본 Session 검색과 동일하지 않습니다. CJK/trigram/tokenizer, 인덱스 재구축·삭제 정합성은 노트의 심화 범위입니다.',
        ['H07','H08','H05'],'§9',talk='두 질문의 차이를 제시하고 검색→선택→현재 입력의 흐름을 따라간다. 실제 검색 품질을 측정한 결과처럼 제시하지 않는다.')

    # 14. Read path and write path meet at an approved reusable artifact.
    d=text(0,30,'읽고 사용하기',30,'context',700)
    d+=chain([('인덱스','이름·설명으로 후보 확인','context'),('SKILL.md','선택한 절차 본문','context'),('참고 자료','필요한 파일·스크립트','tool')],y=70,h=135)
    d+=text(0,305,'만들고 수정하기',30,'runtime',700)
    d+=group(4,box(0,345,480,140,'skill_manage','생성 · 수정 · 삭제 요청','tool')+arrow('M480 415 H573','runtime')+box(585,345,480,140,'검사·승인','경로·내용 검사 · 필요 시 Diff 검토','runtime')+arrow('M1065 415 H1158','context')+box(1170,345,480,140,'파일 반영','이후 작업에서 다시 로딩','context'))
    d+=group(5,text(0,600,'Curator',30,'runtime',700)+text(250,600,'Agent 생성 Skill의 사용 이력 관리: active → stale → archived',28,'text'))
    put('S12','Skill을 만들고 다시 사용하는 과정','절차를 읽는 경로와 파일을 갱신하는 경로를 함께 봅니다.','생성된 Skill을 공식 SOP나 검증된 기준으로 자동 승격하지 않습니다.',2,d,
        ['목록','절차 본문','지원 자료','변경과 검토','Curator'],
        [('Skill','작업 순서와 주의점, 참고 자료를 제공하는 문서형 절차입니다. 실제 실행은 Tool이 맡습니다.'),('skill_manage','변경 요청을 검사하고 설정에 따라 승인·보류 후 파일에 반영합니다.'),('Curator','Agent 생성 Skill의 사용 이력을 관리하며 모든 사용자 Skill을 무조건 삭제하지는 않습니다.')],
        '목록→본문→필요한 참고 파일의 점진적 로딩으로 Context 점유를 줄입니다. 명시 선택, autoload, 모델 skill_view, Cron 첨부 등 로딩 경로가 있으며 모든 Skill이 무조건 모델 의미 검색으로 선택되는 것은 아닙니다.\n\n모델이 재사용 가치를 판단해 skill_manage를 호출하면 경로·인자 검증, 활성화된 scanner와 write approval을 거쳐 파일을 변경합니다. 승인 설정 시 pending과 Diff 검토 경로가 있습니다. Scanner와 승인, advisory linter는 목적이 다르며 업무 정확성을 보장하지 않습니다. 자기 개선은 이 재사용 정보의 변경을 뜻하며 기반 모델 가중치 학습과 다릅니다. 잘못된 절차도 재사용될 수 있어 SOP 원문·버전·범위를 확인하는 업무 검토가 필요합니다. Curator의 active/stale/archived 관리는 Agent 생성 대상과 발동 조건을 확인합니다.',
        ['H09','H10','H15'],'§10',talk='읽는 흐름을 먼저, 변경하는 흐름을 다음에 설명한다. SOP 범위·소유자·만료 관리 등은 제안이지 Hermes 기본 필드가 아니다.')

    # 15. Keep the accepted prefix illustration, now after state/skill lifecycles.
    put('S08','반복되는 입력과 Prefix Cache','Hermes가 구성한 입력을 추론 서비스가 재사용할 수 있습니다.','입력을 다시 보내도 같은 Prefix의 계산은 재사용될 수 있습니다.',3,old['S08']['diagram'],old['S08']['steps'][1:],
        [('입력 구성','Hermes는 지침·이력·schema의 내용과 배치를 구성하고 지원 Provider의 cache marker를 적용할 수 있습니다.'),('캐시 적중','실제 계산 재사용은 Provider·서빙 엔진이 결정하며 입력 길이 자체를 줄이지 않습니다.')],
        '세션 snapshot과 append 중심 이력은 안정적인 Prefix를 유지하는 데 도움이 됩니다. 반대로 앞부분의 지침 변경, schema 순서 변경, History 수정·압축은 재사용 구간에 영향을 줄 수 있습니다. 일부 앞부분만 바뀌었다고 모든 캐시가 항상 동일하게 무효화된다고 단정하지 않습니다.\n\n8,000/2,000 tokens는 설명용 수치입니다. PromptCachePlan, cache_control, TTL·one-shot 조건은 특정 Provider 경로의 심화 설명이며 vLLM 공통 계약으로 보지 않습니다. 실제 적중·비용·TTFT는 지원 모델과 환경에서 측정해야 하고 OpenAI 프록시 기록을 vLLM 캐시 실측으로 제시하지 않습니다.',
        ['H04','V01'],'§6·7.6')

    # 16. Show the work between before and after, not just a shorter result.
    d=chain([('Tool 결과 축소','오래되고 큰 본문부터 검토','context'),('보호 구간 선택','최근 문맥 · 아직 쓸 결과 · 호출 쌍','context'),('중간 이력 요약','보조 모델로 필요한 내용 정리','model')],y=45,h=160)
    d+=group(4,box(0,395,760,145,'요약과 보호 구간 합성','현재 작업을 이어갈 Context 구성','context')+arrow('M1650 125 H1665 V305 H380 V383','context'))
    d+=group(5,box(890,395,760,145,'Call / Result 정합성 확인','대응 ID와 프로토콜 관계 보존','runtime')+arrow('M760 468 H878','runtime'))
    d+=text(0,625,'정확한 수치·SQL·원본 근거는 별도 보관 · 업무 설계 예시',25,'muted')
    put('S09','Context가 길어졌을 때 줄이고 보존하기','Tool 결과 축소부터 요약과 정합성 확인까지','요약으로 줄일 내용과 원문으로 남길 근거를 구분합니다.',3,d,
        ['큰 결과 축소','보호할 문맥','요약','합성','정합성 확인'],
        [('Pruning','보호 대상이 아닌 오래되고 큰 Tool 결과를 줄이는 처리입니다.'),('Summary와 보호 구간','중간 이력을 요약하되 최근 작업과 호출·결과 관계를 보존합니다.'),('실패와 근거 보존','압축도 실패할 수 있는 처리이며 원본 근거의 보관·재조회 정책이 필요합니다.')],
        '현재 토큰과 메시지 상태로 필요 여부를 판단하고 오래된 큰 Tool body를 줄인 뒤 최근 Turn·아직 판단에 쓰지 않은 결과·호출 쌍을 보호합니다. 중간 History를 보조 모델로 요약하고 보호 구간과 합성해 메시지 정합성을 확인합니다. 압축으로 Skill 본문이 사라질 때 재로딩 안내가 필요한 경로와 세션 lineage가 있습니다.\n\nTool Loop의 압축과 Gateway 세션 위생은 다른 위치이며 50%/85%와 최근 20개는 조건·설정에 따른 문서 기본 설명입니다. Timeout 시 원본 유지와 종료 안내, 실제 감소 여부 확인 등 실패 경로도 있습니다. 정확한 단위·SQL·데이터 ID·SOP 리비전·checksum을 artifact에 남기는 것은 업무 설계 제안입니다. SOP가 분석 중 바뀌면 기존 근거 유지 또는 새 분석 시작을 명시적으로 결정해야 하며 frozen Memory만으로 최신성이 보장되지는 않습니다.',
        ['H04','H02'],'§7',talk='도식은 처리 책임을 연결한 설명이다. 모든 압축 호출이 모든 단계를 같은 방식으로 실행한다고 일반화하지 않는다.')

    # 17. Parallel segments within one loop, then emission-order results.
    d=text(0,35,'호출 예시',27,'muted')+text(290,35,'read(A) · read(B) → write(A) → read(C)',31,'context',700)
    d+=group(1,box(0,155,480,95,'read(A)','','tool',30)+box(0,285,360,95,'read(B)','','tool',30))
    d+=group(2,box(660,155,330,225,'write(A)','충돌 작업은 단독 구간','runtime',30)+arrow('M480 202 H648','tool')+arrow('M360 332 H570 V270 H648','tool'))
    d+=group(3,box(1170,155,480,225,'read(C)','앞 구간 이후 실행','tool',30)+arrow('M990 270 H1158','tool'))
    d+=group(4,box(0,500,1650,130,'결과를 모델 이력에 추가','완료 순서와 별개로 Call ID에 대응시키고 원래 호출 순서에 맞춰 정리','context',31))
    put('S14','여러 Tool을 함께 실행하기','독립 호출을 묶고, 충돌하는 작업은 순서를 지킵니다.','여러 Tool을 제안하는 것과 실제로 병렬 실행하는 것은 다릅니다.',3,d,
        ['독립 조회','실행 장벽','후속 작업','결과 순서'],
        [('Segmented execution','Reader·대화형 Tool·경로 충돌 등을 고려해 병렬/순차 구간을 나눕니다.'),('Worker','같은 Agent Loop의 handler를 실행하는 수단이며 독립 Agent가 아닙니다.'),('결과 대응','완료 시각보다 원래 call_id와 결과의 정확한 연결이 중요합니다.')],
        'v0.22.5의 Tool Executor는 sequential/concurrent/segmented 경로와 DaemonThreadPoolExecutor, Worker Context 전달·시작 Gate·deadline 처리를 포함합니다. 도식은 학습자료의 읽기/쓰기 예시를 단순화한 것이며 모든 인자·Backend에서 같은 분할이 나온다는 보장은 아닙니다.\n\n독립 조회는 겹칠 수 있지만 같은 파일의 읽기·쓰기, 대화형 작업 등은 장벽이 필요할 수 있습니다. 결과는 완료 순서가 아니라 원래 호출 순서와 ID 대응을 유지하도록 정리합니다. Timeout 뒤 외부 작업은 미상 상태일 수 있으므로 앞에서 설명한 취소·효과 확인 원칙을 연결합니다. 같은 snapshot으로 조회한다는 데이터 조건은 실행 barrier만으로 자동 보장되지 않습니다.',
        ['H13','HX08'],'§13',evidence='v0.22.5 · 실행 계획 예시')

    # 18. Separate child loops; contracts and fan-in stay visible.
    d=group(1,box(550,15,550,115,'부모 AIAgent','Goal · Context · Toolset · 예산 전달','runtime',32))
    d+=group(2,box(0,255,720,180,'Child A · 데이터 분석','독립 Context · 별도 모델/Tool Loop|허용 Toolset과 실행 예산','runtime',31)+box(930,255,720,180,'Child B · 근거 검색','독립 Context · 별도 모델/Tool Loop|허용 Toolset과 실행 예산','runtime',31)+arrow('M690 130 V195 H360 V243','runtime')+arrow('M960 130 V195 H1290 V243','runtime'))
    d+=group(3,box(550,525,550,110,'결과 검토·통합','요약 · 상태 · 필요한 출력 검증','context',30)+arrow('M360 435 V480 H700 V513','context')+arrow('M1290 435 V480 H950 V513','context')+arrow('M1100 580 H1690 V72 H1112','context'))
    put('S14A','별도 Agent에게 작업 맡기기','delegate_task로 하위 목표를 나누고 결과를 부모가 받습니다.','독립 Context를 사용해도 파일·DB·인증 권한은 따로 확인해야 합니다.',3,d,
        ['작업 범위 전달','자식 Loop','검토와 부모 복귀'],
        [('Child AIAgent','자신의 메시지·Goal·Context·Task·예산을 가진 별도 Loop입니다.'),('결과 통합','부모가 자식의 결과와 상태를 받아 다음 판단을 이어갑니다.'),('격리와 비용','대화 분리, 터미널, worktree, credential은 다른 격리 범위이며 호출 비용도 증가할 수 있습니다.')],
        '부모가 delegate_task로 목표와 필요한 문맥을 전달하면 자식의 Toolset·권한·예산 등을 구성해 별도 AIAgent Loop를 실행합니다. 부모 History와 자식 Messages는 분리되며, 자식은 부모에 요약·상태 또는 지정한 출력 계약을 반환합니다.\n\n문서상 output_schema로 구조 검증과 제한적 수정 경로를 구성할 수 있지만 자식 완료가 내용의 신뢰성을 보장하지는 않습니다. 배치·background 반환은 코드 태그와 현행 문서의 조건을 확인합니다. 독립 조사·검토에는 유용할 수 있으나 강한 순서 의존 작업·공유 파일 쓰기는 조정 비용이 커집니다. Worktree는 선택적·환경 의존 기능이며 Context 분리만으로 OS/DB/credential 격리가 완성되지 않습니다.',
        ['H14'],'§14',base='S14')

    # 19. The canonical writer is the Gateway, not every client independently.
    d=group(1,box(0,20,350,105,'CLI / TUI','','runtime',29)+box(0,205,350,105,'API / ACP','','runtime',29)+box(0,390,350,105,'메신저 Client','','runtime',29))
    d+=group(2,box(500,125,650,345,'Gateway','인증 · Session Routing|Turn 순서 · Busy Session 처리|정식 세션의 논리적 쓰기 소유권','runtime',37)+arrow('M350 72 H420 V185 H488','runtime')+arrow('M350 257 H488','runtime')+arrow('M350 442 H420 V395 H488','runtime'))
    d+=group(3,box(1290,80,360,120,'AIAgent','모델 호출 · Tool 실행','runtime',31)+arrow('M1150 165 H1278','runtime')+arrow('M1290 195 H1220 V250 H1162','context')+box(1290,410,360,120,'Session DB','기록 · 상태 · 이력','context',31)+arrow('M1150 390 H1220 V470 H1278','context'))
    d+=group(4,text(0,600,'새 메시지 → 대기·중단 정책 / 승인·거부·Stop → 별도 제어 경로',29,'context',700))
    put('S14B','Gateway가 세션과 실행을 관리하는 방식','여러 Client가 같은 Session을 사용할 때 실행 순서와 기록을 관리합니다.','연결·Agent 실행·승인 대기·세션 저장은 서로 다른 수명을 가집니다.',4,d,
        ['여러 입력 표면','세션 소유권','실행과 저장','실행 중 개입'],
        [('Session Authority','공식 세션 문서에서 프로필 Gateway가 정식 세션의 논리적 쓰기 주체를 맡는 구조입니다.'),('Turn admission','실행 중인 세션의 추가 요청을 대기·중단 등 정책으로 처리합니다.'),('전달과 실행 수명','동기 응답·SSE Stream·비동기 Run 관리와 실제 Agent 실행을 구분합니다.')],
        '공식 v0.22 계열 Session Storage 문서는 CLI/TUI/Desktop/API/ACP/Cron 등 Client가 프로필 Gateway를 통해 정식 세션 요청과 쓰기를 관리하는 구조를 설명합니다. 이 논리적 소유권을 SQLite WAL의 일반적인 writer 제약과 혼동하지 않습니다. 도식은 해당 문서의 책임 배치이며 모든 standalone 진입점의 세부 호출을 고정한 구현도가 아닙니다.\n\n실행 중 같은 Session에 요청이 오면 Queue/Interrupt 정책을 적용하고 승인·거부·stop 같은 제어 메시지는 별도 통로로 처리할 수 있습니다. 동기·SSE·비동기 Run은 연결과 실행 상태를 관리하는 서로 다른 표면입니다. API/승인/재연결의 지원 조건은 실제 릴리스에서 대조해야 합니다. Agent Runtime의 CPU·Tool I/O·모델 대기·승인 대기와 모델 서버 GPU 자원을 분리해 관찰해야 하며 이 구조만으로 Worker 수나 재시작 복구를 보장할 수는 없습니다.',
        ['H07','HX04','HX05'],'§15',base='S04',evidence='공식 세션 문서 · 책임 배치')

    # 20. Claiming an occurrence is not exactly-once external effects/delivery.
    d=chain([('스케줄 확인','Tick · 실행 시각 확인','runtime'),('실행 슬롯 Claim','Lock · 예약 회차 관리','context'),('새 Session','Prompt · Skills · Memory','context'),('Agent Loop','Tool 실행 · 결과 저장·전달','tool')],y=45,w=345,gap=90,h=165)
    d+=group(5,text(0,325,'구분해서 확인할 세 가지',31,'text',700)+box(0,385,480,170,'예약 중복 방지','같은 예약 회차의 시작 관리','runtime',30)+box(585,385,480,170,'외부 작업','중복 부작용은 대상 시스템과 확인','tool',30)+box(1170,385,480,170,'결과 전달','작업 성공과 전달 성공을 구분','context',30))
    d+=text(0,625,'Agent 작업 모드의 예시 · 새 Session도 지속 Memory와 Skills를 사용할 수 있음',25,'muted')
    put('S14C','Cron으로 예약 작업 실행하기','예약 시각이 되면 새 Agent 작업을 시작하고 결과를 전달합니다.','실행 슬롯의 중복 방지는 외부 작업의 exactly-once 보장과 다릅니다.',4,d,
        ['예약 확인','회차 Claim','새 실행 구성','작업과 전달','서로 다른 성공 기준'],
        [('Cron occurrence','특정 예약 회차를 Lock·Claim·다음 시각 갱신 등으로 관리합니다.'),('Fresh Session','이전 Cron 대화를 무한 누적하지 않고 새 Agent 작업으로 시작합니다.'),('외부 효과와 Delivery','작업 시작, 외부 부작용, 결과 전달은 서로 다른 성공·실패 기준입니다.')],
        'Agent 작업 모드의 Cron은 Gateway tick 또는 관리형 Trigger에서 실행 시각과 Lock/Claim을 확인하고 새 세션을 구성한 뒤 Prompt와 첨부 Skills 등을 사용해 Loop를 실행합니다. jobs.json, pending_slot과 next-run 관리의 세부 동작은 문서·코드 태그를 함께 확인합니다. 새 Session이라도 지속 Memory와 Skills는 로드될 수 있어 완전 stateless로 설명하지 않습니다.\n\n예약 회차 중복 시작을 줄이는 것과 외부 API/DB 효과가 정확히 한 번 발생하는 것, 결과가 사용자에게 전달되는 것은 다릅니다. 멱등성·효과 확인·전달 재시도는 대상 시스템과 업무 설계가 필요합니다. 공식 문서에는 no-agent script 모드도 있어 Cron을 무조건 Agent 실행이라고 일반화하지 않습니다. 사전 Script가 실행되면 Tool 승인과 같은 정책이 자동 적용된다고 보지 않으며 무인 승인·권한을 별도로 확인합니다.',
        ['H16','HX06','HX07'],'§16',base='S15',evidence='공식 Cron 문서 · Agent 모드')

    # 21. Observe the sequence already explained; no fabricated runtime output.
    d=chain([('질문 입력','합성 데이터 조회 요청','runtime'),('모델 요청','system · history · tools','model'),('Tool 처리','Call ID · 인자 · 결과','tool'),('저장 확인','Session · Memory 변경','context')],y=70,w=345,gap=90,h=160)
    d+=group(5,box(0,380,760,165,'후속 질문과 Memory','누적 이력 · 파일 diff|현재 snapshot과 다음 세션 비교','context',31)+box(890,380,760,165,'선택한 확장 한 경로','Skill · MCP · 위임 중 실제 발생한 경로|나머지는 별도 실행 기록으로 확인','runtime',31))
    d+=text(0,625,'현재 Demo 링크는 연결 안내입니다. 실제 실행 서비스는 별도로 연결합니다.',25,'muted')
    put('S15','Hermes Demo','지금까지 설명한 요청·Tool·저장 과정을 실행 기록에서 확인합니다.','기본 흐름을 먼저 확인하고, 확장 기능은 실제 발생한 경로만 살펴봅니다.',5,d,
        ['입력','최종 모델 요청','Tool 호출과 반환','저장 상태','후속 질문과 확장'],
        [('관찰 단위','사용자 요청→모델 입력→Tool Call/Result→세션·파일 변경을 ID로 연결합니다.'),('Memory 확인','실제 Tool 반환과 파일 diff, 현재 snapshot/다음 세션을 나누어 봅니다.'),('실행 기록의 구분','live·사전 기록·fixture를 표시하고 이번 실행에서 일어나지 않은 기능을 시연한 것처럼 표시하지 않습니다.')],
        '합성 데이터 조회와 후속 질문으로 기본 실행을 확인하고 최종 request, tool_call_id, 인자·반환, 종료 원인과 세션 저장을 관찰하는 Demo 계획입니다. Memory 쓰기를 선택하면 실제 Tool·파일 diff와 snapshot을 비교합니다. Skill/MCP/위임/압축/승인을 한 자연 실행에 모두 강제하지 않고 이름 있는 별도 시나리오로 준비합니다.\n\n현재 연결 페이지에는 실제 Hermes 실행 서비스나 Trace가 없으며 이 장도 실행 결과를 꾸며 표시하지 않습니다. Codex 지시의 두 Demo는 10000, Antigravity 지시의 두 Demo는 10001 호환 endpoint를 사용한다는 계약을 유지합니다. 로컬 프록시와 대상 PC의 vLLM은 실제 관찰 환경을 구분합니다. 기존 Profile과 DB/Memory를 덮어쓰지 않는 별도 Demo 환경이 필요합니다.',
        ['H01','H02','H05','H11','H14'],'§3·8·11·14',evidence='실행 관찰 계획 · 서비스 별도')

    # Retain the original snapshot/FTS/resource comments as linked local evidence.
    for ident,section in [('S10','§1'),('S09','§1'),('S11','§2'),('S14B','§3')]:
        slides[ident]['localEvidence'].append({'path':str(comments.relative_to(project)).replace('\\','/'),'sections':section})
    for ident in HERMES_ORDER:
        if 'blueprintIds' not in slides[ident]:
            slides[ident]['blueprintIds']=([ident] if ident in env['specs'] else [])+(['S06'] if ident=='S05' else [])
    return HERMES_ORDER
