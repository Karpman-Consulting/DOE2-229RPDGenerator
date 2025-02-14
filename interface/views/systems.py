import customtkinter as ctk
import interface.custom_widgets as cw

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


ARIAL_16_BOLD = ("Arial", 16, "bold")
READONLY = "readonly"
W = "w"
LEFT = "left"
PAD20 = (0, 20)


class SystemsView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        # All subviews will be placed inside this frame. Single row/column allows formatting of subview to be handled by the subview itself
        self.subview_frame = ctk.CTkFrame(self)
        self.current_subview = None

        self.subviews = {
            "Heat Rejection": HeatRejectionView(self.subview_frame),
            "HVAC Systems": HVACSystemView(self.subview_frame),
            "Zonal Exhaust": ZonalExhaustView(self.subview_frame),
        }

        # Directions frame holds all directions info and will get 'gridded' within the surfaces view grid
        self.directions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.directions_label = ctk.CTkLabel(
            self.directions_frame,
            text="Directions: ",
            font=ARIAL_16_BOLD,
        )
        self.directions_widget = ctk.CTkLabel(
            self.directions_frame,
            text=" Assign the various data parameters for each surface.",
            font=("Arial", 14),
        )

        self.subview_buttons = {}
        self.subview_button_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.create_subbutton_bar()

    def __repr__(self):
        return "SystemsView"

    def open_view(self):
        self.toggle_active_button("Systems")
        self.grid_propagate(False)

        # 3 rows in the main surface view structure. Subview frame (row 3, index 2) has a weight to make it fill up the empty space in the window
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Directions
        self.directions_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        self.directions_label.grid(row=0, column=0)
        self.directions_widget.grid(row=0, column=1)

        # Subview buttons
        self.subview_button_frame.grid(row=1, column=0, sticky=W, padx=20)
        for index, name in enumerate(self.subview_buttons):
            # Layout the button inside the frame
            button = self.subview_buttons[name]
            button.grid(row=0, column=index, padx=(0, 4))

        # Subview frame
        self.subview_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=PAD20)
        self.subview_frame.grid_rowconfigure(0, weight=1)
        self.subview_frame.grid_columnconfigure(0, weight=1)

    def create_subbutton_bar(self):
        # TODO: Check for empty subviews
        if not self.window.main_app.data.is_all_new_construction():
            callback_methods = {
                "Heat Rejection": lambda: self.show_subview("Heat Rejection"),
                "HVAC Systems": lambda: self.show_subview("HVAC Systems"),
                "Zonal Exhaust": lambda: self.show_subview("Zonal Exhaust"),
            }
        else:
            callback_methods = {
                "Heat Rejection": lambda: self.show_subview("Heat Rejection"),
                "HVAC Systems": lambda: self.show_subview("HVAC Systems"),
            }

        for name in callback_methods:
            # Create the button to go inside this button frame
            button = ctk.CTkButton(
                self.subview_button_frame,
                text=name,
                fg_color="#FFD966",
                hover_color="#FFD966",
                text_color="black",
                font=("Arial", 12, "bold"),
                width=140,
                height=30,
                corner_radius=0,
                compound=LEFT,
                command=callback_methods[name],
            )
            self.subview_buttons[name] = button

    def show_subview(self, subview_name):
        # Clear previous subview
        if self.current_subview is not None:
            self.current_subview.grid_forget()

        # Show new subview
        subview = self.subviews.get(subview_name)
        if subview:
            self.current_subview = subview
            self.current_subview.grid(row=0, column=0, sticky="nsew")
            self.current_subview.open_subview()

    def toggle_active_subbutton(self, active_subbutton_name):
        for name, button in self.subview_buttons.items():
            if name == active_subbutton_name:
                self.subview_buttons[name].configure(
                    fg_color="#FFED67",
                    hover_color="#FFED67",
                    text_color="black",
                    font=("Arial", 11, "bold"),
                )
            else:
                self.subview_buttons[name].configure(
                    fg_color="#FFD966",
                    hover_color="#FFD966",
                    text_color="black",
                    font=("Arial", 11, "bold"),
                )


class HeatRejectionView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.systems_view = subview_frame.master
        self.main_app_data = self.systems_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "HeatRejectionView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("Heat Rejection")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        if len(self.main_app_data.rmds[0].heat_rejection_names) == 0:
            # TODO: No heat rejection data, hide tab
            return

        for i, heat_rejection_name in enumerate(
            self.main_app_data.rmds[0].heat_rejection_names
        ):
            self.add_row(i, heat_rejection_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=ARIAL_16_BOLD)
        name_label.grid(row=0, column=0, padx=PAD20, pady=5)
        fan_type_label = ctk.CTkLabel(self, text="Fan Type", font=ARIAL_16_BOLD)
        fan_type_label.grid(row=0, column=1, padx=PAD20, pady=5)

    def add_row(self, i, heat_rejection_name):
        heat_rejection_label = ctk.CTkLabel(self, text=f"{heat_rejection_name}")
        heat_rejection_label.grid(
            row=(i + 1), column=0, padx=PAD20, pady=PAD20, sticky=W
        )
        fan_type_combo = ctk.CTkComboBox(
            self, values=["Axial", "Centrifugal"], state=READONLY
        )
        fan_type_combo._entry.configure(justify=LEFT)
        fan_type_combo.grid(row=(i + 1), column=1, padx=PAD20, pady=PAD20)


