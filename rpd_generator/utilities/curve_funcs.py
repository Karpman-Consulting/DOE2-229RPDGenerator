from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums
from rpd_generator.utilities import curve_funcs

BDL_CurveFitKeywords = BDLEnums.bdl_enums["CurveFitKeywords"]
BDL_CurveFitInputTypes = BDLEnums.bdl_enums["CurveFitInputTypes"]
BDL_CurveFitTypes = BDLEnums.bdl_enums["CurveFitTypes"]


def calculate_bi_quadratic(
    curve_coeffs: list, x: float, y: float, min_val: float, max_val: float
) -> float:
    """Function takes a list of curve coefficients with a = 0 index and f = 5th index and two independent variables x and y.
    Function then computes and returns Z = a + b * x + c * x^2 + d * y + e * y^2 + f * x * y ensuring z is within the range min_val and max_val
    This function works for any eQuest BI-QUADRATIC curve
    """
    z = (
        curve_coeffs[0]
        + curve_coeffs[1] * x
        + curve_coeffs[2] * x**2
        + curve_coeffs[3] * y
        + curve_coeffs[4] * y**2
        + curve_coeffs[5] * x * y
    )

    # Ensure z is within the range [min_val, max_val]
    z = max(min_val, min(z, max_val))

    return z


def calculate_cubic(
    curve_coeffs: list, x: float, min_val: float, max_val: float
) -> float:
    """Function takes a list of curve coefficients with a = 0 index and d = 3rd index and an independent variable X.
    Function then computes and returns Z = a + b * X + c * X^2 + d * X^3 ensuring z is within the range min_val and max_val
    """
    z = (
        curve_coeffs[0]
        + curve_coeffs[1] * x
        + curve_coeffs[2] * x**2
        + curve_coeffs[3] * x**3
    )

    # Ensure z is within the range [min_val, max_val]
    z = max(min_val, min(z, max_val))

    return z


def calculate_quadratic(
    curve_coeffs: list, x: float, min_val: float, max_val: float
) -> float:
    """Function takes a list of curve coefficients with a = 0 index and c = 2nd index and an independent variable X.
    Function then computes and returns Z = a + b * X + c * X^2 ensuring z is within the range min_val and max_val
    """
    z = curve_coeffs[0] + curve_coeffs[1] * x + curve_coeffs[2] * x**2

    # Ensure z is within the range [min_val, max_val]
    z = max(min_val, min(z, max_val))

    return z


def convert_cop_and_capacity_to_different_conditions(
    curves: dict,
    evap_leaving_temp_starting_condition: float,
    condenser_entering_temp_starting_condition: float,
    evap_leaving_temp_new_condition: float,
    condenser_entering_temp_new_condition: float,
    cop_starting_condition: float,
    capacity_starting_condition: float,
) -> list:
    """The curves dictionary should contain the following keys eff_ft, cap_ft, eff_fplr which should have the curve objects as values.
    evap_leaving_temp_starting_condition is the evaporator leaving temp in which the cop_starting_condition and capacity_starting_condition are defined
    condenser_entering_temp_starting_condition is the condenser entering temp in which the cop_starting_condition and capacity_starting_condition are defined. These
    temperatures were likely entered in eQuest for the rated temperatures for the capacity and efficiency but they do not have to be. evap_leaving_temp_new_condition is the
    temperature condition that the efficiency and capacity are being converted to. Sme with condenser_entering_temp_new_condition.
    cop_starting_condition and capacity_starting_condition will be adjusted. This function returns a list with the first index being the adjusted COP and the second being the adjusted capacity. This assumes 100% load.
    """

    coeffs = {}
    min_outputs = {}
    max_outputs = {}

    for key, obj in curves.items():
        input_type = obj.get_inp(BDL_CurveFitKeywords.INPUT_TYPE)
        if input_type == BDL_CurveFitInputTypes.DATA:
            # Currently, we are unable to obtain the curve coefficients when DATA is the input_type
            return ["Keyword DATA was used for coefficient determination"]
        coeffs[f"{key}_coeffs"] = list(
            map(float, obj.get_inp(BDL_CurveFitKeywords.COEF))
        )
        min_outputs[f"{key}_min_otpt"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MIN)
        )
        max_outputs[f"{key}_max_otpt"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MAX)
        )

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

    eff_fplr_curve_type = curves["cap_ft"].get_inp(BDL_CurveFitKeywords.TYPE)

    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
    }

    data_starting_condition = {
        "evap_leaving_temp": evap_leaving_temp_starting_condition,
        "condenser_entering_temp": condenser_entering_temp_starting_condition,
    }

    data_new_condition = {
        "evap_leaving_temp": evap_leaving_temp_new_condition,
        "condenser_entering_temp": condenser_entering_temp_new_condition,
    }

    load_percent = 1.0
    # Calculate and retrieve the results
    all_results = execute_calculations(
        data_starting_condition,
        data_new_condition,
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
        load_percent,
    )

    capacity_adjusted_to_new_condition = capacity_starting_condition / (
        all_results["entered_results"]["cap_ft_result"]
        / all_results["rated_results"]["cap_ft_result"]
    )
    helper_multiplier_starting_condition = (
        all_results["entered_results"]["eff_ft_result"]
        * all_results["entered_results"]["eff_fplr_result"]
    ) / all_results["entered_results"]["part_load_ratio"]
    helper_multiplier_new_condition = (
        all_results["rated_results"]["eff_ft_result"]
        * all_results["rated_results"]["eff_fplr_result"]
    ) / all_results["rated_results"]["part_load_ratio"]
    efficiency_adjusted_to_new_condition = cop_starting_condition * (
        helper_multiplier_starting_condition / helper_multiplier_new_condition
    )

    return [efficiency_adjusted_to_new_condition, capacity_adjusted_to_new_condition]


