from rpd_generator.bdl_structure.parent_node import ParentNode
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
BDL_ExteriorWallKeywords = BDLEnums.bdl_enums["ExteriorWallKeywords"]
BDL_ConstructionKeywords = BDLEnums.bdl_enums["ConstructionKeywords"]
BDL_WallLocationOptions = BDLEnums.bdl_enums["WallLocationOptions"]
BDL_SpaceKeywords = BDLEnums.bdl_enums["SpaceKeywords"]
BDL_FloorKeywords = BDLEnums.bdl_enums["FloorKeywords"]


class ExteriorWall(ChildNode, ParentNode):
    """ExteriorWall object in the tree."""

    bdl_command = BDL_Commands.EXTERIOR_WALL

    CEILING_TILT_THRESHOLD = 60
    FLOOR_TILT_THRESHOLD = 120

    def __init__(self, u_name, parent, rmd):
        super().__init__(u_name, parent, rmd)

        self.exterior_wall_data_structure = {}

        # data elements with children
        self.subsurfaces = []
        self.construction = {}
        self.optical_properties = {"id": self.u_name + " OpticalProps"}

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
        self.absorptance_thermal_exterior = None
        self.absorptance_solar_exterior = None
        self.absorptance_visible_exterior = None
        self.absorptance_thermal_interior = None
        self.absorptance_solar_interior = None
        self.absorptance_visible_interior = None

    def __repr__(self):
        return f"ExteriorWall(u_name='{self.u_name}', parent={self.parent})"

    def populate_data_elements(self):
        """Populate data elements for exterior wall object."""
        self.area = self.try_float(self.get_inp(BDL_ExteriorWallKeywords.AREA))
        if self.area is None:
            height = self.try_float(self.get_inp(BDL_ExteriorWallKeywords.HEIGHT))
            width = self.try_float(self.get_inp(BDL_ExteriorWallKeywords.WIDTH))
            if height is not None and width is not None:
                self.area = height * width

        self.tilt = self.try_float(self.get_inp(BDL_ExteriorWallKeywords.TILT))
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
        surface_azimuth = self.try_float(self.get_inp(BDL_ExteriorWallKeywords.AZIMUTH))
        self.azimuth = (
            self.rmd.building_azimuth
            + parent_floor_azimuth
            + parent_space_azimuth
            + surface_azimuth
        ) % 360
        if self.azimuth < 0:
            self.azimuth += 360

        self.adjacent_to = SurfaceAdjacencyOptions.EXTERIOR
        self.does_cast_shade = self.boolean_map.get(
            self.get_inp(BDL_ExteriorWallKeywords.SHADING_SURFACE)
        )

        self.absorptance_thermal_exterior = self.try_float(
            self.get_inp(BDL_ExteriorWallKeywords.OUTSIDE_EMISS)
        )

        self.absorptance_solar_interior = self.try_float(
            self.get_inp(BDL_ExteriorWallKeywords.INSIDE_SOL_ABS)
        )

        reflectance_visible_interior = self.try_float(
            self.get_inp(BDL_ExteriorWallKeywords.INSIDE_VIS_REFL)
        )
        if reflectance_visible_interior is not None:
            self.absorptance_visible_interior = 1 - reflectance_visible_interior

        construction = self.get_obj(self.get_inp(BDL_ExteriorWallKeywords.CONSTRUCTION))
        if construction is not None:
            self.absorptance_solar_exterior = self.try_float(
                construction.get_inp(BDL_ConstructionKeywords.ABSORPTANCE)
            )

    # def get_output_requests(self):
    #     requests = {}
    #     if (
    #         self.area is None
    #         and self.get_inp(BDL_ExteriorWallKeywords.LOCATION)
    #         == BDL_WallLocationOptions.TOP
    #     ):
    #         requests["Roof Area"] = (1104008, "", self.u_name)
    #     return requests

    def populate_data_group(self):
        """Populate schema structure for exterior wall object."""
        construction = self.get_obj(self.get_inp(BDL_ExteriorWallKeywords.CONSTRUCTION))
        self.construction = construction.construction_data_structure

        optical_property_attributes = [
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
                self.optical_properties[attr] = value

        self.exterior_wall_data_structure = {
            "id": self.u_name,
            "subsurfaces": self.subsurfaces,
            "construction": self.construction,
            "optical_properties": self.optical_properties,
        }

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

        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.exterior_wall_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert exterior wall object into the rpd data structure."""
        zone = rmd.space_map.get(self.parent.u_name)
        zone.surfaces.append(self.exterior_wall_data_structure)
