from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums
from rpd_generator.utilities import curve_funcs


EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
ChillerCompressorOptions = SchemaEnums.schema_enums["ChillerCompressorOptions"]
ChillerEfficiencyMetricOptions = SchemaEnums.schema_enums[
    "ChillerEfficiencyMetricOptions"
]

BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ChillerKeywords = BDLEnums.bdl_enums["ChillerKeywords"]
BDL_ChillerTypes = BDLEnums.bdl_enums["ChillerTypes"]
BDL_CondenserTypes = BDLEnums.bdl_enums["CondenserTypes"]
BDL_CurveFitKeywords = BDLEnums.bdl_enums["CurveFitKeywords"]
BDL_CurveFitInputTypes = BDLEnums.bdl_enums["CurveFitInputTypes"]
BDL_CurveFitTypes = BDLEnums.bdl_enums["CurveFitTypes"]
BDL_CirculationLoopKeywords = BDLEnums.bdl_enums["CirculationLoopKeywords"]

OMIT = "OMIT"

# Global variable defined at the module level to be used in the functions in this module
absorp_or_engine = False


class Chiller(BaseNode):
    """Chiller object in the tree."""

    bdl_command = BDL_Commands.CHILLER

    compressor_type_map = {
        BDL_ChillerTypes.ELEC_OPEN_CENT: ChillerCompressorOptions.CENTRIFUGAL,
        BDL_ChillerTypes.ELEC_OPEN_REC: ChillerCompressorOptions.RECIPROCATING,
        BDL_ChillerTypes.ELEC_HERM_CENT: ChillerCompressorOptions.CENTRIFUGAL,
        BDL_ChillerTypes.ELEC_HERM_REC: ChillerCompressorOptions.RECIPROCATING,
        BDL_ChillerTypes.ELEC_SCREW: ChillerCompressorOptions.SCREW,
        BDL_ChillerTypes.ELEC_HTREC: ChillerCompressorOptions.OTHER,
        BDL_ChillerTypes.ABSOR_1: ChillerCompressorOptions.SINGLE_EFFECT_INDIRECT_FIRED_ABSORPTION,
        BDL_ChillerTypes.ABSOR_2: ChillerCompressorOptions.DOUBLE_EFFECT_INDIRECT_FIRED_ABSORPTION,
        BDL_ChillerTypes.GAS_ABSOR: ChillerCompressorOptions.DOUBLE_EFFECT_DIRECT_FIRED_ABSORPTION,
        BDL_ChillerTypes.ENGINE: ChillerCompressorOptions.OTHER,
        BDL_ChillerTypes.HEAT_PUMP: ChillerCompressorOptions.OTHER,
        BDL_ChillerTypes.LOOP_TO_LOOP_HP: ChillerCompressorOptions.OTHER,
        BDL_ChillerTypes.WATER_ECONOMIZER: OMIT,
        BDL_ChillerTypes.STRAINER_CYCLE: OMIT,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.chiller_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.omit = False
        self.chiller_data_structure = {}

        # data elements with children
        self.efficiency_metric_values = []
        self.efficiency_metric_types = []
        self.capacity_validation_points = []
        self.power_validation_points = []

        # data elements with no children
        self.cooling_loop = None
        self.condensing_loop = None
        self.compressor_type = None
        self.energy_source_type = None
        self.design_capacity = None
        self.rated_capacity = None
        self.rated_entering_condenser_temperature = None
        self.rated_leaving_evaporator_temperature = None
        self.minimum_load_ratio = None
        self.design_flow_evaporator = None
        self.design_flow_condenser = None
        self.design_entering_condenser_temperature = None
        self.design_leaving_evaporator_temperature = None
        self.is_chilled_water_pump_interlocked = None
        self.is_condenser_water_pump_interlocked = None
        self.heat_recovery_loop = None
        self.heat_recovery_fraction = None

    def __repr__(self):
        return f"Chiller(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for chiller object."""
        global absorp_or_engine
        absorp_or_engine = False
        if self.compressor_type_map.get(self.get_inp(BDL_ChillerKeywords.TYPE)) == OMIT:
            self.omit = True
            return

        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ABSOR_1,
            BDL_ChillerTypes.ABSOR_2,
            BDL_ChillerTypes.GAS_ABSOR,
            BDL_ChillerTypes.ENGINE,
        ]:
            absorp_or_engine = True

        requests = self.get_output_requests(absorp_or_engine)
        output_data = self.get_output_data(requests)
        for key in [
            "Design Parameters - Capacity",
            "Normalized (ARI) Capacity at Peak (Btu/hr)",
            "Primary Equipment (Chillers) - Capacity (Btu/hr)",
        ]:
            if key in output_data:
                output_data[key] = self.try_convert_units(
                    output_data[key], "Btu/hr", "MMBtu/hr"
                )

        self.cooling_loop = self.get_inp(BDL_ChillerKeywords.CHW_LOOP)

        self.condensing_loop = self.get_inp(BDL_ChillerKeywords.CW_LOOP)

        self.heat_recovery_loop = self.get_inp(BDL_ChillerKeywords.HTREC_LOOP)

        self.compressor_type = self.compressor_type_map.get(
            self.get_inp(BDL_ChillerKeywords.TYPE)
        )

        if not absorp_or_engine:
            self.energy_source_type = EnergySourceOptions.ELECTRICITY

        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ENGINE,
            BDL_ChillerTypes.GAS_ABSOR,
        ]:
            self.energy_source_type = EnergySourceOptions.NATURAL_GAS

        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ABSOR_1,
            BDL_ChillerTypes.ABSOR_2,
        ]:
            hot_water_loop_name = self.get_obj(
                self.get_inp(BDL_ChillerKeywords.HW_LOOP)
            )
            hot_water_loop = self.get_obj(hot_water_loop_name)

            if hot_water_loop:
                self.energy_source_type = self.get_loop_energy_source(hot_water_loop)

        chw_loop = self.get_obj(self.cooling_loop)
        self.design_leaving_evaporator_temperature = self.try_float(
            chw_loop.get_inp(BDL_CirculationLoopKeywords.DESIGN_COOL_T)
        )

        # This says ARI but appears to report out the design condenser water temperature
        # TODO Test what this reports when the condenser type is air source or remote, hopefully it still reports a condenser temp
        self.design_entering_condenser_temperature = self.try_float(
            output_data.get(
                "Normalized (ARI) Entering Condenser Water Temperature (°F)"
            )
        )

        self.design_capacity = self.try_float(
            output_data.get("Design Parameters - Capacity")
        )

        self.minimum_load_ratio = self.try_float(
            self.get_inp(BDL_ChillerKeywords.MIN_RATIO)
        )

        rated_part_load_ratio = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_PLR)
        )
        # If BDL_ChillerKeywords.RATED_PLR is not populated then it is n/a and so the value is set to 1
        if not rated_part_load_ratio:
            rated_part_load_ratio = 1

        if absorp_or_engine:
            input_ratio_keyword = BDL_ChillerKeywords.HEAT_INPUT_RATIO
        else:
            input_ratio_keyword = BDL_ChillerKeywords.ELEC_INPUT_RATIO

        coefficients, coeffs, min_outputs, max_outputs = (
            self.get_dict_of_curve_coefficient_min_and_max()
        )
        # Obtain the AHRI rated temperatures
        rated_temperatures = (
            self.get_evap_leaving_and_condenser_entering_ahri_conditions()
        )
        rated_leaving_evaporator_temperature = rated_temperatures[0]
        rated_entering_condenser_temperature = rated_temperatures[1]

        curves_normalized_to_ahri_allowed_margin_of_error = 1.5
        are_curve_outputs_all_equal_to_one_at_ahri_temperatures = curve_funcs.are_curve_outputs_all_equal_to_a_value_of_one(
                coefficients,
                rated_leaving_evaporator_temperature,
                rated_entering_condenser_temperature,
                curves_normalized_to_ahri_allowed_margin_of_error,
            )


        # The if statement checks if any of the performance curves were defined as data_input type of DATA. If so, at this point in time we cannot perform
        # efficiency or capacity adjustments or IPLV calculations using the curves so we take the approach shown below.
        # This also checks if the entered rated conditions match AHRI and if the performance curves are normalized to ahri conditions.
        # If the answer to both is no then the logic is run.
        if not coeffs or (
            not self.is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions()
            and not are_curve_outputs_all_equal_to_one_at_ahri_temperatures):
            # Instead of setting these to AHRI conditions and adjusting capacity and efficiency to match AHRI conditions we just populate these
            # as defined.
            if not coeffs: self.notes = "Performance curve INPUT-TYPE of DATA is not currently supported for determining and populating chiller IPLV."
            self.rated_leaving_evaporator_temperature = self.try_float(
                self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
            )
            self.rated_entering_condenser_temperature = self.try_float(
                self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
            )
            # If a hardcoded capacity does not exist then it will not be populated, without usable performance curves we can't obtain this rated capacity.
            # For auto-sized equipment.
            self.rated_capacity = self.try_float(
                self.get_inp(BDL_ChillerKeywords.CAPACITY)
            )
            if (
                self.is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions()
            ):
                self.efficiency_metric_values.append(
                    1 / self.try_float(self.get_inp(input_ratio_keyword))
                )
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                )
            else:
                self.efficiency_metric_values.append(
                    1 / self.try_float(self.get_inp(input_ratio_keyword))
                )
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.OTHER
                )
        else:
            # First section covers when capacity and efficiency are defined at AHRI conditions
            # For the design to rated capacity calcs this assumes that the curves are normalized to AHRI rated conditions.
            if (
                self.is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions()
            ):
                # Assign AHRI conditions to these rated temperatures
                self.rated_leaving_evaporator_temperature = (
                    rated_leaving_evaporator_temperature
                )
                self.rated_entering_condenser_temperature = (
                    rated_entering_condenser_temperature
                )

                # Obtain results of curves at 100% load and AHRI temperature conditions
                curve_results_at_rated_conditions_and_100_percent_load = (
                    self.get_output_of_curves_at_temperature_and_load_conditions(
                        rated_leaving_evaporator_temperature,
                        rated_entering_condenser_temperature,
                        1,
                    )
                )
                cap_ft_result = curve_results_at_rated_conditions_and_100_percent_load[
                    "cap_ft_result"
                ]

                # Obtain results of efficiency curves (not capacity curves) by plugging the user interface rated part load ratio into the curves equations
                efficiency_curve_result_rated_part_load = curve_funcs.calculate_results_of_efficiency_performance_curves_with_specific_part_load_ratio(
                    rated_leaving_evaporator_temperature,
                    rated_entering_condenser_temperature,
                    coefficients,
                    rated_part_load_ratio,
                )
                eff_ft_result_rated_part_load = efficiency_curve_result_rated_part_load[
                    "eff_ft_result"
                ]
                eff_fplr_result_rated_part_load = (
                    efficiency_curve_result_rated_part_load["eff_fplr_result"]
                )

                # Obtain results of curves at 100% load and design temperature conditions
                design_leaving_evaporator_temperature = (
                    self.design_leaving_evaporator_temperature
                )
                design_entering_condenser_temperature = (
                    self.design_entering_condenser_temperature
                )
                curve_results_at_design_conditions_and_100_percent_load = (
                    self.get_output_of_curves_at_temperature_and_load_conditions(
                        design_leaving_evaporator_temperature,
                        design_entering_condenser_temperature,
                        1,
                    )
                )
                cap_ft_result_design = (
                    curve_results_at_design_conditions_and_100_percent_load[
                        "cap_ft_result"
                    ]
                )

                # If capacity is hard coded and PLR RATED is entered (not n/a).
                if (
                    self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio != 1
                ):
                    entered_capacity = self.try_float(
                        self.get_inp(BDL_ChillerKeywords.CAPACITY)
                    )
                    adjusted_capacity = curve_funcs.adjust_capacity_for_entered_plr(
                        rated_part_load_ratio, entered_capacity, cap_ft_result
                    )
                    # This efficiency will be in EIR or HIR
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        rated_part_load_ratio
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_rated_part_load
                            * eff_fplr_result_rated_part_load
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier

                    self.rated_capacity = adjusted_capacity
                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )
                    # Check that performance curves are normalized to 1 at ahri temperatures
                    if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                        iplv_value = self.calculate_iplv()
                        if iplv_value:
                            self.efficiency_metric_values.append(iplv_value)
                        self.efficiency_metric_types.append(
                            ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                        )
                # If capacity is auto-sized and PLR RATED is entered (not n/a).
                elif (
                    not self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio != 1
                ):
                    autosized_design_capacity = self.try_float(
                        output_data.get(
                            "Primary Equipment (Chillers) - Capacity (Btu/hr)"
                        )
                    )
                    # Adjusts from design to rated conditions.
                    self.rated_capacity = (
                        autosized_design_capacity
                        * (1 / (cap_ft_result * rated_part_load_ratio))
                        * (cap_ft_result / cap_ft_result_design)
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        rated_part_load_ratio
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_rated_part_load
                            * eff_fplr_result_rated_part_load
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier

                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    # Check that performance curves are normalized to 1 at ahri temperatures
                    if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                        iplv_value = self.calculate_iplv()
                        if iplv_value:
                            self.efficiency_metric_values.append(iplv_value)
                        self.efficiency_metric_types.append(
                            ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                        )
                # If capacity is hard-coded and PLR Rated is n/a or 1
                elif (
                    self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio == 1
                ):
                    self.rated_capacity = self.try_float(
                        self.get_inp(BDL_ChillerKeywords.CAPACITY)
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    self.efficiency_metric_values.append(1 / user_interface_eff)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    # Check that performance curves are normalized to 1 at ahri temperatures
                    if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                        iplv_value = self.calculate_iplv()
                        if iplv_value:
                            self.efficiency_metric_values.append(iplv_value)
                        self.efficiency_metric_types.append(
                            ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                        )
                #  If capacity is auto-sized and Rated is n/a or 1
                else:
                    autosized_design_capacity = self.try_float(
                        output_data.get(
                            "Primary Equipment (Chillers) - Capacity (Btu/hr)"
                        )
                    )
                    # Adjusts from design to rated conditions.
                    self.rated_capacity = autosized_design_capacity * (
                        cap_ft_result / cap_ft_result_design
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    self.efficiency_metric_values.append(1 / user_interface_eff)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    # Check that performance curves are normalized to 1 at ahri temperatures
                    if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                        iplv_value = self.calculate_iplv()
                        if iplv_value:
                            self.efficiency_metric_values.append(iplv_value)
                        self.efficiency_metric_types.append(
                            ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                        )
            # Rated temperatures entered in the UI are not at AHRI conditions and curves are normalized to 1 at AHRI conditions.
            else:
                # The curves will be used below to adjust values (cap and eff) to AHRI conditions so we set the rated temps in the RPD to AHRI
                # temperatures even though these were not entered in the UI.
                self.rated_leaving_evaporator_temperature = (
                    rated_leaving_evaporator_temperature
                )
                self.rated_entering_condenser_temperature = (
                    rated_entering_condenser_temperature
                )

                entered_leaving_evaporator_temperature = (
                    self.rated_leaving_evaporator_temperature
                ) = self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_CHW_T))
                entered_entering_condenser_temperature = (
                    self.rated_entering_condenser_temperature
                ) = self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_COND_T))

                # Obtain results of curves at 100% load and entered rated (non AHRI) temperature conditions
                curve_results_at_entered_conditions_and_100_percent_load = (
                    self.get_output_of_curves_at_temperature_and_load_conditions(
                        entered_leaving_evaporator_temperature,
                        entered_entering_condenser_temperature,
                        1,
                    )
                )
                eff_ft_result_entered = (
                    curve_results_at_entered_conditions_and_100_percent_load[
                        "eff_ft_result"
                    ]
                )
                eff_fplr_result_entered = (
                    curve_results_at_entered_conditions_and_100_percent_load[
                        "eff_fplr_result"
                    ]
                )
                part_load_ratio_entered = (
                    curve_results_at_entered_conditions_and_100_percent_load[
                        "part_load_ratio"
                    ]
                )
                cap_ft_result_entered = (
                    curve_results_at_entered_conditions_and_100_percent_load[
                        "cap_ft_result"
                    ]
                )

                # Obtain results of efficiency curves (not capacity curves) by plugging the user interface rated part load ratio into the curves equations
                efficiency_curve_result_entered_part_load = curve_funcs.calculate_results_of_efficiency_performance_curves_with_specific_part_load_ratio(
                    entered_leaving_evaporator_temperature,
                    entered_entering_condenser_temperature,
                    coefficients,
                    rated_part_load_ratio,
                )
                eff_ft_result_rated_part_load_entered = (
                    efficiency_curve_result_entered_part_load["eff_ft_result"]
                )
                eff_fplr_result_rated_part_load_entered = (
                    efficiency_curve_result_entered_part_load["eff_fplr_result"]
                )

                # Obtain results of curves at 100% load and design temperature conditions
                design_leaving_evaporator_temperature = (
                    self.design_leaving_evaporator_temperature
                )
                design_entering_condenser_temperature = (
                    self.design_entering_condenser_temperature
                )
                curve_results_at_design_conditions_and_100_percent_load = (
                    self.get_output_of_curves_at_temperature_and_load_conditions(
                        design_leaving_evaporator_temperature,
                        design_entering_condenser_temperature,
                        1,
                    )
                )
                cap_ft_result_design = (
                    curve_results_at_design_conditions_and_100_percent_load[
                        "cap_ft_result"
                    ]
                )

                # If capacity is hard coded and PLR RATED is entered (not n/a). (This is the same as used above for when it is at AHRI)
                if (
                    self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio != 1
                ):
                    entered_capacity = self.try_float(
                        self.get_inp(BDL_ChillerKeywords.CAPACITY)
                    )
                    adjusted_capacity = curve_funcs.adjust_capacity_for_entered_plr(
                        rated_part_load_ratio, entered_capacity, cap_ft_result_entered
                    )
                    # This efficiency will be in EIR or HIR
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        rated_part_load_ratio
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_rated_part_load_entered
                            * eff_fplr_result_rated_part_load_entered
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier

                    self.rated_capacity = adjusted_capacity
                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    iplv_value = self.calculate_iplv()
                    if iplv_value:
                        self.efficiency_metric_values.append(iplv_value)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                    )
                # If capacity is auto-sized and PLR RATED is entered (not n/a). (This is the same as used above for when it is at AHRI)
                elif (
                    not self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio != 1
                ):
                    autosized_design_capacity = self.try_float(
                        output_data.get(
                            "Primary Equipment (Chillers) - Capacity (Btu/hr)"
                        )
                    )
                    # Adjusts from design to rated conditions.
                    self.rated_capacity = (
                        autosized_design_capacity
                        * (1 / (cap_ft_result_entered * rated_part_load_ratio))
                        * (cap_ft_result_entered / cap_ft_result_design)
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        rated_part_load_ratio
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_rated_part_load_entered
                            * eff_fplr_result_rated_part_load_entered
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier

                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    iplv_value = self.calculate_iplv()
                    if iplv_value:
                        self.efficiency_metric_values.append(iplv_value)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                    )
                # If capacity is hard-coded and PLR Rated is n/a or 1 (Differs from AHRI section above. It may be because curves = 1 at ahri so it may actually be the same)
                elif (
                    self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                    and rated_part_load_ratio == 1
                ):
                    self.rated_capacity = (
                        self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                        / cap_ft_result_entered
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        part_load_ratio_entered
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_entered
                            * eff_fplr_result_entered
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier
                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    iplv_value = self.calculate_iplv()
                    if iplv_value:
                        self.efficiency_metric_values.append(iplv_value)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                    )
                #  If capacity is auto-sized and Rated is n/a or 1
                else:
                    autosized_design_capacity = self.try_float(
                        output_data.get(
                            "Primary Equipment (Chillers) - Capacity (Btu/hr)"
                        )
                    )
                    # Adjusts from design to rated conditions. (Differs from AHRI section above. It may be because curves = 1 at ahri so it may actually be the same)
                    self.rated_capacity = autosized_design_capacity * (
                        cap_ft_result_entered / cap_ft_result_design
                    )
                    user_interface_eff = self.try_float(
                        self.get_inp(input_ratio_keyword)
                    )
                    eir_multiplier = (
                        part_load_ratio_entered
                        / 1000
                        / (
                            3.412
                            * eff_ft_result_entered
                            * eff_fplr_result_entered
                            / 3412
                        )
                    )
                    eff_adj = user_interface_eff * eir_multiplier

                    self.efficiency_metric_values.append(1 / eff_adj)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
                    )

                    iplv_value = self.calculate_iplv()
                    if iplv_value:
                        self.efficiency_metric_values.append(iplv_value)
                    self.efficiency_metric_types.append(
                        ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                    )

        self.design_flow_evaporator = self.try_float(
            output_data.get("Design Parameters - Flow")
        )

        self.design_flow_condenser = self.try_float(
            output_data.get("Design Parameters - Condenser Flow")
        )

        (
            self.is_chilled_water_pump_interlocked,
            self.is_condenser_water_pump_interlocked,
        ) = self.are_pumps_interlocked(self.cooling_loop, self.condensing_loop)

        # Assign pump data elements populated from the boiler keyword value pairs
        chw_pump_name = self.get_inp(BDL_ChillerKeywords.CHW_PUMP)
        if chw_pump_name is not None:
            pump = self.get_obj(chw_pump_name)
            if pump is not None:
                pump.loop_or_piping = [self.cooling_loop] * pump.qty

        # Assign pump data elements populated from the chiller keyword value pairs
        cw_pump_name = self.get_inp(BDL_ChillerKeywords.CW_PUMP)
        if cw_pump_name is not None:
            pump = self.get_obj(cw_pump_name)
            if pump is not None:
                pump.loop_or_piping = [self.condensing_loop] * pump.qty

    def get_output_requests(self, absorp_or_engine):
        """Get output data requests for chiller object."""

        if not absorp_or_engine:
            requests = {
                "Normalized (ARI) Capacity at Peak (Btu/hr)": (
                    2318901,
                    self.u_name,
                    "",
                ),
                "Normalized (ARI) Leaving Chilled Water Temperature (°F)": (
                    2318902,
                    self.u_name,
                    "",
                ),
                "Normalized (ARI) Entering Condenser Water Temperature (°F)": (
                    2318903,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Capacity": (
                    2318003,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Flow": (2318004, self.u_name, ""),
                "Design Parameters - Condenser Flow": (
                    2318009,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Electric Input Ratio": (
                    2318005,
                    self.u_name,
                    "",
                ),
                "Primary Equipment (Chillers) - Capacity (Btu/hr)": (
                    2401051,
                    "",
                    self.u_name,
                ),
                "Elec Chillers - Sizing Info/Circ Loop - Design T": (
                    2401051,
                    "",
                    self.u_name,
                ),
            }
        else:
            requests = {
                "Normalized (ARI) Capacity at Peak (Btu/hr)": (
                    2319901,
                    self.u_name,
                    "",
                ),
                "Normalized (ARI) Leaving Chilled Water Temperature (°F)": (
                    2319902,
                    self.u_name,
                    "",
                ),
                "Normalized (ARI) Entering Condenser Water Temperature (°F)": (
                    2319903,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Capacity": (
                    2319003,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Flow": (
                    2319004,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Condenser Flow": (
                    2319010,
                    self.u_name,
                    "",
                ),
                "Design Parameters - Electric Input Ratio": (
                    2319005,
                    self.u_name,
                    "",
                ),
                "Primary Equipment (Chillers) - Capacity (Btu/hr)": (
                    2401051,
                    "",
                    self.u_name,
                ),
            }

        return requests

    def populate_data_group(self):
        """Populate schema structure for chiller object."""
        if self.omit:
            return

        self.chiller_data_structure = {
            "id": self.u_name,
            "efficiency_metric_values": self.efficiency_metric_values,
            "efficiency_metric_types": self.efficiency_metric_types,
            "capacity_validation_points": self.capacity_validation_points,
            "power_validation_points": self.power_validation_points,
        }

        no_children_attributes = [
            "cooling_loop",
            "condensing_loop",
            "compressor_type",
            "energy_source_type",
            "design_capacity",
            "rated_capacity",
            "rated_entering_condenser_temperature",
            "rated_leaving_evaporator_temperature",
            "minimum_load_ratio",
            "design_flow_evaporator",
            "design_flow_condenser",
            "design_entering_condenser_temperature",
            "design_leaving_evaporator_temperature",
            "is_chilled_water_pump_interlocked",
            "is_condenser_water_pump_interlocked",
            "heat_recovery_loop",
            "heat_recovery_fraction",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.chiller_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert chiller object into the rpd data structure."""
        if self.omit:
            return

        rmd.chillers.append(self.chiller_data_structure)

    def get_loop_energy_source(self, hot_water_loop):
        """Get the energy source type for the loop. Used for absorption chillers to populate the energy_source_type."""
        energy_source_set = set()
        for boiler_name in self.rmd.boiler_names:
            boiler = self.get_obj(boiler_name)
            if boiler.loop == hot_water_loop.u_name:
                energy_source_set.add(boiler.energy_source_type)

        for steam_meter_name in self.rmd.steam_meter_names:
            steam_meter = self.get_obj(steam_meter_name)
            if steam_meter.loop == hot_water_loop.u_name:
                energy_source_set.add(steam_meter.energy_source_type)

        for chiller_name in self.rmd.chiller_names:
            chiller = self.get_obj(chiller_name)
            if chiller.heat_recovery_loop == hot_water_loop.u_name:
                energy_source_set.add(EnergySourceOptions.ELECTRICITY)

        if len(energy_source_set) == 1:
            return energy_source_set.pop()
        else:
            return EnergySourceOptions.OTHER

    def are_pumps_interlocked(self, chw_loop_name, cw_loop_name):
        """Check if the chiller has a pump with interlocked operation."""
        chw_pump_interlocked = False
        cw_pump_interlocked = False
        for pump_name in self.rmd.pump_names:
            pump = self.get_obj(pump_name)
            if pump.loop_or_piping == chw_loop_name:  # pump is guaranteed to exist
                chw_pump_interlocked = bool(self.get_inp(BDL_ChillerKeywords.CHW_PUMP))

            if pump.loop_or_piping == cw_loop_name:  # pump is guaranteed to exist
                cw_pump_interlocked = bool(self.get_inp(BDL_ChillerKeywords.CW_PUMP))
        return chw_pump_interlocked, cw_pump_interlocked

    def get_dict_of_curve_coefficient_min_and_max(self):
        """Returns a dictionary with curve coefficients and the min and max associated with each curve.
        Returns information for "eff_ft": eff_ft, "cap_ft": cap_ft, "eff_fplr": eff_fplr
        """
        cap_ft = self.get_obj(self.get_inp(BDL_ChillerKeywords.CAPACITY_FT))

        if not absorp_or_engine:
            eff_ft_key = BDL_ChillerKeywords.EIR_FT
            eff_fplr_key = BDL_ChillerKeywords.EIR_FPLR
        else:
            eff_ft_key = BDL_ChillerKeywords.HIR_FT
            eff_fplr_key = BDL_ChillerKeywords.HIR_FPLR

        eff_ft = self.get_obj(self.get_inp(eff_ft_key))
        eff_fplr = self.get_obj(self.get_inp(eff_fplr_key))

        coefficients = {"eff_ft": eff_ft, "cap_ft": cap_ft, "eff_fplr": eff_fplr}
        coeffs = {}
        min_outputs = {}
        max_outputs = {}

        for key, obj in coefficients.items():
            input_type = obj.get_inp(BDL_CurveFitKeywords.INPUT_TYPE)
            if input_type == BDL_CurveFitInputTypes.DATA:
                return coefficients, {}, {}, {}
            coeffs[f"{key}_coeffs"] = list(
                map(float, obj.get_inp(BDL_CurveFitKeywords.COEF))
            )
            min_outputs[f"{key}_min_otpt"] = float(
                obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MIN)
            )
            max_outputs[f"{key}_max_otpt"] = float(
                obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MAX)
            )

        return coefficients, coeffs, min_outputs, max_outputs

    def calculate_iplv(self):
        """Calculates IPLV based upon the modeled performance curves and the rated conditions.
        No corrections for fouling factor have been included - perhaps not relevant."""
        # TODO continued Do more testing to ensure it producing the correct results

        # If the chiller cannot be unloaded to all of the IPLV load categories then do not perform calcs and return nothing
        minimum_load_ratio = self.minimum_load_ratio
        if minimum_load_ratio > 0.25:

            return

        # Dictionary includes percent of rated capacity as the key and then the efficiency result at each percentage. 0.0s are placeholders
        iplv_rating_load_conditions = {
            key: {"results": 0.0} for key in [1, 0.75, 0.5, 0.25]
        }

        condenser_type = self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        condenser_type_iplv_rating_condenser_temp_conditions_map = {
            BDL_CondenserTypes.WATER_COOLED: [85, 75, 65, 65],
            BDL_CondenserTypes.AIR_COOLED: [95, 80, 65, 55],
            BDL_CondenserTypes.REMOTE_AIR_COOLED: [125, 107.5, 90, 72.5],
            BDL_CondenserTypes.REMOTE_EVAP_COOLED: [105, 95, 85, 75],
        }

        ahri_rated_temperatures = (
            self.get_evap_leaving_and_condenser_entering_ahri_conditions()
        )
        evap_leaving_temp_rated = ahri_rated_temperatures[0]
        cond_entering_temp_rated = ahri_rated_temperatures[1]

        if not absorp_or_engine:
            condenser_type_iplv_rating_condenser_temp_conditions = (
                condenser_type_iplv_rating_condenser_temp_conditions_map[condenser_type]
            )
        else:
            condenser_type_iplv_rating_condenser_temp_conditions = [85, 75, 70, 70]

        iplv_percent_of_operation_at_each_load = [0.01, 0.42, 0.45, 0.12]

        coefficients, coeffs, min_outputs, max_outputs = (
            self.get_dict_of_curve_coefficient_min_and_max()
        )

        if not coeffs:
            return "Keyword DATA was used for coefficient determination"

        # Coefficients, min_outputs, and max_outputs dictionaries
        eff_ft_coeffs = coeffs["eff_ft_coeffs"]
        cap_ft_coeffs = coeffs["cap_ft_coeffs"]
        eff_fplr_coeffs = coeffs["eff_fplr_coeffs"]

        eff_ft_min_otpt = min_outputs["eff_ft_min_otpt"]
        eff_ft_max_otpt = max_outputs["eff_ft_max_otpt"]
        cap_ft_min_otpt = min_outputs["cap_ft_min_otpt"]
        cap_ft_max_otpt = max_outputs["cap_ft_max_otpt"]
        eff_fplr_min_otpt = min_outputs["eff_fplr_min_otpt"]
        eff_fplr_max_otpt = max_outputs["eff_fplr_max_otpt"]

        cap_ft = coefficients["cap_ft"]
        eff_fplr_curve_type = cap_ft.get_inp(BDL_CurveFitKeywords.TYPE)

        curve_function_map = {
            BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
            BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
        }

        # All conversions based on rated conditions will have been made in the logic in the main body when establishing Full_LOAD_EFFICIENCY
        full_load_efficiency_rated = self.efficiency_metric_values[
            self.efficiency_metric_types.index(
                ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
            )
        ]

        for index, key in enumerate(iplv_rating_load_conditions):
            cond_entering_temp = condenser_type_iplv_rating_condenser_temp_conditions[
                index
            ]
            # Function below returns:
            # "cap_ft_result": cap_ft_result,
            # "eff_ft_result": eff_ft_result,
            # "part_load_ratio": part_load_ratio,
            # "eff_fplr_result": eff_fplr_result
            results = curve_funcs.calculate_results_of_performance_curves(
                evap_leaving_temp_rated,
                cond_entering_temp,
                cap_ft_coeffs,
                eff_ft_coeffs,
                cap_ft_min_otpt,
                cap_ft_max_otpt,
                eff_ft_min_otpt,
                eff_ft_max_otpt,
                eff_fplr_curve_type,
                eff_fplr_coeffs,
                eff_fplr_min_otpt,
                eff_fplr_max_otpt,
                curve_function_map,
                curve_funcs,
                key,
            )

            eff_ft_result = results["eff_ft_result"]
            eff_fplr_result = results["eff_fplr_result"]
            part_load_ratio = results["part_load_ratio"]

            eff_result_cop = (
                part_load_ratio
                / 1000
                / (
                    (3.412 / full_load_efficiency_rated)
                    * eff_ft_result
                    * eff_fplr_result
                    / 3412
                )
            )

            iplv_rating_load_conditions[key]["results"] = eff_result_cop

        keys_list = list(iplv_rating_load_conditions.keys())
        iplv = 0
        for index, op_percent in enumerate(iplv_percent_of_operation_at_each_load):
            weighted_eff_load = (
                op_percent * iplv_rating_load_conditions[keys_list[index]]["results"]
            )
            iplv = iplv + weighted_eff_load

        return iplv

    def get_evap_leaving_and_condenser_entering_ahri_conditions(self):
        """Returns a list with the AHRI 550 590-2023 rated evaporator leaving temp as index 0 and condenser entering temp as index 1"""
        condenser_type = self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        # Mapped according to AHRI 550 590-2023
        condenser_type_rating_condenser_temp_conditions_map = {
            BDL_CondenserTypes.WATER_COOLED: 85,
            BDL_CondenserTypes.AIR_COOLED: 95,
            BDL_CondenserTypes.REMOTE_AIR_COOLED: 125,
            BDL_CondenserTypes.REMOTE_EVAP_COOLED: 105,
        }
        # For chillers this always equals 44F per AHRI 550 590-2023
        rated_evaporator_leaving_temp = 44
        rated_condenser_entering_temp = (
            condenser_type_rating_condenser_temp_conditions_map[condenser_type]
        )

        return [rated_evaporator_leaving_temp, rated_condenser_entering_temp]

    def is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions(self):
        """Function compares the user defined rating conditions (evap leaving and condenser entering
        temperatures) associated with the user entered eff and capacity to AHRI 550 590-2023
        rated temperature conditions. Returns True if user defined (or eQuest defaults) match AHRI conditions.
        """
        user_defined_rated_temperatures = (
            self.get_user_defined_rated_temperates_for_efficiency_and_capacity()
        )
        user_defined_evaporator_leaving_temp = user_defined_rated_temperatures[0]
        user_defined_condenser_temperature = user_defined_rated_temperatures[1]

        rated_temperatures = (
            self.get_evap_leaving_and_condenser_entering_ahri_conditions()
        )

        is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions = (
            user_defined_evaporator_leaving_temp == rated_temperatures[0]
            and user_defined_condenser_temperature == rated_temperatures[1]
        )
        return is_user_defined_rated_eff_and_cap_defined_at_ahri_rating_conditions

    def get_user_defined_rated_temperates_for_efficiency_and_capacity(self):
        """Returns the temperatures that the modeler entered for the rated conditions for
        evaporator leaving and condenser entering temperatures associated with efficiency
        and capacity. Function returns a list with the entered (i.e., user defined) evaporator
        leaving temperatures as index 0 and the entered (i.e., user defined condenser entering
         temperatures as 1."""
        user_defined_evaporator_leaving_temp = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
        )
        user_defined_condenser_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
        )

        return [
            user_defined_evaporator_leaving_temp,
            user_defined_condenser_temperature,
        ]

    def get_output_of_curves_at_temperature_and_load_conditions(
        self, evap_leaving_temp: float, cond_entering_temp: float, load: float
    ):
        """Returns the results of the Cap_ft curve given the temperatures and % load sent to the function."""

        coefficients, coeffs, min_outputs, max_outputs = (
            self.get_dict_of_curve_coefficient_min_and_max()
        )

        eff_ft_coeffs = coeffs["eff_ft_coeffs"]
        cap_ft_coeffs = coeffs["cap_ft_coeffs"]
        eff_fplr_coeffs = coeffs["eff_fplr_coeffs"]

        eff_ft_min_otpt = min_outputs["eff_ft_min_otpt"]
        eff_ft_max_otpt = max_outputs["eff_ft_max_otpt"]
        cap_ft_min_otpt = min_outputs["cap_ft_min_otpt"]
        cap_ft_max_otpt = max_outputs["cap_ft_max_otpt"]
        eff_fplr_min_otpt = min_outputs["eff_fplr_min_otpt"]
        eff_fplr_max_otpt = max_outputs["eff_fplr_max_otpt"]

        cap_ft = coefficients["cap_ft"]
        eff_fplr_curve_type = cap_ft.get_inp(BDL_CurveFitKeywords.TYPE)

        curve_function_map = {
            BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
            BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
        }

        # Function below returns:
        # "cap_ft_result": cap_ft_result,
        # "eff_ft_result": eff_ft_result,
        # "part_load_ratio": part_load_ratio,
        # "eff_fplr_result": eff_fplr_result
        results = curve_funcs.calculate_results_of_performance_curves(
            evap_leaving_temp,
            cond_entering_temp,
            cap_ft_coeffs,
            eff_ft_coeffs,
            cap_ft_min_otpt,
            cap_ft_max_otpt,
            eff_ft_min_otpt,
            eff_ft_max_otpt,
            eff_fplr_curve_type,
            eff_fplr_coeffs,
            eff_fplr_min_otpt,
            eff_fplr_max_otpt,
            curve_function_map,
            curve_funcs,
            load,
        )

        return results
