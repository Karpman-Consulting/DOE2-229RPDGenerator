import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.schedule import (
    DaySchedulePD,
    WeekSchedulePD,
    Schedule,
    BDL_DayScheduleKeywords,
    BDL_WeekScheduleKeywords,
    BDL_ScheduleKeywords,
    BDL_ScheduleTypes,
)
from rpd_generator.bdl_structure.bdl_commands.system import System
from rpd_generator.bdl_structure.bdl_commands.zone import Zone
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
from rpd_generator.bdl_structure.bdl_commands.floor import Floor
from rpd_generator.bdl_structure.bdl_commands.space import *


class TestSpaces(unittest.TestCase):
    @patch("rpd_generator.bdl_structure.bdl_commands.system.System")
    def setUp(self, MockSystem):
        self.maxDiff = None
        self.rpd = RulesetProjectDescription()
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.bdl_obj_instances["ASHRAE 229"] = self.rpd
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)
        self.rmd.space_map = {"Space 1": self.zone}
        self.floor = Floor("Floor 1", self.rmd)
        self.space = Space("Space 1", self.floor, self.rmd)
        self.daySchedule = DaySchedulePD("Day Schedule Non-continuous", self.rmd)
        self.weekSchedule = WeekSchedulePD("Week Schedule Non-continuous", self.rmd)
        self.run_period = RunPeriod("Run Period 1", self.rmd)
        self.holidays = Holidays("Holidays 1", self.rmd)
        self.annualSchedule = Schedule("Annual Schedule 1", self.rmd)

        self.run_period.keyword_value_pairs = {
            BDL_RunPeriodKeywords.END_YEAR: "2021",
        }
        self.holidays.keyword_value_pairs = {
            BDL_HolidayKeywords.TYPE: BDL_HolidayTypes.OFFICIAL_US,
        }
        self.daySchedule.keyword_value_pairs = {
            BDL_DayScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_DayScheduleKeywords.VALUES: [str(i % 2) for i in range(0, 24)],
        }
        self.weekSchedule.keyword_value_pairs = {
            BDL_WeekScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_WeekScheduleKeywords.DAY_SCHEDULES: ["Day Schedule Non-continuous"]
            * 12,
        }
        self.annualSchedule.keyword_value_pairs = {
            BDL_ScheduleKeywords.TYPE: BDL_ScheduleTypes.ON_OFF,
            BDL_ScheduleKeywords.WEEK_SCHEDULES: "Week Schedule Non-continuous",
            BDL_ScheduleKeywords.MONTH: "12",
            BDL_ScheduleKeywords.DAY: "31",
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_space(self, mock_get_output_data):
        """Tests that the space data structure is populated correctly, given valid inputs with 1 interior lighting and 1 misc equipment."""
        mock_get_output_data.return_value = {}
        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.VOLUME: "4000",
            BDL_SpaceKeywords.AREA: "400",
            BDL_SpaceKeywords.LIGHTING_SCHEDUL: "Annual Schedule 1",
            BDL_SpaceKeywords.LIGHTING_W_AREA: "20.1",
            BDL_SpaceKeywords.LIGHTING_KW: "30.1",
            BDL_SpaceKeywords.EQUIP_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.EQUIPMENT_W_AREA: "40.1",
            BDL_SpaceKeywords.EQUIPMENT_KW: "50.1",
            BDL_SpaceKeywords.EQUIP_SENSIBLE: "0.4",
            BDL_SpaceKeywords.EQUIP_LATENT: "0.5",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.PEOPLE_HG_SENS: "2",
            BDL_SpaceKeywords.PEOPLE_HG_LAT: "3",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Space 1",
            "interior_lighting": [
                {
                    "id": "Space 1 IntLtg1",
                    "lighting_multiplier_schedule": "Annual Schedule 1",
                    "power_per_area": 95.35,
                }
            ],
            "miscellaneous_equipment": [
                {
                    "id": "Space 1 MiscEqp1",
                    "energy_type": "ELECTRICITY",
                    "power": 66.14,
                    "multiplier_schedule": "Annual Schedule 1",
                    "sensible_fraction": 0.4,
                    "latent_fraction": 0.5,
                },
            ],
            "service_water_heating_uses": [],
            "floor_area": 400.0,
            "number_of_occupants": 10.0,
            "occupant_multiplier_schedule": "Annual Schedule 1",
            "occupant_sensible_heat_gain": 2.0,
            "occupant_latent_heat_gain": 3.0,
        }
        self.assertEqual(expected_data_structure, self.space.space_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_space_multiple_lighting_schedules(
        self, mock_get_output_data
    ):
        """Tests that the interior_lighting and miscellaneous equipment sub data structures are populated correctly,
        given multiple lighting schedules and multiple misc equipment."""
        mock_get_output_data.return_value = {}
        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.VOLUME: "4000",
            BDL_SpaceKeywords.AREA: "400",
            BDL_SpaceKeywords.LIGHTING_SCHEDUL: [
                "Annual Schedule 1",
                "Annual Schedule 1",
            ],
            BDL_SpaceKeywords.LIGHTING_W_AREA: ["20.1", "20.2"],
            BDL_SpaceKeywords.LIGHTING_KW: ["30.1", "30.2"],
            BDL_SpaceKeywords.EQUIP_SCHEDULE: [
                "Annual Schedule 1",
                "Annual Schedule 1",
            ],
            BDL_SpaceKeywords.EQUIPMENT_W_AREA: ["40.1", "40.1"],
            BDL_SpaceKeywords.EQUIPMENT_KW: ["50.1", "50.1"],
            BDL_SpaceKeywords.EQUIP_SENSIBLE: ["0.4", "0.4"],
            BDL_SpaceKeywords.EQUIP_LATENT: ["0.5", "0.5"],
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.PEOPLE_HG_SENS: "2",
            BDL_SpaceKeywords.PEOPLE_HG_LAT: "3",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Space 1",
            "interior_lighting": [
                {
                    "id": "Space 1 IntLtg1",
                    "lighting_multiplier_schedule": "Annual Schedule 1",
                    "power_per_area": 95.35,
                },
                {
                    "id": "Space 1 IntLtg2",
                    "lighting_multiplier_schedule": "Annual Schedule 1",
                    "power_per_area": 95.7,
                },
            ],
            "miscellaneous_equipment": [
                {
                    "id": "Space 1 MiscEqp1",
                    "energy_type": "ELECTRICITY",
                    "power": 66.14,
                    "multiplier_schedule": "Annual Schedule 1",
                    "sensible_fraction": 0.4,
                    "latent_fraction": 0.5,
                },
                {
                    "id": "Space 1 MiscEqp2",
                    "energy_type": "ELECTRICITY",
                    "power": 66.14,
                    "multiplier_schedule": "Annual Schedule 1",
                    "sensible_fraction": 0.4,
                    "latent_fraction": 0.5,
                },
            ],
            "service_water_heating_uses": [],
            "floor_area": 400.0,
            "number_of_occupants": 10.0,
            "occupant_multiplier_schedule": "Annual Schedule 1",
            "occupant_sensible_heat_gain": 2.0,
            "occupant_latent_heat_gain": 3.0,
        }
        self.assertEqual(expected_data_structure, self.space.space_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_space_multiple_equipment_schedules(
        self, mock_get_output_data
    ):
        """Tests that the miscellaneous_equipment sub data structure is populated correctly, given multiple
        equipment schedules and internal energy sources."""
        mock_get_output_data.return_value = {}
        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.VOLUME: "4000",
            BDL_SpaceKeywords.AREA: "400",
            BDL_SpaceKeywords.LIGHTING_SCHEDUL: "Annual Schedule 1",
            BDL_SpaceKeywords.LIGHTING_W_AREA: "2",
            BDL_SpaceKeywords.EQUIP_SCHEDULE: [
                "Annual Schedule 1",
                "Annual Schedule 1",
            ],
            BDL_SpaceKeywords.EQUIPMENT_W_AREA: ["40.1", "40.2"],
            BDL_SpaceKeywords.EQUIPMENT_KW: ["50.1", "50.2"],
            BDL_SpaceKeywords.EQUIP_SENSIBLE: ["0.4", "0.41"],
            BDL_SpaceKeywords.EQUIP_LATENT: ["0.6", "0.59"],
            BDL_SpaceKeywords.SOURCE_SCHEDULE: [
                "Annual Schedule 1",
                "Annual Schedule 1",
            ],
            BDL_SpaceKeywords.SOURCE_TYPE: [
                BDL_InternalEnergySourceOptions.GAS,
                BDL_InternalEnergySourceOptions.ELECTRIC,
            ],
            BDL_SpaceKeywords.SOURCE_POWER: ["150", "200"],
            BDL_SpaceKeywords.SOURCE_SENSIBLE: ["0.6", "1"],
            BDL_SpaceKeywords.SOURCE_LATENT: "0.4",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.PEOPLE_HG_SENS: "2",
            BDL_SpaceKeywords.PEOPLE_HG_LAT: "3",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Space 1",
            "interior_lighting": [
                {
                    "id": "Space 1 IntLtg1",
                    "lighting_multiplier_schedule": "Annual Schedule 1",
                    "power_per_area": 2.0,
                }
            ],
            "miscellaneous_equipment": [
                {
                    "id": "Space 1 MiscEqp1",
                    "energy_type": "ELECTRICITY",
                    "power": 66.14,
                    "multiplier_schedule": "Annual Schedule 1",
                    "sensible_fraction": 0.4,
                    "latent_fraction": 0.6,
                },
                {
                    "id": "Space 1 MiscEqp2",
                    "energy_type": "ELECTRICITY",
                    "power": 66.28,
                    "multiplier_schedule": "Annual Schedule 1",
                    "sensible_fraction": 0.41,
                    "latent_fraction": 0.59,
                },
                {
                    "id": "Space 1 MiscEqp3",
                    "energy_type": "NATURAL_GAS",
                    "power": 0.04396066666666667,
                },
                {
                    "id": "Space 1 MiscEqp4",
                    "energy_type": "ELECTRICITY",
                    "power": 0.05861422222222223,
                },
            ],
            "service_water_heating_uses": [],
            "floor_area": 400.0,
            "number_of_occupants": 10.0,
            "occupant_multiplier_schedule": "Annual Schedule 1",
            "occupant_sensible_heat_gain": 2.0,
            "occupant_latent_heat_gain": 3.0,
        }
        self.assertEqual(expected_data_structure, self.space.space_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_space_no_equip_nor_lighting(self, mock_get_output_data):
        """Tests that the space data structure is populated correctly, given no lighting nor equipment in the space."""
        mock_get_output_data.return_value = {}
        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.VOLUME: "4000",
            BDL_SpaceKeywords.AREA: "400",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.PEOPLE_HG_SENS: "2",
            BDL_SpaceKeywords.PEOPLE_HG_LAT: "3",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Space 1",
            "interior_lighting": [],
            "miscellaneous_equipment": [],
            "service_water_heating_uses": [],
            "floor_area": 400.0,
            "number_of_occupants": 10.0,
            "occupant_multiplier_schedule": "Annual Schedule 1",
            "occupant_sensible_heat_gain": 2.0,
            "occupant_latent_heat_gain": 3.0,
        }
        self.assertEqual(expected_data_structure, self.space.space_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_space_process_hot_water_internal_energies(
        self, mock_get_output_data
    ):
        """Tests that the energy sources populate as NONE when the internal energy source is set to PROCESS and HOT_WATER."""
        mock_get_output_data.return_value = {}
        self.space.keyword_value_pairs = {
            BDL_SpaceKeywords.VOLUME: "4000",
            BDL_SpaceKeywords.AREA: "400",
            BDL_SpaceKeywords.NUMBER_OF_PEOPLE: "10",
            BDL_SpaceKeywords.PEOPLE_SCHEDULE: "Annual Schedule 1",
            BDL_SpaceKeywords.PEOPLE_HG_SENS: "2",
            BDL_SpaceKeywords.PEOPLE_HG_LAT: "3",
            BDL_SpaceKeywords.SOURCE_SCHEDULE: [
                "Annual Schedule 1",
                "Annual Schedule 1",
            ],
            BDL_SpaceKeywords.SOURCE_TYPE: [
                BDL_InternalEnergySourceOptions.PROCESS,
                BDL_InternalEnergySourceOptions.HOT_WATER,
            ],
            BDL_SpaceKeywords.SOURCE_POWER: ["150", "200"],
            BDL_SpaceKeywords.SOURCE_SENSIBLE: "0.6",
            BDL_SpaceKeywords.SOURCE_LATENT: ["0.4", "1"],
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Space 1",
            "interior_lighting": [],
            "miscellaneous_equipment": [
                {
                    "id": "Space 1 MiscEqp1",
                    "energy_type": "NONE",
                    "power": 0.04396066666666667,
                },
                {
                    "id": "Space 1 MiscEqp2",
                    "energy_type": "NONE",
                    "power": 0.05861422222222223,
                },
            ],
            "service_water_heating_uses": [],
            "floor_area": 400.0,
            "number_of_occupants": 10.0,
            "occupant_multiplier_schedule": "Annual Schedule 1",
            "occupant_sensible_heat_gain": 2.0,
            "occupant_latent_heat_gain": 3.0,
        }
        self.assertEqual(expected_data_structure, self.space.space_data_structure)
