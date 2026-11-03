/* === MODEL: blueprint audience slides only; reserved content is presenter-only === */
const data=__SLIDES__;
const privateMaterial=__PRIVATE__;
const slides=[...document.querySelectorAll('.slide')];
const stage=document.querySelector('.deck-stage');
const dialog=document.querySelector('.menu-dialog');
const reader=document.querySelector('.sources-dialog');
let index=0,step=0,notesWindow=null,notesTab='current';

/* === FIXED STAGE AND REPLACEABLE BUILDS === */
function scale(){const z=Math.min(innerWidth/1920,innerHeight/1080);stage.style.transform=`translate(${(innerWidth-1920*z)/2}px,${(innerHeight-1080*z)/2}px) scale(${z})`}
// Quiet focus frames for text-only comparisons and feature groups. They do not
// change layout, text or sequence, and are hidden in the complete/printed view.
function prepareFocusFrames(){
 const ns='http://www.w3.org/2000/svg';
 document.querySelectorAll('svg g[data-focus]').forEach(g=>{
  if(g.querySelector('.node,[data-focus],.focus-frame,[marker-end]'))return;
  const b=g.getBBox();if(b.width<150||b.height<38)return;
  const r=document.createElementNS(ns,'rect');r.setAttribute('class','focus-frame');
  const x=Math.max(-18,b.x-18),y=Math.max(-16,b.y-16);
  r.setAttribute('x',x);r.setAttribute('y',y);r.setAttribute('width',Math.min(1670-x,b.width+36));r.setAttribute('height',Math.min(666-y,b.height+32));r.setAttribute('rx','8');r.setAttribute('aria-hidden','true');g.prepend(r);
 });
}
function state(){return {index,step,id:data[index].id,maxStep:data[index].steps.length-1,total:data.length}}
function go(i,s=0){index=Math.max(0,Math.min(data.length-1,i));step=Math.max(0,Math.min(data[index].steps.length-1,s));render()}
function next(){if(step<data[index].steps.length-1)step++;else if(index<data.length-1){index++;step=0}render()}
function prev(){if(step>0)step--;else if(index>0){index--;step=data[index].steps.length-1}render()}
function goId(id){id=id==='S06'?'S05':id;const i=data.findIndex(s=>s.id===id);if(i>=0)go(i)}
function render(){
 slides.forEach((s,i)=>{
  const active=i===index;s.classList.toggle('active',active);s.setAttribute('aria-hidden',String(!active));s.inert=!active;
  if(!active)return;
  s.classList.toggle('focus-on',step>0&&!data[index].reveal);
  s.querySelectorAll('[data-focus]').forEach(g=>{g.classList.toggle('dim',step>0&&Number(g.dataset.focus)!==step);g.classList.toggle('highlight',step>0&&Number(g.dataset.focus)===step)});
  s.querySelectorAll('[data-reveal]').forEach(g=>{const show=step>=Number(g.dataset.reveal);g.classList.toggle('revealed',show);g.setAttribute('aria-hidden',String(!show))});
  s.querySelector('.step-label').textContent=`${data[index].steps[step]} · ${step}/${data[index].steps.length-1}`;
  s.querySelector('.jump-number').value=index+1;
 });
 document.title=`${index+1}/${data.length} · ${data[index].title}`;
 document.querySelector('#live').textContent=`${index+1}번. ${data[index].title}. ${data[index].steps[step]}`;
 history.replaceState(null,'',`#${data[index].id}`);
 if(notesWindow&&!notesWindow.closed)writeNotes();
}

