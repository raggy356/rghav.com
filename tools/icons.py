#!/usr/bin/env python3
"""Build an inline SVG sprite of Lucide icons from Blueberry's icon library (plus a hand-drawn bat).
Usage: tools/icons.py pill scissors dna bat  > sprite.html     (then paste where %%SPRITE%% sits)
       tools/icons.py --list                                    (every icon name available)
Use an icon in a page as:  <svg class="ic" aria-hidden="true"><use href="#i-pill"/></svg>
"""
import re,sys
LIB='/Users/codered/Desktop/codex/AI/purpleberry/testing/blueberry/themegen/themes/purpleberry/theme/snippets/lucide-library.liquid'
EXTRA={'bat':'<path fill="currentColor" stroke="none" d="M12 4.2c-.9 1.9-1.9 2.9-3.4 3.3C7.1 6.2 5 5.6 2.2 6c1.9 1.9 2.4 3.8 2 5.8 1.9-.9 3.8-.5 4.8 1 .9-.5 1.9 0 3 2.2 1.1-2.2 2.1-2.7 3-2.2 1-1.5 2.9-1.9 4.8-1-.4-2 .1-3.9 2-5.8-2.8-.4-4.9.2-6.4 1.5-1.5-.4-2.5-1.4-3.4-3.3z"/>'}
lib=open(LIB).read()
icons={}
for m in re.finditer(r'\{%- when "([a-z0-9-]+)" -%\}(.*?)(?=\{%- (?:when|comment|else|endcase))',lib,re.S):
    icons[m.group(1)]=re.sub(r'\{%- comment -%\}.*?\{%- endcomment -%\}','',m.group(2),flags=re.S).strip()
icons.update(EXTRA)
args=sys.argv[1:]
if not args or args==['--list']:
    print(' '.join(sorted(icons))); sys.exit(0)
missing=[a for a in args if a not in icons]
if missing: sys.exit('not in library: '+' '.join(missing)+'\nrun tools/icons.py --list')
print('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">'+''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{icons[k]}</symbol>' for k in args)+'</svg>')
