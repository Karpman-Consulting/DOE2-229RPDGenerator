import unittest

from rpd_generator.bdl_structure.bdl_commands.construction import Construction
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.underground_wall import *


BDL_ShadingSurfaceOptions = BDLEnums.bdl_enums["ShadingSurfaceOptions"]


class TestUndergroundWalls(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.rmd.building_azimuth = 100
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.underground_wall = BelowGradeWall(
            "Below Grade Wall 1", self.space, self.rmd
        )
        self.construction = Construction("Construction 1", self.rmd)

        self.rmd.bdl_obj_instances["Test Construction"] = self.construction

    def test_populate_data_with_underground_wall(self):
        """Tests that Underground Wall outputs contains expected values, given valid inputs"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}

        self.floor.populate_data_elements()

        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.AREA: "400",
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_UndergroundWallKeywords.TILT: "10",
            BDL_UndergroundWallKeywords.AZIMUTH: "110",
            BDL_UndergroundWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.YES,
            BDL_UndergroundWallKeywords.INSIDE_SOL_ABS: 2.0,
            BDL_UndergroundWallKeywords.INSIDE_VIS_REFL: 0.5,
        }

        self.underground_wall.populate_data_elements()
        self.underground_wall.populate_data_group()

        expected_data_structure = {
            "id": "Below Grade Wall 1",
            "area": 400.0,
            "tilt": 10.0,
            "classification": "CEILING",
            "optical_properties": {
                "absorptance_solar_interior": 2.0,
                "absorptance_visible_interior": 0.5,
            },
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "adjacent_to": "GROUND",
            "azimuth": 340.0,
            "does_cast_shade": True,
        }

        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )

    def test_populate_data_with_underground_wall_no_area_provided(self):
        """Tests that when no AREA is provided, an area is properly calculated from HEIGHT and WIDTH
        and that a TILT over the FLOOR_TILT_THRESHOLD produces a wall classification of FLOOR
        and that when any floor, surface, or wall azimuth is provided, there is no output AZIMUTH
        """
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.HEIGHT: "10",
            BDL_UndergroundWallKeywords.WIDTH: "40",
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_UndergroundWallKeywords.TILT: "120",
        }

        self.underground_wall.populate_data_elements()
        self.underground_wall.populate_data_group()

        expected_data_structure = {
            "id": "Below Grade Wall 1",
            "area": 400.0,
            "tilt": 10.0,
            "classification": "FLOOR",
            "optical_properties": {},
            "construction": {},
            "adjacent_to": "GROUND",
        }

        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )

    def test_populate_data_with_underground_wall_is_wall_classification(self):
        """Tests that when no TILT is provided, the wall is classified as a WALL"""
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.AREA: "400",
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Test Construction",
        }

        self.underground_wall.populate_data_elements()
        self.underground_wall.populate_data_group()

        expected_data_structure = {
            "id": "Below Grade Wall 1",
            "area": 400.0,
            "classification": "WALL",
            "optical_properties": {},
            "construction": {},
            "adjacent_to": "GROUND",
        }

        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )
