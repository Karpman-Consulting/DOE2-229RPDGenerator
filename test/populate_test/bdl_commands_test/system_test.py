import unittest
from unittest.mock import patch

from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.system import System


class TestSystems(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.system = System("System 1", self.rmd)

        # KEYWORDS / OUTPUT DATA KEYS FOR REFERENCE
        # self.zone.keyword_value_pairs = {
        #     BDL_SystemKeywords.TYPE: "",
        #     BDL_SystemKeywords.HEAT_SOURCE: "",
        #     BDL_SystemKeywords.COOL_SOURCE: "",
        #     BDL_SystemKeywords.PREHEAT_SOURCE: "",
        #     BDL_SystemKeywords.OA_CONTROL: "",
        #     BDL_SystemKeywords.RECOVER_EXHAUST: "",
        #     BDL_SystemKeywords.RETURN_STATIC: "",
        #     BDL_SystemKeywords.RETURN_KW_FLOW: "",
        #     BDL_SystemKeywords.DDS_TYPE: "",
        #     BDL_SystemKeywords.RETURN_AIR_PATH: "",
        #     BDL_SystemKeywords.FAN_CONTROL: "",
        #     BDL_SystemKeywords.MIN_OA_METHOD: "",
        #     BDL_SystemKeywords.COOL_CONTROL: "",
        #     BDL_SystemKeywords.COOL_MIN_RESET_T: "",
        #     BDL_SystemKeywords.COOL_MAX_RESET_T: "",
        #     BDL_SystemKeywords.NIGHT_CYCLE_CTRL: "",
        #     BDL_SystemKeywords.HW_LOOP: "",
        #     BDL_SystemKeywords.CW_LOOP: "",
        #     BDL_SystemKeywords.HUMIDIFIER_TYPE: "",
        #     BDL_SystemKeywords.HEAT_SET_T: "",
        #     BDL_SystemKeywords.HP_SUPP_SOURCE: "",
        #     BDL_SystemKeywords.MAX_HP_SUPP_T: "",
        #     BDL_SystemKeywords.MIN_HP_T: "",
        #     BDL_SystemKeywords.SIZING_RATIO: "",
        #     BDL_SystemKeywords.HEAT_SIZING_RATI: "",
        #     BDL_SystemKeywords.HEATING_CAPACITY: "",
        #     BDL_SystemKeywords.CHW_LOOP: "",
        #     BDL_SystemKeywords.COOL_SIZING_RATI: "",
        #     BDL_SystemKeywords.COOLING_CAPACITY: "",
        #     BDL_SystemKeywords.COOL_SH_CAP: "",
        #     BDL_SystemKeywords.PREHEAT_CAPACITY: "",
        #     BDL_SystemKeywords.PREHEAT_T: "",
        #     BDL_SystemKeywords.PHW_LOOP: "",
        #     BDL_SystemKeywords.SUPPLY_FLOW: "",
        #     BDL_SystemKeywords.SUPPLY_STATIC: "",
        #     BDL_SystemKeywords.SUPPLY_MTR_EFF: "",
        #     BDL_SystemKeywords.SUPPLY_MECH_EFF: "",
        #     BDL_SystemKeywords.RETURN_FAN_LOC: "",
        #     BDL_SystemKeywords.RETURN_FLOW: "",
        #     BDL_SystemKeywords.RETURN_MTR_EFF: "",
        #     BDL_SystemKeywords.RETURN_MECH_EFF: "",
        #     BDL_SystemKeywords.HSUPPLY_FLOW: "",
        #     BDL_SystemKeywords.HSUPPLY_STATIC: "",
        #     BDL_SystemKeywords.HSUPPLY_MTR_EFF: "",
        #     BDL_SystemKeywords.HSUPPLY_MECH_EFF: "",
        #     BDL_SystemKeywords.ECONO_LIMIT_T: "",
        #     BDL_SystemKeywords.ECONO_LOCKOUT: "",
        #     BDL_SystemKeywords.ERV_RECOVER_TYPE: "",
        #     BDL_SystemKeywords.ERV_RUN_CTRL: "",
        #     BDL_SystemKeywords.ERV_TEMP_CTRL: "",
        #     BDL_SystemKeywords.ERV_SENSIBLE_EFF: "",
        #     BDL_SystemKeywords.ERV_LATENT_EFF: "",
        #     BDL_SystemKeywords.ERV_OA_FLOW: "",
        #     BDL_SystemKeywords.ERV_EXH_FLOW: "",
        #     BDL_SystemKeywords.FAN_SCHEDULE: "",
        #     BDL_SystemKeywords.INDOOR_FAN_MODE: "",
        #     BDL_SystemKeywords.DOA_SYSTEM: "",
        #     BDL_SystemKeywords.COOL_SET_T: "",
        #     BDL_SystemKeywords.HEAT_CONTROL: "",
        #     BDL_SystemKeywords.HEAT_MAX_RESET_T: "",
        #     BDL_SystemKeywords.MIN_FLOW_RATIO: "",
        #     BDL_SystemKeywords.HEAT_FUEL_METER: "",
        # }
        # mock_get_output_data.return_value = {
        # "Cooling Capacity": 0,
        # "Heating Capacity": 0,
        # "Outside Air Ratio": 0,
        # "Sensible Heat Ratio": 0,
        # "Supply Fan - Airflow": 0,
        # "Supply Fan - Power": 0,
        # "Supply Fan - Min Flow Ratio": 0,
        # "Return Fan - Airflow": 0,
        # "Return Fan - Power": 0,
        # "Heating Supply Fan - Airflow": 0,
        # "Heating Supply Fan - Power": 0,
        # "Design Cooling capacity": 0,
        # "Design Cooling SHR": 0,
        # "Rated Cooling capacity": 0,
        # "Rated Cooling SHR": 0,
        # "Design Heating capacity": 0,
        # "Rated Heating capacity": 0,
        # "Design Preheat capacity": 0,
        # }

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_system_multizone_vav(self, mock_get_output_data):
        """Test populating a System data group from a multi-zone VAV system BDL command with zone-reset temperature controls, a return fan, propane furnace preheat system, CHW cooling system, integrated economizer, and ERV. Supply fan is sized based on design day with detailed spec method. System operates continuously during occupied hours and cycles during unoccupied hours."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_system_multizone_vav2(self, mock_get_output_data):
        """Test populating a System data group from a multi-zone VAV system BDL command with constant temperature controls, a relief fan, fuel-oil HW heating system, CHW cooling system, integrated economizer, and ERV. Supply fan is sized based on design day with detailed spec method. System operates continuously during occupied hours and cycles during unoccupied hours."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_zonal_system_with_multiple_zones(self, mock_get_output_data):
        """Test populating System data groups from a zonal system BDL command with zone-reset DX cooling, heat pump heating, non-integrated eceonomizer, and multiple zones assigned. Supply fans are not sized based on design day with simple spec method. System cycles during occupied and unoccupied hours."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system(self, mock_get_output_data):
        """Test populating System data groups from a DOAS system BDL command with continuous fan operation, DX cooling, hot water heating"""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_doas_system2(self, mock_get_output_data):
        """Test populating System data groups from a DOAS system BDL command where all_occupied_off criteria is met and fan operation populates as KEEP_OFF."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_dual_duct_system(self, mock_get_output_data):
        """Test populating System data groups from a dual duct system BDL command with heating/cooling supply fans, DX cooling, hot water heating, integrated economizer, and ERV. System operates continuously during occupied hours and stays off during unoccupied hours."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_sum_system(self):
        """Verify that no system data groups are populated when the system is a SUM system."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system1(self):
        """Verify that no system data groups are populated when the system meets is_terminal criteria."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_terminal_system2(self):
        """Verify that no system data groups are populated when the system meets alternate is_terminal criteria."""
        pass

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_fan_schedule_neg_999_error(self):
        """Verify that a VAVS system with a fan schedule with any value of -999 raises an error."""
        pass
