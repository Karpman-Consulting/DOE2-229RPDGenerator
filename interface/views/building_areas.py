import customtkinter as ctk

from interface.base_view import BaseView


class BuildingAreasView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "BuildingAreasView"

    def open_view(self):
        self.toggle_active_button("Building Areas")
        self.grid_propagate(False)
