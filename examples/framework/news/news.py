#!/usr/bin/env python
from gi.repository import Gtk

from kiwi.ui.views import BaseView, SlaveView
from kiwi.ui.gadgets import quit_if_last

news = [
    ("Smallpox Vaccinations for EVERYONE",
        "JRoyale",
        "http://www.pigdog.org/auto/Power_Corrupts/link/2700.html"),
    ("Is that uranium in your pocket or are you just happy to see me?",
        "Baron Earl",
        "http://www.pigdog.org/auto/bad_people/link/2699.html"),
    ("Cut 'n Paste",
        "Baron Earl",
        "http://www.pigdog.org/auto/ArtFux/link/2690.html"),
    ("A Slippery Exit",
        "Reverend CyberSatan",
        "http://www.pigdog.org/auto/TheCorporateFuck/link/2683.html"),
    ("Those Crazy Dutch Have Resurrected Elvis",
        "Miss Conduct",
        "http://www.pigdog.org/auto/viva_la_musica/link/2678.html")
]


class News(SlaveView):
    def __init__(self):
        model = Gtk.ListStore(str, str)
        treeview = Gtk.TreeView(model)
        renderer = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn('News', renderer, text=0)
        col2 = Gtk.TreeViewColumn('Author', renderer, text=1)
        treeview.append_column(col1)
        treeview.append_column(col2)
        treeview.get_selection().set_mode(Gtk.SelectionMode.BROWSE)
        for item in news:
            model.append(item[:-1])
        SlaveView.__init__(self, treeview)

news = News()

shell = BaseView(gladefile="news_shell.ui",
                 delete_handler=quit_if_last)
shell.attach_slave("placeholder", news)

news.show_all()
news.focus_toplevel()  # explained next section, don't worry
shell.show()
Gtk.main()
