#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CORE="$PROGRAMIX_ROOT/apps/programix-core/programix-core.sh"

source "$CORE"

while true; do
    clear

    echo "================================"
    echo "        🐧 PROGRAMIX OS"
    echo "================================"
    echo
    echo "Version: $PROGRAMIX_VERSION"
    echo
    echo "[1] System Information"
    echo "[2] System Check"
    echo "[3] Hardware"
    echo "[4] Settings"
    echo "[5] Exit"
    echo
    echo "================================"
    read -rp "Select: " choice

    case "$choice" in
        1)
            clear
            "$PROGRAMIX_ROOT/scripts/programix-info.sh"
            read -rp "Press Enter to continue..."
            ;;

        2)
            clear
            "$PROGRAMIX_ROOT/scripts/programix-system-check.sh"
            read -rp "Press Enter to continue..."
            ;;

        3)
            clear
            "$PROGRAMIX_ROOT/scripts/programix-hardware.sh"
            read -rp "Press Enter to continue..."
            ;;

        4)
            clear
            programix_settings
            read -rp "Press Enter to continue..."
            ;;

        5)
            clear
            echo "Goodbye from ProgramixOS! 🐧"
            exit 0
            ;;

        *)
            echo
            echo "Invalid option."
            sleep 1
            ;;
    esac
done