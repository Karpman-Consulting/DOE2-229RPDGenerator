import customtkinter as ctk

from interface.base_view import BaseView


class SurfacesView(BaseView):
    def __init__(self, app):
        super().__init__(app)

    def open_view(self):
        self.clear_window()
        self.toggle_active_button("Surfaces")
