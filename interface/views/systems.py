import customtkinter as ctk

from interface.base_view import BaseView


class SystemsView(BaseView):
    def __init__(self, main):
        super().__init__(main)

        self.subviews = {
            "Heat Rejection": HeatRejectionView(self),
            "HVAC Systems": HVACSystemView(self),
            "Zonal Exhaust": ZonalExhaustView(self),
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
            text=" Assign the various data parameters for each system.",
            anchor="w",
            justify="left",
            font=("Arial", 14),
        )

        for col in range(3):
            self.columnconfigure(col, weight=0)

        self.create_subbutton_bar()

    def __repr__(self):
        return "SystemsView"

    def open_view(self):
        self.toggle_active_button("Systems")
        self.grid_propagate(False)

        self.directions_label.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
        self.directions_widget.grid(
            row=0, column=1, columnspan=8, sticky="new", padx=5, pady=20
        )

        self.subview_button_frame.grid(row=1, column=0, columnspan=8, sticky="nsew")

        for index, button_name in enumerate(self.subview_buttons):
            # Layout the button inside the frame
            button = self.subview_buttons[button_name]
            button.grid(row=0, column=index)

    def create_subbutton_bar(self):
        callback_methods = {
            "Heat Rejection": lambda: self.show_subview("Heat Rejection"),
            "HVAC Systems": lambda: self.show_subview("HVAC Systems"),
            "Zonal Exhaust": lambda: self.show_subview("Zonal Exhaust"),
        }

        for name in callback_methods:
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
                    font=("Arial", 11, "bold"),
                )
            else:
                self.subview_buttons[name].configure(
                    fg_color="#FFD966",
                    hover_color="#FFD966",
                    text_color="black",
                    font=("Arial", 11, "bold"),
                )


class HeatRejectionView(ctk.CTkFrame):
    def __init__(self, systems_view):
        ctk.CTkFrame.__init__(self, systems_view)
        self.systems_view = systems_view

    def __repr__(self):
        return "HeatRejectionView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("Heat Rejection")


class HVACSystemView(ctk.CTkFrame):
    def __init__(self, systems_view):
        ctk.CTkFrame.__init__(self, systems_view)
        self.systems_view = systems_view

    def __repr__(self):
        return "HVACSystemView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("HVAC Systems")


class ZonalExhaustView(ctk.CTkFrame):
    def __init__(self, systems_view):
        ctk.CTkFrame.__init__(self, systems_view)
        self.systems_view = systems_view

    def __repr__(self):
        return "ZonalExhaustView"

    def open_subview(self):
        self.systems_view.toggle_active_subbutton("Zonal Exhaust")
