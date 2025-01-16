import customtkinter as ctk


class ProjectConfigWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Project Configuration")

    def __repr__(self):
        return "ProjectConfigWindow"
