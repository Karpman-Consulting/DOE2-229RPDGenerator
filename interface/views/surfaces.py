import customtkinter as ctk

from interface.base_view import BaseView


class SurfacesView(BaseView):
    def __init__(self, main):
        super().__init__(main)

        self.subviews = {
            "Exterior": self.ExteriorSurfaceView(self),
            "Interior": self.InteriorSurfaceView(self),
            "Underground": self.UndergroundSurfaceView(self),
            "Windows": self.WindowSurfaceView(self),
            "Skylights": self.SkylightSurfaceView(self),
            "Doors": self.DoorSurfaceView(self),
        }

        self.current_subview = None
        self.subview_buttons = {}

    def __repr__(self):
        return "SurfacesView"

    def open_view(self):
        self.toggle_active_button("Surfaces")

        directions_label = ctk.CTkLabel(
            self,
            text="Directions: ",
            anchor="e",
            justify="left",
            font=("Arial", 16, "bold"),
        )
        directions_text = " Assign the various data parameters for each surface."
        directions_widget = ctk.CTkLabel(
            self,
            text=directions_text,
            anchor="w",
            justify="left",
            font=("Arial", 14),
        )
        directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        directions_widget.grid(
            row=0, column=1, columnspan=8, sticky="new", padx=5, pady=20
        )

        self.create_subbutton_bar()

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
            # Create a frame for each button that will act as the border
            button_frame = ctk.CTkFrame(self, width=144, height=36, corner_radius=0)
            button_frame.grid(row=1, column=index, sticky="nsew")

            # Then create the button inside this frame
            button = ctk.CTkButton(
                button_frame,
                text=name,
                fg_color="#FFD966",
                hover_color="#FFD966",
                font=("Arial", 12),
                width=140,
                height=30,
                corner_radius=0,
                compound="left",
                command=callback_methods[name],
            )
            button.place(relx=0.5, rely=0.5, anchor="center")
            self.subview_buttons[name] = button

    def show_subview(self, subview_name):
        # Clear previous subview
        if self.current_subview is not None:
            self.current_subview.grid_forget()

        # Show new subview
        subview = self.subviews.get(subview_name)
        if subview:
            self.current_subview = subview
            self.current_subview.grid(row=1, column=0, columnspan=9, sticky="nsew")
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

    class ExteriorSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "ExteriorSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Exterior")

    class InteriorSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "InteriorSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Interior")

    class UndergroundSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "UndergroundSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Underground")

    class WindowSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "WindowSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Windows")

    class SkylightSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "SkylightSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Skylights")

    class DoorSurfaceView(ctk.CTkFrame):
        def __init__(self, main):
            super().__init__(main)
            self.main = main

        def __repr__(self):
            return "DoorSurfaceView"

        def open_subview(self):
            self.main.toggle_active_subbutton("Doors")
