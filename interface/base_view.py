import customtkinter as ctk


class BaseView(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

    def clear_window(self):
        # Clear the window of all widgets after the first row which contains the button bar
        for widget in self.winfo_children():
            if "row" in widget.grid_info() and int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()
                widget.destroy()

    def toggle_active_button(self, active_button_name):
        for name, button in self.app.navbar_buttons.items():
            if name == active_button_name:
                self.app.navbar_buttons[name].configure(
                    fg_color="#269ac3",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )
            else:
                self.app.navbar_buttons[name].configure(
                    fg_color="#3B8ED0",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )

    def update_warnings_errors(self):
        if len(self.app.app_data.warnings) > 0:
            self.app.warnings_button.configure(
                text=f"Warnings ({len(self.app.app_data.warnings)})",
                font=("Arial", 12, "bold"),
                state="normal",
            )
        else:
            self.app.warnings_button.configure(
                text=f"Warnings",
                font=("Arial", 12),
                state="disabled",
            )
        if len(self.app.app_data.errors) > 0:
            self.app.errors_button.configure(
                text=f"Errors ({len(self.app.app_data.errors)})",
                font=("Arial", 12, "bold"),
                state="normal",
            )
        else:
            self.app.errors_button.configure(
                text=f"Errors",
                font=("Arial", 12),
                state="disabled",
            )
