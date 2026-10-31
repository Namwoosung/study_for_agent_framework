import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import config from './site.config.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
const hash=s=>createHash('sha256').update(s).digest('hex');
const runtime=path.join(process.env.USERPROFILE||'','.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
async function dependency(n,e){try{return await import(n);}catch{return import(pathToFileURL(path.join(runtime,e)).href);}}
const {marked,Renderer}=await dependency('marked','marked/lib/marked.esm.js');
const {instance}=await dependency('@viz-js/viz','@viz-js/viz/dist/viz.js');
const viz=await instance();
const sourcePath=path.resolve(root,'../..',config.source),original=fs.readFileSync(sourcePath,'utf8'),source=original.replaceAll('\r\n','\n');
const lines=source.split('\n');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const plain=s=>s.replace(/[`*_]/g,'').trim();
const refs=new Map();
for(const l of lines){
 const def=l.match(/^\[([^\]]+)\]:\s*(https?:\/\/\S+)/);if(def)refs.set(def[1],def[2]);
 if(l.startsWith('|')){const cells=l.split('|');const ids=(cells[1]||'').match(/\b[A-Z]+\d+\b/g)||[];const url=l.match(/https?:\/\/[^\s)<>|]+/);if(url)for(const id of ids)refs.set(id,url[0]);}
}
const definitions='\n\n'+[...refs].map(([id,url])=>`[${id}]: ${url}`).join('\n');
function citations(md){let fence=false;return md.split('\n').map(l=>{
 if(/^\s*```/.test(l)){fence=!fence;return l;}if(fence||/^\[[^\]]+\]:/.test(l))return l;
 return l.replace(/https?:\/\/[^\s<]+|`[^`\n]*`|\[[^\]\n]*\]\([^\n)]*\)|\[[^\]\n]*\]\[[^\]\n]*\]|\[[^\]\n]*\b[A-Z]+\d+[^\]\n]*\]|\b[A-Z]+\d+\b/g,m=>{
  if(m.startsWith('http')||m.startsWith('`')||/\]\(/.test(m))return m;
  if(/\]\[/.test(m)){const pair=m.match(/^\[([^\]]+)\]\[([^\]]+)\]$/);if(!pair||!/^\*{0,2}[A-Z]+\d+\*{0,2}$/.test(pair[1]))return m;}
  return m.replace(/\b[A-Z]+\d+\b/g,id=>refs.has(id)?`[${id}](${refs.get(id)})`:id);
 });
}).join('\n');}

