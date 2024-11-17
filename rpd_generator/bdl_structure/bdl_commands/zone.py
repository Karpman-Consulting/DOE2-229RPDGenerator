from rpd_generator.bdl_structure.child_node import ChildNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


HeatingSourceOptions = SchemaEnums.schema_enums["HeatingSourceOptions"]
CoolingSourceOptions = SchemaEnums.schema_enums["CoolingSourceOptions"]
TerminalOptions = SchemaEnums.schema_enums["TerminalOptions"]
TerminalFanConfigurationOptions = SchemaEnums.schema_enums[
    "TerminalFanConfigurationOptions"
]
FanSystemSupplyFanControlOptions = SchemaEnums.schema_enums[
    "FanSystemSupplyFanControlOptions"
]
FanSpecificationMethodOptions = SchemaEnums.schema_enums[
    "FanSpecificationMethodOptions"
]


BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ZoneKeywords = BDLEnums.bdl_enums["ZoneKeywords"]
BDL_SystemKeywords = BDLEnums.bdl_enums["SystemKeywords"]
BDL_SystemTypes = BDLEnums.bdl_enums["SystemTypes"]
BDL_ZoneHeatSourceOptions = BDLEnums.bdl_enums["ZoneHeatSourceOptions"]
BDL_TerminalTypes = BDLEnums.bdl_enums["TerminalTypes"]
BDL_BaseboardControlOptions = BDLEnums.bdl_enums["BaseboardControlOptions"]
BDL_SystemMinimumOutdoorAirControlOptions = BDLEnums.bdl_enums[
    "SystemMinimumOutdoorAirControlOptions"
]
BDL_DOASAttachedToOptions = BDLEnums.bdl_enums["DOASAttachedToOptions"]
BDL_ZoneFanRunOptions = BDLEnums.bdl_enums["ZoneFanRunOptions"]
BDL_ZoneFanControlOptions = BDLEnums.bdl_enums["ZoneFanControlOptions"]
BDL_ZoneInductionSourceOptions = BDLEnums.bdl_enums["ZoneInductionSourceOptions"]
BDL_OutputCoolingTypes = BDLEnums.bdl_enums["OutputCoolingTypes"]
BDL_OutputHeatingTypes = BDLEnums.bdl_enums["OutputHeatingTypes"]
BDL_ZoneOAMethodsOptions = BDLEnums.bdl_enums["ZoneOAMethodOptions"]
BDL_SpaceKeywords = BDLEnums.bdl_enums["SpaceKeywords"]
BDL_MinFlowControlOptions = BDLEnums.bdl_enums["MinFlowControlOptions"]


