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
OMIT = "OMIT"


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
        # TODO Decide whether to populate full_load_efficiency no matter the rating conditions entered. Maybe populate now that you have the
        # TODO continued function to adjust from entered to rated conditions
        if not absorp_or_engine:
            self.energy_source_type = EnergySourceOptions.ELECTRICITY
            if self.is_rated_full_load_eff_defined_at_ahri_rating_conditions():
                self.efficiency_metric_values.append(
                    1
                    / self.try_float(self.get_inp(BDL_ChillerKeywords.ELEC_INPUT_RATIO))
                )
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY
                )
            else:
                self.notes = ""
        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ENGINE,
            BDL_ChillerTypes.GAS_ABSOR,
        ]:
            self.energy_source_type = EnergySourceOptions.NATURAL_GAS
            if self.is_rated_full_load_eff_defined_at_ahri_rating_conditions():
                self.efficiency_metric_values.append(
                    1
                    / self.try_float(self.get_inp(BDL_ChillerKeywords.HEAT_INPUT_RATIO))
                )
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY
                )
        elif self.get_inp(BDL_ChillerKeywords.TYPE) in [
            BDL_ChillerTypes.ABSOR_1,
            BDL_ChillerTypes.ABSOR_2,
        ]:
            hot_water_loop_name = self.get_obj(
                self.get_inp(BDL_ChillerKeywords.HW_LOOP)
            )
            hot_water_loop = self.get_obj(hot_water_loop_name)
            if self.is_rated_full_load_eff_defined_at_ahri_rating_conditions():
                self.efficiency_metric_values.append(
                    1
                    / self.try_float(self.get_inp(BDL_ChillerKeywords.HEAT_INPUT_RATIO))
                )
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.FULL_LOAD_EFFICIENCY
                )
            if hot_water_loop:
                self.energy_source_type = self.get_loop_energy_source(hot_water_loop)

        # This value comes out in Btu/hr
        self.design_capacity = self.try_float(
            output_data.get("Design Parameters - Capacity")
        )

        # TODO modify this to reference the input instead of this output
        # TODO Update to use the entered capacity if populated and if autosized to reference PV-A?
        # TODO Need to check the capacity that is actually used on an hour basis
        # TODO Rated capacity is defined at a PLR in eQuest, default is 0.92. If it isnot manually entered assume 0.92.
        # TODO If capacity is hard coded then rated capacity at 100% PLR is the entered rated capacity divided by the PLR rated from eQuest.
        # TODO If capacity is autosized then need to obtain the design capacity and design conditions and then convert it to AHRI conditions
        # TODO Apply the following formula to autosized design cap to convert to rated (1/PLR rated) * (1/(Capft at design conditions/Capft rated conditions))
        # TODO All of this is based on seeing what is used in hourly reports

        rated_part_load_ratio = self.try_float(self.get_inp(BDL_ChillerKeywords.RATED_PLR))
        # If capacity is hard coded, then rated capacity at 100% PLR is the entered rated capacity divided by the PLR rated entered in eQuest.
        if self.try_float(self.get_inp(BDL_ChillerKeywords.CAPACITY)):
            self.rated_capacity = self.try_float(
                self.get_inp(BDL_ChillerKeywords.CAPACITY)
            )/rated_part_load_ratio
        else:
            #TODO created a function to convert capacity
            self.rated_capacity = self.try_float(
                output_data.get("Primary Equipment (Chillers) - Capacity (Btu/hr)")
            )/1000000
            self.rated_capacity = self.convert_capacity_from_design_to_rated_conditions(absorp_or_engine)

        self.design_flow_evaporator = self.try_float(
            output_data.get("Design Parameters - Flow")
        )

        self.design_flow_condenser = self.try_float(
            output_data.get("Design Parameters - Condenser Flow")
        )

        self.rated_leaving_evaporator_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
        )

        self.rated_entering_condenser_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
        )

        self.design_leaving_evaporator_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.DESIGN_CHW_T)
        )

        self.design_entering_condenser_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.DESIGN_COND_T)
        )

        self.minimum_load_ratio = self.try_float(
            self.get_inp(BDL_ChillerKeywords.MIN_RATIO)
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

        iplv_value = self.calculate_iplv(absorp_or_engine)
        # TODO modify this because now the entered conditions are converted to rated when calculating IPLV so this can always be populated as IPLV
        if self.is_rated_full_load_eff_defined_at_ahri_rating_conditions():
            if (
                iplv_value
                and iplv_value != "Keyword DATA was used for coefficient determination"
            ):
                self.efficiency_metric_values.append(iplv_value)
                self.efficiency_metric_types.append(
                    ChillerEfficiencyMetricOptions.INTEGRATED_PART_LOAD_VALUE
                )
            else:
                self.notes = "Performance curve INPUT-TYPE of DATA is not currently supported for determining and populating chiller IPLV."
        elif (
            iplv_value
            and iplv_value != "Keyword DATA was used for coefficient determination"
        ):
            self.efficiency_metric_values.append(iplv_value)
            self.efficiency_metric_types.append(ChillerEfficiencyMetricOptions.OTHER)
        else:
            self.notes = "Performance curve INPUT-TYPE of DATA is not currently supported for determining and populating chiller IPLV."

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

    def get_dict_of_curve_coefficient_mins_and_maxs(self, absorp_or_engine):
        cap_ft = self.get_obj(self.get_inp(BDL_ChillerKeywords.CAPACITY_FT))

        if not absorp_or_engine:
            eff_ft_key = BDL_ChillerKeywords.EIR_FT
            eff_fplr_key = BDL_ChillerKeywords.EIR_FPLR
        else:
            eff_ft_key = BDL_ChillerKeywords.HIR_FT
            eff_fplr_key = BDL_ChillerKeywords.HIR_FPLR

        eff_ft = self.get_obj(self.get_inp(eff_ft_key))
        eff_fplr = self.get_obj(self.get_inp(eff_fplr_key))

        # TODO: Ensure the coefficients actually used in the model align with those calculated in the UI when the INPUT-TYPE is DATA instead of COEFFICIENTS.

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

    def calculate_iplv(self, absorp_or_engine):
        """Calculates IPLV based upon the modeled performance curves and the rated conditions and entered efficiency.
        No corrections for fouling factor have been included - perhaps not relevant."""
        # TODO incorporate the E+ logic where it accounts for minimum load ratio.
        # TODO continued Do more testing to ensure it producing the correct results
        # ToDO continued also for full load and IPLV set up to handle if you do not know rated conditions

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

        # Evaporator leaving temperature (a.k.a chilled water supply temperature). 44F AHRI 550 and 560 rated conditions.
        evap_leaving_temp_entered = self.rated_leaving_evaporator_temperature
        evap_leaving_temp_rated = 44

        cond_entering_temp_entered = self.rated_entering_condenser_temperature
        cond_entering_temp_rated = (
            condenser_type_iplv_rating_condenser_temp_conditions_map[condenser_type][0]
        )

        if not absorp_or_engine:
            condenser_type_iplv_rating_condenser_temp_conditions = (
                condenser_type_iplv_rating_condenser_temp_conditions_map[condenser_type]
            )
        else:
            condenser_type_iplv_rating_condenser_temp_conditions = [85, 75, 70, 70]

        iplv_percent_of_operation_at_each_load = [0.01, 0.42, 0.45, 0.12]

        coefficients, coeffs, min_outputs, max_outputs = self.get_dict_of_curve_coefficient_mins_and_maxs(absorp_or_engine)

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

        full_load_efficiency_entered = (
            1 / self.try_float(self.get_inp(BDL_ChillerKeywords.ELEC_INPUT_RATIO))
            if not absorp_or_engine
            else self.try_float(1 / self.get_inp(BDL_ChillerKeywords.HEAT_INPUT_RATIO))
        )
        capacity_entered = self.rated_capacity

        # Returns a list with the rated capacity as index 1 and rated efficiency as index 0. If the capacity and efficiency were
        # defined at rated conditions the function should return the same rated as entered values.
        capacity_and_full_load_efficiency_at_rated_conditions = (
            curve_funcs.convert_cop_and_capacity_to_different_conditions(
                coefficients,
                evap_leaving_temp_entered,
                cond_entering_temp_entered,
                evap_leaving_temp_rated,
                cond_entering_temp_rated,
                full_load_efficiency_entered,
                capacity_entered,
            )
        )
        full_load_efficiency_rated = (
            capacity_and_full_load_efficiency_at_rated_conditions[0]
        )

        for index, key in enumerate(iplv_rating_load_conditions):
            cond_entering_temp = condenser_type_iplv_rating_condenser_temp_conditions[
                index
            ]
            # Returns
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

    def is_rated_full_load_eff_defined_at_ahri_rating_conditions(self):
        rated_evaporator_leaving_temp = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_CHW_T)
        )
        rated_condenser_temperature = self.try_float(
            self.get_inp(BDL_ChillerKeywords.RATED_COND_T)
        )

        condenser_type = self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        condenser_type_rating_condenser_temp_conditions_map = {
            BDL_CondenserTypes.WATER_COOLED: 85,
            BDL_CondenserTypes.AIR_COOLED: 95,
            BDL_CondenserTypes.REMOTE_AIR_COOLED: 125,
            BDL_CondenserTypes.REMOTE_EVAP_COOLED: 105,
        }

        is_rated_full_load_eff_defined_at_ahri_rating_conditions = (
            rated_evaporator_leaving_temp == 44
            and rated_condenser_temperature
            == condenser_type_rating_condenser_temp_conditions_map[condenser_type]
        )

        return is_rated_full_load_eff_defined_at_ahri_rating_conditions

    def convert_capacity_from_design_to_rated_conditions(self, absorp_or_engine):

        coefficients, coeffs, min_outputs, max_outputs = self.get_dict_of_curve_coefficient_mins_and_maxs(absorp_or_engine)

        condenser_type = self.get_inp(BDL_ChillerKeywords.CONDENSER_TYPE)
        condenser_type_rating_condenser_temp_conditions_map = {
            BDL_CondenserTypes.WATER_COOLED: 85,
            BDL_CondenserTypes.AIR_COOLED: 95,
            BDL_CondenserTypes.REMOTE_AIR_COOLED: 125,
            BDL_CondenserTypes.REMOTE_EVAP_COOLED: 105,
        }
        #TODO Work out how to get the design temperatures. They are coming in as None.
        rated_evaporator_leaving_temp = 44
        rated_condenser_temperature = condenser_type_rating_condenser_temp_conditions_map[condenser_type]
        a = self.try_float(
                    self.get_inp(BDL_ChillerKeywords.DESIGN_CHW_T)
                )
        b = self.try_float(
                    self.get_inp(BDL_ChillerKeywords.DESIGN_COND_T)
                )

        capacity_and_full_load_efficiency_at_rated_conditions = (
            curve_funcs.convert_cop_and_capacity_to_different_conditions(
                coefficients,
                a,
                b,
                rated_evaporator_leaving_temp,
                rated_condenser_temperature,
                1,
                self.rated_capacity,
            )
        )

        return capacity_and_full_load_efficiency_at_rated_conditions[1]


