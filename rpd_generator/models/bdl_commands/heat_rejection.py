from rpd_generator.models.base_node import BaseNode


class HeatRejection(BaseNode):
    """Heat Rejection object in the tree."""

    bdl_command = "HEAT-REJECTION"

    def __init__(self, u_name):
        super().__init__(u_name)

    def __repr__(self):
        return f"HeatRejection({self.obj_id})"

    def populate_schema_structure(self):
        """Populate schema structure for heat rejection object."""
        return {}
