from rpd_generator.bdl_structure.base_node import BaseNode


class Material(BaseNode):
    """Material object in the tree."""

    bdl_command = "MATERIAL"

    def __init__(self, u_name):
        super().__init__(u_name)

    def __repr__(self):
        return f"Material({self.u_name})"

    def populate_schema_structure(self):
        """Populate schema structure for material object."""
        return {}
