from gi.repository import Gtk, Gio, Gdk
from galileo_utils import start_galileo

class MainWindow(Gtk.Window):
    BLUE_COLOR = Gdk.RGBA(.1, .1, .222, 1)
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
        self._set_background_color(self.label, self.BLUE_COLOR)
        vbox.pack_start(self.label, True, True, 0)

        hbox = Gtk.HBox()
        self.btn = Gtk.Button(label="Connect")
        hbox.pack_end(self.btn, False, False, 10)
        vbox.pack_start(hbox, False, False, 10)
        self.btn.set_size_request(40, 30)

        # events and actions
        self.btn.connect("clicked", self.on_btn_clicked)
        self.connect("delete-event", Gtk.main_quit)

        # launch main galileo function
        self._disable_actions()
        # self.galileo = start_galileo(self.on_error, self.on_info)

    def on_btn_clicked(self, btn):
        self._disable_actions()
        self.galileo.main()

    def on_error(self, text):
        self.label.set_text(text)
        self._enable_actions()

    def on_info(self, text):
        self.label.set_text(text)
        self._enable_actions()



    def _disable_actions(self):
        self.btn.set_sensitive(False)

    def _enable_actions(self):
        self.btn.set_sensitive(True)

    def _set_background_color(self, widget, color):
        widget.override_background_color(Gtk.StateFlags.NORMAL, color)


if __name__ == "__main__" :
    win = MainWindow()
    win.show_all()
    Gtk.main()
