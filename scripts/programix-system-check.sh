#!/usr/bin/env bash

echo "================================"
echo "     🐧 PROGRAMIX SYSTEM CHECK"
echo "================================"
echo

errors=0
warnings=0

check_command() {
    local name="$1"
    local command="$2"

    if command -v "$command" >/dev/null 2>&1; then
        echo "✓ $name"
    else
        echo "✗ $name"
        ((errors++))
    fi
}

check_service() {
    local name="$1"
    local service="$2"

    if systemctl is-active --quiet "$service"; then
        echo "✓ $name"
    else
        echo "⚠ $name"
        ((warnings++))
    fi
}

echo "Core system:"
check_command "Linux kernel" "uname"
check_command "systemd" "systemctl"
check_command "APT" "apt"

echo
echo "Desktop:"

if command -v gnome-shell >/dev/null 2>&1; then
    echo "✓ GNOME"
else
    echo "✗ GNOME"
    ((errors++))
fi

if [ "${XDG_SESSION_TYPE:-}" = "wayland" ]; then
    echo "✓ Wayland"
else
    echo "⚠ Wayland session not detected"
    ((warnings++))
fi

echo
echo "System services:"
check_service "NetworkManager" "NetworkManager.service"

if systemctl --user is-active --quiet pipewire.service 2>/dev/null; then
    echo "✓ PipeWire"
else
    echo "⚠ PipeWire"
    ((warnings++))
fi

check_service "fwupd" "fwupd.service"

echo
echo "System information:"

if command -v lsb_release >/dev/null 2>&1; then
    distro=$(lsb_release -ds)
    echo "  Base: $distro"
fi

echo "  Kernel: $(uname -r)"
echo "  Architecture: $(uname -m)"
echo "  Session: ${XDG_SESSION_TYPE:-Unknown}"

echo
echo "================================"

if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo "SYSTEM STATUS: OK ✓"
elif [ "$errors" -eq 0 ]; then
    echo "SYSTEM STATUS: WARNING ⚠"
else
    echo "SYSTEM STATUS: ERROR ✗"
fi

echo "Errors: $errors"
echo "Warnings: $warnings"

echo "================================"

exit "$errors"