#!/usr/bin/env bash

PROGRAMIX_NAME="Programix"
PROGRAMIX_VERSION="0.1.0-dev"
PROGRAMIX_BASE="Ubuntu 26.04 LTS"

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