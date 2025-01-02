

def calculate_bi_quadratic_in_t(curve_coeffs: list, x: float, y: float) -> float:
    """Function takes a list of curve coefficients with a = 0 index and f = 5th index and two independent variables x and y.
    Function then computes and returns Z = a + b * x + c * x^2 + d * y + e * y^2 + f * x * y
    """
    z = curve_coeffs[0] + curve_coeffs[1] * x + curve_coeffs[2] * x**2 + curve_coeffs[3] * y + curve_coeffs[4] * y**2 + curve_coeffs[5] * x * y
    return z


def calculate_cubic(curve_coeffs: list, x: float)  -> float:
    """Function takes a list of curve coefficients with a = 0 index and d = 3rd index and an independent variable X.
    Function then computes and returns Z = a + b * X + c * X^2 + d * X^3
    """
    z = curve_coeffs[0] + curve_coeffs[1] * x + curve_coeffs[2] * x**2 + curve_coeffs[3] * x**3
    return z


def calculate_quadratic(curve_coeffs: list, x: float)  -> float:
    """Function takes a list of curve coefficients with a = 0 index and c = 2nd index and an independent variable X.
    Function then computes and returns Z = a + b * X + c * X^2
    """
    z = curve_coeffs[0] + curve_coeffs[1] * x + curve_coeffs[2] * x**2
    return z
