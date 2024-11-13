from itertools import chain
from jsonpath2 import match
from typing import TypedDict


class ZonesTerminalsServedByHVACSys(TypedDict):
    terminal_list: list[str]
    zone_list: list[str]


def create_jsonpath_value_dict(jpath, obj):
    return {
        m.node.tojsonpath(): m.current_value for m in match(ensure_root(jpath), obj)
    }


def ensure_root(jpath):
    return jpath if jpath.startswith("$") else "$." + jpath


def find_all(jpath, obj):
    return [m.current_value for m in match(ensure_root(jpath), obj) if m]


def find_all_by_jsonpaths(jpaths: list, obj: dict) -> list:
    return list(chain.from_iterable([find_all(jpath, obj) for jpath in jpaths]))


def find_all_with_field_value(jpath, field, value, obj):
    return [
        m.current_value
        for m in match(ensure_root(f'{jpath}[?(@.{field}="{value}")]'), obj)
    ]


def find_all_with_filters(jpath, filters, obj):
    # Construct the filter expression
    filter_expr = " and ".join(
        [f'@.{field}="{value}"' for field, value in filters.items()]
    )

    return [
        m.current_value for m in match(ensure_root(f"{jpath}[?({filter_expr})]"), obj)
    ]


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
