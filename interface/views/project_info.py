import customtkinter as ctk
from tkinter import filedialog
from itertools import islice

from interface.base_view import BaseView


class ProjectInfoView(BaseView):
    def __init__(self, app):
        super().__init__(app)

        self.baseline_rotation_rows = {}

        # Initialize attributes to hold references to Widgets
        self.rotation_exception_checkbox = None

    def open_view(self):
        self.clear_window()

        # Overwrite behavior of the continue button
        self.app.continue_button.configure(command=self.validate_project_info)

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
        self.rotation_exception_checkbox = ctk.CTkCheckBox(
            self,
            text="Meets Table G3.1(5) Baseline Building Performance (a) Exceptions",
            font=("Arial", 14),
            command=self.toggle_baseline_rotations,
        )
        self.rotation_exception_checkbox.grid(
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

        ruleset_models_frame = ctk.CTkFrame(self, width=800, height=250)
        ruleset_models_frame.grid(row=4, column=1, columnspan=8, sticky="nsew")

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

                self.app.app_data.ruleset_model_file_paths[label_text.split(":")[0]] = (
                    file_path
                )

        select_button = ctk.CTkButton(
            parent_frame, text="Select", command=select_file, width=80, height=30
        )
        select_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

        return label, path_entry, select_button

    def validate_project_info(self):
        """Verify that all required file paths have been selected."""
        # Check that at least 1 file path has been selected
        if not any(self.app.app_data.ruleset_model_file_paths.values()):
            self.app.app_data.errors.append(
                "At least one file must be selected to continue."
            )
            self.update_warnings_errors()
            return

        # For each file that is selected, make sure that the directory also contains the associated output files
        for model_type, file_path in self.app.app_data.ruleset_model_file_paths.items():
            if file_path:
                if not self.app.app_data.verify_associated_files(file_path):
                    self.app.app_data.errors.append(
                        f"Associated simulation output files not found for the selected '{model_type}' model."
                    )
                    self.update_warnings_errors()
                    return

        # Required model types
        required_models = ["User", "Proposed", "Baseline"]

        # Check if required model types have file paths
        for model_type in required_models:
            if (
                model_type not in self.app.app_data.ruleset_model_file_paths
                or not self.app.app_data.ruleset_model_file_paths[model_type]
            ):
                self.app.app_data.warnings.append(
                    f"The file path for '{model_type}' is missing and is required to evaluate the ASHRAE 90.1-2019 ruleset."
                )

        # Check rotation files if the rotation exception checkbox is not checked
        if not self.rotation_exception_checkbox.get():
            required_rotations = ["Baseline 90", "Baseline 180", "Baseline 270"]
            for model_type in required_rotations:
                if (
                    model_type not in self.app.app_data.ruleset_model_file_paths
                    or not self.app.app_data.ruleset_model_file_paths[model_type]
                ):
                    self.app.app_data.warnings.append(
                        f"The file path for '{model_type}' is missing and is required to evaluate the ASHRAE 90.1-2019 ruleset."
                    )

        self.update_warnings_errors()
        # If there are no errors, continue to the next page
        self.read_project_files__continue()

    def read_project_files__continue(self):
        self.app.app_data.generate_rmds()
        self.toggle_project_tabs()
        self.app.open_buildings_page()

    def toggle_project_tabs(self):
        for name, button in islice(self.app.navbar_buttons.items(), 1, None):
            if self.app.navbar_buttons[name].cget("state") == "disabled":
                self.app.navbar_buttons[name].configure(state="normal")
            else:
                self.app.navbar_buttons[name].configure(state="disabled")
