"""Verify blueprint coverage, sources, fenced Python syntax, and the exported PDF."""
from pathlib import Path
import ast
import hashlib
import json
import re

root=Path(__file__).resolve().parent
project=root.parent.parent
blueprint=project/'2_2차_세미나_최종_slide_blueprint.md'
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
notes=json.loads((root/'notes.json').read_text(encoding='utf-8'))
expected=[f'S{i:02}' for i in range(46) if i not in range(39,43)]
expected.insert(expected.index('S04'),'S03H')
assert [s['id'] for s in notes]==expected
assert manifest['blueprintSha256']==hashlib.sha256(blueprint.read_bytes()).hexdigest()
source=blueprint.read_text(encoding='utf-8')
specs=dict(re.findall(r'^## (S\d{2}) — (.*?)(?=^## S\d{2} — |^# C\.)',source,re.M|re.S))
for slide in notes:
    if slide['id']!='S03H':
        assert specs[slide['id']].strip() in slide['originalSpec']
        expected_refs=set(re.findall(r'\[([HCPV]\d{2})\]',specs[slide['id']]))
        assert expected_refs.issubset({s[0] for s in slide['sources']})
    assert len(slide['concepts'])>0 and len(slide['explanation'])>50
    assert not re.search(r'\bsk-[A-Za-z0-9_-]{16,}',slide['note'])
    assert len(slide['steps'])>0
blocks=re.findall(r'```python\n(.*?)```',source,re.S)
for block in blocks:ast.parse(block)
from pypdf import PdfReader
pdf=PdfReader(root/'agent-framework-seminar-2.pdf')
assert len(pdf.pages)==len(expected)
assert all(len(page.extract_text())>20 for page in pdf.pages)
result={'blueprintCoverage':42,'audienceSlides':len(expected),'speakerSpecCoverage':42,'sourcesExplanations':len(notes),'reservedExcluded':manifest['reserved'],
        'sourceReferencesPreserved':True,'pythonSnippetsSyntaxChecked':len(blocks),
        'pdfPages':len(pdf.pages),'blankPdfPages':0,'result':'pass'}
(root/'validation/content-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
