import customtkinter as ctk


class BaseView(ctk.CTkFrame):
    def __init__(self, main):
        super().__init__(main)
        self.main = main

        self.grid_propagate(False)
        self.configure(height=600)

    def toggle_active_button(self, active_button_name):
        for name, button in self.main.navbar_buttons.items():
            if name == active_button_name:
                self.main.navbar_buttons[name].configure(
                    fg_color="#269ac3",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )
            else:
                self.main.navbar_buttons[name].configure(
                    fg_color="#3B8ED0",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )

    def update_warnings_errors(self):
        if len(self.main.app_data.warnings) > 0:
            self.main.warnings_button.configure(
                text=f"Warnings ({len(self.main.app_data.warnings)})",
                font=("Arial", 12, "bold"),
                state="normal",
                fg_color="orange",
            )
        else:
            self.main.warnings_button.configure(
                text=f"Warnings",
                font=("Arial", 12),
                state="disabled",
                fg_color="gray",
            )
        if len(self.main.app_data.errors) > 0:
            self.main.errors_button.configure(
                text=f"Errors ({len(self.main.app_data.errors)})",
                font=("Arial", 12, "bold"),
                state="normal",
                fg_color="red",
            )
        else:
            self.main.errors_button.configure(
                text=f"Errors",
                font=("Arial", 12),
                state="disabled",
                fg_color="gray",
            )
