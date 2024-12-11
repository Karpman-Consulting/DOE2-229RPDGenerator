import unittest

from rpd_generator.bdl_structure.bdl_commands.material_layers import (
    Layer,
    Material,
    BDL_MaterialKeywords,
    BDL_MaterialTypes,
)
from rpd_generator.bdl_structure.bdl_commands.zone import Zone
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.system import System
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
        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)
        self.rmd.space_map = {"Space 1": self.zone}
        self.interior_wall = InteriorWall("Interior Wall 1", self.space, self.rmd)
        self.construction = Construction("Construction 1", self.rmd)
        self.layer = Layer("Layer 1", self.rmd)
        self.material1 = Material("Material 1", self.rmd)
        self.material2 = Material("Material 2", self.rmd)
        self.material3 = Material("Material 3", self.rmd)

        self.rmd.bdl_obj_instances["Test Construction"] = self.construction
        self.rmd.bdl_obj_instances["Test Space"] = self.space
        self.rmd.bdl_obj_instances["Test Layer"] = self.layer
        self.rmd.bdl_obj_instances["Test Material 1"] = self.material1
        self.rmd.bdl_obj_instances["Test Material 2"] = self.material2
        self.rmd.bdl_obj_instances["Test Material 3"] = self.material3

    def test_populate_data_with_interior_wall(self):
        """Tests that Interior Wall outputs contains expected values, given valid inputs"""
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
            "adjacent_zone": "Zone 1",
            "area": 200.0,
            "tilt": 10.0,
            "azimuth": 270.0,
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

    def test_populate_data_with_interior_wall_no_azimuth(self):
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
            "adjacent_zone": "Zone 1",
            "area": 200.0,
            "tilt": 10.0,
            "classification": "CEILING",
            "does_cast_shade": False,
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_construction_layers_mixed_material_types(
        self,
    ):
        """Tests that construction layers with mixed material types produce expected values
        and that surface_construction_input_option is LAYERS when >= 1 detailed material type is provided
        """
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.floor.populate_data_elements()

        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.space.populate_data_elements()

        self.material1.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.PROPERTIES,
            BDL_MaterialKeywords.THICKNESS: "2",
            BDL_MaterialKeywords.CONDUCTIVITY: "3",
            BDL_MaterialKeywords.DENSITY: "20.1",
            BDL_MaterialKeywords.SPECIFIC_HEAT: "4",
        }
        self.material1.populate_data_elements()
        self.material1.populate_data_group()

        self.material2.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "2",
        }
        self.material2.populate_data_elements()
        self.material2.populate_data_group()

        self.material3.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "3",
        }
        self.material3.populate_data_elements()
        self.material3.populate_data_group()

        self.layer.keyword_value_pairs = {
            BDL_LayerKeywords.MATERIAL: [
                "Test Material 1",
                "Test Material 2",
                "Test Material 3",
            ]
        }
        self.layer.populate_data_elements()

        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.LAYERS,
            BDL_ConstructionKeywords.LAYERS: "Test Layer",
            BDL_ConstructionKeywords.U_VALUE: "0.5",
        }
        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.STANDARD,
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
            BDL_InteriorWallKeywords.AREA: "300",
            BDL_InteriorWallKeywords.TILT: "5",
            BDL_InteriorWallKeywords.AZIMUTH: "132",
            BDL_InteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_InteriorWallKeywords.INSIDE_SOL_ABS: "3",
            BDL_InteriorWallKeywords.INSIDE_VIS_REFL: "0.25",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
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
            "area": 300.0,
            "classification": SurfaceClassificationOptions.CEILING,
            "tilt": 5.0,
            "azimuth": 12.0,
            "adjacent_to": SurfaceAdjacencyOptions.INTERIOR,
            "adjacent_zone": "Zone 1",
            "does_cast_shade": False,
            "optical_properties": {},
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )

    def test_populate_data_with_interior_wall_construction_layers_homogeneous_material_types(
        self,
    ):
        """Tests that construction layers with all material types of RESISTANCE produce expected values
        and that surface_construction_input_option is SIMPLIFIED no detailed material types are provided
        """
        self.floor.keyword_value_pairs = {BDL_FloorKeywords.AZIMUTH: "130"}
        self.floor.populate_data_elements()

        self.space.keyword_value_pairs = {BDL_SpaceKeywords.AZIMUTH: "10"}
        self.space.populate_data_elements()

        self.material1.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "1",
        }
        self.material1.populate_data_elements()
        self.material1.populate_data_group()

        self.material2.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "2",
        }
        self.material2.populate_data_elements()
        self.material2.populate_data_group()

        self.material3.keyword_value_pairs = {
            BDL_MaterialKeywords.TYPE: BDL_MaterialTypes.RESISTANCE,
            BDL_MaterialKeywords.RESISTANCE: "3",
        }
        self.material3.populate_data_elements()
        self.material3.populate_data_group()

        self.layer.keyword_value_pairs = {
            BDL_LayerKeywords.MATERIAL: [
                "Test Material 1",
                "Test Material 2",
                "Test Material 3",
            ]
        }
        self.layer.populate_data_elements()

        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.ABSORPTANCE: "5.5",
            BDL_ConstructionKeywords.TYPE: BDL_ConstructionTypes.LAYERS,
            BDL_ConstructionKeywords.LAYERS: "Test Layer",
            BDL_ConstructionKeywords.U_VALUE: "0.5",
        }
        self.construction.populate_data_elements()
        self.construction.populate_data_group()

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.STANDARD,
            BDL_InteriorWallKeywords.NEXT_TO: "Space 1",
            BDL_InteriorWallKeywords.AREA: "300",
            BDL_InteriorWallKeywords.TILT: "5",
            BDL_InteriorWallKeywords.AZIMUTH: "132",
            BDL_InteriorWallKeywords.SHADING_SURFACE: BDL_ShadingSurfaceOptions.NO,
            BDL_InteriorWallKeywords.INSIDE_SOL_ABS: "3",
            BDL_InteriorWallKeywords.INSIDE_VIS_REFL: "0.25",
            BDL_InteriorWallKeywords.CONSTRUCTION: "Test Construction",
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
                "primary_layers": [
                    {
                        "id": "Simplified Material",
                    },
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
            "area": 300.0,
            "classification": SurfaceClassificationOptions.CEILING,
            "tilt": 5.0,
            "azimuth": 12.0,
            "adjacent_to": SurfaceAdjacencyOptions.INTERIOR,
            "adjacent_zone": "Zone 1",
            "does_cast_shade": False,
            "optical_properties": {},
        }

        self.assertEqual(
            expected_data_structure, self.interior_wall.interior_wall_data_structure
        )
