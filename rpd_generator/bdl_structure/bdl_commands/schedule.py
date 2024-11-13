from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_ScheduleTypes = BDLEnums.bdl_enums["ScheduleTypes"]
BDL_DayScheduleKeywords = BDLEnums.bdl_enums["DayScheduleKeywords"]
BDL_WeekScheduleKeywords = BDLEnums.bdl_enums["WeekScheduleKeywords"]
BDL_ScheduleKeywords = BDLEnums.bdl_enums["ScheduleKeywords"]
LAST_DAY = 364


class DaySchedulePD(BaseDefinition):
    """DaySchedulePD object in the tree."""

    bdl_command = BDL_Commands.DAY_SCHEDULE_PD

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.hourly_values = []
        self.outdoor_high_for_loop_supply_reset_temperature = None
        self.outdoor_low_for_loop_supply_reset_temperature = None
        self.loop_supply_temperature_at_outdoor_high = None
        self.loop_supply_temperature_at_outdoor_low = None

    def __repr__(self):
        return f"DaySchedulePD(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements that originate from eQUEST's DAY-SCHEDULE-PD command"""
        day_sch_type = self.get_inp(BDL_DayScheduleKeywords.TYPE)
        if day_sch_type in Schedule.supported_hourly_schedules:
            day_sch_values_list = self.get_inp(BDL_DayScheduleKeywords.VALUES)
            day_sch_values_list = [self.try_float(val) for val in day_sch_values_list]
            self.hourly_values = day_sch_values_list

        elif day_sch_type == BDL_ScheduleTypes.RESET_TEMP:
            self.outdoor_high_for_loop_supply_reset_temperature = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.OUTSIDE_HI)
            )
            self.outdoor_low_for_loop_supply_reset_temperature = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.OUTSIDE_LO)
            )
            self.loop_supply_temperature_at_outdoor_high = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.SUPPLY_HI)
            )
            self.loop_supply_temperature_at_outdoor_low = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.SUPPLY_LO)
            )


class WeekSchedulePD(BaseDefinition):
    """WeekSchedulePD object in the tree."""

    bdl_command = BDL_Commands.WEEK_SCHEDULE_PD

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        # All lists will store 12 values, Mon-Sun, Holidays and then 4 design day schedules
        self.day_type_hourly_values = []  # 12 lists of 24 hourly values
        self.day_type_outside_highs = []
        self.day_type_outside_lows = []
        self.day_type_supply_highs = []
        self.day_type_supply_lows = []

    def __repr__(self):
        return f"WeekSchedulePD(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Create lists of length 12, including Mon-Sun, Holidays and then 4 design day schedules"""
        wk_sch_type = self.get_inp(BDL_WeekScheduleKeywords.TYPE)
        if wk_sch_type in Schedule.supported_hourly_schedules:
            day_schedule_names = self.get_inp(BDL_WeekScheduleKeywords.DAY_SCHEDULES)
            self.day_type_hourly_values = [
                self.get_obj(day_sch_name).hourly_values
                for day_sch_name in day_schedule_names
            ]

        elif wk_sch_type == BDL_ScheduleTypes.RESET_TEMP:
            attributes = {
                "day_type_outside_highs": "outdoor_high_for_loop_supply_reset_temperature",
                "day_type_outside_lows": "outdoor_low_for_loop_supply_reset_temperature",
                "day_type_supply_highs": "loop_supply_temperature_at_outdoor_high",
                "day_type_supply_lows": "loop_supply_temperature_at_outdoor_low",
            }
            day_schedule_names = self.get_inp(BDL_WeekScheduleKeywords.DAY_SCHEDULES)

            for attr_name, field_name in attributes.items():
                setattr(
                    self,
                    attr_name,
                    [
                        getattr(self.get_obj(day_sch_name), field_name)
                        for day_sch_name in day_schedule_names
                    ],
                )


