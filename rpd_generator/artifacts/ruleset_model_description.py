import copy

from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.base_node import Base

BDL_FuelMeterKeywords = BDLEnums.bdl_enums["FuelMeterKeywords"]
BDL_FuelTypes = BDLEnums.bdl_enums["FuelTypes"]
BDL_ElecGeneratorKeywords = BDLEnums.bdl_enums["ElecGeneratorKeywords"]
BDL_ElecGeneratorTypes = BDLEnums.bdl_enums["ElecGeneratorTypes"]
BDL_UtilityRateKeywords = BDLEnums.bdl_enums["UtilityRateKeywords"]
BDL_UtilityRateTypes = BDLEnums.bdl_enums["UtilityRateTypes"]
EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
EndUseOptions = SchemaEnums.schema_enums["EndUseOptions"]

fuel_type_map = {
    BDL_FuelTypes.ELECTRICITY: EnergySourceOptions.ELECTRICITY,
    BDL_FuelTypes.NATURAL_GAS: EnergySourceOptions.NATURAL_GAS,
    BDL_FuelTypes.LPG: EnergySourceOptions.PROPANE,
    BDL_FuelTypes.FUEL_OIL: EnergySourceOptions.FUEL_OIL,
    BDL_FuelTypes.DIESEL_OIL: EnergySourceOptions.OTHER,
    BDL_FuelTypes.COAL: EnergySourceOptions.OTHER,
    BDL_FuelTypes.METHANOL: EnergySourceOptions.OTHER,
    BDL_FuelTypes.OTHER_FUEL: EnergySourceOptions.OTHER,
    EnergySourceOptions.PURCHASED_HOT_WATER: EnergySourceOptions.PURCHASED_HOT_WATER,
    EnergySourceOptions.PURCHASED_CHILLED_WATER: EnergySourceOptions.PURCHASED_CHILLED_WATER,
    EnergySourceOptions.ON_SITE_RENEWABLES: EnergySourceOptions.ON_SITE_RENEWABLES,
}


