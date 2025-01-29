import customtkinter as ctk

from interface.CTkXYFrame import CTkXYFrame
from interface.base_view import BaseView


class SurfacesView(BaseView):
    def __init__(self, main):
        super().__init__(main)

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
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.main_app_data = self.surfaces_view.master.app_data
        self.is_subview_populated = False

    def __repr__(self):
        return "ExteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Exterior")
        self.populate_subview() if not self.is_subview_populated else None

    # Example of how to pull rmd data from main app
    def populate_subview(self):
        ext_walls = self.main_app_data.rmds[0].ext_wall_names

        # TODO: Align surface names to left side of column
        for i in range(len(ext_walls)):
            surface_label = ctk.CTkLabel(self, text=f"{ext_walls[i]}")
            surface_label.grid(row=i, column=0, padx=(0, 20), pady=(0, 20))
            status_combo = ctk.CTkComboBox(self, values=["Value 1", "Value 2"])
            status_combo.grid(row=i, column=1, padx=(0, 20), pady=(0, 20))

        self.is_subview_populated = True


class InteriorSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.subview_label = ctk.CTkLabel(self, text="Interior Surface Subview")
        self.subview_label.grid()

    def __repr__(self):
        return "InteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Interior")


class UndergroundSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.subview_label = ctk.CTkLabel(self, text="Underground Surface Subview")
        self.subview_label.grid()

    def __repr__(self):
        return "UndergroundSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Underground")


class WindowSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.subview_label = ctk.CTkLabel(self, text="Window Surface Subview")
        self.subview_label.grid()

    def __repr__(self):
        return "WindowSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Windows")


class SkylightSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.subview_label = ctk.CTkLabel(self, text="Skylight Surface Subview")
        self.subview_label.grid()

    def __repr__(self):
        return "SkylightSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Skylights")


class DoorSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master.master
        self.subview_label = ctk.CTkLabel(self, text="Door Surface Subview")
        self.subview_label.grid()

    def __repr__(self):
        return "DoorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Doors")
