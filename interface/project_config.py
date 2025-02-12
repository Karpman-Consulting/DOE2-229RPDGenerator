import customtkinter as ctk
from tkinter import Menu, filedialog
from pathlib import Path

from interface.disclaimer_window import DisclaimerWindow
from interface.error_window import ErrorWindow


class ProjectConfigWindow(ctk.CTkToplevel):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        self.title("Project Configuration")
        self.license_window = None
        self.disclaimer_window = None
        self.error_window = None

        self.ruleset_model_row_widgets = {}

        self.selected_ruleset = ctk.StringVar()
        self.selected_ruleset.set("ASHRAE 90.1-2019")

        # Initialize Widgets
        self.new_construction_checkbox = None
        self.new_construction_checkbox = ctk.CTkCheckBox(
            self,
            text="All new construction?",
            font=("Arial", 14),
        )
        self.rotation_exception_checkbox = ctk.CTkCheckBox(
            self,
            text="Meets 90.1-2019 Table G3.1(5) Baseline Building Performance (a) Exceptions",
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
        self.ruleset_label = ctk.CTkLabel(
            self, text="Energy Code/Program:", font=("Arial", 14, "bold"), anchor="e"
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
            text="Models: ",
            anchor="e",
            justify="left",
            font=("Arial", 14, "bold"),
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
        self.continue_button.grid(row=5, column=0, columnspan=9, pady=15)

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
        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        self.directions.grid(row=0, column=1, columnspan=6, sticky="new", pady=20)
        # Row 1
        self.note_label.grid(row=1, column=0, sticky="new", padx=5, pady=20)
        self.note.grid(
            row=1, column=1, columnspan=8, sticky="ew", padx=(5, 20), pady=20
        )
        # Row 2
        self.ruleset_label.grid(row=2, column=0, sticky="e", padx=(20, 5), pady=10)
        self.ruleset_dropdown.grid(
            row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=10
        )
        self.new_construction_checkbox.grid(
            row=2, column=3, sticky="w", padx=5, pady=10
        )
        # Row 3 Placeholder for the rotation exception checkbox
        # Row 4
        self.ruleset_models_label.grid(row=4, column=0, sticky="ew", padx=5, pady=20)

        self.show_ruleset_models(self.ruleset_models_frame)
        self.ruleset_models_frame.grid(row=4, column=1, columnspan=6, sticky="nsew")

    def update_ruleset_model_frame(self, ruleset_models_frame, selected_ruleset):
        self.selected_ruleset.set(selected_ruleset)
        self.rotation_exception_checkbox.grid_remove()
        self.clear_ruleset_models_frame()
        self.show_ruleset_models(ruleset_models_frame)

    def show_ruleset_models(self, parent_frame):
        # Main logic
        if self.selected_ruleset.get() == "ASHRAE 90.1-2019":
            self.rotation_exception_checkbox.grid(
                row=3, column=3, columnspan=4, sticky="w", padx=5, pady=10
            )
            labels = ["Design: ", "Proposed: ", "Baseline: "]
            """PH stands for Placeholder. Used to fill a UI gap when the rotation exception checkbox is checked.
            Label will not be displayed and other widgets in the row will not be created."""
            if not self.rotation_exception_checkbox.get():
                labels.extend(
                    [
                        "Baseline 90: ",
                        "Baseline 180: ",
                        "Baseline 270: ",
                        "PH Baseline 90: ",
                        "PH Baseline 180: ",
                        "PH Baseline 270: ",
                    ]
                )
        else:
            labels = ["Design: "]

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

            # If the label is a placeholder, do not place the widgets. Only place blank label.
            if label_text in [
                "PH Baseline 90: ",
                "PH Baseline 180: ",
                "PH Baseline 270: ",
            ]:
                label.grid_remove()

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

    """To avoid the jarring experience of the UI elements shifting around when the rotation exception checkbox
     is checked, I made blank placeholder rows for each of the 3 baseline rotations. There is a little bit of 
     movement when the checkbox is toggled, but it is much less noticeable. I think the best solution for this
     would be to disable the baseline rotation rows when the exception checkbox is checked. Tkinter does not handle
     disabling input fields very well, so I went with this solution instead. I could be very easily convinced to
     change my mind here either way."""

    def toggle_baseline_rotations(self):
        """Add or remove Baseline rotation rows based on checkbox state."""
        for row_widgets in self.ruleset_model_row_widgets.values():
            if row_widgets[0].cget("text") in [
                "Baseline 90: ",
                "Baseline 180: ",
                "Baseline 270: ",
                "",
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

        # If the label is a placeholder, do not place the widgets. Only place blank label.
        if label_text in ["PH Baseline 90: ", "PH Baseline 180: ", "PH Baseline 270: "]:
            label = ctk.CTkLabel(parent_frame, text="")
            return label, label, label

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

                self.main_app.data.ruleset_model_file_paths[
                    label_text.split(":")[0].replace("Design", "User")
                ] = file_path

        select_button = ctk.CTkButton(
            parent_frame, text="Select", command=select_file, width=80, height=30
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
            self.save_configuration_data()
            self.main_app.data.generate_rmds()
            self.run_model_checks()
            if len(self.main_app.data.errors) == 0:
                self.main_app.project_config_complete()
            else:
                self.raise_error_window("\n".join(self.main_app.data.errors))
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

    # TODO: Magic string dictionary values in config data. Should we make enums for these?
    def save_configuration_data(self):
        self.main_app.data.configuration_data.update(
            self.main_app.data.ruleset_model_file_paths
        )
        self.main_app.data.configuration_data["new_construction"] = bool(
            self.new_construction_checkbox.get()
        )

    def run_model_checks(self):
        spaces_zones_set = set()
        spaces_zones_list = []
        surfaces_set = set()
        surfaces_list = []

        # Save rmd data to check
        for rmd in self.main_app.data.rmds:
            rmd_spaces_zones_list = []
            rmd_surfaces_list = []

            # Check for DOE version 2.3 - error
            if not rmd.doe2_version.startswith("DOE-2.3"):
                self.main_app.data.errors.append(
                    f"'{rmd.type}' model does not use DOE-2.3"
                )

            if rmd.type in ["Baseline 90", "Baseline 180", "Baseline 270", "Proposed"]:
                rmd_spaces_zones_list.append(len(rmd.zone_names))
                for space in rmd.space_map:
                    rmd_spaces_zones_list.append(space)
                    rmd_spaces_zones_list.append(rmd.space_map[space].u_name)
                    rmd_surfaces_list.append(len(rmd.space_map[space].surfaces))
                    for surface in rmd.space_map[space].surfaces:
                        rmd_surfaces_list.append(surface["classification"])
                        if surface.get("area"):
                            rmd_surfaces_list.append(surface["area"])
                    surfaces_list.append(rmd_surfaces_list)
                spaces_zones_list.append(rmd_spaces_zones_list)

            """Errors: Verify that ZONE-TYPE keyword is not PLENUM for all spaces
            Errors: Verify that the LTG-SPEC-METHOD is POWER-DEFINITION for all spaces"""
            for space in rmd.space_map:
                space_obj = rmd.get_obj(space)
                if space_obj.keyword_value_pairs["ZONE-TYPE"] == "PLENUM":
                    self.main_app.data.errors.append(
                        f"Error: '{rmd.type}' model, space '{space}' has a plenum zone type"
                    )
                if (
                    space_obj.keyword_value_pairs["LTG-SPEC-METHOD"]
                    != "POWER-DEFINITION"
                ):
                    self.main_app.data.errors.append(
                        f"Error: '{rmd.type}' model, does not have a power definition lighting specification method"
                    )

            """Errors: Verify that TYPE keyword is not PLENUM for all zones"""
            for zone in rmd.zone_names:
                zone_obj = rmd.get_obj(zone)
                if zone_obj.keyword_value_pairs["TYPE"] == "PLENUM":
                    self.main_app.data.errors.append(
                        f"Error: '{rmd.type}' model, zone '{zone}' has a plenum zone type"
                    )

            """Warnings: Verify that any/all Boilers, Domestic Water Heaters, and Systems have 
            values > 0 for HEAT-INPUT-RATIO, HEAT-INPUT-RATIO, and FURNACE-HIR respectively"""
            for boiler in rmd.boiler_names:
                boiler_obj = rmd.get_obj(boiler)
                heat_input_ratio = boiler_obj.keyword_value_pairs.get(
                    "HEAT-INPUT-RATIO"
                )
                if heat_input_ratio and float(heat_input_ratio) <= 0.0:
                    self.main_app.data.errors.append(
                        f"Warning: '{rmd.type}' model, boiler '{boiler}' has a heat input ratio of {heat_input_ratio}"
                    )
            for domestic_water_heater in rmd.domestic_water_heater_names:
                domestic_water_heater_obj = rmd.get_obj(domestic_water_heater)
                heat_input_ratio = domestic_water_heater_obj.keyword_value_pairs.get(
                    "HEAT-INPUT-RATIO"
                )
                if heat_input_ratio and float(heat_input_ratio) <= 0.0:
                    self.main_app.data.errors.append(
                        f"Warning: '{rmd.type}' model, domestic water heater '{domestic_water_heater}' "
                        f"has a heat input ratio of {heat_input_ratio}"
                    )
            # TODO: Circle back to this. Not finding "FURNACE-HIR" keyword
            # for system in rmd.system_names:
            #     system_obj = rmd.get_obj(system)
            #     furnace_hir = float(system_obj.keyword_value_pairs["FURNACE-HIR"])
            #     if furnace_hir <= 0.0:
            #         print("Add warning")

        """Warnings: Verify that Baseline (90, 180, 270) and Proposed have the same number of zones and 
        that the IDs of all zones and spaces match between models"""
        for i in spaces_zones_list:
            spaces_zones_set.add(tuple(i))
        if len(spaces_zones_set) > 1:
            self.main_app.data.errors.append(
                f"Warning: Space or zone identifiers do not match between models"
            )

        """Warnings: Verify that every space has the same quantity, types, and areas of surfaces between 
        Baseline (90, 180, 270) and Proposed."""
        for i in surfaces_list:
            surfaces_set.add(tuple(i))
        if len(surfaces_set) > 1:
            self.main_app.data.errors.append(
                f"Warning: Surface identifiers do not match between models"
            )