// 원문의 행을 연속 범위로 나누며, 본문을 추출·요약으로 대체하지 않는다.
const starts=[{start:0,id:'intro',title:'원문 읽기 안내와 증거 기준',group:'읽기 안내'}];
let fence=false,pendingPart=null,currentPart='심층 본문';const sourceHeadings=[];
for(let i=0;i<lines.length;i++){
 const l=lines[i];if(/^\s*```/.test(l)){fence=!fence;continue;}if(fence)continue;
 const h=l.match(/^(#{1,6})\s+(.+?)\s*$/);if(!h)continue;
 sourceHeadings.push({line:i+1,depth:h[1].length,text:h[2],id:`line-${i+1}`});
 if(/^# Part\s/i.test(l)){pendingPart=i;currentPart=plain(h[2]);continue;}
 const m=h[1].length===config.majorDepth&&h[2].match(/^((?:\d+(?:\.\d+)?|W\d+))\.\s+/);
 const final=i>0&&h[1].length<=config.majorDepth&&/^(최종 요약|마지막 정리)/.test(h[2]);
 if(m||final){starts.push({start:pendingPart??i,id:m?m[1]:'final',title:h[2],group:currentPart});pendingPart=null;}
}
const major=starts.filter(s=>/^\d+$/.test(s.id));if(major.length!==config.chapterCount)throw Error(`Chapter count ${major.length}/${config.chapterCount}`);
const pieces=[];
for(let i=0;i<starts.length;i++){
 const s=starts[i],end=starts[i+1]?.start??lines.length;
 const whole=lines.slice(s.start,end).join('\n');
 const cuts=[s.start];
 const workbook=/워크북/.test(s.title)||config.groups.some(g=>g.ids.includes(s.id)&&/워크북/.test(g.title));
 if(whole.length>config.splitAt||(workbook&&whole.length>3500)){
  let last=s.start,f=false;
  for(let j=s.start;j<end;j++){
   if(/^\s*```/.test(lines[j])){f=!f;continue;}
   if(!f&&new RegExp(`^#{${config.majorDepth+1}} `).test(lines[j])&&lines.slice(last,j).join('\n').length>(workbook?1500:2800)){cuts.push(j);last=j;}
  }
 }
 cuts.push(end);
 for(let j=0;j<cuts.length-1;j++){
  const start=cuts[j],stop=cuts[j+1],raw=lines.slice(start,stop).join('\n');
  const sub=sourceHeadings.find(h=>h.line-1>=start&&h.line-1<stop&&h.depth===config.majorDepth+1);
  const group=config.groups.find(g=>g.ids.includes(s.id))||{title:s.id==='final'?'최종 정리':s.group,intro:'원문의 설명과 코드·표를 따라 실행 주체와 상태 변경, 종료·실패 경계를 확인합니다.',focus:'기능의 존재와 실제 실행·저장·인가의 보장 범위를 구분하세요.'};
  pieces.push({...s,start,end:stop,raw,key:`${s.id}-${j+1}`,continuation:j>0,title:j>0?`${s.title} / ${sub?.text||'이어 읽기'}`:s.title,guide:group});
 }
}
const units=[];
for(const piece of pieces){
 const prev=units.at(-1);
 if(prev&&piece.id!=='intro'&&piece.id!=='final'&&prev.parts[0].id!=='intro'&&prev.group===piece.guide.title&&prev.chars+piece.raw.length<config.pageBudget&&!piece.continuation&&!prev.parts.some(p=>p.continuation)){
  prev.parts.push(piece);prev.chars+=piece.raw.length;
 }else units.push({parts:[piece],group:piece.guide.title,guide:piece.guide,chars:piece.raw.length});
}
for(const [i,u]of units.entries()){
 u.slug=`unit-${String(i+1).padStart(2,'0')}`;
 u.title=plain(u.parts[0].title);u.summary=u.parts.map(p=>plain(p.title)).join(' / ');
 u.label=u.title.replace(/^(?:\d+(?:\.\d+)?|W\d+)\.\s*/,'');
 if(u.parts.length>1)u.label+=` 외 ${u.parts.length-1}개 주제`;
 u.minutes=Math.max(2,Math.ceil(u.chars/650));
}
const headingLocations=new Map();for(const h of sourceHeadings){const u=units.find(u=>u.parts.some(p=>h.line-1>=p.start&&h.line-1<p.end));headingLocations.set(h.id,u.slug+'.html#'+h.id);}
const githubSlug=s=>plain(s).toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu,'').replace(/\s/g,'-');
const anchors=new Map();for(const h of sourceHeadings){const slug=githubSlug(h.text);if(!anchors.has(slug))anchors.set(slug,headingLocations.get(h.id));}
fs.mkdirSync(path.join(root,'assets'),{recursive:true});
const diagrams=[],codeBlocks=[],sectionRecords=[];let headingQueue=[],section=null;
function wrap(s){return s.replaceAll('\\n','\n').split('\n').flatMap(l=>{const rows=[];let row='';for(const w of l.split(/\s+/)){if(row.length+w.length>23&&row){rows.push(row);row=w;}else row+=(row?' ':'')+w;}if(row)rows.push(row);return rows;}).join('\n');}
function flow(raw){
 const nodes=new Map(),edges=[];
 if(raw.startsWith('stateDiagram')){
  for(const l of raw.split('\n').slice(1).map(l=>l.trim()).filter(Boolean)){
   const m=l.match(/^(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)(?:\s*:\s*(.+))?$/);if(!m)throw Error('Unsupported state line '+l);
   const from=m[1]==='[*]'?'START':m[1],to=m[2]==='[*]'?'STOP':m[2];
   for(const [id,label]of [[from,from==='START'?'시작':from],[to,to==='STOP'?'종료':to]])if(!nodes.has(id))nodes.set(id,{id,label,shape:['START','STOP'].includes(id)?'ellipse':'box'});
   edges.push({from,to,label:m[3]||'',both:false,dashed:false});
  }
 }else{
  const shapes=/\b([A-Za-z_][\w]*)(\[\(([^\]]*?)\)\]|\(\[(.*?)\]\)|\(\((.*?)\)\)|\[([^\]]*?)\]|\{(.*?)\})/g;
  for(const l of raw.split('\n').slice(1).filter(l=>l.trim()&&!l.trim().startsWith('%%'))){
   let clean=l.replace(shapes,(_,id,shape,db,stadium,circle,box,diamond)=>{nodes.set(id,{id,label:(db??stadium??circle??box??diamond).replace(/^"|"$/g,''),shape:db!==undefined?'cylinder':circle!==undefined||stadium!==undefined?'ellipse':diamond!==undefined?'diamond':'box'});return id;}).trim().replace(/;$/,'');
   while(clean){const m=clean.match(/^(\w+)\s*(<-->|-->|-\.->|--\s+(.+?)\s+-->|-\.\s+(.+?)\s+\.->)\s*(?:\|([^|]+)\|\s*)?(\w+)(.*)$/);if(!m)throw Error('Unsupported flow '+l);edges.push({from:m[1],to:m[6],label:m[5]||m[3]||m[4]||'',both:m[2]==='<-->',dashed:m[2].includes('.')});clean=m[7].trim()?m[6]+m[7]:'';}
  }
  for(const e of edges)for(const id of [e.from,e.to])if(!nodes.has(id))nodes.set(id,{id,label:id,shape:'box'});
 }
 const q=JSON.stringify;
 const dot=`digraph G{graph[rankdir=TB,bgcolor="transparent",pad=.25,nodesep=.35,ranksep=.5];node[style="rounded,filled",fillcolor="#f4f7f2",color="#a1b5a7",fontname="Malgun Gothic",fontcolor="#273f32",fontsize=15,margin=".16,.15"];edge[fontname="Malgun Gothic",fontsize=13,color="#5f7c6b",fontcolor="#3d6049",arrowsize=.7];${[...nodes.values()].map(n=>`${q(n.id)}[shape=${n.shape},label=${q(wrap(n.label))}];`).join('')}${edges.map(e=>`${q(e.from)}->${q(e.to)}[label=${q(e.label)}${e.both?',dir=both':''}${e.dashed?',style=dashed':''}];`).join('')}}`;
 return {nodes:[...nodes.values()],edges,svg:viz.renderString(dot,{format:'svg'}).replace(/<\?xml[^>]*\?>\s*/,'').replace(/<!DOCTYPE[\s\S]*?>\s*/,'')};
}
function sequence(raw){const actors=new Map(),rows=[];let level=0,count=0;const events=[];
 for(const l of raw.split('\n').slice(1).map(l=>l.trim()).filter(Boolean)){
  if(l==='autonumber')continue;
  const actor=l.match(/^participant\s+(\w+)(?:\s+as\s+(.+))?$/);if(actor){actors.set(actor[1],actor[2]||actor[1]);continue;}
  const ctrl=l.match(/^(loop|alt|else|opt|par|and|end)\b\s*(.*)$/);
  if(ctrl){if(ctrl[1]==='end')level=Math.max(0,level-1);rows.push(`<tr class="sequence-control"><td colspan="3">${'↳ '.repeat(level)}<b>${esc(ctrl[1])}</b> ${esc(ctrl[2])}</td></tr>`);if(['loop','alt','opt','par'].includes(ctrl[1]))level++;events.push({type:'control',text:l});continue;}
  const note=l.match(/^Note\s+(.+?):\s*(.*)$/i);if(note){rows.push(`<tr class="sequence-control"><td colspan="3">참고 · ${esc(note[1])}：${esc(note[2])}</td></tr>`);events.push({type:'note',text:l});continue;}
  const m=l.match(/^(\w+)\s*(--?>>|--?>)\s*(\w+)\s*:\s*(.*)$/);if(!m)throw Error('Unsupported sequence '+l);
  rows.push(`<tr><td>${++count}</td><td>${esc(actors.get(m[1])||m[1])} ${m[2].startsWith('--')?'⇢':'→'} ${esc(actors.get(m[3])||m[3])}</td><td>${esc(m[4])}</td></tr>`);events.push({type:'message',from:m[1],to:m[3],arrow:m[2],text:m[4]});
 }
 return {actors:Object.fromEntries(actors),events,html:`<div class="table-scroll" tabindex="0" role="region" aria-label="호출·분기 순서표"><table class="sequence"><thead><tr><th>순서</th><th>보내는 쪽 → 받는 쪽</th><th>호출 내용·조건</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`};
}
function diagram(raw){const number=diagrams.length+1,title=plain(headingQueue.previous?.text||section.title),sequenceKind=raw.startsWith('sequenceDiagram');let drawing,record;
 if(sequenceKind){const s=sequence(raw);drawing=s.html;record={type:'sequence',actors:s.actors,events:s.events};}
 else{const g=flow(raw),file=`assets/diagram-${number}.svg`;const description=g.edges.map(e=>`${g.nodes.find(n=>n.id===e.from).label} ${e.both?'↔':'→'} ${e.label?'('+e.label+') ':''}${g.nodes.find(n=>n.id===e.to).label}`).join(' / ');const svg=g.svg.replace('<svg ','<svg role="img" aria-labelledby="title description" ').replace(/<title>[^<]*<\/title>/,`<title id="title">${esc(title)}</title><desc id="description">${esc(description)}</desc>`);fs.writeFileSync(path.join(root,file),svg);drawing=`<p class="scroll-hint">가로로 이동해서 읽을 수 있습니다. <a href="${file}" target="_blank" rel="noopener">도식 크게 보기 ↗</a></p><div class="diagram-scroll" tabindex="0" role="region" aria-label="${esc(title)}"><img src="${file}" alt="${esc(title)}의 노드·분기·연결 관계"></div>`;record={type:raw.startsWith('stateDiagram')?'state':'flow',file,nodes:g.nodes,edges:g.edges};}
 diagrams.push({number,title,section:section.key,rawHash:hash(raw),...record});
 return `<figure class="diagram" data-diagram="${number}"><figcaption><span>도식 ${number}</span> ${esc(title)}</figcaption>${drawing}<p class="figure-note">원문의 학습용 도식입니다. ${sequenceKind?'호출 방향과 반복·분기·참고를 순서표로 보존했습니다. 실선 →와 점선 ⇢를 구분합니다.':'연결 방향·분기 조건·점선·쌍방향 연결을 보존해 세로로 배치했습니다.'} 실제 구현·의사코드·해석의 구분은 본문을 함께 읽으세요.</p><details class="diagram-original"><summary>도식 원문 보기 (Mermaid)</summary><pre><code>${esc(raw)}</code></pre></details></figure>`;
}
const renderer=new Renderer();
renderer.heading=function({tokens,depth,text}){
 const h=headingQueue.shift();if(!h||plain(h.text)!==plain(text))throw Error('Heading mismatch '+text);headingQueue.previous=h;
 const part=/^Part\s/i.test(h.text);if(part)return `<p class="part-divider" id="${h.id}">${this.parser.parseInline(tokens)}</p>`;
 let d=section.id==='intro'?Math.max(2,depth+1):Math.min(6,Math.max(2,depth+(config.majorDepth===1?1:0)));
 return `<h${d} id="${h.id}">${this.parser.parseInline(tokens)}<a class="anchor" href="#${h.id}" aria-label="이 절의 고유 링크">#</a></h${d}>`;
};
renderer.code=function({text,lang}){
 codeBlocks.push({section:section.key,language:lang||'text',hash:hash(text)});
 if(lang==='mermaid')return diagram(text);
 const label=/의사코드|PSEUDO|pseudo/i.test(text)||config.pseudoDefault?'학습용 의사코드·구조 예시 · 본문에서 실제 코드 여부 확인':/발췌|실제 코드|실제 소스/.test(text)?'원문 수록 코드 발췌 · 버전과 제약 확인':!lang||lang==='text'?'원문 흐름·데이터 예시':'원문 수록 코드 예시 · 실행 미검증';
 return `<div class="code-block"><div class="code-caption"><span>${label}</span><span>${esc(lang||'text')}</span></div><pre tabindex="0" aria-label="${label}"><code>${esc(text)}</code></pre></div>`;
};
const table=renderer.table.bind(renderer);renderer.table=t=>`<div class="table-scroll" role="region" aria-label="비교·분석 표" tabindex="0">${table(t)}</div>`;
const link=renderer.link.bind(renderer);renderer.link=function(t){if(t.href.startsWith('#')){const target=anchors.get(decodeURIComponent(t.href.slice(1)));if(target)t={...t,href:target};}return link(t).replace('<a ',/^https?:/.test(t.href)?'<a target="_blank" rel="noopener noreferrer" ':'<a ');};
renderer.html=({text})=>/^<!--/.test(text)?text:/^<br\s*\/?\s*>$/i.test(text.trim())?'<br>':esc(text);
function render(p){
 section=p;headingQueue=sourceHeadings.filter(h=>h.line-1>=p.start&&h.line-1<p.end);
 let html=marked.parse(citations(p.raw)+definitions,{renderer});
 if(headingQueue.length)throw Error('Unrendered source headings');
 // CommonMark의 한글 인접 강조 해석 차이는 코드 이외의 표시에서 보정한다.
 html=html.split(/(<pre[\s\S]*?<\/pre>|<code[\s\S]*?<\/code>)/g).map((s,i)=>i%2?s:s.replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>')).join('');
 const body=`${p.continuation?`<h2 class="continuation">${esc(plain(starts.find(s=>s.id===p.id).title))} · 이어 읽기</h2>`:''}${html}`;
 sectionRecords.push({key:p.key,chapter:p.id,startLine:p.start+1,endLine:p.end,rawHash:hash(p.raw),htmlHash:hash(body)});
 return `<section class="source-section" data-source-section="${p.key}">${body}</section>`;
}
const allThemes=[['hermes','Hermes Agent'],['OpenAI_Agents_SDK','OpenAI Agents SDK'],['PydanticAI','PydanticAI'],['Google_ADK','Google ADK'],['Claude_Agent_SDK','Claude Agent SDK'],['Claude_Code','Claude Code'],['Microsoft Agent_Framework','Microsoft Agent Framework']];
function sidebar(page){let group='';return `<aside class="sidebar" id="book-nav"><a class="book-title" href="index.html"><span class="book-mark">${esc(config.mark)}</span><span>${esc(config.name)}<small>2차 심층 학습 교재</small></span></a><nav aria-label="심층 교재 목차"><a href="index.html" ${page==='index'?'aria-current="page" class="current"':''}>심층 학습 안내</a>${units.map((u,i)=>{let g=u.group!==group?`<p class="nav-group">${esc(u.group)}</p>`:'';group=u.group;return g+`<a href="${u.slug}.html" ${page===u.slug?'aria-current="page" class="current"':''}><span class="nav-number">${String(i+1).padStart(2,'0')}</span><span>${esc(u.label)}</span></a>`;}).join('')}</nav><div class="book-meta"><a href="../index.html">← 1차 기본 교재</a><a href="../../${encodeURIComponent(config.source)}">2차 원문 Markdown ↗</a><span>${esc(config.version)}</span></div><nav class="other-books" aria-label="다른 주제의 심층 교재"><p class="nav-group">7개 심층 교재</p>${allThemes.map(([folder,name])=>`<a href="../../../${encodeURIComponent(folder)}/html/deep/index.html">${esc(name)}</a>`).join('')}</nav></aside>`;}
function layout(slug,title,body,toc=[],i=-1){const prev=units[i-1],next=units[i+1];return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${esc(config.name)} 2차 심층 학습: 실행·상태·실패·소스코드 분석"><title>${esc(title)} — ${esc(config.name)} 심층 학습</title><link rel="icon" href="../assets/favicon.svg"><link rel="stylesheet" href="../style.css"><link rel="stylesheet" href="deep.css"><script src="../site.js" defer></script></head><body><a class="skip-link" href="#main">본문으로 건너뛰기</a><header class="mobile-header"><a href="index.html">${esc(config.name)}<small>2차 심층 학습</small></a><button id="menu-button" aria-controls="book-nav" aria-expanded="false">목차 열기</button></header>${sidebar(slug)}<div class="reading-layout"><main id="main" tabindex="-1"><nav class="breadcrumb" aria-label="과정 위치"><a href="../index.html">1차 기본 교재</a><span>/</span><a href="index.html">2차 심층 교재</a></nav>${body}<nav class="page-nav" aria-label="이전 다음 단원">${prev?`<a href="${prev.slug}.html"><small>이전 단원</small>← ${esc(prev.label)}</a>`:slug!=='index'?'<a href="index.html"><small>처음으로</small>← 심층 학습 안내</a>':'<span></span>'}${next?`<a class="next" href="${next.slug}.html"><small>다음 단원</small>${esc(next.label)} →</a>`:slug==='index'?`<a class="next" href="${units[0].slug}.html"><small>심층 학습 시작</small>원문 읽기 안내 →</a>`:'<a class="next" href="index.html">심층 학습 안내로 →</a>'}</nav><footer>${esc(config.name)} · 2차 심층 학습<span>제공된 원문 전체를 분할·편집한 로컬 교재 / 실제 SDK 실행·성능 검증 미수행</span><a href="../../${encodeURIComponent(config.source)}">원문과 검증 한계 확인</a></footer></main><aside class="local-toc"><nav aria-label="이 페이지의 내용"><p>이 페이지에서</p>${toc.map(h=>`<a class="toc-depth-${h.depth}" href="#${h.id}">${esc(plain(h.text))}</a>`).join('')}</nav></aside></div></body></html>`;}
for(const [i,u]of units.entries()){
 const toc=sourceHeadings.filter(h=>u.parts.some(p=>h.line-1>=p.start&&h.line-1<p.end)&&!/^Part\s/i.test(h.text)&&h.depth<=config.majorDepth+1);
 const body=`<header class="chapter-header"><p class="eyebrow">SECOND STUDY / ${esc(u.group)}</p><h1>${esc(u.group)}</h1><div class="chapter-meta">단원 ${String(i+1).padStart(2,'0')} · ${esc(config.version)} · 약 ${u.minutes}분 · 원문 ${u.parts[0].start+1}–${u.parts.at(-1).end}행</div></header><section class="unit-intro"><h2>이번 단원의 읽는 관점</h2><p>${esc(u.guide.intro)}</p><p class="reading-question"><strong>살펴볼 경계</strong>${esc(u.guide.focus)}</p></section><details class="inline-toc"><summary>이 페이지의 세부 목차</summary><nav aria-label="본문 세부 목차">${toc.map(h=>`<a href="#${h.id}">${esc(plain(h.text))}</a>`).join('')}</nav></details>${u.parts.map(render).join('\n')}`;
 fs.writeFileSync(path.join(root,u.slug+'.html'),layout(u.slug,u.label,body,toc,i));
}
const home=`<header class="chapter-header"><p class="eyebrow">AGENT FRAMEWORK STUDY / SECOND STUDY</p><h1>${esc(config.name)}<br>2차 심층 학습</h1><p class="lead">${esc(config.lead)}</p><div class="chapter-meta">${esc(config.version)} · 원문 ${config.chapterCount}개 장 · ${units.length}개 읽기 단원</div></header><section id="approach"><h2>기능에서 실행 책임으로</h2><p>${esc(config.overview)}</p><p>1차 교재에서 객체와 기능을 익혔다면, 이번에는 <strong>요청 진입 → 모델 입력 → 도구 실행 → 상태 저장 → 종료·실패·복구</strong>를 연결해 읽습니다. 긴 워크북은 원문 소주제 경계에서 나눴으며, 설명·조건·코드·표·질문·출처를 요약으로 대체하지 않았습니다.</p><p class="callout">원문이 구분하는 공개 코드·공식 문서·설계 해석·의사코드·미검증 범위를 함께 읽으세요. 1차와 2차의 버전은 다를 수 있습니다. 이번 웹페이지 제작은 제공된 문서의 편집·표시이며 최신 API의 추가 조사나 실제 실행 검증이 아닙니다.</p></section><section id="distinctions"><h2>구분하면서 읽을 세 가지</h2><dl class="key-distinctions">${config.distinctions.map(([title,text])=>`<div><dt>${esc(title)}</dt><dd>${esc(text)}</dd></div>`).join('')}</dl></section><section id="reading-order"><h2>심층 학습 순서</h2><p>순서대로 읽거나 필요한 단원으로 이동하세요. 각 페이지의 세부 목차에서 소주제로 바로 이동할 수 있습니다. 읽기 시간은 원문 글자 수에 따른 대략적인 안내입니다.</p><ol class="unit-list">${units.map((u,i)=>`<li><a href="${u.slug}.html"><span class="unit-number">${String(i+1).padStart(2,'0')}</span><span><b>${esc(u.label)}</b><small>${esc(u.group)} · 약 ${u.minutes}분</small></span><span class="unit-arrow" aria-hidden="true">→</span></a></li>`).join('')}</ol></section><section id="source"><h2>원문과 기본 교재</h2><p><a href="../index.html">1차 기본 교재로 돌아가기</a></p><p><a href="../../${encodeURIComponent(config.source)}">${esc(config.source)}</a>의 모든 행을 연속 범위로 배치했습니다. 도식은 로컬 SVG와 호출·분기 표로 표시하고 원래 Mermaid도 함께 제공합니다. 외부 출처 링크 외에는 인터넷 연결이 필요하지 않습니다.</p></section>`;
fs.writeFileSync(path.join(root,'index.html'),layout('index','2차 심층 학습 안내',home,[{id:'approach',text:'학습 관점'},{id:'distinctions',text:'핵심 구분'},{id:'reading-order',text:'학습 순서'},{id:'source',text:'원문과 기본 교재'}]));
const manifest={name:config.name,source:'../../'+config.source,sourceHash:hash(original),normalizedHash:hash(source),lineCount:lines.length,chapterCount:major.length,headings:sourceHeadings,pages:['index.html',...units.map(u=>u.slug+'.html')],sections:sectionRecords,mapping:units.map(u=>({page:u.slug+'.html',sections:u.parts.map(p=>p.key)})),references:Object.fromEntries(refs),codeBlocks,diagrams};
fs.writeFileSync(path.join(root,'content-map.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(`Built ${config.name}: ${manifest.pages.length} pages, ${major.length} chapters, ${sectionRecords.length} source ranges, ${codeBlocks.length} fenced blocks, ${diagrams.length} diagrams.`);
const courseLink=path.resolve(root,'../link-courses.mjs');if(fs.existsSync(courseLink))await import(pathToFileURL(courseLink).href);
