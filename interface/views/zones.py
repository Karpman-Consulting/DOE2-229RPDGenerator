import customtkinter as ctk
import interface.custom_widgets as cw
from PIL import Image

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


STANDARD_FONT = ("Arial", 16, "bold")
READONLY = "readonly"
LEFT = "left"
W = "w"
PAD20 = (0, 20)


class ZonesView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        self.view_frame = ctk.CTkFrame(self)

        """Directions frame holds all directions info and will get 'gridded' within the surfaces view grid"""
        self.directions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.directions_label = ctk.CTkLabel(
            self.directions_frame,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=STANDARD_FONT,
        )
        self.directions_widget = ctk.CTkLabel(
            self.directions_frame,
            text="Assign all Zones in your model to the Building Areas created on the previous tab. This can be done by Floor, or more granularly by Zone. If any zones in the \n"
            "model represent multiple zones in the design, provide the quantity of aggregated zones. If a zone's infiltration in the Proposed model is based on a \n"
            "measured infiltration rate declare so here. If a zone contains more than 1 space, define additional spaces as necessary by clicking the quantity in the Child \n"
            "Spaces column to open the Child Spaces window. Child Spaces should be created as necessary to represent the entirety of the Zone, e.g. an aggregated \n"
            "zone that is in reality 3 zones where each zone has 2 spaces should have 6 Child Spaces total.",
            font=("Arial", 14, "bold"),
            anchor="w",
            justify="left",
        )

    def __repr__(self):
        return "ZonesView"

    def open_view(self):
        self.toggle_active_button("Zones")
        self.grid_propagate(False)

        """2 rows in the main surface view structure. View frame (row 2, index 1) has a weight to make it fill up
        the empty space in the window"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Directions
        self.directions_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        self.directions_widget.grid(
            row=0, column=1, columnspan=8, sticky="new", padx=5, pady=20
        )

        # Subview frame
        self.view_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=PAD20)
        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)

        zones_view = ZonesSubview(self.view_frame)
        zones_view.grid(row=0, column=0, sticky="nsew")
        zones_view.open_view()


class ZonesSubview(CTkXYFrame):
    def __init__(self, view_frame):
        super().__init__(view_frame)
        self.zones_view = view_frame.master
        self.main_app_data = self.zones_view.window.main_app.data
        self.is_view_populated = False
        self.child_space_window = None
        self.zones_by_floor = {}
        self.floor_comboboxes = {}
        self.zone_comboboxes = {}
        self.zone_widgets = {}

        self.get_zones_by_floors()

    def __repr__(self):
        return "ZonesSubview"

    def open_view(self):
        self.populate_subview() if not self.is_view_populated else None

    def populate_subview(self):
        self.add_column_headers()

        main_row = 0
        for floor, zones in self.zones_by_floor.items():
            self.add_main_row(main_row, floor)
            main_row += 1
            for zone in zones:
                self.add_row(main_row, zone)
                main_row += 1

        self.is_view_populated = True

    def add_column_headers(self):
        collapse_expand_label = ctk.CTkLabel(self, text="", font=STANDARD_FONT)
        collapse_expand_label.grid(row=0, column=0, padx=PAD20, pady=5)

        zone_floor_label = ctk.CTkLabel(self, text="Floor/Zone", font=STANDARD_FONT)
        zone_floor_label.grid(row=0, column=1, padx=PAD20, pady=5)
        building_area_label = ctk.CTkLabel(
            self, text="Building Area", font=STANDARD_FONT
        )
        building_area_label.grid(row=0, column=2, padx=PAD20, pady=5)
        aggregated_zone_quantity_label = ctk.CTkLabel(
            self, text="Aggregated Zone Qty", font=STANDARD_FONT
        )
        aggregated_zone_quantity_label.grid(row=0, column=3, padx=PAD20, pady=5)
        measured_infiltration_rate_label = ctk.CTkLabel(
            self, text="Measured Infiltration Rate?", font=STANDARD_FONT
        )
        measured_infiltration_rate_label.grid(row=0, column=4, padx=PAD20, pady=5)
        child_spaces_label = ctk.CTkLabel(self, text="Child Spaces", font=STANDARD_FONT)
        child_spaces_label.grid(row=0, column=5, padx=PAD20, pady=5)

    def add_main_row(self, i, floor_name):
        # Frame spanning all columns with a different background color
        main_row_frame = ctk.CTkFrame(self, fg_color="gray30")
        main_row_frame.grid(row=(i + 1), column=0, columnspan=6, sticky="ew")

        collapse_button = ctk.CTkButton(
            self,
            text="−",  # Default to expanded state
            width=30,
            height=30,
            corner_radius=10,
            command=lambda: self.toggle_zone_visibility(floor_name, collapse_button),
            bg_color="gray30",  # Same color as the frame
        )
        collapse_button.grid(row=(i + 1), column=0, padx=(5, 0))

        # Ensure the frame stretches across all columns
        for col in range(5):
            main_row_frame.grid_columnconfigure(col, weight=1)

        floor_label = ctk.CTkLabel(
            self,
            text=f"{floor_name}",
            width=135,
            anchor=W,
            font=("Arial", 14, "bold"),  # Larger, bold font
            text_color="white",
            bg_color="gray30",  # Same color as the frame
        )
        floor_label.grid(row=(i + 1), column=1, padx=20, pady=10, sticky=W)

        # Place the Building Area ComboBox in `self` (not inside `main_row_frame`) to align properly
        building_area_combo = ctk.CTkComboBox(
            self,
            # TODO: Placeholder for Building Areas tab data
            values=["Building Area 1"],
            state=READONLY,
            fg_color="#5B9BD5",
            border_color="#5B9BD5",
            button_color="#3A7EBF",
            dropdown_fg_color="#5B9BD5",
            dropdown_hover_color="lightblue",
            bg_color="gray30",  # Same color as the frame
            command=lambda value, floor=floor_name: self.set_default_value_by_floor(
                floor, value
            ),
        )
        building_area_combo.set("Building Area 1")
        building_area_combo._entry.configure(justify=LEFT)
        building_area_combo.grid(row=(i + 1), column=2, padx=PAD20, pady=10)

        self.floor_comboboxes[floor_name] = building_area_combo

        # Add empty labels in `main_row_frame` for spacing
        ctk.CTkLabel(main_row_frame, text="").grid(row=0, column=3, padx=PAD20, pady=10)
        ctk.CTkLabel(main_row_frame, text="").grid(row=0, column=4, padx=PAD20, pady=10)

    def add_row(self, i, zone_name):
        floor_label = ctk.CTkLabel(self, text=f"{zone_name}")
        floor_label.grid(row=(i + 1), column=1, padx=20, pady=PAD20, sticky=W)
        building_area_combo = ctk.CTkComboBox(
            self,
            # TODO: Placeholder for Building Areas tab data
            values=["Building Area 1"],
            state=READONLY,
        )
        building_area_combo.set("Building Area 1")
        building_area_combo._entry.configure(justify=LEFT)
        building_area_combo.grid(row=(i + 1), column=2, padx=PAD20, pady=PAD20)

        self.zone_comboboxes[zone_name] = building_area_combo
        # TODO: Apply numerical entry validation
        aggregated_zone_qty_spinbox = cw.IntSpinbox(self, width=125, default_value=1)
        aggregated_zone_qty_spinbox.grid(
            row=(i + 1), column=3, padx=PAD20, pady=PAD20, sticky="nsew"
        )
        measured_infiltration_rate_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        measured_infiltration_rate_checkbox.grid(
            row=(i + 1), column=4, padx=PAD20, pady=PAD20
        )
        image = ctk.CTkImage(
            light_image=Image.open("interface/static/white_plus.png"),
            dark_image=None,
            size=(20, 20),
        )
        add_child_space_button = ctk.CTkButton(
            self,
            text="",
            image=image,
            width=30,
            height=30,
            corner_radius=10,
            command=self.open_child_space_window,
        )
        add_child_space_button.grid(row=(i + 1), column=5, padx=PAD20, pady=PAD20)

        self.zone_widgets[zone_name] = [
            floor_label,
            building_area_combo,
            aggregated_zone_qty_spinbox,
            measured_infiltration_rate_checkbox,
            add_child_space_button,
        ]

    def get_zones_by_floors(self):
        for zone_name in self.main_app_data.rmds[0].zone_names:
            zone_obj = self.main_app_data.rmds[0].get_obj(zone_name)
            if self.zones_by_floor.get(zone_obj.floor_name):
                self.zones_by_floor[zone_obj.floor_name].append(zone_name)
            else:
                self.zones_by_floor[zone_obj.floor_name] = [zone_name]

    def set_default_value_by_floor(self, floor_name, selected_value):
        """Update all zones under a floor with the selected value from the floor's combobox"""
        for zone_name in self.main_app_data.rmds[0].zone_names:
            zone_obj = self.main_app_data.rmds[0].get_obj(zone_name)
            if zone_obj.floor_name == floor_name:
                if zone_name in self.zone_comboboxes:
                    self.zone_comboboxes[zone_name].set(selected_value)

    def toggle_zone_visibility(self, floor_name, button):
        """Toggles visibility of all zone rows under a given floor"""
        if floor_name in self.zones_by_floor:
            first_zone = self.zones_by_floor[floor_name][0]
            is_visible = self.zone_widgets[first_zone][
                0
            ].winfo_ismapped()  # Check if first zone widget is visible
            new_state = "hide" if is_visible else "show"

            for zone_name in self.zones_by_floor[floor_name]:
                if zone_name in self.zone_widgets:
                    for widget in self.zone_widgets[zone_name]:
                        if new_state == "hide":
                            widget.grid_remove()
                        else:
                            widget.grid()

            # Change button text accordingly
            button.configure(text="+" if new_state == "hide" else "−")

    def open_child_space_window(self):
        if (
            self.child_space_window is None
            or not self.child_space_window.winfo_exists()
        ):
            self.child_space_window = ChildSpaceWindow(self)
            self.child_space_window.after(10, self.child_space_window.lift)


# TODO: Implement child spaces window after spaces view
class ChildSpaceWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = ctk.CTkLabel(self, text="Child Spaces")
        self.label.pack(padx=20, pady=20)
