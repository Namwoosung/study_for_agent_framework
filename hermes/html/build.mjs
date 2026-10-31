import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {units} from './editorial.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
const runtime=path.join(process.env.USERPROFILE||'','.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
async function dependency(name,file){try{return await import(name);}catch{return import(pathToFileURL(path.join(runtime,file)).href);}}
const {marked,Renderer}=await dependency('marked','marked/lib/marked.esm.js');
const {instance}=await dependency('@viz-js/viz','@viz-js/viz/dist/viz.js');
const viz=await instance();
const original=fs.readFileSync(path.join(root,'../Hermes_Agent.md'),'utf8');
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const definitions=original.split(/\r?\n/).filter(l=>/^\[(?:S|C)\d+\]:/.test(l)).join('\n');
const sections=new Map();let current=null,fenced=false;
for(const line of original.split(/\r?\n/)){
  if(line.startsWith('```'))fenced=!fenced;
  if(!fenced&&/^## \d+\./.test(line)){const id=Number(line.match(/^## (\d+)/)[1]);current={id,title:line.slice(3),lines:[]};sections.set(id,current);continue;}
  if(!fenced&&/^# 부록 /.test(line)){const id=line.includes('부록 A')?'glossary':'sources';current={id,title:line.slice(2),lines:[]};sections.set(id,current);continue;}
  if(!fenced&&/^# Part /.test(line)){current=null;continue;}
  if(current)current.lines.push(line);
}
if(sections.size!==25)throw Error(`Expected 25 source sections, got ${sections.size}`);
fs.mkdirSync(path.join(root,'assets'),{recursive:true});
let diagramCount=0;
const figureNames=['전체 아키텍처: 구성요소 사이의 관계','Agent Loop: 정상 호출과 반복 경로','Context: 압축 여부에 따른 분기','Tool 실행: 일반 도구와 상태 기반 도구의 분기','MCP: 외부 도구가 연결되는 경로','Subagent: 위임과 결과 통합','반도체 분석: 가상 구성요소와 책임'];
const diagramRecords=[];
function wrapped(label){
  const lines=label.replaceAll('\\n','\n').split('\n');
  return lines.flatMap(line=>{
    if(line.length<25)return [line];
    const words=line.split(/\s+/);let result=[],row='';
    for(const w of words){if((row+' '+w).length>25&&row){result.push(row);row=w;}else row+=(row?' ':'')+w;}
    if(row)result.push(row);return result;
  }).join('\n');
}
function dotGraph(nodes,edges){
  const quote=JSON.stringify;
  return `digraph G { graph [rankdir=TB,bgcolor="transparent",pad="0.22",nodesep="0.3",ranksep="0.5"]; node [shape=box,style="rounded,filled",fillcolor="#f6f8f5",color="#a9bbb2",fontcolor="#233d34",fontname="Malgun Gothic",fontsize=14,margin="0.18,0.15"]; edge [color="#627e72",fontcolor="#456558",fontname="Malgun Gothic",fontsize=12,arrowsize=0.7]; ${nodes.map(n=>{
    const label=wrapped(n.label),max=Math.max(...label.split('\n').map(x=>[...x].reduce((a,c)=>a+(c.charCodeAt(0)>255?1.65:1),0)));
    return `${n.id}[label=${quote(label)},width=${Math.max(1.7,max*.11).toFixed(2)}${n.shape?',shape='+n.shape:''}];`;
  }).join('\n')} ${edges.map(e=>`${e.from}->${e.to}[label=${quote(e.label||'')}${e.both?',dir=both':''}];`).join('\n')} }`;
}
function flowGraph(text){
 const nodes=new Map(),edges=[];
 for(const line of text.split('\n').slice(1).filter(x=>x.trim())){
   const clean=line.replace(/\b([A-Za-z]\w*)(\[([^\]]+)\]|\{([^}]+)\})/g,(_,id,shape,box,diamond)=>{
     let label=box||diamond;if(box?.startsWith('(')&&box.endsWith(')'))label=box.slice(1,-1);
     nodes.set(id,{id,label,shape:diamond?'diamond':box?.startsWith('(')?'cylinder':undefined});return id;
   }).trim();
   const match=clean.match(/^(\w+)\s*(<-->|-->|--\s+(.+?)\s+-->)\s*(\w+)$/);
   if(!match)throw Error('Unsupported diagram line: '+line);
   edges.push({from:match[1],to:match[4],label:match[3]||'',both:match[2]==='<-->'});
 }
 for(const e of edges)for(const id of [e.from,e.to])if(!nodes.has(id))throw Error('Unknown node '+id);
 return {nodes:[...nodes.values()],edges};
}
function sequenceGraph(){return {nodes:[{id:'U',label:'User → AIAgent\n사용자 메시지 추가'},{id:'P',label:'Prompt Builder\n시스템 지침 / Context 조합'},{id:'L',label:'LLM Provider\nmessages + tool schemas'},{id:'B',label:'모델 응답 종류',shape:'diamond'},{id:'T',label:'Tool Executor\n요청 검토 및 실행'},{id:'S',label:'Session Store\n대화 / 메타데이터 저장'},{id:'R',label:'User\n최종 응답 반환'}],edges:[{from:'U',to:'P'},{from:'P',to:'L'},{from:'L',to:'B'},{from:'B',to:'T',label:'Tool Calls'},{from:'T',to:'L',label:'호출·결과를 메시지에 추가'},{from:'B',to:'S',label:'최종 텍스트'},{from:'S',to:'R'}]};}
function architectureSvg(graph){
 // 부채꼴 자동 배치 대신 세 열에 배치한다. 모든 원문 간선은 그대로 그린다.
 const boxes={U:[275,20,220,50],E:[255,100,260,85],A:[270,245,260,60],P:[20,215,205,85],R:[570,215,190,70],L:[570,345,190,50],T:[270,365,260,60],X:[270,495,260,90],S:[20,375,205,70],M:[20,495,205,70],K:[20,625,205,70],D:[570,495,190,70]};
 const routes={'U-E':'M385 70 V100','E-A':'M385 185 V245','A-P':'M270 260 L225 258','A-R':'M530 260 L570 250','R-L':'M665 285 V345','L-A':'M570 370 H558 V280 H530','A-T':'M385 305 V365','T-A':'M410 365 V305','T-X':'M385 425 V495','X-T':'M410 495 V425','A-S':'M270 280 H248 V410 H225','A-M':'M270 290 H255 V530 H225','A-K':'M270 300 H262 V660 H225','A-D':'M530 290 H545 V530 H570'};
 const paths=graph.edges.map(edge=>{const route=routes[edge.from+'-'+edge.to];if(!route)throw Error('Architecture edge missing');return `<path d="${route}" fill="none" stroke="#627e72" stroke-width="1.4" marker-end="url(#arrow)" ${edge.both?'marker-start="url(#arrow)"':''}/>`;}).join('');
 const nodes=graph.nodes.map(node=>{const [x,y,w,h]=boxes[node.id],lines=wrapped(node.label).split('\n');return `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7" fill="${node.id==='A'?'#e6efdf':'#f6f8f5'}" stroke="#a9bbb2"/><text x="${x+w/2}" y="${y+h/2-(lines.length-1)*10+5}" text-anchor="middle" fill="#233d34" font-family="Malgun Gothic, sans-serif" font-size="14">${lines.map((line,i)=>`<tspan x="${x+w/2}" dy="${i?'20':'0'}">${escape(line)}</tspan>`).join('')}</text></g>`;}).join('');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="780" height="725" viewBox="0 0 780 725"><title>전체 아키텍처</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#627e72"/></marker></defs>${paths}${nodes}</svg>`;
}
function diagram(text){
 const num=++diagramCount;const g=text.startsWith('sequenceDiagram')?sequenceGraph():flowGraph(text);
 const svg=(num===1?architectureSvg(g):viz.renderString(dotGraph(g.nodes,g.edges),{format:'svg'})).replace(/<\?xml[^>]*\?>\s*/,'').replace(/<!DOCTYPE[\s\S]*?>\s*/,'');
 const accessible=svg.replace('<svg ','<svg role="img" aria-labelledby="title desc" ').replace(/<title>[^<]*<\/title>/,`<title id="title">${escape(figureNames[num-1])}</title><desc id="desc">${escape(g.edges.map(e=>`${g.nodes.find(n=>n.id===e.from).label} ${e.both?'↔':'→'} ${e.label?`(${e.label}) `:''}${g.nodes.find(n=>n.id===e.to).label}`).join(' / '))}</desc>`);
 fs.writeFileSync(path.join(root,`assets/diagram-${num}.svg`),accessible);
 diagramRecords.push({number:num,title:figureNames[num-1],nodes:g.nodes.length,edges:g.edges.length,source:text});
 const note=num===7?'[예시] 원문의 가상 PoC 설계도입니다. Hermes의 기본 구성이나 검증 완료 시스템을 뜻하지 않습니다.':num===2?'[개념도] 원문의 호출 순서를 정상 실행 중심으로 재구성했습니다. 오류·중단·예산 종료는 아래 본문을 함께 읽으세요.':'[개념도] 원문의 연결 관계를 보존해 다시 배치했습니다. 실제 구현의 모든 호출·보안 경계를 표시한 그림은 아닙니다.';
 return `<figure class="diagram" id="figure-${num}"><figcaption><span>그림 ${num}</span> ${figureNames[num-1]}</figcaption><p class="scroll-hint">넓은 도식은 가로로 스크롤하여 읽을 수 있습니다.</p><div class="diagram-scroll" tabindex="0" role="region" aria-label="${escape(figureNames[num-1])}"><img src="assets/diagram-${num}.svg" alt="${escape(figureNames[num-1])}. 연결 관계는 도식 원문의 화살표로도 확인할 수 있습니다." loading="lazy"></div><p class="figure-note">${note} <a href="assets/diagram-${num}.svg" target="_blank" rel="noopener">도식 크게 보기 ↗</a></p><details class="diagram-original"><summary>연결 관계 원문 (Mermaid)</summary><pre><code>${escape(text)}</code></pre></details></figure>`;
}
const renderer=new Renderer();let prefix='',toc=[];
renderer.heading=function({tokens,depth,text}){
 const clean=text.replaceAll('`','');
 const raw=clean.match(/^(\d+(?:\.\d+)*|B\.\d+)/)?.[1]||clean;
 const id=`s-${prefix}-${raw.toLowerCase().replace(/[^\p{L}\p{N}]+/gu,'-')}`;
 if(depth===2)toc.push({id,label:clean});
 return `<h${depth} id="${id}">${this.parser.parseInline(tokens)}<a class="anchor" href="#${id}" aria-label="${escape(clean)} 섹션 링크">#</a></h${depth}>\n`;
};
renderer.code=function({text,lang}){
 if(lang==='mermaid')return diagram(text);
 let caption=lang==='python'?(text.includes('[코드')?'실제 함수·시그니처 일부 / 생략 포함':text.includes('conceptual_')?'설명용 의사코드':'설명용 예시'):lang==='bash'?'공식 명령 예시 / 실행하지 않음':lang==='json'?'구조를 설명하는 JSON 예시':lang==='yaml'?'설명용 설정 예시':lang==='markdown'?'학습용 Skill 문서 예시':'구조·흐름 설명';
 return `<div class="code-block"><div class="code-caption"><span>${caption}</span><span>${escape(lang||'text')}</span></div><pre tabindex="0" aria-label="${escape(caption)}"><code class="language-${escape(lang||'text')}">${escape(text)}</code></pre></div>\n`;
};
const originalTable=renderer.table.bind(renderer);
renderer.table=function(token){return `<div class="table-scroll" tabindex="0" role="region" aria-label="비교 및 설명 표">${originalTable(token)}</div>`;};
function renderSection(id){
 prefix=String(id);const c=sections.get(id);if(!c)throw Error('Missing source chapter '+id);
 let md=`## ${c.title}\n\n${c.lines.join('\n')}`;
 // 원문 수식을 브라우저 의존성 없이 읽을 수 있는 개념식으로 표시한다.
 md=md.replace(/\\\[\s*C_\{total\}[\s\S]*?\\\]/g,'<p class="equation" role="math" aria-label="총비용은 각 모델 호출 비용의 합과 도구, 인프라, 저장, 관측 비용의 합으로 근사합니다."><i>C</i><sub>total</sub> ≈ ∑<sub>i</sub> <i>C</i><sub>model,i</sub> + <i>C</i><sub>tool</sub> + <i>C</i><sub>infra</sub> + <i>C</i><sub>storage</sub> + <i>C</i><sub>observability</sub></p>');
 // Markdown에서 한글 조사와 맞닿은 강조도 의도대로 표시한다.
 let html=marked.parse(md+'\n\n'+definitions,{renderer});
 html=html.replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>');
 html=html.replace(/<a href="(https?:[^\"]+)"/g,'<a href="$1" target="_blank" rel="noopener noreferrer"');
 return `<section class="source-section" data-source-chapter="${id}">${html}</section>`;
}
const allPages=[{slug:'index',title:'학습 안내',short:'학습 안내'},...units,{slug:'glossary',title:'학습 용어 사전',short:'용어 사전'},{slug:'sources',title:'출처와 검증 범위',short:'출처와 검증 범위'}];
function sidebar(active){let group='';return `<aside class="sidebar" id="book-nav"><a class="book-title" href="index.html"><span class="book-mark" aria-hidden="true">H.</span><span>Hermes Agent<small>개인 학습 교재</small></span></a><nav aria-label="교재 목차"><a class="nav-intro ${active==='index'?'current':''}" href="index.html" ${active==='index'?'aria-current="page"':''}>학습 안내</a>${units.map(u=>{let h=u.group!==group?`<p class="nav-group">${u.group}</p>`:'';group=u.group;return h+`<a href="${u.slug}.html" ${active===u.slug?'class="current" aria-current="page"':''}><span class="nav-number">${u.number}</span><span>${u.short}</span></a>`;}).join('')}<p class="nav-group">참고 자료</p><a href="glossary.html" ${active==='glossary'?'class="current" aria-current="page"':''}>용어 사전</a><a href="sources.html" ${active==='sources'?'class="current" aria-current="page"':''}>출처와 검증 범위</a></nav><div class="book-meta"><span>원문 기준 2026.10.29</span><a href="../Hermes_Agent.md">원본 Markdown ↗</a></div></aside>`;}
function layout(page,content,localToc){const i=allPages.findIndex(p=>p.slug===page.slug),prev=allPages[i-1],next=allPages[i+1];
 return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Hermes Agent의 개념, 실행 원리, 코드와 반도체 적용 판단을 배우는 개인 학습 교재"><title>${escape(page.title)} — Hermes Agent</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="site.js" defer></script></head><body><a class="skip-link" href="#main">본문으로 건너뛰기</a><header class="mobile-header"><a href="index.html">Hermes Agent</a><button id="menu-button" type="button" aria-controls="book-nav" aria-expanded="false">목차 열기</button></header>${sidebar(page.slug)}<div class="reading-layout"><main id="main" tabindex="-1"><div class="breadcrumb"><a href="index.html">Hermes Agent</a><span aria-hidden="true">/</span><span>${escape(page.short||page.title)}</span></div>${content}<nav class="page-nav" aria-label="이전 다음 단원">${prev?`<a href="${prev.slug}.html"><small>이전 단원</small>← ${escape(prev.short||prev.title)}</a>`:'<span></span>'}${next?`<a class="next" href="${next.slug}.html"><small>다음 단원</small>${escape(next.short||next.title)} →</a>`:'<a class="next" href="index.html"><small>처음으로</small>학습 안내 →</a>'}</nav><footer>Hermes Agent 학습 교재<span>문헌·소스 검토 기반 / 실제 설치·벤치마크 미수행</span><a href="sources.html">출처와 검증 범위</a></footer></main><aside class="local-toc"><nav aria-label="이 페이지의 내용"><p>이 페이지에서</p>${localToc.map(t=>`<a href="#${t.id}">${escape(t.label)}</a>`).join('')}</nav></aside></div></body></html>`;
}
function save(page,content,links=toc){fs.writeFileSync(path.join(root,page.slug+'.html'),layout(page,content,links));}
const overview=`<header class="chapter-header"><p class="eyebrow">AGENT FRAMEWORK STUDY · READING GUIDE</p><h1>Hermes Agent<br>이해하기</h1><p class="lead">모델이 판단하고, Runtime이 실행합니다.<br>이 둘이 하나의 Agent로 연결되는 과정을 배웁니다.</p><div class="chapter-meta">개인 학습 교재 <span>·</span> 원문 기준 2026.10.29</div></header>
<section id="starting-point"><h2>시작점: Hermes는 무엇을 하는가?</h2><p>LLM은 텍스트와 도구 호출 요청을 생성합니다. 파일을 읽고, 함수를 실행하고, 결과를 다시 모델에 전달하려면 실행을 관리하는 시스템이 필요합니다. <strong>Hermes Agent는 이러한 반복 실행·도구·세션·기억·작업 절차를 갖춘 범용 Agent Harness</strong>입니다. <a href="https://hermes-agent.nousresearch.com/docs" target="_blank" rel="noopener">[S01]</a> <a href="https://hermes-agent.nousresearch.com/docs/developer-guide/architecture" target="_blank" rel="noopener">[S02]</a></p><p>이 교재에서는 “기능이 있는가”에서 한 걸음 더 들어가, <strong>누가 판단하고, 누가 실행하며, 무엇을 저장하는가</strong>를 연결해 읽습니다.</p>
<figure class="reading-flow"><figcaption>개념 예시 · 한 요청의 정상 실행 흐름</figcaption><ol><li><b>사용자 요청</b><span>“센서 CSV를 분석해 줘”</span></li><li><b>LLM의 선택</b><span>필요한 Tool Call 생성</span></li><li><b>Runtime의 실행</b><span>권한·정책 확인 → 도구 실행</span></li><li><b>결과 관찰</b><span>결과를 모델에 전달 → 반복 또는 응답</span></li></ol><p class="figure-note">가상의 학습 시나리오입니다. 도구 호출이 가능한 환경을 가정하며, 실제 분석 정확성을 검증한 예가 아닙니다. <a href="execution.html">실행 경로 자세히 읽기 →</a></p></figure></section>
<section id="distinctions"><h2>읽는 동안 유지할 세 가지 구분</h2><dl class="key-distinctions"><div><dt>모델의 판단 / Runtime의 실행</dt><dd>Tool Call은 실행 요청 데이터입니다. 실제 함수 호출과 실행 권한은 Runtime 및 실행환경이 처리합니다.</dd></div><div><dt>현재 입력 / 기억 / 과거 이력 / 작업 절차</dt><dd>Context는 현재 요청의 정보, Memory는 재사용할 사실, History는 대화 기록, Skills는 작업 방법입니다. 서로 다른 저장·검색 경로를 가집니다.</dd></div><div><dt>지식 갱신 / 모델 가중치 학습</dt><dd>기억과 Skill을 기록·수정하는 자기 개선을, 기반 모델의 자동 재학습으로 해석하면 안 됩니다.</dd></div></dl><p class="source-note">원문 0·2·9·10장에 근거한 편집 요약입니다. <a href="sources.html#s-0-0">원문의 표기와 검증 범위</a>를 함께 확인하세요.</p></section>
<section id="reading-order"><h2>개념에서 적용 판단까지</h2><p>처음 읽을 때는 순서대로 진행하세요. 특정 개념을 다시 확인할 때는 왼쪽 목차나 아래 단원으로 바로 이동할 수 있습니다.</p><ol class="unit-list">${units.map(u=>`<li><a href="${u.slug}.html"><span class="unit-number">${u.number}</span><span><b>${u.title}</b><small>${u.subtitle}</small></span><span class="unit-arrow" aria-hidden="true">→</span></a></li>`).join('')}</ol></section>
<section id="how-to-read"><h2>이 교재를 읽는 방법</h2><p>각 단원의 도입에서 먼저 큰 그림을 잡고, 이어지는 원문의 비교표·예시·코드로 세부 동작을 확인하세요. 코드는 실코드의 일부, 설명용 의사코드, 가상 설정을 구분해 표시합니다. 도식은 본문 옆의 설명과 함께 읽어야 합니다.</p><p>내용은 <a href="../Hermes_Agent.md">Hermes_Agent.md</a>를 바탕으로 구성했습니다. 기능·기본값·파일명은 원문의 조사 시점에 해당하며, 실제 개발 시 선택한 버전으로 다시 검증해야 합니다. <a href="sources.html">검증 범위와 공식 자료 →</a></p><p class="callout">설치·실행·벤치마크 결과가 아닌 문헌·공개 소스 검토입니다. 반도체 적용 사례 역시 설계 검토용 가상 시나리오입니다.</p></section>`;
save(allPages[0],overview,[{id:'starting-point',label:'Hermes의 역할'},{id:'distinctions',label:'세 가지 구분'},{id:'reading-order',label:'단원별 읽기 순서'},{id:'how-to-read',label:'읽는 방법과 범위'}]);
for(const unit of units){
 toc=[];
 const sectionsHtml=unit.chapters.map(renderSection).join('\n');
 const header=`<header class="chapter-header"><p class="eyebrow">${unit.group} <span>/</span> 단원 ${unit.number}</p><h1>${unit.title}</h1><p class="lead">${unit.subtitle}</p><div class="chapter-meta">원문 ${unit.chapters.length===1?unit.chapters[0]:unit.chapters[0]+'–'+unit.chapters.at(-1)}장</div></header><section class="unit-intro" id="overview"><h2>먼저 연결해 보기</h2>${unit.intro}<p class="reading-question"><strong>읽는 관점</strong>${unit.focus}</p></section>`;
 save(unit,header+sectionsHtml+`<div class="next-bridge"><p>${unit.next}</p></div>`,[{id:'overview',label:'먼저 연결해 보기'},...toc]);
}
toc=[];
save(allPages.find(p=>p.slug==='glossary'),`<header class="chapter-header"><p class="eyebrow">참고 자료 / GLOSSARY</p><h1>학습 용어 사전</h1><p class="lead">본문의 개념을 짧은 정의로 다시 연결합니다.</p></header><p>원문 부록 A의 용어를 모았습니다. 정의를 읽은 뒤 관련 단원에서 실제 동작과 한계를 함께 확인하세요.</p><nav class="related-links" aria-label="개념별 단원"><a href="context.html">Context와 Prompt</a><a href="memory.html">Memory와 History</a><a href="tools.html">Tool과 MCP</a><a href="operations.html">Guardrails</a></nav>${renderSection('glossary')}`);
toc=[];
save(allPages.find(p=>p.slug==='sources'),`<header class="chapter-header"><p class="eyebrow">참고 자료 / EVIDENCE & SCOPE</p><h1>출처와 검증 범위</h1><p class="lead">문서로 확인한 내용과 실험으로 확인해야 할 내용을 구분합니다.</p></header><div class="callout"><strong>자료 기준: 2026년 10월 29일</strong><p>이 교재는 사용자의 원문을 학습 교재로 편집한 결과입니다. 이번 웹페이지 제작에서 Hermes 공식 문서의 최신 상태나 소스 구현을 추가로 검증하지 않았습니다. 원문의 검토 범위와 한계를 아래에 보존했습니다.</p></div>${renderSection(0)}${renderSection('sources')}`);
fs.writeFileSync(path.join(root,'assets/favicon.svg'),'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#254c42"/><text x="14" y="47" font-family="Georgia,serif" font-size="46" fill="#fff">H</text></svg>');
const report={source:'../Hermes_Agent.md',sha256:createHash('sha256').update(original).digest('hex'),pages:allPages.map(p=>p.slug+'.html'),chapterMapping:units.map(u=>({page:u.slug+'.html',chapters:u.chapters})),diagrams:diagramRecords.map(({source,...d})=>d),sourceSections:sections.size};
fs.writeFileSync(path.join(root,'content-map.json'),JSON.stringify(report,null,2)+'\n');
if(diagramCount!==7)throw Error('Expected all 7 source diagrams to render');
console.log(`Built ${allPages.length} static pages; preserved ${sections.size} source sections; rendered ${diagramCount} SVG diagrams.`);

// 기본 교재를 재생성해도 2차 과정 탐색을 유지한다.
await import('./link-courses.mjs');
