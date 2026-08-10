#!/usr/bin/env python3

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
        title.set_markup("<span size='24000' weight='bold'>🐧 ProgramixOS</span>")

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
        hardware_button = Gtk.Button(label="Hardware")
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