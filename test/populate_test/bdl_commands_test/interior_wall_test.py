import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.construction import Construction
from rpd_generator.bdl_structure.bdl_commands.interior_wall import *


BDL_ShadingSurfaceOptions = BDLEnums.bdl_enums["ShadingSurfaceOptions"]


class TestInteriorWalls(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.rmd.building_azimuth = 100
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.interior_wall = InteriorWall("Interior Wall 1", self.floor, self.rmd)
        self.construction = Construction("Construction 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)

        self.rmd.bdl_obj_instances["Test Construction"] = self.construction
        self.rmd.bdl_obj_instances["Space 1"] = self.space

    def test_populate_data_with_interior_wall(self):
        """Tests that Interior Wall outputs contains expected values, given valid inputs"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}

        self.floor.populate_data_elements()

        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.STANDARD,
            BDL_InteriorWallKeywords.AREA: "200",
            BDL_InteriorWallKeywords.TILT: "10",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
            BDL_InteriorWallKeywords.AZIMUTH: "30",
            BDL_InteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_InteriorWallKeywords.INSIDE_SOL_ABS: [1.0, 2.0],
            BDL_InteriorWallKeywords.INSIDE_VIS_REFL: [0.5, 0.6],
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "optical_properties": {
                "absorptance_solar_interior": 1.0,
                "absorptance_solar_exterior": 2.0,
                "absorptance_visible_interior": 0.5,
                "absorptance_visible_exterior": 0.4,
            },
            "adjacent_to": "INTERIOR",
            "area": 200.0,
            "tilt": 10.0,
            "classification": "CEILING",
            "does_cast_shade": False,
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_air_wall_adjacency(self):
        """Tests that AIR wall adjacency type outputs minimal results"""
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.AIR,
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "optical_properties": {},
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_internal_wall_adjacency(self):
        """Tests that INTERNAL wall adjacency type outputs minimal results"""
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.AIR,
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "optical_properties": {},
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_adiabatic_wall_adjacency(self):
        """Tests that ADIABATIC wall adjacency type outputs IDENTICAL for 'adjacent_to' value
        and that when a WIDTH and HEIGHT are provided instead of an AREA, that the AREA is accurately calculated
        and that a TILT over the FLOOR_TILT_THRESHOLD classifies the wall as a FLOOR"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "10"}

        self.floor.populate_data_elements()

        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.ADIABATIC,
            BDL_InteriorWallKeywords.HEIGHT: "10",
            BDL_InteriorWallKeywords.WIDTH: "20",
            BDL_InteriorWallKeywords.TILT: "120",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
            BDL_InteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_InteriorWallKeywords.INSIDE_SOL_ABS: [1.0, 2.0],
            BDL_InteriorWallKeywords.INSIDE_VIS_REFL: [0.5, 0.6],
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "optical_properties": {
                "absorptance_solar_interior": 1.0,
                "absorptance_solar_exterior": 2.0,
                "absorptance_visible_interior": 0.5,
                "absorptance_visible_exterior": 0.4,
            },
            "adjacent_to": "IDENTICAL",
            "area": 200.0,
            "tilt": 120.0,
            "classification": "FLOOR",
            "does_cast_shade": False,
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_no_tilt_wall_type(self):
        """Tests that no provided TILT will lead to a WALL classification"""
        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.AREA: "200",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {},
            "optical_properties": {},
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall(self):
        """Tests that missing azimuth input provides no azimuth output"""
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "0",
        }

        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.STANDARD,
            BDL_InteriorWallKeywords.AREA: "200",
            BDL_InteriorWallKeywords.TILT: "10",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
            BDL_InteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_InteriorWallKeywords.INSIDE_SOL_ABS: [1.0, 2.0],
            BDL_InteriorWallKeywords.INSIDE_VIS_REFL: [0.5, 0.6],
        }

        self.interior_wall.populate_data_elements()
        self.interior_wall.populate_data_group()

        expected_data_structure = {
            "id": "Interior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [{"id": "Simplified Material"}],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.0,
            },
            "optical_properties": {
                "absorptance_solar_interior": 1.0,
                "absorptance_solar_exterior": 2.0,
                "absorptance_visible_interior": 0.5,
                "absorptance_visible_exterior": 0.4,
            },
            "adjacent_to": "INTERIOR",
            "area": 200.0,
            "tilt": 10.0,
            "classification": "CEILING",
            "does_cast_shade": False,
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )
