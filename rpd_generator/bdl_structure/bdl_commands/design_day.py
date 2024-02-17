from rpd_generator.bdl_structure.base_definition import BaseDefinition


class DesignDay(BaseDefinition):
    """DesignDay class"""

    bdl_command = "DESIGN-DAY"

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

    def __repr__(self):
        return f"DesignDay(u_name='{self.u_name}')"
