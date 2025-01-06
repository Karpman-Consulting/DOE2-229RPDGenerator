import unittest
from unittest.mock import patch

from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.bdl_structure.bdl_commands.project import (
    RunPeriod,
    Holidays,
    BDL_RunPeriodKeywords,
    BDL_HolidayKeywords,
    BDL_HolidayTypes,
)
from rpd_generator.bdl_structure.bdl_commands.schedule import (
    BDL_DayScheduleKeywords,
    BDL_ScheduleTypes,
    BDL_WeekScheduleKeywords,
    BDL_ScheduleKeywords,
    DaySchedulePD,
    WeekSchedulePD,
    Schedule,
)
from rpd_generator.bdl_structure.bdl_commands.zone import Zone
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.system import (
    System,
    BDL_SystemKeywords,
    BDL_SystemTypes,
    BDL_CoolControlOptions,
    BDL_SystemHeatingTypes,
    BDL_SystemCoolingTypes,
    BDL_EconomizerOptions,
    BDL_EnergyRecoveryOptions,
    BDL_NightCycleControlOptions,
    BDL_HeatControlOptions,
    BDL_ReturnFanOptions,
    BDL_SystemEconoLockoutOptions,
    BDL_DualDuctFanOptions,
)


class TestSystems(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rpd = RulesetProjectDescription()
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.bdl_obj_instances["ASHRAE 229"] = self.rpd
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = System("System 1", self.rmd)
        self.zone1 = Zone("Zone 1", self.system, self.rmd)
        self.run_period = RunPeriod("Run Period 1", self.rmd)
        self.holidays = Holidays("Holidays 1", self.rmd)

        # Create System Fan Schedules
        self.fan_schedule_day_schedule = DaySchedulePD("Fan Day Schedule", self.rmd)
        self.fan_schedule_week_schedule = WeekSchedulePD("Fan Week Schedule", self.rmd)
        self.fan_schedule_annual_schedule = Schedule("Fan Annual Schedule", self.rmd)

        self.run_period.keyword_value_pairs = {
            BDL_RunPeriodKeywords.END_YEAR: "2021",
        }
        self.holidays.keyword_value_pairs = {
            BDL_HolidayKeywords.TYPE: BDL_HolidayTypes.OFFICIAL_US,
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

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_system_multizone_vav(self, mock_get_output_data):
        """Test populating a System data group from a multi-zone VAV system BDL command with zone-reset temperature controls,
        a return fan,
        propane furnace preheat system,
        CHW cooling system,
        integrated economizer,
        and ERV.
        Supply fan is sized based on design day with detailed spec method.
        System operates continuously during occupied hours and cycles during unoccupied hours.
        """
        mock_get_output_data.return_value = {
            "Return Fan - Airflow": 10,
            "Return Fan - Power": 11,
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: (["0"] * 12) + (["1"] * 12),
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.VAVS,
            BDL_SystemKeywords.COOL_CONTROL: BDL_CoolControlOptions.WARMEST,
            BDL_SystemKeywords.COOL_MAX_RESET_T: "60",
            BDL_SystemKeywords.HEAT_SET_T: "70",
            BDL_SystemKeywords.RETURN_FLOW: "10.1",
            BDL_SystemKeywords.RETURN_KW_FLOW: "11.5",
            BDL_SystemKeywords.RETURN_STATIC: "15",
            BDL_SystemKeywords.RETURN_MTR_EFF: "0.7",
            BDL_SystemKeywords.RETURN_MECH_EFF: "0.8",
            BDL_SystemKeywords.PREHEAT_SOURCE: BDL_SystemHeatingTypes.FURNACE,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.SUPPLY_STATIC: "20",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "0.95",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "TEMPERATURE",
                },
                "air_energy_recovery": {"id": "System 1 AirEnergyRecovery"},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "CYCLING",
                "relief_fans": [],
                "return_fans": [
                    {
                        "design_airflow": 10,
                        "design_electric_power": 11,
                        "design_pressure_rise": 15.0,
                        "id": "System 1 ReturnFan",
                        "is_airflow_sized_based_on_design_day": False,
                        "motor_efficiency": 0.7,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.5599999999999999,
                    }
                ],
                "supply_fans": [
                    {
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": True,
                        "motor_efficiency": 0.9,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.855,
                    }
                ],
                "temperature_control": "ZONE_RESET",
            },
            "heating_system": {},
            "id": "System 1",
            "preheat_system": {
                "id": "System 1 PreheatSys",
                "is_sized_based_on_design_day": True,
                "type": "FURNACE",
            },
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_system_multizone_vav2(self, mock_get_output_data):
        """Test populating a System data group from a multi-zone VAV system BDL command with constant temperature controls,
        a relief fan,
        fuel-oil HW heating system,
        CHW cooling system,
        integrated economizer,
        and ERV.
        Supply fan is sized based on design day with detailed spec method.
        System operates continuously during occupied hours and cycles during unoccupied hours.
        """
        mock_get_output_data.return_value = {
            "Return Fan - Airflow": 10,
            "Return Fan - Power": 11,
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: (["0"] * 12) + (["1"] * 12),
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.VAVS,
            BDL_SystemKeywords.COOL_CONTROL: BDL_CoolControlOptions.CONSTANT,
            BDL_SystemKeywords.HEAT_CONTROL: BDL_HeatControlOptions.CONSTANT,
            BDL_SystemKeywords.HEAT_SET_T: "75",
            BDL_SystemKeywords.COOL_SET_T: "70",
            BDL_SystemKeywords.RETURN_FAN_LOC: BDL_ReturnFanOptions.RELIEF,
            BDL_SystemKeywords.RETURN_FLOW: "10.1",
            BDL_SystemKeywords.RETURN_KW_FLOW: "11.5",
            BDL_SystemKeywords.RETURN_STATIC: "15",
            BDL_SystemKeywords.RETURN_MTR_EFF: "0.7",
            BDL_SystemKeywords.RETURN_MECH_EFF: "0.8",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.SUPPLY_STATIC: "20",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "0.95",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "TEMPERATURE",
                },
                "air_energy_recovery": {"id": "System 1 AirEnergyRecovery"},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "CYCLING",
                "return_fans": [],
                "relief_fans": [
                    {
                        "design_airflow": 10,
                        "design_electric_power": 11,
                        "design_pressure_rise": 15.0,
                        "id": "System 1 ReliefFan",
                        "is_airflow_sized_based_on_design_day": False,
                        "motor_efficiency": 0.7,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.5599999999999999,
                    }
                ],
                "supply_fans": [
                    {
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": True,
                        "motor_efficiency": 0.9,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.855,
                    }
                ],
                "temperature_control": "CONSTANT",
            },
            "heating_system": {
                "heating_coil_setpoint": 75.0,
                "id": "System 1 HeatSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "id": "System 1",
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zonal_system_with_multiple_zones(self, mock_get_output_data):
        """Test populating System data groups from a zonal system BDL command with zone-reset DX cooling,
        heat pump heating,
        non-integrated economizer,
        and multiple zones assigned.
        Supply fans are not sized based on design day with simple spec method.
        System cycles during occupied and unoccupied hours."""
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
        }
        self.zone2 = Zone("Zone 2", self.system, self.rmd)
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["-999"] + (["0"] * 23),
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PTAC,
            BDL_SystemKeywords.COOL_CONTROL: BDL_CoolControlOptions.WARMEST,
            BDL_SystemKeywords.COOL_MAX_RESET_T: "60",
            BDL_SystemKeywords.HEAT_SET_T: "70",
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.ELEC_DX,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HEAT_PUMP,
            BDL_SystemKeywords.ECONO_LOCKOUT: BDL_SystemEconoLockoutOptions.YES,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.SUPPLY_FLOW: "100",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "DIRECT_EXPANSION",
            },
            "fan_system": {
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": False,
                    "type": "TEMPERATURE",
                },
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CYCLING",
                "operation_during_unoccupied": "CYCLING",
                "relief_fans": [],
                "return_fans": [],
                "supply_fans": [
                    {
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": False,
                        "output_validation_points": [],
                        "specification_method": "SIMPLE",
                    }
                ],
                "temperature_control": "ZONE_RESET",
            },
            "heating_system": {
                "energy_source_type": "ELECTRICITY",
                "heating_coil_setpoint": 70.0,
                "id": "System 1 HeatSys",
                "is_sized_based_on_design_day": True,
                "type": "HEAT_PUMP",
            },
            "id": "System 1",
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system(self, mock_get_output_data):
        """Test populating System data groups from a DOAS system BDL command with continuous fan operation,
        DX cooling,
        hot water heating"""
        mock_get_output_data.return_value = {}
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["-999"] * 24,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.DOAS,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.ELEC_DX,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "DIRECT_EXPANSION",
            },
            "fan_system": {
                "air_economizer": {},
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "operation_during_occupied": "CONTINUOUS",
                "relief_fans": [],
                "return_fans": [],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": True,
                        "output_validation_points": [],
                        "specification_method": "SIMPLE",
                    }
                ],
            },
            "heating_system": {
                "id": "System 1 HeatSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "id": "System 1",
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system2(self, mock_get_output_data):
        """Test populating System data groups from a DOAS system BDL command where all_occupied_off criteria is met and fan operation populates as KEEP_OFF."""
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.DOAS,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
            },
            "fan_system": {
                "air_economizer": {},
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "operation_during_occupied": "KEEP_OFF",
                "relief_fans": [],
                "return_fans": [],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": True,
                        "output_validation_points": [],
                        "specification_method": "SIMPLE",
                    }
                ],
            },
            "heating_system": {},
            "id": "System 1",
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_dual_duct_system(self, mock_get_output_data):
        """Test populating System data groups from a dual duct system BDL command
        with heating/cooling supply fans,
        DX cooling, hot water heating,
        integrated economizer,
        and ERV.
        System operates continuously during occupied hours and stays off during unoccupied hours.
        """
        mock_get_output_data.return_value = {
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
            "Heating Supply Fan - Airflow": 14,
            "Heating Supply Fan - Power": 15,
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: ["1"] * 24,
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.DDS,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.ELEC_DX,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.DDS_TYPE: BDL_DualDuctFanOptions.DUAL_FAN,
            BDL_SystemKeywords.SUPPLY_STATIC: "20",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "0.95",
            BDL_SystemKeywords.HSUPPLY_STATIC: "21",
            BDL_SystemKeywords.HSUPPLY_MTR_EFF: "0.91",
            BDL_SystemKeywords.HSUPPLY_MECH_EFF: "0.96",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "cooling_system": {
                "efficiency_metric_types": [],
                "efficiency_metric_values": [],
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "TEMPERATURE",
                },
                "air_energy_recovery": {"id": "System 1 AirEnergyRecovery"},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "id": "System 1 FanSys",
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "KEEP_OFF",
                "return_fans": [],
                "relief_fans": [],
                "supply_fans": [
                    {
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
                        "id": "System 1 SupplyFan",
                        "is_airflow_sized_based_on_design_day": True,
                        "motor_efficiency": 0.9,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.855,
                    },
                    {
                        "design_airflow": 14,
                        "design_electric_power": 15,
                        "design_pressure_rise": 21.0,
                        "id": "System 1 HeatingSupplyFan",
                        "is_airflow_sized_based_on_design_day": False,
                        "motor_efficiency": 0.91,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.8736,
                    },
                ],
                "temperature_control": "OTHER",
            },
            "heating_system": {
                "id": "System 1 HeatSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "id": "System 1",
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_sum_system(self, mock_get_output_data):
        """Verify that no system data groups are populated when the system is a SUM system."""
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {BDL_SystemKeywords.TYPE: BDL_SystemTypes.SUM}

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system1(self, mock_get_output_data):
        """Verify that no system data groups are populated when the system meets is_terminal criteria."""
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.FC,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.NONE,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.NONE,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system2(self, mock_get_output_data):
        """Verify that no system data groups are populated when the system meets alternate is_terminal criteria."""
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.PTAC,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_fan_schedule_neg_999_error(self, mock_get_output_data):
        """Verify that a VAVS system with a fan schedule with any value of -999 raises an error."""
        with self.assertRaises(ValueError):
            mock_get_output_data.return_value = {}
            self.fan_schedule_day_schedule.keyword_value_pairs = {
                BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
                BDL_DayScheduleKeywords.VALUES: ["-999"] + (["0"] * 23),
            }
            self.system.keyword_value_pairs = {
                BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
                BDL_SystemKeywords.TYPE: BDL_SystemTypes.VAVS,
            }

            self.rmd.populate_rmd_data(testing=True)
