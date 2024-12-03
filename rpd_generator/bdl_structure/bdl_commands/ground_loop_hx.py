from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class GroundLoopHX(BaseDefinition):
    """GroundLoopHX object in the tree."""

    bdl_command = BDL_Commands.GROUND_LOOP_HX

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.ground_loop_hx_names.append(u_name)

    def __repr__(self):
        return f"GroundLoopHX(u_name='{self.u_name}')"
