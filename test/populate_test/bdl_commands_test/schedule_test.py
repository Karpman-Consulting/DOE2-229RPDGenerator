import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.project import RunPeriod, Holidays
from rpd_generator.bdl_structure.bdl_commands.schedule import *


class TestSchedules(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.schedule = Schedule("Schedule 1", self.rmd)

    # @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    # def test_populate_data_with_schedule(self, mock_get_output_data):
    #     mock_get_output_data.return_value = {}
    #
    #     self.schedule.keyword_value_pairs = {}
    #
    #     self.schedule.populate_data_elements()
    #     self.schedule.populate_data_group()
    #
    #     expected_data_structure = {}
    #
    #     self.assertEqual(expected_data_structure, self.schedule.schedule_data_structure)
