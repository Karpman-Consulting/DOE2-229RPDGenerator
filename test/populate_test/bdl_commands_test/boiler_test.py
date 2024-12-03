import unittest
from unittest.mock import patch
import os

from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.boiler import *
from rpd_generator.bdl_structure.bdl_commands.boiler import Boiler
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import CirculationLoop
from rpd_generator.bdl_structure.bdl_commands.utility_and_economics import (
    MasterMeters,
    FuelMeter,
)
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_BoilerKeywords = BDLEnums.bdl_enums["BoilerKeywords"]
BDL_BoilerTypes = BDLEnums.bdl_enums["BoilerTypes"]
BDL_FuelTypes = BDLEnums.bdl_enums["FuelTypes"]
BDL_FuelMeterKeywords = BDLEnums.bdl_enums["FuelMeterKeywords"]
BDL_MasterMeterKeywords = BDLEnums.bdl_enums["MasterMeterKeywords"]
BoilerCombustionOptions = SchemaEnums.schema_enums["BoilerCombustionOptions"]
EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
BoilerEfficiencyMetricOptions = SchemaEnums.schema_enums[
    "BoilerEfficiencyMetricOptions"
]


class TestFuelBoiler(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.rmd.file_path = os.path.abspath(
            os.path.join(
                script_dir, "../../full_rpd_test/E-2/229 Test Case E-2 (CHW VAV)"
            )
        )
        self.master_meter = MasterMeters("Master Meters", self.rmd)
        self.fuel_meter = FuelMeter("Test Fuel Meter", self.rmd)
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.loop = CirculationLoop("Test HW Loop", self.rmd)

        self.rmd.bdl_obj_instances["Boiler 1"] = self.boiler
        self.rmd.bdl_obj_instances["Test HW Loop"] = self.loop
        self.rmd.bdl_obj_instances["Master Meters"] = self.master_meter
        self.rmd.bdl_obj_instances["Test Fuel Meter"] = self.fuel_meter

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_with_fuel_meter(self, mock_get_output_data):
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 188203.578125,
            "Boilers - Design Parameters - Flow": 28.88204002380371,
            "Boilers - Design Parameters - Efficiency": 0.9000089372091853,
            "Boilers - Design Parameters - Electric Input Ratio": 0.0,
            "Boilers - Design Parameters - Fuel Input Ratio": 1.1111,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        fuel_meter = FuelMeter("Test Fuel Meter", self.rmd)
        fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.METHANOL
        }
        self.fuel_meter.populate_data_elements()

        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.HW_BOILER,
            BDL_BoilerKeywords.FUEL_METER: "Test Fuel Meter",
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.boiler.populate_data_elements()
        self.boiler.populate_data_group()

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
            "efficiency": [0.900009000090001, 0.920009000090001, 0.9085817143885725],
            "efficiency_metrics": ["THERMAL", "COMBUSTION", "ANNUAL_FUEL_UTILIZATION"],
        }

        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_without_fuel_meter(self, mock_get_output_data):
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 188203.578125,
            "Boilers - Design Parameters - Flow": 28.88204002380371,
            "Boilers - Design Parameters - Efficiency": 0.9000089372091853,
            "Boilers - Design Parameters - Electric Input Ratio": 0.0,
            "Boilers - Design Parameters - Fuel Input Ratio": 1.1111,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 188203.578125,
        }
        self.rmd.bdl_obj_instances = {}

        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.HW_BOILER_W_DRAFT,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.boiler.populate_data_elements()
        self.boiler.populate_data_group()

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
            "efficiency": [0.9000089372091853, 0.9200089372091853, 0.9085816425247832],
            "efficiency_metrics": ["THERMAL", "COMBUSTION", "ANNUAL_FUEL_UTILIZATION"],
        }

        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)


class TestElectricBoiler(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        validate_configuration.find_equest_installation()

        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH

        self.master_meter = MasterMeters("Master Meters", self.rmd)
        self.fuel_meter = FuelMeter("Test Fuel Meter", self.rmd)
        self.boiler = Boiler("Boiler 1", self.rmd)
        self.loop = CirculationLoop("Test HW Loop", self.rmd)

        self.rmd.bdl_obj_instances["Boiler 1"] = self.boiler
        self.rmd.bdl_obj_instances["Test HW Loop"] = self.loop
        self.rmd.bdl_obj_instances["Master Meters"] = self.master_meter
        self.rmd.bdl_obj_instances["Test Fuel Meter"] = self.master_meter

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_electric_boiler(self, mock_get_output_data):
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 882239.8125,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 882239.8125,
            "Boilers - Design Parameters - Electric Input Ratio": 1.02,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
        }
        self.rmd.bdl_obj_instances = {}

        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.ELEC_HW_BOILER,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.boiler.populate_data_elements()
        self.boiler.populate_data_group()

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
            "efficiency": [0.9803921568627451],
            "efficiency_metrics": ["THERMAL"],
        }

        self.assertDictEqual(expected_data_structure, self.boiler.boiler_data_structure)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_elements_electric_steam_boiler_1EIR(
        self, mock_get_output_data
    ):
        mock_get_output_data.return_value = {
            "Boilers - Design Parameters - Capacity": 882239.8125,
            "Boilers - Rated Capacity at Peak (Btu/hr)": 882239.8125,
            "Boilers - Design Parameters - Electric Input Ratio": 1.0,
            "Boilers - Design Parameters - Auxiliary Power": 0.0,
        }
        self.rmd.bdl_obj_instances = {}

        self.boiler.keyword_value_pairs = {
            BDL_BoilerKeywords.TYPE: BDL_BoilerTypes.ELEC_STM_BOILER,
            BDL_BoilerKeywords.HW_LOOP: "Test HW Loop",
            BDL_BoilerKeywords.MIN_RATIO: "0.33",
        }

        self.boiler.populate_data_elements()
        self.boiler.populate_data_group()

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
            "efficiency": [1, 1, 1],
            "efficiency_metrics": ["THERMAL", "COMBUSTION", "ANNUAL_FUEL_UTILIZATION"],
        }

        self.assertDictEqual(self.boiler.boiler_data_structure, expected_data_structure)
