from pathlib import Path
from rpd_generator import main as rpd_generator
from rpd_generator.utilities import validate_configuration


def generate_test_rpds_from_bdls():

    test_directory = Path(__file__).parent
    test_bdl_files = [bdl_file for bdl_file in test_directory.rglob("*.BDL")]

    for test_bdl_file in test_bdl_files:
        print(f"Processing BDL File for Test Case {test_bdl_file.parent.name}...")

        output_path = test_bdl_file.with_suffix(".json")
        rpd_generator.write_rpd_json_from_bdl([str(test_bdl_file)], str(output_path))


if __name__ == "__main__":
    validate_configuration.find_equest_installation()
    generate_test_rpds_from_bdls()
