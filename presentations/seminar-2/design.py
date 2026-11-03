"""Slate presentation design. Content, slide IDs and build semantics stay intact."""
import re
import xml.etree.ElementTree as ET

PALETTE={
    '#205BC7':'#9CC4FF', '#6941B8':'#BCC7F3', '#087756':'#7AD8C5',
    '#9B4F0A':'#E9C38F', '#BD2845':'#F1A0AC', '#087C74':'#7BD8CC',
    '#52647B':'#B8C6D8', '#7E90A8':'#72859E', '#172B46':'#F1F5FC',
    '#F0F4FA':'#1F2B3A',
}

def rounded_path(d, radius=10):
    """Round orthogonal elbows without changing endpoints or arrow direction."""
    if re.search(r'[a-zA-GI-KN-UW-Z]',d): return d
    tokens=re.findall(r'[MHVL]|-?\d+(?:\.\d+)?',d)
    points=[];i=0;x=y=0
    try:
        while i<len(tokens):
            c=tokens[i];i+=1
            if c in ('M','L'):x,y=float(tokens[i]),float(tokens[i+1]);i+=2
            elif c=='H':x=float(tokens[i]);i+=1
            elif c=='V':y=float(tokens[i]);i+=1
            else:return d
            points.append((x,y))
    except (ValueError,IndexError): return d
    if len(points)<3:return d
    out=f'M{points[0][0]:g} {points[0][1]:g}'
    for a,b,c in zip(points,points[1:],points[2:]):
        u=(b[0]-a[0],b[1]-a[1]);v=(c[0]-b[0],c[1]-b[1])
        la=abs(u[0])+abs(u[1]);lb=abs(v[0])+abs(v[1])
        if not la or not lb or u[0]*v[1]==u[1]*v[0]:out+=f' L{b[0]:g} {b[1]:g}';continue
        r=min(radius,la/2,lb/2)
        before=(b[0]-u[0]/la*r,b[1]-u[1]/la*r)
        after=(b[0]+v[0]/lb*r,b[1]+v[1]/lb*r)
        out+=f' L{before[0]:g} {before[1]:g} Q{b[0]:g} {b[1]:g} {after[0]:g} {after[1]:g}'
    return out+f' L{points[-1][0]:g} {points[-1][1]:g}'

