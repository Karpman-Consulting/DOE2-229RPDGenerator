from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_GlassTypeKeywords = BDLEnums.bdl_enums["GlassTypeKeywords"]


class GlassType(BaseDefinition):
    """GlassType object in the tree."""

    bdl_command = BDL_Commands.GLASS_TYPE

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.u_factor = None
        self.shading_coefficient = None
        self.visible_transmittance = None
        self.absorptance_thermal_exterior = None

    def __repr__(self):
        return f"GlassType(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate schema structure for glass type object."""
        self.u_factor = self.try_float(
            self.get_inp(BDL_GlassTypeKeywords.GLASS_CONDUCT)
        )

        self.shading_coefficient = self.try_float(
            self.get_inp(BDL_GlassTypeKeywords.SHADING_COEF)
        )

        self.visible_transmittance = self.try_float(
            self.get_inp(BDL_GlassTypeKeywords.VIS_TRANS)
        )

        self.absorptance_thermal_exterior = self.try_float(
            self.get_inp(BDL_GlassTypeKeywords.OUTSIDE_EMISS)
        )
