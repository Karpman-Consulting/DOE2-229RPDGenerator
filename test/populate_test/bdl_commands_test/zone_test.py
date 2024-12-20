import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.system import System
from rpd_generator.bdl_structure.bdl_commands.zone import *


class TestZones(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = System("System 1", self.rmd)
        self.zone = Zone("Zone 1", self.system, self.rmd)

        # KEYWORDS / OUTPUT DATA KEYS FOR REFERENCE
        # self.zone.keyword_value_pairs = {
        #     BDL_ZoneKeywords.DESIGN_COOL_T: "",
        #     BDL_ZoneKeywords.COOL_TEMP_SCH: "",
        #     BDL_ZoneKeywords.DESIGN_HEAT_T: "",
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

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_terminal_system_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone served by a constant volume, single-zone system with CHW cooling, HW
        heating, and constant temperature control

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

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_on_sum_system_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone that is assigned to a SUM type system

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_exhaust_fan_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with an exhaust fan

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_induction_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with induction units and secondary airflow

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_doas_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone served by a system which is served by a dedicated outside air system

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_baseboard_data(self, mock_get_output_data):
        """
        Test populating data elements for a zone with baseboard supplemental heating

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv_prevented_by_occ_cfm(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation that is prevented by the minimum
        occupancy CFM

        """
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zone_with_dcv_prevented_by_min_oa_sch(self, mock_get_output_data):
        """
        Test populating data elements for a zone with demand control ventilation that is prevented by the minimum OA
        schedule(s)

        """
        pass
