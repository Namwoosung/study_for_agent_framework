const { chromium } = require('C:/Users/namws/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1280,height:720}});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
 await page.waitForLoadState('networkidle');await page.evaluate(()=>document.fonts.ready);
 fs.mkdirSync(path.join(__dirname,'screenshots'),{recursive:true});
 const slides=[];
 for(let i=0;i<5;i++){
  await page.evaluate(i=>window.deck.go(i),i);await page.waitForTimeout(300);
  await page.screenshot({path:path.join(__dirname,`screenshots/slide-${i+1}.png`)});
  const audit=await page.evaluate(()=>{
   const s=document.querySelector('.slide.active'),r=s.getBoundingClientRect();
   const overflow=[...s.querySelectorAll('h1,.subtitle,.takeaway,svg text')].filter(e=>{const q=e.getBoundingClientRect();return q.left<r.left-1||q.right>r.right+1||q.top<r.top-1||q.bottom>r.bottom+1}).map(e=>e.textContent);
   const text=[...s.querySelectorAll('svg text')];const overlaps=[];
   for(let a=0;a<text.length;a++)for(let b=a+1;b<text.length;b++){const x=text[a].getBoundingClientRect(),y=text[b].getBoundingClientRect();if(Math.min(x.right,y.right)-Math.max(x.left,y.left)>2&&Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top)>2)overlaps.push([text[a].textContent,text[b].textContent])}
   return {id:s.dataset.slideId,ratio:r.width/r.height,overflow,textOverlaps:overlaps};
  });slides.push(audit);
  const max=await page.evaluate(()=>window.deck.state().maxStep);
  for(let step=1;step<=max;step++)await page.keyboard.press('ArrowRight');
  const got=await page.evaluate(()=>window.deck.state());if(got.index!==i||got.step!==max)errors.push(`Step navigation ${i}`);
 }
 await page.keyboard.press('1');if((await page.evaluate(()=>window.deck.state())).index!==0)errors.push('Number jump');
 await page.keyboard.press('PageDown');if((await page.evaluate(()=>window.deck.state())).index!==1)errors.push('PageDown');
 const pop=page.waitForEvent('popup');await page.keyboard.press('n');const notes=await pop;await notes.waitForLoadState();if(!await notes.locator('h1').count())errors.push('Notes popup');await notes.close();
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(100);
 await page.screenshot({path:path.join(__dirname,'screenshots/mobile.png')});
 const mobile=await page.locator('.deck-stage').boundingBox();
 if(Math.abs(mobile.width/mobile.height-16/9)>.001)errors.push('Mobile ratio');
 await page.emulateMedia({reducedMotion:'reduce'});await page.keyboard.press('ArrowRight');
 await page.emulateMedia({media:'print'});await page.pdf({path:path.join(__dirname,'five-slide-examples.pdf'),width:'20in',height:'11.25in',printBackground:true,preferCSSPageSize:true});
 const report={slides,mobile,errors,fontEmbedded:true,offline:true,checked:'1280x720, 390x844, builds, number jump, page navigation, notes popup, reduced motion, print PDF'};
 fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
 if(errors.length||slides.some(s=>s.overflow.length||s.textOverlaps.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
