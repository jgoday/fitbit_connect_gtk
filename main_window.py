from gi.repository import Gtk, Gio
from galileo_utils import start_galileo

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Fitbit connect")
        self.set_default_size(400, 200)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Fitbit connect"
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        self.label = Gtk.Label()
        box.pack_start(self.label, True, True, 10)

        self.btn = Gtk.Button(label="Connect")
        box.pack_start(self.btn, True, True, 10)

        self.btn.connect("clicked", self.on_btn_clicked)
        self.connect("delete-event", Gtk.main_quit)

        self.btn.set_sensitive(False)
        self.galileo = start_galileo(self.on_error)

    def on_btn_clicked(self, btn):
        self.btn.set_sensitive(False)
        self.galileo.main()


    def on_error(self, text):
        self.label.set_text(text)
        self.btn.set_sensitive(True)

if __name__ == "__main__" :
    win = MainWindow()
    win.show_all()
    Gtk.main()
