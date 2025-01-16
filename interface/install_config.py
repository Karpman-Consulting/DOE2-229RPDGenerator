import customtkinter as ctk


class InstallConfigWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("eQUEST Installation Configuration")

    def __repr__(self):
        return "InstallConfigWindow"
