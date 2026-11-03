"""Build five standalone, offline HTML slide examples from the final blueprint."""
from pathlib import Path
from html import escape
import base64
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
FONT = ROOT / 'assets' / 'NanumGothic-Regular.ttf'
FONT.parent.mkdir(parents=True, exist_ok=True)
if not FONT.exists():
    urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf', FONT)
font_data = base64.b64encode(FONT.read_bytes()).decode()
license_file = FONT.with_name('OFL.txt')
if not license_file.exists():
    urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/OFL.txt', license_file)
font_license = json.dumps(license_file.read_text(encoding='utf-8'), ensure_ascii=False)
base = (ROOT / 'assets/viewport-base.css').read_text(encoding='utf-8')
C = {'model':'#60A5FA','runtime':'#B794F4','tool':'#34D399','context':'#FDBA74','risk':'#FB7185','success':'#5EEAD4','muted':'#9EACC8','line':'#33415D','text':'#EFF4FF'}

def text(x,y,value,size=26,color='text',weight=400,anchor='start',cls=''):
    color=C.get(color,color)
    return f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'

def box(x,y,w,h,title,sub='',color='runtime',size=29):
    col=C[color]
    out=f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" fill-opacity=".055" stroke="{col}" stroke-opacity=".75" stroke-width="1.6"/>'
    out+=text(x+24,y+42,title,size,color,700)
    if sub:
        for i,line in enumerate(sub.split('|')):
            out+=text(x+24,y+78+i*31,line,22,'muted')
    return out

def arrow(d,color='line',dash=False,label=None,lx=0,ly=0):
    out=f'<path d="{d}" fill="none" stroke="{C[color]}" stroke-width="2.3" marker-end="url(#{color}-arrow)"'+(' stroke-dasharray="7 7"' if dash else '')+'/>'
    if label: out+=text(lx,ly,label,21,color)
    return out

def group(step,content): return f'<g data-focus="{step}">{content}</g>'

svg_index = 0
def svg(content,label):
    global svg_index
    svg_index += 1
    prefix = f'svg{svg_index}-'
    content = content.replace('url(#', f'url(#{prefix}')
    defs=''.join(f'<marker id="{prefix}{k}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="{v}"/></marker>' for k,v in C.items())
    return f'<svg viewBox="0 0 1652 650" role="img" aria-label="{escape(label)}"><defs>{defs}</defs>{content}</svg>'

# === S04: architecture; every line carries a direction or relationship label ===
s1=group(1,box(0,0,1260,82,'입력 경로','', 'runtime')+text(250,50,'CLI   /   Gateway   /   HTTP API   /   ACP',25,'muted')+arrow('M630 82 V126','runtime',label='요청',lx=650,ly=112))
s1+='<rect x="0" y="134" width="1260" height="290" rx="16" fill="#B794F4" fill-opacity=".025" stroke="#B794F4" stroke-width="1.8"/>'
s1+=text(26,177,'AIAgent',30,'runtime',700)+text(200,176,'반복 실행 · 응답 분기 · 상태 관리',23,'muted')
s1+=group(2,box(28,218,350,144,'Prompt / Compression','지침·이력 구성|Context 한도 관리','context')+box(448,218,350,144,'Provider adapter','모델별 요청 변환|응답을 내부 형식으로','model')+arrow('M378 290 H438','context'))
s1+=group(3,box(868,218,364,144,'Tool dispatch','이름·인자 확인|실행·결과 수집','tool')+arrow('M798 290 H858','tool',label='호출 요청',lx=791,ly=206))
s1+=group(2,box(1360,178,292,144,'Model','판단 · 응답 생성','model')+arrow('M1260 240 H1350','model',label='모델 요청',lx=1266,ly=219)+arrow('M1360 290 H1270','model'))
s1+=group(3,box(1360,376,292,137,'Tools','파일 · DB · 외부 API','tool')+arrow('M1232 332 H1308 V419 H1350','tool')+arrow('M1360 474 H1308 V391 H1232','tool'))
s1+=group(4,box(0,505,390,128,'Session','SQLite · 대화 기록 · FTS5','context')+box(435,505,390,128,'Memory','MEMORY.md · USER.md','context')+box(870,505,390,128,'Skills','절차 · 참고 자료','context')+arrow('M195 424 V495','context',label='저장·조회',lx=211,ly=469)+arrow('M630 505 V434','context',label='읽기·갱신',lx=647,ly=469)+arrow('M1065 505 V434','context',label='필요시 로딩',lx=1080,ly=469))
s1+=text(24,402,'실행 접점에서 정책 검사 · 승인 · Trace 관찰',21,'muted')

