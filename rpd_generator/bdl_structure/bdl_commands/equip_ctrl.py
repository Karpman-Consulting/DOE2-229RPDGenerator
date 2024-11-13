from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class EquipCtrl(BaseDefinition):
    """EquipCtrl object in the tree."""

    bdl_command = BDL_Commands.EQUIP_CTRL

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.equip_ctrl_names.append(u_name)

    def __repr__(self):
        return f"EquipCtrl(u_name='{self.u_name}')"
