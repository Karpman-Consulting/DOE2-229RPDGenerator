import customtkinter as ctk
from pathlib import Path

from rpd_generator import main as rpd_generator
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.doe2_file_readers.model_input_reader import ModelInputReader
from rpd_generator.config import Config


class MainAppData:
    def __init__(self):
        self.bdl_reader = ModelInputReader()
        RulesetProjectDescription.bdl_command_dict = self.bdl_reader.bdl_command_dict
        self.rpd = RulesetProjectDescription()

        # Config data
        self.installation_path = ctk.StringVar()
        self.user_lib_path = None
        self.files_verified = False

        # Test data
        self.test_inp_path = ctk.StringVar()

        # Project data
        self.selected_ruleset = ctk.StringVar()
        self.selected_ruleset.set("ASHRAE 90.1-2019")
        self.ruleset_model_file_paths = {}

        self.rmds = []
        self.warnings = []
        self.errors = []

        self.installation_path.set(Config.EQUEST_INSTALL_PATH)
        self.configuration_data = {}

    @staticmethod
    def verify_associated_files(file_path: str) -> bool:
        """
        Check if the directory of the given file contains files with the same name
        or the same name with the suffix ' - Baseline Design' for the specified file types.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if all related files are found, False otherwise.
        """
        # Expected file extensions
        file_extensions = [".erp", ".srp", ".lrp", ".nhk"]

        file_path = Path(file_path)
        base_name = file_path.stem
        directory = file_path.parent

        # Check for each file type
        for ext in file_extensions:
            # Construct file names to check
            normal_file = directory / f"{base_name}{ext}"
            baseline_file = directory / f"{base_name} - Baseline Design{ext}"
            # Check existence
            if not normal_file.is_file() and not baseline_file.is_file():
                return False

        return True

    def generate_rmds(self):
        for ruleset_model_type, file_path in self.ruleset_model_file_paths.items():
            if file_path:
                rmd = rpd_generator.generate_rmd_from_inp(file_path)
                rmd.type = ruleset_model_type
                self.rmds.append(rmd)

    def call_write_rpd_json_from_inp(self):
        rpd_generator.write_rpd_json_from_inp(str(self.test_inp_path.get()))

    def is_all_new_construction(self):
        is_all_new_construction = self.configuration_data.get("new_construction")
        if is_all_new_construction:
            return True
        return False
