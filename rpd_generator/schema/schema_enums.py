import json
from pathlib import Path
from collections import defaultdict
from rpd_generator.schema.ruleset import Ruleset
from rpd_generator.utilities.jsonpath_utils import create_enum_dict

"""This module exports the dictionary schema_enums that provides access to the
enumerations in the schema files.

The keys of schema_enums are the names of the enumeration objects; each value
is a class with an attribute for each item in the enumeration. The value
of the attribute is the same as the attribute name.
"""


class _ListEnum:
    """A utility class used to convert a list into a class

    Each item in the list becomes a class attribute whose value is the attribute
    name as a string. This is intended as a more convenient version of Enum.
    """

    def __init__(self, _dict):
        for key in _dict:
            setattr(self, key, key)

    def get_list(self):
        return list(self.__dict__)


class SchemaEnums:
    schema_enums = {}
    schema_descriptions = {}

    @staticmethod
    def update_schema_enum(ruleset: Ruleset):
        # Load the output schema file
        _output_schema_path = Path(__file__).parent / ruleset.output_schema_filename
        with open(_output_schema_path) as json_file:
            _output_schema_obj = json.load(json_file)

        # Load the enumeration schema file
        _enum_schema_path = Path(__file__).parent / ruleset.enum_schema_filename
        with open(_enum_schema_path) as json_file:
            _enum_schema_obj = json.load(json_file)

        # Load the schema file
        _schema_path = Path(__file__).parent / "ASHRAE229.schema.json"
        with open(_schema_path) as json_file:
            _schema_obj = json.load(json_file)

        # Query for all objects having an enum field
        _output_schema_enum_jsonpath_value_dict = create_enum_dict(_output_schema_obj)
        _enum_schema_enum_jsonpath_value_dict = create_enum_dict(_enum_schema_obj)
        _schema_enum_jsonpath_value_dict = create_enum_dict(_schema_obj)

        combined_enum_jsonpath_value_dict = defaultdict(list)
        combined_desription_jsonpath_value_dict = defaultdict(list)

        # Merge dictionaries while combining values
        for d in (
            _schema_enum_jsonpath_value_dict,
            _enum_schema_enum_jsonpath_value_dict,
            _output_schema_enum_jsonpath_value_dict,
        ):
            for key, value in d.items():
                # Extend the list for the key with new values
                if "enum" in value:
                    combined_enum_jsonpath_value_dict[key].extend(value["enum"])
                if "descriptions" in value:
                    combined_desription_jsonpath_value_dict[key].extend(
                        value["descriptions"]
                    )

        # Create a dictionary of all the enumerations as dictionaries
        combined_enum_dict = {
            enum_name: enum_list
            for enum_name, enum_list in combined_enum_jsonpath_value_dict.items()
        }

        # Assign to SchemaEnums with the combined lists
        SchemaEnums.schema_enums = {
            key: _ListEnum(enum_list) for key, enum_list in combined_enum_dict.items()
        }

        # Create a dictionary of all the descriptions as dictionaries
        combined_description_dict = {
            description_name: description_list
            for description_name, description_list in combined_desription_jsonpath_value_dict.items()
        }

        # Assign to SchemaEnums with the combined lists
        SchemaEnums.schema_descriptions = {
            key: _ListEnum(description_list)
            for key, description_list in combined_description_dict.items()
        }


def print_schema_enums():
    """Print all the schema enumerations with their names and values

    This is primarily useful for debugging purposes
    """
    SchemaEnums.update_schema_enum(
        Ruleset(
            "ASHRAE 90.1-2019",
            "Enumerations2019ASHRAE901.schema.json",
            "Output2019ASHRAE901.schema.json",
        )
    )
    for key in SchemaEnums.schema_enums:
        print(f"{key}:")
        for e in SchemaEnums.schema_enums[key].get_list():
            print(f"    {e}")
        print()


if __name__ == "__main__":
    print_schema_enums()
