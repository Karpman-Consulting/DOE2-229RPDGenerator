import customtkinter as ctk

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


class SystemsView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        """All subviews will be placed inside this frame. Single row/column allows formatting of subview to be
        handled by the subview itself"""
        self.subview_frame = ctk.CTkFrame(self)
        self.current_subview = None

        self.subviews = {
            "Heat Rejection": HeatRejectionView(self.subview_frame),
            "HVAC Systems": HVACSystemView(self.subview_frame),
            "Zonal Exhaust": ZonalExhaustView(self.subview_frame),
        }

        """Directions frame holds all directions info and will get 'gridded' within the surfaces view grid"""
        self.directions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.directions_label = ctk.CTkLabel(
            self.directions_frame,
            text="Directions: ",
            font=("Arial", 16, "bold"),
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

        """3 rows in the main surface view structure. Subview frame (row 3, index 2) has a weight to make it fill up
        the empty space in the window"""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Directions
        self.directions_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        self.directions_label.grid(row=0, column=0)
        self.directions_widget.grid(row=0, column=1)

        # Subview buttons
        self.subview_button_frame.grid(row=1, column=0, sticky="w", padx=20)
        for index, name in enumerate(self.subview_buttons):
            # Layout the button inside the frame
            button = self.subview_buttons[name]
            button.grid(row=0, column=index, padx=(0, 4))

        # Subview frame
        self.subview_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
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
                compound="left",
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

    def validate_entry(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False


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
        heat_rejections = self.main_app_data.rmds[0].heat_rejection_names
        if len(heat_rejections) == 0:
            # TODO: No heat rejection data, hide tab
            return
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        fan_type_label = ctk.CTkLabel(self, text="Fan Type", font=("Arial", 16, "bold"))
        fan_type_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        for i, heat_rejection in enumerate(heat_rejections):
            heat_rejection_label = ctk.CTkLabel(self, text=f"{heat_rejection}")
            heat_rejection_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            fan_type_combo = ctk.CTkComboBox(
                self, values=["Axial", "Centrifugal"], state="readonly"
            )
            fan_type_combo._entry.configure(justify="left")
            fan_type_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True


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
        systems = self.main_app_data.rmds[0].system_names
        validate_command = self.register(self.systems_view.validate_entry)
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        if not self.main_app_data.is_all_new_construction():
            status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
            status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        dehumidification_type_label = ctk.CTkLabel(
            self, text="Dehumidification Type", font=("Arial", 16, "bold")
        )
        dehumidification_type_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        ducted_supply_label = ctk.CTkLabel(
            self, text="Ducted Supply?", font=("Arial", 16, "bold")
        )
        ducted_supply_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        air_filter_merv_rating_label = ctk.CTkLabel(
            self, text="Air Filter MERV Rating", font=("Arial", 16, "bold")
        )
        air_filter_merv_rating_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        for i, system in enumerate(systems):
            system_label = ctk.CTkLabel(self, text=f"{system}")
            system_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            if not self.main_app_data.is_all_new_construction():
                status_combo = ctk.CTkComboBox(
                    self, values=["Existing", "New"], state="readonly"
                )
                status_combo._entry.configure(justify="left")
                status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
            dehumidification_type_combo = ctk.CTkComboBox(
                self, values=["Desiccant", "Mechanical Cooling"], state="readonly"
            )
            dehumidification_type_combo._entry.configure(justify="left")
            dehumidification_type_combo.grid(
                row=(i + 1), column=2, padx=(0, 20), pady=(0, 20)
            )
            ducted_supply_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            ducted_supply_checkbox.grid(
                row=(i + 1), column=3, padx=(0, 20), pady=(0, 20)
            )
            air_filter_merv_rating_input = ctk.CTkEntry(
                self,
                width=125,
                validate="all",
                validatecommand=(validate_command, "%P"),
            )
            air_filter_merv_rating_input.grid(
                row=(i + 1), column=4, padx=(0, 20), pady=(0, 20)
            )

        self.is_subview_populated = True


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
        zones = self.main_app_data.rmds[0].zone_names
        zonal_exhaust_fans = {}

        # Capture existing zonal exhaust fan data
        for zone in zones:
            zone_obj = self.main_app_data.rmds[0].get_obj(zone)
            if zone_obj and len(zone_obj.zonal_exhaust_fan) > 0:
                zonal_exhaust_fans.update(zone_obj.zonal_exhaust_fan)

        if len(zonal_exhaust_fans) == 0:
            # TODO: No zonal exhaust fans, hide tab
            return

        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Fan Type", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        for i, zone in enumerate(zones):
            heat_rejection_label = ctk.CTkLabel(self, text=f"{zone}")
            heat_rejection_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Axial", "Centrifugal"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True
