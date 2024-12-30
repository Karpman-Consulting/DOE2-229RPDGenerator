import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import (
    CirculationLoop,
    BDL_CirculationLoopKeywords,
    BDL_CirculationLoopSizingOptions,
    BDL_CirculationLoopTypes,
    BDL_CirculationLoopTemperatureResetOptions,
    BDL_CirculationLoopOperationOptions,
)
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.pump import (
    BDL_PumpKeywords,
    Pump,
)
from rpd_generator.bdl_structure.bdl_commands.schedule import (
    DaySchedulePD,
    WeekSchedulePD,
    Schedule,
    BDL_DayScheduleKeywords,
    BDL_WeekScheduleKeywords,
    BDL_ScheduleKeywords,
    BDL_ScheduleTypes,
)
from rpd_generator.bdl_structure.bdl_commands.project import (
    RunPeriod,
    Holidays,
    BDL_RunPeriodKeywords,
    BDL_HolidayKeywords,
    BDL_HolidayTypes,
)
from rpd_generator.bdl_structure.bdl_commands.system import (
    System,
    BDL_SystemHeatingTypes,
    BDL_SystemCoolingTypes,
)
from rpd_generator.bdl_structure.bdl_commands.zone import *
from rpd_generator.bdl_structure.bdl_commands.space import Space
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription


