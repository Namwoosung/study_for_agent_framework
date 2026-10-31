import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url)),report=JSON.parse(fs.readFileSync(path.join(root,'content-map.json'),'utf8'));
const hash=s=>createHash('sha256').update(s).digest('hex'),errors=[];
const original=fs.readFileSync(path.resolve(root,report.source),'utf8'),source=original.replaceAll('\r\n','\n'),lines=source.split('\n');
if(hash(original)!==report.sourceHash||hash(source)!==report.normalizedHash)errors.push('Source hash changed');
const pages=new Map(report.pages.map(n=>[n,fs.readFileSync(path.join(root,n),'utf8')]));
const runtime=path.join(process.env.USERPROFILE||'','.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js');
const {marked}=await import(pathToFileURL(runtime).href);
const decode=s=>s.replace(/&#(x[0-9a-f]+|\d+);/gi,(_,n)=>String.fromCodePoint(n[0].toLowerCase()==='x'?parseInt(n.slice(1),16):+n)).replace(/&(amp|lt|gt|quot|apos|#39|nbsp);/g,(_,n)=>({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",'#39':"'",nbsp:' '}[n]));
const normalize=s=>decode(s.replace(/<!--[\s\S]*?-->/g,'').replace(/<[^>]*>/g,' ')).replace(/\*\*/g,'').replace(/[A-Z]+\d+/g,'').replace(/[\[\]]/g,'').replace(/\s+/g,'').trim();
const combined=[...pages.values()].join('\n'),defs='\n\n'+Object.entries(report.references).map(([id,url])=>`[${id}]: ${url}`).join('\n');
let nextLine=1,links=0,textBlocks=0,tableRows=0;
for(const section of report.sections){
 if(section.startLine!==nextLine)errors.push('Source gap/overlap at '+section.key);
 const raw=lines.slice(section.startLine-1,section.endLine).join('\n');nextLine=section.endLine+1;
 if(hash(raw)!==section.rawHash)errors.push('Source range hash mismatch '+section.key);
 const mapping=report.mapping.find(m=>m.sections.includes(section.key));
 const html=pages.get(mapping?.page)||'';
 const start=`<section class="source-section" data-source-section="${section.key}">`,at=html.indexOf(start),end=html.indexOf('</section>',at);
 if(at<0||end<0){errors.push('Section absent '+section.key);continue;}
 const content=html.slice(at+start.length,end);
 if(hash(content)!==section.htmlHash)errors.push('Generated content changed '+section.key);
 const actual=normalize(content);
 const prose=raw.replace(/^\x60\x60\x60[^\n]*\n[\s\S]*?^\x60\x60\x60/gm,'').replace(/^\[[^\]]+\]:.*$/gm,'').replace(/`[^`]*`/g,'');
 for(const id of new Set(prose.match(/\b[A-Z]+\d+\b/g)||[])){const url=report.references[id];if(url&&!content.includes(esc(url)))errors.push('Citation target missing '+section.key+': '+id);}
 // 원문의 모든 텍스트 블록과 표 셀을 별도로 다시 파싱해 표시 결과와 대조한다.
 function check(tokens){for(const t of tokens){
  if(['paragraph','heading','text'].includes(t.type)&&t.text){const expected=normalize(marked.parse(t.raw||t.text,{gfm:true})+'' );if(expected&&!actual.includes(expected)){
    const withRefs=normalize(marked.parse((t.raw||t.text)+defs));if(!actual.includes(withRefs))errors.push(`Text missing ${section.key}: ${t.text.slice(0,90)}`);
   }textBlocks++;}
  if(t.type==='table'){tableRows+=t.rows.length+1;for(const c of [...t.header,...t.rows.flat()]){const value=normalize(marked.parse(c.text+defs));if(value&&!actual.includes(value))errors.push('Table cell missing '+section.key+': '+c.text.slice(0,60));}}
  if(t.type==='list')for(const item of t.items)check(item.tokens);
  if(t.type==='blockquote')check(t.tokens);
 }}
 check(marked.lexer(raw+defs));
}
if(nextLine!==lines.length+1)errors.push('Source tail missing');
function esc(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
const fences=[...source.matchAll(/^```([^\n]*)\n([\s\S]*?)\n```/gm)];
if(fences.length!==report.codeBlocks.length)errors.push('Fenced block count mismatch');
for(const [i,m]of fences.entries())if(!combined.includes(esc(m[2])))errors.push('Code/diagram source absent '+(i+1));
const mermaids=fences.filter(m=>m[1].trim()==='mermaid');if(mermaids.length!==report.diagrams.length)errors.push('Diagram count mismatch');
for(const d of report.diagrams){
 if(!combined.includes(`data-diagram="${d.number}"`))errors.push('Rendered diagram absent '+d.number);
 if(d.file){const svg=fs.readFileSync(path.join(root,d.file),'utf8');if(!svg.includes('role="img"')||!svg.includes('<desc'))errors.push('Diagram accessibility '+d.number);for(const n of d.nodes)if(!decode(svg.replace(/<[^>]*>/g,'')).replace(/\s/g,'').includes(n.label.replace(/\s/g,'')))errors.push('SVG node text missing '+d.number+': '+n.label);}
}
for(const [name,html]of pages){
 if((html.match(/<h1[ >]/g)||[]).length!==1)errors.push('Expected one h1 '+name);
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);if(ids.length!==new Set(ids).size)errors.push('Duplicate IDs '+name);
 const levels=[...html.matchAll(/<h([1-6])\b/g)].map(m=>+m[1]);for(let i=1;i<levels.length;i++)if(levels[i]>levels[i-1]+1)errors.push('Heading level skipped '+name);
 if(/localStorage|sessionStorage|fetch\(|src="https?:/.test(html))errors.push('Unexpected remote runtime/storage '+name);
 for(const [,attr,uri]of html.matchAll(/\b(href|src)="([^"]+)"/g)){
  if(/^(https?:|mailto:|data:)/.test(uri))continue;
  const [file,frag]=uri.split('#'),target=path.resolve(root,decodeURIComponent(file||name));
  if(!fs.existsSync(target)){errors.push(name+': missing '+uri);continue;}links++;
  if(frag&&target.endsWith('.html')&&!fs.readFileSync(target,'utf8').includes(`id="${decodeURIComponent(frag)}"`))errors.push('Missing anchor '+name+': '+uri);
 }
}
for(const h of report.headings){const count=[...pages.values()].filter(s=>s.includes(`id="${h.id}"`)).length;if(count!==1)errors.push('Source heading count '+h.line+': '+count);}
if(errors.length){console.error([...new Set(errors)].join('\n'));process.exitCode=1;}else{
 const result={name:report.name,pages:pages.size,chapters:report.chapterCount,sourceLines:lines.length,textBlocks,tableRows,fencedBlocks:fences.length,diagrams:mermaids.length,localLinks:links,sourceHash:report.sourceHash,passed:true};
 fs.writeFileSync(path.join(root,'validation.json'),JSON.stringify(result,null,2)+'\n');console.log('PASS '+JSON.stringify(result));
}
