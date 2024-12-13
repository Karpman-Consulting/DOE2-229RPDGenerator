from rpd_generator.bdl_structure.parent_definition import ParentDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]


class Floor(ParentDefinition):
    """Floor object in the tree."""

    bdl_command = BDL_Commands.FLOOR

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"Floor(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate schema structure for floor object."""
        pass
