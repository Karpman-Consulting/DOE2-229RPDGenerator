import customtkinter as ctk

from interface.ctk_xyframe import CTkXYFrame
from interface.base_view import BaseView


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
            font=("Arial", 16, "bold"),
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
        callback_methods = {
            "Exterior": lambda: self.show_subview("Exterior"),
            "Interior": lambda: self.show_subview("Interior"),
            "Underground": lambda: self.show_subview("Underground"),
            "Windows": lambda: self.show_subview("Windows"),
            "Skylights": lambda: self.show_subview("Skylights"),
            "Doors": lambda: self.show_subview("Doors"),
        }

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
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "ExteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Exterior")
        self.populate_subview() if not self.is_subview_populated else None

    # Example of how to pull rmd data from main app
    def populate_subview(self):
        ext_walls = self.main_app_data.rmds[0].ext_wall_names
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        for i, ext_wall in enumerate(ext_walls):
            surface_label = ctk.CTkLabel(self, text=f"{ext_wall}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Value 1", "Value 2"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True


class InteriorSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "InteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Interior")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        int_walls = self.main_app_data.rmds[0].int_wall_names
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        for i, int_wall in enumerate(int_walls):
            surface_label = ctk.CTkLabel(self, text=f"{int_wall}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Existing", "New"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True


class UndergroundSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "UndergroundSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Underground")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        undg_walls = self.main_app_data.rmds[0].undg_wall_names
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        for i, undg_wall in enumerate(undg_walls):
            surface_label = ctk.CTkLabel(self, text=f"{undg_wall}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Existing", "New"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True


class WindowSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "WindowSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Windows")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        windows = self.main_app_data.rmds[0].window_names
        skylights = []

        # Remove skylights from windows list
        for window in windows:
            window_obj = self.main_app_data.rmds[0].get_obj(window)
            if window_obj and window_obj.classification == "Skylight":
                skylights.append(window)
        # TODO: List comprehension seemed like the best choice here. Please correct if not ideal
        windows = [window for window in windows if window not in skylights]

        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=("Arial", 16, "bold")
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        framing_type_label = ctk.CTkLabel(
            self, text="Framing Type", font=("Arial", 16, "bold")
        )
        framing_type_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        operable_label = ctk.CTkLabel(
            self, text="Operable?", font=("Arial", 16, "bold")
        )
        operable_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        open_sensor_label = ctk.CTkLabel(
            self, text="Open Sensor?", font=("Arial", 16, "bold")
        )
        open_sensor_label.grid(row=0, column=5, padx=(0, 20), pady=5)
        manual_interior_shades_label = ctk.CTkLabel(
            self, text="Manual Interior Shades?", font=("Arial", 16, "bold")
        )
        manual_interior_shades_label.grid(row=0, column=6, padx=(0, 20), pady=5)
        for i, window in enumerate(windows):
            surface_label = ctk.CTkLabel(self, text=f"{window}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Existing", "New"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
            classification_combo = ctk.CTkComboBox(
                self, values=["Spandrel", "Other", "Glass Block"], state="readonly"
            )
            classification_combo._entry.configure(justify="left")
            classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))
            framing_type_combo = ctk.CTkComboBox(
                self, values=["Metal", "Wood", "Vinyl", "Other"], state="readonly"
            )
            framing_type_combo._entry.configure(justify="left")
            framing_type_combo.grid(row=(i + 1), column=3, padx=(0, 20), pady=(0, 20))
            operable_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            operable_checkbox.grid(row=(i + 1), column=4, padx=(0, 20), pady=(0, 20))
            open_sensor_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            open_sensor_checkbox.grid(row=(i + 1), column=5, padx=(0, 20), pady=(0, 20))
            manual_interior_shades_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            manual_interior_shades_checkbox.grid(
                row=(i + 1), column=6, padx=(0, 20), pady=(0, 20)
            )

        self.is_subview_populated = True


class SkylightSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "SkylightSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Skylights")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        windows = self.main_app_data.rmds[0].window_names
        skylights = []

        # Get only skylights in the current list of windows
        for window in windows:
            window_obj = self.main_app_data.rmds[0].get_obj(window)
            if window_obj and window_obj.classification == "Skylight":
                skylights.append(window)
        if not skylights:
            return

        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=("Arial", 16, "bold")
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        framing_type_label = ctk.CTkLabel(
            self, text="Framing Type", font=("Arial", 16, "bold")
        )
        framing_type_label.grid(row=0, column=3, padx=(0, 20), pady=5)
        operable_label = ctk.CTkLabel(
            self, text="Operable?", font=("Arial", 16, "bold")
        )
        operable_label.grid(row=0, column=4, padx=(0, 20), pady=5)
        open_sensor_label = ctk.CTkLabel(
            self, text="Open Sensor?", font=("Arial", 16, "bold")
        )
        open_sensor_label.grid(row=0, column=5, padx=(0, 20), pady=5)
        manual_interior_shades_label = ctk.CTkLabel(
            self, text="Manual Interior Shades?", font=("Arial", 16, "bold")
        )
        manual_interior_shades_label.grid(row=0, column=6, padx=(0, 20), pady=5)
        for i, window in enumerate(windows):
            surface_label = ctk.CTkLabel(self, text=f"{window}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Existing", "New"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
            classification_combo = ctk.CTkComboBox(
                self, values=["Spandrel", "Other", "Glass Block"], state="readonly"
            )
            classification_combo._entry.configure(justify="left")
            classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))
            framing_type_combo = ctk.CTkComboBox(
                self, values=["Metal", "Wood", "Vinyl", "Other"], state="readonly"
            )
            framing_type_combo._entry.configure(justify="left")
            framing_type_combo.grid(row=(i + 1), column=3, padx=(0, 20), pady=(0, 20))
            operable_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            operable_checkbox.grid(row=(i + 1), column=4, padx=(0, 20), pady=(0, 20))
            open_sensor_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            open_sensor_checkbox.grid(row=(i + 1), column=5, padx=(0, 20), pady=(0, 20))
            manual_interior_shades_checkbox = ctk.CTkCheckBox(self, text="", width=30)
            manual_interior_shades_checkbox.grid(
                row=(i + 1), column=6, padx=(0, 20), pady=(0, 20)
            )

        self.is_subview_populated = True


class DoorSurfaceView(CTkXYFrame):
    def __init__(self, subview_frame):
        super().__init__(subview_frame)
        self.surfaces_view = subview_frame.master
        self.main_app_data = self.surfaces_view.window.main_app.data
        self.is_subview_populated = False

    def __repr__(self):
        return "DoorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Doors")
        self.populate_subview() if not self.is_subview_populated else None

    def populate_subview(self):
        doors = self.main_app_data.rmds[0].door_names
        name_label = ctk.CTkLabel(self, text="Name", font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=0, padx=(0, 20), pady=5)
        status_label = ctk.CTkLabel(self, text="Status", font=("Arial", 16, "bold"))
        status_label.grid(row=0, column=1, padx=(0, 20), pady=5)
        classification_label = ctk.CTkLabel(
            self, text="Classification", font=("Arial", 16, "bold")
        )
        classification_label.grid(row=0, column=2, padx=(0, 20), pady=5)
        for i, door in enumerate(doors):
            surface_label = ctk.CTkLabel(self, text=f"{door}")
            surface_label.grid(
                row=(i + 1), column=0, padx=(0, 20), pady=(0, 20), sticky="w"
            )
            status_combo = ctk.CTkComboBox(
                self, values=["Existing", "New"], state="readonly"
            )
            status_combo._entry.configure(justify="left")
            status_combo.grid(row=(i + 1), column=1, padx=(0, 20), pady=(0, 20))
            classification_combo = ctk.CTkComboBox(
                self, values=["Swinging", "Non-swinging", "Other"], state="readonly"
            )
            classification_combo._entry.configure(justify="left")
            classification_combo.grid(row=(i + 1), column=2, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True
