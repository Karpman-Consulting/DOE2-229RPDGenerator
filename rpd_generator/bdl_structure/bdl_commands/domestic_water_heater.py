from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
ComponentLocationOptions = SchemaEnums.schema_enums["ComponentLocationOptions"]
ServiceWaterHeaterOptions = SchemaEnums.schema_enums["ServiceWaterHeaterOptions"]
StatusOptions = SchemaEnums.schema_enums["StatusOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_DWHeaterKeywords = BDLEnums.bdl_enums["DomesticWaterHeaterKeywords"]
BDL_DWHeaterTypes = BDLEnums.bdl_enums["DomesticWaterHeaterTypes"]
BDL_DWHeaterLocationOptions = BDLEnums.bdl_enums["DomesticWaterHeaterLocationOptions"]
BDL_FuelTypes = BDLEnums.bdl_enums["FuelTypes"]
BDL_MasterMeterKeywords = BDLEnums.bdl_enums["MasterMeterKeywords"]
BDL_FuelMeterKeywords = BDLEnums.bdl_enums["FuelMeterKeywords"]


class DomesticWaterHeater(BaseNode):
    """DomesticWaterHeater object in the tree."""

    bdl_command = BDL_Commands.DW_HEATER

    heater_type_map = {
        BDL_DWHeaterTypes.GAS: ServiceWaterHeaterOptions.CONVENTIONAL,
        BDL_DWHeaterTypes.ELEC: ServiceWaterHeaterOptions.CONVENTIONAL,
        BDL_DWHeaterTypes.HEAT_PUMP: ServiceWaterHeaterOptions.HEAT_PUMP_PACKAGED,
    }

    location_map = {
        BDL_DWHeaterLocationOptions.OUTDOOR: ComponentLocationOptions.OUTSIDE,
        BDL_DWHeaterLocationOptions.ZONE: ComponentLocationOptions.IN_ZONE,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.domestic_water_heater_names.append(u_name)

        self.data_structure = {}

        # data elements with children
        self.output_validation_points = []
        self.compressor_capacity_validation_points = []
        self.compressor_power_validation_points = []
        self.tank = {}
        self.solar_thermal_systems = []

        # data elements with no children
        self.heater_fuel_type = None
        self.distribution_system = None
        self.energy_factor = None
        self.thermal_efficiency = None
        self.standby_loss_fraction = None
        self.uniform_energy_factor = None
        self.first_hour_rating = None
        self.input_power = None
        self.rated_capacity = None
        self.minimum_capacity = None
        self.recovery_efficiency = None
        self.setpoint_temperature = None
        self.compressor_location = None
        self.compressor_zone = None
        self.compressor_heat_rejection_source = None
        self.compressor_heat_rejection_zone = None
        self.draft_fan_power = None
        self.has_electrical_ignition = None
        self.heater_type = None
        self.status_type = None
        self.hot_water_loop = None

        # Tank data elements
        self.storage_capacity = None
        self.type = None
        self.height = None
        self.interior_insulation = None
        self.exterior_insulation = None
        self.location = None
        self.location_zone = None

    def __repr__(self):
        return f"DomesticWaterHeater(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for domestic water heater object."""
        requests = self.get_output_requests()
        output_data = self.get_output_data(requests)
        for key in ["DW Heaters - Design Parameters - Capacity"]:
            if key in output_data:
                output_data[key] = self.try_convert_units(
                    output_data[key], "Btu/hr", "MMbtu_h"
                )

        self.heater_type = self.heater_type_map.get(
            self.get_inp(BDL_DWHeaterKeywords.TYPE)
        )

        if self.get_inp(BDL_DWHeaterKeywords.TYPE) == BDL_DWHeaterTypes.ELEC:
            self.heater_fuel_type = EnergySourceOptions.ELECTRICITY

        else:
            fuel_meter_ref = self.get_inp(BDL_DWHeaterKeywords.FUEL_METER)
            fuel_meter = self.get_obj(fuel_meter_ref)

            # If the fuel meter is not found, then it must be a MasterMeter.
            if fuel_meter is None:
                master_meters = self.get_obj(self.rmd.master_meters)
                if master_meters:
                    dhw_fuel_meter_name = master_meters.get_inp(
                        BDL_MasterMeterKeywords.DHW_FUEL_METER
                    )
                    dhw_fuel_meter = self.get_obj(dhw_fuel_meter_name)
                    if dhw_fuel_meter:
                        self.heater_fuel_type = dhw_fuel_meter.fuel_type
            else:
                self.heater_fuel_type = fuel_meter.fuel_type

        self.distribution_system = self.get_inp(BDL_DWHeaterKeywords.DHW_LOOP)

        self.rated_capacity = self.try_abs(
            self.try_float(output_data.get("DW Heaters - Design Parameters - Capacity"))
        )

        loop = self.get_obj(self.distribution_system)
        loop_stpt = None
        if loop is not None:
            loop_stpt = loop.design_supply_temperature[1]
        tank_stpt = self.get_inp(BDL_DWHeaterKeywords.AQUASTAT_SETPT_T)
        if tank_stpt is not None and loop_stpt is not None:
            self.setpoint_temperature = max(loop_stpt, tank_stpt)
        elif tank_stpt is None:
            self.setpoint_temperature = loop_stpt

        self.storage_capacity = self.try_float(
            self.get_inp(BDL_DWHeaterKeywords.TANK_VOLUME)
        )

        self.location = self.location_map.get(
            self.get_inp(BDL_DWHeaterKeywords.LOCATION)
        )

        self.location_zone = self.get_inp(BDL_DWHeaterKeywords.ZONE_NAME)

    def get_output_requests(self):
        """Get the output requests for the domestic water heater object."""
        requests = {
            "DW Heaters - Design Parameters - Capacity": (2321003, self.u_name, ""),
            "DW Heaters - Design Parameters - Flow": (2321004, self.u_name, ""),
            "DW Heaters - Design Parameters - Electric Input Ratio": (
                2321005,
                self.u_name,
                "",
            ),
            "DW Heaters - Design Parameters - Fuel Input Ratio": (
                2321006,
                self.u_name,
                "",
            ),
            "DW Heaters - Design Parameters - Auxiliary Power": (
                2321007,
                self.u_name,
                "",
            ),
        }
        return requests

    def populate_data_group(self):
        """Populate schema structure for domestic water heater object."""

        self.data_structure.update(
            {
                "id": self.u_name,
                "output_validation_points": self.output_validation_points,
                "tank": self.tank,
                "solar_thermal_systems": self.solar_thermal_systems,
                "compressor_capacity_validation_points": self.compressor_capacity_validation_points,
                "compressor_power_validation_points": self.compressor_power_validation_points,
            }
        )

        if self.storage_capacity is not None and self.storage_capacity > 0:
            self.tank["id"] = self.u_name + " Tank"
            tank_data_elements = [
                "storage_capacity",
                "type",
                "height",
                "interior_insulation",
                "exterior_insulation",
                "location",
                "location_zone",
            ]

            for attr in tank_data_elements:
                value = getattr(self, attr, None)
                if value is not None:
                    self.tank[attr] = value

        no_children_attributes = [
            "reporting_name",
            "notes",
            "heater_fuel_type",
            "distribution_system",
            "energy_factor",
            "thermal_efficiency",
            "standby_loss_fraction",
            "uniform_energy_factor",
            "first_hour_rating",
            "input_power",
            "rated_capacity",
            "minimum_capacity",
            "recovery_efficiency",
            "setpoint_temperature",
            "compressor_location",
            "compressor_zone",
            "compressor_heat_rejection_source",
            "compressor_heat_rejection_zone",
            "draft_fan_power",
            "has_electrical_ignition",
            "heater_type",
            "status_type",
            "hot_water_loop",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert window object into the rpd data structure."""
        rmd.service_water_heating_equipment.append(self.data_structure)
