#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

CORE="$PROGRAMIX_ROOT/apps/programix-core/programix-core.sh"
LAUNCHER="$PROGRAMIX_ROOT/apps/programix-launcher/programix-launcher.sh"

source "$CORE"

if [ ! -f "$LAUNCHER" ]; then
    echo "ERROR: Programix Launcher not found."
    exit 1
fi

source "$LAUNCHER"

while true; do
    clear

    echo "================================"
    echo "        🐧 PROGRAMIX OS"
    echo "================================"
    echo
    echo "Version: $PROGRAMIX_VERSION"
    echo
    echo "[1] Applications"
    echo "[2] Exit"
    echo
    echo "================================"

    read -rp "Select: " choice

    case "$choice" in
        1)
            programix_launcher
            read -rp "Press Enter to continue..."
            ;;

        2)
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