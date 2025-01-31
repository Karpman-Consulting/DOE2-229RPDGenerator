import customtkinter as ctk

from interface.base_view import BaseView


class ZonesView(BaseView):
    def __init__(self, window):
        super().__init__(window)

    def __repr__(self):
        return "ZonesView"

    def open_view(self):
        self.toggle_active_button("Zones")

        # Create a button to test accessing rmd data
        test_button = ctk.CTkButton(
            self,
            text="Test Access RMD Zones",
            width=300,
            corner_radius=12,
            command=lambda: self.window.raise_error_window(
                f"RMD Zones: {self.window.main_app.data.rmds[0].zone_names}"
            ),
        )
        test_button.grid(row=0, column=0, columnspan=9, pady=5)
