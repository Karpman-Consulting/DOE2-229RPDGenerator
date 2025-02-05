import os
import configparser
from pathlib import Path
from rpd_generator.config import Config


def find_equest_installation(installation_path=None):
    """
    Search recursively for a directory that matches a target directory starting from start_path.
    If found, checks if all target files exist within that directory in a case-insensitive manner.

    :return: Path of the directory if it exists with all target files, else None.
    """
    if not installation_path:
        start_path = Path(os.environ.get("ProgramFiles(x86)", "C:/"))
    else:
        start_path = Path(installation_path)
    target_dir = "eQUEST 3-65-7175".lower()  # Convert target directory to lowercase
    target_files = [
        "equest.ini",
        "equestd23.ini",
        "d2result.dll",
        "bdlcio32.dll",
    ]  # Converted target files to lowercase for comparison

    for path in start_path.rglob("*"):
        # Check if the current path is a directory and matches the target directory name (case-insensitive)
        if path.is_dir() and path.name.lower() == target_dir:
            # List all files in the current directory (case-insensitive match)
            files_in_dir = [
                file.name.lower() for file in path.iterdir() if file.is_file()
            ]
            # Check if all target files exist in the current directory (case-insensitive)
            if all(file in files_in_dir for file in target_files):
                Config.EQUEST_INSTALL_PATH = path
                set_data_paths_from_config()


def verify_equest_installation(installation_path=None):
    error_message = ""
    find_equest_installation(installation_path)
    all_paths_found = True

    if not Config.EQUEST_INSTALL_PATH:
        error_message += "eQUEST installation not found.\n"
        all_paths_found = False
    if not Config.DOE22_DATA_PATH:
        error_message += "DOE-22 data path not found.\n"
        all_paths_found = False
    if not Config.DOE23_DATA_PATH:
        error_message += "DOE-23 data path not found.\n"
        all_paths_found = False
    if not all_paths_found:
        return error_message  # Return early if any paths are missing

    # List of files to check
    files_to_check = [
        Path(Config.EQUEST_INSTALL_PATH) / "BDLCIO32.DLL",
        Path(Config.EQUEST_INSTALL_PATH) / "D2Result.dll",
        Path(Config.DOE22_DATA_PATH) / "DOE-2" / "eQ_Lib.dat",
        Path(Config.DOE23_DATA_PATH) / "DOE23" / "eQ_Lib.dat",
        Path(Config.DOE22_DATA_PATH) / "DOE-2" / "BDLLIB.DAT",
        Path(Config.DOE23_DATA_PATH) / "DOE23" / "BDLLIB.DAT",
        Path(Config.DOE22_DATA_PATH) / "DOE-2" / "Usrlib.dat",
        Path(Config.DOE23_DATA_PATH) / "DOE23" / "Usrlib.dat",
    ]

    # Check each file and raise an error if it doesn't exist
    for file_path in files_to_check:
        if not file_path.exists():
            error_message += f"File not found: {file_path}\n"

    return error_message


def set_data_paths_from_config():
    doe22_ini_path = str(Path(Config.EQUEST_INSTALL_PATH) / "eQUEST.ini")
    doe23_ini_path = str(Path(Config.EQUEST_INSTALL_PATH) / "eQUESTD23.ini")
    config = configparser.ConfigParser()
    config.read(doe22_ini_path)
    doe22_data_path = config.get("paths", "DataPath").strip('"')
    if doe22_data_path:
        Config.DOE22_DATA_PATH = doe22_data_path
    config.read(doe23_ini_path)
    doe23_data_path = config.get("paths", "DataPath").strip('"')
    if doe23_data_path:
        Config.DOE23_DATA_PATH = doe23_data_path
