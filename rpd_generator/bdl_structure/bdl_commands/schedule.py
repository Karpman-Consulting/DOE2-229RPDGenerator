from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

ScheduleOptions = SchemaEnums.schema_enums["ScheduleOptions"]
ScheduleSequenceOptions = SchemaEnums.schema_enums["ScheduleSequenceOptions"]
PrescribedScheduleOptions = SchemaEnums.schema_enums[
    "PrescribedScheduleOptions2019ASHRAE901"
]
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
        self.rmd.bdl_obj_instances[u_name] = self

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
        if day_sch_type in Schedule.schedule_type_map:
            self.hourly_values = [
                self.try_float(val)
                for val in self.get_inp(BDL_DayScheduleKeywords.VALUES)
            ]

        elif day_sch_type == BDL_ScheduleTypes.RESET_TEMP:
            self.outdoor_high_for_loop_supply_reset_temperature = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.OUTSIDE_HI)
            )
            self.outdoor_low_for_loop_supply_reset_temperature = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.OUTSIDE_LO)
            )
            self.loop_supply_temperature_at_outdoor_high = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.SUPPLY_LO)
            )
            self.loop_supply_temperature_at_outdoor_low = self.try_float(
                self.get_inp(BDL_DayScheduleKeywords.SUPPLY_HI)
            )


class WeekSchedulePD(BaseDefinition):
    """WeekSchedulePD object in the tree."""

    bdl_command = BDL_Commands.WEEK_SCHEDULE_PD

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

        # All lists will store 12 values, Mon-Sun, Holidays and then 4 design day schedules
        self.outdoor_high_for_loop_supply_reset_temperature = []
        self.outdoor_low_for_loop_supply_reset_temperature = []
        self.loop_supply_temperature_at_outdoor_high = []
        self.loop_supply_temperature_at_outdoor_low = []
        self.day_type_hourly_values = []  # 12 lists of 24 hourly values

    def __repr__(self):
        return f"WeekSchedulePD(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Create lists of length 12, including Mon-Sun, Holidays and then 4 design day schedules"""
        wk_sch_type = self.get_inp(BDL_WeekScheduleKeywords.TYPE)
        if wk_sch_type in Schedule.schedule_type_map:
            day_schedule_names = self.get_inp(BDL_WeekScheduleKeywords.DAY_SCHEDULES)
            # for day_name in day_schedule_names:
            #     d = self.get_obj(day_name)
            #     hv = d.hourly_values
            #     self.day_type_hourly_values.append(hv)
            self.day_type_hourly_values = [
                self.get_obj(day_sch_name).hourly_values
                for day_sch_name in day_schedule_names
            ]

        elif wk_sch_type == BDL_ScheduleTypes.RESET_TEMP:
            for day_schedule_name in self.get_inp(
                BDL_WeekScheduleKeywords.DAY_SCHEDULES
            ):
                day_schedule = self.get_obj(day_schedule_name)
                self.outdoor_high_for_loop_supply_reset_temperature.append(
                    day_schedule.outdoor_high_for_loop_supply_reset_temperature
                )
                self.outdoor_low_for_loop_supply_reset_temperature.append(
                    day_schedule.outdoor_low_for_loop_supply_reset_temperature
                )
                self.loop_supply_temperature_at_outdoor_high.append(
                    day_schedule.loop_supply_temperature_at_outdoor_high
                )
                self.loop_supply_temperature_at_outdoor_low.append(
                    day_schedule.loop_supply_temperature_at_outdoor_low
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
    schedule_type_map = {
        BDL_ScheduleTypes.ON_OFF: ScheduleOptions.MULTIPLIER_DIMENSIONLESS,
        BDL_ScheduleTypes.ON_OFF_FLAG: ScheduleOptions.MULTIPLIER_DIMENSIONLESS,
        BDL_ScheduleTypes.FRACTION: ScheduleOptions.MULTIPLIER_DIMENSIONLESS,
        BDL_ScheduleTypes.MULTIPLIER: ScheduleOptions.MULTIPLIER_DIMENSIONLESS,
        BDL_ScheduleTypes.TEMPERATURE: ScheduleOptions.TEMPERATURE,
        BDL_ScheduleTypes.FRAC_DESIGN: ScheduleOptions.MULTIPLIER_DIMENSIONLESS,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

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
        self.prescribed_type = PrescribedScheduleOptions.NOT_APPLICABLE
        self.is_modified_for_workaround = None

    def __repr__(self):
        return f"Schedule(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for schedule object."""
        # Get the type of schedule
        ann_sch_type = self.get_inp(BDL_ScheduleKeywords.TYPE)

        self.type = self.schedule_type_map.get(ann_sch_type)
        self.sequence_type = ScheduleSequenceOptions.HOURLY

        # There are no hourly values for temperature and ratio reset schedules so ignore those types
        if ann_sch_type in [
            *self.schedule_type_map.keys(),
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

            if ann_sch_type in self.schedule_type_map:
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
                        wk_schedule_pd.outdoor_high_for_loop_supply_reset_temperature[
                            day_type - 1
                        ]
                    )
                    outdoor_low_for_loop_supply_reset_temperature.add(
                        wk_schedule_pd.outdoor_low_for_loop_supply_reset_temperature[
                            day_type - 1
                        ]
                    )
                    loop_supply_temperature_at_outdoor_high.add(
                        wk_schedule_pd.loop_supply_temperature_at_outdoor_high[
                            day_type - 1
                        ]
                    )
                    loop_supply_temperature_at_outdoor_low.add(
                        wk_schedule_pd.loop_supply_temperature_at_outdoor_low[
                            day_type - 1
                        ]
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
