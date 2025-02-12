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

AHRI_550_590_2023_COND_ENTERING_T = {
    BDL_CondenserTypes.WATER_COOLED: 85,
    BDL_CondenserTypes.AIR_COOLED: 95,
    BDL_CondenserTypes.REMOTE_AIR_COOLED: 125,
    BDL_CondenserTypes.REMOTE_EVAP_COOLED: 105,
}
AHRI_550_590_2023_EVAP_LEAVING_T = 44
TYPICAL_IPLV_COND_ENTERING_T_BY_CONDENSER_TYPE = {
    BDL_CondenserTypes.WATER_COOLED: [85, 75, 65, 65],
    BDL_CondenserTypes.AIR_COOLED: [95, 80, 65, 55],
    BDL_CondenserTypes.REMOTE_AIR_COOLED: [125, 107.5, 90, 72.5],
    BDL_CondenserTypes.REMOTE_EVAP_COOLED: [105, 95, 85, 75],
}
ABSORP_ENG_IPLV_COND_ENTERING_T = {0.25: 70, 0.5: 70, 0.75: 75, 1: 85}

# Percent of time at each PLR 25%, 50%, 75%, 100%
IPLV_PART_LOAD_PCT_TIME = {0.25: 0.01, 0.50: 0.42, 0.75: 0.45, 1.0: 0.12}
PCT_ERROR_MARGIN = 0.015
MIN_AHRI_PART_LOAD = 0.25


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
        self.absorp_or_engine = False
        self.input_ratio_keyword = None

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
        if self.compressor_type_map.get(self.get_inp(BDL_ChillerKeywords.TYPE)) == OMIT:
            self.omit = True
            return

        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ABSOR_1,
            BDL_ChillerTypes.ABSOR_2,
            BDL_ChillerTypes.GAS_ABSOR,
            BDL_ChillerTypes.ENGINE,
        ]:
            self.absorp_or_engine = True

        self.input_ratio_keyword = (
            BDL_ChillerKeywords.HEAT_INPUT_RATIO
            if self.absorp_or_engine
            else BDL_ChillerKeywords.ELEC_INPUT_RATIO
        )
        requests = self.get_output_requests()
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

        if not self.absorp_or_engine:
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
            hw_loop = self.get_obj(
                self.get_obj(self.get_inp(BDL_ChillerKeywords.HW_LOOP))
            )

            if hw_loop:
                self.energy_source_type = self.get_loop_energy_source(hw_loop)

        chw_loop = self.get_obj(self.cooling_loop)
        self.design_leaving_evaporator_temperature = (
            self.try_float(chw_loop.get_inp(BDL_CirculationLoopKeywords.DESIGN_COOL_T))
            if chw_loop
            else None
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

        self.design_flow_evaporator = self.try_float(
            output_data.get("Design Parameters - Flow")
        )

        self.design_flow_condenser = self.try_float(
            output_data.get("Design Parameters - Condenser Flow")
        )

        self.is_chilled_water_pump_interlocked = bool(
            self.get_inp(BDL_ChillerKeywords.CHW_PUMP)
        )

        self.is_condenser_water_pump_interlocked = bool(
            self.get_inp(BDL_ChillerKeywords.CW_PUMP)
        )

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

        # Obtain the AHRI rated temperatures
        ahri_evaporator_leaving_t = AHRI_550_590_2023_EVAP_LEAVING_T
        ahri_condenser_entering_t = AHRI_550_590_2023_COND_ENTERING_T.get(
            self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        )

        performance_curve_data = self.get_performance_curve_data()

        are_curve_outputs_all_equal_to_one_at_ahri_temperatures = (
            curve_funcs.are_curve_outputs_all_equal_to_a_value_of_one(
                performance_curve_data,
                ahri_evaporator_leaving_t,
                ahri_condenser_entering_t,
                PCT_ERROR_MARGIN,
            )
        )
        # Checks if any of the performance curves were defined as data_input type of DATA or if the entered rated conditions match AHRI and if the performance curves are normalized to ahri conditions.
        curve_calcs_unavailable = not performance_curve_data["coefficients"] or (
            not self.are_user_defined_input_ratio_and_cap_at_ahri_rating_conditions()
            and not are_curve_outputs_all_equal_to_one_at_ahri_temperatures
        )

        if curve_calcs_unavailable:
            self.populate_full_load_eff_with_curve_calcs_unavailable(
                performance_curve_data["coefficients"]
            )

        else:
            # Capacity and efficiency are defined at AHRI conditions, so adjustments for rating conditions are not necessary
            if self.are_user_defined_input_ratio_and_cap_at_ahri_rating_conditions():
                self.populate_efficiency_when_user_defined_rated_temps_match_ahri(
                    performance_curve_data,
                    output_data,
                    are_curve_outputs_all_equal_to_one_at_ahri_temperatures,
                )

            # Capacity and efficiency are not defined at AHRI conditions, so adjustments for rating conditions must be made.
            else:
                self.populate_efficiency_when_user_defined_rated_temps_dont_match_ahri(
                    performance_curve_data, output_data
                )

    def get_output_requests(self):
        """Get output data requests for chiller object."""

        if not self.absorp_or_engine:
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

    def get_performance_curve_data(self) -> dict:
        """
        Retrieves performance curve objects along with their coefficient lists and output range values.

        This method gathers three performance curve objects corresponding to:
          - "cap_f_t": Capacity as a function of temperature.
          - "eff_f_t": Efficiency as a function of temperature (or Energy Input Ratio as a function of temperature for engine types).
          - "eff_f_plr": Efficiency as a function of part-load ratio.

        For each performance curve object, the method:
          1. Retrieves the object using the internal `get_obj(get_inp(...))` calls.
          2. Checks the curve's input type. If the input type is set to DATA (i.e., `BDL_CurveFitInputTypes.DATA`), the method returns
             the dictionary of curve objects immediately, along with empty dictionaries for the coefficients and output ranges.
          3. Otherwise, extracts the following details:
             - **Coefficients:** Retrieved via the 'COEF' keyword, converted to a list of floats, and stored in a dictionary
               with keys formatted as "<curve_key>_coeffs".
             - **Minimum Output:** Retrieved via the 'OUTPUT_MIN' keyword, converted to a float, and stored in a dictionary
               with keys formatted as "<curve_key>_min_otpt".
             - **Maximum Output:** Retrieved via the 'OUTPUT_MAX' keyword, converted to a float, and stored in a dictionary
               with keys formatted as "<curve_key>_max_otpt".

        Returns:
            tuple: A tuple of four dictionaries:
                - **coefficients (dict):** Maps string keys ("eff_f_t", "cap_f_t", "eff_f_plr") to their corresponding performance curve objects.
                - **coeffs (dict):** Maps string keys (formatted as "<curve_key>_coeffs") to lists of coefficient values (floats) for each curve.
                - **min_outputs (dict):** Maps string keys (formatted as "<curve_key>_min_otpt") to the minimum output values (floats) for each curve.
                - **max_outputs (dict):** Maps string keys (formatted as "<curve_key>_max_otpt") to the maximum output values (floats) for each curve.
        """
        perf_curves = {
            "cap_f_t": self.get_obj(self.get_inp(BDL_ChillerKeywords.CAPACITY_FT)),
            "eff_f_t": self.get_obj(
                self.get_inp(
                    BDL_ChillerKeywords.HIR_FT
                    if self.absorp_or_engine
                    else BDL_ChillerKeywords.EIR_FT
                )
            ),
            "eff_f_plr": self.get_obj(
                self.get_inp(
                    BDL_ChillerKeywords.HIR_FPLR
                    if self.absorp_or_engine
                    else BDL_ChillerKeywords.EIR_FPLR
                )
            ),
        }

        coefficients = {}
        min_outputs = {}
        max_outputs = {}
        for key, obj in perf_curves.items():
            input_type = obj.get_inp(BDL_CurveFitKeywords.INPUT_TYPE)
            if input_type == BDL_CurveFitInputTypes.DATA:
                return {
                    "performance_curves": perf_curves,
                    "coefficients": {},
                    "min_outputs": {},
                    "max_outputs": {},
                }

            coefficients[f"{key}_coeffs"] = list(
                map(float, obj.get_inp(BDL_CurveFitKeywords.COEF))
            )
            min_outputs[f"{key}_min_otpt"] = float(
                obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MIN)
            )
            max_outputs[f"{key}_max_otpt"] = float(
                obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MAX)
            )

        return {
            "performance_curves": perf_curves,
            "coefficients": coefficients,
            "min_outputs": min_outputs,
            "max_outputs": max_outputs,
        }

    def populate_iplv(self, performance_curve_data):
        """Populates IPLV based upon the modeled performance curves and the rated conditions.
        No corrections for fouling factor have been included - perhaps not relevant."""
        # TODO continued Do more testing to ensure it producing the correct results

        # If the chiller cannot be unloaded to all the IPLV load categories then do not perform calcs and return nothing
        if self.minimum_load_ratio > MIN_AHRI_PART_LOAD:
            return

        if not performance_curve_data["coefficients"]:
            return "Keyword DATA was used for coefficient determination"

        condenser_type = self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        ahri_evaporator_leaving_t = AHRI_550_590_2023_EVAP_LEAVING_T
        iplv_condenser_temp_conditions = (
            ABSORP_ENG_IPLV_COND_ENTERING_T
            if self.absorp_or_engine
            else TYPICAL_IPLV_COND_ENTERING_T_BY_CONDENSER_TYPE.get(condenser_type)
        )
        cap_f_t_curve = performance_curve_data["performance_curves"]["cap_f_t"]
        eff_f_t_curve_type = cap_f_t_curve.get_inp(BDL_CurveFitKeywords.TYPE)
        full_load_efficiency_rated = self.efficiency_metric_values[
            self.efficiency_metric_types.index(
                ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
            )
        ]

        # Dictionary of rated capacity as the key and efficiency result as the value. 0.0 as placeholder
        iplv_part_load_efficiencies = {plr: 0.0 for plr in IPLV_PART_LOAD_PCT_TIME}
        for plr in iplv_part_load_efficiencies:
            cond_entering_temp = iplv_condenser_temp_conditions[plr]

            results = curve_funcs.calculate_results_of_performance_curves(
                performance_curve_data,
                ahri_evaporator_leaving_t,
                cond_entering_temp,
                eff_f_t_curve_type,
                plr,
            )

            eff_f_t_result = results["eff_f_t_result"]
            eff_f_plr_result = results["eff_f_plr_result"]
            part_load_ratio = results["part_load_ratio"]

            eff_result_cop = part_load_ratio / (
                eff_f_t_result * eff_f_plr_result / full_load_efficiency_rated
            )

            iplv_part_load_efficiencies[plr] = eff_result_cop

        iplv = 0
        for plr in IPLV_PART_LOAD_PCT_TIME:
            weighted_eff_load = (
                IPLV_PART_LOAD_PCT_TIME[plr] * iplv_part_load_efficiencies[plr]
            )
            iplv = iplv + weighted_eff_load

        if iplv:
            self.efficiency_metric_values.append(iplv)
        self.efficiency_metric_types.append(
            ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
        )

    def populate_full_load_efficiency(self, curve_results):
        """Populates the full load efficiency for the chiller object."""
        user_defined_rated_plr = (
            self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_PLR)) or 1
        )

        user_defined_input_ratio = self.try_float(
            self.get_inp(self.input_ratio_keyword)
        )

        rated_full_load_cop = (
            curve_results["eff_f_t_result"]
            * curve_results["eff_f_plr_result"]
            / (user_defined_input_ratio * user_defined_rated_plr)
        )

        self.efficiency_metric_values.append(rated_full_load_cop)
        self.efficiency_metric_types.append(
            ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
        )

    def are_user_defined_input_ratio_and_cap_at_ahri_rating_conditions(self) -> bool:
        """Function compares the user defined rating conditions (evap leaving and condenser entering
        temperatures) associated with the user entered eff and capacity to AHRI 550 590-2023
        rated temperature conditions. Returns True if user defined (or eQuest defaults) match AHRI conditions.
        """
        user_defined_evaporator_leaving_t = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
        )
        user_defined_condenser_entering_t = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
        )
        rated_evaporator_leaving_temp = AHRI_550_590_2023_EVAP_LEAVING_T
        rated_condenser_entering_temp = AHRI_550_590_2023_COND_ENTERING_T.get(
            self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        )
        return (
            user_defined_evaporator_leaving_t == rated_evaporator_leaving_temp
            and user_defined_condenser_entering_t == rated_condenser_entering_temp
        )

    def populate_full_load_eff_with_curve_calcs_unavailable(self, coefficients):
        # Instead of setting these to AHRI conditions and adjusting capacity and efficiency to match AHRI conditions we just populate these as defined.
        if not coefficients:
            self.notes = "Performance curve INPUT-TYPE of DATA is not currently supported for determining and populating chiller IPLV."

        self.rated_leaving_evaporator_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
        )
        self.rated_entering_condenser_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
        )
        # If a hardcoded capacity does not exist then it will not be populated. Without usable performance curves we can't obtain this rated capacity for auto-sized equipment.
        self.rated_capacity = self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
        self.efficiency_metric_values.append(
            1 / self.try_float(self.get_inp(self.input_ratio_keyword))
        )
        (
            self.efficiency_metric_types.append(
                ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
            )
            if (self.are_user_defined_input_ratio_and_cap_at_ahri_rating_conditions())
            else self.efficiency_metric_types.append(
                ChillerEfficiencyMetricOptions.OTHER
            )
        )

    def populate_efficiency_when_user_defined_rated_temps_match_ahri(
        self,
        performance_curve_data,
        output_data,
        are_curve_outputs_all_equal_to_one_at_ahri_temperatures,
    ):
        # Assign AHRI conditions to these rated temperatures
        self.rated_leaving_evaporator_temperature = AHRI_550_590_2023_EVAP_LEAVING_T
        self.rated_entering_condenser_temperature = (
            AHRI_550_590_2023_COND_ENTERING_T.get(
                self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
            )
        )
        user_defined_rated_plr = (
            self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_PLR)) or 1
        )

        # Obtain results of curves at 100% load and AHRI temperature conditions
        curve_results_at_rated_conditions_and_100_percent_load = (
            curve_funcs.get_output_of_curves_at_temperature_and_load_conditions(
                performance_curve_data,
                self.rated_leaving_evaporator_temperature,
                self.rated_entering_condenser_temperature,
                1,
            )
        )
        cap_f_t_result = curve_results_at_rated_conditions_and_100_percent_load[
            "cap_f_t_result"
        ]

        # If capacity is hard coded and PLR RATED is entered (not n/a).
        if (
            self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr != 1
        ):
            # Obtain results of efficiency curves (not capacity curves) by plugging the user defined rated part load ratio into the curves equations
            efficiency_curve_result_rated_part_load = (
                curve_funcs.calculate_efficiency_at_part_load_ratio(
                    self.rated_leaving_evaporator_temperature,
                    self.rated_entering_condenser_temperature,
                    performance_curve_data["performance_curves"],
                    user_defined_rated_plr,
                )
            )

            user_defined_capacity = self.try_float(
                self.get_inp(BDL_ChillerKeywords.CAPACITY)
            )
            self.rated_capacity = curve_funcs.adjust_capacity_for_user_defined_plr(
                user_defined_rated_plr, user_defined_capacity, cap_f_t_result
            )

            self.populate_full_load_efficiency(efficiency_curve_result_rated_part_load)

            # Check that performance curves are normalized to 1 at ahri temperatures
            if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                self.populate_iplv(performance_curve_data)

        # If capacity is auto-sized and PLR RATED is entered (not n/a).
        elif (
            not self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr != 1
        ):
            # Obtain results of curves at 100% load and design temperature conditions
            curve_results_at_design_conditions_and_100_percent_load = (
                curve_funcs.get_output_of_curves_at_temperature_and_load_conditions(
                    performance_curve_data,
                    self.design_leaving_evaporator_temperature,
                    self.design_entering_condenser_temperature,
                    1,
                )
            )

            # Obtain results of efficiency curves (not capacity curves) by plugging the user defined rated part load ratio into the curves equations
            efficiency_curve_result_rated_part_load = (
                curve_funcs.calculate_efficiency_at_part_load_ratio(
                    self.rated_leaving_evaporator_temperature,
                    self.rated_entering_condenser_temperature,
                    performance_curve_data["performance_curves"],
                    user_defined_rated_plr,
                )
            )
            cap_f_t_result_design = (
                curve_results_at_design_conditions_and_100_percent_load[
                    "cap_f_t_result"
                ]
            )
            autosized_design_capacity = self.try_float(
                output_data.get("Primary Equipment (Chillers) - Capacity (Btu/hr)")
            )
            # Adjusts from design to rated conditions.
            self.rated_capacity = (
                autosized_design_capacity
                / cap_f_t_result_design
                / user_defined_rated_plr
            )

            self.populate_full_load_efficiency(efficiency_curve_result_rated_part_load)

            # Check that performance curves are normalized to 1 at ahri temperatures
            if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                self.populate_iplv(performance_curve_data)

        # If capacity is hard-coded and PLR Rated is n/a or 1
        elif (
            self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr == 1
        ):
            self.rated_capacity = self.try_float(
                self.get_inp(BDL_ChillerKeywords.CAPACITY)
            )
            self.efficiency_metric_values.append(
                1 / self.try_float(self.get_inp(self.input_ratio_keyword))
            )
            self.efficiency_metric_types.append(
                ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
            )

            # Check that performance curves are normalized to 1 at ahri temperatures
            if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                self.populate_iplv(performance_curve_data)

        #  If capacity is auto-sized and Rated is n/a or 1
        else:
            # Obtain results of curves at 100% load and design temperature conditions
            curve_results_at_design_conditions_and_100_percent_load = (
                curve_funcs.get_output_of_curves_at_temperature_and_load_conditions(
                    performance_curve_data,
                    self.design_leaving_evaporator_temperature,
                    self.design_entering_condenser_temperature,
                    1,
                )
            )
            cap_f_t_result_design = (
                curve_results_at_design_conditions_and_100_percent_load[
                    "cap_f_t_result"
                ]
            )

            autosized_design_capacity = self.try_float(
                output_data.get("Primary Equipment (Chillers) - Capacity (Btu/hr)")
            )
            # Adjusts from design to rated conditions.
            self.rated_capacity = autosized_design_capacity * (
                cap_f_t_result / cap_f_t_result_design
            )
            self.efficiency_metric_values.append(
                1 / self.try_float(self.get_inp(self.input_ratio_keyword))
            )
            self.efficiency_metric_types.append(
                ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY_RATED
            )

            # Check that performance curves are normalized to 1 at ahri temperatures
            if are_curve_outputs_all_equal_to_one_at_ahri_temperatures:
                self.populate_iplv(performance_curve_data)

    def populate_efficiency_when_user_defined_rated_temps_dont_match_ahri(
        self, performance_curve_data, output_data
    ):
        # The curves are used to adjust values (cap and eff) to AHRI conditions so rated temps are set to AHRI temperatures even though these were not entered in the UI.
        self.rated_leaving_evaporator_temperature = AHRI_550_590_2023_EVAP_LEAVING_T
        self.rated_entering_condenser_temperature = (
            AHRI_550_590_2023_COND_ENTERING_T.get(
                self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
            )
        )
        user_defined_rated_plr = (
            self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_PLR)) or 1
        )

        # Obtain results of curves at 100% load and entered rated (non AHRI) temperature conditions
        curve_results_at_user_defined_conditions_and_full_load = (
            curve_funcs.get_output_of_curves_at_temperature_and_load_conditions(
                performance_curve_data,
                self.rated_leaving_evaporator_temperature,
                self.rated_entering_condenser_temperature,
                1,
            )
        )
        # Obtain results of curves at 100% load and design temperature conditions
        curve_results_at_design_conditions_and_full_load = (
            curve_funcs.get_output_of_curves_at_temperature_and_load_conditions(
                performance_curve_data,
                self.design_leaving_evaporator_temperature,
                self.design_entering_condenser_temperature,
                1,
            )
        )
        # Obtain results of efficiency curves (not capacity curves) by plugging the user defined rated part load ratio into the curves equations
        curve_results_at_user_defined_part_load_rating = (
            curve_funcs.calculate_efficiency_at_part_load_ratio(
                self.rated_leaving_evaporator_temperature,
                self.rated_entering_condenser_temperature,
                performance_curve_data["performance_curves"],
                user_defined_rated_plr,
            )
        )

        cap_f_t_result_user_defined_temps_full_load = (
            curve_results_at_user_defined_conditions_and_full_load["cap_f_t_result"]
        )
        cap_f_t_result_design = curve_results_at_design_conditions_and_full_load[
            "cap_f_t_result"
        ]

        # If capacity is hard coded and PLR RATED is entered (not n/a). (This is the same as used above for when it is at AHRI)
        if (
            self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr != 1
        ):
            user_defined_capacity = self.try_float(
                self.get_inp(BDL_ChillerKeywords.CAPACITY)
            )
            self.rated_capacity = curve_funcs.adjust_capacity_for_user_defined_plr(
                user_defined_rated_plr,
                user_defined_capacity,
                cap_f_t_result_user_defined_temps_full_load,
            )
            self.populate_full_load_efficiency(
                curve_results_at_user_defined_part_load_rating
            )
            self.populate_iplv(performance_curve_data)

        # If capacity is auto-sized and PLR RATED is entered (not n/a). (This is the same as used above for when it is at AHRI)
        elif (
            not self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr != 1
        ):
            autosized_design_capacity = self.try_float(
                output_data.get("Primary Equipment (Chillers) - Capacity (Btu/hr)")
            )
            # Adjusts from design to rated conditions.
            self.rated_capacity = (
                autosized_design_capacity
                * cap_f_t_result_design
                / user_defined_rated_plr
            )
            self.populate_full_load_efficiency(
                curve_results_at_user_defined_part_load_rating
            )
            self.populate_iplv(performance_curve_data)

        # If capacity is hard-coded and PLR Rated is n/a or 1 (Differs from AHRI section above. It may be because curves = 1 at ahri so it may actually be the same)
        elif (
            self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
            and user_defined_rated_plr == 1
        ):
            self.rated_capacity = (
                self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY))
                / cap_f_t_result_user_defined_temps_full_load
            )

            self.populate_full_load_efficiency(
                curve_results_at_user_defined_conditions_and_full_load
            )
            self.populate_iplv(performance_curve_data)

        #  If capacity is auto-sized and Rated is n/a or 1
        else:
            autosized_design_capacity = self.try_float(
                output_data.get("Primary Equipment (Chillers) - Capacity (Btu/hr)")
            )
            # Adjusts from design to rated conditions. (Differs from AHRI section above. It may be because curves = 1 at ahri so it may actually be the same)
            self.rated_capacity = autosized_design_capacity * (
                cap_f_t_result_user_defined_temps_full_load / cap_f_t_result_design
            )
            self.populate_full_load_efficiency(
                curve_results_at_user_defined_conditions_and_full_load
            )
            self.populate_iplv(performance_curve_data)
