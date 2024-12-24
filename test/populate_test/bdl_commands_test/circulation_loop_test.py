import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.boiler import Boiler
from rpd_generator.bdl_structure.bdl_commands.chiller import Chiller
from rpd_generator.bdl_structure.bdl_commands.ground_loop_hx import GroundLoopHX
from rpd_generator.bdl_structure.bdl_commands.heat_rejection import HeatRejection
from rpd_generator.bdl_structure.bdl_commands.pump import (
    Pump,
    BDL_PumpKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.system import System
from rpd_generator.bdl_structure.bdl_commands.schedule import (
    BDL_ScheduleTypes,
    DaySchedulePD,
    BDL_DayScheduleKeywords,
    WeekSchedulePD,
    BDL_WeekScheduleKeywords,
    Schedule,
    BDL_ScheduleKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.zone import (
    Zone,
    BDL_ZoneCWValveOptions,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import *
from rpd_generator.utilities import schedule_funcs


class TestCHWLoop(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        # Create objects for testing
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.circulation_loop = CirculationLoop("Circulation Loop 1", self.rmd)
        self.circulation_loop_2 = CirculationLoop("Circulation Loop 2", self.rmd)
        self.pump = Pump("Pump 1", self.rmd)
        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)
        self.chiller = Chiller("Chiller 1", self.rmd)

        # Create Chilled Water/Hot Water Temperature Reset Schedules
        self.temp_reset_day_schedule = DaySchedulePD(
            "Temp Reset Day Schedule", self.rmd
        )
        self.temp_reset_week_schedule = WeekSchedulePD(
            "Temp Reset Week Schedule", self.rmd
        )
        self.temp_reset_annual_schedule = Schedule(
            "Temp Reset Annual Schedule", self.rmd
        )

        # Create Loop Operation Schedules
        self.loop_operation_day_schedule = DaySchedulePD(
            "Loop Operation Day Schedule", self.rmd
        )
        self.loop_operation_week_schedule = WeekSchedulePD(
            "Loop Operation Week Schedule", self.rmd
        )
        self.loop_operation_annual_schedule = Schedule(
            "Loop Operation Annual Schedule", self.rmd
        )

        # Create System Fan Schedules
        self.fan_schedule_day_schedule = DaySchedulePD("Fan Day Schedule", self.rmd)
        self.fan_schedule_week_schedule = WeekSchedulePD("Fan Week Schedule", self.rmd)
        self.fan_schedule_annual_schedule = Schedule("Fan Annual Schedule", self.rmd)

        # Generate annual calendar for schedules
        generated_calendar = schedule_funcs.generate_year_calendar(2020, "WEDNESDAY")
        self.temp_reset_annual_schedule.annual_calendar = generated_calendar
        self.loop_operation_annual_schedule.annual_calendar = generated_calendar
        self.fan_schedule_annual_schedule.annual_calendar = generated_calendar

        # Populate default keyword value pairs for all tests
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "1"}
        self.temp_reset_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.temp_reset_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Temp Reset Day Schedule" for i in range(12)
            ],
        }
        self.temp_reset_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Temp Reset Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.loop_operation_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["1" for i in range(24)],
        }
        self.loop_operation_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Loop Operation Day Schedule" for i in range(12)
            ],
        }
        self.loop_operation_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Loop Operation Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["0" for i in range(24)],
        }
        self.fan_schedule_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: [
                "Fan Day Schedule" for i in range(12)
            ],
        }
        self.fan_schedule_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Fan Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule"
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_oa_reset_continuous_scheduled_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE CHW
            - OA-RESET COOL-SETPT-CTRL
            - SCHEDULED LOOP-OPERATION
            - Continuous LOOP-OPERATION-SCHEDULE
        """
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
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fixed_continuous_system_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE CHW
            - FIXED COOL-SETPT-CTRL
            - STANDBY LOOP-OPERATION
            - Continuous SYSTEM Fan Schedule
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["1" for i in range(24)],
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_chw_loop_fixed_intermittent_system_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE CHW
            - FIXED COOL-SETPT-CTRL
            - STANDBY LOOP-OPERATION
            - Noncontinuous SYSTEM Fan Schedule
        """
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
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "INTERMITTENT",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_primary_secondary_chw_loop(self, mock_get_output_data):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - Loop 1 TYPE CHW
            - Loop 2 TYPE CHW, SUBTYPE SECONDARY
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.CHW_LOOP: "Circulation Loop 2",
            BDL_SystemKeywords.CHW_VALVE_TYPE: BDL_SecondaryLoopValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }
        self.circulation_loop_2.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.SECONDARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "Circulation Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_hw_loop_oa_reset_continuous_scheduled_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE HW
            - OA-RESET HEAT-SETPT-CTRL
            - SCHEDULED LOOP-OPERATION
            - Continuous LOOP-OPERATION-SCHEDULE
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.HEATING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {},
            "type": "HEATING",
            "heating_design_and_control": {
                "id": "Circulation Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 160.0,
                "design_return_temperature": 78.0,
                "loop_supply_temperature_at_low_load": 48.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_hw_loop_fixed_demand_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE HW
            - FIXED HEAT-SETPT-CTRL
            - DEMAND LOOP-OPERATION
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {},
            "type": "HEATING",
            "heating_design_and_control": {
                "id": "Circulation Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 160.0,
                "design_return_temperature": 78.0,
                "loop_supply_temperature_at_low_load": 48.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "INTERMITTENT",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_cw_loop_oa_reset_continuous_scheduled_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE CW
            - OA-RESET COOL-SETPT-CTRL
            - SCHEDULED LOOP-OPERATION
            - Continuous LOOP-OPERATION-SCHEDULE
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CondensingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "CONDENSER",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_heat_cool_changeover_loop_continuous_scheduled_operation(
        self, mock_get_output_data
    ):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE PIPE2
            - OA-RESET HEAT-SETPT-CTRL
            - OA-RESET COOL-SETPT-CTRL
            - SCHEDULED LOOP-OPERATION
            - Continuous LOOP-OPERATION-SCHEDULE
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.PIPE2,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.MIN_RESET_T: "45.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
            BDL_CirculationLoopKeywords.HEATING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 78.5,
                "design_return_temperature": 160.5,
                "loop_supply_temperature_at_low_load": 98.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "HEATING_AND_COOLING",
            "heating_design_and_control": {
                "id": "Circulation Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 160.0,
                "design_return_temperature": 78.0,
                "loop_supply_temperature_at_low_load": 45.5,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 95.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 5000.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_swh_loop(self, mock_get_output_data):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE DHW
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "68",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "design_supply_temperature": 160.0,
            "design_supply_temperature_difference": 82.0,
            "is_ground_temperature_used_for_entering_water": False,
            "tanks": {},
            "service_water_piping": {},
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_chw_loop_flow_control_variable_secondary_loop_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - Loop 1 TYPE CHW
            - Loop 2 TYPE CHW, SUBTYPE SECONDARY
            - Loop 2 VALVE_TYPE_2ND TWO-WAY
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        # TODO: I feel like this test should return VARIABLE_FLOW without having to have the system
        # TODO: keyword value pairs set. See comments around line 660 in circulation_loop.py
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.CHW_LOOP: "Circulation Loop 2",
            BDL_SystemKeywords.CHW_VALVE_TYPE: BDL_SecondaryLoopValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }
        self.circulation_loop_2.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.SECONDARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "Circulation Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop_2.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_chw_loop_flow_control_variable_chiller_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE CHW
            - Chiller CHW-FLOW-CTRL VARIABLE-FLOW
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.CHW_LOOP: "Circulation Loop 1",
            BDL_ChillerKeywords.CHW_FLOW_CTRL: BDL_FlowControlOptions.VARIABLE_FLOW,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_hw_loop_flow_control_variable_system_phw_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE HW
            - System PHW-VALVE-TYPE TWO-WAY
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.HW_LOOP: "Circulation Loop 1",
            BDL_SystemKeywords.PHW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_hw_loop_flow_control_variable_zone_hw_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE HW
            - Zone HW-VALVE-TYPE TWO-WAY
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.HW_LOOP: "Circulation Loop 1",
            BDL_ZoneKeywords.HW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.FIXED_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_hw_loop_flow_control_variable_boiler_hw_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE HW
            - Boiler HW-FLOW-CTRL VARIABLE-FLOW
        """
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.HW_LOOP: "Circulation Loop 1",
            BDL_BoilerKeywords.HW_FLOW_CTRL: BDL_FlowControlOptions.VARIABLE_FLOW,
        }
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_wlhp_loop_flow_control_variable_hp_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE WLHP
            - HP SYSTEM CW-VALVE YES
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.CW_LOOP: "Circulation Loop 1",
            BDL_ZoneKeywords.CW_VALVE: BDL_ZoneCWValveOptions.YES,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.WLHP,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_cw_loop_flow_control_variable_heat_rejection_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE CW
            - Heat Rejection CW-FLOW-CTRL VARIABLE-FLOW
        """
        self.heat_rejection = HeatRejection("Heat Rejection 1", self.rmd)
        self.heat_rejection.keyword_value_pairs = {
            BDL_HeatRejectionKeywords.CW_LOOP: "Circulation Loop 1",
            BDL_HeatRejectionKeywords.CW_FLOW_CTRL: BDL_FlowControlOptions.VARIABLE_FLOW,
        }
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_cw_loop_flow_control_variable_glhx_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE CW
            - GLHX HX-FLOW-CTRL VARIABLE-FLOW
        """
        self.ground_loop_hx = GroundLoopHX("Ground Loop HX 1", self.rmd)
        self.ground_loop_hx.keyword_value_pairs = {
            BDL_GroundLoopHXKeywords.CIRCULATION_LOOP: "Circulation Loop 1",
            BDL_GroundLoopHXKeywords.HX_FLOW_CTRL: BDL_FlowControlOptions.VARIABLE_FLOW,
        }
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "48.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.DEMAND,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_determine_heat_cool_loop_flow_control_variable_system_valve(
        self, mock_get_output_data
    ):
        """
        Tests that determine_loop_flow_control returns expected values, given valid inputs for loop with:
            - TYPE PIPE2
            - System CHW-VALVE-TYPE TWO-WAY
        """
        mock_get_output_data.return_value = {
            "Pump - Flow (gal/min)": 30,
            "Pump - Power (kW)": 150,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.CHW_LOOP: "Circulation Loop 1",
            BDL_SystemKeywords.CHW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.PIPE2,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "78.5",
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "82",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "98.5",
            BDL_CirculationLoopKeywords.MIN_RESET_T: "45.5",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
            BDL_CirculationLoopKeywords.HEATING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )
