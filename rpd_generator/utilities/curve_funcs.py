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
