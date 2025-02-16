import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.project import (
    RunPeriod,
    Holidays,
    BDL_RunPeriodKeywords,
    BDL_HolidayKeywords,
    BDL_HolidayTypes,
)
from rpd_generator.bdl_structure.bdl_commands.schedule import (
    Schedule,
    WeekSchedulePD,
    DaySchedulePD,
    BDL_DayScheduleKeywords,
    BDL_WeekScheduleKeywords,
    BDL_ScheduleKeywords,
    BDL_ScheduleTypes,
)
from rpd_generator.bdl_structure.bdl_commands.utility_and_economics import (
    MasterMeters,
    FuelMeter,
    BDL_FuelMeterKeywords,
    BDL_FuelTypes,
)
from rpd_generator.bdl_structure.bdl_commands.zone import Zone
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import (
    CirculationLoop,
    BDL_CirculationLoopKeywords,
    BDL_CirculationLoopTypes,
)
from rpd_generator.bdl_structure.bdl_commands.boiler import (
    Boiler,
    BDL_BoilerKeywords,
    BDL_BoilerTypes,
)
from rpd_generator.bdl_structure.bdl_commands.system import *
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BDL_SystemEconoLockoutOptions = BDLEnums.bdl_enums["SystemEconoLockoutOptions"]


class TestSystems(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rpd = RulesetProjectDescription("Test RPD")
        self.rmd = RulesetModelDescription("Test RMD", self.rpd)
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = System("System 1", self.rmd)
        self.zone1 = Zone("Zone 1", self.system, self.rmd)
        self.run_period = RunPeriod("Run Period 1", self.rmd)
        self.holidays = Holidays("Holidays 1", self.rmd)
        self.master_meter = MasterMeters("Master Meters", self.rmd)
        self.fuel_meter = FuelMeter("Fuel Meter", self.rmd)
        self.circ_loop = CirculationLoop("Circulation Loop", self.rmd)

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
        self.master_meter.keyword_value_pairs = {
            BDL_MasterMeterKeywords.HEAT_FUEL_METER: "Fuel Meter"
        }
        self.circ_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
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
        """
        Test populating a System data group from a multi-zone VAV system BDL command with zone-reset temperature
        controls, a return fan, propane furnace preheat system, CHW cooling system, integrated economizer, and ERV.
        Supply fan is sized based on design day with detailed spec method. System operates continuously during occupied
        hours and cycles during unoccupied hours.
        """
        mock_get_output_data.return_value = {
            "Return Fan - Airflow": 10,
            "Return Fan - Power": 11,
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
            "Design Cooling Capacity": 120000,
            "Rated Cooling SHR": 0.7,
            "Rated Cooling Capacity": 124000,
            "Design Preheat Capacity": -100000,
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.LPG
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: (["0"] * 12) + (["1"] * 12),
        }
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.VAVS,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.ERV_RECOVER_TYPE: BDL_EnergyRecoveryTypes.SENSIBLE_WHEEL,
            BDL_SystemKeywords.ERV_RUN_CTRL: BDL_EnergyRecoveryOperationOptions.WHEN_FANS_ON,
            BDL_SystemKeywords.ERV_TEMP_CTRL: BDL_EnergyRecoveryTemperatureControlOptions.MIXED_AIR_RESET,
            BDL_SystemKeywords.ERV_SENSIBLE_EFF: "0.7",
            BDL_SystemKeywords.ERV_LATENT_EFF: "0.6",
            BDL_SystemKeywords.ERV_OA_FLOW: "5000",
            BDL_SystemKeywords.ERV_EXH_FLOW: "5500",
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.PREHEAT_CAPACITY: "-48000",
            BDL_SystemKeywords.PREHEAT_T: "60",
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
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_ENTHALPY,
            BDL_SystemKeywords.SUPPLY_STATIC: "20",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "0.95",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "System 1",
            "cooling_system": {
                "id": "System 1 CoolSys",
                "design_total_cool_capacity": 120000.0,
                "rated_sensible_cool_capacity": 86800.0,
                "rated_total_cool_capacity": 124000.0,
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "ENTHALPY",
                },
                "air_energy_recovery": {
                    "id": "System 1 AirEnergyRecovery",
                    "type": "SENSIBLE_HEAT_WHEEL",
                    "energy_recovery_operation": "WHEN_FANS_ON",
                    "energy_recovery_supply_air_temperature_control": "MIXED_AIR_RESET",
                    "outdoor_airflow": 5000,
                    "exhaust_airflow": 5500,
                    "design_sensible_effectiveness": 0.7,
                    "design_latent_effectiveness": 0.6,
                },
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "CYCLING",
                "relief_fans": [],
                "return_fans": [
                    {
                        "id": "System 1 ReturnFan",
                        "design_airflow": 10,
                        "design_electric_power": 11,
                        "design_pressure_rise": 15.0,
                        "is_airflow_sized_based_on_design_day": False,
                        "motor_efficiency": 0.7,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.5599999999999999,
                    }
                ],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
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
            "preheat_system": {
                "id": "System 1 PreheatSys",
                "rated_capacity": 48000.0,
                "design_capacity": 100000.0,
                "heating_coil_setpoint": 60.0,
                "energy_source_type": "PROPANE",
                "is_sized_based_on_design_day": False,
                "type": "FURNACE",
            },
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_system_multizone_vav2(self, mock_get_output_data):
        """
        Test populating a System data group from a multi-zone VAV system BDL command with constant temperature controls,
        a relief fan, fuel-oil HW heating system, CHW cooling system, integrated economizer, and ERV. Supply fan is
        sized based on design day with detailed spec method. System operates continuously during occupied hours and
        cycles during unoccupied hours.
        """
        mock_get_output_data.return_value = {
            "Return Fan - Airflow": 10,
            "Return Fan - Power": 11,
            "Supply Fan - Airflow": 12,
            "Supply Fan - Power": 13,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 882239.8125,
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.FUEL_OIL
        }
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.HW_BOILER,
            BDL_BoilerKeywords.HW_LOOP: "Circulation Loop",
        }
        self.fan_schedule_day_schedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: (["0"] * 12) + (["1"] * 12),
        }

        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.VAVS,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.ERV_RECOVER_TYPE: BDL_EnergyRecoveryTypes.ENTHALPY_WHEEL,
            BDL_SystemKeywords.ERV_RUN_CTRL: BDL_EnergyRecoveryOperationOptions.WHEN_MIN_OA,
            BDL_SystemKeywords.ERV_TEMP_CTRL: BDL_EnergyRecoveryTemperatureControlOptions.FIXED_SETPT,
            BDL_SystemKeywords.ERV_SENSIBLE_EFF: "0.7",
            BDL_SystemKeywords.ERV_LATENT_EFF: "0.6",
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
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
            BDL_SystemKeywords.HW_LOOP: "Circulation Loop",
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.ECONO_LIMIT_T: "70",
            BDL_SystemKeywords.SUPPLY_STATIC: "20",
            BDL_SystemKeywords.SUPPLY_MTR_EFF: "0.9",
            BDL_SystemKeywords.SUPPLY_MECH_EFF: "0.95",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "System 1",
            "cooling_system": {
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "TEMPERATURE",
                    "high_limit_shutoff_temperature": 70.0,
                },
                "air_energy_recovery": {
                    "id": "System 1 AirEnergyRecovery",
                    "type": "ENTHALPY_HEAT_WHEEL",
                    "energy_recovery_operation": "WHEN_MINIMUM_OUTSIDE_AIR",
                    "energy_recovery_supply_air_temperature_control": "FIXED_SETPOINT",
                    "design_sensible_effectiveness": 0.7,
                    "design_latent_effectiveness": 0.6,
                },
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "CYCLING",
                "return_fans": [],
                "relief_fans": [
                    {
                        "id": "System 1 ReliefFan",
                        "design_airflow": 10,
                        "design_electric_power": 11,
                        "design_pressure_rise": 15.0,
                        "is_airflow_sized_based_on_design_day": False,
                        "motor_efficiency": 0.7,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.5599999999999999,
                    }
                ],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
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
                "id": "System 1 HeatSys",
                "type": "FLUID_LOOP",
                "energy_source_type": "FUEL_OIL",
                "hot_water_loop": "Circulation Loop",
                "heating_coil_setpoint": 75.0,
                "is_sized_based_on_design_day": True,
            },
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zonal_system_with_multiple_zones(self, mock_get_output_data):
        """
        Test populating System data groups from a zonal system BDL command with zone-reset DX cooling, heat pump
        heating, non-integrated economizer, and multiple zones assigned. Supply fans are not sized based on design day
        with simple spec method. System cycles during occupied and unoccupied hours.
        """
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
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.FC,
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.COOL_CONTROL: BDL_CoolControlOptions.WARMEST,
            BDL_SystemKeywords.COOL_MAX_RESET_T: "60",
            BDL_SystemKeywords.HEAT_SET_T: "70",
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.ELEC_DX,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HEAT_PUMP,
            BDL_SystemKeywords.ECONO_LOCKOUT: BDL_SystemEconoLockoutOptions.YES,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.ECONO_LIMIT_T: "70",
            BDL_SystemKeywords.SUPPLY_FLOW: "100",
            BDL_SystemKeywords.NIGHT_CYCLE_CTRL: BDL_NightCycleControlOptions.CYCLE_ON_ANY,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "System 1",
            "cooling_system": {
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": False,
                    "type": "TEMPERATURE",
                    "high_limit_shutoff_temperature": 70.0,
                },
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CYCLING",
                "operation_during_unoccupied": "CYCLING",
                "relief_fans": [],
                "return_fans": [],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "is_airflow_sized_based_on_design_day": False,
                        "output_validation_points": [],
                        "specification_method": "SIMPLE",
                    }
                ],
                "temperature_control": "ZONE_RESET",
            },
            "heating_system": {
                "id": "System 1 HeatSys",
                "energy_source_type": "ELECTRICITY",
                "heating_coil_setpoint": 70.0,
                "is_sized_based_on_design_day": True,
                "type": "HEAT_PUMP",
            },
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

        zonal_system_2 = self.rmd.bdl_obj_instances.get("System 1 - Zone 2")
        expected_data_structure["id"] = "System 1 - Zone 2"
        self.assertEqual(expected_data_structure, zonal_system_2.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system(self, mock_get_output_data):
        """
        Test populating System data groups from a DOAS system BDL command with continuous fan operation, DX cooling, hot
        water heating
        """
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
            "id": "System 1",
            "cooling_system": {
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "DIRECT_EXPANSION",
            },
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {},
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
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
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system2(self, mock_get_output_data):
        """
        Test populating System data groups from a DOAS system BDL command where all_occupied_off criteria is met and fan
        operation populates as KEEP_OFF.
        """
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.DOAS,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "System 1",
            "cooling_system": {},
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {},
                "air_energy_recovery": {},
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
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
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_dual_duct_system(self, mock_get_output_data):
        """
        Test populating System data groups from a dual duct system BDL command with heating/cooling supply fans, DX
        cooling, hot water heating, integrated economizer, and ERV. System operates continuously during occupied hours
        and stays off during unoccupied hours.
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
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.DDS,
            BDL_SystemKeywords.RECOVER_EXHAUST: BDL_EnergyRecoveryOptions.YES,
            BDL_SystemKeywords.ERV_RECOVER_TYPE: BDL_EnergyRecoveryTypes.HEAT_PIPE,
            BDL_SystemKeywords.ERV_RUN_CTRL: BDL_EnergyRecoveryOperationOptions.OA_EXHAUST_DH,
            BDL_SystemKeywords.ERV_TEMP_CTRL: BDL_EnergyRecoveryTemperatureControlOptions.FLOAT,
            BDL_SystemKeywords.ERV_SENSIBLE_EFF: "0.7",
            BDL_SystemKeywords.ERV_LATENT_EFF: "0.6",
            BDL_SystemKeywords.FAN_SCHEDULE: "Fan Annual Schedule",
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.ELEC_DX,
            BDL_SystemKeywords.OA_CONTROL: BDL_EconomizerOptions.OA_TEMP,
            BDL_SystemKeywords.ECONO_LIMIT_T: "70",
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
            "id": "System 1",
            "cooling_system": {
                "id": "System 1 CoolSys",
                "is_sized_based_on_design_day": True,
                "type": "FLUID_LOOP",
            },
            "fan_system": {
                "id": "System 1 FanSys",
                "air_economizer": {
                    "id": "System 1 AirEconomizer",
                    "is_integrated": True,
                    "type": "TEMPERATURE",
                    "high_limit_shutoff_temperature": 70.0,
                },
                "air_energy_recovery": {
                    "id": "System 1 AirEnergyRecovery",
                    "type": "HEAT_PIPE",
                    "energy_recovery_operation": "OTHER",
                    "energy_recovery_supply_air_temperature_control": "OTHER",
                    "design_sensible_effectiveness": 0.7,
                    "design_latent_effectiveness": 0.6,
                },
                "exhaust_fans": [],
                "has_fully_ducted_return": False,
                "maximum_outdoor_airflow": 12,
                "operation_during_occupied": "CONTINUOUS",
                "operation_during_unoccupied": "KEEP_OFF",
                "return_fans": [],
                "relief_fans": [],
                "supply_fans": [
                    {
                        "id": "System 1 SupplyFan",
                        "design_airflow": 12,
                        "design_electric_power": 13,
                        "design_pressure_rise": 20.0,
                        "is_airflow_sized_based_on_design_day": True,
                        "motor_efficiency": 0.9,
                        "output_validation_points": [],
                        "specification_method": "DETAILED",
                        "total_efficiency": 0.855,
                    },
                    {
                        "id": "System 1 HeatingSupplyFan",
                        "design_airflow": 14,
                        "design_electric_power": 15,
                        "design_pressure_rise": 21.0,
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
            "preheat_system": {},
        }
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_sum_system(self, mock_get_output_data):
        """
        Verify that no system data groups are populated when the system is a SUM system.
        """
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {BDL_SystemKeywords.TYPE: BDL_SystemTypes.SUM}

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system1(self, mock_get_output_data):
        """
        Verify that no system data groups are populated when the system meets is_terminal criteria.
        """
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.UHT,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.NONE,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system2(self, mock_get_output_data):
        """
        Verify that no system data groups are populated when the system meets alternate is_terminal criteria.
        """
        mock_get_output_data.return_value = {}
        self.system.keyword_value_pairs = {
            BDL_SystemKeywords.TYPE: BDL_SystemTypes.FC,
            BDL_SystemKeywords.HEAT_SOURCE: BDL_SystemHeatingTypes.HOT_WATER,
            BDL_SystemKeywords.COOL_SOURCE: BDL_SystemCoolingTypes.CHILLED_WATER,
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {}
        self.assertEqual(expected_data_structure, self.system.system_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_fan_schedule_neg_999_error(self, mock_get_output_data):
        """
        Verify that a VAVS system with a fan schedule with any value of -999 raises an error.
        """
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
