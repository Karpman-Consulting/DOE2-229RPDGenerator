import os
import json
import pint
from jsonpath_ng.ext import parse


path_to_ureg = os.path.join(os.path.dirname(__file__), "resources", "unit_registry.txt")
ureg = pint.UnitRegistry(path_to_ureg, autoconvert_offset_to_baseunit=True)

path_to_schema_units = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "schema",
    "resources",
    "schema_units.json",
)
path_to_equest_units = os.path.join(
    os.path.dirname(__file__), "resources", "equest_units.json"
)
path_to_json_paths = os.path.join(
    os.path.dirname(__file__), "resources", "manual_item_json_paths.json"
)


def convert_to_schema_units(rpd_json):
    """Converts the units of the json data to the standard units defined in the schema"""
    with open(path_to_equest_units) as f:
        equest_units = json.load(f)

    with open(path_to_schema_units) as f:
        schema_units = json.load(f)

    with open(path_to_json_paths) as f:
        item_paths = json.load(f)

    processed_ids = set()

    def convert_units(dg, json_data, unit_dict):
        for element in json_data:
            if id(element) in processed_ids:
                continue  # Prevent processing the same object multiple times

            processed_ids.add(id(element))  # Mark this object as processed

            if isinstance(element, list):
                convert_units(dg, element, unit_dict)  # Recurse into lists
            elif isinstance(element, dict):
                for key, value in element.items():
                    if key in unit_dict and isinstance(value, (int, float)):
                        element[key] = value * ureg(unit_dict[key])
                        schema_unit = schema_units.get(dg).get(key)
                        element[key] = element[key].to(schema_unit)
                        element[key] = element[key].magnitude

    for data_group in equest_units:
        elements_w_units = equest_units[data_group]
        json_paths = item_paths.get(data_group)

        for json_path in json_paths:
            jsonpath_expr = parse(json_path)
            matches = [m.value for m in jsonpath_expr.find(rpd_json)]
            unique_matches = [obj for obj in matches if id(obj) not in processed_ids]
            convert_units(data_group, unique_matches, elements_w_units)
