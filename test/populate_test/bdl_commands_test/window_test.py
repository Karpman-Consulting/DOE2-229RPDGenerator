import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.exterior_wall import ExteriorWall
from rpd_generator.bdl_structure.bdl_commands.window import *
from rpd_generator.bdl_structure.bdl_commands.glass_type import GlassType
from rpd_generator.bdl_structure.bdl_commands.schedule import Schedule


class TestWindows(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.exterior_wall = ExteriorWall("Exterior Wall 1", self.space, self.rmd)
        self.window = Window("Window 1", self.exterior_wall, self.rmd)
        self.shading_schedule = Schedule("Test shading schedule", self.rmd)
        self.glass_type = GlassType("Test glass type", self.rmd)

        self.rmd.bdl_obj_instances["Test shading schedule"] = self.shading_schedule
        self.rmd.bdl_obj_instances["Test exterior wall"] = self.exterior_wall
        self.rmd.bdl_obj_instances["Test glass type"] = self.glass_type

    def test_populate_data_with_window(self):
        self.glass_type.keyword_value_pairs = {
            BDL_GlassTypeKeywords.GLASS_CONDUCT: "1",
            BDL_GlassTypeKeywords.SHADING_COEF: "2.3",
            BDL_GlassTypeKeywords.VIS_TRANS: "2"
        }
        self.glass_type.populate_data_elements()

        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.FRAME_WIDTH: "2",
            BDL_WindowKeywords.WIN_SHADE_TYPE: BDL_WindowShadeTypes.MOVABLE_INTERIOR,
            BDL_WindowKeywords.GLASS_TYPE: "Test glass type",
            BDL_WindowKeywords.LEFT_FIN_D: "1.0",
            BDL_WindowKeywords.OVERHANG_D: "1.5",
            BDL_WindowKeywords.SHADING_SCHEDULE: "Test shading schedule"
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 44.0,
            "has_shading_sidefins": True,
            "depth_of_overhang": 1.5,
            "has_shading_overhang": True,
            "has_manual_interior_shades": True,
            "u_factor": 1.0,
            "visible_transmittance": 2.0,
            "solar_heat_gain_coefficient": 2.0
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_is_skylight(self):
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.LOCATION: BDL_WallLocationOptions.TOP
        }
        self.exterior_wall.populate_data_elements()

        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.FRAME_WIDTH: "2"
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "SKYLIGHT",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 44.0,
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_no_frame_width(self):
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 0.0,
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_no_width(self):
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.FRAME_WIDTH: "2"
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_bad_fin_depth(self):
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.LEFT_FIN_D: "0.0"
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1"
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_bad_overhang_depth(self):
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.OVERHANG_D: "0.0",
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1"
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    def test_populate_data_with_window_fixed_shade(self):
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.SHADING_SCHEDULE: "Test shading schedule",
            BDL_WindowKeywords.WIN_SHADE_TYPE: BDL_WindowShadeTypes.FIXED_INTERIOR
        }

        self.window.populate_data_elements()
        self.window.populate_data_group()

        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1"
        }

        self.assertEqual(expected_data_structure, self.window.window_data_structure)