class TestZones(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rpd = RulesetProjectDescription()
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.bdl_obj_instances["ASHRAE 229"] = self.rpd
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.run_period = RunPeriod("Run Period 1", self.rmd)
        self.holidays = Holidays("Holidays 1", self.rmd)

        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)
        self.pump = Pump("Pump 1", self.rmd)
        self.hw_circulation_loop = CirculationLoop("HW Circulation Loop", self.rmd)

        # Create People Schedules
        self.people_day_schedule = DaySchedulePD("People Day Schedule", self.rmd)
        self.people_week_schedule = WeekSchedulePD("People Week Schedule", self.rmd)
        self.people_annual_schedule = Schedule("People Annual Schedule", self.rmd)

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

        # Create Flow Schedules
        self.flow_day_schedule = DaySchedulePD("Flow Day Schedule", self.rmd)
        self.flow_week_schedule = WeekSchedulePD("Flow Week Schedule", self.rmd)
        self.flow_annual_schedule = Schedule("Flow Annual Schedule", self.rmd)

        # Create Thermostat Schedules
        self.thermostat_day_schedule = DaySchedulePD(
            "Thermostat Day Schedule", self.rmd
        )
        self.thermostat_week_schedule = WeekSchedulePD(
            "Thermostat Week Schedule", self.rmd
        )
        self.thermostat_annual_schedule = Schedule(
            "Thermostat Annual Schedule", self.rmd
        )

        # Create System Fan Schedules
        self.fan_schedule_day_schedule = DaySchedulePD("Fan Day Schedule", self.rmd)
        self.fan_schedule_week_schedule = WeekSchedulePD("Fan Week Schedule", self.rmd)
        self.fan_schedule_annual_schedule = Schedule("Fan Annual Schedule", self.rmd)

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

        # Create populate default keyword value pairs for all tests
        self.run_period.keyword_value_pairs = {
            BDL_RunPeriodKeywords.END_YEAR: "2021",
        }
        self.holidays.keyword_value_pairs = {
            BDL_HolidayKeywords.TYPE: BDL_HolidayTypes.OFFICIAL_US,
        }
        self.pump.keyword_value_pairs = {BDL_PumpKeywords.NUMBER: "1"}
        self.people_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_DayScheduleKeywords.VALUES: ["0.1"] * 24,
        }
        self.people_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["People Day Schedule"] * 12,
        }
        self.people_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "People Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.temp_reset_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
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
        self.flow_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_DayScheduleKeywords.VALUES: ["0.5"] * 24,
        }
        self.flow_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Flow Day Schedule"] * 12,
        }
        self.flow_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Flow Week Schedule",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }
        self.thermostat_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_DayScheduleKeywords.OUTSIDE_HI: "100",
            BDL_DayScheduleKeywords.OUTSIDE_LO: "50",
            BDL_DayScheduleKeywords.SUPPLY_HI: "95",
            BDL_DayScheduleKeywords.SUPPLY_LO: "45",
        }
        self.thermostat_week_schedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Thermostat Day Schedule"] * 12,
        }
        self.thermostat_annual_schedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.RESET_TEMP,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Thermostat Week Schedule",
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
        self.loop_operation_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["1"] * 24,
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
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule"
        }
        self.hw_circulation_loop.keyword_value_pairs = {
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

        # KEYWORDS / OUTPUT DATA KEYS FOR REFERENCE
        # self.zone.keyword_value_pairs = {
        #     BDL_ZoneKeywords.DESIGN_COOL_T: "85",
        #     BDL_ZoneKeywords.COOL_TEMP_SCH: "",
        #     BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
        #     BDL_ZoneKeywords.HEAT_TEMP_SCH: "",
        #     BDL_ZoneKeywords.EXHAUST_FLOW: "",
        #     BDL_ZoneKeywords.EXHAUST_FAN_SCH: "",
        #     BDL_ZoneKeywords.EXHAUST_STATIC: "",
        #     BDL_ZoneKeywords.EXHAUST_EFF: "",
        #     BDL_ZoneKeywords.EXHAUST_KW_FLOW: "",
        #     BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "",
        #     BDL_ZoneKeywords.OA_FLOW_PER: "",
        #     BDL_ZoneKeywords.ASSIGNED_FLOW: "",
        #     BDL_ZoneKeywords.HASSIGNED_FLOW: "",
        #     BDL_ZoneKeywords.FLOW_AREA: "",
        #     BDL_ZoneKeywords.HFLOW_AREA: "",
        #     BDL_ZoneKeywords.AIR_CHANGES_HR: "",
        #     BDL_ZoneKeywords.HAIR_CHANGES_HR: "",
        #     BDL_ZoneKeywords.MIN_FLOW_AREA: "",
        #     BDL_ZoneKeywords.HMIN_FLOW_AREA: "",
        #     BDL_ZoneKeywords.HW_LOOP: "",
        #     BDL_ZoneKeywords.TERMINAL_TYPE: "",
        #     BDL_ZoneKeywords.MIN_AIR_SCH: "",
        #     BDL_ZoneKeywords.MIN_FLOW_RATIO: "",
        #     BDL_ZoneKeywords.BASEBOARD_RATING: "",
        #     BDL_ZoneKeywords.SPACE: "",
        #     BDL_ZoneKeywords.OA_CHANGES: "",
        #     BDL_ZoneKeywords.OA_FLOW_AREA: "",
        #     BDL_ZoneKeywords.MIN_FLOW_CTRL: "",
        #     BDL_ZoneKeywords.MIN_FLOW_SCH: "",
        #     BDL_ZoneKeywords.CMIN_FLOW_SCH: "",
        #     BDL_ZoneKeywords.HMIN_FLOW_SCH: ""
        # }
        # mock_get_output_data.return_value = {
        #     "Supply Fan - Airflow": 0,
        #     "Supply Fan - Power": 0,
        #     "Zone Fan Power": 0,
        #     "Zone Supply Airflow": 0,
        #     "Zone Minimum Airflow Ratio": 0,
        #     "Zone Outside Airflow": 0,
        #     "Zone Heating Capacity": 0,
        #     "Zone Cooling Capacity": 0,
        #     "Dual-Duct/Multizone Boxes - Outlet Airflow": 0
        # }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_constant_volume_constant_temp_data(
        self, mock_get_output_data
    ):
        """
        Test populating data elements for a zone served by a constant volume, single-zone system with DX cooling,
        electric heating, and constant temperature control
        """
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Fan Power": 1000,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PSZ,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.ELECTRIC,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.ELECTRIC,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "CONSTANT_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_source": "ELECTRIC",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_terminal_system_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone served by a constant volume, single-zone system with CHW cooling, HW
        heating
        """
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.FC,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 14.0,
                    "cooling_source": "CHILLED_WATER",
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 15.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "HOT_WATER",
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                    "temperature_control": "CONSTANT",
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_variable_volume_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone served by a variable volume, single-duct system, with terminal reheat

        """
        mock_get_output_data.return_value = {
            "Zone Fan Power": 0,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PVAVS,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "HOT_WATER",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_on_sum_system_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone that is assigned to a SUM type system

        """
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.SUM,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.EXHAUST_FLOW: "150",
            BDL_ZoneKeywords.EXHAUST_FAN_SCH: "Fan Annual Schedule",
            BDL_ZoneKeywords.EXHAUST_STATIC: "2",
            BDL_ZoneKeywords.EXHAUST_EFF: "0.8",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "exhaust_airflow_rate_multiplier_schedule": "Fan Annual Schedule",
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_exhaust_fan_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with an exhaust fan

        """
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Fan Power": 1000,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PTAC,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.ELECTRIC,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.ELECTRIC,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.EXHAUST_FLOW: "150",
            BDL_ZoneKeywords.EXHAUST_FAN_SCH: "Fan Annual Schedule",
            BDL_ZoneKeywords.EXHAUST_STATIC: "2",
            BDL_ZoneKeywords.EXHAUST_EFF: "0.8",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "exhaust_airflow_rate_multiplier_schedule": "Fan Annual Schedule",
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "CONSTANT_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "ELECTRIC",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {
                "id": "Zone 1 EF",
                "design_airflow": 150.0,
                "design_electric_power": 0.04408382900635919,
                "design_pressure_rise": 2.0,
                "is_airflow_sized_based_on_design_day": False,
                "specification_method": "DETAILED",
                "total_efficiency": 0.8,
            },
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_induction_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with induction units and secondary airflow

        """
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Fan Power": 1000,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
            "Powered Induction Units - Fan Flow": 1000,
            "Powered Induction Units - Fan kW": 15,
            "Powered Induction Units - Cold Deck Flow": 2000,
            "Powered Induction Units - Cold Deck Minimum Airflow Ratio": 0.95,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PIU,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.ELECTRIC,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.ELECTRIC,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.TERMINAL_IU,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "CONSTANT_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "ELECTRIC",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 2000,
                    "secondary_airflow": 1000,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_doas_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone served by a system which is served by a dedicated outside air system

        """
        self.doas = System("DOAS 1", self.rmd)
        self.doas.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule"
        }
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Fan Power": 1000,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PTAC,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.ELECTRIC,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.ELECTRIC,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_SystemKeywords.DOA_SYSTEM: "DOAS 1",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "CONSTANT_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "ELECTRIC",
                    "minimum_airflow": 30000000,
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                },
                {
                    "id": "Zone 1 DOASTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 0.0,
                    "minimum_airflow": 0.3,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 0.3,
                    "served_by_heating_ventilating_air_conditioning_system": "DOAS 1",
                },
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_baseboard_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with baseboard supplemental heating

        """
        self.hw_bbrd_loop = CirculationLoop("HW Baseboard Loop", self.rmd)
        self.hw_bbrd_loop.keyword_value_pairs = {
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
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 0,
            "Supply Fan - Power": 0,
            "Zone Fan Power": 1000,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PTAC,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.ELECTRIC,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.ELECTRIC,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_SystemKeywords.BASEBOARD_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.BBRD_LOOP: "HW Baseboard Loop",
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.THERMOSTATIC,
            BDL_ZoneKeywords.BASEBOARD_RATING: "-6",
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OUTSIDE_AIR_FLOW: "200",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "CONSTANT_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "ELECTRIC",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                },
                {
                    "id": "Zone 1 BaseboardTerminal",
                    "type": "BASEBOARD",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 6.0,
                    "heating_from_loop": "HW Baseboard Loop",
                    "heating_source": "HOT_WATER",
                    "is_supply_ducted": False,
                },
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation

        """
        mock_get_output_data.return_value = {
            "Zone Fan Power": 0,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PVAVS,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_SystemKeywords.ZONE_OA_METHOD: BDL_ZoneOAMethodsOptions.SUM_OCC_AND_AREA,
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OA_FLOW_PER: "5",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.MIN_FLOW_CTRL: BDL_MinFlowControlOptions.DCV_RESET_DOWN,
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {},
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": True,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "HOT_WATER",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv_prevented_by_occ_cfm(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation that is prevented by the minimum
        occupancy CFM

        """
        mock_get_output_data.return_value = {
            "Zone Fan Power": 0,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }

        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.rmd.space_map["Space 1"] = self.zone

        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "People Annual Schedule",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.VOLUME: "1000",
            BDL_SpaceKeywords.AREA: "100",
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PVAVS,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_SystemKeywords.ZONE_OA_METHOD: BDL_ZoneOAMethodsOptions.MAX_OCC_OR_AREA,
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OA_FLOW_PER: "5",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.MIN_AIR_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.SPACE: "Space 1",
            BDL_ZoneKeywords.OA_CHANGES: "6",
            BDL_ZoneKeywords.OA_FLOW_AREA: "100",
            BDL_ZoneKeywords.MIN_FLOW_CTRL: BDL_MinFlowControlOptions.DCV_RESET_DOWN,
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {
                "id": "Space 1 Infil",
                "modeling_method": "WEATHER_DRIVEN",
            },
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "HOT_WATER",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "minimum_outdoor_airflow_multiplier_schedule": "Flow Annual Schedule",
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "volume": 1000.0,
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv_prevented_by_min_oa_sch(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation that is prevented by the minimum OA
        schedule(s)

        """
        mock_get_output_data.return_value = {
            "Zone Fan Power": 0,
            "Zone Supply Airflow": 10000,
            "Zone Minimum Airflow Ratio": 3000,
            "Zone Outside Airflow": 0.3,
            "Zone Heating Capacity": 12,
            "Zone Cooling Capacity": 0,
        }

        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.rmd.space_map["Space 1"] = self.zone

        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "People Annual Schedule",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.VOLUME: "1000",
            BDL_SpaceKeywords.AREA: "100",
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PVAVS,
            BDL_SystemKeywords.FAN_CONTROL: BDL_SystemFanControlOptions.CONSTANT_VOLUME,
            BDL_SystemKeywords.MAX_SUPPLY_T: "70",
            BDL_SystemKeywords.MIN_SUPPLY_T: "50",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.ZONE_HEAT_SOURCE: BDL_ZoneHeatSourceOptions.HOT_WATER,
            BDL_SystemKeywords.SUPPLY_STATIC: "30",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "1",
            BDL_SystemKeywords.MIN_FLOW_RATIO: "0.4",
            BDL_SystemKeywords.COOL_SET_T: "75",
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.SUPPLY_FLOW: "2500",
            BDL_SystemKeywords.HEATING_CAPACITY: "15",
            BDL_SystemKeywords.COOLING_CAPACITY: "14",
            BDL_SystemKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_SystemKeywords.ZONE_OA_METHOD: BDL_ZoneOAMethodsOptions.MAX_OCC_OR_AREA,
        }
        self.flow_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.FRAC_DESIGN,
            BDL_DayScheduleKeywords.VALUES: ["-999"] * 24,
        }
        self.zone.keyword_value_pairs = {
            BDL_ZoneKeywords.BASEBOARD_CTRL: BDL_BaseboardControlOptions.NONE,
            BDL_ZoneKeywords.DESIGN_COOL_T: "85",
            BDL_ZoneKeywords.COOL_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.DESIGN_HEAT_T: "45",
            BDL_ZoneKeywords.HEAT_TEMP_SCH: "Thermostat Annual Schedule",
            BDL_ZoneKeywords.OA_FLOW_PER: "5",
            BDL_ZoneKeywords.HW_LOOP: "HW Circulation Loop",
            BDL_ZoneKeywords.TERMINAL_TYPE: BDL_TerminalTypes.SVAV,
            BDL_ZoneKeywords.SPACE: "Space 1",
            BDL_ZoneKeywords.OA_CHANGES: "6",
            BDL_ZoneKeywords.OA_FLOW_AREA: "100",
            BDL_ZoneKeywords.MIN_FLOW_CTRL: BDL_MinFlowControlOptions.DCV_RESET_DOWN,
            BDL_ZoneKeywords.MIN_FLOW_SCH: "Flow Annual Schedule",
            BDL_ZoneKeywords.MIN_FLOW_RATIO: "0.6",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Zone 1",
            "design_thermostat_cooling_setpoint": 85.0,
            "design_thermostat_heating_setpoint": 45.0,
            "infiltration": {
                "id": "Space 1 Infil",
                "modeling_method": "WEATHER_DRIVEN",
            },
            "spaces": [],
            "surfaces": [],
            "terminals": [
                {
                    "id": "Zone 1 MainTerminal",
                    "type": "VARIABLE_AIR_VOLUME",
                    "cooling_capacity": 0.0,
                    "has_demand_control_ventilation": False,
                    "heating_capacity": 12000.0,
                    "heating_from_loop": "HW Circulation Loop",
                    "heating_source": "HOT_WATER",
                    "minimum_airflow": 30000000,
                    "minimum_outdoor_airflow": 0.3,
                    "primary_airflow": 10000,
                    "secondary_airflow": 0,
                    "served_by_heating_ventilating_air_conditioning_system": "System 1",
                    "supply_design_cooling_setpoint_temperature": 50.0,
                    "supply_design_heating_setpoint_temperature": 70.0,
                }
            ],
            "thermostat_cooling_setpoint_schedule": "Thermostat Annual Schedule",
            "thermostat_heating_setpoint_schedule": "Thermostat Annual Schedule",
            "volume": 1000.0,
            "zonal_exhaust_fan": {},
        }
        self.assertEqual(expected_data_structure, self.zone.zone_data_structure)
