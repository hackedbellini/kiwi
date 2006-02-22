#!/usr/bin/env python
from kiwi.ui.delegates import ProxyDelegate
from kiwi.ui.objectlist import Column, ObjectList

class DiaryEntry:
    title = ''
    text = ''
    period = 'morning'

    def get_words(self):
        return len(self.text.split())

    def get_chars(self):
        return len(self.text)

class Diary(ProxyDelegate):
    def __init__(self):
        self.entries = ObjectList([Column("title", width=120, sorted=True),
                                   Column("period", width=80),
                                   Column("text", expand=True, visible=False)])
        ProxyDelegate.__init__(self, DiaryEntry(), gladefile="diary2",
                               delete_handler=self.quit_if_last)
        self.hbox.pack_start(self.entries)
        self.entries.show()
        self.entries.grab_focus()
        self.set_editable(False)

    def proxy_updated(self, *args):
        self.entries.update(self.model)

    def on_add__clicked(self, button):
        entry = DiaryEntry()
        entry.title = 'New title'

        self.set_model(entry)
        self.entries.append(entry)
        self.title.grab_focus()
        self.set_editable(True)

    def on_remove__clicked(self, button):
        entry = self.entries.get_selected()
        if entry:
            self.entries.remove(entry)

        if len(self.entries) < 1:
            editable = False
        else:
            editable = True
        self.set_editable(editable)

    def on_text__content_changed(self, *args):
        self.update("chars")
        self.update("words")
        self.entries.update(self.model)

    def on_entries__selection_changed(self, entries, instance):
        if instance:
            self.set_model(instance)

    def set_editable(self, editable):
        self.leftbox.set_sensitive(editable)
        self.remove.set_sensitive(editable)

proxy = Diary()
proxy.show_and_loop()