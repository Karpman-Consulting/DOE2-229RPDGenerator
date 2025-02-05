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
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import Space, BDL_SpaceKeywords
from rpd_generator.bdl_structure.bdl_commands.exterior_wall import *
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_ShadingSurfaceOptions = BDLEnums.bdl_enums["ShadingSurfaceOptions"]


class TestExteriorWall(unittest.TestCase):
    @patch("rpd_generator.bdl_structure.bdl_commands.zone.Zone")
    def setUp(self, MockZone):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.rmd.building_azimuth = 100
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.zone = MockZone.return_value
        self.rmd.space_map = {"Space 1": self.zone}
        self.exterior_wall = ExteriorWall("Exterior Wall 1", self.space, self.rmd)
        self.construction = Construction("Construction 1", self.rmd)
        self.layer = Layer("Layer 1", self.rmd)
        self.material1 = Material("Material 1", self.rmd)
        self.material2 = Material("Material 2", self.rmd)
        self.material3 = Material("Material 3", self.rmd)

    def test_populate_data_with_exterior_wall(self):
        """Tests that Exterior Wall outputs contains expected values, given valid inputs"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "0"}
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.U_VALUE,
            BDL_ConstructionKeywords.U_VALUE: "12.5",
        }
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.AREA: "300",
            BDL_ExteriorWallKeywords.TILT: "5",
            BDL_ExteriorWallKeywords.AZIMUTH: "132",
            BDL_ExteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_ExteriorWallKeywords.OUTSIDE_EMISS: "2.5",
            BDL_ExteriorWallKeywords.INSIDE_SOL_ABS: "3",
            BDL_ExteriorWallKeywords.INSIDE_VIS_REFL: "0.25",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
            "construction": {
                "framing_layers": [],
                "id": "Construction 1",
                "insulation_locations": [],
                "primary_layers": [
                    {"id": "Simplified Material", "r_value": -0.6000000000000001}
                ],
                "r_values": [],
                "u_factor": 4.0,
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.CEILING,
            "tilt": 5.0,
            "azimuth": 2.0,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "does_cast_shade": False,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
                "absorptance_thermal_exterior": 2.5,
                "absorptance_solar_interior": 3.0,
                "absorptance_visible_interior": 0.75,
                "absorptance_solar_exterior": 5.5,
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )

    def test_populate_data_with_exterior_wall_no_area_no_tilt(self):
        """Tests that area is calculated from HEIGHT and WEIGHT is AREA is not provided
        and classification is WALL when no TILT is provided
        and azimuth is not populated if floor, surface, or build azimuths are missing"""
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.HEIGHT: "10",
            BDL_ExteriorWallKeywords.WIDTH: "30",
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
            "construction": {
                "id": "Construction 1",
                "primary_layers": [{"id": "Simplified Material"}],
                "framing_layers": [],
                "insulation_locations": [],
                "r_values": [],
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.WALL,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )

    def test_populate_data_with_exterior_wall_is_floor(self):
        """Tests that classification is FLOOR when TILT exceeds FLOOR_TILT_THRESHOLD (>= 120.0)"""
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.HEIGHT: "10",
            BDL_ExteriorWallKeywords.WIDTH: "30",
            BDL_ExteriorWallKeywords.TILT: "120",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
            "construction": {
                "id": "Construction 1",
                "primary_layers": [{"id": "Simplified Material"}],
                "framing_layers": [],
                "insulation_locations": [],
                "r_values": [],
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.FLOOR,
            "tilt": 120.0,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )

    def test_populate_data_with_exterior_wall_does_cast_shade(self):
        """Tests that does_cast_shade is true if SHADING_SURFACE is 'YES'"""
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.AREA: "300",
            BDL_ExteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.YES,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
            "construction": {
                "id": "Construction 1",
                "primary_layers": [{"id": "Simplified Material"}],
                "framing_layers": [],
                "insulation_locations": [],
                "r_values": [],
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.WALL,
            "does_cast_shade": True,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )

    def test_populate_data_with_exterior_wall_construction_layers_mixed_material_types(
        self,
    ):
        """Tests that construction layers with mixed material types produce expected values"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "0"}
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
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.AREA: "300",
            BDL_ExteriorWallKeywords.TILT: "5",
            BDL_ExteriorWallKeywords.AZIMUTH: "132",
            BDL_ExteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_ExteriorWallKeywords.OUTSIDE_EMISS: "2.5",
            BDL_ExteriorWallKeywords.INSIDE_SOL_ABS: "3",
            BDL_ExteriorWallKeywords.INSIDE_VIS_REFL: "0.25",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
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
                "u_factor": 0.4608294930875576,
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.CEILING,
            "tilt": 5.0,
            "azimuth": 2.0,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "does_cast_shade": False,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
                "absorptance_thermal_exterior": 2.5,
                "absorptance_solar_interior": 3.0,
                "absorptance_visible_interior": 0.75,
                "absorptance_solar_exterior": 5.5,
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )

    def test_populate_data_with_exterior_wall_construction_layers_homogeneous_material_types(
        self,
    ):
        """Tests that construction layers with all material types of RESISTANCE produce expected values"""
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "0"}
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
        self.exterior_wall.keyword_value_pairs = {
            BDL_ExteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_ExteriorWallKeywords.AREA: "300",
            BDL_ExteriorWallKeywords.TILT: "5",
            BDL_ExteriorWallKeywords.AZIMUTH: "132",
            BDL_ExteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_ExteriorWallKeywords.OUTSIDE_EMISS: "2.5",
            BDL_ExteriorWallKeywords.INSIDE_SOL_ABS: "3",
            BDL_ExteriorWallKeywords.INSIDE_VIS_REFL: "0.25",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Exterior Wall 1",
            "subsurfaces": [],
            "construction": {
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
                "framing_layers": [],
                "r_values": [],
                "u_factor": 0.4608294930875576,
            },
            "area": 300.0,
            "classification": SurfaceClassificationOptions.CEILING,
            "tilt": 5.0,
            "azimuth": 2.0,
            "adjacent_to": SurfaceAdjacencyOptions.EXTERIOR,
            "does_cast_shade": False,
            "optical_properties": {
                "id": "Exterior Wall 1 OpticalProps",
                "absorptance_thermal_exterior": 2.5,
                "absorptance_solar_interior": 3.0,
                "absorptance_visible_interior": 0.75,
                "absorptance_solar_exterior": 5.5,
            },
        }
        self.assertEqual(
            expected_data_structure, self.exterior_wall.exterior_wall_data_structure
        )
