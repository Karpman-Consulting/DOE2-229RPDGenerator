from rpd_generator.bdl_structure.parent_node import ParentNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
HeatingSystemOptions = SchemaEnums.schema_enums["HeatingSystemOptions"]
CoolingSystemOptions = SchemaEnums.schema_enums["CoolingSystemOptions"]
FanSystemSupplyFanControlOptions = SchemaEnums.schema_enums[
    "FanSystemSupplyFanControlOptions"
]
FanSystemOperationOptions = SchemaEnums.schema_enums["FanSystemOperationOptions"]
FanSystemTemperatureControlOptions = SchemaEnums.schema_enums[
    "FanSystemTemperatureControlOptions"
]
FanSpecificationMethodOptions = SchemaEnums.schema_enums[
    "FanSpecificationMethodOptions"
]
AirEconomizerOptions = SchemaEnums.schema_enums["AirEconomizerOptions"]
EnergyRecoveryOptions = SchemaEnums.schema_enums["EnergyRecoveryOptions"]
EnergyRecoveryOperationOptions = SchemaEnums.schema_enums[
    "EnergyRecoveryOperationOptions"
]
EnergyRecoverySupplyAirTemperatureControlOptions = SchemaEnums.schema_enums[
    "EnergyRecoverySupplyAirTemperatureControlOptions"
]
DemandControlVentilationControlOptions = SchemaEnums.schema_enums[
    "DemandControlVentilationControlOptions"
]
HumidificationOptions = SchemaEnums.schema_enums["HumidificationOptions"]
HeatpumpAuxiliaryHeatOptions = SchemaEnums.schema_enums["HeatpumpAuxiliaryHeatOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_SystemKeywords = BDLEnums.bdl_enums["SystemKeywords"]
BDL_ZoneKeywords = BDLEnums.bdl_enums["ZoneKeywords"]
BDL_MasterMeterKeywords = BDLEnums.bdl_enums["MasterMeterKeywords"]
BDL_SystemTypes = BDLEnums.bdl_enums["SystemTypes"]
BDL_SystemHeatingTypes = BDLEnums.bdl_enums["SystemHeatingTypes"]
BDL_SystemCoolingTypes = BDLEnums.bdl_enums["SystemCoolingTypes"]
BDL_CoolControlOptions = BDLEnums.bdl_enums["SystemCoolControlOptions"]
BDL_HeatControlOptions = BDLEnums.bdl_enums["SystemHeatControlOptions"]
BDL_SupplyFanTypes = BDLEnums.bdl_enums["SystemSupplyFanTypes"]
BDL_NightCycleControlOptions = BDLEnums.bdl_enums["SystemNightCycleControlOptions"]
BDL_EconomizerOptions = BDLEnums.bdl_enums["SystemEconomizerOptions"]
BDL_EnergyRecoveryTypes = BDLEnums.bdl_enums["SystemEnergyRecoveryTypes"]
BDL_EnergyRecoveryOptions = BDLEnums.bdl_enums["SystemEnergyRecoveryOptions"]
BDL_EnergyRecoveryOperationOptions = BDLEnums.bdl_enums[
    "SystemEnergyRecoveryOperationOptions"
]
BDL_EnergyRecoveryTemperatureControlOptions = BDLEnums.bdl_enums[
    "SystemEnergyRecoveryTemperatureControlOptions"
]
BDL_SystemMinimumOutdoorAirControlOptions = BDLEnums.bdl_enums[
    "SystemMinimumOutdoorAirControlOptions"
]
BDL_IndoorFanModeOptions = BDLEnums.bdl_enums["SystemIndoorFanModeOptions"]
BDL_HumidificationOptions = BDLEnums.bdl_enums["SystemHumidificationOptions"]
BDL_DualDuctFanOptions = BDLEnums.bdl_enums["SystemDualDuctFanOptions"]
BDL_ReturnFanOptions = BDLEnums.bdl_enums["SystemReturnFanLocationOptions"]
BDL_HPSupplementSourceOptions = BDLEnums.bdl_enums["HPSupplementSourceOptions"]
BDL_OutputCoolingTypes = BDLEnums.bdl_enums["OutputCoolingTypes"]
BDL_OutputHeatingTypes = BDLEnums.bdl_enums["OutputHeatingTypes"]
BDL_ReturnAirPathOptions = BDLEnums.bdl_enums["SystemReturnAirPathOptions"]


class System(ParentNode):
    """System object in the tree."""

    bdl_command = BDL_Commands.SYSTEM
    zonal_system_types = [
        BDL_SystemTypes.UHT,
        BDL_SystemTypes.UVT,
        BDL_SystemTypes.FC,
        BDL_SystemTypes.HP,
        BDL_SystemTypes.PTAC,
    ]
    reheat_system_types = [
        BDL_SystemTypes.PMZS,
        BDL_SystemTypes.PVAVS,
        BDL_SystemTypes.SZRH,
        BDL_SystemTypes.VAVS,
        BDL_SystemTypes.RHFS,
        BDL_SystemTypes.PIU,
        BDL_SystemTypes.IU,
        BDL_SystemTypes.CBVAV,
        BDL_SystemTypes.DOAS,
    ]
    heat_type_map = {
        BDL_SystemHeatingTypes.NONE: HeatingSystemOptions.NONE,
        BDL_SystemHeatingTypes.ELECTRIC: HeatingSystemOptions.ELECTRIC_RESISTANCE,
        BDL_SystemHeatingTypes.HOT_WATER: HeatingSystemOptions.FLUID_LOOP,
        BDL_SystemHeatingTypes.FURNACE: HeatingSystemOptions.FURNACE,
        BDL_SystemHeatingTypes.HEAT_PUMP: HeatingSystemOptions.HEAT_PUMP,
        BDL_SystemHeatingTypes.CONDENSING_UNIT: HeatingSystemOptions.HEAT_PUMP,
        BDL_SystemHeatingTypes.DHW_LOOP: HeatingSystemOptions.OTHER,
        BDL_SystemHeatingTypes.STEAM: HeatingSystemOptions.OTHER,
    }
    BDL_output_heat_type_map = {
        BDL_SystemHeatingTypes.HEAT_PUMP: BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED,
        BDL_SystemHeatingTypes.FURNACE: BDL_OutputHeatingTypes.FURNACE,
        BDL_SystemHeatingTypes.ELECTRIC: BDL_OutputHeatingTypes.ELECTRIC,
        BDL_SystemHeatingTypes.HOT_WATER: BDL_OutputHeatingTypes.HOT_WATER,
    }
    cool_type_map = {
        BDL_SystemCoolingTypes.ELEC_DX: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemCoolingTypes.CHILLED_WATER: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemCoolingTypes.NONE: CoolingSystemOptions.NONE,
    }
    BDL_output_cool_type_map = {
        BDL_SystemCoolingTypes.ELEC_DX: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemCoolingTypes.CHILLED_WATER: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemCoolingTypes.NONE: None,
    }
    supply_fan_map = {
        BDL_SupplyFanTypes.CONSTANT_VOLUME: FanSystemSupplyFanControlOptions.CONSTANT,
        BDL_SupplyFanTypes.SPEED: FanSystemSupplyFanControlOptions.VARIABLE_SPEED_DRIVE,
        #  "": FanSystemSupplyFanControlOptions.MULTISPEED",  no eQUEST options map to MULTISPEED in DOE2.3
        BDL_SupplyFanTypes.INLET: FanSystemSupplyFanControlOptions.INLET_VANE,
        BDL_SupplyFanTypes.DISCHARGE: FanSystemSupplyFanControlOptions.DISCHARGE_DAMPER,
        BDL_SupplyFanTypes.FAN_EIR_FPLR: FanSystemSupplyFanControlOptions.VARIABLE_SPEED_DRIVE,
    }
    unoccupied_fan_operation_map = {
        BDL_NightCycleControlOptions.CYCLE_ON_ANY: FanSystemOperationOptions.CYCLING,
        BDL_NightCycleControlOptions.CYCLE_ON_FIRST: FanSystemOperationOptions.CYCLING,
        BDL_NightCycleControlOptions.STAY_OFF: FanSystemOperationOptions.KEEP_OFF,
        BDL_NightCycleControlOptions.ZONE_FANS_ONLY: FanSystemOperationOptions.OTHER,
    }
    occupied_fan_operation_map = {
        BDL_IndoorFanModeOptions.CONTINUOUS: FanSystemOperationOptions.CONTINUOUS,
        BDL_IndoorFanModeOptions.INTERMITTENT: FanSystemOperationOptions.CYCLING,
    }
    temperature_control_map = {
        BDL_CoolControlOptions.CONSTANT: FanSystemTemperatureControlOptions.CONSTANT,
        BDL_CoolControlOptions.RESET: FanSystemTemperatureControlOptions.OUTDOOR_AIR_RESET,
        BDL_CoolControlOptions.WARMEST: FanSystemTemperatureControlOptions.ZONE_RESET,
        BDL_CoolControlOptions.COLDEST: FanSystemTemperatureControlOptions.ZONE_RESET,
        BDL_CoolControlOptions.SCHEDULED: FanSystemTemperatureControlOptions.SCHEDULED,
    }
    system_cooling_type_map = {
        BDL_SystemTypes.PTAC: CoolingSystemOptions.DIRECT_EXPANSION,  # Unavailable in DOE 2.3
        BDL_SystemTypes.PSZ: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemTypes.PMZS: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemTypes.PVAVS: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemTypes.PVVT: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemTypes.HP: CoolingSystemOptions.DIRECT_EXPANSION,
        # IS WATER LOOP HEAT PUMP CONSIDERED DIRECT_EXPANSION???
        BDL_SystemTypes.SZRH: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.VAVS: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.RHFS: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.DDS: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.MZS: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.PIU: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.FC: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.IU: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.UVT: CoolingSystemOptions.NONE,
        BDL_SystemTypes.UHT: CoolingSystemOptions.NONE,
        BDL_SystemTypes.RESYS2: CoolingSystemOptions.DIRECT_EXPANSION,
        BDL_SystemTypes.CBVAV: CoolingSystemOptions.FLUID_LOOP,
        BDL_SystemTypes.SUM: CoolingSystemOptions.NONE,
        BDL_SystemTypes.DOAS: None,  # Mapping updated in populate_data_elements method
    }
    BDL_output_system_heating_type_map = {
        BDL_SystemTypes.PTAC: None,  # Mapping updated in populate_data_elements method  # Unavailable in DOE 2.3
        BDL_SystemTypes.PSZ: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.PMZS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.PVAVS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.PVVT: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.HP: BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED,
        BDL_SystemTypes.SZRH: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.VAVS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.RHFS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.DDS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.MZS: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.PIU: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.FC: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.IU: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.UVT: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.UHT: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.RESYS2: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.CBVAV: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.SUM: None,
        BDL_SystemTypes.DOAS: None,  # Mapping updated in populate_data_elements method
    }
    BDL_output_system_cooling_type_map = {
        BDL_SystemTypes.PTAC: BDL_OutputCoolingTypes.DX_AIR_COOLED,  # Unavailable in DOE 2.3
        BDL_SystemTypes.PSZ: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemTypes.PMZS: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemTypes.PVAVS: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemTypes.PVVT: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemTypes.HP: BDL_OutputCoolingTypes.DX_WATER_COOLED,
        BDL_SystemTypes.SZRH: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.VAVS: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.RHFS: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.DDS: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.MZS: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.PIU: None,  # Mapping updated in populate_data_elements method
        BDL_SystemTypes.FC: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.IU: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.UVT: CoolingSystemOptions.NONE,
        BDL_SystemTypes.UHT: CoolingSystemOptions.NONE,
        BDL_SystemTypes.RESYS2: BDL_OutputCoolingTypes.DX_AIR_COOLED,
        BDL_SystemTypes.CBVAV: BDL_OutputCoolingTypes.CHILLED_WATER,
        BDL_SystemTypes.SUM: None,
        BDL_SystemTypes.DOAS: None,  # Mapping updated in populate_data_elements method
    }
    economizer_map = {
        BDL_EconomizerOptions.FIXED: AirEconomizerOptions.FIXED_FRACTION,
        BDL_EconomizerOptions.OA_TEMP: AirEconomizerOptions.TEMPERATURE,
        BDL_EconomizerOptions.OA_ENTHALPY: AirEconomizerOptions.ENTHALPY,
        BDL_EconomizerOptions.DUAL_TEMP: AirEconomizerOptions.DIFFERENTIAL_TEMPERATURE,
        BDL_EconomizerOptions.DUAL_ENTHALPY: AirEconomizerOptions.DIFFERENTIAL_ENTHALPY,
    }
    recovery_type_map = {
        BDL_EnergyRecoveryTypes.SENSIBLE_HX: EnergyRecoveryOptions.SENSIBLE_HEAT_EXCHANGE,
        BDL_EnergyRecoveryTypes.ENTHALPY_HX: EnergyRecoveryOptions.ENTHALPY_HEAT_EXCHANGE,
        BDL_EnergyRecoveryTypes.SENSIBLE_WHEEL: EnergyRecoveryOptions.SENSIBLE_HEAT_WHEEL,
        BDL_EnergyRecoveryTypes.ENTHALPY_WHEEL: EnergyRecoveryOptions.ENTHALPY_HEAT_WHEEL,
        BDL_EnergyRecoveryTypes.HEAT_PIPE: EnergyRecoveryOptions.HEAT_PIPE,
    }
    has_recovery_map = {
        BDL_EnergyRecoveryOptions.NO: EnergyRecoveryOperationOptions.NONE,
        BDL_EnergyRecoveryOptions.RELIEF_ONLY: None,  # Mapping updated in populate_air_energy_recovery method
        BDL_EnergyRecoveryOptions.EXHAUST_ONLY: None,  # Mapping updated in populate_air_energy_recovery method
        BDL_EnergyRecoveryOptions.RELIEF_EXHAUST: None,  # Mapping updated in populate_air_energy_recovery method
        BDL_EnergyRecoveryOptions.YES: None,  # Mapping updated in populate_air_energy_recovery method
    }
    er_operation_map = {
        BDL_EnergyRecoveryOperationOptions.WHEN_FANS_ON: EnergyRecoveryOperationOptions.WHEN_FANS_ON,
        BDL_EnergyRecoveryOperationOptions.WHEN_MIN_OA: EnergyRecoveryOperationOptions.WHEN_MINIMUM_OUTSIDE_AIR,
        BDL_EnergyRecoveryOperationOptions.ERV_SCHEDULE: EnergyRecoveryOperationOptions.SCHEDULED,
        BDL_EnergyRecoveryOperationOptions.OA_EXHAUST_DT: EnergyRecoveryOperationOptions.OTHER,
        BDL_EnergyRecoveryOperationOptions.OA_EXHAUST_DH: EnergyRecoveryOperationOptions.OTHER,
    }
    er_sat_control_map = {
        BDL_EnergyRecoveryTemperatureControlOptions.FLOAT: EnergyRecoverySupplyAirTemperatureControlOptions.OTHER,
        BDL_EnergyRecoveryTemperatureControlOptions.FIXED_SETPT: EnergyRecoverySupplyAirTemperatureControlOptions.FIXED_SETPOINT,
        BDL_EnergyRecoveryTemperatureControlOptions.MIXED_AIR_RESET: EnergyRecoverySupplyAirTemperatureControlOptions.MIXED_AIR_RESET,
    }
    dcv_map = {
        BDL_SystemMinimumOutdoorAirControlOptions.FRAC_OF_DESIGN_FLOW: DemandControlVentilationControlOptions.NONE,
        BDL_SystemMinimumOutdoorAirControlOptions.FRAC_OF_HOURLY_FLOW: DemandControlVentilationControlOptions.NONE,
        BDL_SystemMinimumOutdoorAirControlOptions.DCV_RETURN_SENSOR: DemandControlVentilationControlOptions.CO2_RETURN_AIR,
        BDL_SystemMinimumOutdoorAirControlOptions.DCV_ZONE_SENSORS: DemandControlVentilationControlOptions.CO2_ZONE,
    }
    humidification_map = {
        BDL_HumidificationOptions.NONE: HumidificationOptions.NONE,
        BDL_HumidificationOptions.ELECTRIC: HumidificationOptions.OTHER,
        BDL_HumidificationOptions.HOT_WATER: HumidificationOptions.OTHER,
        BDL_HumidificationOptions.STEAM: HumidificationOptions.OTHER,
        BDL_HumidificationOptions.FURNACE: HumidificationOptions.OTHER,
        BDL_HumidificationOptions.HEAT_PUMP: HumidificationOptions.OTHER,
        BDL_HumidificationOptions.DHW_LOOP: HumidificationOptions.OTHER,
    }
    heatpump_aux_type_map = {
        BDL_HPSupplementSourceOptions.ELECTRIC: HeatpumpAuxiliaryHeatOptions.ELECTRIC_RESISTANCE,
        BDL_HPSupplementSourceOptions.HOT_WATER: HeatpumpAuxiliaryHeatOptions.OTHER,
        BDL_HPSupplementSourceOptions.FURNACE: HeatpumpAuxiliaryHeatOptions.FURNACE,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        # On initialization the parent building segment is not known. It will be set in the GUI.
        self.parent_building_segment = self.get_obj("Default Building Segment")
        self.rmd.system_names.append(u_name)

        self.sys_id = None
        self.system_data_structure = {}

        self.omit = False
        self.is_terminal = False
        self.is_zonal_system = False
        self.is_derived_system = False
        self.output_cool_type = None
        self.output_heat_type = None

        # system data elements with children
        self.fan_system = {}
        self.heating_system = {}
        self.cooling_system = {}
        self.preheat_system = {}

        # fan system data elements
        self.fan_sys_id = None
        self.fan_sys_reporting_name = None
        self.fan_sys_notes = None
        self.fan_sys_supply_fans = []
        self.fan_sys_return_fans = []
        self.fan_sys_exhaust_fans = []
        self.fan_sys_relief_fans = []
        self.fan_sys_air_economizer = {}
        self.fan_sys_air_energy_recovery = {}
        self.fan_sys_temperature_control = None
        self.fan_sys_operation_during_occupied = None
        self.fan_sys_operation_during_unoccupied = None
        self.fan_sys_has_lockout_central_heat_during_unoccupied = None
        self.fan_sys_fan_control = None
        self.fan_sys_reset_differential_temperature = None
        self.fan_sys_supply_air_temperature_reset_load_fraction = None
        self.fan_sys_supply_air_temperature_reset_schedule = None
        self.fan_sys_fan_volume_reset_type = None
        self.fan_sys_fan_volume_reset_fraction = None
        self.fan_sys_operating_schedule = None
        self.fan_sys_minimum_airflow = None
        self.fan_sys_minimum_outdoor_airflow = None
        self.fan_sys_maximum_outdoor_airflow = None
        self.fan_sys_air_filter_merv_rating = None
        self.fan_sys_has_fully_ducted_return = None
        self.fan_sys_demand_control_ventilation_control = None

        # heating system data elements
        self.heat_sys_id = None
        self.heat_sys_reporting_name = None
        self.heat_sys_notes = None
        self.heat_sys_type = None
        self.heat_sys_energy_source_type = None
        self.heat_sys_hot_water_loop = None
        self.heat_sys_water_source_heat_pump_loop = None
        self.heat_sys_design_capacity = None
        self.heat_sys_rated_capacity = None
        self.heat_sys_oversizing_factor = None
        self.heat_sys_is_sized_based_on_design_day = None
        self.heat_sys_heating_coil_setpoint = None
        self.heat_sys_efficiency_metric_values = None
        self.heat_sys_efficiency_metric_types = None
        self.heat_sys_heatpump_auxiliary_heat_type = None
        self.heat_sys_heatpump_auxiliary_heat_high_shutoff_temperature = None
        self.heat_sys_heatpump_low_shutoff_temperature = None
        self.heat_sys_humidification_type = None

        # cooling system data elements
        self.cool_sys_id = None
        self.cool_sys_reporting_name = None
        self.cool_sys_notes = None
        self.cool_sys_type = None
        self.cool_sys_design_total_cool_capacity = None
        self.cool_sys_design_sensible_cool_capacity = None
        self.cool_sys_rated_total_cool_capacity = None
        self.cool_sys_rated_sensible_cool_capacity = None
        self.cool_sys_oversizing_factor = None
        self.cool_sys_is_sized_based_on_design_day = None
        self.cool_sys_chilled_water_loop = None
        self.cool_sys_condenser_water_loop = None
        self.cool_sys_efficiency_metric_values = []
        self.cool_sys_efficiency_metric_types = []
        self.cool_sys_dehumidification_type = None
        self.cool_sys_turndown_ratio = None

        # preheat system data elements
        self.preheat_sys_id = None
        self.preheat_sys_reporting_name = None
        self.preheat_sys_notes = None
        self.preheat_sys_type = None
        self.preheat_sys_energy_source_type = None
        self.preheat_sys_hot_water_loop = None
        self.preheat_sys_water_source_heat_pump_loop = None
        self.preheat_sys_design_capacity = None
        self.preheat_sys_rated_capacity = None
        self.preheat_sys_oversizing_factor = None
        self.preheat_sys_is_sized_based_on_design_day = None
        self.preheat_sys_heating_coil_setpoint = None
        self.preheat_sys_efficiency_metric_values = None
        self.preheat_sys_efficiency_metric_types = None
        self.preheat_sys_heatpump_auxiliary_heat_type = None
        self.preheat_sys_heatpump_auxiliary_heat_high_shutoff_temperature = None
        self.preheat_sys_heatpump_low_shutoff_temperature = None
        self.preheat_sys_humidification_type = None

        # Define the Fan data group instances from SYSTEM that are possible to model in DOE2
        # Return fan or Relief fan can be defined for a system, but not both
        self.cooling_supply_fan = {}
        self.return_fan = {}
        self.relief_fan = {}
        self.heating_supply_fan = {}

        # [cooling supply, return, relief, heating supply] fan data elements
        self.fan_id: list = [None, None, None, None]
        self.fan_reporting_name: list = [None, None, None, None]
        self.fan_notes: list = [None, None, None, None]
        self.fan_design_airflow: list = [None, None, None, None]
        self.fan_is_airflow_sized_based_on_design_day: list = [None, None, None, None]
        self.fan_specification_method: list = [None, None, None, None]
        self.fan_design_electric_power: list = [None, None, None, None]
        self.fan_design_pressure_rise: list = [None, None, None, None]
        self.fan_motor_nameplate_power: list = [None, None, None, None]
        self.fan_shaft_power: list = [None, None, None, None]
        self.fan_total_efficiency: list = [None, None, None, None]
        self.fan_motor_efficiency: list = [None, None, None, None]
        self.fan_motor_heat_to_airflow_fraction: list = [None, None, None, None]
        self.fan_motor_heat_to_zone_fraction: list = [None, None, None, None]
        self.fan_motor_location_zone: list = [None, None, None, None]
        self.fan_status_type: list = [None, None, None, None]
        self.fan_output_validation_points: list = [[], [], [], []]

        # air economizer data elements
        self.air_econ_id = None
        self.air_econ_reporting_name = None
        self.air_econ_notes = None
        self.air_econ_type = None
        self.air_econ_high_limit_shutoff_temperature = None
        self.air_econ_is_integrated = None

        # air energy recovery data elements
        self.air_energy_recovery_id = None
        self.air_energy_recovery_reporting_name = None
        self.air_energy_recovery_notes = None
        self.air_energy_recovery_type = None
        self.air_energy_recovery_enthalpy_recovery_ratio = None
        self.air_energy_recovery_energy_recovery_operation = None
        self.air_energy_recovery_energy_recovery_supply_air_temperature_control = None
        self.air_energy_recovery_design_sensible_effectiveness = None
        self.air_energy_recovery_design_latent_effectiveness = None
        self.air_energy_recovery_outdoor_airflow = None
        self.air_energy_recovery_exhaust_airflow = None

    def __repr__(self):
        return f"System(u_name='{self.u_name}')"

    def create_zonal_systems(self):
        """Create a new system for every zone assigned to this system, starting after the first zone.
        Use the current System object for the first zone assigned to the zonal system"""

        for zone in self.children[1:]:
            sys_id = f"{self.u_name} - {zone.u_name}"
            zone_system = System(self.u_name, self.rmd)
            zone_system.sys_id = sys_id
            zone_system.add_child(zone)
            zone.parent = zone_system
            zone_system.is_derived_system = True
            zone_system.keyword_value_pairs = self.keyword_value_pairs.copy()
            zone_system.populate_data_elements()
            self.rmd.bdl_obj_instances[sys_id] = zone_system
            self.children.remove(zone)

    def populate_data_elements(self):
        """Populate data elements from the keyword_value pairs returned from model_input_reader."""
        system_type = self.get_inp(BDL_SystemKeywords.TYPE)
        if system_type == BDL_SystemTypes.SUM:
            self.omit = True
            return
        if system_type in self.zonal_system_types:
            self.is_zonal_system = True
            if not self.is_derived_system:
                self.create_zonal_systems()

        cool_source = self.get_inp(BDL_SystemKeywords.COOL_SOURCE)
        cool_type = self.cool_type_map.get(cool_source)
        self.system_cooling_type_map.update(
            {
                BDL_SystemTypes.PIU: cool_type,
                BDL_SystemTypes.DOAS: cool_type,
            }
        )
        has_cool = self.system_cooling_type_map.get(
            self.get_inp(BDL_SystemKeywords.TYPE)
        ) not in [None, CoolingSystemOptions.NONE]
        has_preheat = self.get_inp(BDL_SystemKeywords.PREHEAT_SOURCE) and self.get_inp(
            BDL_SystemKeywords.PREHEAT_SOURCE
        ) not in [None, BDL_SystemHeatingTypes.NONE]
        heat_source = self.get_inp(BDL_SystemKeywords.HEAT_SOURCE)
        heat_type = self.heat_type_map.get(heat_source)
        has_heat = heat_type not in [None, HeatingSystemOptions.NONE]
        has_economizer = (
            self.get_inp(BDL_SystemKeywords.OA_CONTROL)
            and self.get_inp(BDL_SystemKeywords.OA_CONTROL)
            != BDL_EconomizerOptions.FIXED
        )
        has_energy_recovery = (
            self.get_inp(BDL_SystemKeywords.RECOVER_EXHAUST)
            and self.get_inp(BDL_SystemKeywords.RECOVER_EXHAUST)
            != BDL_EnergyRecoveryOptions.NO
        )

        self.is_terminal = (
            len(self.children) == 1
            and system_type not in self.reheat_system_types
            and heat_type
            in [
                HeatingSystemOptions.FLUID_LOOP,
                HeatingSystemOptions.NONE,
            ]
            and cool_type
            in [
                CoolingSystemOptions.FLUID_LOOP,
                CoolingSystemOptions.NONE,
            ]
            and not has_preheat
            and not has_economizer
            and not has_energy_recovery
        )
        if self.is_terminal:
            self.omit = True
            return

        output_heat_type = self.BDL_output_heat_type_map.get(heat_source)
        self.BDL_output_system_heating_type_map.update(
            {
                BDL_SystemTypes.PTAC: output_heat_type,
                BDL_SystemTypes.PSZ: output_heat_type,
                BDL_SystemTypes.PMZS: output_heat_type,
                BDL_SystemTypes.PVAVS: output_heat_type,
                BDL_SystemTypes.PVVT: output_heat_type,
                BDL_SystemTypes.SZRH: output_heat_type,
                BDL_SystemTypes.VAVS: output_heat_type,
                BDL_SystemTypes.RHFS: output_heat_type,
                BDL_SystemTypes.DDS: output_heat_type,
                BDL_SystemTypes.MZS: output_heat_type,
                BDL_SystemTypes.PIU: output_heat_type,
                BDL_SystemTypes.FC: output_heat_type,
                BDL_SystemTypes.IU: output_heat_type,
                BDL_SystemTypes.UVT: output_heat_type,
                BDL_SystemTypes.UHT: output_heat_type,
                BDL_SystemTypes.RESYS2: output_heat_type,
                BDL_SystemTypes.CBVAV: output_heat_type,
                BDL_SystemTypes.DOAS: output_heat_type,
            }
        )
        output_cool_type = self.BDL_output_cool_type_map.get(
            self.get_inp(BDL_SystemKeywords.TYPE)
        )
        self.BDL_output_system_cooling_type_map.update(
            {
                BDL_SystemTypes.PIU: output_cool_type,
                BDL_SystemTypes.DOAS: output_cool_type,
            }
        )
        self.output_heat_type = self.BDL_output_system_heating_type_map.get(
            self.get_inp(BDL_SystemKeywords.TYPE)
        )
        self.output_cool_type = self.BDL_output_system_cooling_type_map.get(
            self.get_inp(BDL_SystemKeywords.TYPE)
        )

        requests = self.get_output_requests()
        output_data = self.get_output_data(requests)
        for key in ["Cooling Capacity", "Heating Capacity"]:
            if key in output_data:
                output_data[key] = self.try_convert_units(
                    output_data[key], "kBtu/hr", "Btu/hr"
                )

        self.populate_fan_system(output_data)
        self.populate_fans(output_data)
        if has_cool:
            self.populate_cooling_system(output_data)
        if has_heat:
            self.populate_heating_system(output_data, heat_source)
        if has_preheat:
            self.populate_preheat_system(output_data)
        if has_economizer:
            self.populate_air_economizer()
        if has_energy_recovery:
            self.populate_air_energy_recovery()

    def get_output_requests(self):
        """Get the output requests for the system dependent on various system component types."""
        requests = {
            "Outside Air Ratio": (2201005, self.u_name, ""),
            "Cooling Capacity": (2201006, self.u_name, ""),
            "Sensible Heat Ratio": (2201007, self.u_name, ""),
            "Heating Capacity": (2201008, self.u_name, ""),
            "Supply Fan - Airflow": (2201012, self.u_name, ""),
            "Supply Fan - Power": (2201014, self.u_name, ""),
            "Supply Fan - Min Flow Ratio": (2201022, self.u_name, ""),
        }

        return_or_relief = self.get_inp(
            BDL_SystemKeywords.RETURN_STATIC
        ) or self.get_inp(BDL_SystemKeywords.RETURN_KW_FLOW)

        if return_or_relief:
            requests["Return Fan - Airflow"] = (
                2201023,
                self.u_name,
                "",
            )
            requests["Return Fan - Power"] = (
                2201025,
                self.u_name,
                "",
            )

        if self.get_inp(BDL_SystemKeywords.DDS_TYPE) == BDL_DualDuctFanOptions.DUAL_FAN:
            requests["Heating Supply Fan - Airflow"] = (
                2201034,
                self.u_name,
                "",
            )
            requests["Heating Supply Fan - Power"] = (2201036, self.u_name, "")

        if self.is_zonal_system:
            match self.output_cool_type:
                case BDL_OutputCoolingTypes.CHILLED_WATER:
                    # Design data for Cooling - chilled water - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203505,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Design data for Cooling - chilled water - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203506,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - chilled water - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203516,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - chilled water - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203517,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputCoolingTypes.DX_AIR_COOLED:
                    # Design data for Cooling - DX air cooled - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203557,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Design data for Cooling - DX air cooled - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203558,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - DX air cooled - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203566,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - DX air cooled - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203567,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputCoolingTypes.DX_WATER_COOLED:
                    # Design data for Cooling - DX water cooled - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203587,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Design data for Cooling - DX water cooled - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203588,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - DX water cooled - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203596,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - DX water cooled - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203597,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputCoolingTypes.VRF:
                    # Design data for Cooling - VRF - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203619,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Design data for Cooling - VRF - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203620,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - VRF - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203628,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Cooling - VRF - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203629,
                        self.u_name,
                        self.children[0].u_name,
                    )

            match self.output_heat_type:
                case BDL_OutputHeatingTypes.FURNACE:
                    # Design data for Heating - furnace - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203708,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_AIR_COOLED:
                    # Design data for Heating - heat pump air cooled - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203784,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Heating - heat pump air cooled - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203790,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED:
                    # Design data for Heating - heat pump water cooled - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203805,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Heating - heat pump water cooled - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203811,
                        self.u_name,
                        self.children[0].u_name,
                    )
                case BDL_OutputHeatingTypes.VRF:
                    # Design data for Heating - VRF - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203828,
                        self.u_name,
                        self.children[0].u_name,
                    )
                    # Rated data for Heating - VRF - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203834,
                        self.u_name,
                        self.children[0].u_name,
                    )

        else:
            match self.output_cool_type:
                case BDL_OutputCoolingTypes.CHILLED_WATER:
                    # Design data for Cooling - chilled water - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (2203015, self.u_name, "")
                    # Design data for Cooling - chilled water - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203016, self.u_name, "")
                    # Rated data for Cooling - chilled water - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (2203026, self.u_name, "")
                    # Rated data for Cooling - chilled water - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203027, self.u_name, "")
                case BDL_OutputCoolingTypes.DX_AIR_COOLED:
                    # Design data for Cooling - DX air cooled - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (2203083, self.u_name, "")
                    # Design data for Cooling - DX air cooled - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203084, self.u_name, "")
                    # Rated data for Cooling - DX air cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (2203092, self.u_name, "")
                    # Rated data for Cooling - DX air cooled - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203093, self.u_name, "")
                case BDL_OutputCoolingTypes.DX_WATER_COOLED:
                    # Design data for Cooling - DX water cooled - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (2203143, self.u_name, "")
                    # Design data for Cooling - DX water cooled - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203144, self.u_name, "")
                    # Rated data for Cooling - DX water cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (2203152, self.u_name, "")
                    # Rated data for Cooling - DX water cooled - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203153, self.u_name, "")
                case BDL_OutputCoolingTypes.VRF:
                    # Design data for Cooling - VRF - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (2203207, self.u_name, "")
                    # Design data for Cooling - VRF - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203208, self.u_name, "")
                    # Rated data for Cooling - VRF - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (2203216, self.u_name, "")
                    # Rated data for Cooling - VRF - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203217, self.u_name, "")

            match self.output_heat_type:
                case BDL_OutputHeatingTypes.FURNACE:
                    requests["Design Heating capacity"] = (2203296, self.u_name, "")
                case BDL_OutputHeatingTypes.HEAT_PUMP_AIR_COOLED:
                    # Design data for Heating - heat pump air cooled - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (2203372, self.u_name, "")
                    # Rated data for Heating - heat pump air cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (2203378, self.u_name, "")
                case BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED:
                    # Design data for Heating - heat pump water cooled - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (2203414, self.u_name, "")
                    # Rated data for Heating - heat pump water cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (2203420, self.u_name, "")
                case BDL_OutputHeatingTypes.VRF:
                    # Design data for Heating - VRF - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (2203460, self.u_name, "")
                    # Rated data for Heating - VRF - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (2203466, self.u_name, "")

            match self.preheat_sys_type:
                case HeatingSystemOptions.FLUID_LOOP:
                    pass  # placeholder
                case HeatingSystemOptions.ELECTRIC_RESISTANCE:
                    pass  # placeholder
                case HeatingSystemOptions.FURNACE:
                    # Design Preheat - furnace - SYSTEM - capacity, btu/hr
                    requests["Design Preheat capacity"] = (
                        2203311,
                        self.u_name,
                        "",
                    )

        return requests

    def populate_data_group(self):
        """
        Populate schema structure for system object.
        System configurations that typically are at the zone and include a compressor (such as packaged terminal air
        conditioning, packaged terminal heat pumps, window air conditioning units, and water loop heat pumps) should be
        reported in the schema using HeatingSystem and CoolingSystem. Systems that include gas or electric furnaces
        should be reported in the schema using HeatingSystem. System configurations that are at the zone and only
        include fans and coils (such as four-pipe fan coil, two-pipe fan coil, radiant systems, baseboards, and chilled
        beams) should be reported in the schema using Terminal with the chilled water and hot water systems described
        in the cooling_source and heating_source data elements (and any other relevant Terminal Data elements).
        Evaporative cooling systems should be described in CoolingSystem. Passive diffusers with no coil or fan should
        be described in Terminal. One FanSystem for each HeatingVentilatingAirConditioningSystem so if a direct outdoor
        air system is used a second Zone Terminal should be specified with a separate
        HeatingVentilatingAirConditioningSystem.
        """
        if self.omit:
            return

        else:
            for attr in dir(self):
                value = getattr(self, attr, None)

                if value is None:
                    continue

                if attr.startswith("fan_sys_"):
                    self.fan_system[attr.split("fan_sys_")[1]] = value

                elif attr.startswith("heat_sys_"):
                    self.heating_system[attr.split("heat_sys_")[1]] = value

                elif attr.startswith("cool_sys_"):
                    self.cooling_system[attr.split("cool_sys_")[1]] = value

                elif attr.startswith("preheat_sys_"):
                    self.preheat_system[attr.split("preheat_sys_")[1]] = value

                elif attr.startswith("fan_") and attr[4:7] != "sys":
                    key = attr.split("fan_")[1]  # Get the key by removing 'fan_' prefix
                    for i, fan_dict_name in enumerate(
                        [
                            "cooling_supply_fan",
                            "return_fan",
                            "relief_fan",
                            "heating_supply_fan",
                        ]
                    ):
                        # Check if there is a non-None value for the current fan type
                        if getattr(self, "fan_id")[i] is not None:
                            fan_dict = getattr(self, fan_dict_name)
                            if getattr(self, attr)[i] is not None:
                                fan_dict[key] = getattr(self, attr)[i]
                            # update the fan dictionary
                            setattr(self, fan_dict_name, fan_dict)

                elif attr.startswith("air_econ_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.fan_sys_air_economizer[attr.split("air_econ_")[1]] = value

                elif attr.startswith("air_energy_recovery_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.fan_sys_air_energy_recovery[
                            attr.split("air_energy_recovery_")[1]
                        ] = value

            for fan_dict_name in [
                "cooling_supply_fan",
                "return_fan",
                "relief_fan",
                "heating_supply_fan",
            ]:
                fan_dict = getattr(self, fan_dict_name)
                # append to FanSystem
                if fan_dict and fan_dict_name in [
                    "cooling_supply_fan",
                    "heating_supply_fan",
                ]:
                    self.fan_sys_supply_fans.append(fan_dict)
                elif fan_dict and fan_dict_name == "return_fan":
                    self.fan_sys_return_fans.append(fan_dict)
                elif fan_dict and fan_dict_name == "relief_fan":
                    self.fan_sys_relief_fans.append(fan_dict)

            if self.is_derived_system:
                self.system_data_structure["id"] = self.sys_id
            else:
                self.system_data_structure["id"] = self.u_name
            self.system_data_structure.update(
                {
                    "fan_system": self.fan_system,
                    "heating_system": self.heating_system,
                    "cooling_system": self.cooling_system,
                    "preheat_system": self.preheat_system,
                }
            )

    def insert_to_rpd(self, rmd):
        """Insert system data structure into the rpd data structure."""
        if self.omit:
            return
        self.parent_building_segment.hvac_systems.append(self.system_data_structure)

    def populate_fan_system(self, output_data):
        self.fan_sys_id = self.u_name + " FanSys"
        self.fan_sys_has_fully_ducted_return = (
            self.get_inp(BDL_SystemKeywords.RETURN_AIR_PATH)
            == BDL_ReturnAirPathOptions.DUCT
        )
        self.fan_sys_fan_control = self.supply_fan_map.get(
            self.get_inp(BDL_SystemKeywords.FAN_CONTROL)
        )
        self.fan_sys_temperature_control = self.get_temperature_control()
        self.fan_sys_operation_during_unoccupied = (
            self.unoccupied_fan_operation_map.get(
                self.get_inp(BDL_SystemKeywords.NIGHT_CYCLE_CTRL)
            )
        )
        self.fan_sys_demand_control_ventilation_control = self.dcv_map.get(
            self.get_inp(BDL_SystemKeywords.MIN_OA_METHOD)
        )
        cool_control = self.get_inp(BDL_SystemKeywords.COOL_CONTROL)
        min_reset_t = self.get_inp(BDL_SystemKeywords.COOL_MIN_RESET_T)
        max_reset_t = self.get_inp(BDL_SystemKeywords.COOL_MAX_RESET_T)
        if (
            cool_control == BDL_CoolControlOptions.WARMEST
            and min_reset_t
            and max_reset_t
        ):
            self.fan_sys_reset_differential_temperature = self.try_float(
                max_reset_t
            ) - self.try_float(min_reset_t)
        supply_fan_airflow = output_data.get("Supply Fan - Airflow")
        supply_fan_min_ratio = output_data.get("Supply Fan - Min Flow Ratio")
        oa_ratio = output_data.get("Outside Air Ratio")
        if oa_ratio and supply_fan_airflow:
            self.fan_sys_minimum_outdoor_airflow = self.try_float(
                oa_ratio
            ) * self.try_float(supply_fan_airflow)
        if supply_fan_min_ratio and supply_fan_airflow:
            self.fan_sys_minimum_airflow = self.try_float(
                supply_fan_min_ratio
            ) * self.try_float(supply_fan_airflow)
        self.fan_sys_operation_during_unoccupied = (
            self.unoccupied_fan_operation_map.get(
                self.get_inp(BDL_SystemKeywords.NIGHT_CYCLE_CTRL)
            )
        )
        self.fan_sys_operation_during_occupied = (
            self.populate_fan_operation_during_occupied()
        )

    def populate_heating_system(self, output_data, heat_source):
        self.heat_sys_id = self.u_name + " HeatSys"
        self.heat_sys_type = self.heat_type_map.get(heat_source)
        self.heat_sys_hot_water_loop = self.get_inp(BDL_SystemKeywords.HW_LOOP)
        self.heat_sys_water_source_heat_pump_loop = self.get_inp(
            BDL_SystemKeywords.CW_LOOP
        )
        self.heat_sys_humidification_type = self.humidification_map.get(
            self.get_inp(BDL_SystemKeywords.HUMIDIFIER_TYPE)
        )
        self.heat_sys_heating_coil_setpoint = self.try_float(
            self.get_inp(BDL_SystemKeywords.HEAT_SET_T)
        )
        self.heat_sys_heatpump_auxiliary_heat_type = self.heatpump_aux_type_map.get(
            self.get_inp(BDL_SystemKeywords.HP_SUPP_SOURCE)
        )
        self.heat_sys_heatpump_auxiliary_heat_high_shutoff_temperature = self.try_float(
            self.get_inp(BDL_SystemKeywords.MAX_HP_SUPP_T)
        )
        self.heat_sys_heatpump_low_shutoff_temperature = self.try_float(
            self.get_inp(BDL_SystemKeywords.MIN_HP_T)
        )

        sizing_ratio = self.try_float(self.get_inp(BDL_SystemKeywords.SIZING_RATIO))
        heat_sizing_ratio = self.try_float(
            self.get_inp(BDL_SystemKeywords.HEAT_SIZING_RATI)
        )
        if sizing_ratio is not None and heat_sizing_ratio is not None:
            self.heat_sys_oversizing_factor = max(
                0, sizing_ratio * heat_sizing_ratio - 1
            )

        self.heat_sys_rated_capacity = self.try_abs(
            self.try_float(self.get_inp(BDL_SystemKeywords.HEATING_CAPACITY))
        )
        if not self.heat_sys_rated_capacity:
            self.heat_sys_rated_capacity = self.try_abs(
                output_data.get("Rated Heating capacity")
            )
        if not self.heat_sys_rated_capacity:
            self.heat_sys_rated_capacity = self.try_abs(
                output_data.get("Heating Capacity")
            )
        self.heat_sys_design_capacity = self.try_abs(
            output_data.get("Design Heating capacity")
        )
        if not self.heat_sys_design_capacity:
            self.heat_sys_design_capacity = self.try_abs(
                output_data.get("Heating Capacity")
            )

        if self.is_zonal_system:
            self.heat_sys_is_sized_based_on_design_day = (
                not self.get_inp(BDL_SystemKeywords.HEATING_CAPACITY)
                and not self.children[0].get_inp(BDL_ZoneKeywords.MAX_HEAT_RATE)
                and not self.children[0].get_inp(BDL_ZoneKeywords.HEATING_CAPACITY)
            )
        else:
            self.heat_sys_is_sized_based_on_design_day = not self.get_inp(
                BDL_SystemKeywords.HEATING_CAPACITY
            )

        if self.heat_sys_type in [
            HeatingSystemOptions.FLUID_LOOP,
            HeatingSystemOptions.OTHER,
        ]:
            loop_name = self.get_inp(BDL_SystemKeywords.HW_LOOP)
            loop = self.get_obj(loop_name)
            if loop:
                self.heat_sys_energy_source_type = self.get_loop_energy_source(loop)
        elif self.heat_sys_type in [
            HeatingSystemOptions.ELECTRIC_RESISTANCE,
            HeatingSystemOptions.HEAT_PUMP,
        ]:
            self.heat_sys_energy_source_type = EnergySourceOptions.ELECTRICITY
        elif self.heat_sys_type == HeatingSystemOptions.FURNACE:
            self.heat_sys_energy_source_type = self.get_furnace_energy_source()
        elif self.heat_sys_type == HeatingSystemOptions.NONE:
            self.heat_sys_energy_source_type = EnergySourceOptions.NONE

    def populate_cooling_system(self, output_data):
        self.cool_sys_id = self.u_name + " CoolSys"
        self.cool_sys_type = self.system_cooling_type_map.get(
            self.get_inp(BDL_SystemKeywords.TYPE)
        )
        self.cool_sys_chilled_water_loop = self.get_inp(BDL_SystemKeywords.CHW_LOOP)
        self.cool_sys_condenser_water_loop = self.get_inp(BDL_SystemKeywords.CW_LOOP)
        sizing_ratio = self.try_float(self.get_inp(BDL_SystemKeywords.SIZING_RATIO))
        cool_sizing_ratio = self.try_float(
            self.get_inp(BDL_SystemKeywords.COOL_SIZING_RATI)
        )
        if sizing_ratio is not None and cool_sizing_ratio is not None:
            self.cool_sys_oversizing_factor = max(
                0, sizing_ratio * cool_sizing_ratio - 1
            )
        self.cool_sys_rated_total_cool_capacity = self.try_abs(
            self.try_float(self.get_inp(BDL_SystemKeywords.COOLING_CAPACITY))
        )
        if not self.cool_sys_rated_total_cool_capacity:
            self.cool_sys_rated_total_cool_capacity = self.try_abs(
                output_data.get("Rated Cooling capacity")
            )
        if not self.cool_sys_rated_total_cool_capacity:
            self.cool_sys_rated_total_cool_capacity = self.try_abs(
                output_data.get("Cooling Capacity")
            )
        self.cool_sys_rated_sensible_cool_capacity = self.try_abs(
            self.try_float(self.get_inp(BDL_SystemKeywords.COOL_SH_CAP))
        )
        if not self.cool_sys_rated_sensible_cool_capacity:
            rated_shr = self.try_abs(output_data.get("Rated Cooling SHR"))
            if rated_shr and self.cool_sys_rated_total_cool_capacity and rated_shr != 1:
                self.cool_sys_rated_sensible_cool_capacity = (
                    rated_shr * self.cool_sys_rated_total_cool_capacity
                )
        if not self.cool_sys_rated_sensible_cool_capacity:
            shr = self.try_abs(output_data.get("Sensible Heat Ratio"))
            if shr and self.cool_sys_rated_total_cool_capacity:
                self.cool_sys_rated_sensible_cool_capacity = (
                    shr * self.cool_sys_rated_total_cool_capacity
                )
        self.cool_sys_design_total_cool_capacity = self.try_abs(
            output_data.get("Design Cooling capacity")
        )
        if not self.cool_sys_design_total_cool_capacity:
            self.cool_sys_design_total_cool_capacity = self.try_abs(
                output_data.get("Cooling Capacity")
            )
        design_shr = self.try_abs(output_data.get("Design Cooling SHR"))
        if design_shr and self.cool_sys_design_total_cool_capacity and design_shr != 1:
            self.cool_sys_design_sensible_cool_capacity = (
                design_shr * self.cool_sys_design_total_cool_capacity
            )
        if not self.cool_sys_design_sensible_cool_capacity:
            shr = self.try_abs(output_data.get("Sensible Heat Ratio"))
            if shr and self.cool_sys_design_total_cool_capacity:
                self.cool_sys_design_sensible_cool_capacity = (
                    shr * self.cool_sys_design_total_cool_capacity
                )
        if self.is_zonal_system:
            self.cool_sys_is_sized_based_on_design_day = (
                not self.get_inp(BDL_SystemKeywords.COOLING_CAPACITY)
                and not self.children[0].get_inp(BDL_ZoneKeywords.MAX_COOL_RATE)
                and not self.children[0].get_inp(BDL_ZoneKeywords.COOLING_CAPACITY)
            )
        else:
            self.cool_sys_is_sized_based_on_design_day = not self.get_inp(
                BDL_SystemKeywords.COOLING_CAPACITY
            )

    def populate_preheat_system(self, output_data):
        self.preheat_sys_id = self.u_name + " PreheatSys"
        self.preheat_sys_type = self.heat_type_map.get(
            self.get_inp(BDL_SystemKeywords.PREHEAT_SOURCE)
        )
        self.preheat_sys_rated_capacity = self.try_abs(
            self.try_float(self.get_inp(BDL_SystemKeywords.PREHEAT_CAPACITY))
        )
        self.preheat_sys_design_capacity = self.try_abs(
            output_data.get("Design Preheat capacity")
        )
        self.preheat_sys_is_sized_based_on_design_day = not self.get_inp(
            BDL_SystemKeywords.PREHEAT_CAPACITY
        )
        self.preheat_sys_heating_coil_setpoint = self.try_float(
            self.get_inp(BDL_SystemKeywords.PREHEAT_T)
        )
        self.preheat_sys_hot_water_loop = self.get_inp(BDL_SystemKeywords.PHW_LOOP)
        if self.preheat_sys_type in [
            HeatingSystemOptions.FLUID_LOOP,
            HeatingSystemOptions.OTHER,
        ]:
            loop = self.get_obj(self.preheat_sys_hot_water_loop)
            if loop:
                self.preheat_sys_energy_source_type = self.get_loop_energy_source(loop)
        elif self.preheat_sys_type in [
            HeatingSystemOptions.ELECTRIC_RESISTANCE,
            HeatingSystemOptions.HEAT_PUMP,
        ]:
            self.preheat_sys_energy_source_type = EnergySourceOptions.ELECTRICITY
        elif self.preheat_sys_type == HeatingSystemOptions.FURNACE:
            self.preheat_sys_energy_source_type = self.get_furnace_energy_source()
        elif self.preheat_sys_type == HeatingSystemOptions.NONE:
            self.preheat_sys_energy_source_type = EnergySourceOptions.NONE

    def populate_fans(self, output_data):
        # There is always a supply fan for a fan system in eQUEST, so it is always populated
        self.fan_id[0] = self.u_name + " SupplyFan"
        self.fan_design_airflow[0] = output_data.get("Supply Fan - Airflow")
        self.fan_design_electric_power[0] = output_data.get("Supply Fan - Power")
        if self.get_inp(BDL_SystemKeywords.SUPPLY_FLOW) is not None:
            self.fan_is_airflow_sized_based_on_design_day[0] = False
        if self.fan_is_airflow_sized_based_on_design_day[0] is None:
            self.fan_is_airflow_sized_based_on_design_day[0] = (
                # If any zone served by the system has assigned flow rates, the fan is not sized based on design day
                not any(
                    child_zone.get_inp(BDL_ZoneKeywords.ASSIGNED_FLOW)
                    or child_zone.get_inp(BDL_ZoneKeywords.HASSIGNED_FLOW)
                    or child_zone.get_inp(BDL_ZoneKeywords.FLOW_AREA)
                    or child_zone.get_inp(BDL_ZoneKeywords.HFLOW_AREA)
                    or child_zone.get_inp(BDL_ZoneKeywords.AIR_CHANGES_HR)
                    or child_zone.get_inp(BDL_ZoneKeywords.HAIR_CHANGES_HR)
                    or child_zone.get_inp(BDL_ZoneKeywords.MIN_FLOW_AREA)
                    or child_zone.get_inp(BDL_ZoneKeywords.HMIN_FLOW_AREA)
                    for child_zone in self.children
                )
            )
        self.fan_specification_method[0] = (
            FanSpecificationMethodOptions.DETAILED
            if self.get_inp(BDL_SystemKeywords.SUPPLY_STATIC) is not None
            else FanSpecificationMethodOptions.SIMPLE
        )
        self.fan_design_pressure_rise[0] = self.try_float(
            self.get_inp(BDL_SystemKeywords.SUPPLY_STATIC)
        )
        self.fan_motor_efficiency[0] = self.try_float(
            self.get_inp(BDL_SystemKeywords.SUPPLY_MTR_EFF)
        )
        supply_mech_eff = self.try_float(
            self.get_inp(BDL_SystemKeywords.SUPPLY_MECH_EFF)
        )
        if self.fan_motor_efficiency[0] and supply_mech_eff:
            self.fan_total_efficiency[0] = (
                self.fan_motor_efficiency[0] * supply_mech_eff
            )
        # Determine if there is either a return or relief fan
        return_or_relief = (
            self.get_inp(BDL_SystemKeywords.RETURN_STATIC) is not None
            or self.get_inp(BDL_SystemKeywords.RETURN_KW_FLOW) is not None
        )
        # If there is a return or relief fan and its location is set to RELIEF
        if (
            return_or_relief
            and self.get_inp(BDL_SystemKeywords.RETURN_FAN_LOC)
            == BDL_ReturnFanOptions.RELIEF
        ):
            self.fan_id[2] = self.u_name + " ReliefFan"
            self.fan_design_airflow[2] = output_data.get("Return Fan - Airflow", None)
            self.fan_design_electric_power[2] = output_data.get(
                "Return Fan - Power", None
            )
            if self.get_inp(BDL_SystemKeywords.RETURN_FLOW) is not None:
                self.fan_is_airflow_sized_based_on_design_day[2] = False
            if self.fan_is_airflow_sized_based_on_design_day[2] is None:
                self.fan_is_airflow_sized_based_on_design_day[2] = (
                    self.fan_is_airflow_sized_based_on_design_day[0]
                )
            self.fan_specification_method[2] = (
                FanSpecificationMethodOptions.DETAILED
                if self.get_inp(BDL_SystemKeywords.RETURN_STATIC) is not None
                else FanSpecificationMethodOptions.SIMPLE
            )
            self.fan_design_pressure_rise[2] = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_STATIC)
            )
            self.fan_motor_efficiency[2] = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_MTR_EFF)
            )
            return_mech_eff = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_MECH_EFF)
            )
            if self.fan_motor_efficiency[2] and return_mech_eff:
                self.fan_total_efficiency[2] = (
                    self.fan_motor_efficiency[2] * return_mech_eff
                )

        # If the return or relief fan location is not set to RELIEF, it is categorized as a return fan
        elif return_or_relief:
            self.fan_id[1] = self.u_name + " ReturnFan"
            self.fan_design_airflow[1] = output_data.get("Return Fan - Airflow", None)
            self.fan_design_electric_power[1] = output_data.get("Return Fan - Power")
            if self.get_inp(BDL_SystemKeywords.RETURN_FLOW) is not None:
                self.fan_is_airflow_sized_based_on_design_day[1] = False
            if self.fan_is_airflow_sized_based_on_design_day[1] is None:
                self.fan_is_airflow_sized_based_on_design_day[1] = (
                    self.fan_is_airflow_sized_based_on_design_day[0]
                )

            self.fan_specification_method[1] = (
                FanSpecificationMethodOptions.DETAILED
                if self.get_inp(BDL_SystemKeywords.RETURN_STATIC) is not None
                else FanSpecificationMethodOptions.SIMPLE
            )
            self.fan_design_pressure_rise[1] = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_STATIC)
            )
            self.fan_motor_efficiency[1] = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_MTR_EFF)
            )
            return_mech_eff = self.try_float(
                self.get_inp(BDL_SystemKeywords.RETURN_MECH_EFF)
            )
            if self.fan_motor_efficiency[1] and return_mech_eff:
                self.fan_total_efficiency[1] = (
                    self.fan_motor_efficiency[1] * return_mech_eff
                )
        # If the system is a dual duct system and the dual duct fan option is dual fan, there is a heating supply fan
        if self.get_inp(BDL_SystemKeywords.DDS_TYPE) == BDL_DualDuctFanOptions.DUAL_FAN:
            self.fan_id[3] = self.u_name + " HeatingSupplyFan"
            self.fan_design_airflow[3] = output_data.get("Heating Supply Fan - Airflow")
            self.fan_design_electric_power[3] = output_data.get(
                "Heating Supply Fan - Power"
            )
            if self.get_inp(BDL_SystemKeywords.HSUPPLY_FLOW) is not None:
                self.fan_is_airflow_sized_based_on_design_day[3] = False
            if self.fan_is_airflow_sized_based_on_design_day[3] is None:
                self.fan_is_airflow_sized_based_on_design_day[3] = (
                    # If any zone served by the system has assigned flow rates, the fan is not sized based on design day
                    any(
                        child_zone.get_inp(BDL_ZoneKeywords.HASSIGNED_FLOW)
                        or child_zone.get_inp(BDL_ZoneKeywords.HFLOW_AREA)
                        or child_zone.get_inp(BDL_ZoneKeywords.HAIR_CHANGES_HR)
                        or child_zone.get_inp(BDL_ZoneKeywords.HMIN_FLOW_AREA)
                        for child_zone in self.children
                    )
                )
            self.fan_specification_method[3] = (
                FanSpecificationMethodOptions.DETAILED
                if self.get_inp(BDL_SystemKeywords.HSUPPLY_STATIC) is not None
                else FanSpecificationMethodOptions.SIMPLE
            )
            self.fan_design_pressure_rise[3] = self.try_float(
                self.get_inp(BDL_SystemKeywords.HSUPPLY_STATIC)
            )

    def populate_air_economizer(self):
        self.air_econ_id = self.u_name + " AirEconomizer"
        self.air_econ_type = self.economizer_map.get(
            self.get_inp(BDL_SystemKeywords.OA_CONTROL)
        )
        self.air_econ_high_limit_shutoff_temperature = self.try_float(
            self.get_inp(BDL_SystemKeywords.ECONO_LIMIT_T)
        )
        self.air_econ_is_integrated = (
            True
            if self.get_inp(BDL_SystemKeywords.COOL_SOURCE)
            == BDL_SystemCoolingTypes.CHILLED_WATER
            else not self.boolean_map.get(
                self.get_inp(BDL_SystemKeywords.ECONO_LOCKOUT)
            )
        )

    def populate_air_energy_recovery(self):
        self.air_energy_recovery_id = self.u_name + " AirEnergyRecovery"
        recover_exhaust = self.get_inp(BDL_SystemKeywords.RECOVER_EXHAUST)
        recovery_type = self.recovery_type_map.get(
            self.get_inp(BDL_SystemKeywords.ERV_RECOVER_TYPE)
        )
        self.has_recovery_map.update(
            {
                BDL_EnergyRecoveryOptions.RELIEF_ONLY: recovery_type,
                BDL_EnergyRecoveryOptions.EXHAUST_ONLY: recovery_type,
                BDL_EnergyRecoveryOptions.RELIEF_EXHAUST: recovery_type,
                BDL_EnergyRecoveryOptions.YES: recovery_type,
            }
        )
        self.air_energy_recovery_type = self.has_recovery_map.get(recover_exhaust)
        self.air_energy_recovery_energy_recovery_operation = self.er_operation_map.get(
            self.get_inp(BDL_SystemKeywords.ERV_RUN_CTRL)
        )
        self.air_energy_recovery_energy_recovery_supply_air_temperature_control = (
            self.er_sat_control_map.get(self.get_inp(BDL_SystemKeywords.ERV_TEMP_CTRL))
        )
        self.air_energy_recovery_design_sensible_effectiveness = self.try_float(
            self.get_inp(BDL_SystemKeywords.ERV_SENSIBLE_EFF)
        )
        self.air_energy_recovery_design_latent_effectiveness = self.try_float(
            self.get_inp(BDL_SystemKeywords.ERV_LATENT_EFF)
        )
        self.air_energy_recovery_outdoor_airflow = self.try_float(
            self.get_inp(BDL_SystemKeywords.ERV_OA_FLOW)
        )
        if self.air_energy_recovery_outdoor_airflow is None:
            self.air_energy_recovery_outdoor_airflow = (
                self.fan_sys_minimum_outdoor_airflow
            )
        self.air_energy_recovery_exhaust_airflow = self.try_float(
            self.get_inp(BDL_SystemKeywords.ERV_EXH_FLOW)
        )
        if self.air_energy_recovery_exhaust_airflow is None:
            self.air_energy_recovery_exhaust_airflow = (
                self.air_energy_recovery_outdoor_airflow
            )

    def populate_fan_operation_during_occupied(self):
        fan_sch = self.get_obj(self.get_inp(BDL_SystemKeywords.FAN_SCHEDULE))

        if self.get_inp(BDL_SystemKeywords.TYPE) == BDL_SystemTypes.RESVVT:
            return FanSystemOperationOptions.CYCLING

        elif self.get_inp(BDL_SystemKeywords.TYPE) == BDL_SystemTypes.DOAS:
            if not fan_sch:
                return FanSystemOperationOptions.CONTINUOUS
            elif all(value == -999 for value in fan_sch.hourly_values):
                return FanSystemOperationOptions.CONTINUOUS

            doas_occ_sch = self.get_doas_occ_sch()
            all_occupied_off = True
            all_occupied_on = True
            for i, hour in enumerate(doas_occ_sch):
                if hour == 1:
                    value = fan_sch.hourly_values[i]
                    if value not in [0, -1]:
                        all_occupied_off = False
                    if value not in [1, -999]:
                        all_occupied_on = False
            if all_occupied_off:
                return FanSystemOperationOptions.KEEP_OFF
            if all_occupied_on:
                return FanSystemOperationOptions.CONTINUOUS
            return FanSystemOperationOptions.OTHER

        elif self.get_inp(BDL_SystemKeywords.TYPE) in [
            BDL_SystemTypes.PTAC,
            BDL_SystemTypes.HP,
            BDL_SystemTypes.UVT,
            BDL_SystemTypes.UHT,
            BDL_SystemTypes.PSZ,
            BDL_SystemTypes.PVVT,
            BDL_SystemTypes.RESYS2,
            BDL_SystemTypes.EVAP_COOL,
            BDL_SystemTypes.FC,
            BDL_SystemTypes.SZRH,
            BDL_SystemTypes.HP,
        ]:
            if not fan_sch:
                return self.occupied_fan_operation_map.get(
                    self.get_inp(BDL_SystemKeywords.INDOOR_FAN_MODE)
                )

            has_one = False
            has_neg_999 = False
            is_all_0 = True
            for value in fan_sch.hourly_values:
                if is_all_0 and value != 0:
                    is_all_0 = False
                if value == 1:
                    has_one = True
                elif value == -999:
                    has_neg_999 = True

            # Handle special case where all fan schedule values are 0 so unoccupied/occupied cannot be distinguished
            if is_all_0:
                return self.unoccupied_fan_operation_map.get(
                    self.get_inp(BDL_SystemKeywords.NIGHT_CYCLE_CTRL)
                )

            mixed_operation = has_one and has_neg_999
            if mixed_operation:
                return FanSystemOperationOptions.OTHER
            if has_one:  # and not mixed_operation implied to reach here
                return FanSystemOperationOptions.CONTINUOUS
            if has_neg_999:  # and not mixed_operation implied to reach here
                return FanSystemOperationOptions.CYCLING

        else:
            # Handle special case where all fan schedule values are 0 so unoccupied/occupied cannot be distinguished
            if all(value == 0 for value in fan_sch.hourly_values):
                return self.unoccupied_fan_operation_map.get(
                    self.get_inp(BDL_SystemKeywords.NIGHT_CYCLE_CTRL)
                )

            if any(value == -999 for value in fan_sch.hourly_values):
                # TODO raise this error in a window of the GUI
                raise ValueError(
                    f"""Fan schedule {fan_sch.u_name} for system {self.u_name} is not allowed to have -999 values. These
                    flags are not accurately supported by DOE 2.3 (see help text Volume 2: Dictionary > HVAC Components 
                    > SYSTEM > Airside Control > Fan Availability)"""
                )

            return (
                FanSystemOperationOptions.CONTINUOUS
            )  # if there is no fan schedule or the fan schedule has 1s

    def get_doas_occ_sch(self):
        occupied_hours = [0] * 8760
        systems_served = [
            obj_inst
            for obj_inst in self.rmd.bdl_obj_instances
            if isinstance(obj_inst, System)
            and obj_inst.get_inp(BDL_SystemKeywords.DOA_SYSTEM) == self.u_name
        ]
        system_fan_schedules = {
            self.get_obj(system.get_inp(BDL_SystemKeywords.FAN_SCHEDULE))
            for system in systems_served
        }
        for system_fan_schedule in system_fan_schedules:
            occupied_hours = [
                1 if hour == 1 else occ_hour
                for occ_hour, hour in zip(
                    occupied_hours, system_fan_schedule.hourly_values
                )
            ]
        return occupied_hours

    def get_temperature_control(self):
        heat_control = self.get_inp(BDL_SystemKeywords.HEAT_CONTROL)
        cool_control = self.get_inp(BDL_SystemKeywords.COOL_CONTROL)

        if not heat_control:
            return self.temperature_control_map.get(cool_control)
        if not cool_control:
            return self.temperature_control_map.get(heat_control)
        if cool_control == heat_control:
            return self.temperature_control_map.get(cool_control)
        if (
            cool_control == BDL_CoolControlOptions.WARMEST
            and heat_control == BDL_HeatControlOptions.COLDEST
        ):
            return FanSystemTemperatureControlOptions.ZONE_RESET

    def get_loop_energy_source(self, loop):
        """Get the energy source type for the loop. Used to populate the energy_source_type."""
        energy_source_set = set()
        for boiler_name in self.rmd.boiler_names:
            boiler = self.get_obj(boiler_name)
            if boiler.loop == loop.u_name:
                energy_source_set.add(boiler.energy_source_type)

        for steam_meter_name in self.rmd.steam_meter_names:
            steam_meter = self.get_obj(steam_meter_name)
            if steam_meter.loop == loop.u_name:
                energy_source_set.add(steam_meter.energy_source_type)

        for chiller_name in self.rmd.chiller_names:
            chiller = self.get_obj(chiller_name)
            if chiller.heat_recovery_loop == loop.u_name:
                energy_source_set.add(EnergySourceOptions.ELECTRICITY)

        for domestic_water_heater_name in self.rmd.domestic_water_heater_names:
            domestic_water_heater = self.get_obj(domestic_water_heater_name)
            if domestic_water_heater.hot_water_loop == loop.u_name:
                energy_source_set.add(domestic_water_heater.heater_fuel_type)

        if len(energy_source_set) == 1:
            return energy_source_set.pop()
        else:
            return EnergySourceOptions.OTHER

    def get_furnace_energy_source(self):
        """Get the energy source type for the furnace. Used to populate the energy_source_type."""
        heat_fuel_meter = self.get_obj(self.get_inp(BDL_SystemKeywords.HEAT_FUEL_METER))
        if heat_fuel_meter:
            return heat_fuel_meter.fuel_type
        else:
            master_meters = self.get_obj(self.rmd.master_meters)
            if master_meters:
                heat_fuel_meter = self.get_obj(
                    master_meters.get_inp(BDL_MasterMeterKeywords.HEAT_FUEL_METER)
                )
                if heat_fuel_meter:
                    return heat_fuel_meter.fuel_type
