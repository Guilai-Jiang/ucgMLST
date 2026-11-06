#!/usr/bin/env bash
# Bundle the ucgMLST reference database into a release asset.
#
#   ./scripts/build_db_archive.sh [DB_DIR] [OUTPUT.tar.gz]
set -euo pipefail

DB_DIR="${1:-db}"
OUT="${2:-ucgmlst-db-1.0.tar.gz}"

FILES=(
  staph_aureus.cgMLST
  MLSTdb0.1.fasta
  new_profile_md5.csv
  new_HierCC.HierCC
)

for f in "${FILES[@]}"; do
  if [[ ! -f "$DB_DIR/$f" ]]; then
    echo "Missing $DB_DIR/$f" >&2
    exit 1
  fi
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for f in "${FILES[@]}"; do
  cp "$DB_DIR/$f" "$TMP/"
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp "$ROOT/docs/DATABASE-LICENSES.md" "$TMP/"

tar -czf "$OUT" -C "$TMP" .
echo "Wrote $OUT"
sha256sum "$OUT"
