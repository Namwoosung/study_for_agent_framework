"""Markdown structure/link/syntax audit; does not run demos or claim browser QA."""
import ast
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
path = root / '2_2차_세미나_최종_slide_blueprint.md'
body = path.read_text(encoding='utf-8')
flow = (root / '0_2차_세미나_발표_흐름.md').read_text(encoding='utf-8')
errors = []
ids = re.findall(r'^## (S\d{2}) — ', body, re.M)
if ids != [f'S{i:02}' for i in range(46)]:
    errors.append('Slide IDs must be ordered S00..S45 exactly once')
sections = re.findall(r'^# ([A-G])\. ', body, re.M)
if sections != list('ABCDEFG'):
    errors.append('Top-level A..G structure mismatch')
refs = set(re.findall(r'\[((?:H|C|P|V)\d{2})\]', body))
declared = set(re.findall(r'^\| ((?:H|C|P|V)\d{2}) \|', body, re.M))
if refs - declared:
    errors.append(f'Undefined source references: {sorted(refs - declared)}')
local_links = []
for target in re.findall(r'\]\(([^)]+)\)', body):
    if '://' in target or target.startswith('#'):
        continue
    local_links.append(target)
    if not (root / target.split('#')[0]).is_file():
        errors.append(f'Missing local link: {target}')
blocks = re.findall(r'^```python\n(.*?)^```', body, re.M | re.S)
for index, code in enumerate(blocks, 1):
    try:
        ast.parse(code)
    except SyntaxError as exc:
        errors.append(f'Python block {index}: {exc}')
if len(re.findall(r'^```', body, re.M)) % 2:
    errors.append('Unbalanced code fences')
for docname, doc in [('blueprint', body), ('flow', flow)]:
    for endpoint in ('http://127.0.0.1:10000/v1', 'http://127.0.0.1:10001/v1'):
        if endpoint not in doc:
            errors.append(f'{docname}: missing {endpoint}')
    if re.search(r'\bsk-[A-Za-z0-9_-]{16,}', doc):
        errors.append(f'{docname}: possible API credential')
for field in ('핵심/화면', '설명/대본', '연결·근거'):
    for slide in range(46):
        if slide in range(39, 43):
            continue
        part = re.split(rf'^## S{slide:02} — ', body, flags=re.M)[1]
        part = re.split(r'^## S\d{2} — |^# C\.', part, maxsplit=1, flags=re.M)[0]
        # Demo slides combine return/connection and evidence in separate fields.
        if field == '연결·근거' and slide in (15, 38):
            if '복귀' not in part or '근거' not in part:
                errors.append(f'S{slide:02}: missing demo return/evidence')
        elif field not in part:
            errors.append(f'S{slide:02}: missing {field}')
report = {
    'artifact': path.name,
    'date': '2026-11-03',
    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'slide_specifications': len(ids),
    'audience_slides': len(ids) - 4,
    'reserved_slides': ['S39', 'S40', 'S41', 'S42'],
    'sections': sections,
    'source_references': len(declared),
    'python_blocks_syntax_checked': len(blocks),
    'local_links_checked': len(local_links),
    'errors': errors,
    'result': 'pass' if not errors else 'fail',
    'limitations': ['No API imports or model requests executed',
                    'No HTML/browser rendering created or checked',
                    'No runtime/proxy/target-PC verification'],
}
(root / 'html/seminar-2-blueprint-validation.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
