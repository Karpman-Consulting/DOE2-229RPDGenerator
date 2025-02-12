import customtkinter as ctk
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
            font=STANDARD_FONT,
        )
        self.directions_widget = ctk.CTkLabel(
            self.directions_frame,
            text=" Directions: Assign all Zones in your model to the Building Areas created on the previous tab. This can be done by Floor, or more granularly by Zone. If any zones in the model \n"
            " represent multiple zones in the design, provide the quantity of aggregated zones. If a zone's infiltration in the Proposed model is based on a measured infiltration rate, \n"
            " declare so here. If a zone contains more than 1 space, define additional spaces as necessary by clicking the quantity in the Child Spaces column to open the Child Spaces \n"
            " window. Child Spaces should be created as necessary to represent the entirety of the Zone, e.g. an aggregated zone that is in reality 3 zones where each zone has 2 spaces \n"
            " should have 6 Child Spaces total.",
            font=("Arial", 14),
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
        self.directions_label.grid(row=0, column=0)
        self.directions_widget.grid(row=0, column=1)

        # Subview frame
        self.view_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=PAD20)
        self.view_frame.grid_rowconfigure(0, weight=1)
        self.view_frame.grid_columnconfigure(0, weight=1)

        zones_view = ZonesSubview(self.view_frame)
        zones_view.grid(row=0, column=0, sticky="nsew")
        zones_view.open_view()

    @staticmethod
    def validate_entry(arg):
        if str.isdigit(arg) or arg == "":
            return True
        else:
            return False


class ZonesSubview(CTkXYFrame):
    def __init__(self, view_frame):
        super().__init__(view_frame)
        self.zones_view = view_frame.master
        self.main_app_data = self.zones_view.window.main_app.data
        self.is_view_populated = False
        self.validate_command = self.register(self.zones_view.validate_entry)
        self.child_space_window = None

    def __repr__(self):
        return "ZonesSubview"

    def open_view(self):
        self.populate_subview() if not self.is_view_populated else None

    def populate_subview(self):
        self.add_column_headers()

        # Key is floor name, value is list of zones on that floor
        zones_by_floors = {}
        for zone in self.main_app_data.rmds[0].zone_names:
            zone_obj = self.main_app_data.rmds[0].get_obj(zone)
            if zones_by_floors.get(zone_obj.floor_name):
                zones_by_floors[zone_obj.floor_name].append(zone)
            else:
                zones_by_floors[zone_obj.floor_name] = [zone]

        main_row = 0
        for floor, zones in zones_by_floors.items():
            self.add_main_row(main_row, floor)
            for i, zone in enumerate(zones):
                self.add_row((main_row + 1 + i), zone)
            main_row += len(zones)

        self.is_view_populated = True

    def add_column_headers(self):
        zone_floor_label = ctk.CTkLabel(self, text="Floor/Zone", font=STANDARD_FONT)
        zone_floor_label.grid(row=0, column=0, padx=PAD20, pady=5)
        building_area_label = ctk.CTkLabel(
            self, text="Building Area", font=STANDARD_FONT
        )
        building_area_label.grid(row=0, column=1, padx=PAD20, pady=5)
        aggregated_zone_quantity_label = ctk.CTkLabel(
            self, text="Aggregated Zone Qty", font=STANDARD_FONT
        )
        aggregated_zone_quantity_label.grid(row=0, column=2, padx=PAD20, pady=5)
        measured_infiltration_rate_label = ctk.CTkLabel(
            self, text="Measured Infiltration Rate?", font=STANDARD_FONT
        )
        measured_infiltration_rate_label.grid(row=0, column=3, padx=PAD20, pady=5)
        child_spaces_label = ctk.CTkLabel(self, text="Child Spaces", font=STANDARD_FONT)
        child_spaces_label.grid(row=0, column=4, padx=PAD20, pady=5)

    def add_main_row(self, i, floor_name):
        floor_label = ctk.CTkLabel(self, text=f"{floor_name}")
        floor_label.grid(row=(i + 1), column=0, padx=PAD20, pady=PAD20, sticky=W)
        building_area_combo = ctk.CTkComboBox(
            self,
            # TODO: Placeholder for Building Areas tab data
            values=["Building Area 1", "Placeholder"],
            state=READONLY,
        )
        building_area_combo._entry.configure(justify=LEFT)
        building_area_combo.grid(row=(i + 1), column=1, padx=PAD20, pady=PAD20)

    def add_row(self, i, floor_name):
        floor_label = ctk.CTkLabel(self, text=f"{floor_name}")
        floor_label.grid(row=(i + 1), column=0, padx=PAD20, pady=PAD20, sticky=W)
        building_area_combo = ctk.CTkComboBox(
            self,
            # TODO: Placeholder for Building Areas tab data
            values=["Building Area 1", "Placeholder"],
            state=READONLY,
        )
        building_area_combo._entry.configure(justify=LEFT)
        building_area_combo.grid(row=(i + 1), column=1, padx=PAD20, pady=PAD20)
        aggregated_zone_qty_input = ctk.CTkEntry(
            self,
            width=125,
            validate="all",
            validatecommand=(self.validate_command, "%P"),
        )
        aggregated_zone_qty_input.grid(row=(i + 1), column=2, padx=PAD20, pady=PAD20)
        measured_infiltration_rate_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        measured_infiltration_rate_checkbox.grid(
            row=(i + 1), column=3, padx=PAD20, pady=PAD20
        )
        image = ctk.CTkImage(
            light_image=Image.open("interface/assets/white_plus.png"),
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
        add_child_space_button.grid(row=(i + 1), column=4, padx=PAD20, pady=PAD20)

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
