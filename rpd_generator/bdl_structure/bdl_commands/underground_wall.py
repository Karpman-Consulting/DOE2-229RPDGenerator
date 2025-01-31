import copy

from rpd_generator.bdl_structure.child_node import ChildNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


SurfaceClassificationOptions = SchemaEnums.schema_enums["SurfaceClassificationOptions"]
SurfaceAdjacencyOptions = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"]
AdditionalSurfaceAdjacencyOptions2019ASHRAE901 = SchemaEnums.schema_enums[
    "AdditionalSurfaceAdjacencyOptions2019ASHRAE901"
]
StatusOptions = SchemaEnums.schema_enums["StatusOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_UndergroundWallKeywords = BDLEnums.bdl_enums["UndergroundWallKeywords"]
BDL_ConstructionKeywords = BDLEnums.bdl_enums["ConstructionKeywords"]
BDL_LayerKeywords = BDLEnums.bdl_enums["LayerKeywords"]
BDL_SpaceKeywords = BDLEnums.bdl_enums["SpaceKeywords"]
BDL_FloorKeywords = BDLEnums.bdl_enums["FloorKeywords"]
BDL_WallLocationOptions = BDLEnums.bdl_enums["WallLocationOptions"]
BDL_ConstructionTypes = BDLEnums.bdl_enums["ConstructionTypes"]


class BelowGradeWall(ChildNode):
    """BelowGradeWall object in the tree."""

    bdl_command = BDL_Commands.UNDERGROUND_WALL

    CEILING_TILT_THRESHOLD = 60
    FLOOR_TILT_THRESHOLD = 120

    def __init__(self, u_name, parent, rmd):
        super().__init__(u_name, parent, rmd)
        self.rmd.undg_wall_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.underground_wall_data_structure = {}

        # data elements with children
        self.construction = {}
        self.optical_properties = {}

        # data elements with no children
        self.classification = None
        self.area = None
        self.tilt = None
        self.azimuth = None
        self.adjacent_to = None
        self.adjacent_zone = None
        self.does_cast_shade = None
        self.status_type = None

        # data elements for surface optical properties
        self.optical_property_id = self.u_name + " OpticalProps"
        self.absorptance_thermal_exterior = None
        self.absorptance_solar_exterior = None
        self.absorptance_visible_exterior = None
        self.absorptance_thermal_interior = None
        self.absorptance_solar_interior = None
        self.absorptance_visible_interior = None

    def __repr__(self):
        return f"BelowGradeWall(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for below grade wall object."""

        self.area = self.try_float(self.get_inp(BDL_UndergroundWallKeywords.AREA))
        if self.area is None:
            height = self.try_float(self.get_inp(BDL_UndergroundWallKeywords.HEIGHT))
            width = self.try_float(self.get_inp(BDL_UndergroundWallKeywords.WIDTH))
            if height is not None and width is not None:
                self.area = height * width

        self.tilt = self.try_float(self.get_inp(BDL_UndergroundWallKeywords.TILT))
        if self.tilt is not None and self.tilt < self.CEILING_TILT_THRESHOLD:
            self.classification = SurfaceClassificationOptions.CEILING
        elif self.tilt is not None and self.tilt >= self.FLOOR_TILT_THRESHOLD:
            self.classification = SurfaceClassificationOptions.FLOOR
        else:
            self.classification = SurfaceClassificationOptions.WALL

        parent_floor_azimuth = self.parent.parent.try_float(
            self.parent.parent.get_inp(BDL_FloorKeywords.AZIMUTH)
        )
        parent_space_azimuth = self.parent.try_float(
            self.parent.get_inp(BDL_SpaceKeywords.AZIMUTH)
        )
        surface_azimuth = self.try_float(
            self.get_inp(BDL_UndergroundWallKeywords.AZIMUTH)
        )
        if (
            self.rmd.building_azimuth is not None
            and parent_floor_azimuth is not None
            and parent_space_azimuth is not None
            and surface_azimuth is not None
        ):
            self.azimuth = (
                self.rmd.building_azimuth
                + parent_floor_azimuth
                + parent_space_azimuth
                + surface_azimuth
            ) % 360
            if self.azimuth < 0:
                self.azimuth += 360

        self.adjacent_to = SurfaceAdjacencyOptions.GROUND

        self.does_cast_shade = self.boolean_map.get(
            self.get_inp(BDL_UndergroundWallKeywords.SHADING_SURFACE)
        )

        self.absorptance_solar_interior = self.try_float(
            self.get_inp(BDL_UndergroundWallKeywords.INSIDE_SOL_ABS)
        )

        reflectance_visible_interior = self.try_float(
            self.get_inp(BDL_UndergroundWallKeywords.INSIDE_VIS_REFL)
        )
        if reflectance_visible_interior is not None:
            self.absorptance_visible_interior = 1 - reflectance_visible_interior

    # def get_output_requests(self):
    #     requests = {}
    #     if (
    #         self.area is None
    #         and self.get_inp(BDL_UndergroundWallKeywords.LOCATION)
    #         == BDL_WallLocationOptions.TOP
    #     ):
    #         requests["Roof Area"] = (1105003, "", self.u_name)
    #     return requests

    def populate_data_group(self):
        """Populate schema structure for below grade wall object."""
        self.construction = copy.deepcopy(
            self.get_obj(
                self.get_inp(BDL_UndergroundWallKeywords.CONSTRUCTION)
            ).construction_data_structure
        )
        self.account_for_air_film_resistance()

        optical_property_attributes = [
            "optical_property_id",
            "absorptance_thermal_exterior",
            "absorptance_solar_exterior",
            "absorptance_visible_exterior",
            "absorptance_thermal_interior",
            "absorptance_solar_interior",
            "absorptance_visible_interior",
        ]

        for attr in optical_property_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                attr = attr.replace("optical_property_", "")
                self.optical_properties[attr] = value

        self.underground_wall_data_structure = {
            "id": self.u_name,
            "construction": self.construction,
            "optical_properties": self.optical_properties,
        }
        self.populate_data_elements()

        no_children_attributes = [
            "reporting_name",
            "notes",
            "classification",
            "area",
            "tilt",
            "azimuth",
            "adjacent_to",
            "adjacent_zone",
            "does_cast_shade",
            "status_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.underground_wall_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert below grade wall object into the rpd data structure."""
        zone = rmd.space_map.get(self.parent.u_name)
        zone.surfaces.append(self.underground_wall_data_structure)

    def account_for_air_film_resistance(self):
        """
        Remove interior air film resistance from a simplified construction's simplified material r_value.
        """
        construction_obj = self.get_obj(
            self.get_inp(BDL_UndergroundWallKeywords.CONSTRUCTION)
        )
        spec_method = construction_obj.get_inp(BDL_ConstructionKeywords.TYPE)
        u_factor = self.construction.get("u_factor")
        if u_factor:
            if spec_method == BDL_ConstructionTypes.U_VALUE:
                location = self.get_inp(BDL_UndergroundWallKeywords.LOCATION)
                int_air_film_resistance = (
                    0.61
                    if location == BDL_WallLocationOptions.TOP
                    else 0.92 if location == BDL_WallLocationOptions.BOTTOM else 0.68
                )
                self.construction["primary_layers"][0]["r_value"] = (
                    1 / u_factor - int_air_film_resistance
                )
