// 본문과 링크는 정적 HTML. JavaScript는 좁은 화면의 목차 개폐에만 사용한다.
document.documentElement.classList.add('js-enabled');
const menu=document.querySelector('#menu-button');
const closeMenu=()=>{document.body.classList.remove('nav-open');menu.setAttribute('aria-expanded','false');menu.textContent='목차 열기';};
menu?.addEventListener('click',()=>{
  const open=document.body.classList.toggle('nav-open');
  menu.setAttribute('aria-expanded',String(open));
  menu.textContent=open?'목차 닫기':'목차 열기';
});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&document.body.classList.contains('nav-open')){closeMenu();menu.focus();}});
document.querySelectorAll('#book-nav a').forEach(link=>link.addEventListener('click',closeMenu));
// 넓은 흐름도는 처음에 중앙의 시작 노드가 보이게 한다. 원문 전체는 가로 스크롤로 읽는다.
document.querySelectorAll('.diagram-scroll').forEach(area=>{
  const image=area.querySelector('img');if(!image)return;
  const center=()=>{area.scrollLeft=Math.max(0,(image.clientWidth-area.clientWidth)/2);};
  if(image.complete)center();else image.addEventListener('load',center,{once:true});
});