/* === PRIVATE NOTES: separate window, current notes + appendix, never an audience overlay === */
function esc(x){return String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function markdown(s){
 let code=false,table=false,out=[];
 function inline(v){return esc(v).replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>')}
 for(const line of s.split('\n')){
  if(line.startsWith('```')){if(table){out.push('</tbody></table>');table=false}out.push(code?'</code></pre>':'<pre><code>');code=!code;continue}
  if(code){out.push(esc(line)+'\n');continue}
  if(line.startsWith('|')){if(!table){out.push('<table><tbody>');table=true}if(!/^\|[\s|:-]+\|$/.test(line))out.push('<tr>'+line.split('|').slice(1,-1).map(c=>`<td>${inline(c.trim())}</td>`).join('')+'</tr>');continue}
  if(table){out.push('</tbody></table>');table=false}
  const heading=line.match(/^(#{1,4}) (.*)$/);if(heading){const n=Math.min(4,heading[1].length+1);out.push(`<h${n}>${inline(heading[2])}</h${n}>`)}
  else if(line.trim())out.push(`<p>${inline(line.replace(/^[-] /,'• '))}</p>`);
 }
 if(table)out.push('</tbody></table>');if(code)out.push('</code></pre>');return out.join('');
}
function writeNotes(){
 const d=data[index],w=notesWindow;
 const scroll=w.document?.documentElement?.scrollTop||0;
 const contents=notesTab==='current'?d.note:notesTab==='reserved'?Object.entries(privateMaterial.reserved).map(([k,v])=>`## ${k} — ${v}`).join('\n\n'):privateMaterial[notesTab];
 const tabs=[['current','현재 슬라이드'],['concepts','상세 해설'],['qa','Q&A'],['research','근거·정정'],['demos','데모 제작 명세'],['reserved','예약 SDK']];
 w.document.open();w.document.write(`<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>발표자 노트 · ${esc(d.id)}</title><style>body{background:#27364A;color:#E2EAF5;font:17px/1.8 sans-serif;margin:0}header{position:sticky;top:0;background:#30435D;padding:18px 28px;border-bottom:1px solid #536B89}header .row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}h1{font-size:25px;line-height:1.5;margin:12px 0}h2,h3{margin-top:32px}a{color:#ACD0FF}small{color:#BED0E6}main{max-width:1040px;margin:25px auto;padding:0 28px 60px}button{font:inherit;cursor:pointer;color:#E2EAF5;background:#344C6B;border:1px solid #536B89;border-radius:5px;padding:6px 12px}button.active{border-color:#BCC7F3}pre{background:#1F2B3A;border:1px solid #536B89;padding:18px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:15px;line-height:1.6}code{color:#E9C38F}table{width:100%;border-collapse:collapse}td{border:1px solid #536B89;padding:9px;vertical-align:top}p{overflow-wrap:anywhere}button:focus-visible,a:focus-visible{outline:3px solid #ACD0FF}</style><header><div class="row"><small>발표자 전용 · ${index+1}/${data.length} · ${d.id} · ${step}/${d.steps.length-1}</small><button id="back">← 단계</button><button id="next">단계 →</button><button id="nextSlide">다음 장</button></div><h1>${esc(d.title)}</h1><div class="row">${tabs.map(([k,v])=>`<button data-tab="${k}" class="${notesTab===k?'active':''}">${v}</button>`).join('')}</div></header><main>${markdown(contents||'')}<h2>이 장의 출처</h2>${d.sources.length?d.sources.map(([id,name,url])=>`<p><a href="${esc(url)}" target="_blank" rel="noopener noreferrer">[${id}] ${esc(name)}</a></p>`).join(''):'<p>최종 blueprint의 도입·발표 구성 및 설계 예시.</p>'}<p><small>←/→/Space 단계 · PageUp/Down 장 이동 · G 번호 입력 · T 목차 · N 노트 · F 전체 화면<br>실제 Demo 서비스는 별도 제작·연결 대상입니다. 본 자료는 모델 API를 호출하지 않습니다.</small></p></main></html>`);w.document.close();
 w.document.querySelector('#back').onclick=prev;w.document.querySelector('#next').onclick=next;w.document.querySelector('#nextSlide').onclick=()=>go(index+1);
 w.document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{notesTab=b.dataset.tab;writeNotes()});
 w.document.documentElement.scrollTop=scroll;
}
function notes(){notesWindow=window.open('','seminar2-final-notes','width=1080,height=850');if(notesWindow)writeNotes()}
function sources(){
 const d=data[index];reader.querySelector('.reader-meta').textContent=`${index+1} / ${data.length} · ${d.id} · 개념과 설명`;
 reader.querySelector('h2').textContent=d.title;
 reader.querySelector('main').innerHTML=`<h3>이 장의 개념</h3><dl>${d.concepts.map(c=>`<dt>${esc(c.term)}</dt><dd>${esc(c.meaning)}</dd>`).join('')}</dl><h3>설명</h3>${d.explanation.split(/\n\n+/).map(p=>`<p>${esc(p)}</p>`).join('')}<h3>발표 포인트</h3><p>${esc(d.take)}</p><h3>참고 자료</h3>${d.sources.length?'<ul>'+d.sources.map(([id,name,url])=>`<li><a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(name)}</a></li>`).join('')+'</ul>':'<p>사용자가 정한 세미나 계획과 발표 구성입니다.</p>'}${d.localEvidence?'<h3>프로젝트 학습자료</h3><ul>'+d.localEvidence.map(e=>`<li><a href="${esc('../../'+e.path)}" target="_blank" rel="noopener noreferrer">${esc(e.path.split('/').pop())}</a> · ${esc(e.sections)}</li>`).join('')+'</ul>':''}`;
 reader.showModal();reader.scrollTop=0;reader.querySelector('.reader-close').focus();
}
function closeSources(){reader.close();slides[index].querySelector('.sources').focus()}
function toc(){dialog.showModal();const button=dialog.querySelector(`[data-jump="${index}"]`);button?.focus();button?.scrollIntoView({block:'center'})}
function closeToc(){dialog.close();slides[index].querySelector('.menu').focus()}

/* === KEYBOARD, MOUSE AND TOUCH === */
document.addEventListener('click',e=>{
 if(e.target.closest('.next'))next();
 if(e.target.closest('.prev'))prev();
 if(e.target.closest('.sources'))sources();
 if(e.target.closest('.reader-close'))closeSources();
 if(e.target===reader) {const r=reader.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeSources()}
 if(e.target.closest('.menu'))toc();
 if(e.target.closest('.close'))closeToc();
 const jump=e.target.closest('[data-jump]');if(jump){go(Number(jump.dataset.jump));closeToc()}
});
document.addEventListener('change',e=>{if(e.target.matches('.jump-number')&&e.target.value)go(Number(e.target.value)-1)});
document.addEventListener('keydown',e=>{
 if(e.ctrlKey||e.metaKey||e.altKey)return;
 if(reader.open){if(e.key==='Escape'){e.preventDefault();closeSources()}return}
 if(dialog.open){if(e.key==='Escape'){e.preventDefault();closeToc()}return}
 if(e.target.matches('input')){if(e.key==='Enter'){e.preventDefault();if(e.target.value)go(Number(e.target.value)-1);e.target.blur()}return}
 let handled=true;
 if(['ArrowRight',' '].includes(e.key))next();else if(e.key==='ArrowLeft')prev();
 else if(e.key==='PageDown')go(index+1);else if(e.key==='PageUp')go(index-1);
 else if(e.key==='Home')go(0);else if(e.key==='End')go(data.length-1);
 else if(e.key.toLowerCase()==='n')notes();else if(e.key.toLowerCase()==='t')toc();
 else if(e.key.toLowerCase()==='g'){const n=slides[index].querySelector('.jump-number');n.focus();n.select()}
 else if(e.key.toLowerCase()==='f'){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen().catch(()=>{})}
 else if(e.key==='Escape'){if(notesWindow&&!notesWindow.closed)notesWindow.close()}
 else handled=false;if(handled)e.preventDefault();
});
let startX=null;addEventListener('touchstart',e=>{if(dialog.open||reader.open)return;startX=e.touches[0].clientX},{passive:true});
addEventListener('touchend',e=>{if(startX===null)return;const dx=e.changedTouches[0].clientX-startX;if(Math.abs(dx)>50){if(dx<0)next();else prev()}startX=null},{passive:true});
let lastWheel=0;addEventListener('wheel',e=>{if(dialog.open||reader.open||Math.abs(e.deltaY)<30||Date.now()-lastWheel<550)return;lastWheel=Date.now();if(e.deltaY>0)next();else prev()},{passive:true});
addEventListener('resize',scale);addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(id!==data[index].id)goId(id)});
const initialId=location.hash==='#S06'?'S05':location.hash.slice(1);const initial=data.findIndex(s=>s.id===initialId);if(initial>=0)index=initial;
scale();render();window.deck={go,goId,next,prev,state,notes,toc,sources};
document.fonts.ready.then(prepareFocusFrames);
