#!/usr/bin/env python3

import subprocess
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class ProgramixWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("ProgramixOS")
        self.set_default_size(800, 500)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12
        )

        main_box.set_margin_top(30)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)

        title = Gtk.Label()
        title.set_markup(
            "<span size='24000' weight='bold'>🐧 ProgramixOS</span>"
        )

        version = Gtk.Label(label="Programix 0.1.0-dev")
        base = Gtk.Label(label="Ubuntu 26.04 LTS")

        welcome = Gtk.Label(
            label="Welcome to ProgramixOS"
        )

        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )

        system_button = Gtk.Button(label="System")
        system_button.connect(
            "clicked",
            self.show_system_info
        )

        hardware_button = Gtk.Button(label="Hardware")
        hardware_button.connect(
            "clicked",
            self.show_hardware_info
        )

        apps_button = Gtk.Button(label="Applications")

        button_box.append(system_button)
        button_box.append(hardware_button)
        button_box.append(apps_button)

        main_box.append(title)
        main_box.append(welcome)
        main_box.append(version)
        main_box.append(base)
        main_box.append(button_box)

        self.set_child(main_box)

    def show_system_info(self, button):
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

        dialog = Gtk.Dialog(
            transient_for=self,
            modal=True
        )

        dialog.set_title("Programix System Information")
        dialog.set_default_size(450, 250)

        content = dialog.get_content_area()

        label = Gtk.Label(
            label=result.stdout.strip()
        )

        label.set_xalign(0)
        label.set_selectable(True)

        content.append(label)

        dialog.add_button("OK", Gtk.ResponseType.OK)

        dialog.connect(
            "response",
            lambda dialog, response: dialog.destroy()
        )

        dialog.present()

    def show_hardware_info(self, button):
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

        dialog = Gtk.Dialog(
            transient_for=self,
            modal=True
        )

        dialog.set_title("Programix Hardware")
        dialog.set_default_size(700, 600)

        content = dialog.get_content_area()

        label = Gtk.Label(
            label=result.stdout.strip()
        )

        label.set_xalign(0)
        label.set_yalign(0)
        label.set_selectable(True)

        content.append(label)

        dialog.add_button("OK", Gtk.ResponseType.OK)

        dialog.connect(
            "response",
            lambda dialog, response: dialog.destroy()
        )

        dialog.present()


class ProgramixApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.programix.desktop"
        )

    def do_activate(self):
        window = ProgramixWindow(self)
        window.present()


app = ProgramixApp()
app.run()