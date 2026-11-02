#!/usr/bin/env python3
"""Make web-sized images for a page. Run with Purpleberry's venv python (has Pillow).
  tools/img.py photo <in> <out.jpg> [maxpx=1000] [quality=84]   -> resized JPEG, EXIF stripped
  tools/img.py crop-bars <in> <out.jpg>                          -> strips black letterbox bars top/bottom, then as photo
  tools/img.py gif <in.gif|mp4> <out.gif> [width=480] [fps=12]   -> palette-optimised GIF via ffmpeg (keep under ~3 MB, lazy-load it)
  tools/img.py og <slug> "<title html>" "<subtitle>"             -> <slug>/og.png (1200x630) from templates/og.html
"""
import sys,subprocess,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def photo(i,o,maxpx=1000,q=84):
    from PIL import Image
    im=Image.open(i).convert('RGB'); im.thumbnail((int(maxpx),int(maxpx))); im.save(o,quality=int(q),optimize=True); print(o,im.size,os.path.getsize(o)//1024,'KB')
def crop_bars(i,o):
    from PIL import Image,ImageStat
    im=Image.open(i).convert('RGB'); W,H=im.size; g=im.convert('L')
    rows=[ImageStat.Stat(g.crop((0,y,W,y+1))).mean[0] for y in range(H)]
    top=next(y for y in range(H) if rows[y]>18); bot=next(y for y in range(H-1,-1,-1) if rows[y]>18)
    im.crop((0,top,W,bot+1)).save(o,quality=84,optimize=True); print(o,'cropped bars',top,H-1-bot)
def gif(i,o,w=480,fps=12):
    vf=f"fps={fps},scale={w}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle"
    subprocess.run(['ffmpeg','-v','error','-y','-i',i,'-vf',vf,'-loop','0',o],check=True); print(o,os.path.getsize(o)//1024,'KB')
def og(slug,title,sub):
    t=open(f'{ROOT}/templates/og.html').read()
    t=re.sub(r'<h1>.*?</h1>',f'<h1>{title}</h1>',t,flags=re.S); t=re.sub(r'<div class="sub">.*?</div>',f'<div class="sub">{sub}</div>',t,flags=re.S)
    tmp=f'{ROOT}/{slug}/_og.html'; open(tmp,'w').write(t)
    srv=subprocess.Popen(['python3','-m','http.server','8762','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        import time; time.sleep(1)
        subprocess.run(['playwright-cli','-s=og','open','about:blank'],capture_output=True)
        code=f"async (page) => {{ await page.setViewportSize({{width:1200,height:630}}); await page.goto('http://127.0.0.1:8762/{slug}/_og.html'); await page.waitForTimeout(2000); await page.screenshot({{path:'{ROOT}/{slug}/og.png'}}); return 'ok'; }}"
        subprocess.run(['playwright-cli','-s=og','run-code',code],capture_output=True)
        subprocess.run(['playwright-cli','-s=og','close'],capture_output=True)
    finally:
        srv.kill(); os.remove(tmp)
    print(f'{slug}/og.png', os.path.getsize(f'{ROOT}/{slug}/og.png')//1024,'KB')
cmd,*a=sys.argv[1:] or ['help']
{'photo':photo,'crop-bars':crop_bars,'gif':gif,'og':og}.get(cmd,lambda *x: print(__doc__))(*a)
