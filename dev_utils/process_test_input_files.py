import tempfile
import shutil
from pathlib import Path

from rpd_generator import main as rpd_generator
from rpd_generator.config import Config
from rpd_generator.doe2_file_readers.bdlcio32 import process_input_file
from rpd_generator.utilities import validate_configuration


def process_test_input_files():
    validate_configuration.find_equest_installation()
    test_directory = Path(__file__).parents[1] / "test" / "full_rpd_test"
    test_inp_files = list(test_directory.rglob("*.inp"))

    with tempfile.TemporaryDirectory() as temp_dir:

        for test_inp_file in test_inp_files:
            print(f"Processing INP File for Test Case {test_inp_file.parent.name}...")

            # Prepare the inp file for processing and save the revised copy to the temporary directory
            temp_file_path = rpd_generator.prepare_inp(
                Path(test_inp_file), Path(temp_dir)
            )

            # Set the paths for the inp file, json file, and the directories
            temp_inp_path = Path(temp_file_path)
            bdl_path = temp_inp_path.with_suffix(".BDL")
            doe23_path = Path(Config.DOE23_DATA_PATH) / "DOE23"
            bdlcio32_path = Path(Config.EQUEST_INSTALL_PATH) / "Bdlcio32.dll"

            # Process the inp file to create the BDL file with Diagnostic Comments (defaults and evaluated values) in the temporary directory
            process_input_file(
                str(bdlcio32_path),
                str(doe23_path) + "\\",
                str(temp_inp_path.parent) + "\\",
                temp_inp_path.name,
            )

            # Copy the BDL file from the temporary directory back to the project directory
            shutil.copy(str(bdl_path), str(test_inp_file.parent))

            print(f"Diagnostic-Commented BDL file created.")
            print("----------------------------------------")


if __name__ == "__main__":
    process_test_input_files()
