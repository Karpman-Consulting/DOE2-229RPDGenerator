from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums
rom rpd_generator.utilities import curve_funcs

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


def convert_cop_and_capacity_to_ahri_conditions(
    curves: dict,
    evap_leaving_temp_entered: float,
    condenser_entering_temp_entered: float,
    evap_leaving_temp_rated: float,
    condenser_entering_temp_rated: float,
    cop_entered: float,
    capacity_entered: float,
) -> list:
    """The curves dictionary should contain the following keys eff_ft, cap_ft, eff_fplr which should have the curve objects as values.
    evap_leaving_temp_entered is the evaporator leaving temp in which the user defined efficiency and capacity and
    condenser_entering_temp_entered is the condenser entering temp in which the user defined efficiency and capacity. These
    temperatures were entered in eQuest for the rated temperatures for the capacity and efficiency. evap_leaving_temp_rated is the evaporator
    leaving temp at actual AHRI rating conditions and condenser_entering_temp_rated is the condenser entering temp at actual AHRI rated conditions.
    cop_entered and capacity_entered were entered by the modeler as the efficiency and capacity and these will be adjusted. This function returns
    a list with the first index being the adjusted COP and the second being the adjusted capacity. This assumes 100% load.
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

    data_entered = {
        'evap_leaving_temp': evap_leaving_temp_entered,
        'condenser_entering_temp': condenser_entering_temp_entered,
    }

    data_rated = {
        'evap_leaving_temp': evap_leaving_temp_rated,
        'condenser_entering_temp': condenser_entering_temp_rated,
    }

    # Calculate and retrieve the results
    all_results = execute_calculations(
        data_entered, data_rated, cap_ft_coeffs, eff_ft_coeffs, cap_ft_min_otpt, cap_ft_max_otpt,
        eff_ft_min_otpt, eff_ft_max_otpt, eff_fplr_curve_type, eff_fplr_coeffs, eff_fplr_min_otpt,
        eff_fplr_max_otpt, curve_function_map, curve_funcs)

    #TODO NEED TO TEST!!! Also, give the functions being called better names.
    #To convert from entered capacity conditions to rated. Rated capacity =  Entered capacity/ (CAPftentered/CAPftrated)
    #MultiplierEntered = (EIRftentered * EIRfPLRentered)/PLRentered and Multiplierrated = (EIRftrated * EIRfPLRrated)/PLRrated. Rated COP =  COPentered * (Multiplierentered/Multiplierrated)

    capacity_adjusted_to_rated = capacity_entered/(all_results["entered_results"]["cap_ft_result"]/all_results["rated_results"]["cap_ft_result"])
    helper_multiplier_entered = (all_results["entered_results"]["eff_ft_result"] * all_results["entered_results"]["eff_fplr_result"])/all_results["entered_results"]["part_load_ratio"]
    helper_multiplier_rated = (all_results["rated_results"]["eff_ft_result"] * all_results["rated_results"]["eff_fplr_result"])/all_results["rated_results"]["part_load_ratio"]
    efficiency_adjusted_to_rated = cop_entered * (helper_multiplier_entered/helper_multiplier_rated)

    return [efficiency_adjusted_to_rated, capacity_adjusted_to_rated]
def calculate_results(evap_leaving_temp, condenser_entering_temp, cap_ft_coeffs, eff_ft_coeffs, cap_ft_min_otpt,
                      cap_ft_max_otpt, eff_ft_min_otpt, eff_ft_max_otpt, eff_fplr_curve_type, eff_fplr_coeffs,
                      eff_fplr_min_otpt, eff_fplr_max_otpt, curve_function_map, curve_funcs):
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
    part_load_ratio = 1 / cap_ft_result

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
        "eff_fplr_result": eff_fplr_result
    }
    return results


def execute_calculations(data_entered, data_rated, cap_ft_coeffs, eff_ft_coeffs, cap_ft_min_otpt, cap_ft_max_otpt,
                         eff_ft_min_otpt, eff_ft_max_otpt, eff_fplr_curve_type, eff_fplr_coeffs, eff_fplr_min_otpt,
                         eff_fplr_max_otpt, curve_function_map, curve_funcs):
    # Calculate with "entered" variables
    entered_results = calculate_results(
        data_entered['evap_leaving_temp'], data_entered['condenser_entering_temp'],
        cap_ft_coeffs, eff_ft_coeffs, cap_ft_min_otpt, cap_ft_max_otpt,
        eff_ft_min_otpt, eff_ft_max_otpt, eff_fplr_curve_type, eff_fplr_coeffs,
        eff_fplr_min_otpt, eff_fplr_max_otpt, curve_function_map, curve_funcs
    )

    # Calculate with "rated" variables
    rated_results = calculate_results(
        data_rated['evap_leaving_temp'], data_rated['condenser_entering_temp'],
        cap_ft_coeffs, eff_ft_coeffs, cap_ft_min_otpt, cap_ft_max_otpt,
        eff_ft_min_otpt, eff_ft_max_otpt, eff_fplr_curve_type, eff_fplr_coeffs,
        eff_fplr_min_otpt, eff_fplr_max_otpt, curve_function_map, curve_funcs
    )

    # Return a dictionary of all results
    return {
        "entered_results": entered_results,
        "rated_results": rated_results
    }






