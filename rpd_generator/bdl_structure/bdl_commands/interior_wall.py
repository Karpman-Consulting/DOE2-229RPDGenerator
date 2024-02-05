from rpd_generator.bdl_structure.parent_node import ParentNode
from rpd_generator.bdl_structure.child_node import ChildNode


class InteriorWall(
    ChildNode, ParentNode
):  # Inherit ChildNode first so that the MRO does not try to call ParentNode.__init__ twice
    """InteriorWall object in the tree."""

    bdl_command = "INTERIOR-WALL"
    used_constructions = []

    def __init__(self, u_name, parent):
        super().__init__(u_name, parent)

        self.interior_wall_data_structure = {}

        # data elements with children
        self.subsurfaces = []
        self.construction = {}
        self.surface_optical_properties = {}

        # data elements with no children
        self.classification = None
        self.area = None
        self.tilt = None
        self.azimuth = None
        self.adjacent_to = None
        self.adjacent_zone = None
        self.does_cast_shade = None
        self.status_type = None

    def __repr__(self):
        return f"InteriorWall(u_name='{self.u_name}', parent={self.parent.__class__.__name__}('{self.parent.u_name}')"

    def populate_data_group(self):
        """Populate schema structure for interior wall object."""
        self.interior_wall_data_structure[self.u_name] = {
            "subsurfaces": self.subsurfaces,
            "construction": self.construction,
            "surface_optical_properties": self.surface_optical_properties,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "classification",
            "area",
            "tilt",
            "azimuth",
            "adjacent_to",
            "adjacent_zone",
            "does_cast_shade",
            "status_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.interior_wall_data_structure[self.u_name][attr] = value

    def insert_to_rpd(self, zone):
        """Insert exterior wall object into the rpd data structure."""
        zone.surfaces.append(self.interior_wall_data_structure)
