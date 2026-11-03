"""Arrange already-rendered browser screenshots for manual visual QA."""
from pathlib import Path
from PIL import Image, ImageDraw
import json

root=Path(__file__).resolve().parent/'validation'
manifest=json.loads((root.parent/'manifest.json').read_text(encoding='utf-8'))
paths=[root/'revision-screenshots'/(s['id']+'.png') for s in manifest['slides']]
for start in range(0,len(paths),6):
    canvas=Image.new('RGB',(1280,1140),'#E9EEF5')
    draw=ImageDraw.Draw(canvas)
    for index,path in enumerate(paths[start:start+6]):
        x=(index%2)*640;y=(index//2)*380
        draw.text((x+10,y+2),path.stem,fill='#172B46')
        with Image.open(path) as im:
            canvas.paste(im.resize((640,360)),(x,y+20))
    canvas.save(root/f'contact-{start//6+1}.png')
print(f'{len(paths)} screenshots / {(len(paths)+5)//6} sheets')