def calculate_results_of_performance_curves(
    evap_leaving_temp,
    condenser_entering_temp,
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
    load_percent,
):
    """Returns the results of performance curves and partload ratio for cap_ft, eir_PLR, eir_ft"""
    cap_ft_result = curve_funcs.calculate_bi_quadratic(
        cap_ft_coeffs,
        evap_leaving_temp,
        condenser_entering_temp,
        cap_ft_min_otpt,
        cap_ft_max_otpt,
    )
    eff_ft_result = curve_funcs.calculate_bi_quadratic(
        eff_ft_coeffs,
        evap_leaving_temp,
        condenser_entering_temp,
        eff_ft_min_otpt,
        eff_ft_max_otpt,
    )
    part_load_ratio = (1 / cap_ft_result) * load_percent

    if eff_fplr_curve_type in curve_function_map:
        eff_fplr_result = curve_function_map[eff_fplr_curve_type](
            eff_fplr_coeffs,
            part_load_ratio,
            eff_fplr_min_otpt,
            eff_fplr_max_otpt,
        )
    else:
        delta_temp = condenser_entering_temp - evap_leaving_temp
        eff_fplr_result = curve_funcs.calculate_bi_quadratic(
            eff_fplr_coeffs,
            part_load_ratio,
            delta_temp,
            eff_fplr_min_otpt,
            eff_fplr_max_otpt,
        )
    results = {
        "cap_ft_result": cap_ft_result,
        "eff_ft_result": eff_ft_result,
        "part_load_ratio": part_load_ratio,
        "eff_fplr_result": eff_fplr_result,
    }
    return results


def execute_calculations(
    data_starting_condition,
    data_new_condition,
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
    load_percent,
):
    # Calculate with "entered" variables
    entered_results = calculate_results_of_performance_curves(
        data_starting_condition["evap_leaving_temp"],
        data_starting_condition["condenser_entering_temp"],
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
        load_percent,
    )

    # Calculate with "rated" variables
    rated_results = calculate_results_of_performance_curves(
        data_new_condition["evap_leaving_temp"],
        data_new_condition["condenser_entering_temp"],
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
        load_percent,
    )

    # Return a dictionary of all results
    return {"entered_results": entered_results, "rated_results": rated_results}


