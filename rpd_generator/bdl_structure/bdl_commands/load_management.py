from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class LoadManagement(BaseDefinition):
    """LoadManagement object in the tree."""

    bdl_command = BDL_Commands.LOAD_MANAGEMENT

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

    def __repr__(self):
        return f"LoadManagement(u_name='{self.u_name}')"
