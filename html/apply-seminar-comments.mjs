import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

const thisFile=fileURLToPath(import.meta.url),root=path.resolve(path.dirname(thisFile),'..');
const settings=JSON.parse(fs.readFileSync(path.join(root,'html/seminar-comments.json'),'utf8'));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cleanTitle=s=>s.replaceAll('`','');
const hash=s=>createHash('sha256').update(s).digest('hex');
export const stripSeminarAdditions=html=>html.replace(/<!-- seminar-addition:start\b[\s\S]*?<!-- seminar-addition:end -->/g,'');
const block=(id,html)=>`<!-- seminar-addition:start key="${id}" -->${html}<!-- seminar-addition:end -->`;
const href=(from,to)=>path.relative(path.dirname(from),to).split(path.sep).map(encodeURIComponent).join('/');
const globalId=(t,n)=>'seminar-'+t.folder.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-'+n.id;

function locations(t){
 const directory=path.join(root,t.folder,'html/deep');
 const m=JSON.parse(fs.readFileSync(path.join(directory,'content-map.json'),'utf8'));
 const original=fs.readFileSync(path.join(root,t.folder,t.source));
 if(hash(original)!==t.sourceHash||m.sourceHash!==t.sourceHash)throw Error('원문 변경 확인 필요: '+t.folder);
 const source=original.toString('utf8');
 return t.notes.map(n=>{
  const heading=m.headings.find(h=>h.line===n.anchorLine&&h.text===n.anchorTitle);
  if(!heading)throw Error('코멘트 기준 절 불일치: '+t.folder+' '+n.id);
  const section=m.sections.find(s=>s.startLine<=n.anchorLine&&s.endLine>=n.anchorLine);
  const page=m.mapping.find(p=>p.sections.includes(section.key)).page;
  const references=[...n.evidenceIds.map(id=>{if(!m.references[id])throw Error('없는 근거 ID '+t.folder+' '+id);return {label:id,url:m.references[id]};}),...n.evidenceUrls.map((url,i)=>{if(!source.includes(url))throw Error('원문 밖의 근거 '+url);return {label:'원문 출처 '+(i+1),url};})];
  return {...n,section:section.key,page,id:globalId(t,n),references,directory};
 });
}
function withStyle(file,html){return html.replace('</head>',block('seminar-style',`<link rel="stylesheet" href="${href(file,path.join(root,'html/seminar-comments.css'))}">`)+'</head>');}
function annotation(t,n,file){return block(n.id,`<aside class="seminar-comment" id="${n.id}" aria-labelledby="${n.id}-title"><p class="seminar-label">발표·실무 시사점 / 추가 해석 · 가상 사례</p><h3 id="${n.id}-title">${esc(n.title)}</h3><p class="seminar-takeaway"><strong>${esc(n.takeaway)}</strong></p>${n.paragraphs.map(p=>`<p>${esc(p)}</p>`).join('')}<p class="seminar-next"><strong>3차 확인 질문</strong>${esc(n.followup)}</p><p class="seminar-evidence">기술 설명의 근거: <a href="#line-${n.anchorLine}">${esc(cleanTitle(n.anchorTitle))}</a>${n.references.map(r=>` · <a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.label)}</a>`).join('')}<br><a href="${href(file,path.join(root,t.folder,t.companion))}">이 주제의 추가 코멘트 모아 읽기 (Markdown)</a></p></aside>`);}
function markdown(t,notes){
 return `# ${t.name} — 발표·실무 시사점 코멘트\n\n> 기존 학습 원문에서 도출한 추가 해석입니다. 반도체 사례는 가정이며, 실제 구축·성능 측정·제품의 추가 기능 검증이 아닙니다. 기존 원문은 수정하지 않았습니다.\n> 발표 위치: ${t.emphasis}. 1차의 공통 개념 재설명은 줄이고, 2차에는 구현 차이가 만드는 선택과 Trade-off를 짚습니다. 상세 운영 설계·검증은 3차 확인 질문으로 남깁니다.\n\n[2차 발표 흐름](../${encodeURIComponent(settings.flow)}) · [1차 발표 범위](../${encodeURIComponent(settings.blueprint)})\n\n`+notes.map((n,i)=>{
 const page='html/deep/'+n.page;
 return `## ${i+1}. ${n.title}\n\n**발표 핵심:** ${n.takeaway}\n\n**연결할 원문:** ${cleanTitle(n.anchorTitle)} — 원문 ${n.anchorLine}행, [교재의 추가 코멘트](${page}#${n.id})\n\n${n.paragraphs.join('\n\n')}\n\n**3차 확인 질문:** ${n.followup}\n\n**기술 근거:** [원문의 해당 절](${page}#line-${n.anchorLine})${n.references.map(r=>` · [${r.label}](${r.url})`).join('')}\n`;
 }).join('\n');
}
function applyTopic(t){
 const notes=locations(t),byPage=new Map();
 for(const n of notes){if(!byPage.has(n.page))byPage.set(n.page,[]);byPage.get(n.page).push(n);}
 for(const page of fs.readdirSync(notes[0].directory).filter(n=>n.endsWith('.html'))){
  const file=path.join(notes[0].directory,page),before=fs.readFileSync(file,'utf8');let html=stripSeminarAdditions(before);
  if(byPage.has(page)){
   for(const n of byPage.get(page)){
    const tag=`data-source-section="${n.section}"`,start=html.indexOf(tag),end=html.indexOf('</section>',start);
    if(start<0||end<0)throw Error('원문 영역을 찾을 수 없음 '+t.folder+' '+n.id);
    const at=end+'</section>'.length;
    html=html.slice(0,at)+annotation(t,n,file)+html.slice(at);
   }
   html=withStyle(file,html);
  }else if(page==='index.html'){
   const guide=block('seminar-topic-index',`<section class="seminar-comment-index" id="seminar-comments" aria-labelledby="seminar-comments-title"><p class="seminar-label">2차 발표를 위한 선택적 보완</p><h2 id="seminar-comments-title">발표·실무 시사점 ${notes.length}곳</h2><p>원문의 개념을 실제 도메인의 설계 판단에 연결하는 추가 해석입니다. 반도체 사례는 가정이며, 구현·실측 결과가 아닙니다. 1차 공통 개념을 되풀이하지 않고, 운영 상세는 3차 확인 질문으로 남깁니다.</p><ul>${notes.map(n=>`<li><a href="${n.page}#${n.id}">${esc(n.title)}</a></li>`).join('')}</ul><p><a href="${href(file,path.join(root,t.folder,t.companion))}">추가 코멘트만 모아 읽기 (Markdown)</a></p></section>`);
   const at=html.indexOf('<nav class="page-nav"');if(at<0)throw Error('단원 탐색 없음 '+file);
   html=withStyle(file,html.slice(0,at)+guide+html.slice(at));
  }
  if(stripSeminarAdditions(html)!==stripSeminarAdditions(before))throw Error('원본 HTML 변경 감지: '+file);
  if(html!==before)fs.writeFileSync(file,html);
 }
 fs.writeFileSync(path.join(root,t.folder,t.companion),markdown(t,notes));
 return notes.map(n=>({topic:t.name,folder:t.folder,id:n.id,title:n.title,source:t.source,sourceLine:n.anchorLine,sourceTitle:n.anchorTitle,section:n.section,page:[t.folder,'html/deep',n.page].join('/'),companion:[t.folder,t.companion].join('/'),references:n.references}));
}
function applyHome(){
 const file=path.join(root,'index.html');if(!fs.existsSync(file))return;
 const before=fs.readFileSync(file,'utf8');let html=stripSeminarAdditions(before);
 const list=settings.topics.map(t=>{const n=locations(t)[0];return `<li><a href="${href(file,path.join(n.directory,n.page))}#${n.id}">${esc(t.name)} · ${t.notes.length}곳</a></li>`;}).join('');
 const directory=block('seminar-home-index',`<section class="seminar-comment-index" aria-labelledby="seminar-overview-title"><p class="seminar-label">기존 교재에 덧붙인 발표 관점</p><h2 id="seminar-overview-title">개념에서 실제 개발의 판단으로</h2><p>7개 주제에서 필요한 17곳에만 추가 해석을 달았습니다. Hermes·PydanticAI는 집중 설명에, 나머지는 차별점 비교에 활용할 수 있습니다. 반도체 가상 사례와 3차 검증 질문을 구분해 읽으세요.</p><ul>${list}</ul></section>`);
 const end=html.indexOf('</aside>');if(end<0)throw Error('홈 안내 영역 없음');const at=end+'</aside>'.length;
 html=withStyle(file,html.slice(0,at)+directory+html.slice(at));
 if(stripSeminarAdditions(html)!==stripSeminarAdditions(before))throw Error('원본 홈 변경 감지');
 fs.writeFileSync(file,html);
}
export function applySeminarComments(folder){
 const selected=folder?settings.topics.filter(t=>t.folder===folder):settings.topics;
 if(!selected.length)throw Error('알 수 없는 주제 '+folder);
 for(const t of selected)applyTopic(t);
 applyHome();
 const report=settings.topics.flatMap(t=>locations(t).map(n=>({topic:t.name,folder:t.folder,id:n.id,title:n.title,source:t.source,sourceLine:n.anchorLine,sourceTitle:n.anchorTitle,section:n.section,page:[t.folder,'html/deep',n.page].join('/'),companion:[t.folder,t.companion].join('/'),references:n.references})));
 fs.writeFileSync(path.join(root,'html/seminar-comment-map.json'),JSON.stringify({flow:settings.flow,blueprint:settings.blueprint,basis:settings.basis,commentCount:report.length,comments:report},null,2)+'\n');
 console.log(`Applied seminar comments: ${selected.length} topics; existing source and HTML content preserved.`);
}
if(process.argv[1]&&path.resolve(process.argv[1])===thisFile)applySeminarComments();
