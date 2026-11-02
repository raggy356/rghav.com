#!/usr/bin/env python3
"""Find meme/photo candidates on Reddit via RSS (the JSON API is blocked on this network; RSS is not).
  tools/memes.py r/blackcats [query] [--gif]   -> downloads up to 36 candidates to render/memes/ and builds render/memes/sheet.jpg
Then look at the sheet, pick numbers, and run tools/img.py photo on the ones you want.
Run with Purpleberry's venv python (Pillow)."""
import sys,re,html,subprocess,os,json
sub=sys.argv[1].replace('r/',''); q=[a for a in sys.argv[2:] if not a.startswith('--')]; want_gif='--gif' in sys.argv
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'
urls=[f'https://www.reddit.com/r/{sub}/top/.rss?t=month&limit=100',f'https://www.reddit.com/r/{sub}/top/.rss?t=year&limit=100']
if q: urls.append(f'https://www.reddit.com/r/{sub}/search.rss?q={"+".join(q)}&restrict_sr=1&sort=top&t=all&limit=100')
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out=f'{ROOT}/render/memes'; os.makedirs(out,exist_ok=True)
ext='gif' if want_gif else 'jpg|jpeg|png'; rows=[]; seen=set()
for u in urls:
    x=html.unescape(subprocess.run(['curl','-s','-A',UA,'--max-time','20',u],capture_output=True,text=True).stdout)
    for e in re.findall(r'<entry>(.*?)</entry>',x,re.S):
        t=re.search(r'<title>(.*?)</title>',e,re.S); t=t.group(1)[:70] if t else ''
        for m in re.findall(rf'https://(?:i\.redd\.it|i\.imgur\.com)/[a-z0-9]+\.(?:{ext})',e):
            if m not in seen: seen.add(m); rows.append({'title':t,'url':m})
rows=rows[:36]
for i,r in enumerate(rows):
    f=f"{out}/{i:02d}.{r['url'].rsplit('.',1)[1]}"; subprocess.run(['curl','-s','-A',UA,'--max-time','40','-o',f,r['url']]); r['file']=f
json.dump(rows,open(f'{out}/cands.json','w'),indent=1)
from PIL import Image,ImageDraw
cell=300; cols=6; n=len(rows); sheet=Image.new('RGB',(cols*cell,((n+cols-1)//cols)*(cell+34)),(20,20,24)); d=ImageDraw.Draw(sheet)
for i,r in enumerate(rows):
    try: im=Image.open(r['file']); im.seek(0); im=im.convert('RGB'); im.thumbnail((cell-8,cell-8))
    except Exception: continue
    x=(i%cols)*cell; y=(i//cols)*(cell+34); sheet.paste(im,(x+4,y+4)); d.text((x+6,y+cell+4),f"{i:02d} {r['title'][:40]}",fill=(240,240,240))
sheet.save(f'{out}/sheet.jpg',quality=80); print(f'{n} candidates -> {out}/sheet.jpg (files {out}/NN.ext, titles in cands.json)')
