#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE="$PROGRAMIX_ROOT/apps/programix-core/programix-core.sh"

if [ ! -f "$CORE" ]; then
    echo "ERROR: Programix Core not found."
    exit 1
fi

source "$CORE"

echo "================================"
echo "        🐧 PROGRAMIX"
echo "================================"
echo
echo "Version: $PROGRAMIX_VERSION"
echo "Architecture: $(uname -m)"
echo "Kernel: $(uname -r)"
echo "Hostname: $(hostname)"
echo
echo "Base system:"
echo "$PROGRAMIX_BASE"
echo
echo "Desktop: ${XDG_CURRENT_DESKTOP:-Unknown}"
echo "Session: ${XDG_SESSION_TYPE:-Unknown}"
echo
echo "================================"
echo "Programix development build"