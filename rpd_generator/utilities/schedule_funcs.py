MONDAY = 1
THURSDAY = 4
FRIDAY = 5
WEEKEND = {6, 7}
HOLIDAY = 8


def get_day_of_week_jan_1(year: int) -> str:
    """
    Get the day of the week for January 1st of a given year using Zeller's Congruence method.
    :param year: (int) The year to get the day of the week for
    :return: day_of_week (str): "MONDAY", "TUESDAY", etc.
    """
    # Adjustments for January
    q = 1  # Day of the month
    m = 13  # Month (January is treated as the 13th month of the previous year)
    year -= 1  # Adjust year since January is treated as part of the previous year

    # Zeller's Congruence components
    k = year % 100  # Year of the century
    j = year // 100  # Zero-based century
    # Zeller's Congruence for Gregorian calendar
    h = (q + ((13 * (m + 1)) // 5) + k + (k // 4) + (j // 4) - (2 * j)) % 7

    # Convert Zeller's result to weekday with 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    day_of_week = (h + 5) % 7

    days = [
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY",
    ]

    return days[day_of_week]


def is_leap_year(year: int) -> bool:
    """
    Determine if a year is a leap year.
    :param year:
    :return: True/False boolean
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def generate_year_calendar(year: int, first_day: str) -> dict:
    """
    Generate a dictionary of days in a year with day types.
    :param year:
    :param first_day:
    :return: dictionary of days in a year with day types
    """
    first_day = [
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY",
    ].index(first_day) + 1
    day_types_365 = {}
    day_types = [7, 1, 2, 3, 4, 5, 6]
    day_type = None

    month_days = [
        31,
        28 if not is_leap_year(year) else 29,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    m = 0
    d = 1

    days_left_in_month = month_days[m]

    for i in range(366 if is_leap_year(year) else 365):
        days_left_in_month -= 1

        day_type = day_types[(i + first_day) % 7]

        day_types_365[f"{m+1}/{d}"] = day_type

        if days_left_in_month > 0:
            d += 1
        else:
            m += 1
            d = 1
            if m < 12:
                days_left_in_month = month_days[m]

    return day_types_365


def set_holiday_if_workday(day_types_365: dict, date: str):
    """Helper function to set the date as a holiday if it's a workday."""
    if day_types_365[date] == MONDAY:
        day_types_365[date] = HOLIDAY


def find_nth_weekday_in_range(
    day_types_365: dict, month: int, start: int, end: int, weekday_type: int
) -> str | None:
    """Find the nth weekday of a specific type within a range."""
    for day in range(start, end + 1):
        date = f"{month}/{day}"
        if day_types_365.get(date) == weekday_type:
            return date
    return None


def get_official_us_holidays(day_types_365: dict) -> dict:
    """
    Set official US holidays to type 8 in the calendar dictionary returned by `generate_year_calendar()`.
    :param day_types_365: Dictionary mapping "month/day" to a day type.
    :return: Updated calendar with official US holidays set to type 8.
    """

    # New Year's Day
    if day_types_365["12/31"] == FRIDAY:
        day_types_365["12/31"] = HOLIDAY
    elif day_types_365["1/1"] not in WEEKEND:
        day_types_365["1/1"] = HOLIDAY
    elif day_types_365["1/2"] == MONDAY:
        day_types_365["1/2"] = HOLIDAY

    # Martin Luther King Jr. Day (Third Monday in January)
    mlk_day = find_nth_weekday_in_range(day_types_365, 1, 15, 21, MONDAY)
    if mlk_day:
        day_types_365[mlk_day] = HOLIDAY

    # Washington's Birthday (Third Monday in February)
    presidents_day = find_nth_weekday_in_range(day_types_365, 2, 15, 21, MONDAY)
    if presidents_day:
        day_types_365[presidents_day] = HOLIDAY

    # Memorial Day (Last Monday in May)
    memorial_day = find_nth_weekday_in_range(day_types_365, 5, 25, 31, MONDAY)
    if memorial_day:
        day_types_365[memorial_day] = HOLIDAY

    # Independence Day
    if day_types_365["7/3"] == FRIDAY:
        day_types_365["7/3"] = HOLIDAY
    elif day_types_365["7/4"] not in WEEKEND:
        day_types_365["7/4"] = HOLIDAY
    elif day_types_365["7/5"] == MONDAY:
        day_types_365["7/5"] = HOLIDAY

    # Labor Day (First Monday in September)
    labor_day = find_nth_weekday_in_range(day_types_365, 9, 1, 7, MONDAY)
    if labor_day:
        day_types_365[labor_day] = HOLIDAY

    # Columbus Day (Second Monday in October)
    columbus_day = find_nth_weekday_in_range(day_types_365, 10, 8, 14, MONDAY)
    if columbus_day:
        day_types_365[columbus_day] = HOLIDAY

    # Veterans Day
    if day_types_365["11/10"] == FRIDAY:
        day_types_365["11/10"] = HOLIDAY
    elif day_types_365["11/11"] not in WEEKEND:
        day_types_365["11/11"] = HOLIDAY
    elif day_types_365["11/12"] == MONDAY:
        day_types_365["11/12"] = HOLIDAY

    # Thanksgiving (Fourth Thursday in November)
    thanksgiving = find_nth_weekday_in_range(day_types_365, 11, 22, 28, 4)
    if thanksgiving:
        day_types_365[thanksgiving] = HOLIDAY

    # Christmas
    if day_types_365["12/24"] == FRIDAY:
        day_types_365["12/24"] = HOLIDAY
    elif day_types_365["12/25"] not in WEEKEND:
        day_types_365["12/25"] = HOLIDAY
    elif day_types_365["12/26"] == MONDAY:
        day_types_365["12/26"] = HOLIDAY

    return day_types_365


def get_alternate_holidays(
    calendar: dict, holiday_months: list, holiday_days: list
) -> dict:
    """
    Set custom to type 8 in the calendar dictionary returned by `generate_year_calendar()`.
    :param calendar:
    :return: calendar with custom holidays set to type 8
    :param holiday_months: list of months
    :param holiday_days: list of days
    """
    for i in range(len(holiday_months)):
        calendar[f"{int(float(holiday_months[i]))}/{int(float(holiday_days[i]))}"] = 8

    return calendar
