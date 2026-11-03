"""Final 42-slide speaking deck. Input: final blueprint, not the comparison report."""
from pathlib import Path
from html import escape
import base64
import hashlib
import json
import re
import runpy

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
BLUEPRINT = PROJECT / '2_2차_세미나_최종_slide_blueprint.md'
source = BLUEPRINT.read_text(encoding='utf-8')
example = runpy.run_path(str(ROOT / 'artwork.py'))
text, box, arrow, group = (example[n] for n in ('text','box','arrow','group'))
colors = example['C']
existing = {s['id']:s.copy() for s in example['slides']}
specs = dict(re.findall(r'^## (S\d{2}) — (.*?)(?=^## S\d{2} — |^# C\.)', source, re.M | re.S))
references = {key:(label,url) for key,label,url in re.findall(r'^\| ([HCPV]\d{2}) \| \[([^]]+)\]\(([^)]+)\)',source,re.M)}
sections = {key:value.strip() for key,value in re.findall(r'^# ([C-G])\. (.*?)(?=^# [A-G]\. |\Z)',source,re.M|re.S)}
slides = {}

def add(number,title,sub,diagram,take,steps,kind='content-slide',extra_note=''):
    ident=f'S{number:02}'
    spec=specs[ident]
    section=re.search(r'\*\*섹션·우선순위:\*\* (.*?) ·',spec).group(1).rstrip('.')
    refs=list(dict.fromkeys(re.findall(r'\[([HCPV]\d{2})\]',spec)))
    version=('Hermes v0.22.5' if 4<=number<=15 else 'PydanticAI v2.61.0' if 20<=number<=38 else '공식 공개 동작' if 16<=number<=19 else 'Seminar 02')
    if number in (7,9,10,11,12,13): version='Hermes · 공식 문서 기준'
    if number in (30,31,32,33,34): version='PydanticAI · 현행 문서 / 버전 대조'
    if number in (15,38): version='실행 관찰 안내 · 실제 Demo 별도'
    if number in (43,44): version='운영·검증 설계 예시'
    slides[ident]=dict(id=ident,title=title,sub=sub,diagram=diagram,take=take,
        steps=['전체 구성']+steps,section=section,version=version,kind=kind,
        note=spec.strip()+'\n\n'+extra_note,sources=[(k,*references[k]) for k in refs if k in references],
        demo=('hermes' if number==15 else 'pydanticai' if number==38 else None))

def rule(x1,y1,x2,y2,color='line',dash=False):
    return f'<path d="M{x1} {y1} H{x2}" fill="none" stroke="{colors[color]}"/>' if y1==y2 else f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{colors[color]}"'+(' stroke-dasharray="7 7"' if dash else '')+'/>'

def label(x,y,name,desc,color='context',size=31):
    return text(x,y,name,size,color,700)+''.join(text(x,y+47+i*34,line,24,'muted') for i,line in enumerate(desc.split('|')))

