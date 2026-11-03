"""Verify blueprint coverage, sources, fenced Python syntax, and the exported PDF."""
from pathlib import Path
import ast
import hashlib
import json
import re
from html.parser import HTMLParser
from hermes_revision import HERMES_ORDER

root=Path(__file__).resolve().parent
project=root.parent.parent
blueprint=project/'2_2차_세미나_최종_slide_blueprint.md'
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
notes=json.loads((root/'notes.json').read_text(encoding='utf-8'))
expected=['S00','S01','S02','S03','S03H']+HERMES_ORDER+[f'S{i:02}' for i in range(16,46) if i not in range(39,43)]
assert [s['id'] for s in notes]==expected
assert manifest['blueprintSha256']==hashlib.sha256(blueprint.read_bytes()).hexdigest()
source=blueprint.read_text(encoding='utf-8')
specs=dict(re.findall(r'^## (S\d{2}) — (.*?)(?=^## S\d{2} — |^# C\.)',source,re.M|re.S))
for slide in notes:
    if slide['id'] in specs:
        assert specs[slide['id']].strip() in slide['originalSpec']
        expected_refs=set(re.findall(r'\[([HCPV]\d{2})\]',specs[slide['id']]))
        assert expected_refs.issubset({s[0] for s in slide['sources']})
    assert len(slide['concepts'])>0 and len(slide['explanation'])>50
    assert not re.search(r'\bsk-[A-Za-z0-9_-]{16,}',slide['note'])
    assert len(slide['steps'])>0
all_original_notes='\n\n'.join(s.get('originalSpec','') for s in notes)
assert all(specs[f'S{i:02}'].strip() in all_original_notes for i in range(46) if i not in range(39,43))
assert manifest['hermesOrder']==HERMES_ORDER and [s['id'] for s in notes[5:21]]==HERMES_ORDER
assert all(s.get('localEvidence') for s in notes[5:21])
for s in notes[5:21]:
    for evidence in s['localEvidence']:assert (project/evidence['path']).is_file()

class DiagramTexts(HTMLParser):
    def __init__(self):super().__init__();self.current=None;self.collect=False;self.buf=[];self.texts={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='section' and 'data-slide-id' in attrs:self.current=attrs['data-slide-id'];self.texts[self.current]=[]
        if tag=='text':self.collect=True;self.buf=[]
    def handle_data(self,data):
        if self.collect:self.buf.append(data)
    def handle_endtag(self,tag):
        if tag=='text' and self.collect:self.texts[self.current].append(''.join(self.buf));self.collect=False
parser=DiagramTexts();parser.feed((root/'index.html').read_text(encoding='utf-8'))
baseline=json.loads((root/'validation/design-content-baseline.json').read_text(encoding='utf-8'))
unchanged=[]
for s in notes:
    if s['id'] in HERMES_ORDER:continue
    before=baseline[s['id']]
    assert sorted(parser.texts[s['id']])==before['text'],s['id']
    assert all(s[k]==v for k,v in before['metadata'].items()),s['id']
    unchanged.append(s['id'])
blocks=re.findall(r'```python\n(.*?)```',source,re.S)
for block in blocks:ast.parse(block)
from pypdf import PdfReader
pdf=PdfReader(root/'agent-framework-seminar-2.pdf')
assert len(pdf.pages)==len(expected)
assert all(len(page.extract_text())>20 for page in pdf.pages)
result={'blueprintCoverage':42,'audienceSlides':len(expected),'speakerSpecCoverage':42,'sourcesExplanations':len(notes),'reservedExcluded':manifest['reserved'],
        'hermesPages':[6,21],'hermesSlides':len(HERMES_ORDER),'unmodifiedOtherSlides':len(unchanged),
        'sourceReferencesPreserved':True,'pythonSnippetsSyntaxChecked':len(blocks),
        'pdfPages':len(pdf.pages),'blankPdfPages':0,'result':'pass'}
(root/'validation/content-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
