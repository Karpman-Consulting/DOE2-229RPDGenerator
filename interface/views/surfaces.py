import customtkinter as ctk

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


STANDARD_FONT = ("Arial", 16, "bold")
READONLY = "readonly"
LEFT = "left"
W = "w"


class SurfacesView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        """All subviews will be placed inside this frame. Single row/column allows formatting of subview to be
        handled by the subview itself"""
        self.subview_frame = ctk.CTkFrame(self)
        self.current_subview = None

        self.subviews = {
            "Exterior": ExteriorSurfaceView(self.subview_frame),
            "Interior": InteriorSurfaceView(self.subview_frame),
            "Underground": UndergroundSurfaceView(self.subview_frame),
            "Windows": WindowSurfaceView(self.subview_frame),
            "Skylights": SkylightSurfaceView(self.subview_frame),
            "Doors": DoorSurfaceView(self.subview_frame),
        }

        """Directions frame holds all directions info and will get 'gridded' within the surfaces view grid"""
        self.directions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.directions_label = ctk.CTkLabel(
            self.directions_frame,
            text="Directions: ",
            font=STANDARD_FONT,
        )
        self.directions_widget = ctk.CTkLabel(
            self.directions_frame,
            text=" Assign the various data parameters for each surface.",
            font=("Arial", 14),
        )

        # Subview buttons
        self.subview_buttons = {}
        self.subview_button_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.create_subbutton_bar()

    def __repr__(self):
        return "SurfacesView"

    def open_view(self):
        self.toggle_active_button("Surfaces")
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
        self.subview_button_frame.grid(row=1, column=0, sticky=W, padx=20)
        for index, name in enumerate(self.subview_buttons):
            # Layout the button inside the frame
            button = self.subview_buttons[name]
            button.grid(row=0, column=index, padx=(0, 4))

        # Subview frame
        self.subview_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.subview_frame.grid_rowconfigure(0, weight=1)
        self.subview_frame.grid_columnconfigure(0, weight=1)

        if self.subview_buttons:
            # Open the first subview available
            self.show_subview(next(iter(self.subview_buttons)))

    def create_subbutton_bar(self):
        callback_methods = {}
        if not self.app_data.is_all_new_construction:
            if len(self.app_data.rmds[0].ext_wall_names) > 0:
                callback_methods["Exterior"] = lambda: self.show_subview("Exterior")
            if len(self.app_data.rmds[0].int_wall_names) > 0:
                callback_methods["Interior"] = lambda: self.show_subview("Interior")
            if len(self.app_data.rmds[0].undg_wall_names) > 0:
                callback_methods["Underground"] = lambda: self.show_subview(
                    "Underground"
                )
        if len(self.app_data.rmds[0].door_names) > 0:
            callback_methods["Doors"] = lambda: self.show_subview("Doors")
        if len(self.app_data.rmds[0].window_names) > 0:
            callback_methods["Windows"] = lambda: self.show_subview("Windows")
        if len(self.app_data.rmds[0].skylight_names) > 0:
            callback_methods["Skylights"] = lambda: self.show_subview("Skylights")

        for index, name in enumerate(callback_methods):
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
                )
            else:
                self.subview_buttons[name].configure(
                    fg_color="#FFD966",
                    hover_color="#FFD966",
                    text_color="black",
                )


class ExteriorSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "ExteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Exterior")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, ext_wall_name in enumerate(self.app_data.rmds[0].ext_wall_names):
            self.add_row(i, ext_wall_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)

    def add_row(self, i, ext_wall_name):
        surface_label = ctk.CTkLabel(self, text=f"{ext_wall_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))


class InteriorSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "InteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Interior")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, int_wall_name in enumerate(self.app_data.rmds[0].int_wall_names):
            self.add_row(i, int_wall_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)

    def add_row(self, i, int_wall_name):
        surface_label = ctk.CTkLabel(self, text=f"{int_wall_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))


class UndergroundSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "UndergroundSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Underground")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, undg_wall_name in enumerate(self.app_data.rmds[0].undg_wall_names):
            self.add_row(i, undg_wall_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)

    def add_row(self, i, undg_wall_name):
        surface_label = ctk.CTkLabel(self, text=f"{undg_wall_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))


class WindowSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "WindowSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Windows")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, window_name in enumerate(self.app_data.rmds[0].window_names):
            self.add_row(i, window_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=STANDARD_FONT
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        framing_type_label = ctk.CTkLabel(self, text="Framing Type", font=STANDARD_FONT)
        framing_type_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        operable_label = ctk.CTkLabel(self, text="Operable?", font=STANDARD_FONT)
        operable_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        open_sensor_label = ctk.CTkLabel(self, text="Open Sensor?", font=STANDARD_FONT)
        open_sensor_label.grid(row=0, column=5, padx=(0, 20), pady=5)
        manual_interior_shades_label = ctk.CTkLabel(
            self, text="Manual Interior Shades?", font=STANDARD_FONT
        )
        manual_interior_shades_label.grid(row=0, column=6, padx=(0, 20), pady=5)

    def add_row(self, i, window_name):
        surface_label = ctk.CTkLabel(self, text=f"{window_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
        classification_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.SubsurfaceSubclassificationDescriptions2019ASHRAE901,
            state=READONLY,
        )
        classification_combo._entry.configure(justify=LEFT)
        classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))
        framing_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.SubsurfaceSubclassificationDescriptions2019ASHRAE901,
            state=READONLY,
        )
        framing_type_combo._entry.configure(justify=LEFT)
        framing_type_combo.grid(row=(i + 1), column=3, padx=(0, 20), pady=(0, 20))
        operable_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        operable_checkbox.grid(row=(i + 1), column=4, padx=(0, 20), pady=(0, 20))
        open_sensor_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        open_sensor_checkbox.grid(row=(i + 1), column=5, padx=(0, 20), pady=(0, 20))
        manual_interior_shades_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        manual_interior_shades_checkbox.grid(
            row=(i + 1), column=6, padx=(0, 20), pady=(0, 20)
        )


class SkylightSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "SkylightSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Skylights")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, skylight_name in enumerate(self.app_data.rmds[0].skylight_names):
            self.add_row(i, skylight_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=STANDARD_FONT
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        framing_type_label = ctk.CTkLabel(self, text="Framing Type", font=STANDARD_FONT)
        framing_type_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        operable_label = ctk.CTkLabel(self, text="Operable?", font=STANDARD_FONT)
        operable_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        open_sensor_label = ctk.CTkLabel(self, text="Open Sensor?", font=STANDARD_FONT)
        open_sensor_label.grid(row=0, column=5, padx=(0, 20), pady=5)
        manual_interior_shades_label = ctk.CTkLabel(
            self, text="Manual Interior Shades?", font=STANDARD_FONT
        )
        manual_interior_shades_label.grid(row=0, column=6, padx=(0, 20), pady=5)

    def add_row(self, i, skylight_name):
        surface_label = ctk.CTkLabel(self, text=f"{skylight_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
        classification_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.SubsurfaceSubclassificationDescriptions2019ASHRAE901,
            state=READONLY,
        )
        classification_combo._entry.configure(justify=LEFT)
        classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))
        framing_type_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.SubsurfaceFrameDescriptions2019ASHRAE901,
            state=READONLY,
        )
        framing_type_combo._entry.configure(justify=LEFT)
        framing_type_combo.grid(row=(i + 1), column=3, padx=(0, 20), pady=(0, 20))
        operable_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        operable_checkbox.grid(row=(i + 1), column=4, padx=(0, 20), pady=(0, 20))
        open_sensor_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        open_sensor_checkbox.grid(row=(i + 1), column=5, padx=(0, 20), pady=(0, 20))
        manual_interior_shades_checkbox = ctk.CTkCheckBox(self, text="", width=30)
        manual_interior_shades_checkbox.grid(
            row=(i + 1), column=6, padx=(0, 20), pady=(0, 20)
        )


class DoorSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "DoorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Doors")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        self.add_column_headers()

        for i, door_name in enumerate(self.app_data.rmds[0].door_names):
            self.add_row(i, door_name)

        self.is_subview_populated = True

    def add_column_headers(self):
        name_label = ctk.CTkLabel(self, text="Name", font=STANDARD_FONT)
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=STANDARD_FONT)
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=STANDARD_FONT
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)

    def add_row(self, i, door_name):
        surface_label = ctk.CTkLabel(self, text=f"{door_name}")
        surface_label.grid(row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky=W)
        status_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.StatusDescriptions,
            state=READONLY,
        )
        status_combo._entry.configure(justify=LEFT)
        status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
        classification_combo = ctk.CTkComboBox(
            self,
            values=self.app_data.SubsurfaceSubclassificationDescriptions2019ASHRAE901,
            state=READONLY,
        )
        classification_combo._entry.configure(justify=LEFT)
        classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))