def are_curve_outputs_all_equal_to_a_value_of_one(
    curves: dict,
    evap_leaving_temp: float,
    condenser_entering_temp: float,
    percent_margin_of_error: float,
):
    """ This assumes 100% load. The function checks whether the output of each curve is equal to 1 with the specified margin of error.
    The function returns a True or False. This was created to assess cap_ft, eff_ct, and eir_fplr curves only. The margin of error
    is expected to be a number from 0 to 100 (not a fraction). Default based on observations of curves 1.5.
        """

    coeffs = {}
    min_outputs = {}
    max_outputs = {}

    for key, obj in curves.items():
        input_type = obj.get_inp(BDL_CurveFitKeywords.INPUT_TYPE)
        if input_type == BDL_CurveFitInputTypes.DATA:
            # Currently, we are unable to obtain the curve coefficients when DATA is the input_type
            return ["Keyword DATA was used for coefficient determination"]
        coeffs[f"{key}_coeffs"] = list(
            map(float, obj.get_inp(BDL_CurveFitKeywords.COEF))
        )
        min_outputs[f"{key}_min_otpt"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MIN)
        )
        max_outputs[f"{key}_max_otpt"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MAX)
        )

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

    eff_fplr_curve_type = curves["cap_ft"].get_inp(BDL_CurveFitKeywords.TYPE)

    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
    }

    load_percent = 1

    # Calculate and retrieve the results
    results = calculate_results_of_performance_curves(
        evap_leaving_temp,
        condenser_entering_temp,
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
        load_percent,
    )

    result_cap_ft = results["cap_ft_result"]
    result_eff_ft = results["eff_ft_result"]
    result_eff_plr = results["eff_fplr_result"]
    result_plr = results["part_load_ratio"]

    is_cap_ft_within_margin = is_within_margin(result_cap_ft, 1, percent_margin_of_error)
    is_eff_ft_within_margin = is_within_margin(result_eff_ft, 1, percent_margin_of_error)
    is_eff_plr_within_margin = is_within_margin(result_eff_plr, 1, percent_margin_of_error)

    all_within_margin = all([is_cap_ft_within_margin, is_eff_ft_within_margin, is_eff_plr_within_margin])

    return all_within_margin


def is_within_margin(value, target, percent_margin):
    lower_bound = target * (1 - percent_margin / 100)
    upper_bound = target * (1 + percent_margin / 100)
    return lower_bound <= value <= upper_bound


def adjust_capacity_for_entered_plr(plr_rated: float, capacity: float, capft_result: float):
    """ Function adjusts capacity for the situation when part load ratio rated in defined.
    This formula adjusts to AHRI rated conditions. plr_rated is the part load ratio defined in the
    eQuest UI. Capacity is the unadjusted capacity. cap_ft_result is the results of the capacity as
    a function of temperature curve"""

    capacity_adj = capacity * (1/capft_result) * (1/plr_rated)

    return capacity_adj

def calculate_results_of_efficiency_performance_curves_with_specific_part_load_ratio(
    evap_leaving_temp,
    condenser_entering_temp,
    curves: dict,
    part_load_ratio,
):

    # Coefficients, min_outputs, and max_outputs dictionaries
    eff_ft_coeffs = coeffs["eff_ft_coeffs"]
    eff_fplr_coeffs = coeffs["eff_fplr_coeffs"]

    eff_ft_min_otpt = min_outputs["eff_ft_min_otpt"]
    eff_ft_max_otpt = max_outputs["eff_ft_max_otpt"]
    eff_fplr_min_otpt = min_outputs["eff_fplr_min_otpt"]
    eff_fplr_max_otpt = max_outputs["eff_fplr_max_otpt"]

    eff_fplr_curve_type = curves["cap_ft"].get_inp(BDL_CurveFitKeywords.TYPE)

    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
    }


    eff_ft_result = curve_funcs.calculate_bi_quadratic(
        eff_ft_coeffs,
        evap_leaving_temp,
        condenser_entering_temp,
        eff_ft_min_otpt,
        eff_ft_max_otpt,
    )


    if eff_fplr_curve_type in curve_function_map:
        eff_fplr_result = curve_function_map[eff_fplr_curve_type](
            eff_fplr_coeffs,
            part_load_ratio,
            eff_fplr_min_otpt,
            eff_fplr_max_otpt,
        )
    else:
        delta_temp = condenser_entering_temp - evap_leaving_temp
        eff_fplr_result = curve_funcs.calculate_bi_quadratic(
            eff_fplr_coeffs,
            part_load_ratio,
            delta_temp,
            eff_fplr_min_otpt,
            eff_fplr_max_otpt,
        )
    results = {
        "eff_ft_result": eff_ft_result,
        "eff_fplr_result": eff_fplr_result,
    }
    return results