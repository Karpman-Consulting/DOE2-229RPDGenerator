import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.bdl_structure.bdl_commands.interior_wall import (
    InteriorWall,
    BDL_InteriorWallKeywords,
    BDL_InteriorWallTypes,
)
from rpd_generator.bdl_structure.bdl_commands.construction import (
    Construction,
    BDL_ConstructionKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.door import *


class TestDoor(unittest.TestCase):
    @patch("rpd_generator.bdl_structure.bdl_commands.system.System")
    @patch("rpd_generator.bdl_structure.bdl_commands.zone.Zone")
    @patch("rpd_generator.bdl_structure.bdl_commands.exterior_wall.ExteriorWall")
    def setUp(self, MockSystem, MockZone, MockExteriorWall):
        self.maxDiff = None

        self.rpd = RulesetProjectDescription("Test RPD")
        self.rmd = RulesetModelDescription("Test RMD", self.rpd)
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = MockSystem.return_value
        self.zone = MockZone.return_value
        self.rmd.space_map = {"Space 1": self.zone}
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.exterior_wall = MockExteriorWall.return_value
        self.door = Door("Door 1", self.exterior_wall, self.rmd)
        self.construction = Construction("Construction 1", self.rmd)

    def test_populate_data_with_door(self):
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.U_VALUE: 0.5,
        }
        self.door.keyword_value_pairs = {
            BDL_DoorKeywords.CONSTRUCTION: "Construction 1",
            BDL_DoorKeywords.HEIGHT: 7,
            BDL_DoorKeywords.WIDTH: 4,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "DOOR",
            "id": "Door 1",
            "opaque_area": 28,
            "glazed_area": 0,
            "u_factor": 0.2976190476190476,
        }
        self.assertEqual(expected_data_structure, self.door.door_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    @patch("rpd_generator.bdl_structure.bdl_commands.zone.Zone")
    def test_populate_data_with_interior_door(self, mock_get_output_data, MockZone):
        # Create additional objects for this test specifically
        space2 = Space("Space 2", self.floor, self.rmd)
        zone2 = MockZone.return_value
        self.rmd.space_map["Space 2"] = zone2
        self.interior_wall = InteriorWall("Interior Wall 1", self.space, self.rmd)

        self.interior_wall.keyword_value_pairs = {
            BDL_InteriorWallKeywords.CONSTRUCTION: "Construction 1",
            BDL_InteriorWallKeywords.INT_WALL_TYPE: BDL_InteriorWallTypes.STANDARD,
            BDL_InteriorWallKeywords.NEXT_TO: "Space 2",
        }
        self.construction.keyword_value_pairs = {
            BDL_ConstructionKeywords.U_VALUE: 0.5,
        }
        self.door.keyword_value_pairs = {
            BDL_DoorKeywords.CONSTRUCTION: "Construction 1",
            BDL_DoorKeywords.HEIGHT: 7,
            BDL_DoorKeywords.WIDTH: 4,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "classification": "DOOR",
            "id": "Door 1",
            "opaque_area": 28,
            "glazed_area": 0,
            "u_factor": 0.2976190476190476,
        }
        self.assertEqual(expected_data_structure, self.door.door_data_structure)

    def test_populate_data_with_door_no_height(self):
        self.door.keyword_value_pairs = {BDL_DoorKeywords.WIDTH: 4}

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "DOOR", "id": "Door 1"}
        self.assertEqual(expected_data_structure, self.door.door_data_structure)

    def test_populate_data_with_door_no_width(self):
        self.door.keyword_value_pairs = {BDL_DoorKeywords.HEIGHT: 7}

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "DOOR", "id": "Door 1"}
        self.assertEqual(expected_data_structure, self.door.door_data_structure)

    def test_populate_data_with_door_no_height_or_width(self):
        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {"classification": "DOOR", "id": "Door 1"}
        self.assertEqual(expected_data_structure, self.door.door_data_structure)
