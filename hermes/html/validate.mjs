import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const report=JSON.parse(fs.readFileSync(path.join(root,'content-map.json'),'utf8'));
const pages=new Map(report.pages.map(name=>[name,fs.readFileSync(path.join(root,name),'utf8')]));
let links=0,images=0;const errors=[];
const usedChapters=[];
for(const [name,html] of pages){
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 if(ids.length!==new Set(ids).size)errors.push(`${name}: duplicate section id`);
 if((html.match(/<h1[ >]/g)||[]).length!==1)errors.push(`${name}: expected exactly one h1`);
 for(const m of html.matchAll(/data-source-chapter="([^"]+)"/g))usedChapters.push(m[1]);
 if(/localStorage|sessionStorage|fetch\(|https?:[^" ]+\.js/.test(html))errors.push(`${name}: unexpected storage or external script`);
 for(const [,attribute,uri] of html.matchAll(/\b(href|src)="([^"]+)"/g)){
  if(/^(?:https?:|mailto:)/.test(uri))continue;
  const [file,fragment]=uri.split('#');
  const resolved=path.resolve(root,file||name);
  if(!fs.existsSync(resolved)){errors.push(`${name}: missing ${uri}`);continue;}
  if(attribute==='src'&&/\.(?:svg|png|jpg|webp)$/.test(file))images++;else if(attribute==='href')links++;
  if(fragment&&resolved.endsWith('.html')){
   const target=fs.readFileSync(resolved,'utf8');
   if(!target.includes(`id="${decodeURIComponent(fragment)}"`))errors.push(`${name}: missing anchor ${uri}`);
  }
 }
}
const expected=[...Array(23).keys()].map(String).concat(['glossary','sources']);
if(usedChapters.length!==25||expected.some(id=>usedChapters.filter(x=>x===id).length!==1))errors.push('Each original chapter/appendix must appear exactly once');
if(images!==7)errors.push(`Expected 7 rendered source diagrams; found ${images}`);
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}
else console.log(`PASS: ${pages.size} pages, 25 original sections exactly once, ${images} diagrams, ${links} local links, unique heading IDs.`);
