import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.pump import *


class TestPumps(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.pump = Pump("Test Pump", self.rmd)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_pump(self, mock_get_output_data):
        """Tests that Pump outputs contains expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Power (kW)": 125,
            "Pump - Mechanical Eff (frac)": 0.75,
            "Pump - Motor Eff (frac)": 0.80,
            "Pump - Flow (gal/min)": 30,
        }

        self.pump.keyword_value_pairs = {
            BDL_PumpKeywords.NUMBER: "2",
            BDL_PumpKeywords.PUMP_KW: "100",
            BDL_PumpKeywords.HEAD: "5",
            BDL_PumpKeywords.CAP_CTRL: BDL_PumpCapacityControlOptions.ONE_SPEED_PUMP,
            BDL_PumpKeywords.FLOW: "2.0",
        }

        self.pump.populate_data_elements()
        self.pump.populate_data_group()

        expected_data_structures = [
            {
                "id": "Test Pump",
                "output_validation_points": [],
                "specification_method": "SIMPLE",
                "design_electric_power": 100.0,
                "design_head": 5.0,
                "impeller_efficiency": 0.75,
                "motor_efficiency": 0.8,
                "design_flow": 30,
                "speed_control": "FIXED_SPEED",
                "is_flow_sized_based_on_design_day": False,
            },
            {
                "id": "Test Pump 1",
                "output_validation_points": [],
                "specification_method": "SIMPLE",
                "design_electric_power": 100.0,
                "design_head": 5.0,
                "impeller_efficiency": 0.75,
                "motor_efficiency": 0.8,
                "design_flow": 30,
                "speed_control": "FIXED_SPEED",
                "is_flow_sized_based_on_design_day": False,
            },
        ]

        self.assertEqual(expected_data_structures, self.pump.pump_data_structures)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_pump_detailed(self, mock_get_output_data):
        """Tests that specification_method is DETAILED when no PUMP_KW value is provided"""
        mock_get_output_data.return_value = {
            "Pump - Power (kW)": 125,
        }

        self.pump.keyword_value_pairs = {
            BDL_PumpKeywords.NUMBER: "1",
            BDL_PumpKeywords.HEAD: "5",
            BDL_PumpKeywords.CAP_CTRL: BDL_PumpCapacityControlOptions.ONE_SPEED_PUMP,
            BDL_PumpKeywords.FLOW: "2.0",
        }

        self.pump.populate_data_elements()
        self.pump.populate_data_group()

        expected_data_structures = [
            {
                "id": "Test Pump",
                "output_validation_points": [],
                "specification_method": "DETAILED",
                "design_electric_power": 125.0,
                "design_head": 5.0,
                "speed_control": "FIXED_SPEED",
                "is_flow_sized_based_on_design_day": False,
            }
        ]

        self.assertEqual(expected_data_structures, self.pump.pump_data_structures)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_pump_two_speed(self, mock_get_output_data):
        """Tests that speed_control is TWO_SPEED when capacity control value is TWO_SPEED_PUMP"""
        mock_get_output_data.return_value = {
            "Pump - Power (kW)": 125,
        }

        self.pump.keyword_value_pairs = {
            BDL_PumpKeywords.NUMBER: "1",
            BDL_PumpKeywords.HEAD: "5",
            BDL_PumpKeywords.CAP_CTRL: BDL_PumpCapacityControlOptions.TWO_SPEED_PUMP,
            BDL_PumpKeywords.FLOW: "2.0",
        }

        self.pump.populate_data_elements()
        self.pump.populate_data_group()

        expected_data_structures = [
            {
                "id": "Test Pump",
                "output_validation_points": [],
                "specification_method": "DETAILED",
                "design_electric_power": 125.0,
                "design_head": 5.0,
                "speed_control": "TWO_SPEED",
                "is_flow_sized_based_on_design_day": False,
            }
        ]

        self.assertEqual(expected_data_structures, self.pump.pump_data_structures)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_pump_variable_speed(self, mock_get_output_data):
        """Tests that speed_control is VARIABLE_SPEED when capacity control value is VARIABLE_SPEED_PUMP"""
        mock_get_output_data.return_value = {
            "Pump - Power (kW)": 125,
        }

        self.pump.keyword_value_pairs = {
            BDL_PumpKeywords.NUMBER: "1",
            BDL_PumpKeywords.HEAD: "5",
            BDL_PumpKeywords.CAP_CTRL: BDL_PumpCapacityControlOptions.VAR_SPEED_PUMP,
            BDL_PumpKeywords.FLOW: "2.0",
        }

        self.pump.populate_data_elements()
        self.pump.populate_data_group()

        expected_data_structures = [
            {
                "id": "Test Pump",
                "output_validation_points": [],
                "specification_method": "DETAILED",
                "design_electric_power": 125.0,
                "design_head": 5.0,
                "speed_control": "VARIABLE_SPEED",
                "is_flow_sized_based_on_design_day": False,
            }
        ]

        self.assertEqual(expected_data_structures, self.pump.pump_data_structures)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_pump_design_day(self, mock_get_output_data):
        """Tests that is_flow_sized_based_on_design_day is True when no FLOW value is provided"""
        mock_get_output_data.return_value = {
            "Pump - Power (kW)": 125,
        }

        self.pump.keyword_value_pairs = {
            BDL_PumpKeywords.NUMBER: "1",
            BDL_PumpKeywords.HEAD: "5",
            BDL_PumpKeywords.CAP_CTRL: BDL_PumpCapacityControlOptions.VAR_SPEED_PUMP,
        }

        self.pump.populate_data_elements()
        self.pump.populate_data_group()

        expected_data_structures = [
            {
                "id": "Test Pump",
                "output_validation_points": [],
                "specification_method": "DETAILED",
                "design_electric_power": 125.0,
                "design_head": 5.0,
                "speed_control": "VARIABLE_SPEED",
                "is_flow_sized_based_on_design_day": True,
            }
        ]

        self.assertEqual(expected_data_structures, self.pump.pump_data_structures)
