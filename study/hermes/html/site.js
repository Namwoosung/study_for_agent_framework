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
