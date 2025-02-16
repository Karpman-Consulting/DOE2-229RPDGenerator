from time import strftime, gmtime

OUTPUT_SCHEMA_ASHRAE901_2019 = "OUTPUT_SCHEMA_ASHRAE901_2019"


class RulesetProjectDescription:
    """
    This class is used to represent the RulesetProjectDescription object in the 229 schema. It also stores additional project-level data.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.rpd_data_structure = {}

        # data elements with children
        self.ruleset_model_descriptions = []
        self.ground_temperature_schedule = None
        self.file_name = None
        self.data_source_type = None
        self.climate_zone = None
        self.cooling_design_day_type = None
        self.heating_design_day_type = None

        # data elements with no children
        self.reporting_name = None
        self.notes = None
        self.data_timestamp = strftime("%Y-%m-%dT%H:%MZ", gmtime())
        self.data_version = "0.1.0"
        self.compliance_path = None
        self.output_format_type = OUTPUT_SCHEMA_ASHRAE901_2019

    def populate_data_group(self):
        """
        Populate the RPD data group (only data elements directly under the RPD Data Group)
        """
        self.rpd_data_structure = {
            "id": f"{self.project_name}",
            "ruleset_model_descriptions": self.ruleset_model_descriptions,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "data_timestamp",
            "data_version",
            "compliance_path",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.rpd_data_structure[attr] = value
