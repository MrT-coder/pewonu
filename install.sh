#!/bin/sh
# PeWoNu installer for macOS and Linux. One command installs uv, Python, the code and every
# dependency, then starts the system:
#   curl -LsSf https://raw.githubusercontent.com/MrT-coder/pewonu/develop/install.sh | sh
# Optional environment variables: PEWONU_DIR (default ~/pewonu), PEWONU_BRANCH (default develop),
# PEWONU_REPO (git URL), PEWONU_NO_START=1 (install only, do not start).
set -eu

REPO="${PEWONU_REPO:-https://github.com/MrT-coder/pewonu.git}"
BRANCH="${PEWONU_BRANCH:-develop}"
DIR="${PEWONU_DIR:-$HOME/pewonu}"

say() { printf '%s\n' "$*"; }

if ! command -v uv >/dev/null 2>&1; then
  say "==> Installing uv (it also downloads the right Python for you)"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  export PATH
fi

if [ -d "$DIR/.git" ]; then
  say "==> Updating $DIR"
  git -C "$DIR" pull --ff-only
elif command -v git >/dev/null 2>&1; then
  say "==> Downloading PeWoNu to $DIR"
  git clone --depth 1 --branch "$BRANCH" "$REPO" "$DIR"
else
  say "==> git not found: downloading the source archive to $DIR"
  mkdir -p "$DIR"
  curl -LsSf "https://github.com/MrT-coder/pewonu/archive/refs/heads/$BRANCH.tar.gz" |
    tar -xz --strip-components=1 -C "$DIR"
fi

cd "$DIR"
say "==> Installing Python and dependencies (first time takes a few minutes)"
uv sync --extra astronaut --extra ground

say ""
say "PeWoNu is installed in $DIR"
say "Start it any time with:  cd \"$DIR\" && uv run pewonu"
say "Astronaut app: http://127.0.0.1:8550  (codes AST-0001, AST-0002, AST-0003)"
say "Ground base:   http://127.0.0.1:8560"
if [ "${PEWONU_NO_START:-}" = "1" ]; then
  exit 0
fi
say "==> Starting PeWoNu (press Ctrl+C to stop)"
exec uv run pewonu