def refine(slides, env):
    text,box,arrow,group,rule=(env[n] for n in ('text','box','arrow','group','rule'))
    # Keep every label; give the cover a visual centre rather than equal boxes.
    d=text(0,105,'Agent',98,'text',700)+text(0,230,'Framework',98,'text',700)
    d+=text(5,306,'세부 구조를 살펴봅니다',39,'text',700)+text(5,379,'2차 세미나',29,'muted')
    d+=rule(5,440,680,440)+text(5,492,'Hermes',28,'runtime',700)+text(210,492,'Claude Code',28,'runtime',700)+text(495,492,'PydanticAI',28,'runtime',700)
    d+=box(1095,20,510,120,'Model','판단과 응답 생성','model',34)
    d+='<g class="cover-runtime">'+box(850,235,730,160,'Runtime / Harness','모델 호출 · 도구 실행 · 상태 관리','runtime',38)+'</g>'
    d+=box(1080,510,525,120,'Tools & State','외부 작업과 실행 결과','tool',34)
    d+=arrow('M1350 140 V185 H1215 V223','model')+arrow('M1215 395 V498','tool')
    d+=arrow('M1605 570 H1640 V80 H1617','context')
    slides['S00']['diagram']=d

    # Uncross the overview's memory/guard paths. Same components and labels.
    d=text(0,120,'Agent를 이루는',49,'text',700)+text(0,186,'주요 구성요소',49,'text',700)
    d+=text(0,280,'목표와 지침을 읽고',29,'muted')+text(0,327,'모델과 도구를 연결해',29,'muted')+text(0,374,'작업을 이어갑니다.',29,'muted')
    def n(x,y,w,h,t,s='',c='runtime'):return box(x,y,w,h,t,s,c,25)
    d+=group(1,n(500,0,330,95,'User Goal','','context')+n(940,0,370,95,'Instructions','','context')+arrow('M665 95 V173','context')+arrow('M1125 95 V135 H840 V173','context'))
    d+=group(2,n(500,185,420,120,'Context Builder','지침 · 이력 · 필요한 정보','context')+n(1120,185,440,120,'LLM / Model','판단 · Tool Call · 답변','model')+arrow('M920 230 H1108','model')+arrow('M1120 280 H1040 V420 H932','model'))
    d+=group(3,n(500,380,420,120,'Runtime / Harness','반복 · 실행 · 종료','runtime')+n(1120,380,220,120,'Tools','','tool')+n(1440,380,210,120,'Environment','','tool')+arrow('M710 380 V317','context')+arrow('M920 450 H1108','tool')+arrow('M1120 485 H932','tool')+arrow('M1340 430 H1428','tool')+arrow('M1440 480 H1352','tool'))
    d+=group(4,n(500,570,190,80,'State','','context')+n(740,570,300,80,'Memory Store','','context')+arrow('M595 570 V512','context')+arrow('M840 570 V512','context'))
    d+=group(5,n(1120,570,260,80,'Guardrails','','risk')+n(1440,570,210,80,'Trace','','muted')+arrow('M1250 570 V512','risk')+arrow('M1545 500 V558','muted')+text(1330,35,'개념 구성도',22,'muted'))
    slides['S01']['diagram']=d

    for ident,s in slides.items():
        root=ET.fromstring('<g>'+s['diagram']+'</g>')
        for e in root.iter():
            for attr in ('fill','stroke'):
                if e.get(attr) in PALETTE:e.set(attr,PALETTE[e.get(attr)])
            if e.tag=='rect' and 'node' in e.get('class','').split():
                e.set('fill','#2C3B4E');e.set('fill-opacity','1')
                e.set('stroke','#61738B');e.set('stroke-opacity','.78');e.set('stroke-width','1.3');e.set('rx','9')
            if e.tag=='path':
                e.set('d',rounded_path(e.get('d','')))
                e.set('stroke-linejoin','round');e.set('stroke-linecap','round')
                if e.get('marker-end'):e.set('class',(e.get('class','')+' connector').strip());e.set('stroke-width','2.6')
            if e.tag=='text' and e.get('font-weight')=='700' and e.get('fill') not in ('#B8C6D8','#F1F5FC'):
                e.set('class',(e.get('class','')+' node-label').strip())
            if ident=='S14' and e.tag=='text' and e.text=='여러 Tool Call':e.set('y','195')
        s['diagram']=''.join(ET.tostring(e,encoding='unicode') for e in root)
    for key,col in env['colors'].items():env['colors'][key]=PALETTE.get(col,col)

