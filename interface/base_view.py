import customtkinter as ctk


class BaseView(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.app_data = self.window.main_app.data
        self.configure(height=600)

    def toggle_active_button(self, active_button_name):
        for name, button in self.window.navbar_buttons.items():
            if name == active_button_name:
                self.window.navbar_buttons[name].configure(
                    fg_color="#3CB6DC",
                    hover_color="#3CB6DC",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )
            else:
                self.window.navbar_buttons[name].configure(
                    fg_color="#3B8ED0",
                    hover_color="#325882",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )

    def update_warnings_errors(self):
        if len(self.app_data.warnings) > 0:
            self.window.warnings_button.configure(
                text=f"Warnings ({len(self.app_data.warnings)})",
                font=("Arial", 12, "bold"),
                state="normal",
                fg_color="orange",
            )
        else:
            self.window.warnings_button.configure(
                text=f"Warnings",
                font=("Arial", 12),
                state="disabled",
                fg_color="gray",
            )
        if len(self.app_data.errors) > 0:
            self.window.errors_button.configure(
                text=f"Errors ({len(self.app_data.errors)})",
                font=("Arial", 12, "bold"),
                state="normal",
                fg_color="red",
            )
        else:
            self.window.errors_button.configure(
                text=f"Errors",
                font=("Arial", 12),
                state="disabled",
                fg_color="gray",
            )
