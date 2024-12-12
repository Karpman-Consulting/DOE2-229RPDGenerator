import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.circulation_loop import (
    CirculationLoop,
    BDL_CirculationLoopKeywords,
    BDL_CirculationLoopTypes,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.heat_rejection import *
from rpd_generator.bdl_structure.bdl_commands.pump import (
    Pump,
    BDL_PumpKeywords,
)


class TestHeatRejection(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.heat_rejection = HeatRejection("Heat Rejection 1", self.rmd)
        self.loop = CirculationLoop("Loop 1", self.rmd)
        self.pump = Pump("Pump 1", self.rmd)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_heat_rejection(self, mock_get_output_data):
        """Tests that heat_rejection outputs expected values, given valid inputs"""
        mock_get_output_data.return_value = {"Cooling Tower - Flow (gal/min)": 80}
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "2"}
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "62",
        }
        self.heat_rejection.keyword_value_pairs = {
            BDL_HeatRejectionKeywords.CW_LOOP: "Loop 1",
            BDL_HeatRejectionKeywords.TYPE: BDL_HeatRejectionTypes.OPEN_TWR,
            BDL_HeatRejectionKeywords.CAPACITY_CTRL: BDL_HeatRejectionFanSpeedControlOptions.ONE_SPEED_FAN,
            BDL_HeatRejectionKeywords.RATED_RANGE: "45.6",
            BDL_HeatRejectionKeywords.RATED_APPROACH: "13",
            BDL_HeatRejectionKeywords.DESIGN_WETBULB: "68.5",
            BDL_HeatRejectionKeywords.CW_PUMP: "Pump 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Heat Rejection 1",
            "loop": "Loop 1",
            "type": "OPEN_CIRCUIT_COOLING_TOWER",
            "fan_speed_control": "CONSTANT",
            "range": 45.6,
            "approach": 13.0,
            "design_wetbulb_temperature": 68.5,
            "rated_water_flowrate": 80.0,
            "leaving_water_setpoint_temperature": 62.0,
        }
        self.assertEqual(
            expected_data_structure, self.heat_rejection.heat_rejection_data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_heat_rejection_no_circulation_loop(
        self, mock_get_output_data
    ):
        """Tests that heat_rejection outputs expected values, given valid inputs with no circulation_loop"""
        mock_get_output_data.return_value = {"Cooling Tower - Flow (gal/min)": 80}
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "2"}
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "62",
        }
        self.heat_rejection.keyword_value_pairs = {
            BDL_HeatRejectionKeywords.TYPE: BDL_HeatRejectionTypes.OPEN_TWR,
            BDL_HeatRejectionKeywords.CAPACITY_CTRL: BDL_HeatRejectionFanSpeedControlOptions.ONE_SPEED_FAN,
            BDL_HeatRejectionKeywords.RATED_RANGE: "45.6",
            BDL_HeatRejectionKeywords.RATED_APPROACH: "13",
            BDL_HeatRejectionKeywords.DESIGN_WETBULB: "68.5",
            BDL_HeatRejectionKeywords.CW_PUMP: "Pump 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Heat Rejection 1",
            "type": "OPEN_CIRCUIT_COOLING_TOWER",
            "fan_speed_control": "CONSTANT",
            "range": 45.6,
            "approach": 13.0,
            "design_wetbulb_temperature": 68.5,
            "rated_water_flowrate": 80.0,
        }
        self.assertEqual(
            expected_data_structure, self.heat_rejection.heat_rejection_data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_heat_rejection_no_pump(self, mock_get_output_data):
        """Tests that heat_rejection outputs expected values, given valid inputs and no pump"""
        mock_get_output_data.return_value = {"Cooling Tower - Flow (gal/min)": 80}
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "2"}
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "62",
        }
        self.heat_rejection.keyword_value_pairs = {
            BDL_HeatRejectionKeywords.CW_LOOP: "Loop 1",
            BDL_HeatRejectionKeywords.TYPE: BDL_HeatRejectionTypes.OPEN_TWR,
            BDL_HeatRejectionKeywords.CAPACITY_CTRL: BDL_HeatRejectionFanSpeedControlOptions.ONE_SPEED_FAN,
            BDL_HeatRejectionKeywords.RATED_RANGE: "45.6",
            BDL_HeatRejectionKeywords.RATED_APPROACH: "13",
            BDL_HeatRejectionKeywords.DESIGN_WETBULB: "68.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Heat Rejection 1",
            "loop": "Loop 1",
            "type": "OPEN_CIRCUIT_COOLING_TOWER",
            "fan_speed_control": "CONSTANT",
            "range": 45.6,
            "approach": 13.0,
            "design_wetbulb_temperature": 68.5,
            "rated_water_flowrate": 80.0,
            "leaving_water_setpoint_temperature": 62.0,
        }
        self.assertEqual(
            expected_data_structure, self.heat_rejection.heat_rejection_data_structure
        )
