import sys
import os
import json
import math
from difflib import get_close_matches

from rpd_generator.utilities.jsonpath_utils import (
    find_one,
    find_all,
    find_all_with_field_value,
    find_all_with_filters,
    get_dict_of_zones_and_terminals_served_by_hvac_sys,
)


def load_json_file(file_path):
    """Loads JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)


def compare_json_values(spec, generated_values, reference_values, generated_ids):
    """Compares a list of generated and reference JSON values based on the spec."""
    json_key_path = spec["json-key-path"]
    compare_value = spec.get("compare-value", True)
    tolerance = spec.get("tolerance", 0)

    warnings = []
    errors = []

    for i, generated_id in enumerate(generated_ids):
        if generated_id not in generated_values and i in generated_values:
            generated_id = i
        generated_value = generated_values[generated_id]
        reference_value = reference_values[generated_id]

        if generated_value is None and reference_value is not None:
            warnings.append(
                f"Missing value for key '{json_key_path.split('.')[-1]}' at {generated_ids[i]}"
            )
            continue

        if isinstance(reference_value, dict):
            raise ValueError("json-test-key-path should not result in a dictionary.")

        elif isinstance(reference_value, list):

            if len(generated_value) != len(reference_value):
                errors.append(
                    f"List length mismatch at '{generated_ids[i]}' for key '{json_key_path.split('.')[-1]}'. Expected: {len(reference_value)}; got: {len(generated_value)}"
                )
                continue

            if compare_value:
                for j, (gen_item, ref_item) in enumerate(
                    zip(generated_value, reference_value)
                ):
                    if gen_item != ref_item:
                        errors.append(
                            f"List element mismatch for {generated_ids[i]} at index [{j}]. Expected: {ref_item}; got: {gen_item}"
                        )
                continue

        if compare_value is False:
            continue  # No comparison needed, just check for existence

        if reference_value is None and generated_value is None:
            continue  # Both values are None, no need to compare

        # Else: the values are strings, ints, or floats, and we need to compare them
        does_match = compare_values(generated_value, reference_value, tolerance)
        if not does_match and reference_value is None:
            warnings.append(
                f"Extra data provided at '{generated_ids[i]}' for key '{json_key_path.split('.')[-1]}'. Expected: 'None'; got: '{generated_value}'"
            )
        elif not does_match:
            errors.append(
                f"Value mismatch at '{generated_ids[i]}' for key '{json_key_path.split('.')[-1]}'. Expected: '{reference_value}'; got: '{generated_value}'"
            )

    return warnings, errors


def get_zones_from_json(json_data):
    """Extracts zones from the given JSON data."""
    return find_all(
        "$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]",
        json_data,
    )


def find_best_match(target, candidates, cutoff=0.4):
    """Finds the best match for a target in a list of candidates."""
    matches = get_close_matches(target, candidates, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def get_mapping(
    match_type,
    generated_values,
    reference_values,
    generated_zone_id=None,
    reference_zone_id=None,
    object_id_map=None,
):
    """Find matches for a key in the generated and reference JSON based on the json path in the spec."""
    mapping = {}
    if match_type == "Surfaces":
        mapping = match_by_attributes(
            generated_values,
            reference_values,
            generated_zone_id,
            reference_zone_id,
            ["area", "azimuth"],
        )

    if match_type == "HVAC Systems":
        mapping = match_sys_by_zones_served(
            generated_values, reference_values, object_id_map
        )
        if not mapping:
            mapping = match_by_attributes(
                generated_values,
                reference_values,
                generated_zone_id,
                reference_zone_id,
                ["cooling_system.type", "heating_system.type"],
            )

    if match_type == "Terminals":
        mapping = match_terminal_by_references(
            generated_values, reference_values, object_id_map
        )

    if match_type == "Boilers":
        mapping = match_by_attributes(
            generated_values,
            reference_values,
            generated_zone_id,
            reference_zone_id,
            ["draft_type", "energy_source_type"],
        )

    if match_type == "Chillers":
        mapping = match_by_attributes(
            generated_values,
            reference_values,
            generated_zone_id,
            reference_zone_id,
            ["compressor_type", "energy_source_type"],
        )

    if match_type == "Heat Rejections":
        mapping = match_by_attributes(
            generated_values,
            reference_values,
            generated_zone_id,
            reference_zone_id,
            ["type", "fan_type", "fan_speed_control"],
        )

    if match_type == "Loops":
        mapping = match_by_attributes(
            generated_values,
            reference_values,
            generated_zone_id,
            reference_zone_id,
            ["type", "child_loops"],
        )

    if match_type == "Pumps":
        mapping = match_pumps_by_references(
            generated_values, reference_values, object_id_map
        )

    # TODO: Expand capabilities when length of mapping is less than length of generated_values -e.g. unmatched objects
    if not mapping:
        mapping = match_by_id(generated_values, reference_values)

    return mapping


def match_by_id(generated_values, reference_values):
    """Matches generated and reference objects by ID."""
    mapping, used_ids = {}, set()
    for generated_object in generated_values:
        best_match = find_best_match(
            generated_object.get("id"), [ref.get("id") for ref in reference_values]
        )
        if best_match and best_match not in used_ids:
            mapping[generated_object.get("id")] = best_match
            used_ids.add(best_match)
    return mapping


def match_by_attributes(
    generated_values, reference_values, generated_zone_id, reference_zone_id, attrs
):
    """Matches generated and reference objects based on specified attributes."""
    mapping = {}
    for generated_object in generated_values:
        best_match = get_best_match_attrs(
            generated_object,
            reference_values,
            attrs,
            generated_zone_id,
            reference_zone_id,
        )
        if best_match:
            mapping[generated_object.get("id")] = best_match.get("id")
    return mapping


def match_sys_by_zones_served(generated_values, reference_values, object_id_map):
    mapping = {}

    # Create a dictionary to map sets of reference zones served to their corresponding HVAC IDs
    reference_zones_map = {
        frozenset(data["zone_list"]): ref_hvac_id
        for ref_hvac_id, data in reference_values.items()
    }

    # Match generated HVAC systems by looking up the set of corresponding reference zones
    for generated_hvac_id, data in generated_values.items():
        generated_hvac_zones_served = data["zone_list"]
        corresponding_reference_zones = [
            object_id_map.get(zone_id) for zone_id in generated_hvac_zones_served
        ]

        corresponding_reference_zones_set = frozenset(corresponding_reference_zones)

        if corresponding_reference_zones_set in reference_zones_map:
            mapping[generated_hvac_id] = reference_zones_map[
                corresponding_reference_zones_set
            ]

    return mapping


def match_terminal_by_references(generated_values, reference_values, object_id_map):
    """Matches generated and reference terminal objects based on references to the hvac systems that serve them."""
    mapping = {}
    for generated_object in generated_values:
        generated_hvac_id = generated_object.get(
            "served_by_heating_ventilating_air_conditioning_system"
        )
        if generated_hvac_id:
            reference_hvac_id = object_id_map.get(generated_hvac_id)
            if reference_hvac_id:
                best_match = next(
                    terminal
                    for terminal in reference_values
                    if terminal.get(
                        "served_by_heating_ventilating_air_conditioning_system"
                    )
                    == reference_hvac_id
                )
                if best_match:
                    mapping[generated_object.get("id")] = best_match.get("id")
        else:
            best_match = get_best_match_attrs(
                generated_object,
                reference_values,
                [
                    "type",
                    "is_supply_ducted",
                    "heating_source",
                    "heating_capacity",
                    "cooling_capacity",
                    "primary_airflow",
                    "minimum_outdoor_airflow",
                ],
                None,
                None,
            )
            if best_match:
                mapping[generated_object.get("id")] = best_match.get("id")

    return mapping


def match_pumps_by_references(generated_values, reference_values, object_id_map):
    """Match generated and reference pumps based on references to the loops that they serve."""
    mapping = {}
    for generated_object in generated_values:
        generated_loop_id = generated_object.get("loop_or_piping")
        if generated_loop_id:
            reference_loop_id = object_id_map.get(generated_loop_id)
            if reference_loop_id:
                best_match = next(
                    reference_value
                    for reference_value in reference_values
                    if reference_value.get("loop_or_piping") == reference_loop_id
                )
                if best_match:
                    mapping[generated_object.get("id")] = best_match
                    reference_values.pop(reference_values.index(best_match))

    return mapping


def get_best_match_attrs(
    target, candidates, attrs, generated_zone_id, reference_zone_id
):
    """Finds the best match for a target object based on specified attributes."""
    best_match_found, highest_qty_matched = None, 0
    for candidate in candidates:
        qty_matched = sum(
            compare_attributes(
                target, candidate, attr, generated_zone_id, reference_zone_id
            )
            for attr in attrs
        )
        if qty_matched > highest_qty_matched:
            highest_qty_matched, best_match_found = qty_matched, candidate
    return best_match_found


def compare_values(value, reference_value, tolerance):
    """Compares a generated value with a reference value based on the tolerance."""
    if isinstance(reference_value, str):
        return value == reference_value

    if isinstance(reference_value, bool):
        return value == reference_value

    if isinstance(reference_value, (int, float)):
        return math.isclose(value, reference_value, abs_tol=tolerance)

    return False


def compare_attributes(target, candidate, attr, generated_zone_id, reference_zone_id):
    """Compares attributes between two objects with special rules for azimuth and area."""
    target_value, candidate_value = target.get(attr), candidate.get(attr)
    if attr == "azimuth":
        return compare_azimuth(
            target,
            candidate,
            generated_zone_id,
            reference_zone_id,
            target_value,
            candidate_value,
        )

    elif attr == "area":
        return compare_values(target_value, candidate_value, 0.1)

    elif isinstance(target_value, list):
        candidate_length = len(candidate_value) if candidate_value else 0
        return len(target_value) == candidate_length

    else:
        return target_value == candidate_value


def compare_azimuth(
    target,
    candidate,
    generated_zone_id,
    reference_zone_id,
    target_value,
    candidate_value,
):
    """Special comparison rule for azimuth attributes."""
    mismatched_wall_origin_adjacent_zone = (
        target.get("adjacent_zone") == generated_zone_id
    ) != (candidate.get("adjacent_zone") == reference_zone_id)
    if (
        not mismatched_wall_origin_adjacent_zone and target_value == candidate_value
    ) or (
        mismatched_wall_origin_adjacent_zone
        and abs(target_value - candidate_value) == 180
    ):
        return 1
    return 0


def compare_fan_power(generated_fans, expected_w_per_flow):
    """Compare the design electric power based on design airflow."""
    warnings = []
    errors = []

    for fan in generated_fans:
        design_flow = fan.get("design_airflow")
        design_power = fan.get("design_electric_power")
        if not design_flow:
            warnings.append(f"Missing design airflow for '{fan['id']}'")
            continue

        if not design_power:
            warnings.append(f"Missing design electric power for '{fan['id']}'")
            continue

        if not compare_values(design_power, expected_w_per_flow * design_flow, 1):
            errors.append(
                f"Value mismatch at '{fan['id']}'. Expected: {expected_w_per_flow * design_flow}; got: {design_power}"
            )
    return warnings, errors


def compare_pump_power(pump: dict, expected_w_per_flow: float):
    """Compare the design electric power based on design airflow."""
    warnings = []
    errors = []

    design_flow = pump.get("design_flow")
    design_power = pump.get("design_electric_power")
    if not design_flow:
        warnings.append(f"Missing design flow for '{pump['id']}'")
        return warnings, errors

    if not design_power:
        warnings.append(f"Missing design electric power for '{pump['id']}'")
        return warnings, errors

    if not compare_values(design_power, expected_w_per_flow * design_flow, 1):
        errors.append(
            f"Value mismatch at '{pump['id']}'. Expected: {expected_w_per_flow * design_flow}; got: {design_power}"
        )
    return warnings, errors


def define_surface_map(generated_zone, reference_zone, generated_json, reference_json):
    generated_zone_id = generated_zone["id"]
    reference_zone_id = reference_zone["id"]
    surface_map = {}

    surface_types = [
        ("Exterior Wall", {"classification": "WALL", "adjacent_to": "EXTERIOR"}),
        ("Interior Wall", {"classification": "WALL", "adjacent_to": "INTERIOR"}),
        ("Ground Floor", {"classification": "FLOOR", "adjacent_to": "GROUND"}),
        ("Roof", {"classification": "CEILING", "adjacent_to": "EXTERIOR"}),
    ]

    for surface_type, filters in surface_types:
        generated_surfaces = find_all_with_filters(
            "$.surfaces[*]", filters, generated_zone
        )
        reference_surfaces = find_all_with_filters(
            "$.surfaces[*]", filters, reference_zone
        )

        if surface_type == "Interior Wall":
            # Extend with surfaces from other zones where this zone is the adjacent_zone
            generated_surfaces.extend(
                find_all_with_field_value(
                    "$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*]",
                    "adjacent_zone",
                    generated_zone_id,
                    generated_json,
                )
            )
            reference_surfaces.extend(
                find_all_with_field_value(
                    "$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*]",
                    "adjacent_zone",
                    reference_zone_id,
                    reference_json,
                )
            )

        local_surface_map = define_local_surface_map(
            generated_zone_id,
            reference_zone_id,
            surface_type,
            generated_surfaces,
            reference_surfaces,
        )[0]

        surface_map.update(local_surface_map)

    return surface_map


def define_local_surface_map(
    generated_zone_id,
    reference_zone_id,
    surface_type,
    generated_surfaces,
    reference_surfaces,
):
    errors = []
    local_surface_map = {}

    if len(generated_surfaces) != len(reference_surfaces):
        errors.append(
            f"{surface_type} surface count mismatch in zone id '{generated_zone_id}'. Expected: {len(reference_surfaces)}; got: {len(generated_surfaces)}"
        )
        return local_surface_map, errors

    elif len(generated_surfaces) == 1:
        local_surface_map[generated_surfaces[0]["id"]] = reference_surfaces[0]["id"]
        return local_surface_map, errors

    else:
        local_surface_map = get_mapping(
            "Surfaces",
            generated_surfaces,
            reference_surfaces,
            generated_zone_id=generated_zone_id,
            reference_zone_id=reference_zone_id,
        )
        return local_surface_map, errors


def define_hvac_map(generated_json, reference_json, object_id_map):
    errors = []
    hvac_map = {}

    generated_hvacs = get_dict_of_zones_and_terminals_served_by_hvac_sys(generated_json)
    reference_hvacs = get_dict_of_zones_and_terminals_served_by_hvac_sys(reference_json)

    if len(generated_hvacs) != len(reference_hvacs):
        errors.append(
            f"HVAC system count mismatch. Expected: {len(reference_hvacs)}; got: {len(generated_hvacs)}"
        )
        return hvac_map, errors

    if len(generated_hvacs) == 1:
        generated_hvac_id, generated_hvac_data = next(iter(generated_hvacs.items()))
        reference_hvac_id, reference_hvac_data = next(iter(reference_hvacs.items()))
        hvac_map[generated_hvac_id] = reference_hvac_id
        return hvac_map, errors

    else:
        hvac_map = get_mapping(
            "HVAC Systems",
            generated_hvacs,
            reference_hvacs,
            object_id_map=object_id_map,
        )

    return hvac_map, errors


def define_terminal_map(object_id_map, generated_zone, reference_zone):
    errors = []
    terminal_map = {}

    generated_terminals = find_all(
        "$.terminals[*]",
        generated_zone,
    )
    reference_terminals = find_all(
        "$.terminals[*]",
        reference_zone,
    )

    generated_zone_id = generated_zone.get("id")

    if len(generated_terminals) != len(reference_terminals):
        errors.append(
            f"Terminal count mismatch in zone id '{generated_zone_id}'. Expected: {len(reference_terminals)}; got: {len(generated_terminals)}"
        )
        return terminal_map, errors

    if len(generated_terminals) == 1:
        terminal_map[generated_terminals[0]["id"]] = reference_terminals[0]["id"]
        return terminal_map, errors

    else:
        terminal_map = get_mapping(
            "Terminals",
            generated_terminals,
            reference_terminals,
            generated_zone_id=generated_zone_id,
            reference_zone_id=reference_zone["id"],
            object_id_map=object_id_map,
        )
    return terminal_map, errors


def define_boiler_map(generated_json, reference_json, object_id_map):
    errors = []
    boiler_map = {}

    generated_boilers = find_all(
        "$.ruleset_model_descriptions[0].boilers[*]",
        generated_json,
    )
    reference_boilers = find_all(
        "$.ruleset_model_descriptions[0].boilers[*]",
        reference_json,
    )

    if len(generated_boilers) != len(reference_boilers):
        errors.append(
            f"Boiler count mismatch. Expected: {len(reference_boilers)}; got: {len(generated_boilers)}"
        )
        return boiler_map, errors

    if len(generated_boilers) == 1:
        generated_boiler_data = generated_boilers[0]
        reference_boiler_data = reference_boilers[0]
        boiler_map[generated_boiler_data["id"]] = reference_boiler_data["id"]
        return boiler_map, errors

    else:
        boiler_map = get_mapping(
            "Boilers",
            generated_boilers,
            reference_boilers,
            object_id_map=object_id_map,
        )

    return boiler_map, errors


def define_chiller_map(generated_json, reference_json, object_id_map):
    errors = []
    chiller_map = {}

    generated_chillers = find_all(
        "$.ruleset_model_descriptions[0].chillers[*]",
        generated_json,
    )
    reference_chillers = find_all(
        "$.ruleset_model_descriptions[0].chillers[*]",
        reference_json,
    )

    if len(generated_chillers) != len(reference_chillers):
        errors.append(
            f"Chiller count mismatch. Expected: {len(reference_chillers)}; got: {len(generated_chillers)}"
        )
        return chiller_map, errors

    if len(generated_chillers) == 1:
        generated_chiller_data = generated_chillers[0]
        reference_chiller_data = reference_chillers[0]
        chiller_map[generated_chiller_data["id"]] = reference_chiller_data["id"]
        return chiller_map, errors

    else:
        chiller_map = get_mapping(
            "Chillers",
            generated_chillers,
            reference_chillers,
            object_id_map=object_id_map,
        )

    return chiller_map, errors


def define_heat_rejection_map(generated_json, reference_json, object_id_map):
    errors = []
    heat_rejection_map = {}

    generated_heat_rejections = find_all(
        "$.ruleset_model_descriptions[0].heat_rejections[*]",
        generated_json,
    )
    reference_heat_rejections = find_all(
        "$.ruleset_model_descriptions[0].heat_rejections[*]",
        reference_json,
    )

    if len(generated_heat_rejections) != len(reference_heat_rejections):
        errors.append(
            f"Heat Rejection count mismatch. Expected: {len(reference_heat_rejections)}; got: {len(generated_heat_rejections)}"
        )
        return heat_rejection_map, errors

    if len(generated_heat_rejections) == 1:
        generated_heat_rejection_data = generated_heat_rejections[0]
        reference_heat_rejection_data = reference_heat_rejections[0]
        heat_rejection_map[generated_heat_rejection_data["id"]] = (
            reference_heat_rejection_data["id"]
        )
        return heat_rejection_map, errors

    else:
        heat_rejection_map = get_mapping(
            "Heat Rejections",
            generated_heat_rejections,
            reference_heat_rejections,
            object_id_map=object_id_map,
        )

    return heat_rejection_map, errors


def define_loop_map(generated_json, reference_json, object_id_map):
    errors = []
    loop_map = {}

    generated_loops = find_all(
        "$.ruleset_model_descriptions[0].fluid_loops[*]",
        generated_json,
    )
    generated_loops.extend(
        find_all(
            "$.ruleset_model_descriptions[0].fluid_loops[*].child_loops[*]",
            generated_json,
        )
    )
    reference_loops = find_all(
        "$.ruleset_model_descriptions[0].fluid_loops[*]",
        reference_json,
    )
    reference_loops.extend(
        find_all(
            "$.ruleset_model_descriptions[0].fluid_loops[*].child_loops[*]",
            reference_json,
        )
    )

    if len(generated_loops) != len(reference_loops):
        errors.append(
            f"Loop count mismatch. Expected: {len(reference_loops)}; got: {len(generated_loops)}"
        )
        return loop_map, errors

    if len(generated_loops) == 1:
        generated_loop_data = generated_loops[0]
        reference_loop_data = reference_loops[0]
        loop_map[generated_loop_data["id"]] = reference_loop_data["id"]
        return loop_map, errors

    else:
        loop_map = get_mapping(
            "Loops",
            generated_loops,
            reference_loops,
            object_id_map=object_id_map,
        )

    return loop_map, errors


def define_pump_map(generated_json, reference_json, object_id_map):
    errors = []
    pump_map = {}

    generated_pumps = find_all(
        "$.ruleset_model_descriptions[0].pumps[*]",
        generated_json,
    )
    reference_pumps = find_all(
        "$.ruleset_model_descriptions[0].pumps[*]",
        reference_json,
    )

    if len(generated_pumps) != len(reference_pumps):
        errors.append(
            f"Pump count mismatch. Expected: {len(reference_pumps)}; got: {len(generated_pumps)}"
        )
        return pump_map, errors

    if len(generated_pumps) == 1:
        generated_pump_data = generated_pumps[0]
        reference_pump_data = reference_pumps[0]
        pump_map[generated_pump_data["id"]] = reference_pump_data["id"]
        return pump_map, errors

    else:
        pump_map = get_mapping(
            "Pumps",
            generated_pumps,
            reference_pumps,
            object_id_map=object_id_map,
        )

    return pump_map, errors


def map_objects(generated_json, reference_json):
    warnings = []
    errors = []

    generated_zones = get_zones_from_json(generated_json)
    reference_zones = get_zones_from_json(reference_json)

    # Define a map for Zones. ! Maps for other objects will depend on this map !
    object_id_map = get_mapping("Zones", generated_zones, reference_zones)

    if len(object_id_map) != len(reference_zones):
        errors.append(
            f"""Could not match zones between the generated and reference files. Try to better align your modeled zone names with the correct answer file's zone naming conventions.\n{chr(10).join(f"- {zone['id']}" for zone in reference_zones)}"""
        )  # chr(10) is a newline character
        # Return early if zones could not be matched
        return object_id_map, warnings, errors

    # Define maps for HVAC systems
    hvac_map, hvac_map_errors = define_hvac_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(hvac_map)
    errors.extend(hvac_map_errors)

    reference_zone_ids = [zone["id"] for zone in reference_zones]

    for i, generated_zone in enumerate(generated_zones):
        generated_zone_id = generated_zone["id"]
        reference_zone_id = object_id_map[generated_zone_id]
        reference_zone = reference_zones[reference_zone_ids.index(reference_zone_id)]

        # Define maps for surfaces
        surface_map = define_surface_map(
            generated_zone, reference_zone, generated_json, reference_json
        )
        object_id_map.update(surface_map)

        # Define maps for terminals
        terminal_map, terminal_map_errors = define_terminal_map(
            object_id_map,
            generated_zone,
            reference_zone,
        )
        object_id_map.update(terminal_map)
        errors.extend(terminal_map_errors)

    boiler_map, boiler_map_errors = define_boiler_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(boiler_map)
    errors.extend(boiler_map_errors)

    chiller_map, chiller_map_errors = define_chiller_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(chiller_map)
    errors.extend(chiller_map_errors)

    heat_rejection_map, heat_rejection_map_errors = define_heat_rejection_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(heat_rejection_map)
    errors.extend(heat_rejection_map_errors)

    loop_map, loop_map_errors = define_loop_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(loop_map)
    errors.extend(loop_map_errors)

    pump_map, pump_map_errors = define_pump_map(
        generated_json, reference_json, object_id_map
    )
    object_id_map.update(pump_map)
    errors.extend(pump_map_errors)

    return object_id_map, warnings, errors


