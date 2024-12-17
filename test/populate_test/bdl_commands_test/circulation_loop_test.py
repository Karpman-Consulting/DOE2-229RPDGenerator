import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.pump import (
    Pump,
    BDL_PumpKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.system import System, BDL_SystemTypes
from rpd_generator.bdl_structure.bdl_commands.schedule import (
    BDL_DayScheduleKeywords,
    BDL_ScheduleTypes,
    DaySchedulePD,
    WeekSchedulePD,
    BDL_WeekScheduleKeywords,
    Schedule,
    BDL_ScheduleKeywords,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import *
from rpd_generator.utilities import schedule_funcs


class TestCHWLoop(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.circulation_loop = CirculationLoop("CHW Loop 1", self.rmd)
        self.pump = Pump("Pump 1", self.rmd)
        self.system = System("System 1", self.rmd)
        self.daySchedule = DaySchedulePD("Day Schedule Non-continuous", self.rmd)
        self.daySchedule2 = DaySchedulePD("Day Schedule Continuous", self.rmd)
        self.weekSchedule = WeekSchedulePD("Week Schedule Non-continuous", self.rmd)
        self.weekSchedule2 = WeekSchedulePD("Week Schedule Continuous", self.rmd)
        self.annualSchedule = Schedule("Annual Schedule 1", self.rmd)
        self.annualSchedule.annual_calendar = schedule_funcs.generate_year_calendar(
            2020, "WEDNESDAY"
        )

        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "2"}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Annual Schedule 1"
        }
        self.daySchedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: [
                str(i) for i in range(0, 24)
            ],  # Non-continuous schedule
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.weekSchedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Day Schedule Non-continuous" for i in range(12)
            ],
        }
        self.annualSchedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: [
                "Week Schedule Non-continuous" for i in range(52)
            ],
            BDL_ScheduleKeywords.MONTH: "1",
            BDL_ScheduleKeywords.DAY: "1",
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop(self, mock_get_output_data):
        """Tests that circulation_loop output contains expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "CHW Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "SCHEDULED",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_temp_reset_outside_air(
        self, mock_get_output_data
    ):
        """Tests that outdoor hi and lo temps and supply hi and lo temps are set, given OUTDOOR_AIR temp reset type
        and that operation mode is intermittent when loop operation mode is STANDBY and non-continuous
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Annual Schedule 1",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.RESVVT,
        }
        self.daySchedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.VALUES: [str(i) for i in range(0, 24)],
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.weekSchedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Day Schedule Non-continuous" for i in range(12)
            ],
        }
        self.annualSchedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: [
                "Week Schedule Non-continuous" for i in range(52)
            ],
            BDL_ScheduleKeywords.MONTH: "1",
            BDL_ScheduleKeywords.DAY: "1",
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "CHW Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "INTERMITTENT",
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fluid_loop_condenser(
        self, mock_get_output_data
    ):
        """Tests when circulation loop type is CONDENSER, circulation_loop outputs expected values for valid inputs,
        and that when a continuous schedule is provided, operation status is CONTINUOUS
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.daySchedule2.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: [
                str(i) for i in range(1, 25)
            ],  # Continuous schedule
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.weekSchedule2.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Day Schedule Continuous" for i in range(12)
            ],
        }
        self.annualSchedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: [
                "Week Schedule Continuous" for i in range(52)
            ],
            BDL_ScheduleKeywords.MONTH: "1",
            BDL_ScheduleKeywords.DAY: "1",
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "CHW Loop 1 CondensingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "CONDENSER",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fluid_loop_condenser_wlhp(
        self, mock_get_output_data
    ):
        """Tests that when circulation loop type is CONDENSER via circulation_loop_type WLHP, circulation_loop outputs
        expected values for valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.WLHP,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "CHW Loop 1 CondensingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "INTERMITTENT",
            },
            "type": "CONDENSER",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fluid_loop_heating(self, mock_get_output_data):
        """Tests when circulation loop type is HEATING, circulation_loop outputs expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "24.0",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "heating_design_and_control": {
                "id": "CHW Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": -3.5,
                "loop_supply_temperature_at_low_load": 24.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "INTERMITTENT",
            },
            "type": "HEATING",
            "cooling_or_condensing_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fluid_loop_heating_and_cooling(
        self, mock_get_output_data
    ):
        """Tests when circulation loop type is HEATING_AND_COOLING, circulation_loop outputs expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Annual Schedule 1",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.RESVVT,
        }
        self.daySchedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.VALUES: [str(i) for i in range(0, 24)],
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.weekSchedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Day Schedule Non-continuous" for i in range(12)
            ],
        }
        self.annualSchedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: [
                "Week Schedule Non-continuous" for i in range(52)
            ],
            BDL_ScheduleKeywords.MONTH: "1",
            BDL_ScheduleKeywords.DAY: "1",
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.PIPE2,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Annual Schedule 1",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "24.0",
            BDL_CirculationLoopKeywords.MAX_RESET_T: "85.0",
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "CHW Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Annual Schedule 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "heating_design_and_control": {
                "id": "CHW Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": -3.5,
                "loop_supply_temperature_at_low_load": 24.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "INTERMITTENT",
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
            },
            "cooling_or_condensing_design_and_control": {
                "id": "CHW Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 85.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "INTERMITTENT",
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
            },
            "type": "HEATING_AND_COOLING",
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_service_water_heating_distribution_system(
        self, mock_get_output_data
    ):
        """Tests that circulation_loop type ServiceWaterHeatingDistributionSystem produces expected output,
        given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "10",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
            "design_supply_temperature": 78.5,
            "design_supply_temperature_difference": 82.0,
            "is_ground_temperature_used_for_entering_water": False,
            "tanks": {},
            "service_water_piping": {},
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_service_water_piping(
        self, mock_get_output_data
    ):
        """Tests that circulation_loop type ServiceWaterPiping  produces expected output,
        given valid inputs"""
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "10",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "CHW Loop 1",
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)
