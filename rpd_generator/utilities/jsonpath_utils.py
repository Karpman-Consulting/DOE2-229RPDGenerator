import re
from itertools import chain
from jsonpath_ng.ext import parse
from typing import TypedDict


class ZonesTerminalsServedByHVACSys(TypedDict):
    terminal_list: list[str]
    zone_list: list[str]


def create_enum_dict(obj):
    enum_dict = {}
    if "definitions" in obj:
        for key, value in obj["definitions"].items():
            if "enum" in value:
                enum_dict[key] = value["enum"]
    return enum_dict


def ensure_root(jpath):
    return jpath if jpath.startswith("$") else "$." + jpath


def find_all(jpath, obj):
    def recursive_find(keys, current_obj):
        if not keys:
            return [current_obj]  # Base case: no more keys to process

        key = keys[0]

        if key == "*":  # Match all keys or array elements
            if isinstance(current_obj, dict):
                return [
                    value
                    for sub_key, value in current_obj.items()
                    for value in recursive_find(keys[1:], value)
                ]
            elif isinstance(current_obj, list):
                return [
                    value
                    for item in current_obj
                    for value in recursive_find(keys[1:], item)
                ]
            else:
                return []  # No match for non-dict/non-list objects

        elif "[" in key and "]" in key:  # Handle array indexing
            try:
                k, idx = key.split("[")
                idx = idx.strip("]")
                if idx == "*":  # Handle wildcard in array indexing
                    if k in current_obj and isinstance(current_obj[k], list):
                        return [
                            value
                            for item in current_obj[k]
                            for value in recursive_find(keys[1:], item)
                        ]
                    return []
                else:  # Regular array indexing
                    idx = int(idx)
                    if k in current_obj and isinstance(current_obj[k], list):
                        return recursive_find(keys[1:], current_obj[k][idx])
                    return []
            except (ValueError, IndexError, KeyError):
                return []  # Handle invalid array indexing gracefully

        else:  # Handle normal key lookup
            if isinstance(current_obj, dict) and key in current_obj:
                return recursive_find(keys[1:], current_obj[key])
            return []

    # Remove leading "$." and split the path into keys
    keys = jpath.strip("$.").split(".")
    return recursive_find(keys, obj)


def find_all_by_jsonpaths(jpaths: list, obj: dict) -> list:
    return list(chain.from_iterable([find_all(jpath, obj) for jpath in jpaths]))


def find_all_with_field_value(jpath, field, value, obj):
    def recursive_find(keys, current_obj):
        if not keys:
            return [current_obj]  # Base case: no more keys to process

        if current_obj is None:  # Safeguard against None
            return []

        key = keys[0]

        if key == "*":  # Match all keys or array elements
            if isinstance(current_obj, dict):
                return [
                    result
                    for sub_key, sub_value in current_obj.items()
                    for result in recursive_find(keys[1:], sub_value)
                ]
            elif isinstance(current_obj, list):
                return [
                    result
                    for item in current_obj
                    for result in recursive_find(keys[1:], item)
                ]
            else:
                return []  # No match for non-dict/non-list objects

        elif "[" in key and "]" in key:  # Handle filters and indexing
            try:
                base_key, condition = key.split("[", 1)
                condition = condition.strip("]")
                if "?" in condition:  # Handle filters like `[?(@.field="value")]`
                    field_name, field_value = parse_filter(condition)
                    if base_key in current_obj and isinstance(
                        current_obj[base_key], list
                    ):
                        return [
                            item
                            for item in current_obj.get(base_key, [])
                            if isinstance(item, dict)
                            and item.get(field_name) == field_value
                        ]
                elif condition == "*":  # Handle wildcard in array indexing
                    if base_key in current_obj and isinstance(
                        current_obj[base_key], list
                    ):
                        return [
                            result
                            for item in current_obj.get(base_key, [])
                            for result in recursive_find(keys[1:], item)
                        ]
                else:  # Regular array indexing
                    idx = int(condition)
                    if base_key in current_obj and isinstance(
                        current_obj[base_key], list
                    ):
                        array = current_obj.get(base_key, [])
                        if isinstance(array, list) and 0 <= idx < len(
                            array
                        ):  # Check index bounds
                            return recursive_find(keys[1:], array[idx])
                    return []
            except (ValueError, IndexError, KeyError, TypeError):
                return []  # Handle invalid array indexing gracefully

        else:  # Handle normal key lookup
            if isinstance(current_obj, dict):
                next_obj = current_obj.get(key)
                if next_obj is not None:  # Ensure the result is not None
                    return recursive_find(keys[1:], next_obj)
            return []

    def parse_filter(condition):
        # Parse filter conditions of the form `?(@.field == "value")`
        if condition.startswith("?(@.") and condition.endswith(")"):
            field, field_value = condition[4:-1].split(" == ")
            return field.strip(), field_value.strip("'")
        raise ValueError(f"Invalid condition: {condition}")

    # Dynamically create the filter based on the field and value
    cleaned_path = re.sub(r"\[\*\]$", "", jpath)
    filter_path = f"{cleaned_path}[?(@.{field} == '{value}')]"
    keys = split_jsonpath(filter_path)
    return recursive_find(keys, obj)


