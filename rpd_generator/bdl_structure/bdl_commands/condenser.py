from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class Condenser(BaseDefinition):
    """Condenser object in the tree."""

    bdl_command = BDL_Commands.CONDENSING_UNIT

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"Condenser(u_name='{self.u_name}')"