# === S07: frozen snapshot versus request-time additions ===
s2=text(0,28,'세션에서 재사용하는 System Prompt',28,'context',700)
s2+=group(1,'<rect x="0" y="57" width="650" height="440" rx="14" fill="#FDBA74" fill-opacity=".025" stroke="#FDBA74" stroke-width="1.5"/>'+box(22,80,606,110,'Stable','SOUL · 정체성 · 기본 행동 지침','context')+box(22,213,606,110,'Context','프로젝트 규칙 · 호출자 지침','context')+box(22,346,606,127,'Volatile','MEMORY / USER · 런타임 snapshot','context')+text(0,540,'Volatile도 고정된 snapshot의 일부일 수 있다',25,'context',700))
s2+=group(2,box(770,80,380,130,'대화 이력','user / assistant / tool','context')+box(770,315,380,130,'이번 호출 정보','실행 상태 · 일시적 안내','runtime'))
s2+=group(3,box(1250,185,402,233,'모델 요청','고정 System Prompt|+ 누적 대화 이력|+ 호출 시점 정보','model')+arrow('M650 275 H1240','context',label='snapshot 재사용',lx=798,ly=259)+arrow('M1150 143 H1197 V225 H1240','context')+arrow('M1150 380 H1240','runtime')+arrow('M1451 418 V492','model')+text(1451,535,'Model',30,'model',700,'middle'))
s2+=text(770,605,'Provider adapter가 최종 API 형식으로 변환',24,'muted')

# === S14: two units of parallelism ===
s3='<line x1="826" x2="826" y1="0" y2="650" stroke="#33415D"/>'
s3+=text(0,30,'여러 Tool',33,'tool',700)+text(0,70,'한 Loop가 요청하고 결과를 모은다',24,'muted')
s3+=text(885,30,'여러 Child Agent',33,'runtime',700)+text(885,70,'각자 모델 호출과 Context를 가진다',24,'muted')
s3+=group(1,box(125,113,520,99,'한 번의 모델 응답','','model')+text(385,181,'여러 Tool Call',23,'muted',400,'middle')+arrow('M385 212 V253 H118 V284','tool')+arrow('M385 253 V284','tool')+arrow('M385 253 H652 V284','tool')+box(0,294,236,110,'온도 조회','Tool A','tool',27)+box(267,294,236,110,'압력 조회','Tool B','tool',27)+box(534,294,236,110,'통계 계산','Tool C','tool',27)+arrow('M118 404 V446 H385 V483','tool')+arrow('M385 404 V483','tool')+arrow('M652 404 V446 H385','tool')+box(125,493,520,106,'결과를 Context에 추가','같은 Loop의 다음 모델 호출','context'))
s3+=group(2,box(1000,113,520,99,'부모 AIAgent','','runtime')+text(1260,181,'delegate_task',23,'muted',400,'middle')+arrow('M1260 212 V245 H1060 V284','runtime')+arrow('M1260 245 H1460 V284','runtime')+box(885,294,350,145,'Child A','독립 Context + Loop|온도 데이터 분석','runtime')+box(1285,294,350,145,'Child B','독립 Context + Loop|압력 데이터 분석','runtime')+arrow('M1060 439 V469 H1260 V500','context')+arrow('M1460 439 V469 H1260','context')+box(1000,510,520,89,'요약을 받아 부모가 계속 판단','','context',27))
s3+=group(3,text(885,645,'공유 파일·DB 권한은 별도로 격리해야 한다',24,'risk'))

