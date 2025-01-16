from interface.install_config import InstallConfigWindow
from interface.project_config import ProjectConfigWindow
from interface.main_app_window import MainApplicationWindow

from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration


def main(test_mode=False):
    if test_mode:
        app = MainApplicationWindow(test_mode)
        app.mainloop()

    else:
        validate_configuration.find_equest_installation()
        if Config.EQUEST_INSTALL_PATH:
            project_config_window = ProjectConfigWindow()
            project_config_window.mainloop()
        else:
            config_window = InstallConfigWindow()
            config_window.mainloop()


if __name__ == "__main__":
    # main(test_mode=True)
    main()
