from rpd_generator.models.base_definition import BaseDefinition


class Condenser(BaseDefinition):
    """Condenser object in the tree."""

    bdl_command = "CONDENSING-UNIT"

    def __init__(self, u_name):
        super().__init__(u_name)

    def __repr__(self):
        return f"Condenser('{self.u_name}')"
