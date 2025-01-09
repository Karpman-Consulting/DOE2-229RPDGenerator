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

def convert_to_ahri_conditions(curves: dict, x: float, y: float) -> list:
    """The curves dictionary should contain the following keys eff_ft, cap_ft, eff_fplr which are the curve objects.
     x is likely equal to the evaporator leaving temp and y is likely equal to condenser entering temp. These
     temperatures were entered in eQuest for the rated temperatures for the capacity and efficiency."""

    coeffs = {}
    min_outputs = {}
    max_outputs = {}

    for key, obj in curves.items():
        input_type = obj.get_inp(BDL_CurveFitKeywords.INPUT_TYPE)
        if input_type == BDL_CurveFitInputTypes.DATA:
            return "Keyword DATA was used for coefficient determination"
        coeffs[f"{key}_coeffs"] = list(map(float, obj.get_inp(BDL_CurveFitKeywords.COEF)))
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

    eff_fplr_curve_type = cap_ft.get_inp(BDL_CurveFitKeywords.TYPE)

    curve_function_map = {
        BDL_CurveFitTypes.QUADRATIC: curve_funcs.calculate_quadratic,
        BDL_CurveFitTypes.CUBIC: curve_funcs.calculate_cubic,
    }