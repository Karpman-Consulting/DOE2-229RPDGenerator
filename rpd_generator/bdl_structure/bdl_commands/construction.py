from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

SurfaceConstructionInputOptions = SchemaEnums.schema_enums[
    "SurfaceConstructionInputOptions"
]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ConstructionKeywords = BDLEnums.bdl_enums["ConstructionKeywords"]
BDL_MaterialTypes = BDLEnums.bdl_enums["MaterialTypes"]


class Construction(BaseNode):
    """Construction object in the tree."""

    bdl_command = BDL_Commands.CONSTRUCTION

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.construction_data_structure = {}
        self.material_references = None

        # data elements with children
        self.primary_layers = []
        self.framing_layers = []
        self.insulation_locations = []
        self.r_values = []

        # data elements with no children
        self.classification = None
        self.surface_construction_input_option = None
        self.fraction_framing = None
        self.u_factor = None
        self.c_factor = None
        self.f_factor = None
        self.has_radiant_heating = None
        self.has_radiant_cooling = None

    def __repr__(self):
        return f"Construction(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for construction object."""
        layer = self.get_obj(self.get_inp(BDL_ConstructionKeywords.LAYERS))
        # Material references will be empty if construction uses U-Value Input method
        self.material_references = layer.material_references if layer else []

        any_detailed_materials = False
        for material_reference in self.material_references or []:
            material = self.get_obj(material_reference)
            if material and material.material_type == BDL_MaterialTypes.PROPERTIES:
                any_detailed_materials = True

        self.surface_construction_input_option = (
            SurfaceConstructionInputOptions.LAYERS
            if any_detailed_materials
            else SurfaceConstructionInputOptions.SIMPLIFIED
        )

        if (
            self.surface_construction_input_option
            == SurfaceConstructionInputOptions.SIMPLIFIED
        ):
            simplified_material = {"id": "Simplified Material"}
            # This simplified material will have its r_value added when used for a surface based on Ext/Int/Underground Wall air film resistances
            self.primary_layers.append(simplified_material)

        # This u_factor will be adjusted when used for a surface based on Ext/Int/Underground Wall air film resistances
        self.u_factor = self.try_float(self.get_inp(BDL_ConstructionKeywords.U_VALUE))

    def populate_data_group(self):
        """Populate schema structure for construction object."""

        for material_reference in self.material_references or []:
            material = self.get_obj(material_reference)
            if material:
                self.primary_layers.append(material.material_data_structure)

        self.construction_data_structure = {
            "id": self.u_name,
            "primary_layers": self.primary_layers,
            "framing_layers": self.framing_layers,
            "insulation_locations": self.insulation_locations,
            "r_values": self.r_values,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "classification",
            "surface_construction_input_option",
            "fraction_framing",
            "u_factor",
            "c_factor",
            "f_factor",
            "has_radiant_heating",
            "has_radiant_cooling",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.construction_data_structure[attr] = value
