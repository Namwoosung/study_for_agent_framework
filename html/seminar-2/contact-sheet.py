"""Arrange already-rendered browser screenshots for manual visual QA."""
from pathlib import Path
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent/'validation'
paths=sorted((root/'screenshots').glob('S*.png'))
for start in range(0,len(paths),6):
    canvas=Image.new('RGB',(1280,1140),'#070b16')
    draw=ImageDraw.Draw(canvas)
    for index,path in enumerate(paths[start:start+6]):
        x=(index%2)*640;y=(index//2)*380
        draw.text((x+10,y+2),path.stem,fill='#EFF4FF')
        with Image.open(path) as im:
            canvas.paste(im.resize((640,360)),(x,y+20))
    canvas.save(root/f'contact-{start//6+1}.png')
print(f'{len(paths)} screenshots / {(len(paths)+5)//6} sheets')
