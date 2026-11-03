/* Offline browser QA of all audience slides and presenter interactions. */
const {chromium}=require('C:/Users/namws/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const out=path.join(__dirname,'validation');fs.mkdirSync(out,{recursive:true});fs.mkdirSync(path.join(out,'revision-screenshots'),{recursive:true});
 const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'manifest.json'),'utf8'));
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1920,height:1080}}),errors=[],requests=[];
 async function screenshot(target){
  const bytes=await page.screenshot();
  // OneDrive can briefly hold a generated image while syncing it.
  for(let attempt=0;attempt<6;attempt++){
   try{fs.writeFileSync(target,bytes);return}catch(error){if(attempt===5)throw error;await new Promise(resolve=>setTimeout(resolve,350))}
  }
 }
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);await page.waitForLoadState('networkidle');await page.evaluate(()=>document.fonts.ready);
 await page.emulateMedia({reducedMotion:'reduce'});
 const reports=[];
 for(const viewport of [{width:1920,height:1080},{width:1280,height:720},{width:390,height:844}]){
  await page.setViewportSize(viewport);await page.evaluate(()=>dispatchEvent(new Event('resize')));
  for(let i=0;i<manifest.slides.length;i++){
   await page.evaluate(i=>deck.go(i),i);await page.waitForTimeout(20);
   const report=await page.evaluate(()=>{
    const s=document.querySelector('.slide.active'),r=s.getBoundingClientRect();
    const isVisible=e=>getComputedStyle(e).visibility!=='hidden';
    const els=[...s.querySelectorAll('h1,.subtitle,.takeaway,svg text,.slide-footer,.demo-link')].filter(isVisible);
    const overflow=els.filter(e=>{const q=e.getBoundingClientRect();return q.left<r.left-1||q.right>r.right+1||q.top<r.top-1||q.bottom>r.bottom+1}).map(e=>e.textContent);
    const texts=[...s.querySelectorAll('svg text')],overlaps=[];
    for(let a=0;a<texts.length;a++)for(let b=a+1;b<texts.length;b++){
     const x=texts[a].getBoundingClientRect(),y=texts[b].getBoundingClientRect();
     if(Math.min(x.right,y.right)-Math.max(x.left,y.left)>1&&Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top)>1)overlaps.push([texts[a].textContent,texts[b].textContent]);
    }
    const header=s.querySelector('header'),diag=s.querySelector('.diagram');
    const headerIntrusion=isVisible(header)&&header.getBoundingClientRect().bottom>diag.getBoundingClientRect().top+1;
    const stage=document.querySelector('.deck-stage').getBoundingClientRect();
    const viewportOverflow=stage.left<-.5||stage.right>innerWidth+.5||stage.top<-.5||stage.bottom>innerHeight+.5;
    return {id:s.dataset.slideId,ratio:r.width/r.height,overflow,overlaps,headerIntrusion,viewportOverflow};
   });
   reports.push({viewport,...report});
   if(viewport.width===1280)await screenshot(path.join(out,`revision-screenshots/${report.id}.png`));
  }
 }
 await page.setViewportSize({width:1280,height:720});
 for(let i=0;i<manifest.slides.length;i++){
  await page.evaluate(i=>deck.go(i),i);
  const count=manifest.slides[i].builds;
  for(let n=1;n<=count;n++)await page.keyboard.press('ArrowRight');
  let s=await page.evaluate(()=>deck.state());if(s.index!==i||s.step!==count)errors.push(`Build walk ${i}`);
  if(i<manifest.slides.length-1){await page.keyboard.press('ArrowRight');s=await page.evaluate(()=>deck.state());if(s.index!==i+1||s.step!==0)errors.push(`Next after build ${i}`);await page.keyboard.press('ArrowLeft');s=await page.evaluate(()=>deck.state());if(s.index!==i||s.step!==count)errors.push(`Reverse build ${i}`)}
 }
 await page.keyboard.press('Home');await page.keyboard.press('PageDown');if((await page.evaluate(()=>deck.state())).index!==1)errors.push('PageDown');
 await page.keyboard.press('g');await page.locator('.slide.active .jump-number').fill(String(manifest.slides.findIndex(s=>s.id==='S38')+1));await page.keyboard.press('Enter');if((await page.evaluate(()=>deck.state())).id!=='S38')errors.push('Jump display index');
 await page.keyboard.press('PageDown');if((await page.evaluate(()=>deck.state())).id!=='S43')errors.push('Reserved not skipped');
 await page.keyboard.press('t');if(!await page.locator('.menu-dialog').evaluate(d=>d.open))errors.push('TOC open');
 await page.locator(`[data-jump="${manifest.slides.findIndex(s=>s.id==='S15')}"]`).click();if((await page.evaluate(()=>deck.state())).id!=='S15')errors.push('TOC jump');
 if(await page.locator('.menu-dialog').evaluate(d=>d.open))errors.push('TOC close');
 const popup=page.waitForEvent('popup');await page.keyboard.press('n');const notes=await popup;await notes.waitForLoadState();
 if(!(await notes.locator('h1').innerText()).includes('실행 권한'))errors.push('Current notes');
 await notes.locator('[data-tab="qa"]').click();if(!(await notes.locator('main').innerText()).includes('graceful'))errors.push('Private QA');
 await notes.locator('[data-tab="reserved"]').click();if(!(await notes.locator('main').innerText()).includes('S39'))errors.push('Private reserved');
 await notes.locator('[data-tab="current"]').click();await notes.locator('#nextSlide').click();if((await page.evaluate(()=>deck.state())).id!=='S16')errors.push('Presenter navigation');await notes.close();
 // Every Sources reader must explain this slide, without navigating the deck.
 for(let i=0;i<manifest.slides.length;i++){
  await page.evaluate(i=>deck.go(i),i);await page.locator('.slide.active .sources').click();
  const reader=page.locator('.sources-dialog');
  if(!await reader.evaluate(d=>d.open))errors.push(`Sources open ${i}`);
  if(await reader.locator('h2').innerText()!==manifest.slides[i].title)errors.push(`Sources title ${i}`);
  if(!await reader.locator('dt').count()||(await reader.locator('main').innerText()).length<100)errors.push(`Sources content ${i}`);
  await page.keyboard.press('ArrowRight');if((await page.evaluate(()=>deck.state())).index!==i)errors.push(`Reader keyboard ${i}`);
  await page.keyboard.press('Escape');if(await reader.evaluate(d=>d.open))errors.push(`Sources close ${i}`);
 }
 await page.evaluate(()=>deck.goId('S02'));
 if(await page.locator('.slide.active [data-reveal].revealed').count())errors.push('Names initially visible');
 for(let i=1;i<=3;i++){await page.keyboard.press('Space');if(await page.locator('.slide.active [data-reveal].revealed').count()!==i)errors.push(`Name reveal ${i}`)}
 await page.keyboard.press('ArrowLeft');if(await page.locator('.slide.active [data-reveal].revealed').count()!==2)errors.push('Name reverse');
 await page.evaluate(()=>deck.goId('S03'));await page.keyboard.press('Space');
 const focus=await page.locator('.slide.active .highlight').allTextContents();if(focus.length!==2||!focus.some(t=>t.includes('Hermes'))||!focus.some(t=>t.includes('PydanticAI')))errors.push('Harness/SDK simultaneous focus');
 await screenshot(path.join(out,'revision-screenshots/S03-focus.png'));
 await page.evaluate(()=>deck.goId('S02'));await page.keyboard.press('Space');await page.keyboard.press('Space');await page.keyboard.press('Space');await screenshot(path.join(out,'revision-screenshots/S02-names.png'));
 await page.evaluate(()=>deck.goId('S04'));await page.locator('.slide.active .sources').click();await screenshot(path.join(out,'revision-screenshots/S04-sources.png'));await page.keyboard.press('Escape');
 for(const [id,demo] of [['S15','hermes'],['S38','pydanticai']]){
  await page.evaluate(id=>deck.goId(id),id);const popup=page.waitForEvent('popup');await page.locator('.slide.active .demo-link').click();const tab=await popup;await tab.waitForLoadState('networkidle');
  if(!(await tab.locator('.status').innerText()).includes('연결되어 있지'))errors.push(`Demo status ${id}`);
  if(!(await tab.locator('#return').getAttribute('href')).endsWith(id))errors.push(`Demo return ${id}`);await tab.close();
 }
 const ids=await page.locator('[id]').evaluateAll(els=>els.map(e=>e.id));if(new Set(ids).size!==ids.length)errors.push('Duplicate DOM/marker ids');
 if(requests.length)errors.push('Unexpected remote requests: '+requests.join(','));
 await page.evaluate(()=>deck.go(0));await page.emulateMedia({media:'print'});await page.pdf({path:path.join(__dirname,'agent-framework-seminar-2.pdf'),width:'20in',height:'11.25in',printBackground:true,preferCSSPageSize:true});
 const layoutFailures=reports.filter(r=>r.overflow.length||r.overlaps.length||r.headerIntrusion||r.viewportOverflow||Math.abs(r.ratio-16/9)>.001);
 const result={audienceSlides:manifest.slides.length,excluded:manifest.reserved,viewports:3,layoutFailures,interactionErrors:errors,remoteRequests:requests,reports,result:layoutFailures.length||errors.length?'fail':'pass',limits:['No actual Hermes/PydanticAI runtime or proxy is connected.','Diagrams implement the supplied blueprint; no new API functionality claimed.']};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({result:result.result,slides:manifest.slides.length,layoutFailures:layoutFailures.filter(r=>r.viewport.width===1920),failureCount:layoutFailures.length,interactionErrors:errors},null,2));await browser.close();if(result.result!=='pass')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
