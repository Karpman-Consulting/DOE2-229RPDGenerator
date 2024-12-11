import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.construction import Construction
from rpd_generator.bdl_structure.bdl_commands.exterior_wall import ExteriorWall
from rpd_generator.bdl_structure.bdl_commands.window import *
from rpd_generator.bdl_structure.bdl_commands.glass_type import (
    GlassType,
    BDL_GlassTypeKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.schedule import Schedule


class TestWindows(unittest.TestCase):
    @patch("rpd_generator.bdl_structure.bdl_commands.space.Space")
    def setUp(self, MockSpace):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.floor = Floor("Floor 1", self.rmd)
        self.space = MockSpace.return_value
        self.exterior_wall = ExteriorWall("Exterior Wall 1", self.space, self.rmd)
        self.window = Window("Window 1", self.exterior_wall, self.rmd)
        self.shading_schedule = Schedule("Test shading schedule", self.rmd)
        self.glass_type = GlassType("Test glass type", self.rmd)
        self.construction = Construction("Construction 1", self.rmd)

        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1"
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window(self, mock_get_output_data):
        """Tests that all values populate with expected values, given valid inputs"""
        self.glass_type.keyword_value_pairs = {
            BDL_GlassTypeKeywords.TYPE: BDL_GlassTypeOptions.SHADING_COEF,
            BDL_GlassTypeKeywords.GLASS_CONDUCT: "1",
            BDL_GlassTypeKeywords.SHADING_COEF: "2.3",
            BDL_GlassTypeKeywords.VIS_TRANS: "2",
        }
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.WINDOW_TYPE: BDL_WindowTypes.STANDARD,
            BDL_WindowKeywords.GLASS_TYPE: "Test glass type",
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.FRAME_WIDTH: "0.25",
            BDL_WindowKeywords.FRAME_CONDUCT: "0.5",
            BDL_WindowKeywords.WIN_SHADE_TYPE: BDL_WindowShadeTypes.MOVABLE_INTERIOR,
            BDL_WindowKeywords.LEFT_FIN_D: "1.0",
            BDL_WindowKeywords.OVERHANG_D: "1.5",
            BDL_WindowKeywords.SHADING_SCHEDULE: "Test shading schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 3.75,
            "has_shading_sidefins": True,
            "depth_of_overhang": 1.5,
            "has_shading_overhang": True,
            "has_manual_interior_shades": True,
            "u_factor": 0.5632360471070148,
            "visible_transmittance": 2.0,
            "solar_heat_gain_coefficient": 2.0,
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_from_glass_library(self, mock_get_output_data):
        """Tests that all values populate with expected values, given valid inputs"""
        mock_get_output_data.return_value = {"Window - Input - Glass center u-value": 1}

        self.glass_type.keyword_value_pairs = {
            BDL_GlassTypeKeywords.TYPE: BDL_GlassTypeOptions.GLASS_TYPE_CODE
        }
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.WINDOW_TYPE: BDL_WindowTypes.STANDARD,
            BDL_WindowKeywords.GLASS_TYPE: "Test glass type",
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.FRAME_WIDTH: "0.25",
            BDL_WindowKeywords.FRAME_CONDUCT: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 3.75,
            "u_factor": 0.5632360471070148,
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_standard_skylight(self, mock_get_output_data):
        """Tests that window is classified as a SKYLIGHT when it's on an exterior ceiling wall"""
        self.glass_type.keyword_value_pairs = {
            BDL_GlassTypeKeywords.TYPE: BDL_GlassTypeOptions.SHADING_COEF
        }
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.LOCATION: BDL_WallLocationOptions.TOP,
        }
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.WINDOW_TYPE: BDL_WindowTypes.SKYLIGHT_FLAT,
            BDL_WindowKeywords.GLASS_TYPE: "Test glass type",
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.CURB_HEIGHT: "0.25",
            BDL_WindowKeywords.CURB_CONDUCT: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "SKYLIGHT",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 3.75,
            "u_factor": 0.10972130787798991,
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_glass_library_skylight(self, mock_get_output_data):
        """Tests that window u-factor is calculated correctly when the skylight glass type and curb performance comes
        from the glass library"""
        mock_get_output_data.return_value = {
            "Window - Input - Glass center u-value": 1,
        }
        self.glass_type.keyword_value_pairs = {
            BDL_GlassTypeKeywords.TYPE: BDL_GlassTypeOptions.GLASS_TYPE_CODE
        }
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.LOCATION: BDL_WallLocationOptions.TOP,
        }
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.WINDOW_TYPE: BDL_WindowTypes.SKYLIGHT_FLAT,
            BDL_WindowKeywords.GLASS_TYPE: "Test glass type",
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
            BDL_WindowKeywords.CURB_HEIGHT: "0.25",
            BDL_WindowKeywords.CURB_CONDUCT: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "SKYLIGHT",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 3.75,
            "u_factor": 0.5829540792474073,
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_no_frame_width(self, mock_get_output_data):
        """Tests that opaque_area is 0 when no window frame width is specified"""
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.WIDTH: "3",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
            "glazed_area": 12.0,
            "opaque_area": 0.0,
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_no_width(self, mock_get_output_data):
        """Tests that no opaque_area or glazed_area is specified if no width is provided"""
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.HEIGHT: "4",
            BDL_WindowKeywords.FRAME_WIDTH: "2",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "WINDOW",
            "id": "Window 1",
        }
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_bad_fin_depth(self, mock_get_output_data):
        """Tests that has_shading_sidefins is not populated when an invalid fin depth is provided"""
        self.window.keyword_value_pairs = {BDL_WindowKeywords.LEFT_FIN_D: "0.0"}

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "WINDOW", "id": "Window 1"}
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_bad_overhang_depth(self, mock_get_output_data):
        """Tests that has_shading_overhand and overhand_depth are not populated when an invalid overhang depth
        is provided"""
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.OVERHANG_D: "0.0",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "WINDOW", "id": "Window 1"}
        self.assertEqual(expected_data_structure, self.window.window_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_window_fixed_shade(self, mock_get_output_data):
        """Tests that has_manual_interior_shades is not populated when an existing shade is a fixed type"""
        self.window.keyword_value_pairs = {
            BDL_WindowKeywords.SHADING_SCHEDULE: "Test shading schedule",
            BDL_WindowKeywords.WIN_SHADE_TYPE: BDL_WindowShadeTypes.FIXED_INTERIOR,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "WINDOW", "id": "Window 1"}
        self.assertEqual(expected_data_structure, self.window.window_data_structure)
