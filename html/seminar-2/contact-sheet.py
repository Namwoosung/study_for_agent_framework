"""Arrange already-rendered browser screenshots for manual visual QA."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import io
import time

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
    buffer=io.BytesIO();canvas.save(buffer,format='PNG')
    for attempt in range(6):
        try:
            (root/f'contact-{start//6+1}.png').write_bytes(buffer.getvalue())
            break
        except OSError:
            if attempt==5:raise
            time.sleep(.35)
print(f'{len(paths)} screenshots / {(len(paths)+5)//6} sheets')