STYLE=r'''
/* Slate canvas: no black, no neon, clear typographic hierarchy. */
:root{color-scheme:dark;--stage-bg:#192330;--slide-bg:#243142;--text:#F1F5FC;--muted:#B8C6D8;--line:#4D6078;--runtime:#BCC7F3;--context:#E9C38F;--model:#9CC4FF;--tool:#7AD8C5}
.slide{background:#243142}.slide::before{content:'';position:absolute;left:72px;top:64px;bottom:82px;width:1px;background:#3B4D65}
.slide::after{content:'';position:absolute;left:72px;top:64px;width:3px;height:42px;background:#9CC4FF;border-radius:2px}
.slide header{position:relative;z-index:1}.section-label{font-size:18px;font-weight:500;letter-spacing:.2px;color:#AABCD2;margin-bottom:23px}.section-label:before{display:none}
h1{font-size:51px;line-height:1.25;letter-spacing:-1.5px;font-weight:700;color:#F1F5FC}.subtitle{font-size:27px;font-weight:400;line-height:1.5;color:#B8C6D8;margin-top:17px}
.diagram{top:269px}.diagram svg{overflow:visible}.diagram svg text{font-family:'Seminar Korean',sans-serif;letter-spacing:-.25px}.diagram .code-line{letter-spacing:0;font-family:Consolas,'Courier New',monospace}
.slide .node{transition:fill .16s,stroke .16s,stroke-width .16s}.slide .connector{opacity:.9}.slide g[data-focus]{transition:opacity .16s ease}
.slide g.dim{opacity:.58}.slide g.highlight{opacity:1}.slide g.highlight .node{fill:#3A526F;fill-opacity:1;stroke:#A7CEFF;stroke-opacity:1;stroke-width:3;filter:none}
.slide g.highlight text{fill:#FFFFFF;font-weight:700}.slide g.highlight .connector{stroke-width:3.5;opacity:1}
.focus-frame{fill:#354B65;fill-opacity:0;stroke:#91BFF7;stroke-opacity:0;stroke-width:1.3;pointer-events:none;transition:fill-opacity .16s,stroke-opacity .16s}
.slide g.highlight>.focus-frame{fill-opacity:.75;stroke-opacity:.8}.cover-runtime .node{fill:#354961;stroke:#A7CEFF;stroke-width:2}
.takeaway{top:938px;color:#E2EAF5;font-size:26px;line-height:1.35;border-left:0;padding:0 0 0 24px;right:134px}
.takeaway:before{content:'';position:absolute;left:0;top:7px;width:6px;height:21px;border-radius:2px;background:#E9C38F}
.slide-footer{border-top-color:#43556E;bottom:24px;padding-top:16px;font-size:16px;gap:20px;color:#ACBDD2}.page-count{font-size:20px;color:#E7EFFB;font-variant-numeric:tabular-nums}.version{font-size:15px;color:#9DAFC7}
.controls{gap:8px}.controls button,.controls .jump-number{height:34px;border-color:#4D6078;background:#29394D;color:#D2DEED;border-radius:5px}.controls button:hover{color:#FFFFFF;border-color:#9CC4FF;background:#3A506C}
.sources{border:1px solid #536B89;background:#30445D;color:#D7E8FF;border-radius:5px;padding:5px 12px;text-decoration:none;font-weight:500;font-size:16px}
.sources:hover{background:#3B5678;border-color:#9CC4FF}.step-label{font-size:15px;font-weight:400;min-width:160px;background:#2C3C51;color:#C1D1E5;border:1px solid #4B607C;padding:6px 10px;border-radius:5px}
.slide.focus-on .step-label{color:#EAF3FF;background:#365578;border-color:#8AB7ED;font-weight:500}.key-hint{color:#AABCD2}.progress{height:3px;background:#90B8ED}
.demo-link{border-color:#7FA6D6;background:#344F70;color:#EAF3FF;font-size:22px;padding:9px 20px;border-radius:6px}
.cover::before,.cover::after,.section-opening::before,.section-opening::after{display:none}.cover .diagram{top:190px}.cover header,.cover .takeaway,.section-opening header{visibility:hidden}.section-opening .diagram{top:180px;height:720px}
.menu-dialog{background:#27364A;color:#F1F5FC;border:1px solid #60738E;box-shadow:0 24px 100px #111b2f77}.menu-dialog button{background:#2B3D53;color:#E1ECF9;border-color:#506784;border-radius:6px}.menu-dialog button:hover{background:#385274;border-color:#94BFF4}.menu-dialog small{color:#AEC5E0}.menu-dialog::backdrop{background:#101b2cc4}
.sources-dialog{color-scheme:dark;background:#27364A;color:#E2EAF5;border:1px solid #60738E;box-shadow:0 24px 100px #111b2f77;border-radius:12px;font-family:'Seminar Korean',sans-serif;line-height:1.85}
.sources-dialog::backdrop{background:#101b2cb8}.sources-dialog header{background:#30435D;border-color:#536B89;padding-top:28px;padding-bottom:28px}.sources-dialog h2{color:#F1F5FC;font-size:28px;letter-spacing:-.5px}.sources-dialog .reader-meta{color:#BED0E6}.sources-dialog .reader-close{color:#F1F5FC;background:#344C6B;border-color:#7B96BA}.sources-dialog dt,.sources-dialog a{color:#ACD0FF}.sources-dialog h3{color:#F1F5FC}.sources-dialog main{max-width:86ch;margin:0 auto;padding-bottom:40px}
@media print{.slide{background:#243142!important;print-color-adjust:exact;-webkit-print-color-adjust:exact}.slide::before,.slide::after{display:none}.focus-frame{visibility:hidden!important}.slide g.dim{opacity:1!important}.slide g.highlight .node{fill:#2C3B4E;fill-opacity:1;stroke:#61738B;stroke-width:1.3}.slide-footer{bottom:24px}}
'''

STYLE += r'''
.learning-role{float:right;color:#D6E6F7;font-size:18px;letter-spacing:0}
.slide g.dim{opacity:.35}
.slide g.highlight .code-line{font-weight:400}
.sources-dialog main{max-width:78ch;margin:0 auto;line-height:1.8}
.sources-dialog h3{margin-top:1.8em;border-top:1px solid #536B89;padding-top:.7em}
.sources-dialog dt{margin-top:1em}
.sources-dialog dd{margin-top:.3em}
@media print{.slide g.dim{opacity:1!important}}
'''
