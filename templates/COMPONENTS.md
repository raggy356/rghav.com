# Components in templates/page.html

Every class below is already styled in the template's `<style>`. Copy a snippet, fill it, keep the class names.
Icons: `<svg class="ic" aria-hidden="true"><use href="#i-NAME"/></svg>` after `tools/icons.py NAME ...` has filled `%%SPRITE%%`.
Anything that should animate in gets `class="... reveal"` and an optional `style="--i:N"` stagger.

## Section shell
```html
<section id="slug" data-chapter="01 · Chapter name">
  <div class="wrap">
    <div class="eyebrow reveal">01</div>
    <h2 class="reveal" style="--i:1">Heading</h2>
    <p class="lede reveal" style="--i:2">One or two sentences. <b>Bold</b> for the key phrase.</p>
    ...
  </div>
</section>
```
`data-chapter` feeds the little label top-right as the reader scrolls. The `.two` wrapper puts eyebrow+h2 beside the lede on desktop.

## Short version (numbered rows with an icon)
```html
<div class="tldr">
  <div class="row reveal" style="--i:0"><div class="n"><svg class="ic" aria-hidden="true"><use href="#i-pill"/></svg></div><p>Point with a <b>bold phrase</b>.<small>One line of support.</small></p></div>
</div>
```

## Ladder (rungs with evidence pips; `.top` = highlighted)
```html
<div class="ladder">
  <div class="rung top reveal" style="--i:0"><div class="ico"><svg class="ic" aria-hidden="true"><use href="#i-pill"/></svg></div><div>
    <div class="k">Rung one</div><h3>Name</h3><p>Body with <b>the number</b>.</p>
    <div class="pips"><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><span>Label</span></div>
  </div></div>
</div>
```
2 columns at 720px, 4 at 1000px.

## Chart (treatment vs placebo bars; any two-value comparison)
```html
<div class="chart reveal">
  <div class="legend"><span><i style="background:var(--grad)"></i>Treatment</span><span><i style="background:var(--line-2)"></i>Placebo</span></div>
  <div class="crow"><div class="lab"><b>Row name</b><small>what the number is</small></div>
    <div class="bars">
      <div class="bar drug"><div class="track"><div class="fill" style="--w:75%"></div></div><div class="v">75%</div></div>
      <div class="bar pl"><div class="track"><div class="fill" style="--w:28%"></div></div><div class="v">28%</div></div>
    </div></div>
  <div class="cap">Source line in small grey text.</div>
</div>
```
Bars animate to `--w` when the block reveals; the red bar gets a pulsing tip.

## Two panels with a big number
```html
<div class="duo">
  <div class="panel reveal" style="--i:0"><div class="hd"><svg class="ic" aria-hidden="true"><use href="#i-activity"/></svg><h3>Title</h3></div><div class="big">2.0<small>unit or context</small></div><p>Body.</p></div>
</div>
<p class="note reveal">A quiet one-liner under the panels.</p>
```

## Yes / no columns
```html
<div class="yn">
  <div class="col reveal" style="--i:0"><h3><svg class="ic" aria-hidden="true"><use href="#i-circle-check-big"/></svg>Has a signal</h3>
    <div class="li"><svg class="ic" aria-hidden="true"><use href="#i-circle-check-big"/></svg><div><b>Item</b><span>Why.</span></div></div>
  </div>
  <div class="col no reveal" style="--i:1"><h3><svg class="ic" aria-hidden="true"><use href="#i-x-circle"/></svg>No signal</h3>
    <div class="li"><svg class="ic" aria-hidden="true"><use href="#i-x-circle"/></svg><div><b>Item</b><span>Why.</span></div></div>
  </div>
</div>
```

## Timeline (`.hl` = the headline event, glows)
```html
<div class="tl" id="tl"><div class="draw"></div>
  <div class="ev reveal"><div class="dot"><svg class="ic" aria-hidden="true"><use href="#i-brain"/></svg></div><div class="yr">2026</div><h3>Name</h3><p>Body.</p><span class="pill">Status · tag</span></div>
  <div class="ev hl reveal">...</div>
</div>
```

## Numbered steps
```html
<div class="steps">
  <div class="step reveal" style="--i:0"><div><h3>Do this</h3><p>How.</p></div></div>
</div>
<p class="disclaimer reveal">Small grey caveat.</p>
```

## Meme / picture with caption (tilted frame, sways)
```html
<figure class="meme reveal"><div class="fr"><img src="assets/name.jpg" alt="what is in it" loading="lazy" width="W" height="H"></div><figcaption><b>Lead.</b> Dry caption.</figcaption></figure>
```
Width/height = the real pixel size (`tools/img.py photo` prints it) so nothing jumps while loading.

## Hero extras
```html
<div class="herocat"><img src="assets/x.jpg" alt="" width="W" height="H"></div>   <!-- big tilted picture, bobs; tilts to cursor on desktop -->
<div class="dedic"><span class="ics"><svg class="ic" aria-hidden="true"><use href="#i-bat"/></svg><svg class="ic" aria-hidden="true"><use href="#i-heart"/></svg></span><span>For someone.</span></div>
<div class="embers">14× <i style="left:N%;--dx:Npx;animation-duration:Ns;animation-delay:Ns"></i></div>   <!-- rising embers -->
<div class="batfly"><svg aria-hidden="true"><use href="#i-bat"/></svg></div>                               <!-- bat glides across -->
```

## Collapsible source list
```html
<section id="sources" data-chapter="The literature" style="padding-top:50px;padding-bottom:30px"><div class="wrap">
  <details><summary><span>The literature</span><span class="pm">+</span></summary>
    <div class="src"><a href="URL"><b>Journal YEAR</b> · what it is</a></div>
  </details>
</div></section>
```
