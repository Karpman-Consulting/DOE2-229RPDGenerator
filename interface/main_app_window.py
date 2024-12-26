import customtkinter as ctk
from PIL import Image
from tkinter import Menu

from interface.main_app_data import MainAppData
from interface.views.test import TestView
from interface.views.install_config import InstallConfigView
from interface.views.project_info import ProjectInfoView
from interface.views.buildings import BuildingsView
from interface.views.building_segments import BuildingSegmentsView
from interface.views.zones import ZonesView
from interface.views.surfaces import SurfacesView
from interface.views.systems import SystemsView
from interface.views.ext_lighting import ExteriorLightingView
from interface.views.miscellaneous import MiscellaneousView
from interface.views.results import ResultsView
from interface.disclaimer_window import DisclaimerWindow
from interface.error_window import ErrorWindow

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class MainApplicationWindow(ctk.CTk):
    def __init__(self, test_mode=False):
        super().__init__()
        self.title("eQUEST 229 RPD Generator")
        self.geometry(f"{1300}x{700}")
        self.minsize(1300, 350)
        self.grid_propagate(False)
        self.bg_color = self.cget("fg_color")[0]

        self.app_data = MainAppData()
        self.views = {
            "Test": TestView(self),
            "Configuration": InstallConfigView(self),
            "Project Info": ProjectInfoView(self),
            "Buildings": BuildingsView(self),
            "Building Segments": BuildingSegmentsView(self),
            "Zones": ZonesView(self),
            "Surfaces": SurfacesView(self),
            "Systems": SystemsView(self),
            "Ext. Lighting": ExteriorLightingView(self),
            "Misc.": MiscellaneousView(self),
            "Results": ResultsView(self),
        }

        self.navbar_buttons = {}

        # Initialize attributes to hold references to Widgets & Windows
        self.current_view = None

        self.warnings_button = ctk.CTkButton(
            self,
            text="Warnings",
            width=90,
            fg_color="orange",
            hover_color="#FF8C00",
            corner_radius=12,
            command=lambda: self.raise_error_window("\n".join(self.app_data.warnings)),
        )
        self.errors_button = ctk.CTkButton(
            self,
            text="Errors",
            width=90,
            fg_color="red",
            hover_color="#E60000",
            corner_radius=12,
            command=lambda: self.raise_error_window("\n".join(self.app_data.errors)),
        )
        self.continue_button = ctk.CTkButton(
            self, text="Continue", width=100, corner_radius=12
        )

        self.license_window = None
        self.disclaimer_window = None
        self.error_window = None

        # Create main application widgets
        self.menubar = self.create_menu_bar()
        self.create_button_bar()
        self.create_nav_bar()

        if not self.app_data.installation_path.get():
            # Initialize the configuration window to select and verify the eQUEST installation path
            self.show_view("Configuration")

        elif test_mode:
            self.show_view("Test")

        else:
            # If the eQUEST installation path is found, continue to the Project Info page
            self.navbar_buttons["Project Info"].configure(state="normal")
            self.show_view("Project Info")

    def create_menu_bar(self):
        menubar = Menu(self)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command="donothing")
        file_menu.add_command(label="Open", command="donothing")
        file_menu.add_command(label="Save", command="donothing")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Instructions", command="donothing")
        help_menu.add_command(label="Background", command="donothing")
        help_menu.add_separator()
        help_menu.add_command(label="License", command="donothing")
        help_menu.add_command(label="Disclaimer", command=self.open_disclaimer)
        menubar.add_cascade(label="About", menu=help_menu)

        self.config(menu=menubar)
        return menubar

    def create_button_bar(self):
        # Define button names
        button_names = [
            "Project Info",
            "Buildings",
            "Building Segments",
            "Zones",
            "Surfaces",
            "Systems",
            "Ext. Lighting",
            "Misc.",
            "Results",
        ]

        # Define button icons
        icon_paths = [
            "menu.png",
            "buildings.png",
            "building_segments.png",
            "spaces.png",
            "surfaces.png",
            "systems.png",
            "ext_lighting.png",
            "misc.png",
            "results.png",
        ]
        callback_methods = {
            "Project Info": lambda: self.show_view("Project Info"),
            "Buildings": lambda: self.show_view("Buildings"),
            "Building Segments": lambda: self.show_view("Building Segments"),
            "Zones": lambda: self.show_view("Zones"),
            "Surfaces": lambda: self.show_view("Surfaces"),
            "Systems": lambda: self.show_view("Systems"),
            "Ext. Lighting": lambda: self.show_view("Ext. Lighting"),
            "Misc.": lambda: self.show_view("Misc."),
            "Results": lambda: self.show_view("Results"),
        }

        for index, (name, icon_path) in enumerate(zip(button_names, icon_paths)):
            # Load and recolor the icon for the button
            icon = Image.open(f"interface/static/{icon_path}").convert("RGBA")

            r, g, b, alpha = icon.split()
            white_icon = Image.merge(
                "RGBA", (alpha, alpha, alpha, alpha)
            )  # Merge all channels into alpha to keep transparency
            icon_image = ctk.CTkImage(white_icon)

            # Create a frame for each button that will act as the border
            button_frame = ctk.CTkFrame(self, width=144, height=36, corner_radius=0)
            button_frame.grid(row=0, column=index, sticky="nsew")

            # Then create the button inside this frame with the icon
            button = ctk.CTkButton(
                button_frame,
                image=icon_image,
                text=name,
                font=("Arial", 12),
                width=140,
                height=30,
                corner_radius=0,
                state="disabled",
                compound="left",
                command=callback_methods[name],
            )
            button.place(relx=0.5, rely=0.5, anchor="center")
            self.navbar_buttons[name] = button

            # Keep a reference to the image to prevent garbage collection
            button.image = icon_image

    def create_nav_bar(self):
        # Create the button to continue to the Buildings page
        self.continue_button.grid(row=2, column=3, columnspan=3, pady=5)
        # Create the errors and warnings buttons
        self.warnings_button.grid(row=2, column=0, pady=5)
        self.errors_button.grid(row=2, column=1, pady=5)

    def show_view(self, view_name):
        # Clear previous view
        if self.current_view is not None:
            self.current_view.grid_forget()

        # Show new view
        view = self.views.get(view_name)
        if view:
            self.current_view = view
            self.current_view.grid(row=1, column=0, columnspan=9, sticky="nsew")
            self.current_view.open_view()

    def open_disclaimer(self):
        if self.disclaimer_window is None or not self.disclaimer_window.winfo_exists():
            self.disclaimer_window = DisclaimerWindow(self)
            self.disclaimer_window.after(100, self.disclaimer_window.lift)
        else:
            self.disclaimer_window.focus()  # if window exists, focus it

    def raise_error_window(self, error_text):
        self.error_window = ErrorWindow(self, error_text)
        self.error_window.after(100, self.error_window.lift)
