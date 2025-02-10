from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


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


def calculate_results_of_performance_curves(
    performance_curve_data,
    evap_leaving_temp,
    condenser_entering_temp,
    eff_f_plr_curve_type,
    load_percent,
):
    """Returns the results of performance curves and partload ratio for cap_f_t, eir_PLR, eir_f_t"""
    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: calculate_cubic,
    }
    coefficients = performance_curve_data["coefficients"]
    min_outputs = performance_curve_data["min_outputs"]
    max_outputs = performance_curve_data["max_outputs"]

    cap_f_t_result = calculate_bi_quadratic(
        coefficients["cap_f_t_coeffs"],
        evap_leaving_temp,
        condenser_entering_temp,
        min_outputs["cap_f_t_min_output"],
        max_outputs["cap_f_t_max_output"],
    )
    eff_f_t_result = calculate_bi_quadratic(
        coefficients["eff_f_t_coeffs"],
        evap_leaving_temp,
        condenser_entering_temp,
        min_outputs["eff_f_t_min_output"],
        max_outputs["eff_f_t_max_output"],
    )
    part_load_ratio = (1 / cap_f_t_result) * load_percent

    if eff_f_plr_curve_type in curve_function_map:
        eff_f_plr_result = curve_function_map[eff_f_plr_curve_type](
            coefficients["eff_f_plr_coeffs"],
            part_load_ratio,
            min_outputs["eff_f_plr_min_output"],
            max_outputs["eff_f_plr_max_output"],
        )
    else:
        delta_temp = condenser_entering_temp - evap_leaving_temp
        eff_f_plr_result = calculate_bi_quadratic(
            coefficients["eff_f_plr_coeffs"],
            part_load_ratio,
            delta_temp,
            min_outputs["eff_f_plr_min_output"],
            max_outputs["eff_f_plr_max_output"],
        )
    results = {
        "cap_f_t_result": cap_f_t_result,
        "eff_f_t_result": eff_f_t_result,
        "part_load_ratio": part_load_ratio,
        "eff_f_plr_result": eff_f_plr_result,
    }
    return results


def execute_calculations(
    performance_curve_data,
    data_starting_condition,
    data_new_condition,
    eff_f_plr_curve_type,
    load_percent,
):
    # Calculate with "entered" variables
    entered_results = calculate_results_of_performance_curves(
        performance_curve_data,
        data_starting_condition["evap_leaving_temp"],
        data_starting_condition["condenser_entering_temp"],
        eff_f_plr_curve_type,
        load_percent,
    )

    # Calculate with "rated" variables
    rated_results = calculate_results_of_performance_curves(
        performance_curve_data,
        data_new_condition["evap_leaving_temp"],
        data_new_condition["condenser_entering_temp"],
        eff_f_plr_curve_type,
        load_percent,
    )

    # Return a dictionary of all results
    return {"entered_results": entered_results, "rated_results": rated_results}


def are_curve_outputs_all_equal_to_a_value_of_one(
    performance_curve_data: dict,
    evap_leaving_temp: float,
    condenser_entering_temp: float,
    percent_margin_of_error: float,
) -> [bool, None]:
    """This assumes 100% load. The function checks whether the output of each curve is equal to 1 with the specified margin of error.
    The function returns a True or False. This was created to assess cap_f_t, eff_ct, and eir_f_plr curves only. The margin of error
    is expected to be a number from 0 to 100 (not a fraction). Default based on observations of curves 1.5.
    """

    eff_f_plr_curve_type = performance_curve_data["performance_curves"][
        "cap_f_t"
    ].get_inp(BDL_CurveFitKeywords.TYPE)

    load_percent = 1

    # Calculate and retrieve the results
    results = calculate_results_of_performance_curves(
        performance_curve_data["performance_curves"],
        evap_leaving_temp,
        condenser_entering_temp,
        eff_f_plr_curve_type,
        load_percent,
    )

    is_cap_f_t_within_margin = is_within_margin(
        results["cap_f_t_result"], 1, percent_margin_of_error
    )
    is_eff_f_t_within_margin = is_within_margin(
        results["eff_f_t_result"], 1, percent_margin_of_error
    )
    is_eff_plr_within_margin = is_within_margin(
        results["eff_f_plr_result"], 1, percent_margin_of_error
    )

    return all(
        [is_cap_f_t_within_margin, is_eff_f_t_within_margin, is_eff_plr_within_margin]
    )


def is_within_margin(value, target, percent_margin):
    lower_bound = target * (1 - percent_margin)
    upper_bound = target * (1 + percent_margin)
    return lower_bound <= value <= upper_bound


def adjust_capacity_for_entered_plr(
    plr_rated: float, capacity: float, capft_result: float
):
    """Function adjusts capacity for the situation when part load ratio rated in defined.
    This formula adjusts to AHRI rated conditions. plr_rated is the part load ratio defined in the
    eQuest UI. Capacity is the unadjusted capacity. cap_f_t_result is the results of the capacity as
    a function of temperature curve"""

    capacity_adj = capacity * (1 / capft_result) * (1 / plr_rated)

    return capacity_adj


def calculate_efficiency_at_part_load_ratio(
    evap_leaving_temp: int,
    condenser_entering_temp: int,
    curves: dict,
    part_load_ratio: float,
):
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
        min_outputs[f"{key}_min_output"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MIN)
        )
        max_outputs[f"{key}_max_output"] = float(
            obj.get_inp(BDL_CurveFitKeywords.OUTPUT_MAX)
        )

    eff_f_plr_curve_type = curves["cap_f_t"].get_inp(BDL_CurveFitKeywords.TYPE)

    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: calculate_cubic,
    }

    eff_f_t_result = calculate_bi_quadratic(
        coeffs["eff_f_t_coeffs"],
        evap_leaving_temp,
        condenser_entering_temp,
        min_outputs["eff_f_t_min_output"],
        max_outputs["eff_f_t_max_output"],
    )

    if eff_f_plr_curve_type in curve_function_map:
        eff_f_plr_result = curve_function_map[eff_f_plr_curve_type](
            coeffs["eff_f_plr_coeffs"],
            part_load_ratio,
            min_outputs["eff_f_plr_min_output"],
            max_outputs["eff_f_plr_max_output"],
        )
    else:
        chw_delta_t = condenser_entering_temp - evap_leaving_temp
        eff_f_plr_result = calculate_bi_quadratic(
            coeffs["eff_f_plr_coeffs"],
            part_load_ratio,
            chw_delta_t,
            min_outputs["eff_f_plr_min_output"],
            max_outputs["eff_f_plr_max_output"],
        )
    results = {
        "eff_f_t_result": eff_f_t_result,
        "eff_f_plr_result": eff_f_plr_result,
    }
    return results
