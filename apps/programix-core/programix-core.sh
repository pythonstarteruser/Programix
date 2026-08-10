#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROGRAMIX_CONFIG="$PROGRAMIX_ROOT/config/programix.conf"

if [ ! -f "$PROGRAMIX_CONFIG" ]; then
    echo "ERROR: Programix configuration not found."
    return 1 2>/dev/null || exit 1
fi

source "$PROGRAMIX_CONFIG"

programix_info() {
    echo "Programix $PROGRAMIX_VERSION"
    echo "Base: $PROGRAMIX_BASE"
    echo "Architecture: $(uname -m)"
    echo "Kernel: $(uname -r)"
}

programix_is_command_available() {
    command -v "$1" >/dev/null 2>&1
}

programix_is_service_active() {
    systemctl is-active --quiet "$1"
}

programix_is_user_service_active() {
    systemctl --user is-active --quiet "$1" 2>/dev/null
}