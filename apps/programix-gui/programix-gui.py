#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib


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


def get_battery_info():
    try:
        result = subprocess.run(
            ["upower", "-e"],
            capture_output=True,
            text=True,
            check=True
        )

        batteries = [
            line.strip()
            for line in result.stdout.splitlines()
            if "/battery_" in line
        ]

        total_energy = 0.0
        total_full = 0.0
        charging = False

        for battery in batteries:
            info = subprocess.run(
                ["upower", "-i", battery],
                capture_output=True,
                text=True
            )

            for line in info.stdout.splitlines():
                line = line.strip()

                if line.startswith("energy:"):
                    try:
                        value = (
                            line.split(":", 1)[1]
                            .replace("Wh", "")
                            .replace(",", ".")
                            .strip()
                        )

                        total_energy += float(value)

                    except ValueError:
                        pass

                elif line.startswith("energy-full:"):
                    try:
                        value = (
                            line.split(":", 1)[1]
                            .replace("Wh", "")
                            .replace(",", ".")
                            .strip()
                        )

                        total_full += float(value)

                    except ValueError:
                        pass

                elif line.startswith("state:"):
                    state = line.split(":", 1)[1].strip()

                    if state in (
                        "charging",
                        "pending-charge"
                    ):
                        charging = True

        if total_full <= 0:
            return (
                "🔋 --",
                "Battery information unavailable"
            )

        percentage = round(
            (total_energy / total_full) * 100
        )

        percentage = max(
            0,
            min(100, percentage)
        )

        if charging:
            icon = "🔌"
            status = "Charging"
        elif percentage <= 10:
            icon = "🪫"
            status = "Critical battery"
        elif percentage <= 30:
            icon = "🔋"
            status = "Low battery"
        else:
            icon = "🔋"
            status = "Battery"

        return (
            f"{icon} {percentage}%",
            status
        )

    except Exception:
        return (
            "🔋 --",
            "Battery information unavailable"
        )


class ProgramixWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(
            application=app
        )

        self.set_title("ProgramixOS")
        self.set_default_size(1000, 650)

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        root_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )

        # =====================================================
        # TOP PANEL
        # =====================================================

        panel = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )

        panel.set_margin_top(8)
        panel.set_margin_bottom(8)
        panel.set_margin_start(15)
        panel.set_margin_end(15)

        logo = Gtk.Label()

        logo.set_markup(
            "<span size='16000' weight='bold'>"
            "🐧 Programix"
            "</span>"
        )

        logo.set_xalign(0)

        panel.append(logo)

        panel_spacer = Gtk.Box()
        panel_spacer.set_hexpand(True)

        panel.append(panel_spacer)

        # Clock

        self.clock_label = Gtk.Label()

        panel.append(
            self.clock_label
        )

        # Notifications

        notifications_button = Gtk.Button(
            label="🔔"
        )

        notifications_button.set_tooltip_text(
            "Notifications"
        )

        panel.append(
            notifications_button
        )

        # Network

        network_button = Gtk.Button(
            label="📶"
        )

        network_button.set_tooltip_text(
            "Network"
        )

        panel.append(
            network_button
        )

        # Audio

        audio_button = Gtk.Button(
            label="🔊"
        )

        audio_button.set_tooltip_text(
            "Audio"
        )

        panel.append(
            audio_button
        )

        # Battery

        self.battery_button = Gtk.Button(
            label="🔋 --"
        )

        self.battery_button.set_tooltip_text(
            "Battery"
        )

        panel.append(
            self.battery_button
        )

        root_box.append(
            panel
        )

        # =====================================================
        # DESKTOP
        # =====================================================

        desktop_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=0
        )

        desktop_box.set_vexpand(True)

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        sidebar.set_margin_top(20)
        sidebar.set_margin_bottom(20)
        sidebar.set_margin_start(15)
        sidebar.set_margin_end(15)

        sidebar.set_size_request(
            190,
            -1
        )

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

        sidebar_spacer = Gtk.Box()
        sidebar_spacer.set_vexpand(True)

        sidebar.append(
            sidebar_spacer
        )

        sidebar.append(
            settings_button
        )

        desktop_box.append(
            sidebar
        )

        # =====================================================
        # CONTENT
        # =====================================================

        self.content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15
        )

        self.content_box.set_margin_top(30)
        self.content_box.set_margin_bottom(30)
        self.content_box.set_margin_start(30)
        self.content_box.set_margin_end(30)

        self.content_box.set_hexpand(True)
        self.content_box.set_vexpand(True)

        desktop_box.append(
            self.content_box
        )

        root_box.append(
            desktop_box
        )

        self.set_child(
            root_box
        )

        # =====================================================
        # BUTTON ACTIONS
        # =====================================================

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

        # =====================================================
        # INITIAL CONTENT
        # =====================================================

        self.show_home(None)

        # Clock update

        self.update_clock()

        GLib.timeout_add(
            1000,
            self.update_clock
        )

        # Battery update

        self.update_battery()

        GLib.timeout_add(
            30000,
            self.update_battery
        )

    # =========================================================
    # CLOCK
    # =========================================================

    def update_clock(self):

        now = datetime.now()

        self.clock_label.set_label(
            now.strftime("%H:%M")
        )

        return True

    # =========================================================
    # BATTERY
    # =========================================================

    def update_battery(self):

        battery_text, battery_status = get_battery_info()

        self.battery_button.set_label(
            battery_text
        )

        self.battery_button.set_tooltip_text(
            battery_status
        )

        return True

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_content(self):

        while child := self.content_box.get_first_child():
            self.content_box.remove(child)

    # =========================================================
    # HOME
    # =========================================================

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

    # =========================================================
    # SYSTEM INFORMATION
    # =========================================================

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

    # =========================================================
    # HARDWARE
    # =========================================================

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

    # =========================================================
    # APPLICATIONS
    # =========================================================

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

        system_app.set_size_request(
            150,
            100
        )

        hardware_app.set_size_request(
            150,
            100
        )

        settings_app.set_size_request(
            150,
            100
        )

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

        self.content_box.append(
            app_box
        )

    # =========================================================
    # SETTINGS
    # =========================================================

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

        window = ProgramixWindow(
            self
        )

        window.present()


app = ProgramixApp()

app.run()