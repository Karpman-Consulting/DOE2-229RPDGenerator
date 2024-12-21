import customtkinter as ctk
from PIL import Image
from tkinter import Menu, filedialog
from itertools import islice

from rpd_generator import main as rpd_generator
from rpd_generator.utilities import validate_configuration
from rpd_generator.config import Config
from interface.disclaimer_window import DisclaimerWindow
from interface.error_window import ErrorWindow
from interface.ctk_xyframe import CTkXYFrame
from interface.main_app_data import MainAppData


ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class MainApplicationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.app_data = MainAppData()

        self.title("eQUEST 229 RPD Generator")
        self.geometry(f"{1300}x{700}")
        self.minsize(1300, 350)

        self.menubar = Menu(self)
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New", command="donothing")
        file_menu.add_command(label="Open", command="donothing")
        file_menu.add_command(label="Save", command="donothing")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Instructions", command="donothing")
        help_menu.add_command(label="Background", command="donothing")
        help_menu.add_separator()
        help_menu.add_command(label="License", command="donothing")
        help_menu.add_command(label="Disclaimer", command=self.open_disclaimer)
        self.menubar.add_cascade(label="About", menu=help_menu)

        self.config(menu=self.menubar)

        self.bg_color = self.cget("fg_color")[0]

        # Define buttons bar - Always Active
        self.navbar_buttons = {}
        self.create_button_bar()

        # Initialize Widgets/Windows that will not always be active
        self.license_window = None
        self.disclaimer_window = None
        self.continue_button = None
        self.error_window = None
        self.baseline_rotation_rows = {}

        # Attempt to automatically find the eQUEST installation path and set the data paths from the config files
        validate_configuration.find_equest_installation()

        if not Config.EQUEST_INSTALL_PATH:
            # Initialize the configuration window to select and test the eQUEST installation path
            self.open_configuration_window()
        else:
            # Uncomment to enable the test view to select an INP file and create an RPD JSON file without compliance parameters
            # self.open_select_test_file_view()
            self.navbar_buttons["Project Info"].configure(state="normal")
            self.open_project_info_page()

        self.app_data.installation_path.set(Config.EQUEST_INSTALL_PATH)

    def create_button_bar(self):
        # Define button names
        button_names = [
            "Project Info",
            "Buildings",
            "Building Segments",
            "Spaces",
            "Surfaces",
            "Systems",
            "Ext. Lighting",
            "Misc.",
            "Results",
        ]

        # Define button icons
        icon_paths = [
            "menu.png",
            "buildings.png",
            "building_segments.png",
            "spaces.png",
            "surfaces.png",
            "systems.png",
            "ext_lighting.png",
            "misc.png",
            "results.png",
        ]
        callback_methods = {
            "Project Info": self.open_project_info_page,
            "Buildings": self.open_buildings_page,
            "Building Segments": self.open_building_segments_page,
            "Spaces": self.open_spaces_page,
            "Surfaces": self.open_surfaces_page,
            "Systems": self.open_systems_page,
            "Ext. Lighting": self.open_ext_lighting_page,
            "Misc.": self.open_misc_page,
            "Results": self.open_results_page,
        }

        for index, (name, icon_path) in enumerate(zip(button_names, icon_paths)):
            # Load and recolor the icon for the button
            icon = Image.open(f"interface/static/{icon_path}").convert("RGBA")

            r, g, b, alpha = icon.split()
            white_icon = Image.merge(
                "RGBA", (alpha, alpha, alpha, alpha)
            )  # Merge all channels into alpha to keep transparency
            icon_image = ctk.CTkImage(white_icon)

            # Create a frame for each button that will act as the border
            button_frame = ctk.CTkFrame(self, width=144, height=36, corner_radius=0)
            button_frame.grid(row=0, column=index, sticky="nsew")

            # Then create the button inside this frame with the icon
            button = ctk.CTkButton(
                button_frame,
                image=icon_image,
                text=name,
                font=("Arial", 12),
                width=140,
                height=30,
                corner_radius=0,
                state="disabled",
                compound="left",
                command=callback_methods[name],
            )
            button.place(relx=0.5, rely=0.5, anchor="center")
            self.navbar_buttons[name] = button
            # Keep a reference to the image to prevent garbage collection
            button.image = icon_image

    def clear_window(self):
        # Clear the window of all widgets after the first row which contains the button bar
        for widget in self.winfo_children():
            if "row" in widget.grid_info() and int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()
                widget.destroy()

    def open_disclaimer(self):
        if self.disclaimer_window is None or not self.disclaimer_window.winfo_exists():
            self.disclaimer_window = DisclaimerWindow(self)
            self.disclaimer_window.after(100, self.disclaimer_window.lift)
        else:
            self.disclaimer_window.focus()  # if window exists, focus it

    def raise_error_window(self, error_text):
        self.error_window = ErrorWindow(self, error_text)
        self.error_window.after(100, self.error_window.lift)

    def verify_files(self):
        error = validate_configuration.verify_equest_installation()
        if error == "":
            self.app_data.files_verified = True
            self.toggle_continue_button()
        else:
            self.raise_error_window(error)

    def toggle_continue_button(self):
        if self.app_data.files_verified:
            self.continue_button.configure(state="normal")
        else:
            self.continue_button.configure(state="disabled")

    def toggle_active_button(self, active_button_name):
        for name, button in self.navbar_buttons.items():
            if name == active_button_name:
                self.navbar_buttons[name].configure(
                    fg_color="#269ac3",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )
            else:
                self.navbar_buttons[name].configure(
                    fg_color="#3B8ED0",
                    hover_color="#1F7D99",
                    text_color="white",
                    font=("Arial", 12, "bold"),
                )

    def call_write_rpd_json_from_inp(self):
        rpd_generator.write_rpd_json_from_inp(str(self.app_data.test_inp_path.get()))

    def select_test_file(self):
        # Open file dialog to select a file with .inp extension
        filepath = filedialog.askopenfilename(filetypes=[("INP files", "*.inp")])
        if filepath:
            # Display the selected file path in the text entry box
            self.app_data.test_inp_path.set(filepath)

    def continue_past_configuration(self):
        self.navbar_buttons["Project Info"].configure(state="normal")
        self.open_project_info_page()

    def validate_project_info(self):
        valid = True  # TODO: Add validation logic to check for erp, lrp, srp, nhk files for each input file
        if valid:
            self.read_project_files__continue()
        else:
            self.raise_error_window(
                "Error: Invalid project information."
            )  # TODO: Expand error message

    def toggle_project_tabs(self):
        for name, button in islice(self.navbar_buttons.items(), 1, None):
            if self.navbar_buttons[name].cget("state") == "disabled":
                self.navbar_buttons[name].configure(state="normal")
            else:
                self.navbar_buttons[name].configure(state="disabled")

    def read_project_files__continue(self):
        self.app_data.generate_rmds()
        self.toggle_project_tabs()
        self.open_buildings_page()

    def toggle_baseline_rotations(self):
        """Add or remove Baseline rotation rows based on checkbox state."""
        for row_widgets in self.baseline_rotation_rows.values():
            if row_widgets[0].winfo_ismapped():
                # If visible, hide them
                for widget in row_widgets:
                    widget.grid_remove()
            else:
                # If hidden, show them
                for widget in row_widgets:
                    widget.grid()

    def create_file_row(self, parent_frame, row_num, label_text):
        """Create a row inside the specified frame."""
        label = ctk.CTkLabel(
            parent_frame,
            text=label_text,
            font=("Arial", 14),
            width=90,
            anchor="e",  # Align text to the right within the label
        )
        label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)

        path_entry = ctk.CTkEntry(parent_frame, width=700, font=("Arial", 10))
        path_entry.grid(
            row=row_num, column=1, columnspan=7, sticky="ew", padx=5, pady=5
        )

        # File select button
        def select_file():
            file_path = filedialog.askopenfilename(
                filetypes=[("eQUEST Input Files", "*.inp")]
            )
            if file_path:
                # Extract parent directory and filename using string parsing
                parts = file_path.rsplit("/", 2)
                if len(parts) > 1:
                    parent_dir = parts[-2]
                    filename = parts[-1]
                    trimmed_path = f"{parent_dir}/{filename}"
                else:
                    trimmed_path = file_path

                # Update the entry with the trimmed path
                path_entry.delete(0, "end")
                path_entry.insert(0, trimmed_path)

                self.app_data.project_input_file_paths[label_text.split(":")[0]] = (
                    file_path
                )

        select_button = ctk.CTkButton(
            parent_frame, text="Select", command=select_file, width=80, height=30
        )
        select_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

        return label, path_entry, select_button

    def open_select_test_file_view(self):
        # Create a disabled text entry box to display the selected file path
        entry = ctk.CTkEntry(
            self, textvariable=self.app_data.test_inp_path, state="disabled", width=200
        )
        entry.grid(row=2, column=1, columnspan=6, sticky="ew", padx=5, pady=(250, 5))

        # Create a button to open the file selection dialog
        select_button = ctk.CTkButton(
            self, text="Select File", command=self.select_test_file
        )
        select_button.grid(
            row=2, column=7, columnspan=1, sticky="ew", padx=5, pady=(250, 5)
        )

        create_rpd_button = ctk.CTkButton(
            self, text="Create JSON", command=self.call_write_rpd_json_from_inp
        )
        create_rpd_button.grid(row=3, column=4, sticky="ew", padx=5, pady=(150, 5))

    def open_configuration_window(self):
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
            textvariable=self.app_data.installation_path,
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
            self, width=50, corner_radius=5, textvariable=self.app_data.user_lib_path
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
        lower_button_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
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
            command=self.verify_files,
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

    def open_project_info_page(self):
        self.clear_window()
        self.toggle_active_button("Project Info")

        directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )
        directions_label.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
        directions_text = "Select the ruleset for your project, then browse and select the eQUEST model input files (*.inp) associated with each of the applicable models expected by the \nruleset."
        directions = ctk.CTkLabel(
            self,
            text=directions_text,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
        )
        directions.grid(row=1, column=1, columnspan=8, sticky="new", padx=5, pady=20)

        note_label = ctk.CTkLabel(
            self, text="Note: ", anchor="e", justify="left", font=("Arial", 16, "bold")
        )
        note_label.grid(row=2, column=0, sticky="new", padx=5, pady=20)
        note_text = "When you select an input file, it is expected that the same directory will also include the simulation output files associated with the selected input file. \nThis application will check for the following associated file extensions:\n(*.nhk), (*.lrp), (*.srp), (*.erp)\n\n(*) can be identical to the selected *.inp file or can include the suffix ' - Baseline Design'"
        note = ctk.CTkLabel(
            self, text=note_text, anchor="w", justify="left", font=("Arial", 14)
        )
        note.grid(row=2, column=1, columnspan=8, sticky="ew", padx=5, pady=20)

        # Project Ruleset and Design Day Criteria (row 3)
        ruleset_label = ctk.CTkLabel(
            self, text="Project Ruleset:", font=("Arial", 14, "bold"), anchor="e"
        )
        ruleset_label.grid(row=3, column=0, sticky="e", padx=5, pady=10)

        ruleset_dropdown = ctk.CTkOptionMenu(self, values=["ASHRAE 90.1-2019"])
        ruleset_dropdown.grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=10
        )

        # Rotation Exception Checkbox (row 3)
        rotation_exception_checkbox = ctk.CTkCheckBox(
            self,
            text="Meets Table G3.1(5) Baseline Building Performance (a) Exceptions",
            font=("Arial", 14),
            command=self.toggle_baseline_rotations,
        )
        rotation_exception_checkbox.grid(
            row=3, column=4, columnspan=4, sticky="w", padx=5, pady=10
        )

        # Create a frame to hold the file paths and select buttons for Ruleset Models
        ruleset_models_label = ctk.CTkLabel(
            self,
            text="Ruleset Models: ",
            anchor="e",
            justify="left",
            font=("Arial", 14, "bold"),
        )
        ruleset_models_label.grid(row=4, column=0, sticky="ew", padx=5, pady=20)

        ruleset_models_frame = CTkXYFrame(self, width=1000, height=250)
        ruleset_models_frame.grid(row=4, column=1, columnspan=8, sticky="nsw")

        # Add rows inside the frame
        self.create_file_row(ruleset_models_frame, 0, "User: ")
        self.create_file_row(ruleset_models_frame, 1, "Proposed: ")
        self.create_file_row(ruleset_models_frame, 2, "Baseline: ")
        self.baseline_rotation_rows["Baseline 90"] = self.create_file_row(
            ruleset_models_frame, 3, "Baseline 90: "
        )
        self.baseline_rotation_rows["Baseline 180"] = self.create_file_row(
            ruleset_models_frame, 4, "Baseline 180: "
        )
        self.baseline_rotation_rows["Baseline 270"] = self.create_file_row(
            ruleset_models_frame, 5, "Baseline 270: "
        )

        # Create the button to continue to the Project Info page
        self.continue_button = ctk.CTkButton(
            self,
            text="Continue",
            width=100,
            corner_radius=12,
            command=self.validate_project_info,
        )
        self.continue_button.grid(row=5, column=0, columnspan=9, pady=5)

    def open_buildings_page(self):
        self.clear_window()
        self.toggle_active_button("Buildings")

        # Create the button to test accessing rmd data
        test_button = ctk.CTkButton(
            self,
            text="Test Access RMD Zones",
            width=300,
            corner_radius=12,
            command=lambda: self.raise_error_window(
                f"RMD Zones: {self.app_data.rmds[0].zone_names}"
            ),
        )
        test_button.grid(row=5, column=0, columnspan=9, pady=5)

    def open_building_segments_page(self):
        self.clear_window()
        self.toggle_active_button("Building Segments")

    def open_spaces_page(self):
        self.clear_window()
        self.toggle_active_button("Spaces")

    def open_surfaces_page(self):
        self.clear_window()
        self.toggle_active_button("Surfaces")

    def open_systems_page(self):
        self.clear_window()
        self.toggle_active_button("Systems")

    def open_ext_lighting_page(self):
        self.clear_window()
        self.toggle_active_button("Ext. Lighting")

    def open_misc_page(self):
        self.clear_window()
        self.toggle_active_button("Misc.")

    def open_results_page(self):
        self.clear_window()
        self.toggle_active_button("Results")
