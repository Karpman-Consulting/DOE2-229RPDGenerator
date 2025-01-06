from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class CurveFit(BaseDefinition):
    """CurveFit object in the tree."""

    bdl_command = BDL_Commands.CURVE_FIT

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.curve_fit_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"CurveFit(u_name='{self.u_name}')"
