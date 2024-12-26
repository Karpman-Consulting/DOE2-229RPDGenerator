import customtkinter as ctk
from tkinter import filedialog
from itertools import islice

from interface.base_view import BaseView


class ProjectInfoView(BaseView):
    def __init__(self, main):
        super().__init__(main)

        self.ruleset_model_row_widgets = {}

        # Initialize Widgets
        self.rotation_exception_checkbox = ctk.CTkCheckBox(
            self,
            text="Meets Table G3.1(5) Baseline Building Performance (a) Exceptions",
            font=("Arial", 14),
            command=self.toggle_baseline_rotations,
        )
        self.directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )

        directions_text = "Select the ruleset for your project, then browse and select the eQUEST model input files (*.inp) associated with each of the applicable models expected by the \nruleset."
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
        self.ruleset_label = ctk.CTkLabel(
            self, text="Project Ruleset:", font=("Arial", 14, "bold"), anchor="e"
        )
        self.ruleset_models_frame = ctk.CTkFrame(self, width=800, height=250)
        self.ruleset_dropdown = ctk.CTkOptionMenu(
            self,
            values=["ASHRAE 90.1-2019", "None"],
            command=lambda selection: self.update_ruleset_model_frame(
                self.ruleset_models_frame, selection
            ),
        )
        self.ruleset_models_label = ctk.CTkLabel(
            self,
            text="Ruleset Models: ",
            anchor="e",
            justify="left",
            font=("Arial", 14, "bold"),
        )

    def __repr__(self):
        return "ProjectInfoView"

    def open_view(self):
        # Overwrite behavior of the continue button
        self.main.continue_button.configure(command=self.validate_project_info)
        # Update the errors and warnings button formatting
        self.update_warnings_errors()

        self.toggle_active_button("Project Info")

        # Place widgets
        # Row 0
        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        self.directions.grid(
            row=0, column=1, columnspan=8, sticky="new", padx=5, pady=20
        )
        # Row 1
        self.note_label.grid(row=1, column=0, sticky="new", padx=5, pady=20)
        self.note.grid(row=1, column=1, columnspan=8, sticky="ew", padx=5, pady=20)
        # Row 2
        self.ruleset_label.grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.ruleset_dropdown.grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=10
        )
        # Row 3 Placeholder for the rotation exception checkbox
        # Row 4
        self.ruleset_models_label.grid(row=4, column=0, sticky="ew", padx=5, pady=20)

        self.show_ruleset_models(self.ruleset_models_frame)
        self.ruleset_models_frame.grid(row=4, column=1, columnspan=8, sticky="nsew")

    def update_ruleset_model_frame(self, ruleset_models_frame, selected_ruleset):
        self.main.app_data.selected_ruleset.set(selected_ruleset)
        self.rotation_exception_checkbox.grid_remove()
        self.clear_ruleset_models_frame()
        self.show_ruleset_models(ruleset_models_frame)

    def show_ruleset_models(self, parent_frame):
        # Main logic
        if self.main.app_data.selected_ruleset.get() == "ASHRAE 90.1-2019":
            self.rotation_exception_checkbox.grid(
                row=3, column=4, columnspan=4, sticky="w", padx=5, pady=10
            )
            labels = ["User: ", "Proposed: ", "Baseline: "]
            if not self.rotation_exception_checkbox.get():
                labels.extend(["Baseline 90: ", "Baseline 180: ", "Baseline 270: "])
        else:
            labels = ["User: "]

        # Create and place rows based on the selected ruleset
        self.create_model_rows(parent_frame, labels)

    def create_model_rows(self, parent_frame, labels):
        """Create and place rows for ruleset model path widgets."""
        for row_num, label_text in enumerate(labels):
            label, path_entry, select_button = self.create_file_row(
                parent_frame, label_text
            )

            # Place widgets using grid
            label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
            path_entry.grid(
                row=row_num, column=1, columnspan=7, sticky="ew", padx=5, pady=5
            )
            select_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

            # Store created widgets for reuse
            self.ruleset_model_row_widgets[label_text.split(":")[0]] = (
                label,
                path_entry,
                select_button,
            )

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

    def create_file_row(self, parent_frame, label_text):
        """Create a row of widgets without placing them using grid()."""
        if self.ruleset_model_row_widgets.get(label_text.split(":")[0]):
            return self.ruleset_model_row_widgets[label_text.split(":")[0]]

        # Create label
        label = ctk.CTkLabel(
            parent_frame,
            text=label_text,
            font=("Arial", 14),
            width=90,
            anchor="e",  # Align text to the right within the label
        )

        # Create entry
        path_entry = ctk.CTkEntry(parent_frame, width=700, font=("Arial", 12))

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

                self.main.app_data.ruleset_model_file_paths[
                    label_text.split(":")[0]
                ] = file_path

        select_button = ctk.CTkButton(
            parent_frame, text="Select", command=select_file, width=80, height=30
        )

        return label, path_entry, select_button

    def validate_project_info(self):
        """Verify that all required file paths have been selected."""
        # Check that at least 1 file path has been selected
        if not any(self.main.app_data.ruleset_model_file_paths.values()):
            self.main.app_data.errors = [
                "At least one file must be selected to continue."
            ]
            self.update_warnings_errors()
            return

        # If the code reaches this point, at least one file is selected so clear any errors
        self.main.app_data.errors.clear()

        # For each file that is selected, make sure that the directory also contains the associated output files
        for (
            model_type,
            file_path,
        ) in self.main.app_data.ruleset_model_file_paths.items():
            if file_path:
                if not self.main.app_data.verify_associated_files(file_path):
                    self.main.app_data.errors.append(
                        f"Associated simulation output files not found for the selected '{model_type}' model."
                    )
                    self.update_warnings_errors()

        if len(self.main.app_data.errors) > 0:
            return

        # If the code reaches this point, at least one file is selected and all associated files are found so clear any errors
        self.main.app_data.errors.clear()

        # Required model types
        required_models = ["User", "Proposed", "Baseline"]
        if not self.rotation_exception_checkbox.get():
            required_models.extend(["Baseline 90", "Baseline 180", "Baseline 270"])

        # Check if all required model types have file paths selected
        for model_type in required_models:
            if (
                model_type not in self.main.app_data.ruleset_model_file_paths
                or not self.main.app_data.ruleset_model_file_paths[model_type]
            ):
                self.main.app_data.warnings.append(
                    f"The '{model_type}' model is missing and is required to evaluate the ASHRAE 90.1-2019 ruleset."
                )

        self.update_warnings_errors()
        # If there are no errors, continue to the next page
        self.read_project_files__continue()

    def read_project_files__continue(self):
        self.main.app_data.generate_rmds()
        self.toggle_project_tabs()
        self.main.show_view("Buildings")

    def toggle_project_tabs(self):
        for name, button in islice(self.main.navbar_buttons.items(), 1, None):
            if self.main.navbar_buttons[name].cget("state") == "disabled":
                self.main.navbar_buttons[name].configure(state="normal")
            else:
                self.main.navbar_buttons[name].configure(state="disabled")
