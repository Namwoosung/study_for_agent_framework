import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import config from './site.config.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
const runtime=path.join(process.env.USERPROFILE||'','.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
async function dependency(name,entry){try{return await import(name);}catch{return import(pathToFileURL(path.join(runtime,entry)).href);}}
const {marked,Renderer}=await dependency('marked','marked/lib/marked.esm.js');
const {instance}=await dependency('@viz-js/viz','@viz-js/viz/dist/viz.js');
const viz=await instance();
const sourcePath=path.resolve(root,'..',config.source);
const source=fs.readFileSync(sourcePath,'utf8');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sections=new Map([['intro',{id:'intro',title:'원문 읽기 안내와 조사 범위',lines:[]}]]);
let current=sections.get('intro'),fenced=false,firstTitle=true;
for(const line of source.split(/\r?\n/)){
 if(/^```/.test(line))fenced=!fenced;
 if(!fenced&&firstTitle&&/^# /.test(line)){firstTitle=false;continue;}
 if(!fenced&&/^# 공식 출처/.test(line)){current={id:'references',title:line.slice(2),lines:[]};sections.set('references',current);continue;}
 if(!fenced&&/^# (?:PART|Part|부|제\s*\d+부)/i.test(line)&&!/^# 부록/.test(line))continue;
 let match=!fenced&&line.match(/^## (\d+)[.．]\s*(.*)/);
 if(match){const id=match[1];if(sections.has(id))throw Error('Duplicate source chapter '+id);current={id,title:line.slice(3),lines:[]};sections.set(id,current);continue;}
 if(!fenced&&/^#{1,2} 부록/.test(line)){const key=line.match(/^#{1,2} 부록\s*([A-Z])/i)?.[1];if(!key)throw Error('Unrecognized appendix '+line);const id='appendix-'+key.toLowerCase();current={id,title:line.replace(/^#{1,2} /,''),lines:[]};sections.set(id,current);continue;}
 current.lines.push(line);
}
const numbered=[...sections.keys()].filter(id=>/^\d+$/.test(id));
if(numbered.length!==config.chapterCount)throw Error(`Source has ${numbered.length} numbered chapters; expected ${config.chapterCount}`);
const refs=new Map();
for(const line of source.split(/\r?\n/)){
 const def=line.match(/^\[([^\]]+)\]:\s*(https?:\/\/\S+)/);
 if(def)refs.set(def[1],def[2]);
 const item=line.match(/\*\*\[([A-Z]+\d+)\][^\n]*?(https?:\/\/\S+)/);
 if(item)refs.set(item[1],item[2].replace(/[)）。，;]+$/,''));
 const row=line.match(/^\|\s*\[?([A-Z]+\d+)\]?\s*\|.*?\]\((https?:\/\/[^)]+)\)/);
 if(row)refs.set(row[1],row[2]);
}
for(const [id,url] of Object.entries(config.references||{}))refs.set(id,url);
function linkCitations(md){let inside=false;return md.split('\n').map(line=>{
 if(/^```/.test(line)){inside=!inside;return line;}
 if(inside||/^\[[^\]]+\]:/.test(line))return line;
 return line.replace(/\[([^\]\n]*\b[A-Z]+\d+[^\]\n]*)\](?!\()/g,(all,items)=>{
  const ids=items.match(/\b[A-Z]+\d+\b/g)||[];
  if(!ids.length||!ids.every(id=>refs.has(id)))return all;
  return items.replace(/\b[A-Z]+\d+\b/g,id=>`[\[${id}\]](${refs.get(id)})`);
 });
}).join('\n');}
fs.mkdirSync(path.join(root,'assets'),{recursive:true});
let prefix='',headingCount=0,localToc=[],diagramCount=0,codeCount=0;
const diagrams=[],codeRecords=[];
const wrap=label=>label.replaceAll('\\n','\n').split('\n').flatMap(line=>{
 const out=[];let row='';for(const word of line.split(/\s+/)){if(row.length+word.length>21&&row){out.push(row);row=word;}else row+=(row?' ':'')+word;}if(row)out.push(row);return out;
}).join('\n');
function parseFlow(raw){
 const nodes=new Map(),edges=[],clusters=[],stack=[];
 const patterns=/\b([A-Za-z_][\w]*)(\[\(([^\]]*?)\)\]|\(\[(.*?)\]\)|\(\((.*?)\)\)|\[([^\]]*?)\]|\{(.*?)\})/g;
 for(const line of raw.split('\n').slice(1).filter(l=>l.trim()&&!l.trim().startsWith('%%'))){
  const cluster=line.trim().match(/^subgraph\s+(\w+)\[(.+)\]$/);if(cluster){clusters.push({id:cluster[1],label:cluster[2]});stack.push(cluster[1]);continue;}
  if(line.trim()==='end'){if(!stack.length)throw Error('Unexpected subgraph end');stack.pop();continue;}
  let clean=line.replace(patterns,(_,id,shape,db,stadium,circle,box,diamond)=>{nodes.set(id,{id,label:(db??stadium??circle??box??diamond).replace(/^"|"$/g,''),cluster:stack.at(-1),shape:db!==undefined?'cylinder':circle!==undefined||stadium!==undefined?'ellipse':diamond!==undefined?'diamond':'box'});return id;}).trim().replace(/;$/,'');
  while(clean){
   const m=clean.match(/^(\w+)\s*(<-->|-->|-\.->|--\s+(.+?)\s+-->|-\.\s+(.+?)\s+\.->)\s*(?:\|([^|]+)\|\s*)?(\w+)(.*)$/);
   if(!m)throw Error('Unsupported Mermaid flow line: '+line);
   edges.push({from:m[1],to:m[6],label:m[5]||m[3]||m[4]||'',both:m[2]==='<-->',dashed:m[2].includes('.')});
   clean=m[7].trim()?m[6]+m[7]:'';
  }
 }
 for(const e of edges)for(const id of [e.from,e.to])if(!nodes.has(id))nodes.set(id,{id,label:id,shape:'box'});
 return {nodes:[...nodes.values()],edges,clusters};
}
function svgFlow(graph,title){
 const q=JSON.stringify;
 const dot=`digraph G { graph [rankdir=TB,bgcolor="transparent",pad=0.2,nodesep=0.28,ranksep=0.48]; node [shape=box,style="rounded,filled",fillcolor="#f4f7f2",color="#a1b5a7",fontname="Malgun Gothic",fontcolor="#273f32",fontsize=14,margin="0.15,0.14"]; edge [fontname="Malgun Gothic",fontsize=12,color="#5f7c6b",fontcolor="#3d6049",arrowsize=0.7]; ${graph.nodes.map(n=>{let label=wrap(n.label),len=Math.max(...label.split('\n').map(l=>[...l].reduce((a,c)=>a+(c.charCodeAt(0)>255?1.6:1),0)));return `${n.id}[label=${q(label)},shape=${n.shape},width=${Math.max(1.6,len*.108).toFixed(2)}];`;}).join('\n')}${graph.edges.map(e=>`${e.from}->${e.to}[label=${q(e.label)}${e.both?',dir=both':''}${e.dashed?',style=dashed':''}];`).join('\n')}}`;
 const clustered=dot.slice(0,-1)+(graph.clusters||[]).map(c=>`subgraph cluster_${c.id}{label=${q(c.label)};fontname="Malgun Gothic";fontsize=13;color="#b8c8b4";${graph.nodes.filter(n=>n.cluster===c.id).map(n=>n.id+';').join('')}}`).join('')+'}';
 let svg=viz.renderString(clustered,{format:'svg'}).replace(/<\?xml[^>]*\?>\s*/,'').replace(/<!DOCTYPE[\s\S]*?>\s*/,'');
 const description=graph.edges.map(e=>`${graph.nodes.find(n=>n.id===e.from).label} ${e.both?'↔':'→'} ${e.label?'('+e.label+') ':''}${graph.nodes.find(n=>n.id===e.to).label}`).join(' / ');
 return svg.replace('<svg ','<svg role="img" aria-labelledby="diagram-title diagram-description" ').replace(/<title>[^<]*<\/title>/,`<title id="diagram-title">${esc(title)}</title><desc id="diagram-description">${esc(description)}</desc>`);
}
function sequence(raw){
 const actors=new Map(),rows=[];let level=0,count=0;
 for(const line of raw.split('\n').slice(1).map(l=>l.trim()).filter(Boolean)){
  const actor=line.match(/^participant\s+(\w+)(?:\s+as\s+(.+))?$/);if(actor){actors.set(actor[1],actor[2]||actor[1]);continue;}
  if(line==='end'){level=Math.max(0,level-1);rows.push(`<tr class="sequence-control"><td colspan="3">${'↳ '.repeat(level)}구간 종료</td></tr>`);continue;}
  const control=line.match(/^(loop|alt|else|opt|par|and|rect)\s*(.*)$/);if(control){const names={loop:'반복',alt:'조건 분기',else:'다른 분기',opt:'조건부 처리',par:'병렬',and:'병렬 분기',rect:'구간'};rows.push(`<tr class="sequence-control"><td colspan="3">${'↳ '.repeat(level)}${names[control[1]]}：${esc(control[2])}</td></tr>`);if(!['else','and'].includes(control[1]))level++;continue;}
  const note=line.match(/^Note\s+(.+?):\s*(.*)$/i);if(note){rows.push(`<tr class="sequence-control"><td colspan="3">참고 · ${esc(note[2])}</td></tr>`);continue;}
  const message=line.match(/^(\w+)\s*(--?>>|--?>)\s*(\w+)\s*:\s*(.*)$/);if(!message)throw Error('Unsupported Mermaid sequence line: '+line);
  count++;rows.push(`<tr><td>${count}</td><td>${esc(actors.get(message[1])||message[1])} → ${esc(actors.get(message[3])||message[3])}</td><td>${esc(message[4])}</td></tr>`);
 }
 return {count,html:`<div class="table-scroll" tabindex="0" role="region" aria-label="호출 순서도"><table class="sequence"><thead><tr><th>순서</th><th>호출자 → 수신자</th><th>전달 내용</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`};
}
function diagram(raw){const n=++diagramCount,title=config.diagramTitles?.[n-1]||`원문 ${prefix}장 실행 흐름`,isSequence=raw.startsWith('sequenceDiagram');let drawing,record;
 if(isSequence){const seq=sequence(raw);drawing=seq.html;record={number:n,type:'sequence',messages:seq.count};}
 else{const graph=parseFlow(raw);const file=`assets/diagram-${n}.svg`;fs.writeFileSync(path.join(root,file),svgFlow(graph,title));drawing=`<p class="scroll-hint">넓은 도식은 가로로 이동하며 읽을 수 있습니다. <a href="${file}" target="_blank" rel="noopener">도식 크게 보기 ↗</a></p><div class="diagram-scroll" tabindex="0" role="region" aria-label="${esc(title)}"><img src="${file}" alt="${esc(title)}. 연결 방향과 분기 조건은 아래 원문에도 보존되어 있습니다."></div>`;record={number:n,type:'flow',file,nodes:graph.nodes.length,edges:graph.edges.length};}
 diagrams.push({...record,chapter:prefix,title});
 return `<figure class="diagram" data-source-diagram="${n}"><figcaption><span>그림 ${n}</span> ${esc(title)}</figcaption>${drawing}<p class="figure-note">원문에 수록된 학습용 도식입니다. ${isSequence?'호출 순서와 반복·분기 조건을 표 형태의 순서도로 보존했습니다.':'노드·화살표·분기 라벨을 보존해 다시 배치했습니다.'} 세부 조건과 예시·구현의 구분은 앞뒤 본문을 함께 읽으세요.</p><details class="diagram-original"><summary>도식 원문 보기 (Mermaid)</summary><pre><code>${esc(raw)}</code></pre></details></figure>`;
}
const renderer=new Renderer();
renderer.heading=function({tokens,depth,text}){const clean=text.replaceAll('`','');const id=`s-${prefix}-${++headingCount}`;const d=Math.max(2,depth);if(d===2)localToc.push({id,label:clean});return `<h${d} id="${id}">${this.parser.parseInline(tokens)}<a class="anchor" href="#${id}" aria-label="이 절의 고유 링크">#</a></h${d}>\n`;};
renderer.code=function({text,lang}){
 codeCount++;codeRecords.push({chapter:prefix,language:lang||'text',hash:createHash('sha256').update(text).digest('hex')});
 if(lang==='mermaid')return diagram(text);
 let label=/의사코드|pseudo|conceptual_|simplified_/i.test(text)?'설명용 의사코드':/재구성|단순화|비문자적/.test(text)?'핵심 구조를 재구성한 예시':/^(bash|sh|powershell|console)$/.test(lang||'')?'원문 수록 명령 예시 · 실행 미검증':'원문 수록 코드 · 구분과 제약은 본문 참조';
 return `<div class="code-block"><div class="code-caption"><span>${label}</span><span>${esc(lang||'text')}</span></div><pre tabindex="0" aria-label="${label}"><code>${esc(text)}</code></pre></div>`;
};
const table=renderer.table.bind(renderer);renderer.table=token=>`<div class="table-scroll" tabindex="0" role="region" aria-label="비교 및 설명 표">${table(token)}</div>`;
const usedSections=[];
function renderSection(id){const section=sections.get(String(id));if(!section)throw Error('Missing chapter '+id);if(usedSections.includes(String(id)))throw Error('Source section included twice '+id);usedSections.push(String(id));prefix=String(id);headingCount=0;
 let html=marked.parse(linkCitations(`## ${section.title}\n\n${section.lines.join('\n')}`),{renderer});
 // 한글 조사와 붙어 있는 원문 강조 표시도 보존한다. 코드 블록은 변형하지 않는다.
 html=html.split(/(<pre[\s\S]*?<\/pre>)/g).map((part,i)=>i%2?part:part.replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>')).join('');
 html=html.replace(/<a href="(https?:[^\"]+)"/g,'<a href="$1" target="_blank" rel="noopener noreferrer"');
 return `<section class="source-section" data-source-chapter="${id}">${html}</section>`;
}
const pages=[{slug:'index',title:'학습 안내',short:'학습 안내'},...config.units,...config.referencesPages];
function sidebar(active){let group='';return `<aside class="sidebar" id="book-nav"><a class="book-title" href="index.html"><span class="book-mark" aria-hidden="true">${esc(config.mark)}</span><span>${esc(config.name)}<small>개인 학습 교재</small></span></a><nav aria-label="교재 목차"><a class="nav-intro ${active==='index'?'current':''}" ${active==='index'?'aria-current="page"':''} href="index.html">학습 안내</a>${config.units.map((u,i)=>{const heading=group!==u.group?`<p class="nav-group">${esc(u.group)}</p>`:'';group=u.group;return heading+`<a href="${u.slug}.html" ${active===u.slug?'class="current" aria-current="page"':''}><span class="nav-number">${String(i+1).padStart(2,'0')}</span><span>${esc(u.short)}</span></a>`;}).join('')}<p class="nav-group">참고 자료</p>${config.referencesPages.map(p=>`<a href="${p.slug}.html" ${p.slug===active?'class="current" aria-current="page"':''}>${esc(p.short)}</a>`).join('')}</nav><div class="book-meta"><span>${esc(config.versionLabel)}</span><a href="../${encodeURIComponent(config.source)}">학습 원문 ↗</a></div></aside>`;}
function layout(page,body,toc){const at=pages.indexOf(page),prev=pages[at-1],next=pages[at+1];return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(config.name)}의 원리·구현·한계를 배우는 개인 학습 교재"><title>${esc(page.title)} — ${esc(config.name)}</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="site.js" defer></script></head><body><a class="skip-link" href="#main">본문으로 건너뛰기</a><header class="mobile-header"><a href="index.html">${esc(config.name)}</a><button id="menu-button" aria-controls="book-nav" aria-expanded="false">목차 열기</button></header>${sidebar(page.slug)}<div class="reading-layout"><main id="main" tabindex="-1"><div class="breadcrumb"><a href="index.html">${esc(config.name)}</a><span aria-hidden="true">/</span><span>${esc(page.short)}</span></div>${body}<nav class="page-nav" aria-label="이전 다음 단원">${prev?`<a href="${prev.slug}.html"><small>이전 단원</small>← ${esc(prev.short)}</a>`:'<span></span>'}${next?`<a class="next" href="${next.slug}.html"><small>다음 단원</small>${esc(next.short)} →</a>`:'<a class="next" href="index.html"><small>처음으로</small>학습 안내 →</a>'}</nav><footer>${esc(config.name)} 개인 학습 교재<span>원문 기반 편집 / 프레임워크 설치·실행 미검증</span><a href="sources.html">출처와 검증 범위</a></footer></main><aside class="local-toc"><nav aria-label="이 페이지의 내용"><p>이 페이지에서</p>${toc.map(t=>`<a href="#${t.id}">${esc(t.label)}</a>`).join('')}</nav></aside></div></body></html>`;}
function save(page,body,toc=localToc){fs.writeFileSync(path.join(root,page.slug+'.html'),layout(page,body,toc));}
const start=`<header class="chapter-header"><p class="eyebrow">AGENT FRAMEWORK STUDY / READING GUIDE</p><h1>${esc(config.name)}<br>이해하기</h1><p class="lead">${config.lead}</p><div class="chapter-meta">${esc(config.versionLabel)}</div></header><section id="big-picture"><h2>먼저 잡을 큰 그림</h2>${config.overview}<p class="source-note">학습 원문을 근거로 재구성한 안내입니다. <a href="sources.html">원문의 근거 표기와 검증 범위</a>를 함께 확인하세요.</p></section><section id="distinctions"><h2>서로 구분하며 읽을 개념</h2><dl class="key-distinctions">${config.distinctions.map(([title,text])=>`<div><dt>${esc(title)}</dt><dd>${esc(text)}</dd></div>`).join('')}</dl></section><section id="reading-order"><h2>개념에서 적용 판단까지</h2><p>처음 읽을 때는 아래 순서로 진행하고, 다시 찾아볼 때는 목차의 단원으로 이동하세요. 단원 도입에서 개념을 연결한 다음 원문의 상세 설명과 조건을 이어 읽을 수 있습니다.</p><ol class="unit-list">${config.units.map((u,i)=>`<li><a href="${u.slug}.html"><span class="unit-number">${String(i+1).padStart(2,'0')}</span><span><b>${esc(u.title)}</b><small>${esc(u.subtitle)}</small></span><span class="unit-arrow" aria-hidden="true">→</span></a></li>`).join('')}</ol></section><section id="scope"><h2>이 교재의 범위</h2><p>상위 폴더의 <a href="../${encodeURIComponent(config.source)}">${esc(config.source)}</a>를 바탕으로 편집했습니다. 본문·코드·표·출처와 원문의 제약을 보존하며, 도식은 로컬에서 읽을 수 있도록 다시 표시합니다.</p><p class="callout">${esc(config.scope)} 이번 웹페이지 제작은 원문의 편집·표시 작업입니다. 최신 API나 구현을 추가 조사한 것으로 간주하지 않으며, 실제 설치·모델 호출·벤치마크는 수행하지 않았습니다.</p></section>`;
save(pages[0],start,[{id:'big-picture',label:'큰 그림'},{id:'distinctions',label:'개념의 차이'},{id:'reading-order',label:'읽기 순서'},{id:'scope',label:'범위와 한계'}]);
for(const [i,unit] of config.units.entries()){
 localToc=[];const body=unit.chapters.map(renderSection).join('\n');
 save(unit,`<header class="chapter-header"><p class="eyebrow">${esc(unit.group)} / 단원 ${String(i+1).padStart(2,'0')}</p><h1>${esc(unit.title)}</h1><p class="lead">${esc(unit.subtitle)}</p><div class="chapter-meta">원문 ${unit.chapters[0]}–${unit.chapters.at(-1)}장</div></header><section class="unit-intro" id="overview"><h2>먼저 연결해 보기</h2>${unit.intro}<p class="reading-question"><strong>읽는 관점</strong>${esc(unit.focus)}</p></section>${body}<div class="next-bridge"><p>${esc(unit.bridge||'핵심 개념을 정리한 뒤 다음 단원에서 실행·저장·검증의 경계를 이어 확인하세요.')}</p></div>`,[{id:'overview',label:'먼저 연결해 보기'},...localToc]);
}
for(const page of config.referencesPages){localToc=[];const body=page.chapters.map(renderSection).join('\n');save(page,`<header class="chapter-header"><p class="eyebrow">참고 자료 / REFERENCE</p><h1>${esc(page.title)}</h1><p class="lead">${esc(page.subtitle)}</p></header>${page.slug==='sources'?`<div class="callout"><strong>원문의 조사·버전 기준을 확인하세요.</strong><p>${esc(config.versionLabel)}. 공식 자료에 대한 원문의 조사 결과와 직접 실행해서 확인해야 할 조건을 구분합니다. 이번 페이지 제작에서 최신 구현을 추가 검증하지 않았습니다.</p></div>`:''}${body}`);}
const expected=[...sections.keys()];if(usedSections.length!==expected.length||expected.some(id=>!usedSections.includes(id)))throw Error('Not all original sections were assigned');
const expectedDiagrams=[...source.matchAll(/^```mermaid\s*$/gm)].length;
if(diagramCount!==expectedDiagrams)throw Error('Source diagrams missing');
const expectedCodes=marked.lexer(source).filter(t=>t.type==='code').length;
if(codeCount!==expectedCodes)throw Error(`Source code blocks missing: ${codeCount}/${expectedCodes}`);
fs.writeFileSync(path.join(root,'assets/favicon.svg'),`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#285d4d"/><text x="12" y="45" font-family="Georgia,serif" font-size="37" fill="white">${esc(config.mark)}</text></svg>`);
const report={name:config.name,source:'../'+config.source,sourceSha256:createHash('sha256').update(source).digest('hex'),sourceSections:expected,sourceCodes:expectedCodes,sourceDiagrams:expectedDiagrams,pages:pages.map(p=>p.slug+'.html'),mapping:[...config.units,...config.referencesPages].map(p=>({page:p.slug+'.html',chapters:p.chapters.map(String)})),references:Object.fromEntries(refs),codeBlocks:codeRecords,diagrams};
fs.writeFileSync(path.join(root,'content-map.json'),JSON.stringify(report,null,2)+'\n');
console.log(`Built ${pages.length} pages, ${expected.length} source sections, ${codeCount} code blocks, ${diagramCount} diagrams.`);

// 기본 교재를 재생성해도 2차 과정 탐색을 유지한다.
await import('./link-courses.mjs');
