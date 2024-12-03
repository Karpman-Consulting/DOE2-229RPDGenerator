import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import *


class TestCHWLoop(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.circulation_loop = CirculationLoop("CHW Loop 1", self.rmd)

    # @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    # def test_populate_data_with_chw_loop(self, mock_get_output_data):
    #     mock_get_output_data.return_value = {}
    #
    #     self.circulation_loop.keyword_value_pairs = {}
    #
    #     self.circulation_loop.populate_data_elements()
    #     self.circulation_loop.populate_data_group()
    #
    #     expected_data_structure = {}
    #
    #     self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)
