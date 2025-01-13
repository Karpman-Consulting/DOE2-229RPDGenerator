import customtkinter as ctk

from rpd_generator.utilities import validate_configuration
from interface.base_view import BaseView


class InstallConfigView(BaseView):
    def __init__(self, main):
        super().__init__(main)

    def __repr__(self):
        return "InstallConfigView"

    def open_view(self):
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
        directions.grid(row=1, column=1, columnspan=8, sticky="ew", padx=5, pady=20)

        # Create the labels for the path entry fields
        install_path_label = ctk.CTkLabel(
            self,
            text="Installation Path: ",
            anchor="e",
            justify="right",
            font=("Arial", 16, "bold"),
        )
        install_path_label.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Create the path entry field
        install_path_entry = ctk.CTkEntry(
            self,
            width=50,
            corner_radius=5,
            textvariable=self.main.app_data.installation_path,
        )
        install_path_entry.grid(
            row=2, column=1, columnspan=7, sticky="ew", padx=5, pady=5
        )

        # Create the button to manually browse for the eQUEST installation
        install_browse_button = ctk.CTkButton(
            self, text="Browse", width=100, corner_radius=12
        )
        install_browse_button.grid(row=2, column=8, padx=5, pady=5)

        # Create the labels for the path entry fields
        userlib_path_label = ctk.CTkLabel(
            self,
            text="(Optional)      \nUser Library: ",
            anchor="e",
            justify="right",
            font=("Arial", 16, "bold"),
        )
        userlib_path_label.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        # Create the path entry field
        user_lib_path_entry = ctk.CTkEntry(
            self,
            width=50,
            corner_radius=5,
            textvariable=self.main.app_data.user_lib_path,
        )
        user_lib_path_entry.grid(
            row=3, column=1, columnspan=7, sticky="ew", padx=5, pady=(20, 5)
        )

        # Create the button to manually browse for the eQUEST installation
        user_lib_browse_button = ctk.CTkButton(
            self, text="Browse", width=100, corner_radius=12
        )
        user_lib_browse_button.grid(row=3, column=8, padx=5, pady=(20, 5))

        # Create a frame to hold the Test button
        lower_button_frame = ctk.CTkFrame(self, fg_color=self.main.bg_color)
        lower_button_frame.grid(
            row=4, column=1, columnspan=7, sticky="ew", padx=5, pady=(30, 5)
        )
        lower_button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create the button to test the eQUEST installation files
        test_button = ctk.CTkButton(
            lower_button_frame,
            text="Test",
            width=100,
            corner_radius=12,
            command=self.verify_installation_files,
        )
        test_button.grid(row=0, column=1, padx=(350, 5), pady=5)

        # Create the button to continue to the Project Info page
        self.continue_button = ctk.CTkButton(
            lower_button_frame,
            text="Continue",
            width=100,
            corner_radius=12,
            state="disabled",
            command=self.continue_past_configuration,
        )
        self.continue_button.grid(row=0, column=2, padx=(5, 350), pady=5)

    def verify_installation_files(self):
        error = validate_configuration.verify_equest_installation()
        if error == "":
            self.main.app_data.files_verified = True
            self.main.toggle_continue_button()
        else:
            self.main.raise_error_window(error)

    def continue_past_configuration(self):
        self.main.navbar_buttons["Project Info"].configure(state="normal")
        self.main.show_view("Project Info")

    def toggle_continue_button(self):
        if self.main.app_data.files_verified:
            self.continue_button.configure(state="normal")
        else:
            self.continue_button.configure(state="disabled")
