from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_commands.schedule import Schedule
from rpd_generator.utilities import schedule_funcs
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_SiteParameterKeywords = BDLEnums.bdl_enums["SiteParameterKeywords"]
BDL_RunPeriodKeywords = BDLEnums.bdl_enums["RunPeriodKeywords"]
BDL_HolidayKeywords = BDLEnums.bdl_enums["HolidayKeywords"]
BDL_HolidayTypes = BDLEnums.bdl_enums["HolidayTypes"]
BDL_ScheduleTypes = BDLEnums.bdl_enums["ScheduleTypes"]


class SiteParameters(BaseDefinition):
    bdl_command = BDL_Commands.SITE_PARAMETERS

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.site_parameter_name = u_name
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"SitePameters(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate schema structure for site parameters object."""
        self.rmd.calendar.setdefault(
            "has_daylight_saving_time",
            self.boolean_map.get(
                self.get_inp(BDL_SiteParameterKeywords.DAYLIGHT_SAVINGS)
            ),
        )
        monthly_ground_temps = self.get_inp(BDL_SiteParameterKeywords.GROUND_T)
        if monthly_ground_temps:
            self.rmd.weather.setdefault(
                "ground_temperature_schedule", "Ground Temperature Schedule"
            )
            self.create_ground_temp_schedule(monthly_ground_temps)

        self.rmd.weather.setdefault("file_name", self.get_single_string_output(1101006))

    def create_ground_temp_schedule(self, monthly_ground_temps):
        """Create ground temperature schedule."""
        assert (
            len(monthly_ground_temps) == 12
        ), "Ground temperature schedule must have 12 values."
        hours_in_month = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
        hourly_values = []
        for i, temp in enumerate(monthly_ground_temps):
            hourly_values.extend([self.try_float(temp)] * hours_in_month[i])
        ground_t_schedule = Schedule("Ground Temperature Schedule", self.rmd)
        ground_t_schedule.type = BDL_ScheduleTypes.TEMPERATURE
        ground_t_schedule.hourly_values = hourly_values
        self.rmd.bdl_obj_instances["Ground Temperature Schedule"] = ground_t_schedule


class BuildingParameters(BaseDefinition):
    bdl_command = "BUILD-PARAMETERS"

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"BuildingPameters(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate schema structure for building parameters object."""
        self.rmd.building_azimuth = self.try_float(self.get_inp("AZIMUTH"))


class RunPeriod(BaseDefinition):
    bdl_command = BDL_Commands.RUN_PERIOD_PD

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"SitePameters(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate schema structure for site parameters object."""
        year = int(float(self.get_inp(BDL_RunPeriodKeywords.END_YEAR)))
        jan_1_day = schedule_funcs.get_day_of_week_jan_1(year)
        self.rmd.calendar.setdefault(
            "day_of_week_for_january_1",
            jan_1_day,
        )
        Schedule.year = year
        Schedule.day_of_week_for_january_1 = jan_1_day


class FixedShade(BaseDefinition):
    bdl_command = BDL_Commands.FIXED_SHADE

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.has_site_shading = True
        self.rmd.bdl_obj_instances[u_name] = self


class Holidays(BaseDefinition):
    bdl_command = BDL_Commands.HOLIDAYS

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def populate_data_elements(self):
        Schedule.holiday_type = self.get_inp(BDL_HolidayKeywords.TYPE)
        calendar = schedule_funcs.generate_year_calendar(
            Schedule.year, Schedule.day_of_week_for_january_1
        )

        if Schedule.holiday_type == BDL_HolidayTypes.OFFICIAL_US:
            calendar = schedule_funcs.get_official_us_holidays(calendar)
        elif Schedule.holiday_type == BDL_HolidayTypes.ALTERNATE:
            Schedule.holiday_months = self.get_inp(BDL_HolidayKeywords.MONTHS)
            Schedule.holiday_days = self.get_inp(BDL_HolidayKeywords.DAYS)
            calendar = schedule_funcs.get_alternate_holidays(
                calendar, Schedule.holiday_months, Schedule.holiday_days
            )

        Schedule.annual_calendar = calendar


class DesignDay(BaseDefinition):
    """DesignDay class"""

    bdl_command = BDL_Commands.DESIGN_DAY

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

    def __repr__(self):
        return f"DesignDay(u_name='{self.u_name}')"