# === S23: internal graph with explicit tool and output branches ===
s4=group(1,box(0,85,410,142,'UserPromptNode','입력·지시·이력 준비','context')+arrow('M410 156 H500','context'))
s4+=group(2,box(510,85,470,142,'ModelRequestNode','요청 구성 · Provider 호출','model')+arrow('M980 156 H1080','model',label='모델 응답',lx=985,ly=133))
s4+=group(3,box(1090,85,562,142,'CallToolsNode','Tool · Output 분류','runtime'))
s4+=group(4,arrow('M1250 227 V308 H745 V355','tool',label='Function Tool',lx=985,ly=288)+box(510,365,470,136,'인자 검증 → Tool 실행','실행 결과를 ToolReturn으로 기록','tool')+arrow('M510 435 H455 V265 H745 V237','context',label='다음 모델 요청',lx=485,ly=292))
s4+=group(5,arrow('M1460 227 V355','runtime',label='최종 Output',lx=1480,ly=301)+box(1130,365,522,136,'출력 검증','타입 · 업무 Validator','runtime')+arrow('M1390 501 V562','success',label='유효',lx=1410,ly=541)+box(1220,572,342,70,'End · 최종 결과','','success',26)+arrow('M1130 447 H1040 V600 H425 V250 H685 V237','risk',label='검증 실패 → 수정 피드백',lx=650,ly=582))
s4+=text(0,25,'PydanticAI 내부 실행 Graph · pydantic-graph',25,'muted')
s4+=text(0,642,'State  /  history · usage · retry · step',23,'context')

# === S28: one emitted response, three concrete execution policies ===
s5=text(0,25,'모델이 한 응답에서 제안한 순서',24,'muted')
cells=[('조회 A','Function Tool','tool'),('출력 O1','Output Tool','runtime'),('게시 Mock B','Function Tool','tool'),('출력 O2','Output Tool','runtime')]
for i,(title,sub,color) in enumerate(cells):
    x=310+i*325
    s5+=box(x,52,290,104,title,sub,color,27)
    if i<3: s5+=arrow(f'M{x+290} 102 H{x+315}','line')
s5+=text(0,193,'전제: O1·O2 모두 유효 / Retry 없음 / 비스트리밍 / barrier 없음',22,'muted')
lanes=[('early',['skip','output','skip','skip'],'O1만 처리하고 종료'),('graceful',['run','output','run','skip'],'뒤 Function도 실행'),('exhaustive',['run','output','run','output'],'모두 실행 · 기본 병렬')]
for j,(name,statuses,explain) in enumerate(lanes):
    y=238+j*132
    part=text(0,y+35,name,31,'runtime',700)+text(0,y+76,explain,21,'muted')
    for i,status in enumerate(statuses):
        x=310+i*325
        col='muted' if status=='skip' else ('runtime' if i%2 else 'tool')
        part+=f'<rect x="{x}" y="{y}" width="290" height="82" rx="10" fill="{C[col]}" fill-opacity="{.025 if status=="skip" else .08}" stroke="{C[col]}" stroke-opacity="{.3 if status=="skip" else .8}"'+(' stroke-dasharray="5 6"' if status=='skip' else '')+'/>'
        label='생략' if status=='skip' else ('O1 선택' if i==1 else ('실행 · 미선택' if i==3 else '실행'))
        part+=text(x+145,y+50,label,26,col,700,'middle')
    s5+=group(j+1,part)
s5+=text(310,647,'최종 결과는 emission 순서의 첫 유효 Output · 완료가 빠른 순서가 아니다',23,'context')

