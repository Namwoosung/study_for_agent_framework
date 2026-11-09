import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {aids, renderAid} from './practice-aids.mjs';

const script = fileURLToPath(import.meta.url);
const study = path.resolve(path.dirname(script), '..');

export const practice = [
  {folder: 'LangChain', name: 'LangChain', summary: '도구 호출, 구조화 출력, 대화 상태와 권한'},
  {folder: 'LangGraph', name: 'LangGraph', summary: '상태 그래프, 승인 후 재개와 병렬 조회'},
  {folder: 'Deep_Agents', name: 'Deep Agents', summary: '작업 공간, 조사 위임과 게시 승인'},
  {folder: 'Oracle_Agent_Spec', name: 'Oracle Open Agent Specification', summary: 'JSON/YAML 선언, WayFlow 실행과 LangGraph 어댑터'},
].map(course => ({
  ...course,
  source: `${course.folder}.md`,
  href: `${course.folder}/html/index.html`,
}));

const escape = value => value.replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[char]));

async function buildPractice() {
  const runtime = path.join(process.env.USERPROFILE || '', '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
  const {marked, Renderer} = await import('marked').catch(error => {
    if (error.code !== 'ERR_MODULE_NOT_FOUND') throw error;
    return import(pathToFileURL(path.join(runtime, 'marked/lib/marked.esm.js')).href);
  });
  const localLinks = new Map(practice.map(course => [
    `../${course.folder}/${course.source}`, `../../${course.href}`,
  ]));

  for (const [index, course] of practice.entries()) {
    const directory = path.join(study, course.folder);
    const source = fs.readFileSync(path.join(directory, course.source), 'utf8');
    const tokens = marked.lexer(source, {gfm: true});
    const title = tokens.shift();
    if (title?.type !== 'heading' || title.depth !== 1) {
      throw new Error(`Expected an opening heading in ${course.source}`);
    }

    const chapters = [];
    const chapterIds = new Map();
    for (const heading of tokens.filter(token => token.type === 'heading')) {
      if (heading.depth === 2) {
        const number = heading.text.match(/^\d+(?=\. )/)?.[0];
        if (number === undefined) throw new Error(`Unnumbered chapter in ${course.source}`);
        const id = `chapter-${number}`;
        chapters.push({heading, id, number, subsections: []});
        chapterIds.set(heading, id);
      } else if (heading.depth === 3 && chapters.length) {
        const parent = chapters.at(-1);
        const id = `${parent.id}-${parent.subsections.length + 1}`;
        parent.subsections.push({heading, id});
        chapterIds.set(heading, id);
      }
    }
    const courseAids = aids[course.folder];
    for (const chapter of Object.keys(courseAids)) {
      if (!chapters.some(({id}) => id === chapter)) {
        throw new Error(`Missing learning aid chapter ${chapter} in ${course.source}`);
      }
    }
    const renderer = new Renderer();
    renderer.heading = function (token) {
      const id = chapterIds.get(token);
      const text = this.parser.parseInline(token.tokens);
      const anchor = id ? ` <a class="permalink" href="#${id}" aria-label="${escape(token.text)} 링크">#</a>` : '';
      const aid = courseAids[id];
      return `<h${token.depth}${id ? ` id="${id}"` : ''}>${text}${anchor}</h${token.depth}>\n`
        + (aid ? renderAid(`aid-${id}`, aid, escape) : '');
    };
    renderer.link = function (token) {
      return Renderer.prototype.link.call(this, {...token, href: localLinks.get(token.href) ?? token.href});
    };
    renderer.table = function (token) {
      return `<div class="table-scroll" tabindex="0" role="region" aria-label="비교 표">${Renderer.prototype.table.call(this, token)}</div>\n`;
    };
    renderer.code = function (token) {
      const language = token.lang === 'python' ? 'Python' : token.lang === 'powershell' ? 'PowerShell' : '흐름도';
      const filename = token.lang === 'python' ? token.text.match(/^# ([\w-]+\.py)\n/)?.[1] : null;
      const label = filename ? `${language} / ${filename}` : language;
      const pre = Renderer.prototype.code.call(this, token).replace('<pre>', `<pre tabindex="0" aria-label="${escape(label)}">`);
      const button = token.lang === 'text' ? '' : '<button type="button" data-copy hidden>코드 복사</button>';
      return `<figure class="example"><figcaption><span>${escape(label)}</span>${button}</figcaption>${pre}</figure>\n`;
    };

    const nav = practice.map((item, i) => (
      `<a href="../../${item.href}"${i === index ? ' aria-current="page"' : ''}>${escape(item.name)}</a>`
    )).join('');
    const toc = chapters.map(({heading, id, number}) => (
      `<li value="${number}"><a href="#${id}">${escape(heading.text.replace(/^\d+\.\s*/, ''))}</a></li>`
    )).join('');
    const next = practice[index + 1];
    const article = marked.parser(tokens, {renderer, gfm: true});
    const html = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${escape(course.summary)}">
  <title>${escape(title.text)}</title>
  <link rel="stylesheet" href="../../html/practice.css">
  <script src="../../html/practice.js" defer></script>
</head>
<body id="top">
  <a class="skip" href="#main">본문으로 건너뛰기</a>
  <header class="site-header">
    <!-- deep-course-link -->
    <a href="../../index.html">전체 학습 홈</a>
    <!-- /deep-course-link -->
    <span>Python 에이전트 실습</span>
  </header>
  <nav class="series" aria-label="실습 교재">${nav}</nav>
  <div class="layout">
    <aside class="sidebar">
      <nav aria-label="이 교재의 단원">
        <p>이 교재의 단원</p>
        <ol start="${chapters[0].number}">${toc}</ol>
      </nav>
    </aside>
    <main id="main" tabindex="-1">
      <article>
        <h1>${escape(title.text)}</h1>
        ${article}
      </article>
      <footer>
        <a href="../${course.source}">Markdown 원문</a>
        <a href="#top">맨 위로</a>${next ? `\n        <a href="../../${next.href}">다음 교재 · ${escape(next.name)}</a>` : ''}
      </footer>
    </main>
  </div>
  <p class="visually-hidden" role="status" id="copy-status"></p>
</body>
</html>
`;
    const output = path.join(directory, 'html');
    fs.mkdirSync(output, {recursive: true});
    fs.writeFileSync(path.join(output, 'index.html'), html);
  }
  console.log(`Built ${practice.length} Python practice guides.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === script) {
  await buildPractice();
}
