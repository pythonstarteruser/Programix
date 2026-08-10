#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORE="$PROGRAMIX_ROOT/apps/programix-core/programix-core.sh"

if [ ! -f "$CORE" ]; then
    echo "ERROR: Programix Core not found."
    exit 1
fi

source "$CORE"

ERRORS=0
WARNINGS=0

check_command() {
    if programix_is_command_available "$1"; then
        echo "✓ $2"
    else
        echo "✗ $2"
        ((ERRORS++))
    fi
}

check_service() {
    if programix_is_service_active "$1"; then
        echo "✓ $2"
    else
        echo "✗ $2"
        ((ERRORS++))
    fi
}

echo "================================"
echo "     🐧 PROGRAMIX SYSTEM CHECK"
echo "================================"
echo

echo "Core system:"
check_command "uname" "Linux kernel"
check_command "systemctl" "systemd"
check_command "apt" "APT"

echo
echo "Desktop:"
check_command "gnome-shell" "GNOME"

if [ "${XDG_SESSION_TYPE:-}" = "wayland" ]; then
    echo "✓ Wayland"
else
    echo "⚠ Wayland"
    ((WARNINGS++))
fi

echo
echo "System services:"
check_service "NetworkManager.service" "NetworkManager"
check_service "fwupd.service" "fwupd"

if programix_is_user_service_active "pipewire.service"; then
    echo "✓ PipeWire"
else
    echo "⚠ PipeWire"
    ((WARNINGS++))
fi

echo
echo "System information:"
echo "  Base: $PROGRAMIX_BASE"
echo "  Kernel: $(uname -r)"
echo "  Architecture: $(uname -m)"
echo "  Session: ${XDG_SESSION_TYPE:-Unknown}"

echo
echo "================================"

if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo "SYSTEM STATUS: OK ✓"
else
    echo "SYSTEM STATUS: ERROR ✗"
fi

echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo "================================"