slides=[
dict(id='S04',section='Hermes / Architecture',title='Hermes는 반복 실행을 중심으로 기능을 묶습니다',sub='입력부터 모델·도구·저장소까지, 먼저 전체 지도를 봅니다.',diagram=s1,steps=['전체 아키텍처','입력 경로','Prompt와 모델 요청','Tool 실행 경로','세션·기억·절차'],take='모델 호출·도구 실행·상태 보존을 AIAgent가 연결한다.',note='실제 구현을 단순화한 구조도입니다. CLI/Gateway/API/ACP 등은 진입 경로입니다. Prompt와 Provider 변환, Tool dispatch, 저장소를 구분해 설명합니다. 도식의 연결은 대표 관계이며 모든 호출의 상세 순서를 뜻하지 않습니다. 다음 확대 장표에서도 같은 역할 색을 유지합니다.',sources=[['Architecture','https://hermes-agent.nousresearch.com/docs/developer-guide/architecture'],['Agent Loop','https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop']],version='Hermes v0.22.5 · 구현 단순화'),
dict(id='S07',section='Hermes / Context',title='고정 Prompt와 호출별 정보는 따로 움직입니다',sub='세션 snapshot에 대화 이력과 이번 호출 정보를 합쳐 요청을 구성합니다.',diagram=s2,steps=['전체 구성','System Prompt snapshot','이력과 호출 시점 정보','최종 모델 요청'],take='Volatile이라는 이름이 매 호출 재작성을 뜻하지는 않는다.',note='Stable은 정체성과 기본 행동, Context는 프로젝트·호출자 지침, Volatile은 기억·사용자·런타임 snapshot의 논리적 계층입니다. 모두 세션 내 고정 prompt의 일부일 수 있습니다. Skill 위치는 현행 문서 자체에 불일치가 있어 여기서는 특정 계층으로 단정하지 않았습니다. 실제 wire payload는 Provider adapter 뒤에서 확인해야 합니다.',sources=[['Prompt Assembly','https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly']],version='Hermes · Prompt assembly'),
dict(id='S14',section='Hermes / Orchestration',title='병렬 Tool과 Child Agent는 실행 단위가 다릅니다',sub='함수를 나란히 실행하는 것과 독립적인 Agent Loop를 위임하는 것은 다릅니다.',diagram=s3,steps=['두 실행 구조','한 Loop의 여러 Tool','자식마다 독립 Loop','공유 자원과 격리'],take='자식의 결과는 부모로 돌아오며, 부모가 다음 판단을 이어간다.',note='왼쪽은 병렬화 가능한 독립 Tool의 개념 예시입니다. 실제 Hermes는 상호작용·파일 충돌 등의 조건에 따라 barrier로 실행 구간을 나눕니다. 오른쪽 delegate_task는 별도 AIAgent의 Goal/Context/Loop를 사용합니다. thread는 실행 수단이며 Agent의 개수와 동일한 개념이 아닙니다. Context 분리만으로 OS·DB·파일 보안 격리가 만들어지지는 않습니다.',sources=[['Tool planner','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/agent/tool_dispatch_helpers.py'],['Delegation','https://github.com/NousResearch/hermes-agent/blob/v0.22.5/tools/delegate_tool.py']],version='Hermes v0.22.5 · 개념 비교'),
dict(id='S23',section='PydanticAI / Graph',title='세 Graph 노드가 다음 실행을 정합니다',sub='모델 응답은 Tool 실행·최종 출력·수정 요청의 서로 다른 경로로 이어집니다.',diagram=s4,steps=['전체 Graph','입력과 이력 준비','모델 요청','응답 분류','Tool 실행과 재요청','Output 검증과 종료'],take='유효한 Output은 종료로, Tool 결과와 수정 피드백은 다음 요청으로 간다.',note='PydanticAI의 내부 실행은 pydantic-graph이며 LangGraph가 아닙니다. UserPromptNode는 입력·지시·이력·재개 상태를 준비합니다. ModelRequestNode는 요청과 Provider 호출을 처리하고 CallToolsNode는 응답을 분류합니다. 출력 검증 실패와 Tool 결과가 다음 모델 요청으로 이어지는 대표 경로를 그렸습니다. 예산 초과·취소·Provider 장애 등은 이 장의 생략된 분기입니다. 정확한 Tool/Output 혼합 정책은 다음 EndStrategy 장표에서 설명합니다.',sources=[['Agent Graph source','https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_agent_graph.py']],version='PydanticAI v2.61.0 · 대표 경로'),
dict(id='S28',section='PydanticAI / Finalization',title='EndStrategy는 실제 실행 범위를 바꿉니다',sub='같은 모델 응답이라도 실행되는 Tool과 최종화 시점이 달라집니다.',diagram=s5,steps=['같은 응답과 통제 조건','early','graceful','exhaustive'],take='graceful에서도 최종 Output 뒤 Function Tool이 실행될 수 있다.',note='비스트리밍·유효 Output·Retry/승인 없음이라는 통제 조건의 설명용 비교입니다. early는 O1만 성공시키고 Function을 생략합니다. graceful은 A를 마친 뒤 O1을 처리하고 뒤 Function B도 실행하며 O2는 생략합니다. exhaustive는 모두 실행하며 emission 순서상 첫 유효 O1을 결과로 선택합니다. Function ModelRetry가 결과를 억제하는 retry-wins, Native/Prompted/plain text, 이미 확정된 streaming 결과는 별도 예외입니다. Mock 게시를 실제 외부 게시로 구현하지 않습니다.',sources=[['Tool executor','https://github.com/pydantic/pydantic-ai/blob/v2.61.0/pydantic_ai_slim/pydantic_ai/_tool_execution.py']],version='PydanticAI v2.61.0 · 통제 조건 예시'),
]

