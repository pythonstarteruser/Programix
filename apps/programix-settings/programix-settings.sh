#!/usr/bin/env bash

PROGRAMIX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SETTINGS="$PROGRAMIX_ROOT/config/settings.conf"

if [ ! -f "$SETTINGS" ]; then
    echo "ERROR: Programix settings not found."
    exit 1
fi

source "$SETTINGS"

while true; do
    clear

    echo "================================"
    echo "      🐧 PROGRAMIX SETTINGS"
    echo "================================"
    echo
    echo "Theme:          $PROGRAMIX_THEME"
    echo "Language:       $PROGRAMIX_LANGUAGE"
    echo "Timezone:       $PROGRAMIX_TIMEZONE"
    echo "Network:        $PROGRAMIX_NETWORK_MANAGER"
    echo "Audio:          $PROGRAMIX_AUDIO_SYSTEM"
    echo "Power profile:  $PROGRAMIX_POWER_PROFILE"
    echo "Auto updates:   $PROGRAMIX_AUTO_UPDATES"
    echo
    echo "--------------------------------"
    echo "[1] Change theme"
    echo "[2] Back"
    echo
    echo "================================"

    read -rp "Select: " choice

    case "$choice" in
        1)
            echo
            echo "Available themes:"
            echo "[1] system"
            echo "[2] light"
            echo "[3] dark"
            echo

            read -rp "Select theme: " theme_choice

            case "$theme_choice" in
                1)
                    PROGRAMIX_THEME="system"
                    ;;
                2)
                    PROGRAMIX_THEME="light"
                    ;;
                3)
                    PROGRAMIX_THEME="dark"
                    ;;
                *)
                    echo "Invalid theme."
                    sleep 1
                    continue
                    ;;
            esac

            sed -i "s/^PROGRAMIX_THEME=.*/PROGRAMIX_THEME=\"$PROGRAMIX_THEME\"/" "$SETTINGS"

            echo
            echo "Theme changed to: $PROGRAMIX_THEME"
            sleep 1
            ;;

        2)
            break
            ;;

        *)
            echo
            echo "Invalid option."
            sleep 1
            ;;
    esac
done