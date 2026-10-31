import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
for(const deep of [false,true]){
 const directory=deep?path.join(root,'deep'):root;if(!fs.existsSync(directory))continue;
 for(const name of fs.readdirSync(directory).filter(n=>n.endsWith('.html'))){
  const file=path.join(directory,name);let html=fs.readFileSync(file,'utf8');
  html=html.replace(/<!-- deep-course-link -->[\s\S]*?<!-- \/deep-course-link -->/g,'');
  html=html.replace(/<link rel="stylesheet" href="(?:\.\.\/)?course-links.css">/g,'');
  html=html.replace('</head>','<link rel="stylesheet" href="'+(deep?'../':'')+'course-links.css"></head>');
  const home=(deep?'../../../':'../../')+'index.html';
  const course=deep?'':'<span>학습 과정</span><a href="index.html" aria-current="true">1차 기본 교재</a><a href="deep/index.html">2차 심층 교재 →</a>';
  html=html.replace(/(<main\b[^>]*>)/,'$1<!-- deep-course-link --><nav class="course-switch" aria-label="전체 학습 탐색"><a class="global-home-button" href="'+home+'">전체 학습 홈</a>'+course+'</nav><!-- /deep-course-link -->');
  fs.writeFileSync(file,html);
 }
}
const homeBuilder=path.resolve(root,'../../html/build-home.mjs');
if(fs.existsSync(homeBuilder))await import(pathToFileURL(homeBuilder).href);
