import customtkinter as ctk


class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master=None, error_message="An error occurred."):
        super().__init__(master)  # Pass only the arguments expected by the superclass

        self.title("ALERT")
        self.geometry("400x400")
        self.resizable(False, False)

        # Create a label for the error message heading
        error_label = ctk.CTkLabel(
            self, text="Message(s):", anchor="w", font=("Helvetica", 20, "bold")
        )
        error_label.pack(fill="x", padx=10, pady=(10, 0))

        text_area_frame = ctk.CTkFrame(self)
        text_area_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create a text area for displaying the error message
        text_area = ctk.CTkTextbox(text_area_frame, wrap="word")
        text_area.pack(side="left", fill="both", expand=True)

        # Insert the passed error message into the text area
        text_area.insert("1.0", error_message)
        text_area.configure(state="disabled")  # Make text area read-only
