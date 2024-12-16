import unittest
from unittest.mock import patch

from rpd_generator.bdl_structure.bdl_commands.utility_and_economics import (
    FuelMeter,
    MasterMeters,
)
from rpd_generator.config import Config
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.bdl_structure.bdl_commands.domestic_water_heater import *
from rpd_generator.bdl_structure.bdl_commands.circulation_loop import (
    CirculationLoop,
    BDL_CirculationLoopKeywords,
    BDL_CirculationLoopTypes,
)


class TestDomesticWaterHeater(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.rmd = RulesetModelDescription("Test RMD")
        self.rmd.doe2_version = "DOE-2.3"
        self.rmd.doe2_data_path = Config.DOE23_DATA_PATH
        self.domestic_water_heater = DomesticWaterHeater("DWH 1", self.rmd)
        self.fuel_meter = FuelMeter("Fuel Meter 1", self.rmd)
        self.master_fuel_meter = FuelMeter("Master Fuel Meter", self.rmd)
        self.master_meters = MasterMeters("Master Meters", self.rmd)
        self.loop = CirculationLoop("Loop 1", self.rmd)

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater(self, mock_get_output_data):
        """Tests that domestic water heater outputs expected values, given valid inputs"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "NATURAL_GAS",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_non_natural_gas_fuel_meter(
        self, mock_get_output_data
    ):
        """Tests that fuel meter exists and is not fueled by natural gas, while water heater is fueled by natural gas"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.FUEL_OIL
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "FUEL_OIL",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_no_fuel_meter(
        self, mock_get_output_data
    ):
        """Tests that master meter is used when no fuel meter is provided"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.master_fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.LPG
        }
        self.master_meters.keyword_value_pairs = {
            BDL_MasterMeterKeywords.DHW_FUEL_METER: "Master Fuel Meter"
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "PROPANE",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_no_heat_elec_input_ratios(
        self, mock_get_output_data
    ):
        """Tests that thermal_efficiency is 1.0 when no HEAT_INPUT_RATIO and ELEC_INPUT_RATIO are provided"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "NATURAL_GAS",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 1.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_no_elec_input_ratio(
        self, mock_get_output_data
    ):
        """Tests that thermal_efficiency is correctly calculated when no ELEC_INPUT_RATIO is provided"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "NATURAL_GAS",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 2.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_no_heat_input_ratio(
        self, mock_get_output_data
    ):
        """Tests that thermal_efficiency is correctly calculated when no HEAT_INPUT_RATIO is provided"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.2",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "NATURAL_GAS",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 5.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_no_tank_stpt(
        self, mock_get_output_data
    ):
        """Tests that setpoint_temperature == loop design temperature when no AQUASTAT_SETPT_T is provided"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.NATURAL_GAS
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.GAS,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "NATURAL_GAS",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 65.0,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_electric_water_heater(
        self, mock_get_output_data
    ):
        """Tests that domestic water heater outputs expected values, given valid inputs and ELEC water heater"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.OTHER_FUEL
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.ELEC,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "CONVENTIONAL",
            "heater_fuel_type": "ELECTRICITY",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )

    @patch("rpd_generator.bdl_structure.base_node.BaseNode.get_output_data")
    def test_populate_data_with_domestic_water_heater_heat_pump(
        self, mock_get_output_data
    ):
        """Tests that domestic water heater outputs expected values, given valid inputs and HEAT_PUMP water heater"""
        mock_get_output_data.return_value = {
            "DW Heaters - Design Parameters - Capacity": -123456789
        }
        self.fuel_meter.keyword_value_pairs = {
            BDL_FuelMeterKeywords.TYPE: BDL_FuelTypes.OTHER_FUEL
        }
        self.loop.keyword_value_pairs = {
            BDL_CirculationLoopKeywords.TYPE: BDL_CirculationLoopTypes.HW,
            BDL_CirculationLoopKeywords.DESIGN_HEAT_T: "65",
        }
        self.domestic_water_heater.keyword_value_pairs = {
            BDL_DWHeaterKeywords.TYPE: BDL_DWHeaterTypes.HEAT_PUMP,
            BDL_DWHeaterKeywords.FUEL_METER: "Fuel Meter 1",
            BDL_DWHeaterKeywords.DHW_LOOP: "Loop 1",
            BDL_DWHeaterKeywords.AQUASTAT_SETPT_T: "70.2",
            BDL_DWHeaterKeywords.TANK_VOLUME: "250",
            BDL_DWHeaterKeywords.LOCATION: BDL_DWHeaterLocationOptions.OUTDOOR,
            BDL_DWHeaterKeywords.ZONE_NAME: "ZONE 1",
            BDL_DWHeaterKeywords.HEAT_INPUT_RATIO: "0.2",
            BDL_DWHeaterKeywords.ELEC_INPUT_RATIO: "0.5",
        }

        self.rmd.populate_rmd_data(testing=True)
        expected_data_structure = {
            "id": "DWH 1",
            "output_validation_points": [],
            "tank": {
                "id": "DWH 1 Tank",
                "storage_capacity": 250.0,
                "location": "OUTSIDE",
                "location_zone": "ZONE 1",
            },
            "solar_thermal_systems": [],
            "compressor_capacity_validation_points": [],
            "compressor_power_validation_points": [],
            "heater_type": "HEAT_PUMP_PACKAGED",
            "compressor_location": "OUTSIDE",
            "compressor_zone": "ZONE 1",
            "compressor_heat_rejection_source": "OTHER",
            "notes": 'At the time of development, heat pump water heaters within a zone are not fully supported by eQUEST. The compressor heat rejection source is therefore populated as OTHER. According to help text Volume 2: Dictionary > HVAC Components > DW-HEATER > Energy Consumption: "Partially implemented; the program will use the zone temperature when calculating the tank losses or the performance of a HEAT-PUMP water heater, however these interactions do not have any effect on the zone temperature."',
            "heater_fuel_type": "ELECTRICITY",
            "distribution_system": "Loop 1",
            "rated_capacity": 123.456789,
            "setpoint_temperature": 70.2,
            "thermal_efficiency": 10.0,
        }
        self.assertEqual(
            expected_data_structure, self.domestic_water_heater.data_structure
        )
