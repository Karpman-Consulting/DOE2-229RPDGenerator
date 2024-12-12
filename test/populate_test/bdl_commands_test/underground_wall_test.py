import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.construction import Construction
from rpd_generator.bdl_structure.bdl_commands.material_layers import (
    Layer,
    Material,
    BDL_MaterialKeywords,
    BDL_MaterialTypes,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.underground_wall import *


BDL_ShadingSurfaceOptions = BDLEnums.bdl_enums["ShadingSurfaceOptions"]


class TestUndergroundWalls(unittest.TestCase):
    @patch("rpd_generator.bdl_structure.bdl_commands.zone.Zone")
    def setUp(self, MockZone):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.rmd.building_azimuth = 100
        self.floor = Floor("Floor 1", self.rmd)
        self.zone = MockZone.return_value
        self.space = Space("Space 1", self.floor, self.rmd)
        self.rmd.space_map = {"Space 1": self.zone}
        self.underground_wall = BelowGradeWall(
            "Below Grade Wall 1", self.space, self.rmd
        )
        self.construction = Construction("Construction 1", self.rmd)
        self.layer = Layer("Layer 1", self.rmd)
        self.material1 = Material("Material 1", self.rmd)
        self.material2 = Material("Material 2", self.rmd)
        self.material3 = Material("Material 3", self.rmd)

    def test_populate_data_with_underground_wall(self):
        """Tests that Underground Wall outputs contains expected values, given valid inputs"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "12.5",
        }
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_UndergroundWallKeywords.AREA: "400",
            BDL_UndergroundWallKeywords.TILT: "10",
            BDL_UndergroundWallKeywords.AZIMUTH: "110",
            BDL_UndergroundWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.YES,
            BDL_UndergroundWallKeywords.INSIDE_SOL_ABS: 2.0,
            BDL_UndergroundWallKeywords.INSIDE_VIS_REFL: 0.5,
        }

        self.rmd.populate_rmd_data(testing=True)
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
                "primary_layers": [
                    {"id": "Simplified Material", "r_value": -0.6000000000000001}
                ],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 12.5,
            },
            "adjacent_to": "GROUND",
            "azimuth": 350.0,
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
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_UndergroundWallKeywords.HEIGHT: "10",
            BDL_UndergroundWallKeywords.WIDTH: "40",
            BDL_UndergroundWallKeywords.TILT: "120",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Below Grade Wall 1",
            "area": 400.0,
            "tilt": 120.0,
            "classification": "FLOOR",
            "optical_properties": {},
            "construction": {
                "id": "Construction 1",
                "surface_construction_input_option": "SIMPLIFIED",
                "primary_layers": [{"id": "Simplified Material"}],
                "framing_layers": [],
                "insulation_locations": [],
                "r_values": [],
            },
            "adjacent_to": "GROUND",
        }
        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )

    def test_populate_data_with_underground_wall_is_wall_classification(self):
        """Tests that when no TILT is provided, the wall is classified as a WALL"""
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_UndergroundWallKeywords.AREA: "400",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Below Grade Wall 1",
            "area": 400.0,
            "classification": "WALL",
            "optical_properties": {},
            "construction": {
                "id": "Construction 1",
                "surface_construction_input_option": "SIMPLIFIED",
                "primary_layers": [{"id": "Simplified Material"}],
                "framing_layers": [],
                "insulation_locations": [],
                "r_values": [],
            },
            "adjacent_to": "GROUND",
        }
        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )

    def test_populate_data_with_interior_wall_construction_layers_mixed_material_types(
        self,
    ):
        """Tests that construction layers with mixed material types produce expected values
        and that surface_construction_input_option is LAYERS when >= 1 detailed material type is provided
        """
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.material1.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.PROPERTIES,
            BDL_MaterialKeywords.THICKNESS: "2",
            BDL_MaterialKeywords.CONDUCTIVITY: "3",
            BDL_MaterialKeywords.DENSITY: "20.1",
            BDL_MaterialKeywords.SPECIFIC_HEAT: "4",
        }
        self.material2.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "2",
        }
        self.material3.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "3",
        }
        self.layer.keyword_value_pairs = {
            BDL_LayerKeywords.MATERIAL: [
                "Material 1",
                "Material 2",
                "Material 3",
            ]
        }
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.LAYERS,
            BDL_ConstructionKeywords.LAYERS: "Layer 1",
            BDL_ConstructionKeywords.U_VALUE: "0.5",
        }
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_UndergroundWallKeywords.AREA: "400",
            BDL_UndergroundWallKeywords.TILT: "10",
            BDL_UndergroundWallKeywords.AZIMUTH: "110",
            BDL_UndergroundWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.YES,
            BDL_UndergroundWallKeywords.INSIDE_SOL_ABS: 2.0,
            BDL_UndergroundWallKeywords.INSIDE_VIS_REFL: 0.5,
        }

        self.rmd.populate_rmd_data(testing=True)
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
                "primary_layers": [
                    {
                        "id": "Material 1",
                        "thickness": 2.0,
                        "thermal_conductivity": 3.0,
                        "specific_heat": 4.0,
                        "density": 20.1,
                    },
                    {
                        "id": "Material 2",
                        "r_value": 2.0,
                    },
                    {
                        "id": "Material 3",
                        "r_value": 3.0,
                    },
                ],
                "r_values": [],
                "surface_construction_input_option": "LAYERS",
                "u_factor": 0.5,
            },
            "adjacent_to": "GROUND",
            "azimuth": 350.0,
            "does_cast_shade": True,
        }
        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )

    def test_populate_data_with_interior_wall_construction_layers_all_no_mass(
        self,
    ):
        """Tests that construction layers with all material types of RESISTANCE produce expected values
        and that surface_construction_input_option is SIMPLIFIED no detailed material types are provided
        """
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.material1.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "1",
        }
        self.material2.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "2",
        }
        self.material3.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "3",
        }
        self.layer.keyword_value_pairs = {
            BDL_LayerKeywords.MATERIAL: [
                "Material 1",
                "Material 2",
                "Material 3",
            ]
        }
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.LAYERS,
            BDL_ConstructionKeywords.LAYERS: "Layer 1",
            BDL_ConstructionKeywords.U_VALUE: "0.5",
        }
        self.underground_wall.keyword_value_pairs = {
            BDL_UndergroundWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_UndergroundWallKeywords.AREA: "400",
            BDL_UndergroundWallKeywords.TILT: "10",
            BDL_UndergroundWallKeywords.AZIMUTH: "110",
            BDL_UndergroundWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.YES,
            BDL_UndergroundWallKeywords.INSIDE_SOL_ABS: 2.0,
            BDL_UndergroundWallKeywords.INSIDE_VIS_REFL: 0.5,
        }

        self.rmd.populate_rmd_data(testing=True)
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
                "primary_layers": [
                    {
                        "id": "Material 1",
                        "r_value": 1.0,
                    },
                    {
                        "id": "Material 2",
                        "r_value": 2.0,
                    },
                    {
                        "id": "Material 3",
                        "r_value": 3.0,
                    },
                ],
                "r_values": [],
                "surface_construction_input_option": "SIMPLIFIED",
                "u_factor": 0.5,
            },
            "adjacent_to": "GROUND",
            "azimuth": 350.0,
            "does_cast_shade": True,
        }
        self.assertEqual(
            expected_data_structure,
            self.underground_wall.underground_wall_data_structure,
        )
