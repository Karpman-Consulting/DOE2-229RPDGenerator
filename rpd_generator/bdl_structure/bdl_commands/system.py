from rpd_generator.bdl_structure.parent_node import ParentNode


class System(ParentNode):
    """System object in the tree."""

    bdl_command = "SYSTEM"

    heat_type_map = {
        "HEAT-PUMP": "HEAT_PUMP",
        "FURNACE": "FURNACE",
        "ELECTRIC": "ELECTRIC_RESISTANCE",
        "HOT-WATER": "FLUID_LOOP",
        "NONE": "NONE",
        "STEAM": "OTHER",
        "DHW-LOOP": "OTHER",
    }
    cool_type_map = {
        "ELEC-DX": "DIRECT_EXPANSION",
        "CHILLED-WATER": "FLUID_LOOP",
        "NONE": "NONE",
    }
    supply_fan_map = {
        "CONSTANT-VOLUME": "CONSTANT",
        "SPEED": "VARIABLE_SPEED_DRIVE",
        #  "": "MULTISPEED",  no eQUEST options map to MULTISPEED in DOE2.3
        "INLET": "INLET_VANE",
        "DISCHARGE": "DISCHARGE_DAMPER",
        "FAN-EIR-FPLR": "VARIABLE_SPEED_DRIVE",
    }
    unocc_fan_operation_map = {
        "CYCLE-ON-ANY": "CYCLING",
        "CYCLE-ON-FIRST": "CYCLING",
        "STAY-OFF": "KEEP_OFF",
        "ZONE-FANS-ONLY": "OTHER",
    }
    system_cooling_type_map = {
        "PSZ": "DIRECT_EXPANSION",
        "PMZS": "DIRECT_EXPANSION",
        "PVAVS": "DIRECT_EXPANSION",
        "PVVT": "DIRECT_EXPANSION",
        "HP": "DIRECT_EXPANSION",  # IS WATER LOOP HEAT PUMP CONSIDERED DIRECT_EXPANSION???
        "SZRH": "FLUID_LOOP",
        "VAVS": "FLUID_LOOP",
        "RHFS": "FLUID_LOOP",
        "DDS": "FLUID_LOOP",
        "MZS": "FLUID_LOOP",
        "PIU": None,  # Mapping updated in populate_cooling_system method
        "FC": "FLUID_LOOP",
        "IU": "FLUID_LOOP",
        "UVT": "NONE",
        "UHT": "NONE",
        "RESYS2": "DIRECT_EXPANSION",
        "CBVAV": "FLUID_LOOP",
        "SUM": "NONE",
        "DOAS": None,  # Mapping updated in populate_cooling_system method
    }
    economizer_map = {
        "FIXED": "FIXED_FRACTION",
        "OA-TEMP": "FIXED_DRY_BULB",
        "OA-ENTHALPY": "FIXED_ENTHALPY",
        "DUAL-TEMP": "DIFFERENTIAL_TEMPERATURE",
        "DUAL-ENTHALPY": "DIFFERENTIAL_ENTHALPY",
    }
    recovery_type_map = {
        "SENSIBLE-HX": "SENSIBLE_HEAT_EXCHANGE",
        "ENTHALPY-HX": "ENTHALPY_HEAT_EXCHANGE",
        "SENSIBLE-WHEEL": "SENSIBLE_HEAT_WHEEL",
        "ENTHALPY-WHEEL": "ENTHALPY_HEAT_WHEEL",
        "HEAT-PIPE": "HEAT_PIPE",
    }
    has_recovery_map = {
        "NO": "NONE",
        "RELIEF-ONLY": None,  # Mapping updated in populate_air_energy_recovery method
        "EXHAUST-ONLY": None,  # Mapping updated in populate_air_energy_recovery method
        "RELIEF+EXHAUST": None,  # Mapping updated in populate_air_energy_recovery method
        "YES": None,  # Mapping updated in populate_air_energy_recovery method
    }
    er_operation_map = {
        "WHEN-FANS-ON": "WHEN_FANS_ON",
        "WHEN-MIN-OA": "WHEN_MINIMUM_OUTSIDE_AIR",
        "ERV-SCHEDULE": "SCHEDULED",
        "OA-EXHAUST-DT": "OTHER",
        "OA-EXHAUST-DH": "OTHER",
    }
    er_sat_control_map = {
        "FLOAT": "OTHER",
        "FIXED-SETPT": "FIXED_SETPOINT",
        "MIXED-AIR-RESET": "MIXED_AIR_RESET",
    }
    dcv_map = {
        "FRAC-OF-DESIGN-FLOW": "NONE",
        "FRAC-OF-HOURLY-FLOW": "NONE",
        "DCV-RETURN-SENSOR": "CO2_RETURN_AIR",
        "DCV-ZONE-SENSORS": "CO2_ZONE",
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        # On initialization the parent building segment is not known. It will be set in the GUI.
        self.parent_building_segment = rmd.bdl_obj_instances.get(
            "Default Building Segment", None
        )

        self.system_data_structure = {}
        self.omit = False

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
        self.fan_sys_temp_control = None
        self.fan_sys_operation_during_occ = None
        self.fan_sys_operation_during_unocc = None
        self.fan_sys_has_unocc_central_heat_lockout = None
        self.fan_sys_fan_control = None
        self.fan_sys_reset_diff_temp = None
        self.fan_sys_sat_reset_load_fraction = None
        self.fan_sys_sat_reset_schedule = None
        self.fan_sys_fan_volume_reset_type = None
        self.fan_sys_fan_volume_reset_fraction = None
        self.fan_sys_operating_schedule = None
        self.fan_sys_min_airflow = None
        self.fan_sys_min_oa_airflow = None
        self.fan_sys_max_oa_airflow = None
        self.fan_sys_air_filter_merv = None
        self.fan_sys_has_fully_ducted_return = None
        self.fan_sys_dcv_control = None

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
        self.cool_sys_design_total_capacity = None
        self.cool_sys_design_sensible_capacity = None
        self.cool_sys_rated_total_capacity = None
        self.cool_sys_rated_sensible_capacity = None
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

        # [supply, return, relief, exhaust] fan data elements
        self.fan_id = [None, None, None, None]
        self.fan_reporting_name = [None, None, None, None]
        self.fan_notes = [None, None, None, None]
        self.fan_design_airflow = [None, None, None, None]
        self.fan_is_airflow_sized_based_on_design_day = [None, None, None, None]
        self.fan_specification_method = [None, None, None, None]
        self.fan_design_electric_power = [None, None, None, None]
        self.fan_design_pressure_rise = [None, None, None, None]
        self.fan_motor_nameplate_power = [None, None, None, None]
        self.fan_shaft_power = [None, None, None, None]
        self.fan_total_efficiency = [None, None, None, None]
        self.fan_motor_efficiency = [None, None, None, None]
        self.fan_motor_heat_to_airflow_fraction = [None, None, None, None]
        self.fan_motor_heat_to_zone_fraction = [None, None, None, None]
        self.fan_motor_location_zone = [None, None, None, None]
        self.fan_status_type = [None, None, None, None]
        self.fan_output_validation_points = [[], [], [], []]

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
        self.air_energy_recovery_operation = None
        self.air_energy_recovery_sat_control = None
        self.air_energy_recovery_sensible_effectiveness = None
        self.air_energy_recovery_latent_effectiveness = None
        self.air_energy_recovery_outdoor_airflow = None
        self.air_energy_recovery_exhaust_airflow = None

        # terminal data elements
        self.terminals_id = [None]
        self.terminals_reporting_name = [None]
        self.terminals_notes = [None]
        self.terminals_type = [None]
        self.terminals_served_by_hvac_system = [None]
        self.terminals_heating_source = [None]
        self.terminals_heating_from_loop = [None]
        self.terminals_cooling_source = [None]
        self.terminals_cooling_from_loop = [None]
        self.terminals_fan = [{}]
        self.terminals_fan_configuration = [None]
        self.terminals_primary_airflow = [None]
        self.terminals_secondary_airflow = [None]
        self.terminals_max_heating_airflow = [None]
        self.terminals_supply_design_heat_t_setpoint = [None]
        self.terminals_supply_design_cool_t_setpoint = [None]
        self.terminals_temp_control = [None]
        self.terminals_minimum_airflow = [None]
        self.terminals_minimum_outdoor_airflow = [None]
        self.terminals_min_oa_multiplier_schedule = [None]
        self.terminals_heating_capacity = [None]
        self.terminals_cooling_capacity = [None]
        self.terminals_is_supply_ducted = [None]
        self.terminals_has_dcv = [None]
        self.terminals_is_fan_first_stage_heat = [None]

    def __repr__(self):
        return f"System(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements from the keyword_value pairs returned from model_input_reader."""
        if self.keyword_value_pairs.get("TYPE") == "SUM":
            self.omit = True
            return

        cool_source = self.keyword_value_pairs.get("COOL-SOURCE")
        cool_type = self.cool_type_map.get(cool_source)
        # Update the cooling type map according to the COOL-SOURCE keyword (only used for PIU and DOAS)
        self.system_cooling_type_map.update(
            {
                "PIU": cool_type,
                "DOAS": cool_type,
            }
        )

        heat_type = self.heat_type_map.get(self.keyword_value_pairs.get("HEAT-SOURCE"))
        terminal_system_conditions = (
                self.keyword_value_pairs.get("TYPE") in ["FC", "IU"]
                and heat_type == "FLUID_LOOP"
        )

        if terminal_system_conditions:
            self.populate_terminal_system()

        else:
            self.populate_fan_system()
            self.populate_heating_system()
            self.populate_cooling_system()
            self.populate_preheat_system()

        # self.get_output_data()

    def get_output_requests(self):
        """Get the output requests for the system dependent on various system component types."""
        #      2201005,  38,  1,  2,  6,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Outside Air Ratio
        #      2201006,  38,  1,  2,  7,  1,  1,  1,  0, 64,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Cooling Capacity
        #      2201007,  38,  1,  2,  8,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Sensible Heat Ratio
        #      2201008,  38,  1,  2,  9,  1,  1,  1,  0, 64,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Heating Capacity
        #      2201009,  38,  1,  2, 10,  1,  1,  1,  0, 46,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Cooling EIR
        #      2201010,  38,  1,  2, 11,  1,  1,  1,  0, 46,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Heating EIR
        #      2201011,  38,  1,  2, 12,  1,  1,  1,  0, 64,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - General - Heat Pump Supplemental Heat
        #      2201012,  38,  1,  4,  3,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Airflow
        #      2201013,  38,  1,  4,  4,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Diversity Factor
        #      2201014,  38,  1,  4,  5,  1,  1,  1,  0, 28,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Power
        #      2201015,  38,  1,  4,  6,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Air Temperature Rise
        #      2201016,  38,  1,  4,  7,  1,  1,  1,  0, 26,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Total Static Pressure
        #      2201017,  38,  1,  4,  8,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Overall Efficiency
        #      2201018,  38,  1,  4,  9,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Mechanical Efficiency
        #      2201019,  38,  1,  4, 10,  2,  1,  3,  0,  1,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Fan Placement
        #      2201020,  38,  1,  4, 13,  2,  1,  2,  0,  1,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Fan Control
        #      2201021,  38,  1,  4, 15,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Maximum Fan Output
        #      2201022,  38,  1,  4, 16,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Supply Fan - Minimum Fan Output
        #      2201023,  38,  1, 15,  3,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Airflow
        #      2201024,  38,  1, 15,  4,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Diversity Factor
        #      2201025,  38,  1, 15,  5,  1,  1,  1,  0, 28,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Power
        #      2201026,  38,  1, 15,  6,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Air Temperature Rise
        #      2201027,  38,  1, 15,  7,  1,  1,  1,  0, 26,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Total Static Pressure
        #      2201028,  38,  1, 15,  8,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Overall Efficiency
        #      2201029,  38,  1, 15,  9,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Mechanical Efficiency
        #      2201030,  38,  1, 15, 10,  2,  1,  3,  0,  1,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Fan Placement
        #      2201031,  38,  1, 15, 13,  2,  1,  2,  0,  1,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Fan Control
        #      2201032,  38,  1, 15, 15,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Maximum Fan Output
        #      2201033,  38,  1, 15, 16,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; HVAC Systems - Design Parameters - Return Fan - Minimum Fan Output

        #      2203001, 103,  1,  7,  9,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - month of peak
        #      2203002, 103,  1,  7, 10,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - day of peak
        #      2203003, 103,  1,  7, 11,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - hour of peak
        #      2203004, 103,  1,  7, 12,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - outdoor DBT at peak
        #      2203005, 103,  1,  7, 13,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - outdoor WBT at peak
        #      2203006, 103,  1,  7, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - capacity, btu/hr
        #      2203007, 103,  1,  7, 15,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - SHR
        #      2203008, 103,  1,  7, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - air flow, cfm
        #      2203009, 103,  1,  7, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - coil entering drybulb
        #      2203010, 103,  1,  7, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - coil entering wetbulb
        #      2203011, 103,  1,  7, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - coil leaving drybulb
        #      2203012, 103,  1,  7, 20,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - coil leaving wetbulb
        #      2203013, 103,  1,  7, 21,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - coil bypass factor
        #      2203014, 103,  1,  7, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Cooling - chilled water - SYSTEM - chilled water entering temp
        #      2203015, 103,  1,  8, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - capacity, btu/hr
        #      2203016, 103,  1,  8, 15,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - SHR
        #      2203017, 103,  1,  8, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - air flow, cfm
        #      2203018, 103,  1,  8, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - coil entering drybulb
        #      2203019, 103,  1,  8, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - coil entering wetbulb
        #      2203020, 103,  1,  8, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - coil leaving drybulb
        #      2203021, 103,  1,  8, 20,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - coil leaving wetbulb
        #      2203022, 103,  1,  8, 21,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - coil bypass factor
        #      2203023, 103,  1,  8, 22,  1,  1,  1,  0,139,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - chilled water flow, gpm
        #      2203024, 103,  1,  8, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - chilled water entering temp
        #      2203025, 103,  1,  8, 24,  1,  1,  1,  0, 74,    0,  0,  0,  0, 2010   ; Design data for Cooling - chilled water - SYSTEM - chilled water delta T
        #      2203026, 103,  1,  9, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - capacity, btu/hr
        #      2203027, 103,  1,  9, 15,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - SHR
        #      2203028, 103,  1,  9, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - air flow, cfm
        #      2203029, 103,  1,  9, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - coil entering drybulb
        #      2203030, 103,  1,  9, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - coil entering wetbulb
        #      2203031, 103,  1,  9, 21,  1,  1,  1,  0, 22,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - coil bypass factor
        #      2203032, 103,  1,  9, 22,  1,  1,  1,  0,139,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - chilled water flow, gpm
        #      2203033, 103,  1,  9, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Rated data for Cooling - chilled water - SYSTEM - chilled water entering temp

        #      2203301, 103,  1, 58,  9,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - month of peak
        #      2203302, 103,  1, 58, 10,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - day of peak
        #      2203303, 103,  1, 58, 11,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - hour of peak
        #      2203304, 103,  1, 58, 12,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - outdoor DBT at peak
        #      2203305, 103,  1, 58, 13,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - outdoor WBT at peak
        #      2203306, 103,  1, 58, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - capacity, btu/hr
        #      2203307, 103,  1, 58, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - air flow, cfm
        #      2203308, 103,  1, 58, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - coil entering drybulb
        #      2203309, 103,  1, 58, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - coil entering wetbulb
        #      2203310, 103,  1, 58, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - furnace - SYSTEM - coil leaving drybulb
        #      2203311, 103,  1, 59, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design data for Preheat - furnace - SYSTEM - capacity, btu/hr
        #      2203312, 103,  1, 59, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design data for Preheat - furnace - SYSTEM - air flow, cfm
        #      2203313, 103,  1, 59, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - furnace - SYSTEM - coil entering drybulb
        #      2203314, 103,  1, 59, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - furnace - SYSTEM - coil entering wetbulb
        #      2203315, 103,  1, 59, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - furnace - SYSTEM - coil leaving drybulb

        #      2203331, 103,  1, 64,  9,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - month of peak
        #      2203332, 103,  1, 64, 10,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - day of peak
        #      2203333, 103,  1, 64, 11,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - hour of peak
        #      2203334, 103,  1, 64, 12,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - outdoor DBT at peak
        #      2203335, 103,  1, 64, 13,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - outdoor WBT at peak
        #      2203336, 103,  1, 64, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - capacity, btu/hr
        #      2203337, 103,  1, 64, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - air flow, cfm
        #      2203338, 103,  1, 64, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - coil entering drybulb
        #      2203339, 103,  1, 64, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - coil entering wetbulb
        #      2203340, 103,  1, 64, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Heating - electric - SYSTEM - coil leaving drybulb
        #      2203341, 103,  1, 67,  9,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - month of peak
        #      2203342, 103,  1, 67, 10,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - day of peak
        #      2203343, 103,  1, 67, 11,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - hour of peak
        #      2203344, 103,  1, 67, 12,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - outdoor DBT at peak
        #      2203345, 103,  1, 67, 13,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - outdoor WBT at peak
        #      2203346, 103,  1, 67, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - capacity, btu/hr
        #      2203347, 103,  1, 67, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - air flow, cfm
        #      2203348, 103,  1, 67, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - coil entering drybulb
        #      2203349, 103,  1, 67, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - coil entering wetbulb
        #      2203350, 103,  1, 67, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - electric - SYSTEM - coil leaving drybulb

        #      2203382, 103,  1, 76,  9,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - month of peak
        #      2203383, 103,  1, 76, 10,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - day of peak
        #      2203384, 103,  1, 76, 11,  0,  1,  1,  0,  0,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - hour of peak
        #      2203385, 103,  1, 76, 12,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - outdoor DBT at peak
        #      2203386, 103,  1, 76, 13,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - outdoor WBT at peak
        #      2203387, 103,  1, 76, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - capacity, btu/hr
        #      2203388, 103,  1, 76, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - air flow, cfm
        #      2203389, 103,  1, 76, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - coil entering drybulb
        #      2203390, 103,  1, 76, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - coil entering wetbulb
        #      2203391, 103,  1, 76, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - coil leaving drybulb
        #      2203392, 103,  1, 76, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design Day data for Preheat - heat pump air cooled - SYSTEM - outdoor temp
        #      2203393, 103,  1, 77, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - capacity, btu/hr
        #      2203394, 103,  1, 77, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - air flow, cfm
        #      2203395, 103,  1, 77, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - coil entering drybulb
        #      2203396, 103,  1, 77, 18,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - coil entering wetbulb
        #      2203397, 103,  1, 77, 19,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - coil leaving drybulb
        #      2203398, 103,  1, 77, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Design data for Preheat - heat pump air cooled - SYSTEM - outdoor temp
        #      2203399, 103,  1, 78, 14,  1,  1,  1,  0,  4,    0,  0,  0,  0, 2010   ; Rated data for Preheat - heat pump air cooled - SYSTEM - capacity, btu/hr
        #      2203400, 103,  1, 78, 16,  1,  1,  1,  0, 25,    0,  0,  0,  0, 2010   ; Rated data for Preheat - heat pump air cooled - SYSTEM - air flow, cfm
        #      2203401, 103,  1, 78, 17,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Rated data for Preheat - heat pump air cooled - SYSTEM - coil entering drybulb
        #      2203402, 103,  1, 78, 23,  1,  1,  1,  0,  8,    0,  0,  0,  0, 2010   ; Rated data for Preheat - heat pump air cooled - SYSTEM - outdoor temp

        #      2201045,  38,  1,  6,  9,  1,  1,  1,  0, 25, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Supply Airflow
        #      2201046,  38,  1,  6, 10,  1,  1,  1,  0, 25, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Exhaust Airflow
        #      2201047,  38,  1,  6, 11,  1,  1,  1,  0, 28, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Zone Fan Power
        #      2201048,  38,  1,  6, 12,  1,  1,  1,  0, 22, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Minimum Airflow Ratio
        #      2201049,  38,  1,  6, 13,  1,  1,  1,  0, 25, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Outside Airflow
        #      2201050,  38,  1,  6, 14,  1,  1,  1,  0, 64, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Cooling Capacity
        #      2201051,  38,  1,  6, 15,  1,  1,  1,  0, 22, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Sensible Heat Ratio
        #      2201052,  38,  1,  6, 16,  1,  1,  1,  0, 64, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Heat Extraction Rate
        #      2201053,  38,  1,  6, 17,  1,  1,  1,  0, 64, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Heating Capacity
        #      2201054,  38,  1,  6, 18,  1,  1,  1,  0, 64, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Heat Addition Rate
        #      2201055,  38,  1,  6, 19,  1,  1,  1,  0,  1, 2019,  8,  1,  0, 2010   ; HVAC Systems - Design Parameters - Zone Design Data - General - Zone Multiplier

        requests = {
            "Outside Air Ratio": (2201005, self.u_name.encode("utf-8"), b""),
            "Cooling Capacity": (2201006, self.u_name.encode("utf-8"), b""),
            "Heating Capacity": (2201008, self.u_name.encode("utf-8"), b""),
            "Cooling EIR": (2201009, self.u_name.encode("utf-8"), b""),
            "Heating EIR": (2201010, self.u_name.encode("utf-8"), b""),
        }

        if len(self.fan_system["supply_fans"]) > 0:
            requests["Supply Fan - Airflow"] = (
                2201012,
                self.u_name.encode("utf-8"),
                b"",
            )
            requests["Supply Fan - Power"] = (2201014, self.u_name.encode("utf-8"), b"")

        if len(self.fan_system["return_fans"]) > 0:
            requests["Return Fan - Airflow"] = (
                2201023,
                self.u_name.encode("utf-8"),
                b"",
            )

        if self.cooling_system["type"] == "FLUID_LOOP":
            requests[
                "Design Day Cooling - chilled water - SYSTEM - capacity, btu/hr"
            ] = (2203006, self.u_name.encode("utf-8"), b"")
            requests["Design Cooling - chilled water - SYSTEM - capacity, btu/hr"] = (
                2203015,
                self.u_name.encode("utf-8"),
                b"",
            )

        match self.preheat_sys_type:
            case "FLUID_LOOP":
                pass
            case "ELECTRIC_RESISTANCE":
                pass
            case "FURNACE":
                requests["Design Preheat - furnace - SYSTEM - capacity, btu/hr"] = (
                    2203311,
                    self.u_name.encode("utf-8"),
                    b"",
                )

        if self.heat_sys_type == "FLUID_LOOP":
            requests["Design Day Heating - hot water - SYSTEM - capacity, btu/hr"] = (
                2203258,
                self.u_name.encode("utf-8"),
                b"",
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
        if self.keyword_value_pairs.get("TYPE") == "SUM":
            self.omit = True
            return

        heat_type = self.heat_type_map.get(self.keyword_value_pairs.get("HEAT-SOURCE"))

        terminal_system_conditions = (
                self.keyword_value_pairs.get("TYPE") in ["FC", "IU"]
                and heat_type == "FLUID_LOOP"
        )

        if terminal_system_conditions:
            for attr in dir(self):
                if attr.startswith("terminals_"):
                    pass

        else:
            self.system_data_structure["id"] = self.u_name
            self.system_data_structure["fan_system"] = self.fan_system
            self.system_data_structure["heating_system"] = self.heating_system
            self.system_data_structure["cooling_system"] = self.cooling_system
            self.system_data_structure["preheat_system"] = self.preheat_system

            for attr in dir(self):
                if attr.startswith("fan_sys_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.fan_system[attr.split("fan_sys_")[1]] = value
                elif attr.startswith("heat_sys_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.heating_system[attr.split("heat_sys_")[1]] = value
                elif attr.startswith("cool_sys_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.cooling_system[attr.split("cool_sys_")[1]] = value
                elif attr.startswith("preheat_sys_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.preheat_system[attr.split("preheat_sys_")[1]] = value
                elif attr.startswith("fan_") and not attr[4:7] == "sys":
                    pass
                elif attr.startswith("air_econ_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.fan_sys_air_economizer[attr.split("air_econ_")[1]] = value
                elif attr.startswith("air_energy_recovery_"):
                    value = getattr(self, attr, None)
                    if value is not None:
                        self.fan_sys_air_energy_recovery[attr.strip("air_energy_recovery_")] = value

    def insert_to_rpd(self, rmd):
        """Insert system data structure into the rpd data structure."""
        if self.omit:
            return
        self.parent_building_segment.hvac_systems.append(self.system_data_structure)

    def populate_fan_system(self):
        self.fan_sys_id = self.u_name + " FanSys"
        self.fan_sys_fan_control = self.supply_fan_map.get(
            self.keyword_value_pairs.get("TYPE")
        )
        self.fan_sys_operation_during_unocc = self.unocc_fan_operation_map.get(
            self.keyword_value_pairs.get("NIGHT-CYCLE-CTRL")
        )
        self.fan_sys_dcv_control = self.dcv_map.get(
            self.keyword_value_pairs.get("MIN-OA-METHOD")
        )

    def populate_heating_system(self):
        self.heat_sys_id = self.u_name + " HeatSys"
        self.heat_sys_type = self.heat_type_map.get(
            self.keyword_value_pairs.get("HEAT-SOURCE")
        )

    def populate_cooling_system(self):
        self.cool_sys_id = self.u_name + " CoolSys"
        self.cool_sys_type = self.system_cooling_type_map.get(
            self.keyword_value_pairs.get("TYPE")
        )
        sizing_ratio = self.keyword_value_pairs.get("SIZING-RATIO")
        cool_sizing_ratio = self.keyword_value_pairs.get("COOL-SIZING-RATI")
        self.cool_sys_oversizing_factor = (
                float(sizing_ratio) * float(cool_sizing_ratio)
        ) if sizing_ratio is not None and cool_sizing_ratio is not None else None

    def populate_preheat_system(self):
        self.preheat_sys_id = self.u_name + " PreheatSys"
        self.preheat_sys_type = self.heat_type_map.get(
            self.keyword_value_pairs.get("PREHEAT-SOURCE")
        )

    def populate_fans(self):
        pass

    def populate_air_economizer(self):
        self.fan_sys_id = self.u_name + " AirEconomizer"
        self.air_econ_type = self.economizer_map.get(
            self.keyword_value_pairs.get("OA-CONTROL")
        )
        self.air_econ_high_limit_shutoff_temperature = self.keyword_value_pairs.get(
            "ECONO-LIMIT-T"
        )
        if self.air_econ_high_limit_shutoff_temperature is not None:
            self.air_econ_high_limit_shutoff_temperature = float(self.air_econ_high_limit_shutoff_temperature)

    def populate_air_energy_recovery(self):
        self.air_econ_id = self.u_name + " AirEnergyRecovery"
        recover_exhaust = self.keyword_value_pairs.get("RECOVER-EXHAUST")
        recovery_type = self.recovery_type_map.get(
            self.keyword_value_pairs.get("ERV-RECOVER-TYPE")
        )
        self.has_recovery_map.update(
            {
                "RELIEF-ONLY": recovery_type,
                "EXHAUST-ONLY": recovery_type,
                "RELIEF+EXHAUST": recovery_type,
                "YES": recovery_type,
            }
        )

        self.air_energy_recovery_type = self.has_recovery_map.get(
            recover_exhaust
        )
        self.air_energy_recovery_operation = self.er_operation_map.get(
            self.keyword_value_pairs.get("ERV-RUN-CTRL")
        )
        self.air_energy_recovery_sat_control = self.er_sat_control_map.get(
            self.keyword_value_pairs.get("ERV-TEMP-CTRL")
        )

    def populate_system_terminals(self):
        pass

    def populate_terminal_system(self):
        pass
