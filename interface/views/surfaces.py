import customtkinter as ctk

from interface.base_view import BaseView


class SurfacesView(BaseView):
    def __init__(self, window):
        super().__init__(window)

    def __repr__(self):
        return "SurfacesView"

    def open_view(self):
        self.toggle_active_button("Surfaces")
        self.grid_propagate(False)
