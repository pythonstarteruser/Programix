#!/usr/bin/env python3

import os
import subprocess
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


PROGRAMIX_SETTINGS = os.path.expanduser(
    "~/Programix/config/settings.conf"
)


def get_programix_theme():
    if not os.path.isfile(PROGRAMIX_SETTINGS):
        return "system"

    with open(
        PROGRAMIX_SETTINGS,
        "r",
        encoding="utf-8"
    ) as file:
        for line in file:
            line = line.strip()

            if line.startswith("PROGRAMIX_THEME="):
                return (
                    line.split("=", 1)[1]
                    .strip()
                    .strip('"')
                    .lower()
                )

    return "system"


def apply_programix_theme():
    theme = get_programix_theme()

    settings = Gtk.Settings.get_default()

    if settings is None:
        return

    if theme == "dark":
        settings.set_property(
            "gtk-theme-name",
            "Adwaita:dark"
        )

    elif theme == "light":
        settings.set_property(
            "gtk-theme-name",
            "Adwaita"
        )


class ProgramixWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("ProgramixOS")
        self.set_default_size(1000, 650)

        # Main layout
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=0
        )

        # Sidebar
        sidebar = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        sidebar.set_margin_top(20)
        sidebar.set_margin_bottom(20)
        sidebar.set_margin_start(15)
        sidebar.set_margin_end(15)
        sidebar.set_size_request(190, -1)

        logo = Gtk.Label()

        logo.set_markup(
            "<span size='18000' weight='bold'>"
            "🐧 Programix"
            "</span>"
        )

        sidebar.append(logo)

        home_button = Gtk.Button(
            label="🏠  Home"
        )

        system_button = Gtk.Button(
            label="💻  System"
        )

        hardware_button = Gtk.Button(
            label="🔧  Hardware"
        )

        apps_button = Gtk.Button(
            label="🧩  Applications"
        )

        settings_button = Gtk.Button(
            label="⚙️  Settings"
        )

        sidebar.append(home_button)
        sidebar.append(system_button)
        sidebar.append(hardware_button)
        sidebar.append(apps_button)

        spacer = Gtk.Box()
        sidebar.append(spacer)

        sidebar.append(settings_button)

        # Content area
        self.content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15
        )

        self.content_box.set_margin_top(30)
        self.content_box.set_margin_bottom(30)
        self.content_box.set_margin_start(30)
        self.content_box.set_margin_end(30)

        main_box.append(sidebar)
        main_box.append(self.content_box)

        self.set_child(main_box)

        # Button actions
        home_button.connect(
            "clicked",
            self.show_home
        )

        system_button.connect(
            "clicked",
            self.show_system_info
        )

        hardware_button.connect(
            "clicked",
            self.show_hardware_info
        )

        apps_button.connect(
            "clicked",
            self.show_applications
        )

        settings_button.connect(
            "clicked",
            self.show_settings
        )

        # Start on Home
        self.show_home(None)

    def clear_content(self):
        while child := self.content_box.get_first_child():
            self.content_box.remove(child)

    def show_home(self, button):
        self.clear_content()

        title = Gtk.Label()

        title.set_markup(
            "<span size='26000' weight='bold'>"
            "Welcome to ProgramixOS"
            "</span>"
        )

        subtitle = Gtk.Label(
            label="Your Programix desktop environment"
        )

        version = Gtk.Label(
            label="Programix 0.1.0-dev"
        )

        base = Gtk.Label(
            label="Ubuntu 26.04 LTS"
        )

        self.content_box.append(title)
        self.content_box.append(subtitle)
        self.content_box.append(version)
        self.content_box.append(base)

    def show_system_info(self, button):
        self.clear_content()

        title = Gtk.Label()

        title.set_markup(
            "<span size='24000' weight='bold'>"
            "💻 System Information"
            "</span>"
        )

        result = subprocess.run(
            [
                "bash",
                "-c",
                """
                source "$HOME/Programix/apps/programix-core/programix-core.sh"
                programix_info
                """
            ],
            capture_output=True,
            text=True
        )

        info = Gtk.Label(
            label=result.stdout.strip()
        )

        info.set_xalign(0)
        info.set_selectable(True)

        self.content_box.append(title)
        self.content_box.append(info)

    def show_hardware_info(self, button):
        self.clear_content()

        title = Gtk.Label()

        title.set_markup(
            "<span size='24000' weight='bold'>"
            "🔧 Hardware"
            "</span>"
        )

        result = subprocess.run(
            [
                "bash",
                "-c",
                """
                "$HOME/Programix/scripts/programix-hardware.sh"
                """
            ],
            capture_output=True,
            text=True
        )

        info = Gtk.Label(
            label=result.stdout.strip()
        )

        info.set_xalign(0)
        info.set_yalign(0)
        info.set_selectable(True)

        self.content_box.append(title)
        self.content_box.append(info)

    def show_applications(self, button):
        self.clear_content()

        title = Gtk.Label()

        title.set_markup(
            "<span size='24000' weight='bold'>"
            "🧩 Applications"
            "</span>"
        )

        subtitle = Gtk.Label(
            label="Programix system applications"
        )

        self.content_box.append(title)
        self.content_box.append(subtitle)

        app_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=15
        )

        system_app = Gtk.Button(
            label="💻\nSystem"
        )

        hardware_app = Gtk.Button(
            label="🔧\nHardware"
        )

        settings_app = Gtk.Button(
            label="⚙️\nSettings"
        )

        system_app.set_size_request(150, 100)
        hardware_app.set_size_request(150, 100)
        settings_app.set_size_request(150, 100)

        system_app.connect(
            "clicked",
            self.show_system_info
        )

        hardware_app.connect(
            "clicked",
            self.show_hardware_info
        )

        settings_app.connect(
            "clicked",
            self.show_settings
        )

        app_box.append(system_app)
        app_box.append(hardware_app)
        app_box.append(settings_app)

        self.content_box.append(app_box)

    def show_settings(self, button):
        subprocess.Popen(
            [
                "python3",
                os.path.expanduser(
                    "~/Programix/apps/programix-settings/"
                    "programix-settings.py"
                )
            ]
        )


class ProgramixApp(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="org.programix.desktop"
        )

    def do_activate(self):
        apply_programix_theme()

        window = ProgramixWindow(self)
        window.present()


app = ProgramixApp()
app.run()