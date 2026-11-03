"""Check the current repository layout, local links, and relocation inventory."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re

root=Path(__file__).resolve().parents[2]
errors=[]
checked=0

def check(file,uri):
    global checked
    parts=urlsplit(uri.strip('<>'))
    if parts.scheme or not parts.path or uri.startswith('/'):return
    checked+=1
    target=(file.parent/unquote(parts.path)).resolve()
    if not target.exists():errors.append(f'{file.relative_to(root)} -> {uri}')

class Links(HTMLParser):
    def __init__(self,file):super().__init__();self.file=file
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value:check(self.file,value)

for folder in (root/'study',root/'presentations'):
    for file in folder.rglob('*'):
        if file.suffix=='.html':Links(file).feed(file.read_text(encoding='utf-8'))
        elif file.suffix=='.md':
            body=re.sub(r'```[\s\S]*?```','',file.read_text(encoding='utf-8'))
            for uri in re.findall(r'\]\(([^)\n]+)\)',body):check(file,uri)
for name in ('index.html','README.md','AGENTS.md'):
    file=root/name
    if file.suffix=='.html':Links(file).feed(file.read_text(encoding='utf-8'))
    else:
        for uri in re.findall(r'\]\(([^)\n]+)\)',file.read_text(encoding='utf-8')):check(file,uri)

notes=json.loads((root/'presentations/seminar-2/notes.json').read_text(encoding='utf-8'))
for slide in notes:
    for evidence in slide.get('localEvidence',[]):
        if not (root/evidence['path']).is_file():errors.append('Sources: '+evidence['path'])
inventory=json.loads((root/'archive/reorganization-map.json').read_text(encoding='utf-8'))
for entry in inventory['fileMap']:
    if not (root/entry['new']).is_file():errors.append('Relocated file missing: '+entry['new'])
directories=sorted(p.name for p in root.iterdir() if p.is_dir() and p.name!='.git')
if directories!=['archive','presentations','study']:errors.append('Unexpected root directories: '+str(directories))
report={'result':'fail' if errors else 'pass','rootDirectories':directories,
        'originalFilesPresent':len(inventory['fileMap']),'activeLocalLinksChecked':checked,
        'presentationSlides':len(notes),'errors':errors}
(root/'archive/reorganization-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
