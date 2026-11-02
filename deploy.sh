#!/bin/zsh
# Stamp every page's build meta (open tabs self-reload on a new stamp), commit, push.
# Usage: ./deploy.sh "commit message"
set -e
cd "$(dirname "$0")"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
for f in index.html */index.html; do
  [ -f "$f" ] && grep -q 'name="build"' "$f" && sed -i '' -E "s/(<meta name=\"build\" content=\")[^\"]*(\">)/\1$stamp\2/" "$f"
done
git add -A -- . ':!tools/__pycache__'
git -c user.name=raggy -c user.email=akrasia@tuta.com commit -q -m "${1:-deploy $stamp}" && git push -q origin main
echo "pushed build $stamp"
echo "$stamp" > .last_build
