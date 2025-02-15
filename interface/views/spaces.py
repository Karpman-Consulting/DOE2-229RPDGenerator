import customtkinter as ctk

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


STANDARD_FONT = ("Arial", 16, "bold")
READONLY = "readonly"
LEFT = "left"
W = "w"


class SpacesView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        self.view_frame = ctk.CTkFrame(self)

        """Directions frame holds all directions info and will get 'gridded' within the surfaces view grid"""
        self.directions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.directions_label = ctk.CTkLabel(
            self.directions_frame,
            text="Directions: ",
            font=STANDARD_FONT,
        )
        self.directions_widget = ctk.CTkLabel(
            self.directions_frame,
            text=" Directions: Assign the various space data parameters for each Space.",
            font=("Arial", 14),
        )

    def __repr__(self):
        return "SpacesView"

    def open_view(self):
        self.toggle_active_button("Spaces")
        self.grid_propagate(False)

        """2 rows in the main surface view structure. View frame (row 2, index 1) has a weight to make it fill up
        the empty space in the window"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Directions
        self.directions_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        self.directions_label.grid(row=0, column=0)
        self.directions_widget.grid(row=0, column=1)

        # Subview frame
        self.view_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)

        spaces_view = SpacesSubview(self.view_frame)
        spaces_view.grid(row=0, column=0, sticky="nsew")
        spaces_view.open_view()


class SpacesSubview(CTkXYFrame):
    def __init__(self, view_frame):
        super().__init__(view_frame)
        self.spaces_view = view_frame.master
        self.app_data = self.spaces_view.app_data
        self.is_view_populated = False

    def __repr__(self):
        return "SpacesSubview"

    def open_view(self):
        self.populate_subview() if not self.is_view_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, space_name in enumerate(self.app_data.rmds[0].space_map.keys()):
            self.add_row(i, space_name)

        self.is_view_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        if not self.app_data.is_all_new_construction:
            status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
            status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        lighting_space_type_label = ctk.CTkLabel(
            self, text="Lighting Space Type", font=STANDARD_FONT
        )
        lighting_space_type_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        envelope_space_type_label = ctk.CTkLabel(
            self, text="Envelope Space Type", font=STANDARD_FONT
        )
        envelope_space_type_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        ventilation_space_type_label = ctk.CTkLabel(
            self, text="Ventilation Space Type", font=STANDARD_FONT
        )
        ventilation_space_type_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        swh_space_type_label = ctk.CTkLabel(
            self, text="SWH Space Type", font=STANDARD_FONT
        )
        swh_space_type_label.grid(row=0, column=5, padx=(0, 20), pady=5)
        lighting_occ_controls_label = ctk.CTkLabel(
            self, text="Lighting Occ. Controls", font=STANDARD_FONT
        )
        lighting_occ_controls_label.grid(row=0, column=6, padx=(0, 20), pady=5)
        daylighting_controls_label = ctk.CTkLabel(
            self, text="Daylighting Controls", font=STANDARD_FONT
        )
        daylighting_controls_label.grid(row=0, column=7, padx=(0, 20), pady=5)
        occ_controls_modeled_via_schedule_label = ctk.CTkLabel(
            self, text="Occ. Controls Modeled via Schedule?", font=STANDARD_FONT
        )
        occ_controls_modeled_via_schedule_label.grid(
            row=0, column=8, padx=(0, 20), pady=5
        )
        daylighting_modeled_via_schedule_label = ctk.CTkLabel(
            self, text="Daylighting Modeled via Schedule?", font=STANDARD_FONT
        )
        daylighting_modeled_via_schedule_label.grid(
            row=0, column=9, padx=(0, 20), pady=5
        )

    def add_row(self, i, space_name):
        name_label = ctk.CTkLabel(self, text=f"{space_name}")
        name_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        if not self.app_data.is_all_new_construction:
            status_combo = ctk.CTkComboBox(
                self,
                values=self.app_data.StatusDescriptions.get_list(),
                state=READONLY,
            )
            status_combo._entry.configure(justify=LEFT)
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
        lighting_space_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.LightingSpaceDescriptions2019ASHRAE901TG37.get_list(),
            state=READONLY,
        )
        lighting_space_type_combo._entry.configure(justify=LEFT)
        lighting_space_type_combo.grid(
            row=(i + 1), column=2, padx=(0, 20), pady=(0, 20)
        )
        envelope_space_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.EnvelopeSpaceDescriptions2019ASHRAE901.get_list(),
            state=READONLY,
        )
        envelope_space_type_combo._entry.configure(justify=LEFT)
        envelope_space_type_combo.grid(
            row=(i + 1), column=3, padx=(0, 20), pady=(0, 20)
        )
        ventilation_space_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.VentilationSpaceDescriptions2019ASHRAE901.get_list(),
            state=READONLY,
        )
        ventilation_space_type_combo._entry.configure(justify=LEFT)
        ventilation_space_type_combo.grid(
            row=(i + 1), column=4, padx=(0, 20), pady=(0, 20)
        )
        swh_space_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.ServiceWaterHeatingSpaceDescriptions2019ASHRAE901.get_list(),
            state=READONLY,
        )
        swh_space_type_combo._entry.configure(justify=LEFT)
        swh_space_type_combo.grid(row=(i + 1), column=5, padx=(0, 20), pady=(0, 20))
        lighting_occ_controls_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.LightingOccupancyControlOptions.get_list(),
            state=READONLY,
        )
        lighting_occ_controls_combo._entry.configure(justify=LEFT)
        lighting_occ_controls_combo.grid(
            row=(i + 1), column=6, padx=(0, 20), pady=(0, 20)
        )
        daylighting_controls_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.LightingDaylightingControlOptions.get_list(),
            state=READONLY,
        )
        daylighting_controls_combo._entry.configure(justify=LEFT)
        daylighting_controls_combo.grid(
            row=(i + 1), column=7, padx=(0, 20), pady=(0, 20)
        )
        occ_controls_modeled_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        occ_controls_modeled_checkbox.grid(
            row=(i + 1), column=8, padx=(0, 20), pady=(0, 20)
        )
        daylighting_modeled_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        daylighting_modeled_checkbox.grid(
            row=(i + 1), column=9, padx=(0, 20), pady=(0, 20)
        )
