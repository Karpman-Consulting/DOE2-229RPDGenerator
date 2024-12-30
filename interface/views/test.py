import customtkinter as ctk
from tkinter import filedialog

from interface.base_view import BaseView


class TestView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "TestView"

    def open_view(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(
            self,
            textvariable=self.main.app_data.test_inp_path,
            state="disabled",
            width=400,
        )
        entry.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=20, sticky="ew")

        select_button = ctk.CTkButton(
            self, text="Select File", command=self.select_test_file
        )
        select_button.grid(row=0, column=1, padx=(5, 10), pady=20, sticky="e")

        create_rpd_button = ctk.CTkButton(
            self,
            text="Create JSON",
            command=self.main.app_data.call_write_rpd_json_from_inp,
        )
        create_rpd_button.grid(row=1, column=1, padx=10, pady=(20, 10), sticky="ew")

    def select_test_file(self):
        # Open file dialog to select a file with .inp extension
        filepath = filedialog.askopenfilename(filetypes=[("INP files", "*.inp")])
        if filepath:
            # Display the selected file path in the text entry box
            self.main.app_data.test_inp_path.set(filepath)
