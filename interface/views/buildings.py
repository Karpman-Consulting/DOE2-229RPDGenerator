import customtkinter as ctk

from interface.base_view import BaseView


class BuildingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)

    def __repr__(self):
        return "BuildingsView"

    def open_view(self):
        self.toggle_active_button("Buildings")
