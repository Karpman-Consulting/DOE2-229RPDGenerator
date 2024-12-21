import customtkinter as ctk

from rpd_generator import main as rpd_generator
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.doe2_file_readers.model_input_reader import ModelInputReader


class MainAppData:
    def __init__(self):
        self.installation_path = ctk.StringVar()
        self.user_lib_path = None
        self.files_verified = False
        self.test_inp_path = ctk.StringVar()
        self.project_input_file_paths = {}
        self.bdl_reader = ModelInputReader()
        RulesetProjectDescription.bdl_command_dict = self.bdl_reader.bdl_command_dict
        self.rpd = RulesetProjectDescription()
        self.rmds = []

    def generate_rmds(self):
        for ruleset_model_type, file_path in self.project_input_file_paths.items():
            if file_path:
                rmd = rpd_generator.generate_rmd_from_inp(file_path)
                rmd.type = ruleset_model_type
                self.rmds.append(rmd)
