import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
if(fs.existsSync(path.join(root,'deep/index.html'))){
 for(const name of fs.readdirSync(root).filter(n=>n.endsWith('.html'))){
  const file=path.join(root,name);let html=fs.readFileSync(file,'utf8');
  html=html.replace(/<!-- deep-course-link -->[\s\S]*?<!-- \/deep-course-link -->/g,'');
  html=html.replace(/<link rel="stylesheet" href="course-links.css">/g,'');
  html=html.replace('</head>','<link rel="stylesheet" href="course-links.css"></head>');
  html=html.replace(/(<main\b[^>]*>)/,'$1<!-- deep-course-link --><nav class="course-switch" aria-label="학습 과정"><span>학습 과정</span><a href="index.html" aria-current="true">1차 기본 교재</a><a href="deep/index.html">2차 심층 교재 →</a></nav><!-- /deep-course-link -->');
  fs.writeFileSync(file,html);
 }
}
