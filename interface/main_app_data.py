import customtkinter as ctk


class MainAppData:
    def __init__(self):
        self.installation_path = ctk.StringVar()
        self.user_lib_path = None
        self.files_verified = False
        self.test_inp_path = ctk.StringVar()
        self.project_input_file_paths = {}