class HVACSystemView(ctk.CTkFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.systems_view = subview_frame.master
        self.main_app_data = self.systems_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "HVACSystemView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("HVAC Systems")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, hvac_system_name in enumerate(self.main_app_data.rmds[0].system_names):
            self.add_row(i, hvac_system_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=ARIAL_16_BOLD)
        name_label.grid(row=0, column=0, padx=PAD20, pady=5)
        if not self.main_app_data.is_all_new_construction():
            status_label = ctk.CTkLabel(self, text="Status", font=ARIAL_16_BOLD)
            status_label.grid(row=0, column=1, padx=PAD20, pady=5)
        dehumidification_type_label = ctk.CTkLabel(
            self, text="Dehumidification Type", font=ARIAL_16_BOLD
        )
        dehumidification_type_label.grid(row=0, column=2, padx=PAD20, pady=5)
        ducted_supply_label = ctk.CTkLabel(
            self, text="Ducted Supply?", font=ARIAL_16_BOLD
        )
        ducted_supply_label.grid(row=0, column=3, padx=PAD20, pady=5)
        air_filter_merv_rating_label = ctk.CTkLabel(
            self, text="Air Filter MERV Rating", font=ARIAL_16_BOLD
        )
        air_filter_merv_rating_label.grid(row=0, column=4, padx=PAD20, pady=5)

    def add_row(self, i, hvac_system_name):
        system_label = ctk.CTkLabel(self, text=f"{hvac_system_name}")
        system_label.grid(row=(i + 1), column=0, padx=PAD20, pady=PAD20, sticky=W)
        if not self.main_app_data.is_all_new_construction():
            status_combo = ctk.CTkComboBox(
                self,
                values=self.main_app_data.StatusDescriptions.get_list(),
                state=READONLY,
            )
            status_combo._entry.configure(justify=LEFT)
            status_combo.grid(row=(i + 1), column=1, padx=PAD20, pady=PAD20)
        dehumidification_type_combo = ctk.CTkComboBox(
            self,
            values=self.main_app_data.DehumidificationDescriptions.get_list(),
            state=READONLY,
        )
        dehumidification_type_combo._entry.configure(justify=LEFT)
        dehumidification_type_combo.grid(row=(i + 1), column=2, padx=PAD20, pady=PAD20)
        ducted_supply_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        ducted_supply_checkbox.grid(row=(i + 1), column=3, padx=PAD20, pady=PAD20)
        air_filter_merv_rating_spinbox = cw.IntSpinbox(
            self, width=125, minimum_value=1, maximum_value=16, default_value=8
        )
        air_filter_merv_rating_spinbox.grid(
            row=(i + 1), column=4, padx=PAD20, pady=PAD20
        )


class ZonalExhaustView(ctk.CTkFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.systems_view = subview_frame.master
        self.main_app_data = self.systems_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "ZonalExhaustView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("Zonal Exhaust")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        zonal_exhaust_fans = self.get_zonal_exhaust_fans()

        if len(zonal_exhaust_fans) == 0:
            # TODO: No zonal exhaust fans, hide tab
            return

        self.add_column_headers()

        for i, exhaust_fan_dict in enumerate(zonal_exhaust_fans):
            self.add_row(i, exhaust_fan_dict)

        self.is_subview_populated = True

    def get_zonal_exhaust_fans(self):
        # TODO: Review this approach..may be problematic once we are trying to set data back to the rmds
        zonal_exhaust_fans = []
        for zone_name in self.main_app_data.rmds[0].zone_names:
            zone_obj = self.main_app_data.rmds[0].get_obj(zone_name)
            if zone_obj.zonal_exhaust_fan:
                zonal_exhaust_fans.append(zone_obj.zonal_exhaust_fan)
        return zonal_exhaust_fans

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=ARIAL_16_BOLD)
        name_label.grid(row=0, column=0, padx=PAD20, pady=5)
        status_label = ctk.CTkLabel(self, text="Fan Type", font=ARIAL_16_BOLD)
        status_label.grid(row=0, column=1, padx=PAD20, pady=5)

    def add_row(self, i, exhaust_fan_dict):
        zonal_exhaust_fan_label = ctk.CTkLabel(self, text=f"{exhaust_fan_dict['id']}")
        zonal_exhaust_fan_label.grid(
            row=(i + 1), column=0, padx=PAD20, pady=PAD20, sticky=W
        )
        status_combo = ctk.CTkComboBox(
            self,
            values=self.main_app_data.StatusDescriptions.get_list(),
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=PAD20, pady=PAD20)
