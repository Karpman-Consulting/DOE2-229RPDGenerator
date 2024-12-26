import customtkinter as ctk

from interface.base_view import BaseView


class ExteriorLightingView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "ExteriorLightingView"

    def open_view(self):
        self.toggle_active_button("Ext. Lighting")
