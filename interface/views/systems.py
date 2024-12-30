import customtkinter as ctk

from interface.base_view import BaseView


class SystemsView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "SystemsView"

    def open_view(self):
        self.toggle_active_button("Systems")

        # Create a button to test accessing rmd data
        test_button = ctk.CTkButton(
            self,
            text="Test Access RMD Systems",
            width=300,
            corner_radius=12,
            command=lambda: self.main.raise_error_window(
                f"RMD Zones: {self.main.app_data.rmds[0].system_names}"
            ),
        )
        test_button.grid(row=0, column=0, columnspan=9, pady=5)
