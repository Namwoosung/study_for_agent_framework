import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {stripSeminarAdditions} from './apply-seminar-comments.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const config=JSON.parse(fs.readFileSync(path.join(root,'html/seminar-comments.json'),'utf8'));
const map=JSON.parse(fs.readFileSync(path.join(root,'html/seminar-comment-map.json'),'utf8'));
const baseline=JSON.parse(fs.readFileSync(path.join(root,'html/seminar-baseline.json'),'utf8'));
const hash=s=>createHash('sha256').update(s).digest('hex');
const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const errors=[];let markdown=0,html=0;
for(const f of baseline.files){
 const file=path.join(root,f.path);
 if(!fs.existsSync(file)){errors.push('기존 파일 누락 '+f.path);continue;}
 const current=fs.readFileSync(file);
 if(f.path.endsWith('.md')){markdown++;if(hash(current)!==f.hash)errors.push('원본 Markdown 변경 '+f.path);}
 else{html++;if(hash(stripSeminarAdditions(current.toString('utf8')))!==f.hash)errors.push('추가 코멘트 외 기존 HTML 변경 '+f.path);}
}
let count=0;
const home=fs.readFileSync(path.join(root,'index.html'),'utf8');
for(const t of config.topics){
 const guide=fs.readFileSync(path.join(root,t.folder,'html/deep/index.html'),'utf8');
 const md=fs.readFileSync(path.join(root,t.folder,t.companion),'utf8');
 for(const n of t.notes){
  const record=map.comments.find(c=>c.folder===t.folder&&c.id.endsWith('-'+n.id));
  if(!record){errors.push('코멘트 매핑 없음 '+t.folder+' '+n.id);continue;}
  const file=path.join(root,record.page),page=fs.readFileSync(file,'utf8');
  const marker=`id="${record.id}"`;
  if(page.split(marker).length!==2)errors.push('코멘트 ID 중복/누락 '+record.id);
  if(!guide.includes(`href="${path.basename(file)}#${record.id}"`))errors.push('심층 안내에서 코멘트 연결 누락 '+record.id);
  if(!home.includes('#'+record.id)){
   // 홈에서는 주제별 첫 코멘트로 연결하고, 주제 안내에서 전체 목록을 제공한다.
   if(n===t.notes[0])errors.push('홈에서 주제 코멘트 연결 누락 '+record.id);
  }
  for(const p of [n.title,n.takeaway,...n.paragraphs,n.followup]){
   if(!page.includes(esc(p)))errors.push('추가 문구 누락 '+record.id);
   if(!md.includes(p))errors.push('코멘트 Markdown 누락 '+record.id);
  }
  if(!page.includes(`id="line-${n.anchorLine}"`))errors.push('근거 절 누락 '+record.id);
  count++;
 }
}
if(config.topics.length!==7||count!==17||count!==map.commentCount)errors.push('선택 코멘트 수 불일치');
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else{
 const result={passed:true,topics:7,comments:count,existingMarkdownUnchanged:markdown,existingHtmlPreserved:html,method:'추가 블록을 제거하면 기존 모든 HTML의 SHA-256과 일치; 기존 Markdown은 원본 바이트 해시 일치'};
 fs.writeFileSync(path.join(root,'html/seminar-validation.json'),JSON.stringify(result,null,2)+'\n');
 console.log('PASS: '+JSON.stringify(result));
}