style=r'''
/* === TOKENS AND TYPOGRAPHY: unchanged blueprint palette === */
:root{--stage-bg:#070b16;--slide-bg:#0B1020;--text:#EFF4FF;--muted:#9EACC8;--line:#33415D;--runtime:#B794F4;--context:#FDBA74;--model:#60A5FA;--tool:#34D399}
*{box-sizing:border-box}body{font-family:'Seminar Korean',sans-serif;color:var(--text)}button,a{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid var(--model);outline-offset:5px}
/* === SLIDE FRAME === */
.slide{padding:65px 134px 55px;transition:opacity .25s ease-out}
.section-label{font-size:18px;color:var(--muted);margin:0 0 26px;display:flex;align-items:center;gap:17px}.section-label:before{content:'';width:24px;height:3px;background:var(--runtime)}
h1{font-size:50px;line-height:1.3;margin:0;font-weight:700;letter-spacing:-1.6px}.subtitle{font-size:26px;line-height:1.5;color:var(--muted);margin:20px 0 0}
.diagram{position:absolute;left:134px;right:134px;top:263px;height:650px}svg{width:100%;height:100%;overflow:visible}svg text{font-family:'Seminar Korean',sans-serif}g[data-focus]{transition:opacity .25s ease-out}g.dim{opacity:.46}g.highlight .node{stroke-width:2.8;fill-opacity:.1}
.takeaway{position:absolute;left:134px;right:134px;top:935px;margin:0;border-left:3px solid var(--context);padding:0 0 0 21px;font-size:27px;line-height:1.4}
.slide-footer{position:absolute;bottom:28px;left:134px;right:134px;border-top:1px solid var(--line);padding-top:15px;display:flex;align-items:center;justify-content:space-between;gap:30px;color:var(--muted);font-size:17px}.page-count{color:var(--text);font-size:21px;margin-right:20px}.version{margin-left:16px}.controls{display:flex;align-items:center;gap:10px}.controls button{border:1px solid var(--line);background:transparent;color:var(--muted);height:37px;min-width:37px;border-radius:5px;font-size:17px}.controls button.current{background:#223151;border-color:var(--model);color:var(--text)}.controls button:hover{border-color:var(--model);color:var(--text)}.controls .prev,.controls .next{padding:0 12px}.step-label{min-width:185px;text-align:right;font-size:16px}.sources{background:transparent;border:0;padding:0;color:var(--muted);text-decoration:underline;text-underline-offset:4px;font-size:17px}.key-hint{position:fixed;left:12px;top:8px;color:#9EACC8;font-size:11px;z-index:5;opacity:0;transition:opacity .2s}body:hover .key-hint{opacity:1}.sr-only{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0,0,0,0)}
@media print{.controls,.sources,.key-hint,.sr-only{display:none!important}.slide-footer{bottom:28px}.slide [data-focus]{opacity:1!important}@page{size:20in 11.25in;margin:0}}
@media(prefers-reduced-motion:reduce){.slide,g[data-focus]{transition:none!important}}
'''