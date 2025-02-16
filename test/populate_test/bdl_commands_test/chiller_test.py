import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import (
    CirculationLoop,
    BDL_CirculationLoopKeywords,
)
from rpd_generator.bdl_structure.bdl_commands.chiller import (
    Chiller,
    BDL_ChillerTypes,
    BDL_CondenserTypes,
)
from rpd_generator.bdl_structure.bdl_commands.curve_fit import (
    CurveFit,
    BDL_CurveFitKeywords,
)
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ChillerKeywords = BDLEnums.bdl_enums["ChillerKeywords"]
EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]


class TestElectricChillers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.chilled_water_loop = CirculationLoop(
            "Chilled Water Loop (Primary)", self.rmd
        )
        self.chiller = Chiller("Chiller 1", self.rmd)
        self.f_t = CurveFit("fT Curve", self.rmd)
        self.f_plr = CurveFit("fPLR Curve", self.rmd)
        self.cap_f_t = CurveFit("CAP-fT Curve", self.rmd)

        self.chilled_water_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
        }
        self.f_t.keyword_value_pairs = {
            BDL_CurveFitKeywords.COEF: [
                "1.42868233",
                "-0.08227751",
                "0.00030243",
                "0.03622194",
                "-0.00029211",
                "0.00043788",
            ],
            BDL_CurveFitKeywords.TYPE: "BI-QUADRATIC-T",
            BDL_CurveFitKeywords.INPUT_TYPE: "COEFFICIENTS",
            BDL_CurveFitKeywords.OUTPUT_MIN: "-1000000.0000",
            BDL_CurveFitKeywords.OUTPUT_MAX: "1000000.0000",
        }

        self.f_plr.keyword_value_pairs = {
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
    def test_populate_data_with_centrif_chiller(self, mock_get_output_data):
        """Tests that all values populate with expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "Design Parameters - Capacity": 151941.078125,
            "Design Parameters - Condenser Flow": 36.10254669189453,
            "Design Parameters - Flow": 28.88204002380371,
            "Normalized (ARI) Capacity at Peak (Btu/hr)": 120092.3359375,
            "Normalized (ARI) Entering Condenser Water Temperature (°F)": 70.0,
            "Normalized (ARI) Leaving Chilled Water Temperature (°F)": 44.0,
            "Primary Equipment (Chillers) - Capacity (Btu/hr)": 120092.3359375,
        }
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.TYPE: BDL_ChillerTypes.ELEC_OPEN_CENT,
            BDL_ChillerKeywords.CONDENSER_TYPE: BDL_CondenserTypes.WATER_COOLED,
            BDL_ChillerKeywords.CHW_LOOP: "Chilled Water Loop (Primary)",
            BDL_ChillerKeywords.CW_LOOP: "Condenser Water Loop",
            BDL_ChillerKeywords.EIR_FT: "fT Curve",
            BDL_ChillerKeywords.EIR_FPLR: "fPLR Curve",
            BDL_ChillerKeywords.CAPACITY_FT: "CAP-fT Curve",
            BDL_ChillerKeywords.ELEC_INPUT_RATIO: "0.16",
            BDL_ChillerKeywords.MIN_RATIO: "0.25",
            BDL_ChillerKeywords.RATED_CHW_T: "44",
            BDL_ChillerKeywords.RATED_COND_T: "85",
            BDL_ChillerKeywords.DESIGN_CHW_T: "50",
            BDL_ChillerKeywords.DESIGN_COND_T: "70",
        }

        self.rmd.populate_rmd_data(testing=True)
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
            "minimum_load_ratio": 0.25,
            "rated_capacity": 0.11449739478507026,
            "design_capacity": 0.151941078125,
            "design_flow_condenser": 36.10254669189453,
            "design_flow_evaporator": 28.88204002380371,
            "is_chilled_water_pump_interlocked": False,
            "is_condenser_water_pump_interlocked": False,
            "capacity_validation_points": [],
            "power_validation_points": [],
            "efficiency_metric_types": [
                "FULL_LOAD_EFFICIENCY_RATED",
                "INTEGRATED_PART_LOAD_VALUE",
            ],
            "efficiency_metric_values": [6.25, 10.801636635546025],
        }
        self.assertEqual(expected_data_structure, self.chiller.chiller_data_structure)


class TestEngineChillers(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.chilled_water_loop = CirculationLoop(
            "Chilled Water Loop (Primary)", self.rmd
        )
        self.chiller = Chiller("Chiller 1", self.rmd)
        self.f_t = CurveFit("fT Curve", self.rmd)
        self.f_plr = CurveFit("fPLR Curve", self.rmd)
        self.cap_f_t = CurveFit("CAP-fT Curve", self.rmd)

        self.chilled_water_loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.DESIGN_COOL_T: "50",
        }

        self.f_t.keyword_value_pairs = {
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

        self.f_plr.keyword_value_pairs = {
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
    def test_populate_data_with_engine_chiller(self, mock_get_output_data):
        """Tests the branch of logic associated with engine chillers to ensure the correct values are populated"""
        mock_get_output_data.return_value = {
            "Design Parameters - Capacity": 151941.078125,
            "Design Parameters - Condenser Flow": 35.50693130493164,
            "Design Parameters - Flow": 28.40554428100586,
            "Normalized (ARI) Capacity at Peak (Btu/hr)": 120092.3359375,
            "Normalized (ARI) Entering Condenser Water Temperature (°F)": 85.0,
            "Normalized (ARI) Leaving Chilled Water Temperature (°F)": 44.0,
            "Primary Equipment (Chillers) - Capacity (Btu/hr)": 113584.79986733246,
        }
        self.chiller.keyword_value_pairs = {
            BDL_ChillerKeywords.TYPE: BDL_ChillerTypes.ENGINE,
            BDL_ChillerKeywords.CONDENSER_TYPE: BDL_CondenserTypes.WATER_COOLED,
            BDL_ChillerKeywords.CHW_LOOP: "Chilled Water Loop (Primary)",
            BDL_ChillerKeywords.CW_LOOP: "Condenser Water Loop",
            BDL_ChillerKeywords.HIR_FT: "fT Curve",
            BDL_ChillerKeywords.HIR_FPLR: "fPLR Curve",
            BDL_ChillerKeywords.CAPACITY_FT: "CAP-fT Curve",
            BDL_ChillerKeywords.HEAT_INPUT_RATIO: "0.16",
            BDL_ChillerKeywords.MIN_RATIO: "0.25",
            BDL_ChillerKeywords.RATED_CHW_T: "44",
            BDL_ChillerKeywords.RATED_COND_T: "85",
            BDL_ChillerKeywords.DESIGN_CHW_T: "50",
            BDL_ChillerKeywords.DESIGN_COND_T: "70",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "Chiller 1",
            "compressor_type": "OTHER",
            "cooling_loop": "Chilled Water Loop (Primary)",
            "condensing_loop": "Condenser Water Loop",
            "energy_source_type": "NATURAL_GAS",
            "design_entering_condenser_temperature": 85.0,
            "design_leaving_evaporator_temperature": 50.0,
            "rated_entering_condenser_temperature": 85.0,
            "rated_leaving_evaporator_temperature": 44.0,
            "minimum_load_ratio": 0.25,
            "rated_capacity": 0.10742989267538551,
            "design_capacity": 0.151941078125,
            "design_flow_condenser": 35.50693130493164,
            "design_flow_evaporator": 28.40554428100586,
            "is_chilled_water_pump_interlocked": False,
            "is_condenser_water_pump_interlocked": False,
            "capacity_validation_points": [],
            "power_validation_points": [],
            "efficiency_metric_types": [
                "FULL_LOAD_EFFICIENCY_RATED",
                "INTEGRATED_PART_LOAD_VALUE",
            ],
            "efficiency_metric_values": [6.25, 8.009551132788362],
        }
        self.assertEqual(expected_data_structure, self.chiller.chiller_data_structure)