def split_jsonpath(jpath):
    """Splits the JSONPath into keys, handling filters properly."""
    result = []
    buffer = ""
    in_brackets = 0

    for char in jpath:
        if char == "." and in_brackets == 0:
            if buffer:
                result.append(buffer)
                buffer = ""
        elif char == "[":
            in_brackets += 1
            buffer += char
        elif char == "]":
            in_brackets -= 1
            buffer += char
        else:
            buffer += char

    if buffer:
        result.append(buffer)

    return [key for key in result if key != "$"]


def find_all_with_filters(jpath, filters, obj):
    # Construct the filter expression
    filter_expr = " & ".join(
        [f"@.{field} == '{value}'" for field, value in filters.items()]
    )
    cleaned_path = re.sub(r"\[\*\]$", "", jpath)
    jsonpath_expr = parse(ensure_root(f"{cleaned_path}[?({filter_expr})]"))
    return [m.value for m in jsonpath_expr.find(obj)]


def find_one(jpath, obj, default=None):
    matches = find_all(jpath, obj)

    return matches[0] if len(matches) > 0 else default


def get_dict_of_zones_and_terminals_served_by_hvac_sys(
    rpd: dict,
) -> dict[str, ZonesTerminalsServedByHVACSys]:
    """
    Returns a dictionary of zones and terminal IDs associated with each HVAC system in the RMD.

    Parameters
    ----------
    rpd: dict
    A dictionary representing a RuleModelDescription object as defined by the ASHRAE229 schema

    Returns ------- dict: a dictionary of zones and terminal IDs associated with each HVAC system in the RMD,
    {hvac_system_1.id: {"zone_list": [zone_1.id, zone_2.id, zone_3.id], "terminal_unit_list": [terminal_1.id,
    terminal_2.id, terminal_3.id]}, hvac_system_2.id: {"zone_list": [zone_4.id, zone_9.id, zone_30.id],
    "terminal_unit_list": [terminal_10.id, terminal_20.id, terminal_30.id]}}
    """
    dict_of_zones_and_terminals_served_by_hvac_sys: dict[
        str, ZonesTerminalsServedByHVACSys
    ] = {}

    for zone in find_all(
        "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*]",
        rpd,
    ):
        zone_id = zone["id"]
        for terminal in find_all("$.terminals[*]", zone):
            terminal_id = terminal["id"]
            hvac_sys_id = terminal.get(
                "served_by_heating_ventilating_air_conditioning_system"
            )
            if hvac_sys_id and isinstance(hvac_sys_id, str):
                if hvac_sys_id not in dict_of_zones_and_terminals_served_by_hvac_sys:
                    dict_of_zones_and_terminals_served_by_hvac_sys[hvac_sys_id] = {
                        "terminal_list": [],
                        "zone_list": [],
                    }

                zone_list = dict_of_zones_and_terminals_served_by_hvac_sys[hvac_sys_id][
                    "zone_list"
                ]
                if zone_id not in zone_list:
                    zone_list.append(zone_id)

                terminal_list = dict_of_zones_and_terminals_served_by_hvac_sys[
                    hvac_sys_id
                ]["terminal_list"]
                if terminal_id not in terminal_list:
                    terminal_list.append(terminal_id)

    return dict_of_zones_and_terminals_served_by_hvac_sys
