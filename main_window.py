#!/usr/bin/env python

from gi.repository import Gtk, Gio, Gdk, GLib
from galileo_utils import GalileoLogHandler, galileo_start
from threading import Thread

class MainWindow(Gtk.Window):
    BLUE_COLOR = Gdk.RGBA(.8, .8, .9, 1)
    RED_COLOR = Gdk.RGBA(.9, .7, .7, 1)
    WHITE_COLOR = Gdk.RGBA(1, 1, 1, 1)

    def __init__(self):
        Gtk.Window.__init__(self, title="Fitbit connect")
        self.set_default_size(400, 300)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Fitbit connect"
        self.set_titlebar(hb)

        vbox = Gtk.VBox(spacing=0)
        self.add(vbox)

        self.label = Gtk.Label()
        self._set_background_color(self.label, self.WHITE_COLOR)
        vbox.pack_start(self.label, True, True, 0)

        hbox = Gtk.HBox()
        self.spinner = Gtk.Spinner()
        self.spinner.set_visible(False)
        hbox.pack_start(self.spinner, False, False, 10)
        self.btn = Gtk.Button(label="Connect")
        hbox.pack_end(self.btn, False, False, 10)
        vbox.pack_start(hbox, False, False, 10)
        self.btn.set_size_request(40, 30)

        # events and actions
        self.btn.connect("clicked", self.on_btn_clicked)
        self.connect("delete-event", Gtk.main_quit)

        # galileo log handler
        self.galileo_log = GalileoLogHandler()

    def call_galileo(self):
        #self.work_th = Thread(target=self.sync_galileo)
        self.running = True
        self.spinner.set_visible(True)
        self.spinner.start()

        #self.work_th.start()
        self.sync_galileo()

    def sync_galileo(self):
        galileo_start(self.galileo_log)
        # GLib.idle_add(self.on_sync_finished)
        self.on_sync_finished()

    def on_sync_finished(self):
        self.running = False
        self.spinner.stop()
        self.spinner.set_visible(False)
        self._enable_actions()

        if self.galileo_log.has_error() is True :
            self.on_error(self.galileo_log.error_message)
        elif self.galileo_log.has_info():
            self.on_info(self.galileo_log.info_message)
        self.galileo_log.clean()

    def on_btn_clicked(self, btn):
        self._disable_actions()
        try :
            self.call_galileo()
        except Exception as e:
            self.on_error(str(e))

    def on_error(self, text):
        self._set_background_color(self.label, self.RED_COLOR)
        self.label.set_text(text)
        self._enable_actions()

    def on_info(self, text):
        self._set_background_color(self.label, self.BLUE_COLOR)
        self.label.set_text(text)
        self._enable_actions()

    def _disable_actions(self):
        self.btn.set_sensitive(False)

    def _enable_actions(self):
        self.btn.set_sensitive(True)

    def _set_background_color(self, widget, color):
        widget.override_background_color(Gtk.StateFlags.NORMAL, color)


galileo_log = GalileoLogHandler()

if __name__ == "__main__" or True:
    win = MainWindow()
    win.show_all()

    GLib.threads_init()
    Gdk.threads_init()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()

