#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

programix_launcher() {
    clear

    echo "================================"
    echo "        🐧 PROGRAMIX OS"
    echo "          APPLICATIONS"
    echo "================================"
    echo

    echo "[1] System Information"
    echo "[2] System Check"
    echo "[3] Hardware"
    echo "[4] Settings"
    echo "[5] Exit"

    echo
    echo "================================"

    read -rp "Select application: " choice

    case "$choice" in
        1)
            "$PROGRAMIX_ROOT/scripts/programix-info.sh"
            ;;

        2)
            "$PROGRAMIX_ROOT/scripts/programix-system-check.sh"
            ;;

        3)
            "$PROGRAMIX_ROOT/scripts/programix-hardware.sh"
            ;;

        4)
            source "$PROGRAMIX_ROOT/apps/programix-core/programix-core.sh"
            programix_settings
            ;;

        5)
            return 0
            ;;

        *)
            echo
            echo "Unknown application."
            ;;
    esac
}