class RulesetModelDescription(Base):
    """
    This class is used to represent the RulesetModelDescription object in the 229 schema. It also stores additional model-level data.
    """

    def __init__(self, obj_id):
        self.file_path = None
        self.doe2_version = None
        self.doe2_data_path = None

        # store BDL objects for the model associated with the RMD
        self.bdl_obj_instances = {}
        # store space names mapped to their zone objects for quick access
        self.space_map = {}

        self.rmd_data_structure = {}

        self.master_meters = None
        self.electric_meter_names = []
        self.fuel_meter_names = []
        self.steam_meter_names = []
        self.chilled_water_meter_names = []
        self.utility_rate_names = []
        self.elec_generator_names = []
        self.system_names = []
        self.zone_names = []
        self.circulation_loop_names = []
        self.boiler_names = []
        self.chiller_names = []
        self.domestic_water_heater_names = []
        self.heat_rejection_names = []
        self.ground_loop_hx_names = []
        self.pump_names = []
        self.equip_ctrl_names = []

        self.building_azimuth = None
        # False by default, will set to True if a FIXED-SHADE object is found
        self.has_site_shading = False

        # data elements with children
        self.transformers = []
        self.buildings = []
        self.schedules = []
        self.fluid_loops = []
        self.service_water_heating_distribution_systems = []
        self.service_water_heating_equipment = []
        self.pumps = []
        self.boilers = []
        self.chillers = []
        self.heat_rejections = []
        self.external_fluid_sources = []
        self.output = {}

        # data elements with no children
        self.obj_id = obj_id
        self.reporting_name = None
        self.notes = None
        self.type = None
        self.is_measured_infiltration_based_on_test = None

        # output data elements
        self.output_id = "Output2019ASHRAE901"
        self.output_reporting_name = None
        self.output_notes = None
        self.output_instance = {}
        self.output_performance_cost_index = None
        self.output_baseline_building_unregulated_energy_cost = None
        self.output_baseline_building_regulated_energy_cost = None
        self.output_baseline_building_performance_energy_cost = None
        self.output_total_area_weighted_building_performance_factor = None
        self.output_performance_cost_index_target = None
        self.output_total_proposed_building_energy_cost_including_renewable_energy = (
            None
        )
        self.output_total_proposed_building_energy_cost_excluding_renewable_energy = (
            None
        )
        self.output_percent_renewable_energy_savings = None

        # output instance data elements
        self.output_instance_id = f"{obj_id} Output"
        self.output_instance_reporting_name = None
        self.output_instance_notes = None
        self.output_instance_ruleset_model_type = None
        self.output_instance_rotation_angle = None
        self.output_instance_unmet_load_hours = None
        self.output_instance_unmet_load_hours_heating = None
        self.output_instance_unmet_occupied_load_hours_heating = None
        self.output_instance_unmet_load_hours_cooling = None
        self.output_instance_unmet_occupied_load_hours_cooling = None
        self.output_instance_annual_source_results = []
        self.output_instance_building_peak_heating_load = None
        self.output_instance_building_peak_cooling_load = None
        self.output_instance_annual_end_use_results = []

    def populate_data_elements(self):
        requests, str_requests = self.get_output_requests()
        output_data = self.get_output_data(self, requests)
        for key, value in str_requests.items():
            output_data[key] = self.get_single_string_output(self, *value)

        self.output_instance_unmet_load_hours_heating = output_data.get(
            "Unmet Heating Load Hours"
        )
        self.output_instance_unmet_load_hours_cooling = output_data.get(
            "Unmet Cooling Load Hours"
        )
        self.output_instance_building_peak_cooling_load = output_data.get(
            "Building Peak Cooling Load"
        )
        self.output_instance_building_peak_heating_load = output_data.get(
            "Building Peak Heating Load"
        )
        energy_source_types = set()
        energy_source_results = {
            "Consumption": {
                "site_energy_use": 0,
                "peak_demand": 0,
            },
            "Interior Lighting": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Space Heating": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Heat Pump Supp.": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Space Cooling": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Pumps & Aux": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Heat Rejection": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Ventilation Fans": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Refrigeration Display": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Domestic Hot Water": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
            "Misc Equip": {
                "site_energy_use": 0,
                "coincident_demand": 0,
                "non_coincident_demand": 0,
            },
        }

        # Populate the set of unique energy sources in the model
        if output_data.get("Elec (all meters) - Elec Use"):
            energy_source_types.add(EnergySourceOptions.ELECTRICITY)
        for fuel_meter_name in self.fuel_meter_names:
            fuel_meter = self.bdl_obj_instances.get(fuel_meter_name)
            if fuel_meter:
                energy_source_types.add(fuel_meter.get_inp(BDL_FuelMeterKeywords.TYPE))
        if self.steam_meter_names:
            energy_source_types.add(EnergySourceOptions.PURCHASED_HOT_WATER)
        if self.chilled_water_meter_names:
            energy_source_types.add(EnergySourceOptions.PURCHASED_CHILLED_WATER)
        if self.elec_generator_names:
            generators = [
                self.bdl_obj_instances.get(generator_name)
                for generator_name in self.elec_generator_names
            ]
            if any(
                generator.get_inp(BDL_ElecGeneratorKeywords.TYPE)
                == BDL_ElecGeneratorTypes.PV_ARRAY
                for generator in generators
            ):
                energy_source_types.add(EnergySourceOptions.ON_SITE_RENEWABLES)

        # Populate the energy source results for each energy source
        for energy_source in energy_source_types:
            source_results = copy.deepcopy(energy_source_results)
            if energy_source == EnergySourceOptions.ELECTRICITY:
                source_results["Consumption"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use"
                )
                source_results["Consumption"]["peak_demand"] = output_data.get(
                    "Elec (all meters) - Peak Demand"
                )

                source_results["Interior Lighting"]["site_energy_use"] = (
                    output_data.get("Elec (all meters) - Elec Use - Lights")
                )
                source_results["Interior Lighting"]["coincident_demand"] = (
                    output_data.get("Elec (all meters) - Coincident Peak - Lights")
                )
                source_results["Interior Lighting"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Lights")
                )

                source_results["Misc Equip"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Misc Equip"
                )
                source_results["Misc Equip"]["coincident_demand"] = output_data.get(
                    "Elec (all meters) - Coincident Peak - Misc Equip"
                )
                source_results["Misc Equip"]["non_coincident_demand"] = output_data.get(
                    "Elec (all meters) - Peak - Misc Equip"
                )

                source_results["Space Heating"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Space Heating"
                )
                source_results["Space Heating"]["coincident_demand"] = output_data.get(
                    "Elec (all meters) - Coincident Peak - Space Heating"
                )
                source_results["Space Heating"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Space Heating")
                )

                source_results["Space Cooling"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Space Cooling"
                )
                source_results["Space Cooling"]["coincident_demand"] = output_data.get(
                    "Elec (all meters) - Coincident Peak - Space Cooling"
                )
                source_results["Space Cooling"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Space Cooling")
                )

                source_results["Heat Rejection"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Heat Rejection"
                )
                source_results["Heat Rejection"]["coincident_demand"] = output_data.get(
                    "Elec (all meters) - Coincident Peak - Heat Rejection"
                )
                source_results["Heat Rejection"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Heat Rejection")
                )

                source_results["Pumps & Aux"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["coincident_demand"] = output_data.get(
                    "Elec (all meters) - Coincident Peak - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Pumps & Aux")
                )

                source_results["Ventilation Fans"]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Ventilation Fans"
                )
                source_results["Ventilation Fans"]["coincident_demand"] = (
                    output_data.get(
                        "Elec (all meters) - Coincident Peak - Ventilation Fans"
                    )
                )
                source_results["Ventilation Fans"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Ventilation Fans")
                )

                source_results["Refrigeration Display"]["site_energy_use"] = (
                    output_data.get(
                        "Elec (all meters) - Elec Use - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["coincident_demand"] = (
                    output_data.get(
                        "Elec (all meters) - Coincident Peak - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Refrigeration Display")
                )

                source_results["Heat Pump Supp."]["site_energy_use"] = output_data.get(
                    "Elec (all meters) - Elec Use - Ht Pump Supplemental Heat"
                )
                source_results["Heat Pump Supp."]["coincident_demand"] = (
                    output_data.get(
                        "Elec (all meters) - Coincident Peak - Ht Pump Supplemental Heat"
                    )
                )
                source_results["Heat Pump Supp."]["non_coincident_demand"] = (
                    output_data.get(
                        "Elec (all meters) - Peak - Ht Pump Supplemental Heat"
                    )
                )

                source_results["Domestic Hot Water"]["site_energy_use"] = (
                    output_data.get("Elec (all meters) - Elec Use - Domestic Hot Water")
                )
                source_results["Domestic Hot Water"]["coincident_demand"] = (
                    output_data.get(
                        "Elec (all meters) - Coincident Peak - Domestic Hot Water"
                    )
                )
                source_results["Domestic Hot Water"]["non_coincident_demand"] = (
                    output_data.get("Elec (all meters) - Peak - Domestic Hot Water")
                )

            elif energy_source == EnergySourceOptions.PURCHASED_HOT_WATER:
                source_results["Consumption"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy"
                )
                source_results["Consumption"]["peak_demand"] = output_data.get(
                    "Steam (all meters) - Peak Demand"
                )

                source_results["Interior Lighting"]["site_energy_use"] = (
                    output_data.get("Steam (all meters) - Energy - Lights")
                )
                source_results["Interior Lighting"]["coincident_demand"] = (
                    output_data.get("Steam (all meters) - Coincident Peak - Lights")
                )
                source_results["Interior Lighting"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Lights")
                )

                source_results["Misc Equip"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Misc Equip"
                )
                source_results["Misc Equip"]["coincident_demand"] = output_data.get(
                    "Steam (all meters) - Coincident Peak - Misc Equip"
                )
                source_results["Misc Equip"]["non_coincident_demand"] = output_data.get(
                    "Steam (all meters) - Peak - Misc Equip"
                )

                source_results["Space Heating"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Space Heating"
                )
                source_results["Space Heating"]["coincident_demand"] = output_data.get(
                    "Steam (all meters) - Coincident Peak - Space Heating"
                )
                source_results["Space Heating"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Space Heating")
                )

                source_results["Space Cooling"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Space Cooling"
                )
                source_results["Space Cooling"]["coincident_demand"] = output_data.get(
                    "Steam (all meters) - Coincident Peak - Space Cooling"
                )
                source_results["Space Cooling"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Space Cooling")
                )

                source_results["Heat Rejection"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Heat Rejection"
                )
                source_results["Heat Rejection"]["coincident_demand"] = output_data.get(
                    "Steam (all meters) - Coincident Peak - Heat Rejection"
                )
                source_results["Heat Rejection"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Heat Rejection")
                )

                source_results["Pumps & Aux"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["coincident_demand"] = output_data.get(
                    "Steam (all meters) - Coincident Peak - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Pumps & Aux")
                )

                source_results["Ventilation Fans"]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Ventilation Fans"
                )
                source_results["Ventilation Fans"]["coincident_demand"] = (
                    output_data.get(
                        "Steam (all meters) - Coincident Peak - Ventilation Fans"
                    )
                )
                source_results["Ventilation Fans"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Ventilation Fans")
                )

                source_results["Refrigeration Display"]["site_energy_use"] = (
                    output_data.get(
                        "Steam (all meters) - Energy - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["coincident_demand"] = (
                    output_data.get(
                        "Steam (all meters) - Coincident Peak - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Refrigeration Display")
                )

                source_results["Heat Pump Supp."]["site_energy_use"] = output_data.get(
                    "Steam (all meters) - Energy - Ht Pump Supplemental Heat"
                )
                source_results["Heat Pump Supp."]["coincident_demand"] = (
                    output_data.get(
                        "Steam (all meters) - Coincident Peak - Ht Pump Supplemental Heat"
                    )
                )
                source_results["Heat Pump Supp."]["non_coincident_demand"] = (
                    output_data.get(
                        "Steam (all meters) - Peak - Ht Pump Supplemental Heat"
                    )
                )

                source_results["Domestic Hot Water"]["site_energy_use"] = (
                    output_data.get("Steam (all meters) - Energy - Domestic Hot Water")
                )
                source_results["Domestic Hot Water"]["coincident_demand"] = (
                    output_data.get(
                        "Steam (all meters) - Coincident Peak - Domestic Hot Water"
                    )
                )
                source_results["Domestic Hot Water"]["non_coincident_demand"] = (
                    output_data.get("Steam (all meters) - Peak - Domestic Hot Water")
                )

            elif energy_source == EnergySourceOptions.PURCHASED_CHILLED_WATER:
                source_results["Consumption"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy"
                )
                source_results["Consumption"]["peak_demand"] = output_data.get(
                    "Chilled Water (all meters) - Peak Demand"
                )

                source_results["Interior Lighting"]["site_energy_use"] = (
                    output_data.get("Chilled Water (all meters) - Energy - Lights")
                )
                source_results["Interior Lighting"]["coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Coincident Peak - Lights"
                    )
                )
                source_results["Interior Lighting"]["non_coincident_demand"] = (
                    output_data.get("Chilled Water (all meters) - Peak - Lights")
                )

                source_results["Misc Equip"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Misc Equip"
                )
                source_results["Misc Equip"]["coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Coincident Peak - Misc Equip"
                )
                source_results["Misc Equip"]["non_coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Peak - Misc Equip"
                )

                source_results["Space Heating"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Space Heating"
                )
                source_results["Space Heating"]["coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Coincident Peak - Space Heating"
                )
                source_results["Space Heating"]["non_coincident_demand"] = (
                    output_data.get("Chilled Water (all meters) - Peak - Space Heating")
                )

                source_results["Space Cooling"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Space Cooling"
                )
                source_results["Space Cooling"]["coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Coincident Peak - Space Cooling"
                )
                source_results["Space Cooling"]["non_coincident_demand"] = (
                    output_data.get("Chilled Water (all meters) - Peak - Space Cooling")
                )

                source_results["Heat Rejection"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Heat Rejection"
                )
                source_results["Heat Rejection"]["coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Coincident Peak - Heat Rejection"
                )
                source_results["Heat Rejection"]["non_coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Peak - Heat Rejection"
                    )
                )

                source_results["Pumps & Aux"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["coincident_demand"] = output_data.get(
                    "Chilled Water (all meters) - Coincident Peak - Pumps & Aux"
                )
                source_results["Pumps & Aux"]["non_coincident_demand"] = (
                    output_data.get("Chilled Water (all meters) - Peak - Pumps & Aux")
                )

                source_results["Ventilation Fans"]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Ventilation Fans"
                )
                source_results["Ventilation Fans"]["coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Coincident Peak - Ventilation Fans"
                    )
                )
                source_results["Ventilation Fans"]["non_coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Peak - Ventilation Fans"
                    )
                )

                source_results["Refrigeration Display"]["site_energy_use"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Energy - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Coincident Peak - Refrigeration Display"
                    )
                )
                source_results["Refrigeration Display"]["non_coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Peak - Refrigeration Display"
                    )
                )

                source_results["Heat Pump Supp."]["site_energy_use"] = output_data.get(
                    "Chilled Water (all meters) - Energy - Ht Pump Supplemental Heat"
                )
                source_results["Heat Pump Supp."]["coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Coincident Peak - Ht Pump Supplemental Heat"
                    )
                )
                source_results["Heat Pump Supp."]["non_coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Peak - Ht Pump Supplemental Heat"
                    )
                )

                source_results["Domestic Hot Water"]["site_energy_use"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Energy - Domestic Hot Water"
                    )
                )
                source_results["Domestic Hot Water"]["coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Coincident Peak - Domestic Hot Water"
                    )
                )
                source_results["Domestic Hot Water"]["non_coincident_demand"] = (
                    output_data.get(
                        "Chilled Water (all meters) - Peak - Domestic Hot Water"
                    )
                )

            elif energy_source == EnergySourceOptions.ON_SITE_RENEWABLES:
                source_results["Consumption"]["site_energy_use"] = sum(
                    output_data.get(f"Elec (meter {generator_name}) - Elec Use")
                    for generator_name in self.elec_generator_names
                    if self.bdl_obj_instances.get(generator_name).get_inp(
                        BDL_ElecGeneratorKeywords.TYPE
                    )
                    == BDL_ElecGeneratorTypes.PV_ARRAY
                )
                if len(self.elec_generator_names) == 1:
                    source_results["Consumption"]["peak_demand"] = output_data.get(
                        f"Elec (meter {self.elec_generator_names[0]}) - Peak Demand"
                    )

            else:
                # Sum results from fuel meters that have the same type
                for fuel_meter_name in self.fuel_meter_names:
                    fuel_meter = self.bdl_obj_instances.get(fuel_meter_name)
                    if (
                        fuel_meter
                        and fuel_meter.get_inp(BDL_FuelMeterKeywords.TYPE)
                        == energy_source
                    ):
                        source_results["Consumption"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use"
                        )

                        source_results["Interior Lighting"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Lights"
                        )
                        source_results["Interior Lighting"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Lights"
                        )

                        source_results["Misc Equip"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Misc Equip"
                        )
                        source_results["Misc Equip"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Misc Equip"
                        )

                        source_results["Space Heating"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Space Heating"
                        )
                        source_results["Space Heating"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Space Heating"
                        )

                        source_results["Space Cooling"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Space Cooling"
                        )
                        source_results["Space Cooling"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Space Cooling"
                        )

                        source_results["Heat Rejection"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Heat Rejection"
                        )
                        source_results["Heat Rejection"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Heat Rejection"
                        )

                        source_results["Pumps & Aux"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Pumps & Aux"
                        )
                        source_results["Pumps & Aux"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Pumps & Aux"
                        )

                        source_results["Ventilation Fans"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Ventilation Fans"
                        )
                        source_results["Ventilation Fans"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Ventilation Fans"
                        )

                        source_results["Refrigeration Display"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Refrigeration Display"
                        )
                        source_results["Refrigeration Display"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Refrigeration Display"
                        )

                        source_results["Heat Pump Supp."][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Ht Pump Supplemental Heat"
                        )
                        source_results["Heat Pump Supp."][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Ht Pump Supplemental Heat"
                        )

                        source_results["Domestic Hot Water"][
                            "site_energy_use"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Fuel Use - Domestic Hot Water"
                        )
                        source_results["Domestic Hot Water"][
                            "non_coincident_demand"
                        ] += output_data.get(
                            f"Fuel (meter {fuel_meter_name}) - Peak - Domestic Hot Water"
                        )

                if len(self.fuel_meter_names) == 1:
                    source_results["Consumption"]["peak_demand"] = output_data.get(
                        f"Fuel (all meters) - Peak Demand"
                    )

                    source_results["Interior Lighting"][
                        "coincident_demand"
                    ] += output_data.get("Fuel (all meters) - Coincident Peak - Lights")

                    source_results["Misc Equip"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Misc Equip"
                    )

                    source_results["Space Heating"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Space Heating"
                    )

                    source_results["Space Cooling"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Space Cooling"
                    )

                    source_results["Heat Rejection"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Heat Rejection"
                    )

                    source_results["Pumps & Aux"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Pumps & Aux"
                    )

                    source_results["Ventilation Fans"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Ventilation Fans"
                    )

                    source_results["Refrigeration Display"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Refrigeration Display"
                    )

                    source_results["Heat Pump Supp."][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Ht Pump Supplemental Heat"
                    )

                    source_results["Domestic Hot Water"][
                        "coincident_demand"
                    ] += output_data.get(
                        "Fuel (all meters) - Coincident Peak - Domestic Hot Water"
                    )

            self.output_instance_annual_source_results.append(
                {
                    # soure results data elements
                    "id": energy_source,
                    "energy_source": fuel_type_map.get(energy_source),
                    "annual_consumption": source_results["Consumption"][
                        "site_energy_use"
                    ],
                    "annual_demand": source_results["Consumption"]["peak_demand"],
                    # "annual_cost": None,
                }
            )

            self.populate_energy_source_end_use_results(source_results, energy_source)

    def get_output_requests(self):
        requests = {
            "Total Site Energy (BTU)": (
                2001001,
                "",
                "",
            ),
            "Unmet Cooling Load Hours": (
                2001022,
                "",
                "",
            ),
            "Unmet Heating Load Hours": (
                2001023,
                "",
                "",
            ),
            "Building Peak Cooling Load": (
                1003003,
                "",
                "",
            ),
            "Building Peak Heating Load": (
                1003005,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Lights": (
                2001009,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Task Lights": (
                2001010,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Misc Equip": (
                2001011,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Space Heating": (
                2001012,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Space Cooling": (
                2001013,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Heat Rejection": (
                2001014,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Pumps & Aux": (
                2001015,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Ventilation Fans": (
                2001016,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Refrigeration Display": (
                2001017,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Ht Pump Supplemental Heat": (
                2001018,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Domestic Hot Water": (
                2001019,
                "",
                "",
            ),
            "Total Site Energy (BTU) - Exterior Usage": (
                2001020,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use": (
                2305001,
                "",
                "",
            ),
            "Elec (all meters) - Peak Demand": (
                2305002,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Lights": (
                2305006,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Task Lights": (
                2305007,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Misc Equip": (
                2305008,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Space Heating": (
                2305009,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Space Cooling": (
                2305010,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Heat Rejection": (
                2305011,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Pumps & Aux": (
                2305012,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Ventilation Fans": (
                2305013,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Refrigeration Display": (
                2305014,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Ht Pump Supplemental Heat": (
                2305015,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Domestic Hot Water": (
                2305016,
                "",
                "",
            ),
            "Elec (all meters) - Elec Use - Exterior Usage": (
                2305017,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Lights": (
                2305019,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Task Lights": (
                2305020,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Misc Equip": (
                2305021,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Space Heating": (
                2305022,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Space Cooling": (
                2305023,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Heat Rejection": (
                2305024,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Pumps & Aux": (
                2305025,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Ventilation Fans": (
                2305026,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Refrigeration Display": (
                2305027,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Ht Pump Supplemental Heat": (
                2305028,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Domestic Hot Water": (
                2305029,
                "",
                "",
            ),
            "Elec (all meters) - Peak - Exterior Usage": (
                2305030,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Lights": (
                2305186,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Task Lights": (
                2305187,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Misc Equip": (
                2305188,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Space Heating": (
                2305189,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Space Cooling": (
                2305190,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Heat Rejection": (
                2305191,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Pumps & Aux": (
                2305192,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Ventilation Fans": (
                2305193,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Refrigeration Display": (
                2305194,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Ht Pump Supplemental Heat": (
                2305195,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Domestic Hot Water": (
                2305196,
                "",
                "",
            ),
            "Elec (all meters) - Coincident Peak - Exterior Usage": (
                2305197,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use": (
                2306001,
                "",
                "",
            ),
            "Fuel (all meters) - Peak Demand": (
                2306002,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Lights": (
                2306006,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Task Lights": (
                2306007,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Misc Equip": (
                2306008,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Space Heating": (
                2306009,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Space Cooling": (
                2306010,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Heat Rejection": (
                2306011,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Pumps & Aux": (
                2306012,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Ventilation Fans": (
                2306013,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Refrigeration Display": (
                2306014,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Ht Pump Supplemental Heat": (
                2306015,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Domestic Hot Water": (
                2306016,
                "",
                "",
            ),
            "Fuel (all meters) - Fuel Use - Exterior Usage": (
                2306017,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Lights": (
                2306019,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Task Lights": (
                2306020,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Misc Equip": (
                2306021,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Space Heating": (
                2306022,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Space Cooling": (
                2306023,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Heat Rejection": (
                2306024,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Pumps & Aux": (
                2306025,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Ventilation Fans": (
                2306026,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Refrigeration Display": (
                2306027,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Ht Pump Supplemental Heat": (
                2306028,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Domestic Hot Water": (
                2306029,
                "",
                "",
            ),
            "Fuel (all meters) - Peak - Exterior Usage": (
                2306030,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Lights": (
                2306186,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Task Lights": (
                2306187,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Misc Equip": (
                2306188,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Space Heating": (
                2306189,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Space Cooling": (
                2306190,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Heat Rejection": (
                2306191,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Pumps & Aux": (
                2306192,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Ventilation Fans": (
                2306193,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Refrigeration Display": (
                2306194,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Ht Pump Supplemental Heat": (
                2306195,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Domestic Hot Water": (
                2306196,
                "",
                "",
            ),
            "Fuel (all meters) - Coincident Peak - Exterior Usage": (
                2306197,
                "",
                "",
            ),
            "Steam (all meters) - Energy": (
                2307001,
                "",
                "",
            ),
            "Steam (all meters) - Peak Demand": (
                2307002,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Lights": (
                2307006,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Task Lights": (
                2307007,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Misc Equip": (
                2307008,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Space Heating": (
                2307009,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Space Cooling": (
                2307010,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Heat Rejection": (
                2307011,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Pumps & Aux": (
                2307012,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Ventilation Fans": (
                2307013,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Refrigeration Display": (
                2307014,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Ht Pump Supplemental Heat": (
                2307015,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Domestic Hot Water": (
                2307016,
                "",
                "",
            ),
            "Steam (all meters) - Energy - Exterior Usage": (
                2307017,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Lights": (
                2307019,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Task Lights": (
                2307020,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Misc Equip": (
                2307021,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Space Heating": (
                2307022,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Space Cooling": (
                2307023,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Heat Rejection": (
                2307024,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Pumps & Aux": (
                2307025,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Ventilation Fans": (
                2307026,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Refrigeration Display": (
                2307027,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Ht Pump Supplemental Heat": (
                2307028,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Domestic Hot Water": (
                2307029,
                "",
                "",
            ),
            "Steam (all meters) - Peak - Exterior Usage": (
                2307030,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Lights": (
                2307186,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Task Lights": (
                2307187,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Misc Equip": (
                2307188,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Space Heating": (
                2307189,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Space Cooling": (
                2307190,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Heat Rejection": (
                2307191,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Pumps & Aux": (
                2307192,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Ventilation Fans": (
                2307193,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Refrigeration Display": (
                2307194,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Ht Pump Supplemental Heat": (
                2307195,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Domestic Hot Water": (
                2307196,
                "",
                "",
            ),
            "Steam (all meters) - Coincident Peak - Exterior Usage": (
                2307197,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy": (
                2308001,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak Demand": (
                2308002,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Lights": (
                2308006,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Task Lights": (
                2308007,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Misc Equip": (
                2308008,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Space Heating": (
                2308009,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Space Cooling": (
                2308010,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Heat Rejection": (
                2308011,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Pumps & Aux": (
                2308012,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Ventilation Fans": (
                2308013,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Refrigeration Display": (
                2308014,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Ht Pump Supplemental Heat": (
                2308015,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Domestic Hot Water": (
                2308016,
                "",
                "",
            ),
            "Chilled Water (all meters) - Energy - Exterior Usage": (
                2308017,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Lights": (
                2308019,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Task Lights": (
                2308020,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Misc Equip": (
                2308021,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Space Heating": (
                2308022,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Space Cooling": (
                2308023,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Heat Rejection": (
                2308024,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Pumps & Aux": (
                2308025,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Ventilation Fans": (
                2308026,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Refrigeration Display": (
                2308027,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Ht Pump Supplemental Heat": (
                2308028,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Domestic Hot Water": (
                2308029,
                "",
                "",
            ),
            "Chilled Water (all meters) - Peak - Exterior Usage": (
                2308030,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Lights": (
                2308186,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Task Lights": (
                2308187,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Misc Equip": (
                2308188,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Space Heating": (
                2308189,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Space Cooling": (
                2308190,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Heat Rejection": (
                2308191,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Pumps & Aux": (
                2308192,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Ventilation Fans": (
                2308193,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Refrigeration Display": (
                2308194,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Ht Pump Supplemental Heat": (
                2308195,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Domestic Hot Water": (
                2308196,
                "",
                "",
            ),
            "Chilled Water (all meters) - Coincident Peak - Exterior Usage": (
                2308197,
                "",
                "",
            ),
        }
        string_requests = {}
        for fuel_meter_name in self.fuel_meter_names:
            string_requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use Units"] = (
                2310001,
                fuel_meter_name,
                "",
            )
            string_requests[f"Fuel (meter {fuel_meter_name}) - Peak Demand Units"] = (
                2310002,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use"] = (
                2310003,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak Demand"] = (
                2310004,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Lights"] = (
                2310008,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Task Lights"] = (
                2310009,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Misc Equip"] = (
                2310010,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Space Heating"] = (
                2310011,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Space Cooling"] = (
                2310012,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Heat Rejection"] = (
                2310013,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Pumps & Aux"] = (
                2310014,
                fuel_meter_name,
                "",
            )
            requests[
                f"Fuel (meter {fuel_meter_name}) - Fuel Use - Ventilation Fans"
            ] = (
                2310015,
                fuel_meter_name,
                "",
            )
            requests[
                f"Fuel (meter {fuel_meter_name}) - Fuel Use - Refrigeration Display"
            ] = (2310016, fuel_meter_name, "")
            requests[
                f"Fuel (meter {fuel_meter_name}) - Fuel Use - Ht Pump Supplemental Heat"
            ] = (
                2310017,
                fuel_meter_name,
                "",
            )
            requests[
                f"Fuel (meter {fuel_meter_name}) - Fuel Use - Domestic Hot Water"
            ] = (
                2310018,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Fuel Use - Exterior Usage"] = (
                2310019,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Lights"] = (
                2310058,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Task Lights"] = (
                2310059,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Misc Equip"] = (
                2310060,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Space Heating"] = (
                2310061,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Space Cooling"] = (
                2310062,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Heat Rejection"] = (
                2310063,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Pumps & Aux"] = (
                2310064,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Ventilation Fans"] = (
                2310065,
                fuel_meter_name,
                "",
            )
            requests[
                f"Fuel (meter {fuel_meter_name}) - Peak - Refrigeration Display"
            ] = (
                2310066,
                fuel_meter_name,
                "",
            )
            requests[
                f"Fuel (meter {fuel_meter_name}) - Peak - Ht Pump Supplemental Heat"
            ] = (
                2310067,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Domestic Hot Water"] = (
                2310068,
                fuel_meter_name,
                "",
            )
            requests[f"Fuel (meter {fuel_meter_name}) - Peak - Exterior Usage"] = (
                2310069,
                fuel_meter_name,
                "",
            )

        for elec_generator_name in self.elec_generator_names:
            elec_generator = self.bdl_obj_instances[elec_generator_name]
            if (
                elec_generator
                and elec_generator.get_inp(BDL_ElecGeneratorKeywords.TYPE)
                == BDL_ElecGeneratorTypes.PV_ARRAY
            ):
                requests[f"PV Array {elec_generator_name} - Energy"] = (
                    2303259,
                    elec_generator_name,
                    "",
                )
                requests[f"PV Array {elec_generator_name} - Peak Demand"] = (
                    2303260,
                    elec_generator_name,
                    "",
                )

        for utility_rate_name in self.utility_rate_names:
            # TODO diagnose why Utility Rate output requests are not being fulfilled
            pass

        return requests, string_requests

    def populate_data_group(self):
        """Populate the RMD data structure."""

        self.output_instance = {
            key: value
            for key, value in {
                "id": self.output_instance_id,
                "ruleset_model_type": self.output_instance_ruleset_model_type,
                "rotation_angle": self.output_instance_rotation_angle,
                "unmet_load_hours": self.output_instance_unmet_load_hours,
                "unmet_load_hours_heating": self.output_instance_unmet_load_hours_heating,
                "unmet_occupied_load_hours_heating": self.output_instance_unmet_occupied_load_hours_heating,
                "unmet_load_hours_cooling": self.output_instance_unmet_load_hours_cooling,
                "unmet_occupied_load_hours_cooling": self.output_instance_unmet_occupied_load_hours_cooling,
                "annual_source_results": self.output_instance_annual_source_results,
                "building_peak_heating_load": self.output_instance_building_peak_heating_load,
                "building_peak_cooling_load": self.output_instance_building_peak_cooling_load,
                "annual_end_use_results": self.output_instance_annual_end_use_results,
            }.items()
            if value is not None
        }

        self.output = {
            key: value
            for key, value in {
                "id": self.output_id,
                "output_instance": self.output_instance,
                "performance_cost_index": self.output_performance_cost_index,
                "baseline_building_unregulated_energy_cost": self.output_baseline_building_unregulated_energy_cost,
                "baseline_building_regulated_energy_cost": self.output_baseline_building_regulated_energy_cost,
                "baseline_building_performance_energy_cost": self.output_baseline_building_performance_energy_cost,
                "total_area_weighted_building_performance_factor": self.output_total_area_weighted_building_performance_factor,
                "performance_cost_index_target": self.output_performance_cost_index_target,
                "total_proposed_building_energy_cost_including_renewable_energy": self.output_total_proposed_building_energy_cost_including_renewable_energy,
                "total_proposed_building_energy_cost_excluding_renewable_energy": self.output_total_proposed_building_energy_cost_excluding_renewable_energy,
                "percent_renewable_energy_savings": self.output_percent_renewable_energy_savings,
            }.items()
            if value is not None
        }

        self.rmd_data_structure = {
            key: value
            for key, value in {
                "id": self.obj_id,
                "buildings": self.buildings,
                "schedules": self.schedules,
                "fluid_loops": self.fluid_loops,
                "service_water_heating_distribution_systems": self.service_water_heating_distribution_systems,
                "service_water_heating_equipment": self.service_water_heating_equipment,
                "pumps": self.pumps,
                "boilers": self.boilers,
                "chillers": self.chillers,
                "heat_rejections": self.heat_rejections,
                "external_fluid_sources": self.external_fluid_sources,
                "output": self.output,
            }.items()
            if value is not None
        }

    def insert_to_rpd(self, rpd):
        """Insert RMD object into the RPD data structure."""
        rpd.ruleset_model_descriptions.append(self.rmd_data_structure)

    def populate_energy_source_end_use_results(
        self, source_results, energy_source_type
    ):
        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Interior Lighting",
                "type": EndUseOptions.INTERIOR_LIGHTING,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Interior Lighting"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Interior Lighting"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results[
                    "Interior Lighting"
                ]["non_coincident_demand"],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Misc Equipment",
                "type": EndUseOptions.MISC_EQUIPMENT,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Misc Equip"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Misc Equip"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Misc Equip"][
                    "non_coincident_demand"
                ],
                "is_regulated": False,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Space Heating",
                "type": EndUseOptions.SPACE_HEATING,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Space Heating"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Space Heating"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Space Heating"][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Space Cooling",
                "type": EndUseOptions.SPACE_COOLING,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Space Cooling"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Space Cooling"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Space Cooling"][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Heat Rejection",
                "type": EndUseOptions.HEAT_REJECTION,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Heat Rejection"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Heat Rejection"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Heat Rejection"][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Pumps & Aux",
                "type": EndUseOptions.PUMPS,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Pumps & Aux"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Pumps & Aux"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Pumps & Aux"][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Ventilation Fans",
                "type": EndUseOptions.FANS_INTERIOR_VENTILATION,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Ventilation Fans"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Ventilation Fans"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Ventilation Fans"][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Refrigeration Display",
                "type": EndUseOptions.REFRIGERATION_EQUIPMENT,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Refrigeration Display"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results[
                    "Refrigeration Display"
                ]["coincident_demand"],
                "annual_site_non_coincident_demand": source_results[
                    "Refrigeration Display"
                ]["non_coincident_demand"],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Ht Pump Supplemental Heat",
                "type": EndUseOptions.HEAT_PUMP_SUPPLEMENTAL_HEATING,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Heat Pump Supp."][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Heat Pump Supp."][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results["Heat Pump Supp."][
                    "non_coincident_demand"
                ],
                "is_regulated": True,
            }
        )

        self.output_instance_annual_end_use_results.append(
            {
                "id": f"{energy_source_type} - Domestic Hot Water",
                "type": EndUseOptions.SERVICE_WATER_HEATING,
                "energy_source": energy_source_type,
                "annual_site_energy_use": source_results["Domestic Hot Water"][
                    "site_energy_use"
                ],
                "annual_site_coincident_demand": source_results["Domestic Hot Water"][
                    "coincident_demand"
                ],
                "annual_site_non_coincident_demand": source_results[
                    "Domestic Hot Water"
                ]["non_coincident_demand"],
                "is_regulated": True,
            }
        )
