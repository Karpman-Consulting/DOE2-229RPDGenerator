import customtkinter as ctk

from interface.base_view import BaseView


class ResultsView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "ResultsView"

    def open_view(self):
        self.toggle_active_button("Results")
        self.grid_propagate(False)
