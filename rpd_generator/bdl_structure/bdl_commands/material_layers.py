from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_MaterialKeywords = BDLEnums.bdl_enums["MaterialKeywords"]
BDL_LayerKeywords = BDLEnums.bdl_enums["LayerKeywords"]
BDL_MaterialTypes = BDLEnums.bdl_enums["MaterialTypes"]


class Material(BaseNode):
    """Material object in the tree."""

    bdl_command = BDL_Commands.MATERIAL

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.material_data_structure = {}
        self.material_type = None

        # data elements with no children
        self.thickness = None
        self.thermal_conductivity = None
        self.density = None
        self.specific_heat = None
        self.r_value = None

    def __repr__(self):
        return f"Material(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for material object."""
        self.material_type = self.get_inp(BDL_MaterialKeywords.TYPE)

        if self.material_type == BDL_MaterialTypes.PROPERTIES:
            self.thickness = self.try_float(
                self.get_inp(BDL_MaterialKeywords.THICKNESS)
            )

            self.thermal_conductivity = self.try_float(
                self.get_inp(BDL_MaterialKeywords.CONDUCTIVITY)
            )

            self.density = self.try_float(self.get_inp(BDL_MaterialKeywords.DENSITY))

            self.specific_heat = self.try_float(
                self.get_inp(BDL_MaterialKeywords.SPECIFIC_HEAT)
            )

        elif self.material_type == BDL_MaterialTypes.RESISTANCE:
            self.r_value = self.try_float(self.get_inp(BDL_MaterialKeywords.RESISTANCE))

    def populate_data_group(self):
        """Populate schema structure for material object."""
        self.material_data_structure["id"] = self.u_name

        no_children_attributes = [
            "reporting_name",
            "notes",
            "thickness",
            "thermal_conductivity",
            "density",
            "specific_heat",
            "r_value",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.material_data_structure[attr] = value


class Layer(BaseDefinition):
    """Layer object in the tree."""

    bdl_command = BDL_Commands.LAYERS

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.material_references = None

    def __repr__(self):
        return f"Layer(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for layers object."""
        material_references = self.get_inp(BDL_LayerKeywords.MATERIAL, [])
        self.material_references = (
            material_references
            if isinstance(material_references, list)
            else [material_references]
        )
