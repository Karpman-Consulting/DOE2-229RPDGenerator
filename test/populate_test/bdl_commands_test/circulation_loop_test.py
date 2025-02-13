import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.boiler import Boiler
from rpd_generator.bdl_structure.bdl_commands.chiller import (
    Chiller,
    BDL_ChillerTypes,
    BDL_CondenserTypes,
)
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
from rpd_generator.bdl_structure.bdl_commands.curve_fit import (
    CurveFit,
    BDL_CurveFitKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.zone import (
    Zone,
    BDL_ZoneCWValveOptions,
)
from rpd_generator.bdl_structure.bdl_commands.project import (
    RunPeriod,
    Holidays,
    BDL_RunPeriodKeywords,
    BDL_HolidayKeywords,
    BDL_HolidayTypes,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import *


class TestCHWLoop(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        # Create objects for testing
        self.rpd = RulesetProjectDescription()
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.bdl_obj_instances["ASHRAE 229"] = self.rpd
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.run_period = RunPeriod("Run Period 1", self.rmd)
        self.holidays = Holidays("Holidays 1", self.rmd)
        self.circulation_loop = CirculationLoop("Circulation Loop 1", self.rmd)
        self.pump = Pump("Pump 1", self.rmd)
        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)
        self.eir_f_t = CurveFit("EIR-fT Curve", self.rmd)
        self.eir_f_plr = CurveFit("EIR-fPLR Curve", self.rmd)
        self.cap_f_t = CurveFit("CAP-fT Curve", self.rmd)

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

        # Populate default keyword value pairs for all tests
        self.run_period.keyword_value_pairs = {
            BDL_RunPeriodKeywords.END_YEAR: "2021",
        }
        self.holidays.keyword_value_pairs = {
            BDL_HolidayKeywords.TYPE: BDL_HolidayTypes.OFFICIAL_US,
        }
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "1"}

        self.loop_operation_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: [i % 2 for i in range(24)],
        }
        self.loop_operation_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Loop Operation Day Schedule"]
            * 12,
        }
        self.loop_operation_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Loop Operation Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["0"] * 24,
        }
        self.fan_schedule_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Fan Day Schedule"] * 12,
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
        self.eir_f_t.keyword_value_pairs = {
            BDL_CurveFitKeywords.COEF: [
                "-0.38924539",
                "-0.02195141",
                "-0.00027343",
                "0.04974775",
                "-0.00053441",
                "0.00067295",
            ],
            BDL_CurveFitKeywords.TYPE: "BI-QUADRATIC-T",
            BDL_CurveFitKeywords.INPUT_TYPE: "COEFFICIENTS",
            BDL_CurveFitKeywords.OUTPUT_MIN: "-1000000.0000",
            BDL_CurveFitKeywords.OUTPUT_MAX: "1000000.0000",
        }
        self.eir_f_plr.keyword_value_pairs = {
            BDL_CurveFitKeywords.COEF: [
                "0.14703037",
                "-0.00349667",
                "1.01161313",
                "-0.00359697",
                "0.00027167",
                "-0.01164471",
            ],
            BDL_CurveFitKeywords.TYPE: "BI-QUADRATIC-RATIO&DT",
            BDL_CurveFitKeywords.INPUT_TYPE: "COEFFICIENTS",
            BDL_CurveFitKeywords.OUTPUT_MIN: "               -1000000.0000",
            BDL_CurveFitKeywords.OUTPUT_MAX: "                1000000.0000",
        }
        self.cap_f_t.keyword_value_pairs = {
            BDL_CurveFitKeywords.COEF: [
                "-0.38924539",
                "-0.02195141",
                "-0.00027343",
                "0.04974775",
                "-0.00053441",
                "0.00067295",
            ],
            BDL_CurveFitKeywords.TYPE: "BI-QUADRATIC-T",
            BDL_CurveFitKeywords.INPUT_TYPE: "COEFFICIENTS",
            BDL_CurveFitKeywords.OUTPUT_MIN: "               -1000000.0000",
            BDL_CurveFitKeywords.OUTPUT_MAX: "                1000000.0000",
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.loop_operation_day_schedule.keyword_value_pairs[
            BDL_DayScheduleKeywords.VALUES
        ] = ["1"] * 24
        self.temp_reset_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "60",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.temp_reset_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Temp Reset Day Schedule"] * 12,
        }
        self.temp_reset_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Temp Reset Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 50,
                "design_return_temperature": 80,
                "loop_supply_temperature_at_outdoor_high": 45.0,
                "loop_supply_temperature_at_outdoor_low": 60.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 50.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.fan_schedule_day_schedule.keyword_value_pairs[
            BDL_DayScheduleKeywords.VALUES
        ] = ["1"] * 24

        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "40",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "50",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "50",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 40,
                "design_return_temperature": 90,
                "loop_supply_temperature_at_low_load": 50,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
            "Normalized (ARI) Entering Condenser Water Temperature (°F)": 70.0,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "60",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.STANDBY,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 50,
                "design_return_temperature": 80,
                "loop_supply_temperature_at_low_load": 60,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "INTERMITTENT",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
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
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.MAX_RESET_T: "60",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.circulation_loop_2 = CirculationLoop("Circulation Loop 2", self.rmd)
        self.circulation_loop_2.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.COINCIDENT,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "Circulation Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.MAX_RESET_T: "60",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        self.circulation_loop_2.insert_to_rpd(self.rmd)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 50.0,
                "design_return_temperature": 80.0,
                "loop_supply_temperature_at_low_load": 60.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "LOAD_RESET",
                "flow_control": "VARIABLE_FLOW",
                "operation": "SCHEDULED",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "type": "COOLING",
            "heating_design_and_control": {},
            "child_loops": [
                {
                    "id": "Circulation Loop 2",
                    "type": "COOLING",
                    "child_loops": [],
                    "cooling_or_condensing_design_and_control": {
                        "id": "Circulation Loop 2 CoolingDesign/Control",
                        "design_return_temperature": 80.0,
                        "design_supply_temperature": 50.0,
                        "flow_control": "VARIABLE_FLOW",
                        "is_sized_using_coincident_load": True,
                        "loop_supply_temperature_at_low_load": 60.0,
                        "minimum_flow_fraction": 0.8,
                        "operation": "SCHEDULED",
                        "operation_schedule": "Loop Operation Annual Schedule",
                        "temperature_reset_type": "LOAD_RESET",
                    },
                    "heating_design_and_control": {},
                    "pump_power_per_flow_rate": 50.0,
                }
            ],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.loop_operation_day_schedule.keyword_value_pairs[
            BDL_DayScheduleKeywords.VALUES
        ] = ["1"] * 24
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET,
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
                "design_return_temperature": 130.0,
                "loop_supply_temperature_at_low_load": 48.5,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "LOAD_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160.0",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.FIXED,
            BDL_CirculationLoopKeywords.MIN_RESET_T: "150",
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
                "design_return_temperature": 130.0,
                "loop_supply_temperature_at_low_load": 150,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "NO_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "INTERMITTENT",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.loop_operation_day_schedule.keyword_value_pairs[
            BDL_DayScheduleKeywords.VALUES
        ] = ["1"] * 24
        self.temp_reset_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "60",
            BDL_DayScheduleKeywords.SUPPLY_HI: "85",
            BDL_DayScheduleKeywords.SUPPLY_LO: "80",
        }
        self.temp_reset_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Temp Reset Day Schedule"] * 12,
        }
        self.temp_reset_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Temp Reset Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "80",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "20",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_RESET_SCH: "Temp Reset Annual Schedule",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.OA_RESET,
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CondensingDesign/Control",
                "design_supply_temperature": 80.0,
                "design_return_temperature": 100.0,
                "loop_supply_temperature_at_outdoor_high": 80.0,
                "loop_supply_temperature_at_outdoor_low": 85.0,
                "outdoor_high_for_loop_supply_reset_temperature": 100.0,
                "outdoor_low_for_loop_supply_reset_temperature": 60.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "OUTSIDE_AIR_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "type": "CONDENSER",
            "heating_design_and_control": {},
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
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
            "Pump - Flow (gal/min)": 300,
            "Pump - Power (kW)": 15,
        }
        self.loop_operation_day_schedule.keyword_value_pairs[
            BDL_DayScheduleKeywords.VALUES
        ] = ["1"] * 24
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.PIPE2,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.LOOP_MIN_FLOW: "0.8",
            BDL_CirculationLoopKeywords.COOL_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET,
            BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL: BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET,
            BDL_CirculationLoopKeywords.MAX_RESET_T: "60",
            BDL_CirculationLoopKeywords.MIN_RESET_T: "150",
            BDL_CirculationLoopKeywords.LOOP_OPERATION: BDL_CirculationLoopOperationOptions.SCHEDULED,
            BDL_CirculationLoopKeywords.COOLING_SCHEDULE: "Loop Operation Annual Schedule",
            BDL_CirculationLoopKeywords.HEATING_SCHEDULE: "Loop Operation Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "cooling_or_condensing_design_and_control": {
                "id": "Circulation Loop 1 CoolingDesign/Control",
                "design_supply_temperature": 50.0,
                "design_return_temperature": 80.0,
                "loop_supply_temperature_at_low_load": 60.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "LOAD_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "type": "HEATING_AND_COOLING",
            "heating_design_and_control": {
                "id": "Circulation Loop 1 HeatingDesign/Control",
                "design_supply_temperature": 160.0,
                "design_return_temperature": 130.0,
                "loop_supply_temperature_at_low_load": 150.0,
                "is_sized_using_coincident_load": False,
                "minimum_flow_fraction": 0.8,
                "temperature_reset_type": "LOAD_RESET",
                "flow_control": "FIXED_FLOW",
                "operation": "CONTINUOUS",
                "operation_schedule": "Loop Operation Annual Schedule",
            },
            "child_loops": [],
            "pump_power_per_flow_rate": 50.0,
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_swh_loop(self, mock_get_output_data):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE DHW
        """
        mock_get_output_data.return_value = {}
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "68",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "design_supply_temperature": 160.0,
            "design_supply_temperature_difference": 30.0,
            "is_ground_temperature_used_for_entering_water": False,
            "tanks": [],
            "service_water_piping": [
                {
                    "id": "Circulation Loop 1 ServiceWaterPiping",
                    "is_recirculation_loop": False,
                    "are_thermal_losses_modeled": False,
                    "child": [],
                    "service_water_heating_design_and_control": {
                        "id": "Circulation Loop 1 Design/Control",
                        "design_supply_temperature": 160.0,
                    },
                }
            ],
        }
        self.assertEqual(expected_data_structure, self.circulation_loop.data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_secndary_swh_loop(self, mock_get_output_data):
        """
        Tests that circulation_loop output contains expected values, given valid inputs for loop with:
            - TYPE DHW
        """
        mock_get_output_data.return_value = {}

        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "68",
            BDL_CirculationLoopKeywords.LOOP_RECIRC_FLOW: "30",
        }

        circulation_loop_2 = CirculationLoop("Circulation Loop 2", self.rmd)
        circulation_loop_2.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.LOOP_PUMP: "Pump 1",
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.DHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "Circulation Loop 1",
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "160",
            BDL_CirculationLoopKeywords.LOOP_DESIGN_DT: "30",
            BDL_CirculationLoopKeywords.DHW_INLET_T: "68",
            BDL_CirculationLoopKeywords.SUPPLY_UA: "10",
        }

        self.rmd.populate_rmd_data(testing=True)
        circulation_loop_2.insert_to_rpd(self.rmd)
        expected_data_structure = {
            "id": "Circulation Loop 1",
            "design_supply_temperature": 160.0,
            "design_supply_temperature_difference": 30.0,
            "is_ground_temperature_used_for_entering_water": False,
            "tanks": [],
            "service_water_piping": [
                {
                    "id": "Circulation Loop 1 ServiceWaterPiping",
                    "is_recirculation_loop": True,
                    "are_thermal_losses_modeled": False,
                    "service_water_heating_design_and_control": {
                        "id": "Circulation Loop 1 Design/Control",
                        "design_supply_temperature": 160.0,
                    },
                    "child": [
                        {
                            "id": "Circulation Loop 2",
                            "is_recirculation_loop": False,
                            "are_thermal_losses_modeled": True,
                            "service_water_heating_design_and_control": {
                                "id": "Circulation Loop 2 Design/Control",
                                "design_supply_temperature": 160.0,
                            },
                            "child": [],
                        }
                    ],
                }
            ],
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
        mock_get_output_data.return_value = {}
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
        }

        self.circulation_loop_2 = CirculationLoop("Circulation Loop 2", self.rmd)
        self.circulation_loop_2.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.SECONDARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.SUBTYPE: BDL_CirculationLoopSubtypes.SECONDARY,
            BDL_CirculationLoopKeywords.PRIMARY_LOOP: "Circulation Loop 1",
            BDL_CirculationLoopKeywords.VALVE_TYPE_2ND: BDL_SecondaryLoopValveTypes.TWO_WAY,
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
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
        self.chiller = Chiller("Chiller 1", self.rmd)
        mock_get_output_data.return_value = {
            "Normalized (ARI) Entering Condenser Water Temperature (°F)": 85.0,
            "Primary Equipment (Chillers) - Capacity (Btu/hr)": 118000.0,
        }
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.TYPE: BDL_ChillerTypes.ELEC_OPEN_CENT,
            BDL_ChillerKeywords.CONDENSER_TYPE: BDL_CondenserTypes.WATER_COOLED,
            BDL_ChillerKeywords.CHW_LOOP: "Circulation Loop 1",
            BDL_ChillerKeywords.EIR_FT: "EIR-fT Curve",
            BDL_ChillerKeywords.EIR_FPLR: "EIR-fPLR Curve",
            BDL_ChillerKeywords.CAPACITY_FT: "CAP-fT Curve",
            BDL_ChillerKeywords.ELEC_INPUT_RATIO: "0.16",
            BDL_ChillerKeywords.MIN_RATIO: "0.25",
            BDL_ChillerKeywords.CHW_FLOW_CTRL: BDL_FlowControlOptions.VARIABLE_FLOW,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CHW,
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
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
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.PHW_LOOP: "Circulation Loop 1",
            BDL_SystemKeywords.PHW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW
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
        mock_get_output_data.return_value = {}
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.HW_LOOP: "Circulation Loop 1",
            BDL_ZoneKeywords.HW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW
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
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW
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
        mock_get_output_data.return_value = {}
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.CW_LOOP: "Circulation Loop 1",
            BDL_ZoneKeywords.CW_VALVE: BDL_ZoneCWValveOptions.YES,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.WLHP
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
        mock_get_output_data.return_value = {}
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
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
        mock_get_output_data.return_value = {}
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.SIZING_OPTION: BDL_CirculationLoopSizingOptions.PRIMARY,
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.CW,
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
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.CHW_LOOP: "Circulation Loop 1",
            BDL_SystemKeywords.CHW_VALVE_TYPE: BDL_SystemHeatingValveTypes.TWO_WAY,
        }
        self.circulation_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.PIPE2
        }

        self.rmd.populate_rmd_data(testing=True)
        fluid_loop_flow_control = self.circulation_loop.determine_loop_flow_control()
        self.assertEqual(
            FluidLoopFlowControlOptions.VARIABLE_FLOW, fluid_loop_flow_control
        )
