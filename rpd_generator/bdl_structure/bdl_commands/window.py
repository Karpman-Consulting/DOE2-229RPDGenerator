from rpd_generator.bdl_structure.child_node import ChildNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


SubsurfaceClassificationOptions = SchemaEnums.schema_enums[
    "SubsurfaceClassificationOptions"
]
SubsurfaceSubclassificationOptions2019ASHRAE901 = SchemaEnums.schema_enums[
    "SubsurfaceSubclassificationOptions2019ASHRAE901"
]
SubsurfaceFrameOptions2019ASHRAE901 = SchemaEnums.schema_enums[
    "SubsurfaceFrameOptions2019ASHRAE901"
]
SubsurfaceDynamicGlazingOptions = SchemaEnums.schema_enums[
    "SubsurfaceDynamicGlazingOptions"
]
StatusOptions = SchemaEnums.schema_enums["StatusOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_WindowKeywords = BDLEnums.bdl_enums["WindowKeywords"]
BDL_WindowShadeTypes = BDLEnums.bdl_enums["WindowShadeTypes"]
BDL_ExteriorWallKeywords = BDLEnums.bdl_enums["ExteriorWallKeywords"]
BDL_WallLocationOptions = BDLEnums.bdl_enums["WallLocationOptions"]


class Window(ChildNode):
    """Window object in the tree."""

    bdl_command = BDL_Commands.WINDOW

    def __init__(self, u_name, parent, rmd):
        super().__init__(u_name, parent, rmd)

        self.window_data_structure = {}

        # data elements with no children
        self.classification = None
        self.subclassification = None
        self.is_operable = None
        self.has_open_sensor = None
        self.framing_type = None
        self.glazed_area = None
        self.opaque_area = None
        self.u_factor = None
        self.dynamic_glazing_type = None
        self.solar_heat_gain_coefficient = None
        self.maximum_solar_heat_gain_coefficient = None
        self.visible_transmittance = None
        self.minimum_visible_transmittance = None
        self.depth_of_overhang = None
        self.has_shading_overhang = None
        self.has_shading_sidefins = None
        self.has_manual_interior_shades = None
        self.solar_transmittance_multiplier_summer = None
        self.solar_transmittance_multiplier_winter = None
        self.has_automatic_shades = None
        self.status_type = None

    def __repr__(self):
        return f"Window(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for window object."""
        height = self.try_float(self.get_inp(BDL_WindowKeywords.HEIGHT))
        width = self.try_float(self.get_inp(BDL_WindowKeywords.WIDTH))
        if height is not None and width is not None:
            self.glazed_area = height * width
            frame_width = self.try_float(self.get_inp(BDL_WindowKeywords.FRAME_WIDTH))
            if frame_width is None or frame_width == 0.0:
                self.opaque_area = 0
            else:
                self.opaque_area = 2 * (
                    frame_width * height + frame_width * width + 2 * frame_width**2
                )

        if (
            self.parent.get_inp(BDL_ExteriorWallKeywords.LOCATION)
            == BDL_WallLocationOptions.TOP
        ):
            self.classification = SubsurfaceClassificationOptions.SKYLIGHT
        else:
            self.classification = SubsurfaceClassificationOptions.WINDOW

        glass_type_name = self.get_inp(BDL_WindowKeywords.GLASS_TYPE)
        glass_type = self.get_obj(glass_type_name)
        if glass_type is not None:
            self.u_factor = glass_type.u_factor
            self.visible_transmittance = glass_type.visible_transmittance
            if glass_type.shading_coefficient is not None:
                self.solar_heat_gain_coefficient = glass_type.shading_coefficient / 1.15

        if self.try_float(
            self.get_inp(BDL_WindowKeywords.LEFT_FIN_D)
        ) or self.try_float(self.get_inp(BDL_WindowKeywords.RIGHT_FIN_D)):
            self.has_shading_sidefins = True

        if self.get_inp(BDL_WindowKeywords.OVERHANG_D):
            self.depth_of_overhang = self.try_float(
                self.get_inp(BDL_WindowKeywords.OVERHANG_D)
            )
            self.has_shading_overhang = True

        if self.get_inp(BDL_WindowKeywords.WIN_SHADE_TYPE) in [
            BDL_WindowShadeTypes.MOVABLE_INTERIOR,
            BDL_WindowShadeTypes.MOVABLE_EXTERIOR,
        ] and self.get_inp(BDL_WindowKeywords.SHADING_SCHEDULE):
            self.has_manual_interior_shades = True

    def populate_data_group(self):
        """Populate schema structure for window object."""
        self.window_data_structure = {
            "id": self.u_name,
        }
        self.populate_data_elements()

        no_children_attributes = [
            "reporting_name",
            "notes",
            "classification",
            "subclassification",
            "is_operable",
            "has_open_sensor",
            "framing_type",
            "glazed_area",
            "opaque_area",
            "u_factor",
            "dynamic_glazing_type",
            "solar_heat_gain_coefficient",
            "maximum_solar_heat_gain_coefficient",
            "visible_transmittance",
            "minimum_visible_transmittance",
            "depth_of_overhang",
            "has_shading_overhang",
            "has_shading_sidefins",
            "has_manual_interior_shades",
            "solar_transmittance_multiplier_summer",
            "solar_transmittance_multiplier_winter",
            "has_automatic_shades",
            "status_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.window_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert window object into the rpd data structure."""
        surface = self.get_obj(self.parent.u_name)
        surface.subsurfaces.append(self.window_data_structure)