def handle_special_cases(path_spec, object_id_map, generated_json, reference_json):
    warnings = []
    errors = []

    json_key_path = path_spec["json-key-path"]
    special_case = path_spec["special-case"]

    # Handle Special Case for design electric power based on design airflow (which is not a specified value)
    if special_case == "W/cfm":
        special_case_value = path_spec["special-case-value"]

        generated_supply_fans = [
            fan
            for sys_fans in find_all(
                "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].fan_system.supply_fans",
                generated_json,
            )
            for fan in sys_fans
        ]
        compare_fan_power_warnings, compare_fan_power_errors = compare_fan_power(
            generated_supply_fans, special_case_value
        )
        if compare_fan_power_warnings:
            warnings.extend(compare_fan_power_warnings)
        if compare_fan_power_errors:
            errors.extend(compare_fan_power_errors)

    # Handle Special Case for design electric power based on design airflow (which is not a specified value)
    elif special_case == "W/GPM":
        special_case_value_dict = path_spec["special-case-value"]
        special_case_value = None

        generated_pumps = find_all(
            "$.ruleset_model_descriptions[*].pumps[*]",
            generated_json,
        )

        for pump in generated_pumps:
            pump_type = "primary"
            loop_id = pump.get("loop_or_piping")
            loop = find_all_with_field_value(
                "$.ruleset_model_descriptions[*].fluid_loops[*]",
                "id",
                loop_id,
                generated_json,
            )

            if not loop:
                pump_type = "secondary"
                loop = find_all_with_field_value(
                    "$.ruleset_model_descriptions[*].fluid_loops[*].child_loops[*]",
                    "id",
                    loop_id,
                    generated_json,
                )

            if not loop:
                errors.append(
                    f"Could not find loop with id '{loop_id}' for pump '{pump['id']}'"
                )
                continue

            loop = loop[0]
            loop_type = loop.get("type")

            if loop_type == "COOLING" and pump_type == "primary":
                special_case_value = special_case_value_dict["PCHW"]
            elif loop_type == "COOLING" and pump_type == "secondary":
                special_case_value = special_case_value_dict["SCHW"]
            elif loop_type == "HEATING":
                special_case_value = special_case_value_dict["HW"]
            elif loop_type == "CONDENSER":
                special_case_value = special_case_value_dict["CW"]

            compare_pump_power_warnings, compare_pump_power_errors = compare_pump_power(
                pump, special_case_value
            )
            if compare_pump_power_warnings:
                warnings.extend(
                    f"Warning at {json_key_path.split('.')[-1]}: {warn}"
                    for warn in compare_pump_power_warnings
                )
            if compare_pump_power_errors:
                errors.extend(
                    f"Error at {json_key_path.split('.')[-1]}: {err}"
                    for err in compare_pump_power_errors
                )

    # Handle Special Case for interior wall azimuths (which may be opposite due to the adjacent zone)
    elif special_case == "azimuth":
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_zones = get_zones_from_json(generated_json)

        generated_surfaces = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("surfaces")) + 1
            ],
            generated_json,
        )

        # Iterate through the generated surfaces to populate data for each surface individually, ensuring correct alignment via object mapping
        for generated_surface in generated_surfaces:
            generated_surface_id = generated_surface["id"]
            reference_surface_id = object_id_map.get(generated_surface_id)

            aligned_reference_surface = find_one(
                json_key_path[
                    : json_key_path.index("].", json_key_path.index("surfaces")) + 1
                ]
                + f'[?(@.id="{reference_surface_id}")]',
                reference_json,
                None,
            )

            generated_parent_zone = next(
                zone
                for zone in generated_zones
                if any(
                    surface["id"] == generated_surface_id
                    for surface in zone.get("surfaces", [])
                )
            )
            generated_parent_zone_id = generated_parent_zone["id"]
            reference_parent_zone_id = object_id_map.get(generated_parent_zone_id)

            generated_value = generated_surface.get(json_key_path.split(".")[-1])
            aligned_generated_values[generated_surface_id] = generated_value
            # Extract values from aligned surfaces using the specified key path
            if "surfaces[*][?(@" in json_key_path:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "surfaces[*][?(",
                        f'surfaces[*][?(@.id="{reference_surface_id}" and ',
                    ),
                    reference_json,
                    None,
                )
            else:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "surfaces[*]",
                        f'surfaces[*][?(@.id="{reference_surface_id}")]',
                    ),
                    reference_json,
                    None,
                )
            aligned_reference_values[generated_surface_id] = aligned_reference_value

            mismatched_wall_origin_adjacent_zone = (
                aligned_reference_surface.get("adjacent_zone")
                == reference_parent_zone_id
            ) != (generated_surface.get("adjacent_zone") == generated_parent_zone_id)
            if not (
                (
                    not mismatched_wall_origin_adjacent_zone
                    and aligned_reference_value == generated_value
                )
                or (
                    mismatched_wall_origin_adjacent_zone
                    and (aligned_reference_value + 180) % 360 == generated_value
                )
            ):
                expected_value = (
                    aligned_reference_value
                    if not mismatched_wall_origin_adjacent_zone
                    else (aligned_reference_value + 180) % 360
                )

                errors.append(
                    f"Value mismatch at '{generated_surface_id}' for key '{json_key_path.split('.')[-1]}': Expected '{expected_value}', got '{generated_value}'"
                )

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")

    return warnings, errors


