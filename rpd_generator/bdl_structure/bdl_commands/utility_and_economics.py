from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums
from rpd_generator.schema.schema_enums import SchemaEnums


EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_FuelMeterKeywords = BDLEnums.bdl_enums["FuelMeterKeywords"]
BDL_FuelTypes = BDLEnums.bdl_enums["FuelTypes"]
BDL_SteamAndCHWaterMeterKeywords = BDLEnums.bdl_enums[
    "SteamAndChilledWaterMeterKeywords"
]
CHILLED_WATER = "CHILLED_WATER"
HOT_WATER = "HOT_WATER"
OTHER = "OTHER"


class MasterMeters(BaseDefinition):

    bdl_command = BDL_Commands.MASTER_METERS

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

        self.rmd.master_meters = u_name

    def __repr__(self):
        return f"MasterMeters(u_name='{self.u_name}')"


class FuelMeter(BaseDefinition):

    bdl_command = BDL_Commands.FUEL_METER

    fuel_type_map = {
        BDL_FuelTypes.NATURAL_GAS: EnergySourceOptions.NATURAL_GAS,
        BDL_FuelTypes.LPG: EnergySourceOptions.PROPANE,
        BDL_FuelTypes.FUEL_OIL: EnergySourceOptions.FUEL_OIL,
        BDL_FuelTypes.DIESEL_OIL: EnergySourceOptions.OTHER,
        BDL_FuelTypes.COAL: EnergySourceOptions.OTHER,
        BDL_FuelTypes.METHANOL: EnergySourceOptions.OTHER,
        BDL_FuelTypes.OTHER_FUEL: EnergySourceOptions.OTHER,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.fuel_meter_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.fuel_type = None

    def __repr__(self):
        return f"FuelMeter(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for FuelMeter object."""
        fuel_meter_type = self.get_inp(BDL_FuelMeterKeywords.TYPE)
        self.fuel_type = self.fuel_type_map.get(fuel_meter_type)


class ElecMeter(BaseDefinition):

    bdl_command = BDL_Commands.ELEC_METER

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.electric_meter_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"ElecMeter(u_name='{self.u_name}')"


class UtilityRate(BaseDefinition):

    bdl_command = BDL_Commands.UTILITY_RATE

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.utility_rate_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"UtilityRate(u_name='{self.u_name}')"


class ElecGenerator(BaseDefinition):
    """ElecGenerator object in the tree."""

    bdl_command = BDL_Commands.ELEC_GENERATOR

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.elec_generator_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"ElecGenerator(u_name='{self.u_name}')"


class SteamMeter(BaseNode):
    """Steam Meter object in the tree."""

    bdl_command = BDL_Commands.STEAM_METER

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.steam_meter_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.data_structure = {}

        # data elements with no children
        self.loop = None
        self.type = HOT_WATER
        self.energy_source_type = OTHER

    def __repr__(self):
        return f"SteamMeter(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for ExternalFluidSource object."""
        self.loop = self.get_inp(BDL_SteamAndCHWaterMeterKeywords.CIRCULATION_LOOP)

    def populate_data_group(self):
        """Populate schema structure for ExternalFluidSource object."""
        self.data_structure = {
            "id": self.u_name,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "loop",
            "type",
            "energy_source_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        rmd.external_fluid_sources.append(self.data_structure)


class CHWMeter(BaseNode):
    """Chiled Water Meter object in the tree."""

    bdl_command = BDL_Commands.CHW_METER

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.chilled_water_meter_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.data_structure = {}

        # data elements with no children
        self.loop = None
        self.type = CHILLED_WATER
        self.energy_source_type = OTHER

    def __repr__(self):
        return f"CHWMeter(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for ExternalFluidSource object."""
        self.loop = self.get_inp(BDL_SteamAndCHWaterMeterKeywords.CIRCULATION_LOOP)

    def populate_data_group(self):
        """Populate schema structure for ExternalFluidSource object."""
        self.data_structure = {
            "id": self.u_name,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "loop",
            "type",
            "energy_source_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        rmd.external_fluid_sources.append(self.data_structure)
