import customtkinter as ctk
from tkinter import ttk, filedialog

import rpd_generator.utilities.validate_configuration as validate_configuration
from interface.disclaimer_window import DisclaimerWindow
from interface.error_window import ErrorWindow


class InstallConfigWindow(ctk.CTkToplevel):
    def __init__(self, main_app, configuration_data):
        super().__init__()
        self.title("eQUEST Installation Configuration")
        self.license_window = None
        self.disclaimer_window = None
        self.error_window = None

        self.main_app = main_app
        self.configuration_data = configuration_data

        self.installation_path = ctk.StringVar()
        self.user_lib_path = ctk.StringVar()
        self.files_verified = False
        self.bg_color = self.cget("fg_color")[0]

        directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )
        directions_label.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
        instruction_text = (
            "1) Use the buttons below to select and validate the path to your eQUEST 3-65-7175 installation directory. \n"
            "       a. If the path populated automatically, your installation path was located by the application. \n"
            "       b. If the path did not populate automatically, you can manually enter the path or use the 'Browse' button "
            "to find the folder that contains your eQUEST installation files\n"
            "2) Optionally, provide the path to your custom User Library file. This is only needed if your model uses "
            "references to custom library entries.\n"
            "3) Click the 'Test' button to validate the eQUEST files required by this application. Upon a successful "
            "test, you will be able to continue to the next page."
        )
        directions = ctk.CTkLabel(
            self, text=instruction_text, anchor="w", justify="left", font=("Arial", 14)
        )
        directions.grid(
            row=1, column=1, columnspan=8, sticky="ew", padx=(5, 20), pady=(20, 5)
        )

        # Directions separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=9, sticky="ew", padx=20, pady=15)

        # Create the labels for the path entry fields
        install_path_label = ctk.CTkLabel(
            self,
            text="Installation Path: ",
            anchor="e",
            justify="right",
            font=("Arial", 16, "bold"),
        )
        install_path_label.grid(row=3, column=0, sticky="nsew", padx=(20, 5), pady=5)

        # Create the path entry field
        install_path_entry = ctk.CTkEntry(
            self,
            width=50,
            corner_radius=5,
            textvariable=self.installation_path,
        )
        install_path_entry.grid(
            row=3, column=1, columnspan=7, sticky="ew", padx=5, pady=5
        )

        # Create the button to manually browse for the eQUEST installation
        install_browse_button = ctk.CTkButton(
            self,
            text="Browse",
            width=100,
            corner_radius=12,
            command=self.select_install_directory,
        )
        install_browse_button.grid(row=3, column=8, padx=5, pady=5)

        # Create the labels for the path entry fields
        user_lib_path_label = ctk.CTkLabel(
            self,
            text="(Optional)      \nUser Library: ",
            anchor="e",
            justify="right",
            font=("Arial", 16, "bold"),
        )
        user_lib_path_label.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        # Create the path entry field
        user_lib_path_entry = ctk.CTkEntry(
            self,
            width=50,
            corner_radius=5,
            textvariable=self.user_lib_path,
        )
        user_lib_path_entry.grid(
            row=4, column=1, columnspan=7, sticky="ew", padx=5, pady=(20, 5)
        )

        # Create the button to manually browse for the eQUEST installation
        user_lib_browse_button = ctk.CTkButton(
            self,
            text="Browse",
            width=100,
            corner_radius=12,
            command=self.select_user_lib_directory,
        )
        user_lib_browse_button.grid(row=4, column=8, padx=5, pady=(20, 5))

        # Create the button to continue to the Project Info page
        self.continue_button = ctk.CTkButton(
            self,
            text="Continue",
            width=100,
            corner_radius=12,
            command=self.continue_past_configuration,
        )
        self.continue_button.grid(row=5, column=0, columnspan=9, pady=15)

    def __repr__(self):
        return "InstallConfigWindow"

    def continue_past_configuration(self):
        error = validate_configuration.verify_equest_installation(
            self.installation_path.get()
        )
        if error == "":
            self.files_verified = True
            self.save_configuration_data()
            self.main_app.install_config_complete()
        else:
            self.raise_error_window(error)

    def toggle_continue_button(self):
        if self.files_verified:
            self.continue_button.configure(state="normal")
        else:
            self.continue_button.configure(state="disabled")

    def raise_disclaimer_window(self):
        if self.disclaimer_window is None or not self.disclaimer_window.winfo_exists():
            self.disclaimer_window = DisclaimerWindow(self)
            self.disclaimer_window.after(100, self.disclaimer_window.lift)
        else:
            self.disclaimer_window.focus()  # if window exists, focus it

    def raise_error_window(self, error_text):
        self.error_window = ErrorWindow(self, error_text)
        self.error_window.after(100, self.error_window.lift)

    def save_configuration_data(self):
        if self.installation_path.get():
            self.configuration_data["installation_path"] = self.installation_path.get()
        if self.user_lib_path.get():
            self.configuration_data["user_lib_path"] = self.user_lib_path.get()

    def select_install_directory(self):
        directory_path = filedialog.askdirectory(mustexist=True)
        if directory_path:
            self.installation_path.set(directory_path)

    def select_user_lib_directory(self):
        directory_path = filedialog.askdirectory(mustexist=True)
        if directory_path:
            self.user_lib_path.set(directory_path)
