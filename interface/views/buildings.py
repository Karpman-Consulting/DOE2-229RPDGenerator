import customtkinter as ctk

from interface.base_view import BaseView


class BuildingsView(BaseView):
    def __init__(self, app):
        super().__init__(app)

    def open_view(self):
        self.clear_window()
        self.toggle_active_button("Buildings")

        # Create the button to test accessing rmd data
        test_button = ctk.CTkButton(
            self,
            text="Test Access RMD Zones",
            width=300,
            corner_radius=12,
            command=lambda: self.app.raise_error_window(
                f"RMD Zones: {self.app.app_data.rmds[0].zone_names}"
            ),
        )
        test_button.grid(row=5, column=0, columnspan=9, pady=5)
