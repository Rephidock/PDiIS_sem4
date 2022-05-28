from __future__ import annotations
from typing import TYPE_CHECKING

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang.builder import Builder
from kivy.clock import Clock

if TYPE_CHECKING:
    from middleman.event_handler import EventHandler


class RecordEditorApp(MDApp):

    event_handler: EventHandler
    dialog: MDDialog | None

    def __init__(self, event_handler: EventHandler, **kwargs):
        self.event_handler = event_handler
        self.event_handler.set_app(self)

        self.dialog = None
        
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.root = Builder.load_file("./ui/root.kv")
        Clock.schedule_once(lambda *_: self.event_handler.on_create())

    def show_dialog(self, title: str = "", text: str = ""):
        if not self.dialog:
            self.dialog = MDDialog()

        self.dialog.title = title
        self.dialog.text = text

        self.dialog.open()
