import tkinter as tk

from interface.compliance_parameter_window import ComplianceParameterWindow
from interface.install_config import InstallConfigWindow
from interface.project_config import ProjectConfigWindow
from interface.main_app_data import MainAppData

from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration

"""MainApplication is the main window of the application. Typically this is a visible window, but in this case it's
acting as a staging ground for all other windows which will be opened as TopLevel windows. It will hold data that
can be passed into and out of the TopLevel windows.

Note: With this paradigm, we need to add a protocol for every top level window to call the quit method of the
MainApplication when the window is closed to make sure the MainApplication closes and doesn't hang in the
background. It looks like this your_window.protocol("WM_DELETE_WINDOW", self.quit)"""


class MainApplication(tk.Tk):
    def __init__(self, test_mode=False):
        super().__init__()
        self.data = MainAppData()
        self.test_mode = test_mode

        self.install_config_window = None
        self.project_config_window = None
        self.compliance_parameter_window = None

        # Placeholder so we can see main app window open for sanity check.
        # If it becomes visible we will at least know what it is.
        self.title("Main Application Window")
        self.main_app_window_label = tk.Label(
            self,
            text="\U0001F419 ...You shouldn't be seeing this... \U0001F419",
            font=("Segoe UI Emoji", 20),
        )
        self.main_app_window_label.pack(anchor="center", padx=10, pady=10)
        self.withdraw()

        # To avoid doing a lot of work in the __init__ method, call this to "start" the application
        self.start_application()

    def start_application(self):
        """If in test mode, go directly to the ComplianceParameterWindow (formerly "MainApplication Window"). If
        not in test mode, check for eQUEST installation. If not found, open installation config window
        """
        if self.test_mode:
            self.compliance_parameter_window = ComplianceParameterWindow(
                self, self.test_mode
            )
            self.compliance_parameter_window.protocol("WM_DELETE_WINDOW", self.quit)

        else:
            validate_configuration.find_equest_installation()
            if Config.EQUEST_INSTALL_PATH:
                self.project_config_window = ProjectConfigWindow(self)
                self.project_config_window.protocol("WM_DELETE_WINDOW", self.quit)
            else:
                self.install_config_window = InstallConfigWindow(self)
                self.install_config_window.protocol("WM_DELETE_WINDOW", self.quit)

    def install_config_complete(self):
        """Called by InstallConfigWindow when the user has successfully configured the installation path. Closes
        the InstallConfigWindow and opens the ProjectConfigWindow"""
        self.install_config_window.destroy()
        self.project_config_window = ProjectConfigWindow(self)
        self.project_config_window.protocol("WM_DELETE_WINDOW", self.quit)

    def project_config_complete(self):
        """Called by ProjectConfigWindow when the user has successfully configured the project. Closes the
        ProjectConfigWindow and opens the ComplianceParameterWindow"""
        self.project_config_window.destroy()
        self.compliance_parameter_window = ComplianceParameterWindow(
            self, self.test_mode
        )
        self.compliance_parameter_window.protocol("WM_DELETE_WINDOW", self.quit)
