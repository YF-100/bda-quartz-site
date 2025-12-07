#!/usr/bin/env bash
# minimal_nb_quartz.sh
# Author: Badr TAJINI / Adapted setup for ESIEE Big Data Analytics Lab

set -euo pipefail

NOTEBOOK_PATH="${1:-}"
if [[ -z "$NOTEBOOK_PATH" ]]; then
  echo "Usage: bash minimal_nb_quartz.sh /abs/path/to/notebook.ipynb"
  exit 1
fi

# 1️⃣ Clone Quartz minimal template
WORKDIR="$(pwd)"
QUARTZ_DIR="$WORKDIR/quartz-min"
rm -rf "$QUARTZ_DIR"
git clone https://github.com/jackyzha0/quartz.git "$QUARTZ_DIR"

cd "$QUARTZ_DIR"
# 2️⃣ Install dependencies
npm ci || npm install

# 3️⃣ Ensure Assets emitter is enabled in quartz.config.ts
if ! grep -q "emitAssets" quartz.config.ts; then
  echo "// Added automatically to support static assets" >> quartz.config.ts
  echo "export const emitAssets = true;" >> quartz.config.ts
fi

# 4️⃣ Convert notebook → HTML
STATIC_DIR="static/nb"
mkdir -p "$STATIC_DIR"
OUT_HTML="$STATIC_DIR/$(basename "${NOTEBOOK_PATH%.ipynb}.html")"
jupyter nbconvert --to html "$NOTEBOOK_PATH" --output "$OUT_HTML"

# 5️⃣ Create wrapper content with iframe
CONTENT_DIR="content/labs-final"
mkdir -p "$CONTENT_DIR"
WRAPPER_MD="$CONTENT_DIR/$(basename "${NOTEBOOK_PATH%.ipynb}.md")"
cat > "$WRAPPER_MD" <<EOF
---
title: "$(basename "${NOTEBOOK_PATH%.ipynb}")"
---

<iframe src="/$OUT_HTML" width="100%" height="800px" frameborder="0"></iframe>
EOF

# 6️⃣ Copy adjacent CSV dataset if exists
DATASET="$(dirname "$NOTEBOOK_PATH")/*.csv"
if ls $DATASET >/dev/null 2>&1; then
  cp $DATASET "$CONTENT_DIR" || true
fi

# 7️⃣ Build Quartz
npx quartz build

echo "✅ Notebook integrated successfully!"
echo "👉 Built HTML available under: $QUARTZ_DIR/public/labs-final/$(basename "${NOTEBOOK_PATH%.ipynb}.html")"
