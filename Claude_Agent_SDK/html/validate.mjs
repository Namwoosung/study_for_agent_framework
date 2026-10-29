import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const report=JSON.parse(fs.readFileSync(path.join(root,'content-map.json'),'utf8'));
const pages=new Map(report.pages.map(name=>[name,fs.readFileSync(path.join(root,name),'utf8')]));
const errors=[],used=[];let links=0,diagrams=0;
const source=fs.readFileSync(path.resolve(root,report.source),'utf8');
if(createHash('sha256').update(source).digest('hex')!==report.sourceSha256)errors.push('Source changed after build');
for(const [name,html] of pages){
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 if(ids.length!==new Set(ids).size)errors.push(name+': duplicate section IDs');
 if((html.match(/<h1[ >]/g)||[]).length!==1)errors.push(name+': expected exactly one h1');
 used.push(...[...html.matchAll(/data-source-chapter="([^"]+)"/g)].map(m=>m[1]));
 diagrams+=(html.match(/data-source-diagram="/g)||[]).length;
 if(/localStorage|sessionStorage|fetch\(|src="https?:/.test(html))errors.push(name+': unexpected browser storage or remote script');
 for(const [,attribute,uri] of html.matchAll(/\b(href|src)="([^"]+)"/g)){
  if(/^(?:https?:|mailto:)/.test(uri))continue;
  const [file,fragment]=uri.split('#'),target=path.resolve(root,decodeURIComponent(file||name));
  if(!fs.existsSync(target)){errors.push(name+': missing file '+uri);continue;}
  if(attribute==='href')links++;
  if(fragment&&target.endsWith('.html')&&!fs.readFileSync(target,'utf8').includes(`id="${decodeURIComponent(fragment)}"`))errors.push(name+': missing section '+uri);
 }
}
if(used.length!==report.sourceSections.length||report.sourceSections.some(id=>used.filter(x=>x===id).length!==1))errors.push('Original sections missing or duplicated');
if(diagrams!==report.sourceDiagrams)errors.push('Original diagrams missing');
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const combined=[...pages.values()].join('\n');
let codeCount=0;for(const match of source.replaceAll('\r\n','\n').matchAll(/^```[^\n]*\n([\s\S]*?)\n```/gm)){codeCount++;if(!combined.includes(esc(match[1])))errors.push('Original code block missing: '+codeCount);}
if(codeCount!==report.sourceCodes)errors.push('Code block count changed');
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log(`PASS: ${report.name}; ${pages.size} pages, ${used.length} source sections, ${codeCount} code blocks, ${diagrams} diagrams, ${links} local links; source hash unchanged.`);
