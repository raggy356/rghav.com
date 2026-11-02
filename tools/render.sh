#!/bin/zsh
# Render a page at phone (375) and desktop (1366) widths with playwright-cli, report overflow + console errors.
# Usage: tools/render.sh /slug/   -> writes render/<slug>_mobile.png, render/<slug>_desktop.png (gitignored)
# playwright-cli blocks file: URLs, so the repo is served over http on a local port.
cd "$(dirname "$0")/.."
pagepath="${1:-/}"; name=$(echo "$pagepath" | tr -c 'a-z0-9' '_' | sed 's/^_*//;s/_*$//'); [ -z "$name" ] && name=home
mkdir -p render; port=8761
python3 -m http.server $port --bind 127.0.0.1 >/dev/null 2>&1 & srv=$!; sleep 1
playwright-cli -s=rg open about:blank >/dev/null 2>&1
playwright-cli -s=rg run-code "async (page) => {
  const u='http://127.0.0.1:$port$pagepath'; const errs=[]; page.on('pageerror',e=>errs.push(e.message));
  await page.setViewportSize({width:375,height:812}); await page.goto(u); await page.waitForTimeout(2000);
  await page.evaluate(()=>document.querySelectorAll('.reveal,.tl').forEach(e=>e.classList.add('in'))); await page.waitForTimeout(1500);
  await page.screenshot({path:'$PWD/render/${name}_mobile.png',fullPage:true});
  const sw=await page.evaluate(()=>document.documentElement.scrollWidth);
  await page.setViewportSize({width:1366,height:860}); await page.goto(u); await page.waitForTimeout(1800);
  await page.evaluate(()=>document.querySelectorAll('.reveal,.tl').forEach(e=>e.classList.add('in'))); await page.waitForTimeout(1500);
  await page.screenshot({path:'$PWD/render/${name}_desktop.png',fullPage:true});
  return 'mobile scrollWidth='+sw+(sw>375?' OVERFLOW':' ok')+' | pageerrors='+errs.length+(errs.length?' '+errs.join(' // '):'');
}" 2>&1 | grep -oE '^"mobile[^"]*"' | tr -d '"'
playwright-cli -s=rg close >/dev/null 2>&1; kill $srv 2>/dev/null
echo "screenshots: render/${name}_mobile.png render/${name}_desktop.png"
