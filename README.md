# rghav.com

Raggy's personal domain. A static site on GitHub Pages: one page per purpose, each at its own path, built by the `/rghav` skill in Claude Code.

- Live: https://rghav.com (custom domain, HTTPS enforced). Repo is **public**, so everything here is public.
- Hosting: GitHub Pages from `main`, root. `rghav.com/<slug>/` serves `<slug>/index.html`.
- DNS: GoDaddy, A records to GitHub's four IPs + `www` CNAME to `raggy356.github.io`.

## Pages

| Path | For | Built |
|---|---|---|
| `/` | Endometriosis research brief, for Dracula's wife | 2026-11-02 |
| `/stl-ava/` | St. Louis stay options with photo slideshows, for Ava | 2026-11-06 |

## Layout

```
index.html          the homepage (a page like any other)
<slug>/index.html   one folder per page, with its images in <slug>/assets/ and its og.png
templates/          page.html (skeleton: tokens, fonts, dark theme, reveal, progress bar, self-update, components)
                    COMPONENTS.md (snippets)   og.html (link-preview card)
tools/              icons.py  img.py  memes.py  render.sh  verify.sh
deploy.sh           stamps every page's build meta, commits, pushes
```

## Workflow in one breath

copy `templates/page.html` to `<slug>/index.html` → fill it (see COMPONENTS.md) → `tools/icons.py a b c` into `%%SPRITE%%` → images through `tools/img.py` → `tools/render.sh /<slug>/` and look at the PNGs → `./deploy.sh "msg"` → `tools/verify.sh /<slug>/`.

## Things that bit us

- GitHub Pages caches HTML for 10 minutes. Pages carry a `build` meta and a 45-second self-update check, so open tabs reload on their own after a deploy. `deploy.sh` is what bumps the stamp; a plain `git push` does not.
- This Mac resolves DNS through Mullvad, which can cache a stale answer for an hour. `tools/verify.sh` goes straight to GitHub's IP with the right hostname, so it is never fooled.
- `playwright-cli` refuses `file:` URLs. `tools/render.sh` serves the repo over a local port instead.
- Reddit's JSON API is blocked from here; the `.rss` feeds work. `tools/memes.py` uses them.
- Pillow lives in Purpleberry's venv: `/Users/codered/Desktop/codex/AI/purpleberry/.venv/bin/python3`. ffmpeg is at `/opt/homebrew/bin/ffmpeg`.
