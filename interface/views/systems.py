import customtkinter as ctk

from interface.base_view import BaseView


class SystemsView(BaseView):
    def __init__(self, app):
        super().__init__(app)

    def open_view(self):
        self.clear_window()
        self.toggle_active_button("Systems")