class Schedule(BaseNode):
    """Schedule object in the tree."""

    bdl_command = BDL_Commands.SCHEDULE_PD

    year = None
    day_of_week_for_january_1 = None
    holiday_type = None
    holiday_months = None
    holiday_days = None
    annual_calendar = {}
    supported_hourly_schedules = [
        BDL_ScheduleTypes.ON_OFF,
        BDL_ScheduleTypes.ON_OFF_FLAG,
        BDL_ScheduleTypes.FRACTION,
        BDL_ScheduleTypes.MULTIPLIER,
        BDL_ScheduleTypes.TEMPERATURE,
        # BDL_ScheduleTypes.FRAC_DESIGN,
    ]

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.schedule_data_structure = {}
        self.outdoor_high_for_loop_supply_reset_temperature = None
        self.outdoor_low_for_loop_supply_reset_temperature = None
        self.loop_supply_temperature_at_outdoor_high = None
        self.loop_supply_temperature_at_outdoor_low = None

        # data elements with no children
        self.purpose = None
        self.sequence_type = None
        self.hourly_values = None
        self.hourly_heating_design_day = None
        self.hourly_cooling_design_day = None
        self.event_times = None
        self.event_values = None
        self.event_times_heating_design_day = None
        self.event_values_heating_design_day = None
        self.event_times_cooling_design_day = None
        self.event_values_cooling_design_day = None
        self.type = None
        self.prescribed_type = None
        self.is_modified_for_workaround = None

    def __repr__(self):
        return f"Schedule(u_name='{self.u_name}')"

    def populate_data_elements(self):

        # Get the type of schedule
        ann_sch_type = self.get_inp(BDL_ScheduleKeywords.TYPE)

        # There are no hourly values for temperature and ratio reset schedules so ignore those types
        if ann_sch_type in [
            *self.supported_hourly_schedules,
            BDL_ScheduleTypes.RESET_TEMP,
        ]:
            proj_calendar = self.annual_calendar

            # Get the month value where a new week-schedule begins
            ann_months = (
                self.get_inp(BDL_ScheduleKeywords.MONTH)
                if isinstance(self.get_inp(BDL_ScheduleKeywords.MONTH), list)
                else [self.get_inp(BDL_ScheduleKeywords.MONTH)]
            )
            ann_months = [int(float(val)) for val in ann_months]

            # Get the day value where a new week-schedule begins
            ann_days = (
                self.get_inp(BDL_ScheduleKeywords.DAY)
                if isinstance(self.get_inp(BDL_ScheduleKeywords.DAY), list)
                else [self.get_inp(BDL_ScheduleKeywords.DAY)]
            )
            ann_days = [int(float(val)) for val in ann_days]

            week_schedules = [self.get_inp(BDL_ScheduleKeywords.WEEK_SCHEDULES)]

            # Create a list to hold the index where there is a change in week schedule based on mo/day in ann sch
            schedule_change_indices = [
                list(proj_calendar.keys()).index(f"{ann_months[i]}/{ann_days[i]}") + 1
                for i in range(len(ann_months))
            ]

            # Loop through each day of the year in the calendar. Extend the hourly schedule values based on the day type
            # result is an 8760 list with the hourly schedule value for the whole year.
            wk_sch_index = 0

            if ann_sch_type in self.supported_hourly_schedules:
                hourly_values = []
                for day_index, day_type in enumerate(proj_calendar.values()):
                    # Check if the index is a change point. If so, continue to the next weekly schedule index
                    if day_index in schedule_change_indices and day_index != LAST_DAY:
                        wk_sch_index += 1

                    wk_schedule_pd = self.get_obj(week_schedules[wk_sch_index])
                    hourly_values.extend(
                        wk_schedule_pd.day_type_hourly_values[day_type - 1]
                    )
                self.hourly_values = hourly_values

            elif ann_sch_type == BDL_ScheduleTypes.RESET_TEMP:
                outdoor_high_for_loop_supply_reset_temperature = set()
                outdoor_low_for_loop_supply_reset_temperature = set()
                loop_supply_temperature_at_outdoor_high = set()
                loop_supply_temperature_at_outdoor_low = set()
                for day_index, day_type in enumerate(proj_calendar.values()):
                    # Check if the index is a change point. If so, continue to the next weekly schedule index
                    if day_index in schedule_change_indices and day_index != LAST_DAY:
                        wk_sch_index += 1

                    wk_schedule_pd = self.get_obj(week_schedules[wk_sch_index])
                    outdoor_high_for_loop_supply_reset_temperature.add(
                        wk_schedule_pd.day_type_outside_highs[day_type - 1]
                    )
                    outdoor_low_for_loop_supply_reset_temperature.add(
                        wk_schedule_pd.day_type_outside_lows[day_type - 1]
                    )
                    loop_supply_temperature_at_outdoor_high.add(
                        wk_schedule_pd.day_type_supply_highs[day_type - 1]
                    )
                    loop_supply_temperature_at_outdoor_low.add(
                        wk_schedule_pd.day_type_supply_lows[day_type - 1]
                    )
                if len(outdoor_high_for_loop_supply_reset_temperature) == 1:
                    self.outdoor_high_for_loop_supply_reset_temperature = (
                        outdoor_high_for_loop_supply_reset_temperature.pop()
                    )
                if len(outdoor_low_for_loop_supply_reset_temperature) == 1:
                    self.outdoor_low_for_loop_supply_reset_temperature = (
                        outdoor_low_for_loop_supply_reset_temperature.pop()
                    )
                if len(loop_supply_temperature_at_outdoor_high) == 1:
                    self.loop_supply_temperature_at_outdoor_high = (
                        loop_supply_temperature_at_outdoor_high.pop()
                    )
                if len(loop_supply_temperature_at_outdoor_low) == 1:
                    self.loop_supply_temperature_at_outdoor_low = (
                        loop_supply_temperature_at_outdoor_low.pop()
                    )

    def populate_data_group(self):
        """Populate schema structure for schedule object."""
        self.schedule_data_structure = {
            "id": self.u_name,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "purpose",
            "sequence_type",
            "hourly_values",
            "hourly_heating_design_day",
            "hourly_cooling_design_day",
            "event_times",
            "event_values",
            "event_times_heating_design_day",
            "event_values_heating_design_day",
            "event_times_cooling_design_day",
            "event_values_cooling_design_day",
            "type",
            "prescribed_type",
            "is_modified_for_workaround",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.schedule_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert window object into the rpd data structure."""
        rmd.schedules.append(self.schedule_data_structure)
