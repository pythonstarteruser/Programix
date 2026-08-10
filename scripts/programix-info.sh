#!/usr/bin/env bash

echo "================================"
echo "        🐧 PROGRAMIX"
echo "================================"
echo
echo "Version: 0.1.0-dev"
echo "Architecture: $(uname -m)"
echo "Kernel: $(uname -r)"
echo "Hostname: $(hostname)"
echo

if command -v lsb_release >/dev/null 2>&1; then
    echo "Base system:"
    lsb_release -ds
fi

echo
echo "Desktop: ${XDG_CURRENT_DESKTOP:-Unknown}"
echo "Session: ${XDG_SESSION_TYPE:-Unknown}"
echo
echo "================================"
echo "Programix development build"
echo "================================"