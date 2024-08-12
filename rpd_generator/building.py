from rpd_generator.bdl_structure.base_definition import BaseDefinition
from rpd_generator.bdl_structure.bdl_commands.project import FixedShade


class Building(BaseDefinition):
    """
    This class is used to describe a building. The building objectis created once per project by default , but more
    can be created through the user interface.
    """

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)

        self.building_data_structure = {}

        # data elements with children
        self.building_segments = []
        self.elevators = []
        self.exterior_lighting = []
        self.refrigerated_cases = []

        # data elements with no children
        self.reporting_name = None
        self.notes = None
        self.building_open_schedule = None
        self.has_site_shading = None
        self.number_of_floors_above_grade = None
        self.number_of_floors_below_grade = None

    def populate_data_elements(self):
        """Populate data elements for building object."""
        self.has_site_shading = any(
            isinstance(value, FixedShade)
            for value in self.rmd.bdl_obj_instances.values()
        )

    def populate_data_group(self):
        """Populate the building data structure."""
        self.building_data_structure = {
            "id": self.u_name,
            "building_segments": self.building_segments,
            "elevators": self.elevators,
            "exterior_lighting": self.exterior_lighting,
            "refrigerated_cases": self.refrigerated_cases,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "building_open_schedule",
            "has_site_shading",
            "number_of_floors_above_grade",
            "number_of_floors_below_grade",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.building_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert building object into the rpd data structure."""
        rmd.buildings.append(self.building_data_structure)
