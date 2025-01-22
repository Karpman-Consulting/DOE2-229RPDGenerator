import customtkinter as ctk

from interface.CTkXYFrame import CTkXYFrame
from interface.base_view import BaseView


class SurfacesView(BaseView):
    def __init__(self, main):
        super().__init__(main)

        self.subviews = {
            "Exterior": ExteriorSurfaceView(self),
            "Interior": InteriorSurfaceView(self),
            "Underground": UndergroundSurfaceView(self),
            "Windows": WindowSurfaceView(self),
            "Skylights": SkylightSurfaceView(self),
            "Doors": DoorSurfaceView(self),
        }

        self.current_subview = None
        self.subview_buttons = {}
        self.subview_button_frame = ctk.CTkFrame(self, corner_radius=0)

        self.directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )
        self.directions_widget = ctk.CTkLabel(
            self,
            text=" Assign the various data parameters for each surface.",
            anchor="w",
            justify="left",
            font=("Arial", 14),
        )
        self.create_subbutton_bar()

        # # Makes subview frame fill the window.
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_columnconfigure(0, weight=1)

    def __repr__(self):
        return "SurfacesView"

    def open_view(self):
        self.toggle_active_button("Surfaces")
        self.grid_propagate(False)

        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        self.directions_widget.grid(
            row=0, column=1, columnspan=5, sticky="new", padx=5, pady=20
        )

        self.subview_button_frame.grid(row=1, column=0, columnspan=6, sticky="nsew")

        for index, name in enumerate(self.subview_buttons):
            # Layout the button inside the frame
            button = self.subview_buttons[name]
            button.grid(row=0, column=index)

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
                font=("Arial", 11),
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
            self.current_subview.grid(row=2, column=0, columnspan=9, sticky="nsew")
            self.current_subview.open_subview()

    def toggle_active_subbutton(self, active_subbutton_name):
        for name, button in self.subview_buttons.items():
            if name == active_subbutton_name:
                self.subview_buttons[name].configure(
                    fg_color="#FFED67",
                    hover_color="#FFED67",
                    text_color="black",
                    font=("Arial", 12, "bold"),
                )
            else:
                self.subview_buttons[name].configure(
                    fg_color="#FFD966",
                    hover_color="#FFD966",
                    text_color="black",
                    font=("Arial", 12, "bold"),
                )

    def dummy_fill(self, subview_frame):
        for i in range(10):
            for j in range(10):
                label = ctk.CTkButton(subview_frame, text=f"Row {i}, Column {j}")
                label.grid(row=i, column=j, padx=20, pady=10)


class ExteriorSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        """Here we can add however many widgets in grid form like normal. The scroll bars will appear when the
         widgets exceed the frame size. Calling this 'dummy fill' method just to show scrolling works"""
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "ExteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Exterior")


class InteriorSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "InteriorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Interior")


class UndergroundSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "UndergroundSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Underground")


class WindowSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "WindowSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Windows")


class SkylightSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "SkylightSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Skylights")


class DoorSurfaceView(CTkXYFrame):
    def __init__(self, master):
        super().__init__(master)
        self.surfaces_view = master
        self.surfaces_view.dummy_fill(self)

    def __repr__(self):
        return "DoorSurfaceView"

    def open_subview(self):
        self.surfaces_view.toggle_active_subbutton("Doors")