class Zone(ChildNode):
    """Zone object in the tree."""

    bdl_command = BDL_Commands.ZONE

    heat_source_map = {
        BDL_ZoneHeatSourceOptions.NONE: None,
        BDL_ZoneHeatSourceOptions.ELECTRIC: HeatingSourceOptions.ELECTRIC,
        BDL_ZoneHeatSourceOptions.HOT_WATER: HeatingSourceOptions.HOT_WATER,
        BDL_ZoneHeatSourceOptions.FURNACE: HeatingSourceOptions.OTHER,
        BDL_ZoneHeatSourceOptions.DHW_LOOP: HeatingSourceOptions.OTHER,
        BDL_ZoneHeatSourceOptions.STEAM: HeatingSourceOptions.OTHER,
        BDL_ZoneHeatSourceOptions.HEAT_PUMP: HeatingSourceOptions.OTHER,
    }

    is_fan_first_stage_map = {
        BDL_ZoneFanRunOptions.HEATING_ONLY: False,
        BDL_ZoneFanRunOptions.HEATING_DEADBAND: True,
        BDL_ZoneFanRunOptions.CONTINUOUS: True,
        BDL_ZoneFanRunOptions.HEATING_COOLING: False,
    }

    terminal_fan_type_map = {
        BDL_ZoneFanControlOptions.CONSTANT_VOLUME: TerminalOptions.CONSTANT_AIR_VOLUME,
        BDL_ZoneFanControlOptions.VARIABLE_VOLUME: TerminalOptions.VARIABLE_AIR_VOLUME,
    }

    def __init__(self, u_name, parent, rmd):
        super().__init__(u_name, parent, rmd)
        self.rmd.zone_names.append(u_name)

        # On initialization the parent building segment is not known. It will be set in the GUI.
        self.parent_building_segment = self.get_obj("Default Building Segment")

        self.zone_data_structure = {}

        # data elements with children
        self.spaces = []
        self.surfaces = []
        self.terminals = []
        self.zonal_exhaust_fan = {}
        self.infiltration = {}

        # data elements with no children
        self.floor_name = None
        self.volume = None
        self.conditioning_type = None
        self.design_thermostat_cooling_setpoint = None
        self.thermostat_cooling_setpoint_schedule = None
        self.design_thermostat_heating_setpoint = None
        self.thermostat_heating_setpoint_schedule = None
        self.minimum_humidity_setpoint_schedule = None
        self.maximum_humidity_setpoint_schedule = None
        self.served_by_service_water_heating_system = None
        self.transfer_airflow_rate = None
        self.transfer_airflow_source_zone = None
        self.exhaust_airflow_rate_multiplier_schedule = None
        self.makeup_airflow_rate = None
        self.non_mechanical_cooling_fan_power = None
        self.non_mechanical_cooling_fan_airflow = None
        self.air_distribution_effectiveness = None
        self.aggregation_factor = None

        # terminal data elements as a list of [Main Terminal, Baseboard Terminal, DOAS Terminal]
        self.terminals_id: list = [None, None, None]
        self.terminals_reporting_name: list = [None, None, None]
        self.terminals_notes: list = [None, None, None]
        self.terminals_type: list = [None, None, None]
        self.terminals_served_by_heating_ventilating_air_conditioning_system: list = [
            None,
            None,
            None,
        ]
        self.terminals_heating_source: list = [None, None, None]
        self.terminals_heating_from_loop: list = [None, None, None]
        self.terminals_cooling_source: list = [None, None, None]
        self.terminals_cooling_from_loop: list = [None, None, None]
        self.terminals_fan: list = [None, None, None]
        self.terminals_fan_configuration: list = [None, None, None]
        self.terminals_primary_airflow: list = [None, None, None]
        self.terminals_secondary_airflow: list = [None, None, None]
        self.terminals_max_heating_airflow: list = [None, None, None]
        self.terminals_supply_design_heating_setpoint_temperature: list = [
            None,
            None,
            None,
        ]
        self.terminals_supply_design_cooling_setpoint_temperature: list = [
            None,
            None,
            None,
        ]
        self.terminals_temperature_control: list = [None, None, None]
        self.terminals_minimum_airflow: list = [None, None, None]
        self.terminals_minimum_outdoor_airflow: list = [None, None, None]
        self.terminals_minimum_outdoor_airflow_multiplier_schedule: list = [
            None,
            None,
            None,
        ]
        self.terminals_heating_capacity: list = [None, None, None]
        self.terminals_cooling_capacity: list = [None, None, None]
        self.terminals_is_supply_ducted: list = [None, None, None]
        self.terminals_has_demand_control_ventilation: list = [None, None, None]
        self.terminals_is_fan_first_stage_heat: list = [None, None, None]

        # terminal fan data elements, maximum of 1 terminal fan per zone
        self.terminal_fan_id = None
        self.terminal_fan_reporting_name = None
        self.terminal_fan_notes = None
        self.terminal_fan_design_airflow = None
        self.terminal_fan_is_airflow_sized_based_on_design_day = None
        self.terminal_fan_specification_method = None
        self.terminal_fan_design_electric_power = None
        self.terminal_fan_design_pressure_rise = None
        self.terminal_fan_motor_efficiency = None
        self.terminal_fan_total_efficiency = None
        self.terminal_fan_output_validation_points = []

        # zonal exhaust fan data elements, maximum of 1 zonal exhaust fan per zone
        self.zone_exhaust_fan_id = None
        self.zone_exhaust_fan_reporting_name = None
        self.zone_exhaust_fan_notes = None
        self.zone_exhaust_fan_design_airflow = None
        self.zone_exhaust_fan_is_airflow_sized_based_on_design_day = None
        self.zone_exhaust_fan_specification_method = None
        self.zone_exhaust_fan_design_electric_power = None
        self.zone_exhaust_fan_design_pressure_rise = None
        self.zone_exhaust_fan_total_efficiency = None
        self.zone_exhaust_fan_output_validation_points = []

        # infiltration data elements
        self.infil_id = None
        self.infil_reporting_name = None
        self.infil_notes = None
        self.infil_modeling_method = None
        self.infil_algorithm_name = None
        self.infil_measured_air_leakage_rate = None
        self.infil_flow_rate = None
        self.infil_multiplier_schedule = None

    def __repr__(self):
        return f"Zone(u_name='{self.u_name}', parent='{self.parent}')"

    def populate_data_elements(self):
        """Populate data elements for zone object."""
        has_baseboard = self.get_inp(BDL_ZoneKeywords.BASEBOARD_CTRL) not in [
            None,
            BDL_BaseboardControlOptions.NONE,
        ]
        has_doas = bool(self.parent.get_inp(BDL_SystemKeywords.DOA_SYSTEM))
        is_iu = self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE) in [
            BDL_TerminalTypes.TERMINAL_IU,
            BDL_TerminalTypes.CEILING_IU,
            BDL_TerminalTypes.SERIES_PIU,
            BDL_TerminalTypes.PARALLEL_PIU,
        ]

        self.design_thermostat_cooling_setpoint = self.try_float(
            self.get_inp(BDL_ZoneKeywords.DESIGN_COOL_T)
        )
        self.thermostat_cooling_setpoint_schedule = self.get_inp(
            BDL_ZoneKeywords.COOL_TEMP_SCH
        )
        self.design_thermostat_heating_setpoint = self.try_float(
            self.get_inp(BDL_ZoneKeywords.DESIGN_HEAT_T)
        )
        self.thermostat_heating_setpoint_schedule = self.get_inp(
            BDL_ZoneKeywords.HEAT_TEMP_SCH
        )
        self.exhaust_airflow_rate_multiplier_schedule = self.get_inp(
            BDL_ZoneKeywords.EXHAUST_FAN_SCH
        )

        # if the zone is served by a SUM system don't populate the data elements below
        if self.parent.get_inp(BDL_SystemKeywords.TYPE) == BDL_SystemTypes.SUM:
            return

        requests = self.get_output_requests()
        output_data = self.get_output_data(requests)
        for key in [
            "HVAC Systems - Design Parameters - Zone Design Data - General - Heating Capacity",
            "HVAC Systems - Design Parameters - Zone Design Data - General - Cooling Capacity",
        ]:
            if key in output_data:
                output_data[key] = self.try_convert_units(
                    output_data[key], "kBtu/hr", "Btu/hr"
                )

        supply_airflow = output_data.get(
            "HVAC Systems - Design Parameters - Zone Design Data - General - Supply Airflow"
        )
        minimum_airflow_ratio = output_data.get(
            "HVAC Systems - Design Parameters - Zone Design Data - General - Minimum Airflow Ratio"
        )
        minimum_outdoor_airflow = output_data.get(
            "HVAC Systems - Design Parameters - Zone Design Data - General - Outside Airflow"
        )
        exhaust_airflow = self.try_float(self.get_inp(BDL_ZoneKeywords.EXHAUST_FLOW))

        # Populate MainTerminal data elements
        self.terminals_id[0] = self.u_name + " MainTerminal"

        # Populate terminals_has_demand_control_ventilation
        # DCV is not modeled when a zone has the OUTSIDE-AIR-FLOW keyword populated or when OA-FLOW/PER is not populated.
        cfm_per_pps = self.get_inp(BDL_ZoneKeywords.OA_FLOW_PER)
        cfm_per_pps = float(cfm_per_pps) if cfm_per_pps is not None else None
        if cfm_per_pps and self.get_inp(BDL_ZoneKeywords.OUTSIDE_AIR_FLOW) is None:
            # If MAX-OCC-OR-AREA was input as the ZONE-OA-METHOD then it will need to be determined whether the OA CFM per person rate is
            # high enough such that it is greater than the OA CFM/sf and the ACH rate during max occupancy periods. If it is not then DCV will not be modeled.
            # Create boolean for if the occupancy based cfm is greater enough for dcv to be modeled.
            if (
                self.parent.get_inp(BDL_SystemKeywords.ZONE_OA_METHOD)
                == BDL_ZoneOAMethodsOptions.MAX_OCC_OR_AREA
            ):
                # Get the space occupancy schedule and number of occupants so that cfm per pps can be converted to cfm for comparison
                space = self.get_obj(self.get_inp(BDL_ZoneKeywords.SPACE))
                spc_occ_sch = space.get_obj(
                    space.get_inp(BDL_SpaceKeywords.PEOPLE_SCHEDULE)
                )
                spc_num_pp = float(space.get_inp(BDL_SpaceKeywords.NUMBER_OF_PEOPLE))
                occ_cfm = cfm_per_pps * spc_num_pp * max(spc_occ_sch.hourly_values)
                # Assess whether ACH or CFM per sf have been populated and if so calculate the total cfm for each for comparison
                ach = self.get_inp(BDL_ZoneKeywords.OA_CHANGES)
                ach = float(ach) if ach is not None else None
                cfm_sf = self.get_inp(BDL_ZoneKeywords.OA_FLOW_AREA)
                cfm_sf = float(cfm_sf) if cfm_sf is not None else None
                ach_cfm = (
                    (float(space.get_inp(BDL_SpaceKeywords.VOLUME)) * ach) / 60
                    if ach is not None
                    else 0
                )
                sf_cfm = (
                    float(space.get_inp(BDL_SpaceKeywords.AREA)) * cfm_sf
                    if cfm_sf is not None
                    else 0
                )
                if occ_cfm <= ach_cfm or occ_cfm <= sf_cfm:
                    occ_cfm_allows_dcv_to_be_modeled = False
                else:
                    occ_cfm_allows_dcv_to_be_modeled = True
            else:
                occ_cfm_allows_dcv_to_be_modeled = True

            # Determine if the system associated with the zone has active model inputs associated with the terminal unit. The system
            # types listed below do
            system_types_with_terminal_inputs_lst = [
                BDL_SystemTypes.MZS,
                BDL_SystemTypes.DDS,
                BDL_SystemTypes.SZCI,
                BDL_SystemTypes.IU,
                BDL_SystemTypes.VAVS,
                BDL_SystemTypes.RHFS,
                BDL_SystemTypes.RHFS,
                BDL_SystemTypes.HVSYS,
                BDL_SystemTypes.CBVAV,
                BDL_SystemTypes.PMZS,
                BDL_SystemTypes.PVAVS,
                BDL_SystemTypes.PIU,
                BDL_SystemTypes.FNSYS,
                BDL_SystemTypes.PTGSD,
            ]

            zone_is_attached_to_sys_with_terminal_inputs = (
                self.parent.get_inp(BDL_SystemKeywords.TYPE)
                in system_types_with_terminal_inputs_lst
            )

            # Check if there is a Min-AIR-SCH populated for the system. Sent chat to Jackson on options here. Maybe need to account for
            # scenarios where DCV is modeled anyway like for systems where DCV is modeled at the terminal unit where it still appears to
            # model DCV unless there are schedules like this defined at the terminal
            min_oa_sch = self.parent.get_obj(
                self.parent.get_inp(BDL_SystemKeywords.MIN_AIR_SCH)
            )
            fan_sch = self.parent.get_obj(
                self.parent.get_inp(BDL_SystemKeywords.FAN_SCHEDULE)
            )
            terminal_flow_control_defined_as_dcv_lst = [
                BDL_MinFlowControlOptions.DCV_RESET_DOWN,
                BDL_MinFlowControlOptions.DCV_RESET_UP_DOWN,
            ]
            terminal_min_flow_control = self.get_inp(BDL_ZoneKeywords.MIN_FLOW_CTRL)
            if min_oa_sch is not None and (
                not zone_is_attached_to_sys_with_terminal_inputs
                or (
                    zone_is_attached_to_sys_with_terminal_inputs
                    and terminal_min_flow_control
                    not in terminal_flow_control_defined_as_dcv_lst
                )
            ):
                dcv_never_takes_precedence_due_to_min_air_sch = (
                    False
                    if min_oa_sch is None
                    else not any(
                        min_oa_sch.hourly_values[i] == -999
                        for i in range(len(fan_sch.hourly_values))
                        if fan_sch.hourly_values[i] == 1
                    )
                )
            else:
                dcv_never_takes_precedence_due_to_min_air_sch = False

            # For units with terminal inputs if MIN-FLOW-SCH, CMIN-FLOW-SCH or HMIN-FLOW-SCH are specified,
            # their hourly specified values will always be used, for the appropriate VAV box minimum flow setting, unless the hourly scheduled value is -999
            system_DCV_control_min_oa_method_lst = [
                BDL_SystemMinimumOutdoorAirControlOptions.DCV_RETURN_SENSOR,
                BDL_SystemMinimumOutdoorAirControlOptions.DCV_ZONE_SENSORS,
            ]
            min_oa_method = self.parent.get_inp(BDL_SystemKeywords.MIN_OA_METHOD)
            if (
                zone_is_attached_to_sys_with_terminal_inputs
                and terminal_min_flow_control
                in terminal_flow_control_defined_as_dcv_lst
            ):
                terminal_schedules = [
                    self.get_obj(self.get_inp(BDL_ZoneKeywords.MIN_FLOW_SCH)),
                    self.get_obj(self.get_inp(BDL_ZoneKeywords.CMIN_FLOW_SCH)),
                    self.get_obj(self.get_inp(BDL_ZoneKeywords.HMIN_FLOW_SCH)),
                ]

                if any(terminal_schedules):
                    lists = [sch for sch in terminal_schedules if sch is not None]

                    for i in range(len(fan_sch.hourly_values)):
                        if fan_sch.hourly_values[i] == 1:
                            if (
                                all(lst.hourly_values[i] == -999 for lst in lists)
                                or min_oa_method in system_DCV_control_min_oa_method_lst
                            ):
                                dcv_never_takes_precedence_due_to_min_air_sch = False
                                break
                        if fan_sch is None:
                            if (
                                all(lst.hourly_values[i] == -999 for lst in lists)
                                or min_oa_method in system_DCV_control_min_oa_method_lst
                            ):
                                dcv_never_takes_precedence_due_to_min_air_sch = False
                                break
                    else:
                        dcv_never_takes_precedence_due_to_min_air_sch = True
                else:
                    dcv_never_takes_precedence_due_to_min_air_sch = False
            # Check if DCV was modeled, there are some caveats for DOAS hence the variable is named likely_has_dcv
            dcv_condition = (
                not dcv_never_takes_precedence_due_to_min_air_sch
                and occ_cfm_allows_dcv_to_be_modeled
                and (
                    (
                        zone_is_attached_to_sys_with_terminal_inputs
                        and terminal_min_flow_control
                        in terminal_flow_control_defined_as_dcv_lst
                    )
                    or min_oa_method in system_DCV_control_min_oa_method_lst
                )
            )
            likely_has_dcv = dcv_condition
        else:
            likely_has_dcv = False

        # Only populate MainTerminal Fan data elements here if the parent system is_terminal is True
        # (Systems that allow PIU terminals cannot be terminal)
        if self.parent.is_terminal:
            if self.parent.is_zonal_system:
                self.terminal_fan_id = self.u_name + " MainTerminal Fan"
                self.terminal_fan_design_airflow = output_data.get(
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Supply Airflow"
                )
                self.terminal_fan_design_electric_power = output_data.get(
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Fan Power"
                )
                self.terminal_fan_specification_method = (
                    FanSpecificationMethodOptions.SIMPLE
                )

            else:  # Parent is not a zonal system (i.e. not FC, HP, UHT, UVT, PTAC)
                self.terminal_fan_id = self.u_name + " MainTerminal Fan"
                self.terminal_fan_design_airflow = output_data.get(
                    "Supply Fan - Airflow"
                )
                self.terminal_fan_design_electric_power = output_data.get(
                    "Supply Fan - Power"
                )
                self.terminal_fan_specification_method = (
                    FanSpecificationMethodOptions.DETAILED
                    if self.parent.get_inp(BDL_SystemKeywords.SUPPLY_STATIC) is not None
                    else FanSpecificationMethodOptions.SIMPLE
                )
                self.terminal_fan_design_pressure_rise = self.try_float(
                    self.parent.get_inp(BDL_SystemKeywords.SUPPLY_STATIC)
                )
                self.terminal_fan_motor_efficiency = self.try_float(
                    self.parent.get_inp(BDL_SystemKeywords.SUPPLY_MTR_EFF)
                )
                supply_mech_eff = self.try_float(
                    self.parent.get_inp(BDL_SystemKeywords.SUPPLY_MECH_EFF)
                )
                if self.terminal_fan_motor_efficiency and supply_mech_eff:
                    self.terminal_fan_total_efficiency = (
                        self.terminal_fan_motor_efficiency * supply_mech_eff
                    )

            if self.parent.get_inp(BDL_SystemKeywords.SUPPLY_FLOW) is not None:
                self.terminal_fan_is_airflow_sized_based_on_design_day = False
            if self.terminal_fan_is_airflow_sized_based_on_design_day is None:
                self.terminal_fan_is_airflow_sized_based_on_design_day = (
                    # If the zone has assigned flow rates, the fan is not sized based on design day
                    not (
                        self.get_inp(BDL_ZoneKeywords.ASSIGNED_FLOW)
                        or self.get_inp(BDL_ZoneKeywords.HASSIGNED_FLOW)
                        or self.get_inp(BDL_ZoneKeywords.FLOW_AREA)
                        or self.get_inp(BDL_ZoneKeywords.HFLOW_AREA)
                        or self.get_inp(BDL_ZoneKeywords.AIR_CHANGES_HR)
                        or self.get_inp(BDL_ZoneKeywords.HAIR_CHANGES_HR)
                        or self.get_inp(BDL_ZoneKeywords.MIN_FLOW_AREA)
                        or self.get_inp(BDL_ZoneKeywords.HMIN_FLOW_AREA)
                    )
                )

            # Terminal Heating/Cooling Capacity uses the same output_data keywords whether the parent is zonal or not
            self.terminals_heating_capacity[0] = self.try_abs(
                self.try_float(self.parent.get_inp(BDL_SystemKeywords.HEATING_CAPACITY))
            )
            if not self.terminals_heating_capacity[0]:
                self.terminals_heating_capacity[0] = self.try_abs(
                    output_data.get("Rated Heating capacity")
                )
            if not self.terminals_heating_capacity[0]:
                self.terminals_heating_capacity[0] = self.try_abs(
                    output_data.get("Heating Capacity")
                )
            self.terminals_cooling_capacity[0] = self.try_abs(
                self.try_float(self.parent.get_inp(BDL_SystemKeywords.COOLING_CAPACITY))
            )
            if not self.terminals_cooling_capacity[0]:
                self.terminals_cooling_capacity[0] = self.try_abs(
                    output_data.get("Rated Cooling capacity")
                )
            if not self.terminals_cooling_capacity[0]:
                self.terminals_cooling_capacity[0] = self.try_abs(
                    output_data.get("Cooling Capacity")
                )
            self.terminals_cooling_source[0] = (
                CoolingSourceOptions.CHILLED_WATER
                if self.terminals_cooling_capacity[0]
                else None
            )
            self.terminals_fan_configuration[0] = TerminalFanConfigurationOptions.SERIES

        if not self.parent.is_terminal:
            self.terminals_served_by_heating_ventilating_air_conditioning_system[0] = (
                self.parent.u_name
            )
            self.terminals_heating_source[0] = self.heat_source_map.get(
                self.parent.get_inp(BDL_SystemKeywords.ZONE_HEAT_SOURCE)
            )
            self.terminals_heating_from_loop[0] = self.get_inp(BDL_ZoneKeywords.HW_LOOP)
            self.terminals_heating_capacity[0] = self.try_abs(
                output_data.get(
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Heating Capacity"
                )
            )
            self.terminals_cooling_capacity[0] = output_data.get(
                "HVAC Systems - Design Parameters - Zone Design Data - General - Cooling Capacity"
            )
            self.terminals_cooling_source[0] = (
                CoolingSourceOptions.CHILLED_WATER
                if self.terminals_cooling_capacity[0]
                else None
            )
            if supply_airflow is not None and minimum_airflow_ratio is not None:
                self.terminals_minimum_airflow[0] = (
                    supply_airflow * minimum_airflow_ratio
                )

        if is_iu:
            induct_source = self.get_inp(BDL_ZoneKeywords.INDUCED_AIR_SRC)
            piu_fan_flow = output_data.get(
                "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Fan Flow"
            )
            piu_fan_kw = output_data.get(
                "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Fan kW"
            )
            piu_cd_flow = output_data.get(
                "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Cold Deck Flow"
            )
            piu_cd_min_airflow_ratio = output_data.get(
                "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Cold Deck Minimum Airflow Ratio"
            )

            if induct_source == BDL_ZoneInductionSourceOptions.SUPPLY_AIR:
                self.terminals_primary_airflow[0] = supply_airflow
                self.terminals_secondary_airflow[0] = 0
            elif (
                self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE)
                == BDL_TerminalTypes.SERIES_PIU
            ):
                self.terminals_primary_airflow[0] = piu_cd_flow
                if (
                    self.terminals_primary_airflow[0]
                    and piu_fan_flow
                    and piu_cd_min_airflow_ratio
                ):
                    self.terminals_secondary_airflow[0] = (
                        piu_fan_flow
                        - self.terminals_primary_airflow[0] * piu_cd_min_airflow_ratio
                    )
                self.terminals_fan_configuration[0] = (
                    TerminalFanConfigurationOptions.SERIES
                )
            else:
                self.terminals_primary_airflow[0] = piu_cd_flow
                self.terminals_secondary_airflow[0] = piu_fan_flow

            # Only populate MainTerminal Fan data elements here if the zone TERMINAL-TYPE is SERIES-PIU or PARALLEL-PIU
            if self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE) in [
                BDL_TerminalTypes.SERIES_PIU,
                BDL_TerminalTypes.PARALLEL_PIU,
            ]:
                self.terminal_fan_id = self.u_name + " MainTerminal Fan"
                self.terminal_fan_design_airflow = piu_fan_flow
                self.terminals_is_fan_first_stage_heat[0] = (
                    self.is_fan_first_stage_map.get(
                        self.get_inp(BDL_ZoneKeywords.ZONE_FAN_RUN)
                    )
                )
                if self.get_inp(BDL_ZoneKeywords.ZONE_FAN_FLOW):
                    self.terminal_fan_is_airflow_sized_based_on_design_day = False
                self.terminal_fan_specification_method = (
                    FanSpecificationMethodOptions.SIMPLE
                )
                self.terminal_fan_design_electric_power = piu_fan_kw
                self.terminals_type[0] = self.terminal_fan_type_map.get(
                    self.get_inp(BDL_ZoneKeywords.ZONE_FAN_CTRL)
                )
                self.terminals_fan_configuration[0] = (
                    self.terminals_fan_configuration[0]
                    or TerminalFanConfigurationOptions.PARALLEL
                )

        else:
            self.terminals_primary_airflow[0] = supply_airflow
            self.terminals_secondary_airflow[0] = 0

        # Populate DOAS Terminal data elements if applicable
        if has_doas:
            doas_system = self.get_obj(
                self.parent.get_inp(BDL_SystemKeywords.DOA_SYSTEM)
            )
            self.terminals_id[2] = self.u_name + " DOASTerminal"
            self.terminals_cooling_capacity[2] = 0.0
            self.terminals_heating_capacity[2] = 0.0
            self.terminals_minimum_outdoor_airflow[2] = minimum_outdoor_airflow
            self.terminals_minimum_outdoor_airflow_multiplier_schedule[2] = (
                self.get_inp(BDL_ZoneKeywords.MIN_AIR_SCH)
            )
            self.terminals_primary_airflow[2] = minimum_outdoor_airflow
            self.terminals_minimum_airflow[2] = minimum_outdoor_airflow
            if (
                doas_system
                and doas_system.fan_sys_fan_control
                == FanSystemSupplyFanControlOptions.CONSTANT
                or self.get_inp(BDL_ZoneKeywords.MIN_FLOW_RATIO) == 1
            ):
                self.terminals_type[2] = TerminalOptions.CONSTANT_AIR_VOLUME
            # TODO: Account for zone minimum air flow schedule(s)
            else:
                self.terminals_type[2] = TerminalOptions.VARIABLE_AIR_VOLUME
            # Special condition for DOAS attached to conditioned zone where the terminal DCV parameters are ignored.
            doas_attached_to = self.parent.get_inp(BDL_SystemKeywords.DOAS_ATTACHED_TO)
            is_attached_to_conditioned_zone = (
                doas_attached_to == BDL_DOASAttachedToOptions.CONDITIONED_ZONES
            )
            min_oa_method = self.parent.get_inp(BDL_SystemKeywords.MIN_OA_METHOD)

            self.terminals_has_demand_control_ventilation[2] = likely_has_dcv and (
                min_oa_method in system_DCV_control_min_oa_method_lst
                or not is_attached_to_conditioned_zone
            )
            self.terminals_has_demand_control_ventilation[0] = (
                not is_attached_to_conditioned_zone and likely_has_dcv
            )

        else:
            self.terminals_minimum_outdoor_airflow[0] = minimum_outdoor_airflow
            self.terminals_minimum_outdoor_airflow_multiplier_schedule[0] = (
                self.get_inp(BDL_ZoneKeywords.MIN_AIR_SCH)
            )
            self.terminals_has_demand_control_ventilation[0] = likely_has_dcv

        # Populate Baseboard Terminal data elements if applicable
        if has_baseboard:
            self.terminals_id[1] = self.u_name + " BaseboardTerminal"
            self.terminals_type[1] = TerminalOptions.BASEBOARD
            self.terminals_is_supply_ducted[1] = False
            self.terminals_has_demand_control_ventilation[1] = False
            self.terminals_cooling_capacity[1] = 0.0
            self.terminals_heating_source[1] = self.heat_source_map.get(
                self.get_inp(BDL_ZoneKeywords.BASEBOARD_SOURCE)
            )
            self.terminals_heating_from_loop[1] = self.parent.get_inp(
                BDL_SystemKeywords.BBRD_LOOP
            )
            self.terminals_heating_capacity[1] = self.try_abs(
                self.try_float(self.get_inp(BDL_ZoneKeywords.BASEBOARD_RATING))
            )
            self.terminals_has_demand_control_ventilation[1] = False

        if exhaust_airflow is not None and exhaust_airflow > 0:
            self.zone_exhaust_fan_id = self.u_name + " EF"
            self.zone_exhaust_fan_design_airflow = exhaust_airflow
            self.zone_exhaust_fan_is_airflow_sized_based_on_design_day = False
            if self.get_inp(BDL_ZoneKeywords.EXHAUST_STATIC) is not None:
                zone_fan_power = output_data.get(
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Fan Power"
                )
                self.zone_exhaust_fan_specification_method = (
                    FanSpecificationMethodOptions.DETAILED
                )
                self.zone_exhaust_fan_design_pressure_rise = self.try_float(
                    self.get_inp(BDL_ZoneKeywords.EXHAUST_STATIC)
                )
                self.zone_exhaust_fan_total_efficiency = self.try_float(
                    self.get_inp(BDL_ZoneKeywords.EXHAUST_EFF)
                )
                self.zone_exhaust_fan_design_electric_power = (
                    None
                    if zone_fan_power is None
                    else (
                        zone_fan_power
                        if self.terminal_fan_design_electric_power is None
                        else zone_fan_power - self.terminal_fan_design_electric_power
                    )
                )
            else:
                self.zone_exhaust_fan_specification_method = (
                    FanSpecificationMethodOptions.SIMPLE
                )
                zone_ef_power_per_flow = self.try_float(
                    self.get_inp(BDL_ZoneKeywords.EXHAUST_KW_FLOW)
                )
                if zone_ef_power_per_flow:
                    self.zone_exhaust_fan_design_electric_power = (
                        zone_ef_power_per_flow * exhaust_airflow
                    )
        return

    def populate_data_group(self):
        """Populate schema structure for zone object."""
        # Populate the terminals data structure
        self.terminals = self.populate_data_group_with_prefix("terminals_")

        # Populate the zonal exhaust fan data structure
        zonal_exhaust_fan_data = self.populate_data_group_with_prefix(
            "zone_exhaust_fan_"
        )
        self.zonal_exhaust_fan = (
            zonal_exhaust_fan_data[0] if zonal_exhaust_fan_data else {}
        )

        # Populate the infiltration data structure
        infiltration_data = self.populate_data_group_with_prefix("infil_")
        self.infiltration = infiltration_data[0] if infiltration_data else {}

        self.zone_data_structure = {
            "id": self.u_name,
            "spaces": self.spaces,
            "surfaces": self.surfaces,
            "terminals": self.terminals,
            "zonal_exhaust_fan": self.zonal_exhaust_fan,
            "infiltration": self.infiltration,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "floor_name",
            "volume",
            "conditioning_type",
            "design_thermostat_cooling_setpoint",
            "thermostat_cooling_setpoint_schedule",
            "design_thermostat_heating_setpoint",
            "thermostat_heating_setpoint_schedule",
            "minimum_humidity_setpoint_schedule",
            "maximum_humidity_setpoint_schedule",
            "served_by_service_water_heating_system",
            "transfer_airflow_rate",
            "transfer_airflow_source_zone",
            "zonal_exhaust_flow",
            "exhaust_airflow_rate_multiplier_schedule",
            "makeup_airflow_rate",
            "non_mechanical_cooling_fan_power",
            "non_mechanical_cooling_fan_airflow",
            "air_distribution_effectiveness",
            "aggregation_factor",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.zone_data_structure[attr] = value

    def get_output_requests(self):
        """Get the output requests for the zone."""
        requests = {}
        if self.parent.is_terminal and self.parent.is_zonal_system:
            requests = {
                "HVAC Systems - Design Parameters - Zone Design Data - General - Supply Airflow": (
                    2201045,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Exhaust Airflow": (
                    2201046,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Fan Power": (
                    2201047,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Minimum Airflow Ratio": (
                    2201048,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Outside Airflow": (
                    2201049,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Cooling Capacity": (
                    2201050,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Sensible Heat Ratio": (
                    2201051,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Heating Capacity": (
                    2201053,
                    self.parent.u_name,
                    self.u_name,
                ),
                "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Multiplier": (
                    2201055,
                    self.parent.u_name,
                    self.u_name,
                ),
            }

            match self.parent.output_cool_type:
                case BDL_OutputCoolingTypes.CHILLED_WATER:
                    # Design data for Cooling - chilled water - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203505,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Design data for Cooling - chilled water - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203506,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - chilled water - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203516,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - chilled water - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203517,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputCoolingTypes.DX_AIR_COOLED:
                    # Design data for Cooling - DX air cooled - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203557,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Design data for Cooling - DX air cooled - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203558,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - DX air cooled - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203566,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - DX air cooled - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203567,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputCoolingTypes.DX_WATER_COOLED:
                    # Design data for Cooling - DX water cooled - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203587,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Design data for Cooling - DX water cooled - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203588,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - DX water cooled - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203596,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - DX water cooled - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203597,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputCoolingTypes.VRF:
                    # Design data for Cooling - VRF - ZONE - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203619,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Design data for Cooling - VRF - ZONE - SHR
                    requests["Design Cooling SHR"] = (
                        2203620,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - VRF - ZONE - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203628,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Cooling - VRF - ZONE - SHR
                    requests["Rated Cooling SHR"] = (
                        2203629,
                        self.parent.u_name,
                        self.u_name,
                    )

            match self.parent.output_heat_type:
                case BDL_OutputHeatingTypes.FURNACE:
                    # Design data for Heating - furnace - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203708,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_AIR_COOLED:
                    # Design data for Heating - heat pump air cooled - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203784,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Heating - heat pump air cooled - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203790,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED:
                    # Design data for Heating - heat pump water cooled - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203805,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Heating - heat pump water cooled - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203811,
                        self.parent.u_name,
                        self.u_name,
                    )
                case BDL_OutputHeatingTypes.VRF:
                    # Design data for Heating - VRF - ZONE - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203828,
                        self.parent.u_name,
                        self.u_name,
                    )
                    # Rated data for Heating - VRF - ZONE - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203834,
                        self.parent.u_name,
                        self.u_name,
                    )

        elif self.parent.is_terminal and not self.parent.is_zonal_system:
            requests = {
                "Outside Air Ratio": (2201005, self.parent.u_name, ""),
                "Cooling Capacity": (2201006, self.parent.u_name, ""),
                "Heating Capacity": (2201008, self.parent.u_name, ""),
                "Supply Fan - Airflow": (2201012, self.parent.u_name, ""),
                "Supply Fan - Power": (2201014, self.parent.u_name, ""),
                "Supply Fan - Min Flow Ratio": (2201022, self.parent.u_name, ""),
            }

            match self.parent.output_cool_type:
                case BDL_OutputCoolingTypes.CHILLED_WATER:
                    # Design data for Cooling - chilled water - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203015,
                        self.parent.u_name,
                        "",
                    )
                    # Design data for Cooling - chilled water - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203016, self.parent.u_name, "")
                    # Rated data for Cooling - chilled water - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203026,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Cooling - chilled water - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203027, self.parent.u_name, "")
                case BDL_OutputCoolingTypes.DX_AIR_COOLED:
                    # Design data for Cooling - DX air cooled - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203083,
                        self.parent.u_name,
                        "",
                    )
                    # Design data for Cooling - DX air cooled - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203084, self.parent.u_name, "")
                    # Rated data for Cooling - DX air cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203092,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Cooling - DX air cooled - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203093, self.parent.u_name, "")
                case BDL_OutputCoolingTypes.DX_WATER_COOLED:
                    # Design data for Cooling - DX water cooled - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203143,
                        self.parent.u_name,
                        "",
                    )
                    # Design data for Cooling - DX water cooled - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203144, self.parent.u_name, "")
                    # Rated data for Cooling - DX water cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203152,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Cooling - DX water cooled - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203153, self.parent.u_name, "")
                case BDL_OutputCoolingTypes.VRF:
                    # Design data for Cooling - VRF - SYSTEM - capacity, btu/hr
                    requests["Design Cooling capacity"] = (
                        2203207,
                        self.parent.u_name,
                        "",
                    )
                    # Design data for Cooling - VRF - SYSTEM - SHR
                    requests["Design Cooling SHR"] = (2203208, self.parent.u_name, "")
                    # Rated data for Cooling - VRF - SYSTEM - capacity, btu/hr
                    requests["Rated Cooling capacity"] = (
                        2203216,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Cooling - VRF - SYSTEM - SHR
                    requests["Rated Cooling SHR"] = (2203217, self.parent.u_name, "")

            match self.parent.output_heat_type:
                case BDL_OutputHeatingTypes.FURNACE:
                    requests["Design Heating capacity"] = (
                        2203296,
                        self.parent.u_name,
                        "",
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_AIR_COOLED:
                    # Design data for Heating - heat pump air cooled - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203372,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Heating - heat pump air cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203378,
                        self.parent.u_name,
                        "",
                    )
                case BDL_OutputHeatingTypes.HEAT_PUMP_WATER_COOLED:
                    # Design data for Heating - heat pump water cooled - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203414,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Heating - heat pump water cooled - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203420,
                        self.parent.u_name,
                        "",
                    )
                case BDL_OutputHeatingTypes.VRF:
                    # Design data for Heating - VRF - SYSTEM - capacity, btu/hr
                    requests["Design Heating capacity"] = (
                        2203460,
                        self.parent.u_name,
                        "",
                    )
                    # Rated data for Heating - VRF - SYSTEM - capacity, btu/hr
                    requests["Rated Heating capacity"] = (
                        2203466,
                        self.parent.u_name,
                        "",
                    )

        else:
            requests.update(
                {
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Supply Airflow": (
                        2201045,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Exhaust Airflow": (
                        2201046,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Fan Power": (
                        2201047,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Minimum Airflow Ratio": (
                        2201048,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Outside Airflow": (
                        2201049,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Cooling Capacity": (
                        2201050,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Sensible Heat Ratio": (
                        2201051,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Heating Capacity": (
                        2201053,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - General - Zone Multiplier": (
                        2201055,
                        self.parent.u_name,
                        self.u_name,
                    ),
                }
            )

        if self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE) in [
            BDL_TerminalTypes.TERMINAL_IU,
            BDL_TerminalTypes.CEILING_IU,
            BDL_TerminalTypes.SERIES_PIU,
            BDL_TerminalTypes.PARALLEL_PIU,
        ]:
            requests.update(
                {
                    "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Fan Flow": (
                        2202001,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Cold Deck Flow": (
                        2202002,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Cold Deck Minimum Airflow Ratio": (
                        2202003,
                        self.parent.u_name,
                        self.u_name,
                    ),
                }
            )

        if self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE) in [
            BDL_TerminalTypes.SERIES_PIU,
            BDL_TerminalTypes.PARALLEL_PIU,
        ]:
            requests.update(
                {
                    "HVAC Systems - Design Parameters - Zone Design Data - Powered Induction Units - Fan kW": (
                        2202006,
                        self.parent.u_name,
                        self.u_name,
                    ),
                }
            )

        if self.get_inp(BDL_ZoneKeywords.TERMINAL_TYPE) in [
            BDL_TerminalTypes.DUAL_DUCT,
            BDL_TerminalTypes.MULTIZONE,
        ]:
            requests.update(
                {
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Cold Deck Airflow": (
                        2201056,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Cold Deck Minimum Flow Ratio": (
                        2201057,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Hot Deck Airflow": (
                        2201058,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Hot Deck Minimum Flow Ratio": (
                        2201059,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Outlet Airflow": (
                        2201060,
                        self.parent.u_name,
                        self.u_name,
                    ),
                    "HVAC Systems - Design Parameters - Zone Design Data - Dual-Duct/Multizone Boxes - Outlet Minimum Flow Ratio": (
                        2201061,
                        self.parent.u_name,
                        self.u_name,
                    ),
                }
            )

        return requests

    def insert_to_rpd(self, rmd):
        """Insert zone object into the rpd data structure."""
        self.parent_building_segment.zones.append(self.zone_data_structure)
