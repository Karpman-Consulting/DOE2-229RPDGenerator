from interface.install_config import InstallConfigWindow
from interface.project_config import ProjectConfigWindow

from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration


def main(test_mode=False):
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