def handle_ordered_comparisons(
    path_spec, object_id_map, reference_json, generated_json
):
    json_key_path = path_spec["json-key-path"]

    warnings = []
    errors = []

    # Handle comparison of data derived from zones which may not be in the same order as the reference zones
    if (
        "zones[" in json_key_path
        and "surfaces[" not in json_key_path
        and "terminals[" not in json_key_path
    ):
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_zones = get_zones_from_json(generated_json)
        generated_zone_ids = [zone["id"] for zone in generated_zones]

        # Populate data for each zone individually and ensure correct alignment via object mapping
        for generated_zone in generated_zones:
            generated_zone_id = generated_zone["id"]
            reference_zone_id = object_id_map[generated_zone_id]

            zone_data_path = json_key_path[
                (json_key_path.index("].", json_key_path.index("zones")) + 2) :
            ]
            generated_value = find_one(zone_data_path, generated_zone)
            aligned_generated_values[generated_zone_id] = generated_value
            # Extract values from aligned zones using the specified key path
            aligned_reference_value = find_one(
                json_key_path.replace(
                    "zones[*]", f'zones[*][?(@.id="{reference_zone_id}")]'
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_zone_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_zone_ids,
        )
        errors.extend(general_comparison_errors)

    elif "surfaces[" in json_key_path:
        # Handle comparison of data derived from surfaces which may not be in the same order as the reference surfaces
        aligned_generated_values = {}
        aligned_reference_values = {}

        # Populate data for each surface individually and ensure correct alignment via object mapping
        generated_surfaces = find_all(
            # Extract the key path for the surface (everything before surfaces[]. )
            json_key_path[
                : json_key_path.index("].", json_key_path.index("surfaces")) + 1
            ],
            generated_json,
        )
        generated_surface_ids = [surface["id"] for surface in generated_surfaces]

        for generated_surface in generated_surfaces:
            generated_surface_id = generated_surface["id"]
            reference_surface_id = object_id_map.get(generated_surface_id)

            generated_value = find_one(
                # Extract the key path for the surface data (everything after surfaces[]. )
                json_key_path[
                    (json_key_path.index("].", json_key_path.index("surfaces"))) + 2 :
                ],
                generated_surface,
            )
            aligned_generated_values[generated_surface_id] = generated_value

            # Extract values from aligned surfaces using the specified key path
            if "surfaces[*][?(@" in json_key_path:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "surfaces[*][?(",
                        f'surfaces[*][?(@.id="{reference_surface_id}" and ',
                    ),
                    reference_json,
                    None,
                )
            else:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "surfaces[*]",
                        f'surfaces[*][?(@.id="{reference_surface_id}")]',
                    ),
                    reference_json,
                    None,
                )

            aligned_reference_values[generated_surface_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_surface_ids,
        )
        warnings.extend(general_comparison_warnings)
        errors.extend(general_comparison_errors)

    elif "terminals[" in json_key_path:
        # Handle comparison of data derived from surfaces which may not be in the same order as the reference surfaces
        aligned_generated_values = {}
        aligned_reference_values = {}

        # Populate data for each surface individually and ensure correct alignment via object mapping
        generated_terminals = find_all(
            # Extract the key path for the surface (everything before surfaces[]. )
            json_key_path[
                : json_key_path.index("].", json_key_path.index("terminals")) + 1
            ],
            generated_json,
        )
        generated_terminal_ids = [terminal["id"] for terminal in generated_terminals]

        for generated_terminal in generated_terminals:
            generated_terminal_id = generated_terminal["id"]
            reference_terminal_id = object_id_map.get(generated_terminal_id)

            generated_value = find_one(
                # Extract the key path for the terminal data (everything after terminals[]. )
                json_key_path[
                    (json_key_path.index("].", json_key_path.index("terminals"))) + 2 :
                ],
                generated_terminal,
            )
            aligned_generated_values[generated_terminal_id] = generated_value

            # Extract values from aligned terminals using the specified key path
            if "terminals[*][?(@" in json_key_path:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "terminals[*][?(",
                        f'terminals[*][?(@.id="{reference_terminal_id}" and ',
                    ),
                    reference_json,
                    None,
                )
            else:
                aligned_reference_value = find_one(
                    json_key_path.replace(
                        "terminals[*]",
                        f'terminals[*][?(@.id="{reference_terminal_id}")]',
                    ),
                    reference_json,
                    None,
                )

            aligned_reference_values[generated_terminal_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_terminal_ids,
        )
        warnings.extend(general_comparison_warnings)
        errors.extend(general_comparison_errors)

    elif "heating_ventilating_air_conditioning_systems[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_hvacs = find_all(
            json_key_path[
                : json_key_path.index(
                    "].",
                    json_key_path.index("heating_ventilating_air_conditioning_systems"),
                )
                + 1
            ],
            generated_json,
        )
        generated_hvac_ids = [hvac["id"] for hvac in generated_hvacs]

        # Populate data for each zone individually and ensure correct alignment via object mapping
        for generated_boiler in generated_hvacs:
            generated_boiler_id = generated_boiler["id"]
            reference_boiler_id = object_id_map[generated_boiler_id]

            hvac_data_path = json_key_path[
                json_key_path.index(
                    "].",
                    json_key_path.index("heating_ventilating_air_conditioning_systems"),
                )
                + 2 :
            ]
            generated_value = find_one(hvac_data_path, generated_boiler)
            aligned_generated_values[generated_boiler_id] = generated_value
            # Extract values from aligned zones using the specified key path
            aligned_reference_value = find_one(
                json_key_path.replace(
                    "heating_ventilating_air_conditioning_systems[*]",
                    f'heating_ventilating_air_conditioning_systems[*][?(@.id="{reference_boiler_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_boiler_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_hvac_ids,
        )
        errors.extend(general_comparison_errors)

    elif "boilers[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_boilers = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("boilers")) + 1
            ],
            generated_json,
        )
        generated_boiler_ids = [boiler["id"] for boiler in generated_boilers]

        for generated_boiler in generated_boilers:
            generated_boiler_id = generated_boiler["id"]
            reference_boiler_id = object_id_map[generated_boiler_id]

            boiler_data_path = json_key_path[
                json_key_path.index("].", json_key_path.index("boilers")) + 2 :
            ]
            generated_value = find_one(boiler_data_path, generated_boiler)
            aligned_generated_values[generated_boiler_id] = generated_value

            aligned_reference_value = find_one(
                json_key_path.replace(
                    "boilers[*]",
                    f'boilers[*][?(@.id="{reference_boiler_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_boiler_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_boiler_ids,
        )
        errors.extend(general_comparison_errors)

    elif "chillers[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_chillers = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("chillers")) + 1
            ],
            generated_json,
        )
        generated_chiller_ids = [chiller["id"] for chiller in generated_chillers]

        for generated_chiller in generated_chillers:
            generated_chiller_id = generated_chiller["id"]
            reference_chiller_id = object_id_map[generated_chiller_id]

            chiller_data_path = json_key_path[
                json_key_path.index("].", json_key_path.index("chillers")) + 2 :
            ]
            generated_value = find_one(chiller_data_path, generated_chiller)
            aligned_generated_values[generated_chiller_id] = generated_value

            aligned_reference_value = find_one(
                json_key_path.replace(
                    "chillers[*]",
                    f'chillers[*][?(@.id="{reference_chiller_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_chiller_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_chiller_ids,
        )
        errors.extend(general_comparison_errors)

    elif "heat_rejections[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_heat_rejections = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("heat_rejections")) + 1
            ],
            generated_json,
        )
        generated_heat_rejection_ids = [
            heat_rejection["id"] for heat_rejection in generated_heat_rejections
        ]

        for generated_heat_rejection in generated_heat_rejections:
            generated_heat_rejection_id = generated_heat_rejection["id"]
            reference_heat_rejection_id = object_id_map[generated_heat_rejection_id]

            heat_rejection_data_path = json_key_path[
                json_key_path.index("].", json_key_path.index("heat_rejections")) + 2 :
            ]
            generated_value = find_one(
                heat_rejection_data_path, generated_heat_rejection
            )
            aligned_generated_values[generated_heat_rejection_id] = generated_value

            aligned_reference_value = find_one(
                json_key_path.replace(
                    "heat_rejections[*]",
                    f'heat_rejections[*][?(@.id="{reference_heat_rejection_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_heat_rejection_id] = (
                aligned_reference_value
            )

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_heat_rejection_ids,
        )
        errors.extend(general_comparison_errors)

    elif "fluid_loops[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_fluid_loops = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("fluid_loops")) + 1
            ],
            generated_json,
        )
        generated_fluid_loop_ids = [
            fluid_loop["id"] for fluid_loop in generated_fluid_loops
        ]

        for generated_fluid_loop in generated_fluid_loops:
            generated_fluid_loop_id = generated_fluid_loop["id"]
            reference_fluid_loop_id = object_id_map[generated_fluid_loop_id]

            fluid_loop_data_path = json_key_path[
                json_key_path.index("].", json_key_path.index("fluid_loops")) + 2 :
            ]
            generated_value = find_one(fluid_loop_data_path, generated_fluid_loop)
            aligned_generated_values[generated_fluid_loop_id] = generated_value

            aligned_reference_value = find_one(
                json_key_path.replace(
                    "fluid_loops[*]",
                    f'fluid_loops[*][?(@.id="{reference_fluid_loop_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_fluid_loop_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_fluid_loop_ids,
        )
        errors.extend(general_comparison_errors)

    elif "pumps[" in json_key_path:
        aligned_generated_values = {}
        aligned_reference_values = {}

        generated_pumps = find_all(
            json_key_path[
                : json_key_path.index("].", json_key_path.index("pumps")) + 1
            ],
            generated_json,
        )
        generated_pump_ids = [pump["id"] for pump in generated_pumps]

        for generated_pump in generated_pumps:
            generated_pump_id = generated_pump["id"]
            reference_pump_id = object_id_map[generated_pump_id]

            pump_data_path = json_key_path[
                json_key_path.index("].", json_key_path.index("pumps")) + 2 :
            ]
            generated_value = find_one(pump_data_path, generated_pump)
            aligned_generated_values[generated_pump_id] = generated_value

            aligned_reference_value = find_one(
                json_key_path.replace(
                    "pumps[*]",
                    f'pumps[*][?(@.id="{reference_pump_id}")]',
                ),
                reference_json,
                None,
            )

            aligned_reference_values[generated_pump_id] = aligned_reference_value

        if all(value is None for value in aligned_generated_values.values()):
            warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
            return warnings, errors

        general_comparison_warnings, general_comparison_errors = compare_json_values(
            path_spec,
            aligned_generated_values,
            aligned_reference_values,
            generated_pump_ids,
        )
        errors.extend(general_comparison_errors)

    return warnings, errors


def handle_unordered_comparisons(path_spec, reference_json, generated_json):
    json_key_path = path_spec["json-key-path"]

    warnings = []
    errors = []
    # The order will be the same for the generated and reference values, or the order does not matter in the tests
    generated_value_parents = find_all(
        ".".join(json_key_path.split(".")[:-1]), generated_json
    )
    generated_value_parent_ids = [
        # Important to use get() here to avoid key errors where objects have no ID such as weather
        value.get("id")
        for value in generated_value_parents
    ]
    generated_values = find_all(json_key_path, generated_json)
    generated_values = {index: value for index, value in enumerate(generated_values)}
    reference_values = find_all(json_key_path, reference_json)
    reference_values = {index: value for index, value in enumerate(reference_values)}

    if all(value is None for value in generated_values):
        warnings.append(f"Missing key {json_key_path.split('.')[-1]}")
        return warnings, errors

    general_comparison_warnings, general_comparison_errors = compare_json_values(
        path_spec,
        generated_values,
        reference_values,
        generated_value_parent_ids,
    )
    warnings.extend(general_comparison_warnings)
    errors.extend(general_comparison_errors)

    return warnings, errors


def run_file_comparison(spec_file, generated_json_file, reference_json_file):
    """Compares generated and reference JSON files according to the spec."""
    spec = load_json_file(spec_file)
    json_test_key_paths = spec.get("json-test-key-paths", [])

    generated_json = load_json_file(generated_json_file)
    reference_json = load_json_file(reference_json_file)

    warnings = []
    errors = []

    object_id_map, map_warnings, map_errors = map_objects(
        generated_json, reference_json
    )
    warnings.extend(map_warnings)
    errors.extend(map_errors)
    if not object_id_map:
        return warnings, errors

    # Once maps have been defined, iterate through the test specs
    for path_spec in json_test_key_paths:
        json_key_path = path_spec["json-key-path"]
        special_case = path_spec.get("special-case")

        # Handle any cases that require special logic
        if special_case:
            special_case_warnings, special_case_errors = handle_special_cases(
                path_spec, object_id_map, generated_json, reference_json
            )
            warnings.extend(special_case_warnings)
            errors.extend(special_case_errors)

        # Begin the General Comparison Methodology
        else:

            # Handle comparison of data derived from objects which may not be in the same order as the reference objects
            if any(
                group in json_key_path
                for group in [
                    "zones[",
                    "surfaces[",
                    "terminals[",
                    "heating_ventilating_air_conditioning_systems[",
                    "boilers[",
                    "chillers[",
                    "heat_rejections[",
                    "fluid_loops[",
                    "pumps[",
                ]
            ):
                (
                    ordered_comparison_warnings,
                    ordered_comparison_errors,
                ) = handle_ordered_comparisons(
                    path_spec, object_id_map, reference_json, generated_json
                )
                warnings.extend(ordered_comparison_warnings)
                errors.extend(ordered_comparison_errors)

            # Handle comparison of data that is not dependent on order
            else:
                (
                    unordered_comparison_warnings,
                    unordered_comparison_errors,
                ) = handle_unordered_comparisons(
                    path_spec, reference_json, generated_json
                )
                warnings.extend(unordered_comparison_warnings)
                errors.extend(unordered_comparison_errors)

    return warnings, errors


def run_comparison_for_all_tests(test_dir):
    """Runs JSON comparison for all test cases in the test directory."""

    reference_dir = os.path.join(test_dir, "Correct Answer RPDs")
    spec_dir = os.path.join(test_dir, "Test Specifications")

    total_errors = 0

    for test in os.listdir(test_dir):
        # Only recognize directories starting with "E-" or "F-" as test cases
        if os.path.isdir(test_dir) and (test.startswith("E-") or test.startswith("F-")):

            test_case_dir = os.path.join(test_dir, test)
            generated_json_file = next(
                (
                    os.path.join(test_case_dir, f)
                    for f in os.listdir(test_case_dir)
                    if f.endswith(".json")
                ),
                None,
            )
            spec_file = os.path.join(spec_dir, f"{test} spec.json")
            reference_json_file = os.path.join(reference_dir, f"{test}.json")

            if (
                generated_json_file
                and os.path.isfile(spec_file)
                and os.path.isfile(generated_json_file)
                and os.path.isfile(reference_json_file)
            ):
                print(f"Running comparison for {test}...")
                warnings, errors = run_file_comparison(
                    spec_file, generated_json_file, reference_json_file
                )
                print_results(test, warnings, errors)
                total_errors += len(errors)

    if total_errors > 0:
        sys.exit(1)


def print_results(test, warnings, errors):
    """Prints the comparison results."""
    if warnings:
        print(
            f"""----------------------------
    Warnings for {test}:
----------------------------"""
        )
        for warning in warnings:
            print(f"{warning}")
    if errors:
        print(
            f"""----------------------------
    Errors for {test}:
----------------------------"""
        )
        for error in errors:
            print(f"{error}")


if __name__ == "__main__":
    test_directory = os.path.dirname(os.path.abspath(__file__))
    run_comparison_for_all_tests(test_directory)
