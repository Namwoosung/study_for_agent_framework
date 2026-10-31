import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const report=JSON.parse(fs.readFileSync(path.join(root,'html/home-map.json'),'utf8'));
const home=fs.readFileSync(path.join(root,'index.html'),'utf8'),errors=[];let pageCount=0,links=0;
function checkLinks(file,html){const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);if(ids.length!==new Set(ids).size)errors.push('Duplicate IDs '+file);for(const [,uri]of html.matchAll(/\b(?:href|src)="([^"]+)"/g)){if(/^(https?:|mailto:|data:)/.test(uri))continue;const [name,fragment]=uri.split('#'),target=path.resolve(path.dirname(file),decodeURIComponent(name||path.basename(file)));if(!fs.existsSync(target)){errors.push('Missing '+uri+' from '+file);continue;}if(fragment&&target.endsWith('.html')&&!fs.readFileSync(target,'utf8').includes(`id="${decodeURIComponent(fragment)}"`))errors.push('Missing fragment '+uri);links++;}}
checkLinks(path.join(root,'index.html'),home);
for(const topic of report.topics)for(const course of topic.courses){
 const directory=path.join(root,topic.folder,course.directory);
 const actual=fs.readdirSync(directory).filter(n=>n.endsWith('.html'));
 if(actual.length!==course.pages.length||actual.some(n=>!course.pages.some(p=>path.basename(p.path)===n)))errors.push('Unlisted HTML in '+directory);
 for(const page of course.pages){
  const file=path.join(root,page.path),html=fs.readFileSync(file,'utf8');pageCount++;
  if(!home.includes(`href="${page.href}"`))errors.push('Home omits '+page.path);
  const nav=html.match(/<!-- deep-course-link -->([\s\S]*?)<!-- \/deep-course-link -->/g)||[];
  if(nav.length!==1)errors.push('Expected one global home navigation '+page.path);
  const homeLink=nav.join('').match(/href="([^"]+)"[^>]*>전체 학습 홈<\/a>/);
  if(!homeLink||path.resolve(path.dirname(file),homeLink[1])!==path.join(root,'index.html'))errors.push('Global home link missing or wrong '+page.path);
  checkLinks(file,html);
 }
}
if(pageCount!==report.totalPages)errors.push('Page count differs');
if((home.match(/<h1\b/g)||[]).length!==1)errors.push('Home should have one h1');
if(/<script|localStorage|sessionStorage|src="https?:/.test(home))errors.push('Unexpected script or remote dependency');
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log(`PASS: root home links all ${pageCount} study pages; every page returns to root home; ${links} local references valid.`);
