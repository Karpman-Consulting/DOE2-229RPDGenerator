import customtkinter as ctk
from tkinter import Menu, filedialog
from pathlib import Path

from interface.disclaimer_window import DisclaimerWindow
from interface.error_window import ErrorWindow
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)


class ProjectConfigWindow(ctk.CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        self.title("Project Configuration")
        self.license_window = None
        self.disclaimer_window = None
        self.error_window = None

        self.ruleset_model_row_widgets = {}

        # Initialize Widgets
        self.directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )
        directions_text = "Select the Energy Code or Above-Code Program for your project, then browse and select the eQUEST model input files (*.inp) \nassociated with each of the applicable models expected by the ruleset."
        self.directions = ctk.CTkLabel(
            self,
            text=directions_text,
            anchor="w",
            justify="left",
            font=("Arial", 14, "bold"),
        )
        self.note_label = ctk.CTkLabel(
            self, text="Note: ", anchor="e", justify="left", font=("Arial", 16, "bold")
        )
        note_text = "When you select an input file, it is expected that the same directory will also include the simulation output files associated with the selected input file. \nThis application will check for the following associated file extensions:\n(*.nhk), (*.lrp), (*.srp), (*.erp)\n\n(*) can be identical to the selected *.inp file or can include the suffix ' - Baseline Design'"
        self.note = ctk.CTkLabel(
            self, text=note_text, anchor="w", justify="left", font=("Arial", 14)
        )
        self.project_name_label = ctk.CTkLabel(
            self, text="Project Name: ", font=("Arial", 14, "bold"), anchor="e"
        )
        self.project_name_entry = ctk.CTkEntry(
            self, font=("Arial", 14), textvariable=self.main_app.data.project_name
        )
        self.ruleset_label = ctk.CTkLabel(
            self, text="Energy Code/Program:", font=("Arial", 14, "bold"), anchor="e"
        )
        self.new_construction_checkbox = ctk.CTkCheckBox(
            self,
            text="All New Construction?",
            font=("Arial", 14),
            variable=self.main_app.data.is_all_new_construction,
        )
        self.rotation_exception_checkbox = ctk.CTkCheckBox(
            self,
            text="Baseline Rotation Exempt? (90.1-2019 Table G3.1(5) Baseline Building Performance (a))",
            font=("Arial", 14),
            variable=self.main_app.data.has_rotation_exception,
            command=self.toggle_baseline_rotations,
        )
        self.ruleset_models_frame = ctk.CTkFrame(self, width=800)
        self.ruleset_dropdown = ctk.CTkOptionMenu(
            self,
            values=["ASHRAE 90.1-2019", "None"],
            variable=self.main_app.data.selected_ruleset,
            command=self.update_ruleset_model_frame,
        )
        self.ruleset_models_label = ctk.CTkLabel(
            self,
            text="Models: ",
            anchor="e",
            justify="left",
            font=("Arial", 14, "bold"),
        )
        self.output_dir_label = ctk.CTkLabel(
            self, text="Output Directory:", font=("Arial", 14, "bold"), anchor="e"
        )
        self.output_dir_entry = ctk.CTkEntry(
            self,
            font=("Arial", 14),
            width=500,
            textvariable=self.main_app.data.output_directory,
        )
        self.output_dir_button = ctk.CTkButton(
            self,
            text="Select",
            command=self.select_output_directory,
            width=80,
        )
        self.continue_button = ctk.CTkButton(
            self,
            text="Continue",
            width=100,
            corner_radius=12,
            command=self.validate_project_info,
        )

        self.menubar = self.create_menu_bar()
        self.place_widgets()
        self.create_nav_bar()

    def __repr__(self):
        return "ProjectConfigWindow"

    def create_nav_bar(self):
        # Create the button to continue to the Buildings page
        self.continue_button.grid(row=7, column=0, columnspan=9, pady=15)

    def create_menu_bar(self):
        menubar = Menu(self)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command="donothing")
        file_menu.add_command(label="Open", command="donothing")
        file_menu.add_command(label="Save", command="donothing")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Instructions", command="donothing")
        help_menu.add_command(label="Background", command="donothing")
        help_menu.add_separator()
        help_menu.add_command(label="License", command="donothing")
        help_menu.add_command(label="Disclaimer", command=self.raise_disclaimer_window)
        menubar.add_cascade(label="About", menu=help_menu)

        self.config(menu=menubar)
        return menubar

    def raise_disclaimer_window(self):
        if self.disclaimer_window is None or not self.disclaimer_window.winfo_exists():
            self.disclaimer_window = DisclaimerWindow(self)
            self.disclaimer_window.after(100, self.disclaimer_window.lift)
        else:
            self.disclaimer_window.focus()  # if window exists, focus it

    def raise_error_window(self, error_text):
        if not error_text:
            return
        self.error_window = ErrorWindow(self, error_text)
        self.error_window.after(100, self.error_window.lift)

    def place_widgets(self):
        # Place widgets
        # Row 0
        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=(20, 5))
        self.directions.grid(
            row=0, column=1, columnspan=6, sticky="new", padx=5, pady=(20, 5)
        )
        # Row 1
        self.note_label.grid(row=1, column=0, sticky="new", padx=5, pady=5)
        self.note.grid(row=1, column=1, columnspan=8, sticky="ew", padx=5, pady=5)
        # Row 2
        self.project_name_label.grid(
            row=2, column=0, sticky="e", padx=(20, 5), pady=(50, 10)
        )
        self.project_name_entry.grid(
            row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=(50, 10)
        )
        self.new_construction_checkbox.grid(
            row=2, column=5, sticky="w", padx=5, pady=(50, 10)
        )

        # Row 3
        self.ruleset_label.grid(row=3, column=0, sticky="e", padx=(20, 5), pady=5)
        self.ruleset_dropdown.grid(
            row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=5
        )

        # Row 4 Placeholder for the rotation exception checkbox
        # Row 5
        self.ruleset_models_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.show_ruleset_models()
        self.ruleset_models_frame.grid(
            row=5, column=1, columnspan=6, sticky="nsew", padx=5
        )

        # Row 6
        self.output_dir_label.grid(
            row=6, column=0, sticky="e", padx=(20, 5), pady=(15, 5)
        )
        self.output_dir_entry.grid(
            row=6, column=1, columnspan=5, sticky="ew", padx=5, pady=(15, 5)
        )
        self.output_dir_button.grid(row=6, column=6, sticky="ew", padx=5, pady=(15, 5))

    def update_ruleset_model_frame(self, selected_ruleset):
        self.rotation_exception_checkbox.grid_remove()
        self.clear_ruleset_models_frame()
        self.show_ruleset_models()

    def show_ruleset_models(self):
        # Main logic
        if self.main_app.data.selected_ruleset.get() == "ASHRAE 90.1-2019":
            self.rotation_exception_checkbox.grid(
                row=4, column=1, columnspan=4, sticky="w", padx=5, pady=(15, 5)
            )
            labels = ["Design: ", "Proposed: ", "Baseline: "]
            if not self.rotation_exception_checkbox.get():
                labels.extend(["Baseline 90: ", "Baseline 180: ", "Baseline 270: "])
        else:
            labels = ["Design: "]

        # Create and place rows based on the selected ruleset
        self.create_model_rows(labels)

    def create_model_rows(self, labels):
        """Create and place rows for ruleset model path widgets."""
        for row_num, label_text in enumerate(labels):
            label, path_entry, select_button = self.create_file_row(label_text)

            # Place widgets using grid
            label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
            path_entry.grid(
                row=row_num, column=1, columnspan=7, sticky="ew", padx=5, pady=5
            )
            select_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

            if len(labels) == 1:
                self.ruleset_models_frame.grid_rowconfigure(
                    0, weight=1
                )  # Center first row
            else:
                for i in range(len(labels)):
                    self.ruleset_models_frame.grid_rowconfigure(i, weight=0)

    def clear_ruleset_models_frame(self):
        for row_widgets in self.ruleset_model_row_widgets.values():
            for widget in row_widgets:
                widget.grid_remove()

    def toggle_baseline_rotations(self):
        """Add or remove Baseline rotation rows based on checkbox state."""
        for row_widgets in self.ruleset_model_row_widgets.values():
            if row_widgets[0].cget("text") in [
                "Baseline 90: ",
                "Baseline 180: ",
                "Baseline 270: ",
            ]:
                if row_widgets[0].winfo_ismapped():
                    # If visible, hide them
                    for widget in row_widgets:
                        widget.grid_remove()
                else:
                    # If hidden, show them
                    for widget in row_widgets:
                        widget.grid()

    def create_file_row(self, label_text):
        """Create a row of widgets without placing them using grid()."""
        model_text = label_text.split(":")[0]

        # Avoid recreating widgets if they already exist
        if model_text in self.ruleset_model_row_widgets:
            return self.ruleset_model_row_widgets[model_text]

        # Create label
        label = ctk.CTkLabel(
            self.ruleset_models_frame,
            text=label_text,
            font=("Arial", 14),
            width=90,
            anchor="e",  # Align text to the right within the label
        )

        # Create entry
        path_entry = ctk.CTkEntry(
            self.ruleset_models_frame, width=700, font=("Arial", 12)
        )

        model_type = model_text.replace("Design", "User")

        # File select button
        def select_file():
            selected_path = filedialog.askopenfilename(
                filetypes=[("eQUEST Input Files", "*.inp")]
            )
            if selected_path:
                path_entry.delete(0, "end")
                path_entry.insert(0, self._get_trimmed_path(selected_path))
                self.main_app.data.ruleset_model_file_paths[model_type] = selected_path

        select_button = ctk.CTkButton(
            self.ruleset_models_frame,
            text="Select",
            command=select_file,
            width=80,
            height=30,
        )

        # Store created widgets for reuse
        self.ruleset_model_row_widgets[model_text] = (
            label,
            path_entry,
            select_button,
        )

        return label, path_entry, select_button

    def validate_project_info(self):
        """Verify that all required file paths have been selected."""
        # Check that at least 1 file path has been selected
        if not any(self.main_app.data.ruleset_model_file_paths.values()):
            self.main_app.data.errors = [
                "At least one file must be selected to continue."
            ]
            self.raise_error_window("\n".join(self.main_app.data.errors))
            return

        # If the code reaches this point, at least one file is selected so clear any errors
        self.main_app.data.errors.clear()

        # For each file that is selected, make sure that the directory also contains the associated output files
        for (
            model_type,
            file_path,
        ) in self.main_app.data.ruleset_model_file_paths.items():
            if file_path:
                if not self.verify_associated_files(file_path):
                    model_type = model_type.replace("User", "Design")
                    self.main_app.data.errors.append(
                        f"Associated simulation output files not found for the selected '{model_type}' model."
                    )

        if len(self.main_app.data.errors) > 0:
            self.raise_error_window("\n".join(self.main_app.data.errors))
            return

        # If the code reaches this point, at least one file is selected and all associated files are found so clear any errors
        self.main_app.data.errors.clear()

        # Required model types
        required_models = ["User", "Proposed", "Baseline"]
        if not self.rotation_exception_checkbox.get():
            required_models.extend(["Baseline 90", "Baseline 180", "Baseline 270"])

        # Check if all required model types have file paths selected
        for model_type in required_models:
            if (
                model_type not in self.main_app.data.ruleset_model_file_paths
                or not self.main_app.data.ruleset_model_file_paths[model_type]
            ):
                model_type = model_type.replace("User", "Design")
                self.main_app.data.warnings.append(
                    f"The '{model_type}' model is missing and is required to evaluate the ASHRAE 90.1-2019 ruleset."
                )

        # If there are no errors, generate RMDs and open the Main Application Window
        if len(self.main_app.data.errors) == 0:
            self.main_app.data.rpd = RulesetProjectDescription(
                self.main_app.data.project_name.get()
            )
            self.main_app.data.generate_rmd_data(self.main_app.data.rpd)
            self.main_app.project_config_complete()

        else:
            self.raise_error_window("\n".join(self.main_app.data.errors))

    @staticmethod
    def verify_associated_files(file_path: str) -> bool:
        """
        Check if the directory of the given file contains files with the same name
        or the same name with the suffix ' - Baseline Design' for the specified file types.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if all related files are found, False otherwise.
        """
        # Expected file extensions
        file_extensions = [".erp", ".srp", ".lrp", ".nhk"]

        file_path = Path(file_path)
        base_name = file_path.stem
        directory = file_path.parent

        # Check for each file type
        for ext in file_extensions:
            # Construct file names to check
            normal_file = directory / f"{base_name}{ext}"
            baseline_file = directory / f"{base_name} - Baseline Design{ext}"
            # Check existence
            if not normal_file.is_file() and not baseline_file.is_file():
                return False

        return True

    def select_output_directory(self):
        """Opens a directory selection dialog and updates the entry field."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_entry.delete(0, "end")
            self.output_dir_entry.insert(0, directory)
            self.main_app.data.output_directory.set(directory)

    @staticmethod
    def _get_trimmed_path(file_path: str) -> str:
        """Helper function to extract parent directory and filename from a file path using pathlib."""
        path = Path(file_path)
        if path.parent:
            return f"{path.parent.name}/{path.name}"
        return path.name
