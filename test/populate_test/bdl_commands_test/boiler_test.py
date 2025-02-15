import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.boiler import *
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import CirculationLoop
from rpd_generator.bdl_structure.bdl_commands.utility_and_economics import (
    MasterMeters,
    FuelMeter,
)
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_CirculationLoopKeywords = BDLEnums.bdl_enums["CirculationLoopKeywords"]


class TestFuelBoiler(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.master_meter = MasterMeters("Master Meters", self.rmd)
        self.fuel_meter = FuelMeter("Test Fuel Meter", self.rmd)
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.loop = CirculationLoop("Test HW Loop", self.rmd)
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: "HOT_WATER",
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_with_fuel_meter(self, mock_get_output_data):
        """Tests that all values populate for a fuel boiler with expected values, given valid inputs,
        with a fuel meter defined"""
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 188203.578125,
            "Boilers - Design Parameters - Flow": 28.88204002380371,
            "Boilers - Design Parameters - Efficiency": 0.9000089372091853,
            "Boilers - Design Parameters - Electric Input Ratio": 0.0,
            "Boilers - Design Parameters - Fuel Input Ratio": 1.1111,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.METHANOL
        }
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.HW_BOILER,
            BDL_BoilerKeywords.FUEL_METER: "Test Fuel Meter",
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Boiler 1",
            "draft_type": "NATURAL",
            "energy_source_type": "OTHER",
            "output_validation_points": [],
            "loop": "Test HW Loop",
            "auxiliary_power": 0.0,
            "design_capacity": 0.188203578125,
            "rated_capacity": 0.188203578125,
            "operation_lower_limit": 0,
            "operation_upper_limit": 0.188203578125,
            "minimum_load_ratio": 0.33,
            "efficiency_metric_values": [0.900009000090001],
            "efficiency_metric_types": ["THERMAL"],
        }
        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_without_fuel_meter(self, mock_get_output_data):
        """Test the branch of logic for fuel boilers where a fuel meter is not defined for the boiler, so the fuel type
        defaults to that of the master meter"""
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 188203.578125,
            "Boilers - Design Parameters - Flow": 28.88204002380371,
            "Boilers - Design Parameters - Efficiency": 0.9000089372091853,
            "Boilers - Design Parameters - Electric Input Ratio": 0.0,
            "Boilers - Design Parameters - Fuel Input Ratio": 1.1111,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        self.master_meter.keyword_value_pairs = {
            BDL_MasterMeterKeywords.HEAT_FUEL_METER: "Test Fuel Meter"
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.HW_BOILER_W_DRAFT,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Boiler 1",
            "draft_type": "FORCED",
            "energy_source_type": "NATURAL_GAS",
            "output_validation_points": [],
            "loop": "Test HW Loop",
            "auxiliary_power": 0.0,
            "design_capacity": 0.188203578125,
            "rated_capacity": 0.188203578125,
            "operation_lower_limit": 0,
            "operation_upper_limit": 0.188203578125,
            "minimum_load_ratio": 0.33,
            "efficiency_metric_values": [0.900009000090001],
            "efficiency_metric_types": ["THERMAL"],
        }
        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)


class TestElectricBoiler(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH

        self.master_meter = MasterMeters("Master Meters", self.rmd)
        self.fuel_meter = FuelMeter("Test Fuel Meter", self.rmd)
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.loop = CirculationLoop("Test HW Loop", self.rmd)
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: "HOT_WATER",
        }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_electric_boiler(self, mock_get_output_data):
        """Test the branch of logic for electric boilers with an EIR other than 1.0"""
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 882239.8125,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 882239.8125,
            "Boilers - Design Parameters - Electric Input Ratio": 1.02,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
        }
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.ELEC_HW_BOILER,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Boiler 1",
            "draft_type": "NATURAL",
            "energy_source_type": "ELECTRICITY",
            "output_validation_points": [],
            "loop": "Test HW Loop",
            "auxiliary_power": 0.0,
            "design_capacity": 0.8822398124999999,
            "rated_capacity": 0.8822398124999999,
            "operation_lower_limit": 0,
            "operation_upper_limit": 0.8822398124999999,
            "minimum_load_ratio": 0.33,
            "efficiency_metric_values": [0.9803921568627451],
            "efficiency_metric_types": ["THERMAL"],
        }
        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_electric_steam_boiler_1EIR(
        self, mock_get_output_data
    ):
        """Test the branch of logic for electric boilers with an EIR of 1.0"""
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 882239.8125,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 882239.8125,
            "Boilers - Design Parameters - Electric Input Ratio": 1.0,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
        }
        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.ELEC_STM_BOILER,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Boiler 1",
            "draft_type": "NATURAL",
            "energy_source_type": "ELECTRICITY",
            "output_validation_points": [],
            "loop": "Test HW Loop",
            "auxiliary_power": 0.0,
            "design_capacity": 0.8822398124999999,
            "rated_capacity": 0.8822398124999999,
            "operation_lower_limit": 0,
            "operation_upper_limit": 0.8822398124999999,
            "minimum_load_ratio": 0.33,
            "efficiency_metric_values": [1, 1],
            "efficiency_metric_types": ["THERMAL", "COMBUSTION"],
        }
        self.assertDictEqual(self.boiler.boiler_data_structure, expected_data_structure)
