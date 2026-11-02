#!/bin/zsh
# Wait for GitHub Pages to serve the last deployed build at a path, bypassing any local DNS cache.
# Usage: tools/verify.sh [/slug/]   (default /)
cd "$(dirname "$0")/.."
path="${1:-/}"; stamp=$(cat .last_build 2>/dev/null)
for i in $(seq 1 30); do
  body=$(curl -s --max-time 10 --resolve rghav.com:443:185.199.108.153 "https://rghav.com${pagepath}?v=$RANDOM")
  if echo "$body" | grep -q "content=\"$stamp\""; then echo "live: https://rghav.com${pagepath} (build $stamp, after $((i*6))s)"; exit 0; fi
  sleep 6
done
echo "NOT LIVE after 180s: https://rghav.com${pagepath} (wanted build $stamp)"; exit 1
