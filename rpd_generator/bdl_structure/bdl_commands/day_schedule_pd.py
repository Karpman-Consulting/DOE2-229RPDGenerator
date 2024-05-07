from rpd_generator.bdl_structure.base_definition import BaseDefinition


class DaySchedulePD(BaseDefinition):
    """DaySchedulePD object in the tree."""

    bdl_command = "DAY-SCHEDULE-PD"

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        # data elements with no children
        self.hourly_values = []


    def __repr__(self):
        return f"DaySchedulePD(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements that originate from eQUEST's DAY-SCHEDULE-PD command"""
        """Does not appear the type is needed, REMOVE after confirming, may need to add something for reset schedules"""
        day_sch_type = self.keyword_value_pairs.get("TYPE")
        day_sch_values_list = self.keyword_value_pairs.get("VALUES")
        day_sch_values_list = [self.try_float(val) for val in day_sch_values_list]
        self.hourly_values = day_sch_values_list

