import customtkinter as ctk

from interface.base_view import BaseView


class MiscellaneousView(BaseView):
    def __init__(self, window):
        super().__init__(window)

    def __repr__(self):
        return "MiscellaneousView"

    def open_view(self):
        self.toggle_active_button("Misc.")
        self.grid_propagate(False)
