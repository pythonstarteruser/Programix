#!/usr/bin/env python3

import os
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


PROGRAMIX_ROOT = os.path.expanduser("~/Programix")

SETTINGS_FILE = os.path.join(
    PROGRAMIX_ROOT,
    "config",
    "settings.conf"
)


def load_settings():
    settings = {}

    if not os.path.isfile(SETTINGS_FILE):
        return settings

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip().strip('"')

            settings[key] = value

    return settings


def save_settings(settings):
    lines = [
        "# Programix Settings",
        "",
        f'PROGRAMIX_THEME="{settings["PROGRAMIX_THEME"]}"',
        f'PROGRAMIX_LANGUAGE="{settings["PROGRAMIX_LANGUAGE"]}"',
        f'PROGRAMIX_TIMEZONE="{settings["PROGRAMIX_TIMEZONE"]}"',
        f'PROGRAMIX_NETWORK_MANAGER="{settings["PROGRAMIX_NETWORK_MANAGER"]}"',
        f'PROGRAMIX_AUDIO_SYSTEM="{settings["PROGRAMIX_AUDIO_SYSTEM"]}"',
        f'PROGRAMIX_POWER_PROFILE="{settings["PROGRAMIX_POWER_PROFILE"]}"',
        f'PROGRAMIX_AUTO_UPDATES="{settings["PROGRAMIX_AUTO_UPDATES"]}"',
        ""
    ]

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write("\n".join(lines))


class ProgramixSettings(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)

        self.settings = load_settings()

        self.set_title("Programix Settings")
        self.set_default_size(700, 550)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15
        )

        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)

        # Title
        title = Gtk.Label()

        title.set_markup(
            "<span size='26000' weight='bold'>"
            "⚙️ Programix Settings"
            "</span>"
        )

        main_box.append(title)

        # -------------------------
        # Appearance
        # -------------------------

        appearance_label = Gtk.Label(
            label="Appearance"
        )

        appearance_label.set_xalign(0)

        main_box.append(appearance_label)

        # Theme

        theme_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=15
        )

        theme_label = Gtk.Label(
            label="Theme"
        )

        theme_label.set_xalign(0)

        theme_combo = Gtk.DropDown.new_from_strings(
            [
                "System",
                "Light",
                "Dark"
            ]
        )

        theme_value = self.settings.get(
            "PROGRAMIX_THEME",
            "system"
        ).lower()

        theme_map = {
            "system": 0,
            "light": 1,
            "dark": 2
        }

        theme_combo.set_selected(
            theme_map.get(theme_value, 0)
        )

        theme_box.append(theme_label)
        theme_box.append(theme_combo)

        main_box.append(theme_box)

        # Language

        language_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=15
        )

        language_label = Gtk.Label(
            label="Language"
        )

        language_label.set_xalign(0)

        language_combo = Gtk.DropDown.new_from_strings(
            [
                "pl_PL",
                "en_US"
            ]
        )

        language_value = self.settings.get(
            "PROGRAMIX_LANGUAGE",
            "pl_PL"
        )

        language_combo.set_selected(
            0 if language_value == "pl_PL" else 1
        )

        language_box.append(language_label)
        language_box.append(language_combo)

        main_box.append(language_box)

        # -------------------------
        # System
        # -------------------------

        system_label = Gtk.Label(
            label="System"
        )

        system_label.set_xalign(0)

        main_box.append(system_label)

        # Network

        network = Gtk.Label(
            label="Network: " + self.settings.get(
                "PROGRAMIX_NETWORK_MANAGER",
                "Unknown"
            )
        )

        network.set_xalign(0)

        main_box.append(network)

        # Audio

        audio = Gtk.Label(
            label="Audio: " + self.settings.get(
                "PROGRAMIX_AUDIO_SYSTEM",
                "Unknown"
            )
        )

        audio.set_xalign(0)

        main_box.append(audio)

        # Timezone

        timezone = Gtk.Label(
            label="Timezone: " + self.settings.get(
                "PROGRAMIX_TIMEZONE",
                "Unknown"
            )
        )

        timezone.set_xalign(0)

        main_box.append(timezone)

        # Power profile

        power = Gtk.Label(
            label="Power profile: " + self.settings.get(
                "PROGRAMIX_POWER_PROFILE",
                "unknown"
            )
        )

        power.set_xalign(0)

        main_box.append(power)

        # Automatic updates

        updates = Gtk.CheckButton(
            label="Automatic updates"
        )

        updates.set_active(
            self.settings.get(
                "PROGRAMIX_AUTO_UPDATES",
                "false"
            ).lower() == "true"
        )

        main_box.append(updates)

        # -------------------------
        # Apply button
        # -------------------------

        apply_button = Gtk.Button(
            label="Apply"
        )

        apply_button.connect(
            "clicked",
            self.apply_settings,
            theme_combo,
            language_combo,
            updates
        )

        main_box.append(apply_button)

        self.set_child(main_box)

    def apply_settings(
        self,
        button,
        theme_combo,
        language_combo,
        updates
    ):
        themes = [
            "system",
            "light",
            "dark"
        ]

        languages = [
            "pl_PL",
            "en_US"
        ]

        self.settings["PROGRAMIX_THEME"] = themes[
            theme_combo.get_selected()
        ]

        self.settings["PROGRAMIX_LANGUAGE"] = languages[
            language_combo.get_selected()
        ]

        self.settings["PROGRAMIX_AUTO_UPDATES"] = (
            "true"
            if updates.get_active()
            else "false"
        )

        save_settings(self.settings)

        print("Programix settings saved.")


class ProgramixSettingsApp(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="org.programix.settings"
        )

    def do_activate(self):
        window = ProgramixSettings(self)
        window.present()


app = ProgramixSettingsApp()
app.run()