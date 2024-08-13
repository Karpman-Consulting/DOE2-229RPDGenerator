from rpd_generator.bdl_structure.child_node import ChildNode
from rpd_generator.schema.schema_enums import SchemaEnums

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


class Window(ChildNode):
    """Window object in the tree."""

    bdl_command = "WINDOW"

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
        height = self.try_float(self.keyword_value_pairs.get("HEIGHT"))
        width = self.try_float(self.keyword_value_pairs.get("WIDTH"))
        if height is not None and width is not None:
            self.glazed_area = height * width
            frame_width = self.try_float(self.keyword_value_pairs.get("FRAME-WIDTH"))
            if frame_width is None or frame_width == 0.0:
                self.opaque_area = 0
            else:
                self.opaque_area = 2 * (
                    frame_width * height + frame_width * width + 2 * frame_width**2
                )

        if self.parent.keyword_value_pairs.get("LOCATION") == "TOP":
            self.classification = SubsurfaceClassificationOptions.SKYLIGHT
        else:
            self.classification = SubsurfaceClassificationOptions.WINDOW

        glass_type_name = self.keyword_value_pairs.get("GLASS-TYPE")
        glass_type = self.rmd.bdl_obj_instances.get(glass_type_name)
        if glass_type is not None:
            self.u_factor = glass_type.u_factor
            self.solar_heat_gain_coefficient = glass_type.shading_coefficient / 1.15
            self.visible_transmittance = glass_type.visible_transmittance

        left_fin_depth = self.try_float(self.keyword_value_pairs.get("LEFT-FIN-D"))
        right_fin_depth = self.try_float(self.keyword_value_pairs.get("RIGHT-FIN-D"))
        if left_fin_depth not in [None, 0.0] or right_fin_depth not in [None, 0.0]:
            self.has_shading_sidefins = True
        overhang_depth = self.keyword_value_pairs.get("OVERHANG-D")
        if overhang_depth not in [None, 0.0]:
            self.depth_of_overhang = overhang_depth
            self.has_shading_overhang = True

        shade_schedule = self.keyword_value_pairs.get("SHADING-SCHEDULE")
        shade_type = self.keyword_value_pairs.get("WIN-SHADE-TYPE")
        if shade_type is not None:
            adjustable_shade = shade_type.startswith("MOVABLE-")
            if shade_schedule is not None and adjustable_shade:
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
        surface = rmd.bdl_obj_instances.get(self.parent.u_name)
        surface.subsurfaces.append(self.window_data_structure)