def table(headers,rows,widths=None,y=45,row_h=126):
    widths=widths or [1652//len(headers)]*len(headers)
    out='';x=0
    for h,w in zip(headers,widths):out+=text(x+18,y,h,25,'muted');x+=w
    out+=rule(0,y+24,1652,y+24)
    for r,row in enumerate(rows):
        x=0;top=y+26+r*row_h;part=''
        for c,(cell,w) in enumerate(zip(row,widths)):
            for j,line in enumerate(cell.split('|')):part+=text(x+18,top+46+j*33,line,27 if c==0 else 24,'context' if c==0 else 'text',700 if c==0 else 400)
            x+=w
        part+=rule(0,top+row_h,1652,top+row_h)
        out+=group(r+1,part)
    return out

def chain(items,y=175,w=340,gap=90,h=140,start=0):
    out=''
    for i,(name,desc,color) in enumerate(items):
        x=start+i*(w+gap)
        out+=group(i+1,box(x,y,w,h,name,desc,color))
        if i<len(items)-1:out+=arrow(f'M{x+w} {y+h/2} H{x+w+gap-12}',color)
    return out

def code_panel(x,y,w,h,code,caption='실제 API 축약 · 앱 정의/연결 설정은 노트 참고',size=23):
    out=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#080d19" stroke="#33415D"/>'
    out+=text(x+25,y+38,caption,21,'muted')+rule(x,y+60,x+w,y+60)
    for i,line in enumerate(code.splitlines()):
        col='muted' if line.strip().startswith('#') else 'runtime' if line.strip().startswith('@') else 'model' if line.strip().startswith(('from ','import ','async def','def ','class ')) else 'text'
        out+=f'<text class="code-line" x="{x+25}" y="{y+103+i*34}" font-size="{size}" fill="{colors[col]}">{escape(line)}</text>'
    return out

def lane_title(x,y,title,sub,color='runtime'):
    return text(x,y,title,31,color,700)+text(x,y+42,sub,24,'muted')

def frame(x,y,w,h,label_,color='runtime'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{colors[color]}" fill-opacity=".018" stroke="{colors[color]}" stroke-opacity=".65" stroke-dasharray="7 7"/>'+text(x+22,y+36,label_,22,color)

# === OPENING: distinct greeting / title / roadmap ===
d=text(826,180,'다시 반갑습니다.',76,'text',700,'middle')+text(826,263,'Agent Framework 세미나 · 2차',32,'muted',400,'middle')+text(826,325,'실행 구조와 개발 책임',28,'context',400,'middle')
d+=rule(1235,485,1385,555)+rule(1385,555,1510,470)
for x,y,c in [(1235,485,'model'),(1385,555,'runtime'),(1510,470,'tool')]:d+=f'<circle cx="{x}" cy="{y}" r="12" fill="{colors[c]}"/>'
add(0,'다시 반갑습니다.','Agent Framework 세미나 · 2차',d,'실행 구조와 개발 책임',[],kind='opening')
d=label(0,125,'AGENT FRAMEWORK','', 'muted',27)+text(0,232,'Inside the',70,'text',700)+text(0,318,'Implementations',70,'text',700)+text(0,397,'같은 구성요소, 서로 다른 실행 책임',30,'muted')
d+=f'<circle cx="1315" cy="300" r="210" fill="none" stroke="{colors["runtime"]}" stroke-width="2"/>'
d+=group(1,box(1128,115,370,105,'Model','판단·응답','model')+box(1128,390,370,105,'Runtime','반복·상태·정책','runtime')+arrow('M1503 230 C1600 300 1580 365 1503 390','tool')+text(1580,333,'Tool',25,'tool',700)+arrow('M1128 390 C1030 330 1030 270 1128 220','context'))
add(1,'이제 실제 구현을 들여다봅니다','개념의 합의에서, 실제 동작과 책임의 경계로',d,'무엇을 제공받고, 무엇을 직접 만드는가?',['Runtime의 책임'],kind='title')
d=chain([('1차 · 공통 개념','Core · Tools|Orchestration','muted'),('2차 · 기술별 구조','실행·상태·정책|이번 발표','runtime'),('3차 · 개발·적용','실제 Agent|업무 검증·회고','muted')],y=95,w=480,gap=105,h=190)
d+=group(2,box(585,355,480,135,'이 파트','Hermes · Claude Code · PydanticAI','runtime',29))
d+=group(3,frame(0,535,1650,100,'다른 발표자', 'muted')+text(230,595,'LangChain / LangGraph',26,'muted')+text(820,595,'Mistral AI Studio · vLLM / SGLang',26,'muted'))
add(2,'2차에서 맡는 범위','기초는 전제로 두고, 기술별 실행 구조를 살펴봅니다.',d,'서빙 엔진 내부와 실제 업무 적용은 다음 발표·3차로 연결한다.',['3회 로드맵','현재 파트','다른 발표자 경계'])
d=group(1,box(0,45,760,205,'Harness에서 출발','Hermes · Claude Code|갖춰진 실행환경에 기능을 연결','runtime',34))+group(2,box(890,45,760,205,'코드로 구성','PydanticAI|업무 계약·Tool·의존성을 정의','runtime',34))
d+=arrow('M380 250 V325 H825 V368','model')+arrow('M1270 250 V325 H825','model')
d+=box(450,378,750,110,'공통 모델 API','추론 서비스 → 모델','model')+text(825,585,'실행 루프는 양쪽 모두에 있다',34,'context',700,'middle')
add(3,'완성된 실행환경과 개발용 구성요소','제품의 우열보다, 개발을 시작하는 위치와 남는 책임을 비교합니다.',d,'Harness / SDK는 배타적인 제품 계급이 아닌 개발 출발점이다.',['Harness에서 출발','Python 코드로 구성'])

# === FIVE ACCEPTED DIAGRAMS: preserve their visual system and mechanics ===
for ident in existing:
    e=existing[ident]
    add(int(ident[1:]),e['title'],e['sub'],e['diagram'],e['take'],e['steps'][1:],extra_note=e['note'])

# === HERMES EXECUTION: sequence and branches ===
d=''
for x,name in [(120,'Entry'),(590,'AIAgent'),(1080,'Provider'),(1530,'Model')]:
    d+=text(x,36,name,29,'runtime' if name in ('Entry','AIAgent') else 'model',700,'middle')+rule(x,65,x,600,'line',True)
events=[(120,590,125,'Task 준비 · user append','runtime'),(590,1080,260,'Prompt / History · tools 준비','context'),(1080,1530,395,'API 형식으로 변환 · 모델 요청','model'),(1530,1080,530,'응답','model')]
for i,(a,b,y,t,c) in enumerate(events):
    d+=group(i+1,arrow(f'M{a} {y} H{b-12 if b>a else b+12}',c,label=t,lx=min(a,b)+25,ly=y-20))
d+=text(650,205,'압축 판단 · 호출별 정보 추가',24,'context')+text(650,337,'지원 Provider에서 cache marker',22,'muted')
add(5,'한 Turn을 실제 요청으로 만드는 경로','프레임워크 객체와 최종 API payload를 나눠서 봅니다.',d,'API 직전 입력에는 지침·이력·도구 스키마·일시 정보가 함께 들어간다.',['입력과 Task','Context 준비','Provider 변환','모델 응답'])
d=box(0,65,420,135,'모델 응답','Runtime이 응답을 분류','model')
d+=group(1,arrow('M420 130 H590 V95 H750','tool',label='Tool Calls',lx=475,ly=72)+box(760,35,650,135,'Tool 실행 → 결과 추가','다음 모델 호출로 진행','tool')+arrow('M1410 100 H1575 V290 H1480','context')+box(1060,240,410,100,'Context → 재요청','','context',27)+arrow('M1060 290 H210 V210','context'))
d+=group(2,arrow('M420 130 H590 V405 H750','success',label='최종 답변',lx=470,ly=389)+box(760,345,650,135,'응답·세션 저장 → 종료','모델의 완료 문장과 업무 성공은 별개','success'))
d+=group(3,text(0,575,'오류·중단·예산',28,'risk',700)+text(385,575,'Tool 오류 → 결과 메시지 / API 오류 → retry·fallback / 중단·예산 → 종료 경로',23,'muted'))
add(6,'응답 분기가 루프와 종료를 결정합니다','Tool 오류와 모델 API 장애는 서로 다른 복구 경로입니다.',d,'응답 종류·취소·실행 예산을 검사해 계속할지 멈출지 결정한다.',['Tool 경로','최종 답변 경로','오류·중단·예산'])

# === HERMES CONTEXT / MEMORY / SKILLS ===
d=text(0,35,'요청 A',26,'muted')+text(0,180,'요청 B',26,'muted')
for y in (70,215):
    d+=f'<rect x="0" y="{y}" width="1240" height="72" fill="#60A5FA" fill-opacity=".15" stroke="#60A5FA"/>'+f'<rect x="1240" y="{y}" width="412" height="72" fill="#FDBA74" fill-opacity=".09" stroke="#FDBA74"/>'
    d+=text(620,y+46,'동일한 앞부분 · 8,000 tokens',27,'model',700,'middle')+text(1446,y+46,'바뀐 2,000',26,'context',700,'middle')
d+=group(1,arrow('M620 142 V205','model')+text(0,350,'총 10,000 tokens · 설명용 수치',22,'muted'))
d+=group(2,chain([('Hermes','입력 순서·내용 구성','context'),('호환 endpoint','서빙 엔진의 캐시 판단','runtime'),('Model','KV 상태 + 신규 계산','model')],y=420,w=480,gap=105,h=155))
add(8,'Prefix 재사용은 서빙 계층의 일입니다','같은 앞부분의 중간 계산을 재사용합니다. 입력 길이가 줄어드는 것은 아닙니다.',d,'Context 구성과 캐시 적중은 서로 다른 책임이다.',['동일 prefix','서빙 계층의 계산 재사용'])
d=lane_title(0,35,'Before','누적된 대화·Tool 결과','context')+lane_title(920,35,'After','요약 + 최근 문맥 + Tool 쌍','context')
for y,title_,sub_,c in [(125,'오래된 대화','이미 처리한 결정·관찰','muted'),(285,'Tool Call + Tool Result','대응 ID가 있는 실행 기록','tool'),(445,'최근 대화','현재 요청·미해결 항목','context')]:d+=box(0,y,680,130,title_,sub_,c)
d+=group(1,arrow('M700 335 H880','context'))
d+=group(2,box(920,125,730,130,'요약과 보존 근거','중요 사실·결정·원본 경로','context')+box(920,285,730,130,'Call / Result 쌍 유지','한쪽만 남기는 축약은 피한다','tool')+box(920,445,730,130,'최근 문맥 유지','현재 작업을 이어갈 정보','context'))
d+=text(0,636,'발동 위치: Tool loop 안 / Gateway의 Turn 전 위생 처리',23,'muted')
add(9,'압축은 실행 이력의 정합성도 지켜야 합니다','단순히 오래된 텍스트를 자르는 작업으로 이해하면 안 됩니다.',d,'압축 임계값과 보존 범위는 실제 모델·설정 조건을 확인한다.',['압축 판단','보존과 축약'])
d=group(1,box(0,80,410,175,'Memory 파일','MEMORY.md|USER.md','context')+box(620,30,460,135,'세션 A 시작','System Prompt snapshot','context')+arrow('M410 130 H510 V95 H610','context',label='읽기',lx=457,ly=75))
d+=group(2,box(620,250,460,135,'세션 A 도중','memory Tool로 파일 갱신','tool')+arrow('M620 320 H215 V265','tool',label='저장',lx=385,ly=300)+text(1150,315,'현재 system snapshot은',25,'muted')+text(1150,355,'자동 교체되지 않음',29,'risk',700))
d+=group(3,box(620,490,460,135,'세션 B 시작','갱신된 파일의 새 snapshot','context')+arrow('M215 255 V555 H610','context',label='다음 세션에서 읽기',lx=240,ly=533))
add(10,'Memory 파일과 지금 보는 기억은 다릅니다','파일 저장·현재 세션의 snapshot·다음 세션 반영을 나눠서 봅니다.',d,'저장 성공이 현재 System Prompt의 즉시 교체를 뜻하지 않는다.',['세션 시작 snapshot','실행 도중 write','다음 세션 반영'])
d=table(['정보 계층','저장·접근','모델 입력으로 들어오는 방식'],[
('Built-in Memory','MEMORY.md / USER.md','세션 시작 snapshot'),
('Session History','state.db · SQLite / FTS5','session_search로 선택한 기록'),
('External Provider','별도 저장소·Plugin','확장 구현의 조회·주입')],widths=[425,590,637],y=45,row_h=136)
d+=text(0,586,'정확한 장비 ID 질의와 표현이 달라진 사례 질의를 나눠 평가한다.',27,'context',700)
add(11,'Session 검색은 전체 Memory의 대체물이 아닙니다','저장된 사실·과거 대화·외부 확장은 수명과 검색 방식이 다릅니다.',d,'전체 DB가 자동 주입되는 것이 아니라 필요한 기록을 선택한다.',['기억 snapshot','과거 대화 검색','외부 확장'])
d=chain([('인덱스','이름·설명으로 후보 탐색','context'),('SKILL.md','선택한 절차 본문 로딩','context'),('참고 자료','필요한 파일·스크립트','tool')],y=60,w=480,gap=105,h=160)
d+=group(4,code_panel(0,315,710,290,'wafer-anomaly-review/\n  SKILL.md\n  references/\n  scripts/','문서형 절차 패키지',25)+text(850,345,'유지 관리',30,'runtime',700)+text(850,408,'skill_manage · 생성·수정·삭제',27,'text')+text(850,480,'Curator',29,'runtime',700)+text(850,535,'active → stale → archived',29,'context')+text(850,590,'Agent 생성 Skill의 사용 이력 기반',23,'muted'))
add(12,'Skill은 필요할 때 읽고 유지 관리합니다','실제 실행은 Tool이 맡고, Skill은 절차와 자료를 제공합니다.',d,'생성된 절차가 재사용되므로 근거·검토·버전 관리가 필요하다.',['목록','본문','지원 파일','Skill 유지 관리'])
d=chain([('등록','Registry · handler','tool'),('모델에 공개','활성 schema 목록','context'),('실행','이름으로 dispatch','runtime')],y=55,w=480,gap=105,h=140)
d+=group(4,box(0,320,480,160,'Local Tool','앱 함수·실행 handler','tool')+box(585,320,480,160,'MCP 연결','Client ↔ 외부 Server','tool')+box(1170,320,480,160,'Plugin','Tool · Hook · 명령 등록','runtime'))
d+=text(0,585,'memory / delegate_task 등 Agent 상태 도구에는 별도 처리 경로가 있을 수 있다.',26,'context')
add(13,'도구 등록·외부 연결·확장 Hook은 다른 접점입니다','Schema 준비와 실제 실행을 연결하되, 확장 지점을 구별합니다.',d,'단일 중앙 Hook이 모든 내부 실행을 관찰한다고 단정하지 않는다.',['등록','모델 노출','dispatch','로컬·MCP·Plugin'])

# === POLICY GATE AND DEMO 1 ===
d=chain([('입력 경계','사용자·세션 확인','runtime'),('실행 정책','명령·파일·인자 검사','runtime'),('승인','smart / manual / off','context'),('실행환경','OS · DB · Sandbox','tool')],y=65,w=345,gap=90,h=160)
d+=group(5,box(0,345,760,165,'패턴 탐지 + 실제 권한','위험 탐지와 접근 제어를 함께 사용|무인 실행의 deny 정책 별도','risk')+box(890,345,760,165,'복구 Checkpoint','opt-in · 지원 범위에 따른 복구|외부 변경 전체 rollback은 아님','context'))
d+=text(0,603,'Demo 1',30,'runtime',700)+text(210,603,'Context → Tool → 세션·기억 저장',29,'text')
add(15,'정책 경계를 확인하고 Hermes Demo로 갑니다','행동의 허가와 실행 자원·복구는 서로 다른 통제 계층입니다.',d,'실제 실행 기록에서 Context·Tool·저장 상태를 확인한다.',['입력 경계','실행 정책','승인','실행환경','별도 실행 관찰'])

# === CLAUDE CODE: architecture, memory, communications ===
d=group(1,box(0,70,350,130,'사용자·프로젝트','지시·파일·대화','context')+arrow('M350 135 H450','context')+frame(460,20,1190,400,'Claude Code · 공개 동작 계약','runtime')+box(510,110,600,170,'Runtime','Gather ↔ Act ↔ Verify|도구·Context·권한을 관리','runtime')+box(1230,110,370,170,'Model','행동 선택·응답','model')+arrow('M1110 155 H1220','model')+arrow('M1230 230 H1120','model'))
d+=group(2,box(460,490,350,130,'Tools','Read · Bash · Edit','tool')+box(880,490,350,130,'지시·기억','프로젝트·Auto Memory','context')+box(1300,490,350,130,'정책·Subagents','권한·위임 설정','runtime')+arrow('M635 420 V480','tool')+arrow('M1055 490 V430','context')+arrow('M1475 420 V480','runtime'))
add(16,'Claude Code도 Harness에서 출발합니다','맥락 수집·행동·검증이 섞여 진행되는 실행환경입니다.',d,'공개 인터페이스를 비교하며, 비공개 엔진의 내부 구현을 창작하지 않는다.',['전체 아키텍처','실행·정보·정책 경계'])
d=table(['제품','사람이 작성하는 지시','Agent가 관리하는 기억'],[
('Hermes','SOUL · 프로젝트 지침','MEMORY.md / USER.md|세션 snapshot'),
('Claude Code','CLAUDE.md|필요시 @AGENTS.md import','Auto Memory 인덱스|필요시 세부 파일 읽기')],widths=[320,650,682],y=65,row_h=185)
d+=text(0,575,'지침 파일은 행동을 안내하고, 실제 접근 권한은 실행 계층에서 집행한다.',28,'context',700)
add(17,'프로젝트 지시와 Auto Memory를 분리합니다','파일 이름이 같아도 제품별 저장·로드 정책은 다릅니다.',d,'지시와 기억은 실제 파일·DB·네트워크 접근 권한을 대신하지 않는다.',['Hermes','Claude Code'])
d=lane_title(0,30,'Subagent','부모의 위임을 수행하고 결과를 반환','runtime')+lane_title(890,30,'Agent Teams','독립 세션·공유 작업·직접 메시지','runtime')
d+=group(1,box(190,125,390,110,'메인 Agent','','runtime')+box(0,345,340,145,'검토자 A','온도 데이터|독립 Context','runtime')+box(430,345,340,145,'검토자 B','압력 데이터|독립 Context','runtime')+arrow('M285 235 V280 H170 V335','runtime')+arrow('M485 235 V280 H600 V335','runtime')+arrow('M340 410 H365 V245','context')+arrow('M430 410 H405 V245','context')+text(175,590,'결과는 부모에게 보고',25,'context'))
d+=group(2,box(1085,125,390,110,'팀 리더','','runtime')+box(890,345,340,145,'세션 A','독립 Context','runtime')+box(1310,345,340,145,'세션 B','독립 Context','runtime')+arrow('M1280 235 V280 H1060 V335','runtime')+arrow('M1280 280 H1480 V335','runtime')+arrow('M1230 392 H1300','tool')+arrow('M1310 444 H1240','tool')+text(1268,322,'직접 메시지',21,'tool',400,'middle')+text(890,590,'공유 작업 목록 · 실험적 제약 · 조정 비용',25,'context'))
add(18,'Subagent 반환과 Team 협업은 다릅니다','누가 누구에게 결과를 전달하고, 다음 행동을 결정하는지 봅니다.',d,'Context 분리와 실제 자원 격리·협업 충돌 관리는 별개다.',['부모로 반환','팀원 간 협업'])
d=table(['제품·입구','명령','바뀌는 상태'],[
('Hermes CLI','hermes sessions refresh-prompts|--session SESSION_ID','저장된 Prompt 갱신 경로'),
('Hermes Slash','/memory pending','보류된 기억 쓰기 검토'),
('Claude Code','/resume · /compact','대화 선택 · Context 압축')],widths=[350,730,572],y=60,row_h=145)
add(19,'Slash command는 실행 상태를 조작하는 입구입니다','명령을 실행하지 않고, 그 뒤에 있는 상태 관리 기능을 비교합니다.',d,'재개·Prompt 갱신·Memory 검토를 같은 동작으로 합치지 않는다.',['세션·Prompt','기억 검토','대화·압축'])

# === PYDANTICAI: core / harness and master architecture ===
d=group(1,box(0,375,720,150,'Pydantic','Python 값·스키마·검증','context',33))
d+=group(2,box(220,205,720,145,'PydanticAI Core','Agent · Tool · Output · 실행 Graph','runtime',33)+arrow('M360 375 V360','runtime'))
d+=group(3,box(440,35,720,145,'선택적 Harness','Memory · Skills · 동작 조합','runtime',33)+arrow('M580 205 V190','runtime'))
d+=text(1260,90,'함께 연결하는 도구',25,'muted')+label(1260,170,'pydantic-graph','명시적 Graph·Workflow','runtime',27)+label(1260,300,'Evals / Logfire','평가와 실행 관찰','context',27)+label(1260,430,'Provider / Model','모델 추론은 외부 계층','model',27)
add(20,'Pydantic → PydanticAI → 선택적 Harness','값의 검증에서 실행 엔진으로, 필요한 기능을 조합하는 구조로 확장합니다.',d,'Core만으로 Agent를 만들 수 있고 Harness는 선택적으로 추가한다.',['값의 계약','실행 엔진','선택 확장'])
d=group(1,box(0,0,590,115,'Python 애플리케이션','Agent · Tools · output_type','runtime')+box(650,0,410,115,'실행 시 Deps','인증 정보 · DB 객체','context')+box(1180,0,470,115,'Provider / Model','실제 추론은 외부 계층','model'))
d+=frame(0,160,1650,415,'PydanticAI Core · 내부 Graph와 실행 접점','runtime')
d+=group(2,box(30,255,410,130,'UserPromptNode','입력·이력 준비','context')+box(530,255,470,130,'ModelRequestNode','요청 구성·모델 호출','model')+box(1090,255,530,130,'CallToolsNode','Tool / Output 분류','runtime')+arrow('M440 320 H520','context')+arrow('M1000 320 H1080','model')+arrow('M1355 385 V435 H765 V395','tool',label='Tool 실행 결과 → 다음 요청',lx=555,ly=467))
d+=group(3,arrow('M765 255 V215 H1415 V125','model')+text(795,198,'모델 요청',23,'model')+text(40,535,'Capabilities: Run · Model · Tool · Output 실행 지점에 개입',25,'runtime')+text(0,635,'연결: History 저장소 / Tool 서비스 / Output 검증 / 선택 Harness',26,'context'))
add(21,'PydanticAI 전체 아키텍처','개발자 정의와 SDK가 실행하는 Graph를 분리해서 봅니다.',d,'내부 Graph는 pydantic-graph이며, 업무 데이터·권한·저장은 앱과 연결한다.',['개발자 정의','내부 실행 Graph','외부 연결과 확장'])
d=code_panel(0,35,1040,555,"agent = Agent(model, deps_type=DemoDeps,\n    instructions='도구 근거로만 답하라.')\n\n@agent.tool\nasync def get_bin_summary(\n    ctx: RunContext[DemoDeps], lot_id: str\n) -> dict:\n    return await ctx.deps.query(lot_id)\n\nresult = await agent.run(\n    'LOT-DEMO의 BIN-X를 조회해줘', deps=deps)",size=23)
d+=group(1,box(1150,35,500,135,'Agent 정의','지침·Tools·결과 계약','runtime'))+group(2,box(1150,230,500,135,'앱 Tool 구현','조회·계산·업무 인가','tool'))+group(3,box(1150,425,500,135,'실행 시 Deps','요청마다 자원·권한 주입','context'))
d+=arrow('M1400 170 V220','runtime')+arrow('M1400 365 V415','tool')
add(22,'개발자는 업무 계약과 Tool을 작성합니다','SDK의 루프를 다시 만들지 않고, 업무별 정의와 실행 함수를 연결합니다.',d,'query와 DemoDeps는 앱 코드이며, 실제 인가는 Tool·서비스에서 검사한다.',['Agent 정의','Tool 구현','Deps와 실행'])

# === INPUT BOUNDARIES / TOOL PIPELINE / CONCURRENCY ===
d=frame(0,0,1650,250,'모델 입력 레인','context')+group(1,box(30,75,450,135,'지시 + History','Instructions · System Prompt','context')+box(590,75,450,135,'Provider adapter','역할·Part를 API 형식으로','model')+box(1150,75,470,135,'Model 요청','이번 호출의 실제 입력','model')+arrow('M480 140 H580','context')+arrow('M1040 140 H1140','model'))
d+=frame(0,335,1650,285,'Python 실행 레인','runtime')+group(2,box(30,420,450,135,'Deps','tenant · DB client · 권한','runtime')+box(590,420,450,135,'Tool / Hook','서버 측 인가·조회','tool')+arrow('M480 485 H580','tool'))
d+=group(3,arrow('M1040 485 H1390 V260','context',label='선택한 지시·Tool 결과만 전달',lx=1060,ly=326)+text(65,602,'Deps 전체가 자동 전송되는 것은 아니다',23,'context'))
add(24,'지시·History·Deps는 같은 입력이 아닙니다','Python 자원과 모델에 전달하는 정보 사이의 경계를 명시합니다.',d,'인증 객체·DB 연결은 deps로 주입하되, Tool 결과의 정보 유출도 따로 검사한다.',['모델 입력','Python 자원','명시적인 정보 전달'])
d=chain([('함수·타입','Tool 정의','tool'),('Schema','모델에 공개','context'),('인자 검증','구조·업무 조건','runtime'),('실행','인가·승인 후','tool')],y=70,w=345,gap=90,h=145)
d+=group(5,table(['등록 방식','Python 실행 문맥','사용 예'],[
('@agent.tool','RunContext를 받음','tenant·DB·권한이 필요한 조회'),
('@agent.tool_plain','일반 인자','독립 계산·변환')],widths=[470,520,662],y=340,row_h=110))
add(25,'Tool은 스키마 준비·검증·실행을 거칩니다','모델에 보이는 함수 계약과 Python에서 실행하는 함수는 연결되지만 다릅니다.',d,'Toolset 노출 필터와 실제 실행 인가는 서로 다른 단계다.',['함수 정의','모델 노출','인자 검증','정책과 실행','tool / tool_plain'])
d=text(0,30,'모델이 제안한 순서',25,'muted')+text(400,30,'A · B → sequential Tool → C · D',29,'context',700)+text(0,130,'실제 실행',25,'muted')
for x,y,w,h,t,c in [(320,150,340,80,'A · 온도 조회','tool'),(320,260,250,80,'B · 압력 조회','tool'),(760,150,300,190,'Barrier','runtime'),(1160,150,390,80,'C · 후속 조회','tool'),(1160,260,300,80,'D · 후속 계산','tool')]:
    d+=group(1 if x==320 else 2 if x==760 else 3,box(x,y,w,h,t,'',c,27))
d+=arrow('M660 195 H750','tool')+arrow('M570 305 H700 V245 H750','tool')+arrow('M1060 245 H1100 V195 H1150','tool')+arrow('M1100 245 V305 H1150','tool')
d+=rule(310,405,1600,405)+arrow('M1550 405 H1640','line')+text(320,452,'시간 →',22,'muted')
d+=text(0,550,'async Tool: task 동시 스케줄',27,'model',700)+text(900,550,'sync Tool: worker thread',27,'runtime',700)+text(0,615,'sequential=True는 실행 장벽이며 데이터 snapshot·트랜잭션을 만들지는 않는다.',26,'context')
add(26,'병렬 실행은 의존성 없는 구간을 겹칩니다','앞 구간 완료 → barrier 단독 실행 → 뒤 구간 시작의 관계를 봅니다.',d,'병렬 조회도 같은 분석 대상·시점·snapshot 계약이 필요하다.',['독립 구간','실행 장벽','후속 구간'])

# === OUTPUT AND FAILURES ===
d=group(1,label(0,60,'ToolOutput','출력용 Tool Schema 제공|모델이 구조화 호출 생성','runtime',32))+group(2,label(585,60,'NativeOutput','Provider의 구조화 기능|모델·스키마 지원 확인','model',32))+group(3,label(1170,60,'PromptedOutput','형식 지시 + 파싱·검증|형식 위반은 수정 경로','context',32))
d+=rule(0,265,1652,265)
d+=group(4,chain([('Pydantic 검증','타입·필수 필드·범위','context'),('업무 Validator','근거·업무 규칙','runtime'),('실데이터 검증','계산·기간·증빙 일치','tool')],y=345,w=480,gap=105,h=155))
d+=text(0,610,'output_type은 최종 결과 계약 · 개별 Tool return type과 목적이 다르다',26,'muted')
add(27,'출력 형식과 결과의 정확성은 따로 검증합니다','Schema를 통과했다고 계산·인과·예측이 옳다는 뜻은 아닙니다.',d,'형식 통과와 도메인 정확성을 서로 다른 검증 기준으로 평가한다.',['ToolOutput','NativeOutput','PromptedOutput','검증의 층'])
d=table(['발생 위치','되돌리는 방식','별도 설계'],[
('인자·출력 오류','검증 실패 → 모델 수정 피드백','ModelRetry · 재시도 한도'),
('Provider/API 장애','429·5xx·연결 실패 → 통신 복구','백오프 · timeout · 중첩 retry'),
('업무 판단 실패','유효한 형식이어도 분석은 틀릴 수 있음','정답·평가·사람 검토')],widths=[390,700,562],y=60,row_h=145)
d+=text(0,605,'UsageLimits + 시간 제한 + Tool 부작용 중복 방지는 별도 관리',27,'context',700)
add(29,'Retry를 발생 위치별로 나눕니다','모델에게 수정시킬 문제와 통신 장애·업무 실패를 구별합니다.',d,'SDK·HTTP·프록시 retry가 겹치면 실제 wire 요청 수가 증폭될 수 있다.',['검증 실패','API 장애','업무 실패'])

# === EXTENSIONS / CONVERSATION / KNOWLEDGE ===
d=group(1,label(0,45,'Hook','모델 요청·Tool·Run의 실행 지점','runtime',34))+group(2,label(880,45,'Capability','지시·도구·Hook·설정을 묶는 기능','runtime',34))
d+=group(3,frame(0,220,1650,295,'A · 감사 wrapper','runtime')+frame(220,285,1210,160,'B · 정책 wrapper','context')+box(560,330,530,80,'core 실행','','tool',28))
d+=text(0,585,'A.enter → B.enter → core → B.exit → A.exit',31,'context',700)+text(0,640,'handler를 생략하는 wrapper는 안쪽 정책 Hook도 건너뛸 수 있다.',24,'risk')
add(30,'Hook을 기능 단위 Capability로 합성합니다','재사용 단위와 실행 순서, Run별 상태 수명을 함께 설계합니다.',d,'정책이 필요한 실행 접점과 wrapper의 우회 가능성을 검증한다.',['Hook 접점','기능 묶음','합성 순서'])
d=chain([('Run 1','typed messages · 결과','runtime'),('저장·로드','사용자별 Conversation','context'),('Run 2','이전 이력을 전달','runtime')],y=65,w=480,gap=105,h=160)
d+=group(4,code_panel(0,340,1070,230,"first = await agent.run('BIN-X를 조회해줘')\nsecond = await agent.run(\n    '분모는?', message_history=first.all_messages())",size=24)+label(1170,375,'함께 이어갈 상태','history · usage · ID|현행 conversation API','context',29))
add(31,'여러 Run의 대화는 명시적으로 이어 붙입니다','Agent 객체를 재사용하는 것과 사용자 대화를 복원하는 것은 다릅니다.',d,'앱이 인증·저장·동시 갱신·TTL과 대화 누적 예산을 관리한다.',['첫 Run','저장 수명','다음 Run','이력 전달 API'])
d=group(1,box(0,50,760,150,'Core','Provider-native compaction|지원 모델·API 조건 필요','runtime')+box(890,50,760,150,'별도 Harness','clear · sliding window · summarize|모델 비종속 전략 선택','runtime'))
d+=group(2,box(0,335,420,150,'원본 보관','별도 감사·저장 정책','context')+box(600,335,470,150,'Run History','축약이 다음 단계에 유지될 수 있음','context')+box(1245,335,405,150,'모델 요청','이번 호출의 입력','model')+arrow('M420 410 H590','context',label='선택·변환',lx=445,ly=388)+arrow('M1070 410 H1235','model'))
d+=text(0,610,'Tool 쌍·정확 수치·근거 경로를 보존하고 원본 복원을 자동 보장하지 않는다.',26,'context')
add(32,'압축 전략은 제공되지만 보존 정책은 설계합니다','모두 직접 구현할 필요는 없지만, 요청 축약과 원본 저장은 구별해야 합니다.',d,'vLLM 이관 기본 경로는 Provider 전용 compaction에 의존하지 않는다.',['제공 계층','원본과 Run history'])
d=group(1,box(0,65,450,150,'앱이 결정한 namespace','인증된 사용자·Agent 범위','runtime')+arrow('M450 140 H590','context')+box(600,65,470,150,'Memory capability','제한된 주입 · 필요시 검색','context')+arrow('M1070 140 H1235','context')+box(1245,65,405,150,'모델 Context','선택한 지속 사실','model'))
d+=group(2,box(600,385,470,160,'Memory Store','파일 · 메모리 · DB 등|정책에 맞게 선택','context')+arrow('M760 385 V225','context',label='읽기·검색',lx=520,ly=302)+arrow('M930 215 V375','tool',label='Memory Tool write',lx=952,ly=304))
d+=text(0,620,'namespace는 저장 범위이며, 인증·DB 접근 권한을 대신하지 않는다.',27,'risk')
add(33,'Harness Memory는 저장·주입·검색을 묶습니다','대화 이력과 다른 수명의 정보를 다루는 선택 확장입니다.',d,'무엇을 기억하고 누가 읽고 갱신할지, SOP 만료 정책까지 정한다.',['범위와 주입','읽기·검색·저장'])
d=lane_title(0,30,'Skills','문서형 절차를 모델 입력에 제공','context')+lane_title(0,355,'MCP','외부 기능의 발견·호출을 연결','tool')
d+=group(1,chain([('Skill library','디렉터리 scan','context'),('목록','이름·설명 노출','context'),('load_capability','선택한 본문 로딩','context')],y=100,w=480,gap=105,h=140))
d+=group(2,chain([('MCP Client','접속·인증','runtime'),('Tool 발견','외부 schema','tool'),('MCP Server','실행·반환','tool')],y=425,w=480,gap=105,h=140))
add(34,'Skill 로딩과 MCP 호출을 따로 연결합니다','기본 추상화가 제공되어도 실제 절차·서버·인증은 구성해야 합니다.',d,'Skill은 입력 경로, MCP는 외부 Tool 실행 연결 경로다.',['Skill 로딩','MCP 호출'])

# === ORCHESTRATION: four distinct control contracts ===
d=rule(826,0,826,650)+rule(0,320,1652,320)
d+=group(1,lane_title(0,35,'도구 내부 위임','부모 → tool(B.run) → 부모','runtime')+box(0,140,250,95,'부모 A','','runtime',27)+box(430,140,340,95,'자식 B','','runtime',27)+arrow('M250 170 H420','runtime',label='작업 위임',lx=275,ly=145)+arrow('M430 218 H260','context',label='결과 반환',lx=280,ly=270))
d+=group(2,lane_title(885,35,'Programmatic Handoff','앱 코드가 다음 Agent를 선택','runtime')+box(885,140,290,95,'앱 Router','','runtime',27)+box(1310,140,340,95,'다음 Agent','','runtime',27)+arrow('M1175 187 H1300','runtime'))
d+=group(3,lane_title(0,375,'Graph Workflow','노드·상태·분기를 명시','runtime')+box(0,475,250,95,'Node A','','runtime',27)+box(430,475,340,95,'Node B','','runtime',27)+arrow('M250 522 H420','runtime',label='조건·상태',lx=275,ly=496))
d+=group(4,lane_title(885,375,'Harness Subagents / Advisor','하위 작업과 조언을 역할별로 구성','runtime')+box(885,475,290,95,'실행 Agent','','runtime',27)+box(1310,475,340,95,'Advisor','','model',27)+arrow('M1175 502 H1300','model')+arrow('M1310 548 H1185','context'))
add(35,'위임·라우팅·Graph·Advisor의 제어권','다음 행동 주체와 반환 위치, 공유 상태를 구분합니다.',d,'delegation은 부모 반환 패턴이며 다른 SDK의 native handoff API와 동일하지 않다.',['부모 반환','코드 라우팅','명시적 Graph','Subagents와 조언'])
d=frame(0,0,1650,250,'SDK 실행','runtime')+frame(0,340,1650,280,'호스트 · 승인 UI / 정책 handler','context')
d+=group(1,box(30,80,470,135,'승인 필요한 Tool','requires_approval','tool')+box(650,80,970,135,'DeferredToolRequests','검증된 인자 + Tool Call ID','runtime')+arrow('M500 147 H640','runtime'))
d+=group(2,arrow('M1135 215 V410','context',label='미해결 호출 반환·보존',lx=1170,ly=316)+box(650,420,970,135,'승인 또는 거절','검토한 인자·보고서 버전과 연결','context'))
d+=group(3,box(30,420,470,135,'재개 · 결과 반영','DeferredToolResults','runtime')+arrow('M650 487 H510','context')+arrow('M265 420 V225','runtime',label='승인: 실행 인가 후 실행',lx=290,ly=302)+text(30,645,'거절: Tool을 실행하지 않고 거절 결과를 모델에 전달',23,'risk'))
add(36,'승인은 보류 Call을 해결하고 재개하는 계약입니다','승인 플래그만으로 업무 UI나 인증·영속 복구가 완성되지는 않습니다.',d,'Call ID·검토한 인자·데이터 버전을 묶고 실행 시 권한을 다시 검사한다.',['호출 보류','호스트의 승인·거절','결과 연결·재개'])
d=table(['책임','Core','선택 Harness','우리 애플리케이션'],[
('실행','Loop · Tools · Output','동작 스택·위임','업무 함수·종료 기준'),
('정보','메시지·이력 API','Memory · Skills','데이터 계약·보존·삭제'),
('통제','검증·Hook·승인 경로','정책 조합','인증·인가·감사·운영')],widths=[250,450,450,502],y=55,row_h=145)
d+=text(0,610,'Logfire / OTel은 실행 관찰, Evals는 목표 기준 평가에 연결한다.',25,'context')
add(37,'Core에 Harness를 더해도 업무 책임은 남습니다','제공받는 실행 접점과 직접 설계할 업무 계약을 함께 봅니다.',d,'이점은 타입 문법을 넘어 검증·실행·최종화·재개를 같은 Runtime에서 조합하는 데 있다.',['실행 책임','정보 책임','통제 책임'])
d=group(1,code_panel(0,60,440,480,'Agent(...)\n\n@agent.tool\n...\n\nagent.run(...)','개발자 코드',25))
d+=group(2,box(610,65,470,145,'입력 준비','UserPromptNode','context')+box(610,275,470,145,'요청 → 분류','ModelRequest / CallTools','runtime')+arrow('M845 210 V265','runtime'))
d+=group(3,box(1250,65,400,145,'요청 JSON','실제 모델 입력','model')+box(1250,275,400,145,'Tool 결과','인자·검증·반환','tool')+arrow('M1080 137 H1240','model')+arrow('M1080 347 H1240','tool'))
d+=text(0,590,'Demo 2',31,'runtime',700)+text(210,590,'Core 먼저 → 선택 Harness의 변화 관찰',29,'context',700)
add(38,'코드와 내부 전이를 PydanticAI Demo에서 잇습니다','최종화 정책 시험은 live 응답과 구별된 고정 응답 시험으로 관찰합니다.',d,'실제 코드 정의가 Graph·최종 입력·Tool 결과로 이어지는 경로를 본다.',['정의 코드','내부 전이','실제 요청·결과'])

# === OPERATIONS AND WRAP-UP ===
d=lane_title(0,30,'중앙 Agent 실행','공통 운영 + 사용자·작업 격리','runtime')+lane_title(890,30,'사용자 로컬 실행','설치·업데이트 + 로컬 실행 권한','runtime')
d+=group(1,box(0,125,760,120,'Client → API / Queue','인증·tenant·세션 순서','runtime')+arrow('M380 245 V290','runtime')+box(0,300,760,130,'Agent Workers','Tool / DB · 작업 수명·예산','runtime'))
d+=group(2,box(890,125,760,120,'Desktop Agent','서명된 배포·업데이트·정책 버전','runtime')+arrow('M1270 245 V290','tool')+box(890,300,760,130,'로컬 Tools / 저장소','사용자 파일·실행 계정 권한','tool'))
d+=group(3,arrow('M380 430 V490 H825 V530','model')+arrow('M1270 430 V490 H825','model')+box(460,540,730,100,'공통 모델 서비스 · 부하·접근 제어','','model',29))
add(43,'중앙 실행과 로컬 실행은 책임 배치가 다릅니다','Agent 실행 자원과 모델 서빙 자원을 분리해서 측정합니다.',d,'로컬 Agent여도 모델 요청으로 데이터가 나가므로 데이터 경로를 검토한다.',['중앙형','로컬형','공통 모델 서비스'])
d=lane_title(0,35,'Trace · 무엇이 실행되었나','관찰 가능한 실행 증거','runtime')+lane_title(890,35,'Evaluation · 옳게 수행했나','업무 목표와 제약 기준','context')
d+=group(1,box(0,150,760,380,'실행 기록','Run / Request / Call ID|실제 인자·Tool 결과|승인·재개·오류 경로|사용한 데이터 snapshot','runtime'))
d+=group(2,box(890,150,760,380,'업무 검증','분자·분모·기간 일치|근거·SOP revision 확인|승인 인자와 실행 일치|예측 시간 분할·누수 확인','context'))
d+=text(0,620,'같은 Tool을 호출했다는 사실만으로 같은 근거·같은 결과를 보장하지 않는다.',26,'muted')
add(44,'분석에 필요한 검증 기준을 정합니다','실행 증거와 계산·근거·정책 충족 여부를 연결합니다.',d,'조회·관측·원인 가설·예측을 구분하고 실측 없이 성능을 주장하지 않는다.',['실행 증거','업무 검증'])
d=''
for i,(title_,desc,col) in enumerate([
('Hermes','상태·기억·정책이 실제로 어떻게 움직이는가','runtime'),
('PydanticAI','검증·실행·최종화·확장을 어떻게 조합하는가','runtime'),
('우리의 계약','데이터·권한·업무 검증을 어떻게 보장하는가','context')]):
    y=75+i*170
    d+=group(i+1,text(0,y+25,str(i+1).zfill(2),31,col,700)+text(120,y+25,title_,36,col,700)+text(120,y+86,desc,29,'text')+rule(120,y+125,1652,y+125))
add(45,'제공받는 실행과 직접 만드는 계약','프레임워크 선택은 실행 책임을 나누는 결정입니다.',d,'다음 발표와 3차에서는 실제 Agent를 만들고 이 계약으로 검증한다.',['Hermes의 실제 구조','PydanticAI의 조합','업무 계약'])

# === USER EDITORIAL REVISION: stable IDs, updated copy and section opener ===
from revision import apply, LIGHT_STYLE
apply(slides, globals())
from hermes_revision import revise, HERMES_ORDER, CHAPTERS
revise(slides, globals())
from design import refine, STYLE as DESIGN_STYLE
refine(slides, globals())
expected=['S00','S01','S02','S03','S03H']+HERMES_ORDER+[f'S{i:02}' for i in range(16,46) if i not in range(39,43)]
assert set(slides)==set(expected) and len(expected)==len(set(expected)), (set(expected)-set(slides),set(slides)-set(expected))
ordered=[slides[k] for k in expected]

# === SVG: unique marker IDs, role names retained across shared diagrams ===
def diagram_svg(s):
    ident=s['id']
    defs=''.join(f'<marker id="{ident}-{k}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="{v}"/></marker>' for k,v in colors.items())
    body=s['diagram'].replace('url(#',f'url(#{ident}-')
    body=re.sub(r'(<text[^>]*>)(UserPromptNode|ModelRequestNode|CallToolsNode|Prompt / Compression|Provider adapter|Tool dispatch)(</text>)',lambda m:f'<g data-node-key="{escape(m[2])}">{m[0]}</g>',body)
    return f'<svg viewBox="0 0 1652 650" role="img" aria-labelledby="{ident}-title {ident}-desc"><title id="{ident}-title">{escape(s["title"])}</title><desc id="{ident}-desc">{escape(s["sub"])}</desc><defs>{defs}</defs>{body}</svg>'

# === OUTSIDE-THE-STAGE CHROME, INSIDE-THE-STAGE PRESENTATION ===
style=example['style']+r'''
/* === FULL-DECK EXTENSIONS: preserve example tokens and diagram frame === */
.controls .jump-number{width:48px;height:35px;background:transparent;border:1px solid var(--line);color:var(--text);font:17px 'Seminar Korean';border-radius:5px;text-align:center;-moz-appearance:textfield}.jump-number::-webkit-inner-spin-button{appearance:none}.jump-total{font-size:17px}.controls .menu{font-size:16px;padding:0 12px}.version{margin-left:12px}.code-line{font-family:Consolas,'Courier New',monospace}.demo-link{position:absolute;right:134px;top:930px;border:1px solid var(--runtime);color:var(--text);padding:9px 20px;border-radius:6px;text-decoration:none;font-size:23px}.slide.has-demo .takeaway{right:460px}.slide.opening header,.slide.opening .takeaway{visibility:hidden}.slide.opening .diagram{top:200px}.slide.opening .diagram text{letter-spacing:-1px}.slide-footer .sources{margin-left:12px}.menu-dialog{background:#10182c;color:#EFF4FF;border:1px solid #33415D;border-radius:12px;max-width:1060px;width:90vw;max-height:85vh;padding:30px}.menu-dialog::backdrop{background:#000b}.menu-dialog h2{margin:0 0 20px}.menu-dialog .toc-list{display:grid;grid-template-columns:1fr 1fr;gap:6px;max-height:65vh;overflow-y:auto}.menu-dialog button{background:transparent;color:#EFF4FF;border:1px solid #33415D;border-radius:5px;text-align:left;padding:10px 14px;font-size:15px;line-height:1.5}.menu-dialog .close{float:right}.menu-dialog small{color:#9EACC8}.progress{position:absolute;bottom:0;left:0;height:2px;background:#B794F4;transition:width .2s}.slide:focus{outline:0}.deck-stage{transition:none!important}.slide g.dim{opacity:.68}
@media(max-width:600px){.menu-dialog .toc-list{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
@media print{.demo-link,.menu-dialog,.progress{display:none!important}.slide.opening header{visibility:hidden!important}.code-line{font-family:Consolas,'Courier New',monospace}}
'''
style+=LIGHT_STYLE+DESIGN_STYLE+r'''
.module-map{position:absolute;left:134px;right:134px;top:233px;display:flex;gap:18px;align-items:center;height:25px;font-size:17px;color:#91A4BE;line-height:1.2}
.module-map span{padding:4px 12px;border-bottom:2px solid transparent}.module-map .current{color:#DCEBFF;border-bottom-color:#A7CEFF;background:#30445D;border-radius:4px 4px 0 0}
'''
font=base64.b64encode((ROOT/'assets/Pretendard-Regular.woff2').read_bytes()).decode()
bold_font=base64.b64encode((ROOT/'assets/Pretendard-Bold.woff2').read_bytes()).decode()
license_=json.dumps((ROOT/'assets/Pretendard-OFL.txt').read_text(encoding='utf-8'),ensure_ascii=False)
html_slides=[]
for i,s in enumerate(ordered):
    demo=f'<a class="demo-link" href="demo-handoff.html?demo={s["demo"]}&amp;return={s["id"]}" target="_blank" rel="noopener">{"Hermes" if s["demo"]=="hermes" else "PydanticAI"} Demo ↗</a>' if s['demo'] else ''
    module_map='<nav class="module-map" aria-label="Hermes 설명 범주">'+''.join(f'<span class="{"current" if n==s["chapter"] else ""}"'+(' aria-current="step"' if n==s['chapter'] else '')+'>'+escape(name)+'</span>' for n,name in enumerate(CHAPTERS))+'</nav>' if 'chapter' in s else ''
    html_slides.append(f'''<!-- === {s['id']}: {escape(s['title'])} === -->
<section class="slide {s['kind']} {'active' if i==0 else ''} {'has-demo' if s['demo'] else ''}" data-index="{i}" data-slide-id="{s['id']}" tabindex="-1" aria-label="{i+1}. {escape(s['title'])}" aria-hidden="{'false' if i==0 else 'true'}">
<header><p class="section-label">{escape(s['section'])}</p><h1>{escape(s['title'])}</h1><p class="subtitle">{escape(s['sub'])}</p></header>
{module_map}<div class="diagram">{diagram_svg(s)}</div><p class="takeaway">{escape(s['take'])}</p>{demo}
<footer class="slide-footer"><div><span class="page-count">{i+1:02} / {len(ordered)}</span><span>{s['id']}</span><span class="version">{escape(s['version'])}</span><button class="sources" aria-label="이 장의 개념·설명·출처 열기">Sources</button></div><nav class="controls" aria-label="발표 탐색"><span class="step-label">전체 구성 · 0/{len(s['steps'])-1}</span><button class="prev" aria-label="이전 단계">←</button><input class="jump-number" type="number" min="1" max="{len(ordered)}" value="{i+1}" aria-label="이동할 슬라이드 번호"><span class="jump-total">/ {len(ordered)}</span><button class="next" aria-label="다음 단계">→</button><button class="menu" aria-label="전체 목차 열기">목차</button></nav></footer><div class="progress" style="width:{(i+1)/len(ordered)*100:.4f}%"></div></section>''')

metadata=[{k:v for k,v in s.items() if k!='diagram'} for s in ordered]
notes_md='# 2차 세미나 — 발표자 전용 노트\n\n'+ '\n\n'.join('## '+s['id']+' — '+s['title']+'\n\n'+s['note'] for s in ordered)+'\n\n# 심층 개념 해설\n\n'+sections['C']+'\n\n# Q&A\n\n'+sections['D']+'\n\n# 근거와 정정\n\n'+sections['F']
(ROOT/'presenter-notes.md').write_text(notes_md,encoding='utf-8')
(ROOT/'notes.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
hermes_guide='## Hermes 개정 안내\n\n6~21페이지를 요청 처리→Tool 실행→기억·재사용→긴 작업·위임→서비스 운영→Demo로 재구성했습니다. 기존 S06은 S05에 통합했습니다. 현재 페이지별 설명은 notes.json과 Sources를 기준으로 합니다. 아래 원 blueprint의 장표 참조는 개정 전 ID 기준일 수 있습니다.\n\n'
private=dict(concepts=hermes_guide+sections['C'],qa=hermes_guide+sections['D'],research=hermes_guide+sections['F'],demos=hermes_guide+sections['E'],reserved={k:specs[k] for k in ('S39','S40','S41','S42')})
script=(ROOT/'controller.js').read_text(encoding='utf-8').replace('__SLIDES__',json.dumps(metadata,ensure_ascii=False)).replace('__PRIVATE__',json.dumps(private,ensure_ascii=False))
toc=''.join(f'<button data-jump="{i}"><small>{i+1:02} · {s["id"]}</small>　{escape(s["title"])}</button>' for i,s in enumerate(ordered))
html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Agent Framework 2차 세미나</title><style>@font-face{{font-family:'Seminar Korean';src:url(data:font/woff2;base64,{font}) format('woff2');font-weight:400;font-display:swap}}@font-face{{font-family:'Seminar Korean';src:url(data:font/woff2;base64,{bold_font}) format('woff2');font-weight:700;font-display:swap}}\n{example['base']}\n{style}</style><script type="application/json" id="font-license">{license_}</script></head><body><div class="key-hint">← → Space 단계 · PageUp/Down 장 이동 · G 번호 이동 · T 목차 · N 노트 · F 전체 화면</div><div class="deck-viewport"><main class="deck-stage">{''.join(html_slides)}</main></div><dialog class="menu-dialog" aria-labelledby="toc-title"><button class="close">닫기</button><h2 id="toc-title">전체 발표 목차</h2><div class="toc-list">{toc}</div></dialog><dialog class="sources-dialog" aria-labelledby="reader-title"><button class="reader-close" aria-label="개념 설명 닫기">닫기</button><header><div class="reader-meta"></div><h2 id="reader-title"></h2></header><main></main></dialog><div class="sr-only" id="live" aria-live="polite"></div><script>{script}</script></body></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
manifest={'blueprint':BLUEPRINT.name,'blueprintSha256':hashlib.sha256(BLUEPRINT.read_bytes()).hexdigest(),'editorialRevision':'2026-11-03 / revision.py and hermes_revision.py / user-approved 16-slide Hermes sequence','hermesOrder':HERMES_ORDER,'hermesPages':[6,21],'aliases':{'S06':'S05'},'slides':[{'id':s['id'],'title':s['title'],'sourceIds':[r[0] for r in s['sources']],'builds':len(s['steps'])-1} for s in ordered],'reserved':['S39','S40','S41','S42'],'demoStatus':'handoff only; no actual runtime connected','visualDesign':'2026-11-03 / design.py / slate surfaces, local Pretendard, orthogonal routing and contextual focus','notes':'Sources: concepts and explanation / N: presenter notes and appendix'}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Final: {len(ordered)} slides, {len(html.encode())//1024} KiB, {ROOT / "index.html"}')
