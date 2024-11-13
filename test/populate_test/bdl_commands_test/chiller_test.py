import unittest
import os

from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.chiller import Chiller, BDL_ChillerTypes
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ChillerKeywords = BDLEnums.bdl_enums["ChillerKeywords"]
EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]


class TestElectricChillers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        validate_configuration.find_equest_installation()
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.rmd.file_path = os.path.abspath(
            os.path.join(
                script_dir, "../../full_rpd_test/E-2/229 Test Case E-2 (CHW VAV)"
            )
        )
        self.chiller = Chiller("Chiller 1", self.rmd)

    def test_populate_data_elements_with_centrif_chiller(self):
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.TYPE: BDL_ChillerTypes.ELEC_OPEN_CENT,
            BDL_ChillerKeywords.CHW_LOOP: "Chilled Water Loop (Primary)",
            BDL_ChillerKeywords.CW_LOOP: "Condenser Water Loop",
            BDL_ChillerKeywords.RATED_CHW_T: "44",
            BDL_ChillerKeywords.RATED_COND_T: "85",
            BDL_ChillerKeywords.DESIGN_CHW_T: "50",
            BDL_ChillerKeywords.DESIGN_COND_T: "70",
        }

        self.chiller.populate_data_elements()
        self.chiller.populate_data_group()

        expected_data_structure = {
            "id": "Chiller 1",
            "compressor_type": "CENTRIFUGAL",
            "energy_source_type": "ELECTRICITY",
            "cooling_loop": "Chilled Water Loop (Primary)",
            "condensing_loop": "Condenser Water Loop",
            "design_entering_condenser_temperature": 70.0,
            "design_leaving_evaporator_temperature": 50.0,
            "rated_entering_condenser_temperature": 85.0,
            "rated_leaving_evaporator_temperature": 44.0,
            "rated_capacity": 0.12009233593749999,
            "design_capacity": 0.151941078125,
            "design_flow_condenser": 36.10254669189453,
            "design_flow_evaporator": 28.88204002380371,
            "is_chilled_water_pump_interlocked": False,
            "is_condenser_water_pump_interlocked": False,
            "capacity_validation_points": [],
            "power_validation_points": [],
            "part_load_efficiency": [],
            "part_load_efficiency_metrics": [],
        }

        self.assertEqual(expected_data_structure, self.chiller.chiller_data_structure)


class TestEngineChillers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.rmd.file_path = os.path.abspath(
            os.path.join(script_dir, "../output_references/Engine Chiller")
        )
        self.chiller = Chiller("Chiller 1", self.rmd)

    def test_populate_data_elements_with_engine_chiller(self):
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.TYPE: BDL_ChillerTypes.ENGINE,
            BDL_ChillerKeywords.CHW_LOOP: "Chilled Water Loop (Primary)",
            BDL_ChillerKeywords.CW_LOOP: "Condenser Water Loop",
            BDL_ChillerKeywords.RATED_CHW_T: "44",
            BDL_ChillerKeywords.RATED_COND_T: "85",
            BDL_ChillerKeywords.DESIGN_CHW_T: "50",
            BDL_ChillerKeywords.DESIGN_COND_T: "70",
        }

        self.chiller.populate_data_elements()
        self.chiller.populate_data_group()

        expected_data_structure = {
            "id": "Chiller 1",
            "compressor_type": "SINGLE_EFFECT_DIRECT_FIRED_ABSORPTION",
            "cooling_loop": "Chilled Water Loop (Primary)",
            "condensing_loop": "Condenser Water Loop",
            "energy_source_type": "NATURAL_GAS",
            "design_entering_condenser_temperature": 70.0,
            "design_leaving_evaporator_temperature": 50.0,
            "rated_entering_condenser_temperature": 85.0,
            "rated_leaving_evaporator_temperature": 44.0,
            "design_capacity": 0.151941078125,
            "design_flow_condenser": 35.50693130493164,
            "design_flow_evaporator": 28.40554428100586,
            "is_chilled_water_pump_interlocked": False,
            "is_condenser_water_pump_interlocked": False,
            "capacity_validation_points": [],
            "power_validation_points": [],
            "part_load_efficiency": [],
            "part_load_efficiency_metrics": [],
        }

        self.assertEqual(expected_data_structure, self.chiller.chiller_data_structure)
