import os
import json
import unittest
from ..full_rpd_test import run_full_rpd_tests as rpd_tests


class TestRunFullRPDTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.reference_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "Zone 1",
                                            "surfaces": [
                                                {
                                                    "id": "Zone 1 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 1 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Zone 1 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Zone 2",
                                            "surfaces": [
                                                {
                                                    "id": "Zone 2 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 2 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Zone 2 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Zone 3",
                                            "surfaces": [
                                                {
                                                    "id": "Zone 3 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Zone 3 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 3 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Zone 4",
                                            "surfaces": [
                                                {
                                                    "id": "Zone 4 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 4 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Zone 4 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Zone 5",
                                            "surfaces": [
                                                {
                                                    "id": "Zone 5 Interior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 1",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 5 Interior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 2",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Zone 5 Interior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 3",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Zone 5 Interior Wall 4",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 4",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                            ],
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

    def test_get_zone_mapping_1(self):
        generated_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "Room 1",
                                        },
                                        {
                                            "id": "Room 2",
                                        },
                                        {
                                            "id": "Room 3",
                                        },
                                        {
                                            "id": "Room 4",
                                        },
                                        {
                                            "id": "Room 5",
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        generated_zones = rpd_tests.get_zones_from_json(generated_json)
        reference_zones = rpd_tests.get_zones_from_json(self.reference_json)

        # Define a map for Zones. ! Maps for other objects will depend on this map !
        object_id_map = rpd_tests.get_mapping("Zones", generated_zones, reference_zones)
        self.assertEqual(
            object_id_map,
            {
                "Room 1": "Zone 1",
                "Room 2": "Zone 2",
                "Room 3": "Zone 3",
                "Room 4": "Zone 4",
                "Room 5": "Zone 5",
            },
        )

    def test_get_zone_mapping_2(self):

        generated_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "123 - Zn2",
                                        },
                                        {
                                            "id": "123 - Zn4",
                                        },
                                        {
                                            "id": "123 - Zn1",
                                        },
                                        {
                                            "id": "123 - Zn5",
                                        },
                                        {
                                            "id": "123 - Zn3",
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        generated_zones = rpd_tests.get_zones_from_json(generated_json)
        reference_zones = rpd_tests.get_zones_from_json(self.reference_json)

        # Define a map for Zones. ! Maps for other objects will depend on this map !
        object_id_map = rpd_tests.get_mapping("Zones", generated_zones, reference_zones)
        self.assertEqual(
            object_id_map,
            {
                "123 - Zn2": "Zone 2",
                "123 - Zn4": "Zone 4",
                "123 - Zn1": "Zone 1",
                "123 - Zn5": "Zone 5",
                "123 - Zn3": "Zone 3",
            },
        )

    def test_get_zone_mapping_3(self):

        generated_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "Z - 1",
                                        },
                                        {
                                            "id": "Z - 2",
                                        },
                                        {
                                            "id": "Z - 3",
                                        },
                                        {
                                            "id": "Z - 4",
                                        },
                                        {
                                            "id": "Z - 5",
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        generated_zones = rpd_tests.get_zones_from_json(generated_json)
        reference_zones = rpd_tests.get_zones_from_json(self.reference_json)

        # Define a map for Zones. ! Maps for other objects will depend on this map !
        object_id_map = rpd_tests.get_mapping("Zones", generated_zones, reference_zones)
        self.assertEqual(
            object_id_map,
            {
                "Z - 1": "Zone 1",
                "Z - 2": "Zone 2",
                "Z - 3": "Zone 3",
                "Z - 4": "Zone 4",
                "Z - 5": "Zone 5",
            },
        )

    def test_failed_zone_mapping_1(self):
        generated_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "1 - 1 - 1",
                                        },
                                        {
                                            "id": "1 - 2 - 1",
                                        },
                                        {
                                            "id": "1 - 3 - 1",
                                        },
                                        {
                                            "id": "1 - 4 - 1",
                                        },
                                        {
                                            "id": "1 - 5 - 1",
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        object_id_map, map_warnings, map_errors = rpd_tests.map_objects(
            generated_json, self.reference_json
        )
        self.assertEqual(
            [
                "Could not match zones between the generated and reference files. Try to better align your modeled zone names with the correct answer file's zone naming conventions.\n- Zone 1\n- Zone 2\n- Zone 3\n- Zone 4\n- Zone 5"
            ],
            map_errors,
        )
        self.assertEqual({}, object_id_map)

    def test_surface_mapping_mismatched_interior_walls(self):
        generated_json = {
            "id": "Test RPD",
            "ruleset_model_descriptions": [
                {
                    "id": "Test RMD",
                    "buildings": [
                        {
                            "id": "Default Building",
                            "building_segments": [
                                {
                                    "id": "Default Building Segment",
                                    "zones": [
                                        {
                                            "id": "Gen Zone 1",
                                            "surfaces": [
                                                {
                                                    "id": "Gen Zone 1 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 1 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 1 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 1 Interior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 5",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Gen Zone 2",
                                            "surfaces": [
                                                {
                                                    "id": "Gen Zone 2 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 2 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 2 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 2 Interior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 5",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Gen Zone 3",
                                            "surfaces": [
                                                {
                                                    "id": "Gen Zone 3 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 3 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 3 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 3 Interior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 5",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                            ],
                                        },
                                        {
                                            "id": "Gen Zone 4",
                                            "surfaces": [
                                                {
                                                    "id": "Gen Zone 4 Exterior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 180,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 4 Exterior Wall 2",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 270,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                                {
                                                    "id": "Gen Zone 4 Exterior Wall 3",
                                                    "classification": "WALL",
                                                    "adjacent_to": "EXTERIOR",
                                                    "azimuth": 0,
                                                    "tilt": 90,
                                                    "area": 50,
                                                },
                                                {
                                                    "id": "Gen Zone 4 Interior Wall 1",
                                                    "classification": "WALL",
                                                    "adjacent_to": "INTERIOR",
                                                    "adjacent_zone": "Zone 5",
                                                    "azimuth": 90,
                                                    "tilt": 90,
                                                    "area": 100,
                                                },
                                            ],
                                        },
                                        {"id": "Gen Zone 5", "surfaces": []},
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        warnings = []
        errors = []

        generated_zones = rpd_tests.get_zones_from_json(generated_json)
        reference_zones = rpd_tests.get_zones_from_json(self.reference_json)

        object_id_map = rpd_tests.get_mapping("Zones", generated_zones, reference_zones)

        if len(object_id_map) != len(reference_zones):
            errors.append(
                f"""Could not match zones between the generated and reference files. Try to better align your modeled zone names with the correct answer file's zone naming conventions.\n{chr(10).join(f"- {zone['id']}" for zone in reference_zones)}"""
            )  # chr(10) is a newline character
            # Return early if zones could not be matched
            return object_id_map, warnings, errors

        reference_zone_ids = [zone["id"] for zone in reference_zones]

        for i, generated_zone in enumerate(generated_zones):
            generated_zone_id = generated_zone["id"]
            reference_zone_id = object_id_map[generated_zone_id]
            reference_zone = reference_zones[
                reference_zone_ids.index(reference_zone_id)
            ]

            surface_map = rpd_tests.define_surface_map(
                generated_zone, reference_zone, generated_json, self.reference_json
            )
            object_id_map.update(surface_map)

        self.assertEqual(
            {
                "Gen Zone 1": "Zone 1",
                "Gen Zone 1 Exterior Wall 1": "Zone 1 Exterior Wall 1",
                "Gen Zone 1 Exterior Wall 2": "Zone 1 Exterior Wall 2",
                "Gen Zone 1 Exterior Wall 3": "Zone 1 Exterior Wall 3",
                "Gen Zone 1 Interior Wall 1": "Zone 5 Interior Wall 1",
                "Gen Zone 2": "Zone 2",
                "Gen Zone 2 Exterior Wall 1": "Zone 2 Exterior Wall 1",
                "Gen Zone 2 Exterior Wall 2": "Zone 2 Exterior Wall 2",
                "Gen Zone 2 Exterior Wall 3": "Zone 2 Exterior Wall 3",
                "Gen Zone 2 Interior Wall 1": "Zone 5 Interior Wall 2",
                "Gen Zone 3": "Zone 3",
                "Gen Zone 3 Exterior Wall 1": "Zone 3 Exterior Wall 1",
                "Gen Zone 3 Exterior Wall 2": "Zone 3 Exterior Wall 2",
                "Gen Zone 3 Exterior Wall 3": "Zone 3 Exterior Wall 3",
                "Gen Zone 3 Interior Wall 1": "Zone 5 Interior Wall 3",
                "Gen Zone 4": "Zone 4",
                "Gen Zone 4 Exterior Wall 1": "Zone 4 Exterior Wall 1",
                "Gen Zone 4 Exterior Wall 2": "Zone 4 Exterior Wall 2",
                "Gen Zone 4 Exterior Wall 3": "Zone 4 Exterior Wall 3",
                "Gen Zone 4 Interior Wall 1": "Zone 5 Interior Wall 4",
                "Gen Zone 5": "Zone 5",
            },
            object_id_map,
        )

    def test_map_e1_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-1.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "E-1", "229 Test Case E-1 (PSZHP).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Perimeter Zone 1 (South)": "Prm Zone 1 (South)",
                "Perimeter Zone 2 (East)": "Prm Zone 2 (East)",
                "Perimeter Zone 3 (North)": "Prm Zone 3 (North)",
                "Perimeter Zone 4 (West)": "Prm Zone 4 (West)",
                "Core Zone 1 (Core)": "Core Zone 1",
                "Baseline System 4 (South)": "RPD_Test_System_4_PSZ_HP Prm Zone 1 (South)",
                "Baseline System 4 (East)": "RPD_Test_System_4_PSZ_HP Prm Zone 2 (East)",
                "Baseline System 4 (North)": "RPD_Test_System_4_PSZ_HP Prm Zone 3 (North)",
                "Baseline System 4 (West)": "RPD_Test_System_4_PSZ_HP Prm Zone 4 (West)",
                "Baseline System 4 (Core)": "RPD_Test_System_4_PSZ_HP Core Zone 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Zone 1 (South) MainTerminal": "RPD_Test_System_4_PSZ_HP - Terminal for Prm Zone 1 (South)",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Zone 2 (East) MainTerminal": "RPD_Test_System_4_PSZ_HP - Terminal for Prm Zone 2 (East)",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 3 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Zone 3 (North) MainTerminal": "RPD_Test_System_4_PSZ_HP - Terminal for Prm Zone 3 (North)",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Zone 4 (West) MainTerminal": "RPD_Test_System_4_PSZ_HP - Terminal for Prm Zone 4 (West)",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Zone 1 (Core) MainTerminal": "RPD_Test_System_4_PSZ_HP - Terminal for Core Zone 1",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_e2_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "E-2", "229 Test Case E-2 (CHW VAV).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Baseline System 7 (CHW VAV)": "RPD_Test_System_7_VAV_HW_Reheat",
                "Boiler 1": "Boiler 1",
                "Boiler 2": "Boiler 2",
                "CHW Pump (Primary)": "Primary CHW Pump 1",
                "CHW Pump (Primary) 1": "Primary CHW Pump 2",
                "CHW Pump (Secondary)": "Secondary CHW Pump",
                "Chilled Water Loop (Primary)": "Primary CHW Loop",
                "Chilled Water Loop (Secondary)": "Secondary CHW Loop",
                "Chiller 1": "Chiller 1",
                "Chiller 2": "Chiller 2",
                "Condenser Water Loop": "CW Loop",
                "Condenser Water Pump": "CW Pump",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone": "Core Zone 1",
                "Core Zone MainTerminal": "RPD_Test_System_7_VAV_HW_Reheat - Terminal for "
                "Core Zone 1",
                "Heat Rejection 1": "Cooling Tower 1",
                "Hot Water Loop": "Boiler Loop 1",
                "Hot Water Pumps": "HW Pump 1",
                "Hot Water Pumps 1": "HW Pump 2",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 N Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 W Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 S Wall": "Core Zone 1 North Wall",
                "Perimeter Space 3 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 E Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Perimeter Zone 1 (South)": "Prm Zone 1 (South)",
                "Perimeter Zone 1 (South) MainTerminal": "RPD_Test_System_7_VAV_HW_Reheat - "
                "Terminal for Prm Zone 1 (South)",
                "Perimeter Zone 2 (East)": "Prm Zone 2 (East)",
                "Perimeter Zone 2 (East) MainTerminal": "RPD_Test_System_7_VAV_HW_Reheat - "
                "Terminal for Prm Zone 2 (East)",
                "Perimeter Zone 3 (North)": "Prm Zone 3 (North)",
                "Perimeter Zone 3 (North) MainTerminal": "RPD_Test_System_7_VAV_HW_Reheat - "
                "Terminal for Prm Zone 3 (North)",
                "Perimeter Zone 4 (West)": "Prm Zone 4 (West)",
                "Perimeter Zone 4 (West) MainTerminal": "RPD_Test_System_7_VAV_HW_Reheat - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_e3_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-3.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "E-3", "229 Test Case E-3 (Pkgd VAV Bbrd).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 BaseboardTerminal": "Baseboard - Terminal for Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard - "
                "Terminal for Core Zone 1",
                "Hot Water Loop": "Primary HW Loop",
                "Hot Water Pumps": "HW Pump 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Pkgd VAV": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn BaseboardTerminal": "Baseboard - Terminal for Prm Zone "
                "1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard "
                "- Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn BaseboardTerminal": "Baseboard - Terminal for Prm Zone "
                "2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard "
                "- Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) BaseboardTerminal": "Baseboard - Terminal for Prm Zone 3 "
                "(North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard "
                "- Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) BaseboardTerminal": "Baseboard - Terminal for Prm Zone 4 "
                "(West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_P_PVAV_HW_Reheat_Baseboard "
                "- Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f100_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-100.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-100", "229 Test Case F-100 (PTAC).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_1_PTAC - Terminal for Core Zone "
                "1",
                "Hot Water Loop": "Boiler Loop 1",
                "Hot Water Pumps": "HW Pump 1",
                "PTAC 1": "RPD_Test_System_1_PTAC Core Zone 1",
                "PTAC 2": "RPD_Test_System_1_PTAC Prm Zone 1 (South)",
                "PTAC 3": "RPD_Test_System_1_PTAC Prm Zone 2 (East)",
                "PTAC 4": "RPD_Test_System_1_PTAC Prm Zone 3 (North)",
                "PTAC 5": "RPD_Test_System_1_PTAC Prm Zone 4 (West)",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_1_PTAC - Terminal for "
                "Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_1_PTAC - Terminal for "
                "Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_1_PTAC - Terminal for Prm "
                "Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_1_PTAC - Terminal for Prm "
                "Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f110_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-110.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-110", "229 Test Case F-110 (PTHP).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_2_PTHP - Terminal for Core Zone "
                "1",
                "PTHP 1": "RPD_Test_System_2_PTHP Core Zone 1",
                "PTHP 2": "RPD_Test_System_2_PTHP Prm Zone 1 (South)",
                "PTHP 3": "RPD_Test_System_2_PTHP Prm Zone 2 (East)",
                "PTHP 4": "RPD_Test_System_2_PTHP Prm Zone 3 (North)",
                "PTHP 5": "RPD_Test_System_2_PTHP Prm Zone 4 (West)",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_2_PTHP - Terminal for "
                "Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_2_PTHP - Terminal for "
                "Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_2_PTHP - Terminal for Prm "
                "Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_2_PTHP - Terminal for Prm "
                "Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f120_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-120.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-120", "229 Test Case F-120 (PSZ).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_3_PSZ_AC_Gas_Furnace - Terminal "
                "for Core Zone 1",
                "PSZ 1": "RPD_Test_System_3_PSZ_AC_Gas_Furnace Core Zone 1",
                "PSZ 2": "RPD_Test_System_3_PSZ_AC_Gas_Furnace Prm Zone 1 (South)",
                "PSZ 3": "RPD_Test_System_3_PSZ_AC_Gas_Furnace Prm Zone 2 (East)",
                "PSZ 4": "RPD_Test_System_3_PSZ_AC_Gas_Furnace Prm Zone 3 (North)",
                "PSZ 5": "RPD_Test_System_3_PSZ_AC_Gas_Furnace Prm Zone 4 (West)",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_3_PSZ_AC_Gas_Furnace - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_3_PSZ_AC_Gas_Furnace - "
                "Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_3_PSZ_AC_Gas_Furnace - "
                "Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_3_PSZ_AC_Gas_Furnace - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f130_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-130.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-130", "229 Test Case F-130 (PVAV).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_5_PVAV_HW_Reheat - Terminal for "
                "Core Zone 1",
                "HW Loop": "Boiler Loop 1",
                "HW Pump": "HW Pump 1",
                "PVAV": "RPD_Test_System_5_PVAV_HW_Reheat",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_5_PVAV_HW_Reheat - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_5_PVAV_HW_Reheat - "
                "Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_5_PVAV_HW_Reheat - "
                "Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_5_PVAV_HW_Reheat - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f140_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-140.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-140", "229 Test Case F-140 (PVAV PFP).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_6_PVAV_Elec_Reheat - Terminal "
                "for Core Zone 1",
                "PVAV PFP": "RPD_Test_System_6_PVAV_Elec_Reheat",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_6_PVAV_Elec_Reheat - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_6_PVAV_Elec_Reheat - "
                "Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_6_PVAV_Elec_Reheat - "
                "Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_6_PVAV_Elec_Reheat - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f150_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-150.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-150", "229 Test Case F-150 (VAV PFP).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "CHW Loop": "CHW Loop 1",
                "CHW-PUMP": "Chiller Pump 1",
                "Chiller 1": "Chiller 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_8_PFP_Reheat - Terminal for Core "
                "Zone 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_8_PFP_Reheat - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_8_PFP_Reheat - Terminal "
                "for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_8_PFP_Reheat - Terminal "
                "for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_8_PFP_Reheat - Terminal "
                "for Prm Zone 4 (West)",
                "VAV PFP": "RPD_Test_System_8_PFP_Reheat",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f160_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-160.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-160", "229 Test Case F-160 (UHT).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_9_Warm_Air_Furnace_Gas - "
                "Terminal for Core Zone 1",
                "Gas Unit Heaters": "RPD_Test_System_9_Warm_Air_Furnace_Gas Core Zone 1",
                "Gas Unit Heaters - Prm Zone 1 (South) Zn": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "Prm Zone 1 (South)",
                "Gas Unit Heaters - Prm Zone 2 (East) Zn": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "Prm Zone 2 (East)",
                "Gas Unit Heaters - Prm Zone 3 (North)": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "Prm Zone 3 (North)",
                "Gas Unit Heaters - Prm Zone 4 (West)": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "Prm Zone 4 (West)",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "- Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_9_Warm_Air_Furnace_Gas "
                "- Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_9_Warm_Air_Furnace_Gas - "
                "Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_9_Warm_Air_Furnace_Gas - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f170_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-170.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-170", "229 Test Case F-170 (UHT).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_10_Warm_air_Furnace_Elec - "
                "Terminal for Core Zone 1",
                "Elec Unit Heaters": "RPD_Test_System_10_Warm_air_Furnace_Elec Core Zone 1",
                "Elec Unit Heaters - Prm Zone 1 (South) Zn": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "Prm Zone 1 (South)",
                "Elec Unit Heaters - Prm Zone 2 (East) Zn": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "Prm Zone 2 (East)",
                "Elec Unit Heaters - Prm Zone 3 (North)": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "Prm Zone 3 (North)",
                "Elec Unit Heaters - Prm Zone 4 (West)": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "Prm Zone 4 (West)",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "- Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "- Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_10_Warm_air_Furnace_Elec "
                "- Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_10_Warm_air_Furnace_Elec - "
                "Terminal for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f180_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-180.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-180", "229 Test Case F-180 (SZ VAV).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "CHW Pump (Primary)": "CHW Pump 1",
                "Chilled Water Loop (Primary)": "CHW Loop 1",
                "Chiller 1": "Chiller 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone": "Core Zone 1",
                "Core Zone MainTerminal": "RPD_Test_System_11.1_VAV_SZ - Terminal for Core "
                "Zone 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 N Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 W Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 S Wall": "Core Zone 1 North Wall",
                "Perimeter Space 3 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 E Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Perimeter Zone 1 (South)": "Prm Zone 1 (South)",
                "Perimeter Zone 1 (South) MainTerminal": "RPD_Test_System_11.1_VAV_SZ - "
                "Terminal for Prm Zone 1 (South)",
                "Perimeter Zone 2 (East)": "Prm Zone 2 (East)",
                "Perimeter Zone 2 (East) MainTerminal": "RPD_Test_System_11.1_VAV_SZ - "
                "Terminal for Prm Zone 2 (East)",
                "Perimeter Zone 3 (North)": "Prm Zone 3 (North)",
                "Perimeter Zone 3 (North) MainTerminal": "RPD_Test_System_11.1_VAV_SZ - "
                "Terminal for Prm Zone 3 (North)",
                "Perimeter Zone 4 (West)": "Prm Zone 4 (West)",
                "Perimeter Zone 4 (West) MainTerminal": "RPD_Test_System_11.1_VAV_SZ - "
                "Terminal for Prm Zone 4 (West)",
                "SZ VAV 1": "RPD_Test_System_11.1_VAV_SZ Prm Zone 1 (South)",
                "SZ VAV 2": "RPD_Test_System_11.1_VAV_SZ Prm Zone 2 (East)",
                "SZ VAV 3": "RPD_Test_System_11.1_VAV_SZ Prm Zone 3 (North)",
                "SZ VAV 4": "RPD_Test_System_11.1_VAV_SZ Prm Zone 4 (West)",
                "SZ VAV 5": "RPD_Test_System_11.1_VAV_SZ Core Zone 1",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f190_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-190.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-190", "229 Test Case F-190 (SZ CV).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "CHW Pump (Primary)": "Chiller Pump 1",
                "CW Pump 1": "Condenser Pump 1",
                "Chilled Water Loop (Primary)": "CHW Loop 1",
                "Chiller 1": "Chiller 1",
                "Condenser Water Loop": "CW Loop 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone": "Core Zone 1",
                "Core Zone MainTerminal": "RPD_Test_System 12_CAV_SZ_HW - Terminal for Core "
                "Zone 1",
                "DEFAULT-HW-PUMP": "Boiler Pump 1",
                "Heat Rejection 1": "Cooling Tower 1",
                "Hot Water Loop": "HW Loop 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 N Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 W Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 S Wall": "Core Zone 1 North Wall",
                "Perimeter Space 3 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 E Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Perimeter Zone 1 (South)": "Prm Zone 1 (South)",
                "Perimeter Zone 1 (South) MainTerminal": "RPD_Test_System 12_CAV_SZ_HW - "
                "Terminal for Prm Zone 1 (South)",
                "Perimeter Zone 2 (East)": "Prm Zone 2 (East)",
                "Perimeter Zone 2 (East) MainTerminal": "RPD_Test_System 12_CAV_SZ_HW - "
                "Terminal for Prm Zone 2 (East)",
                "Perimeter Zone 3 (North)": "Prm Zone 3 (North)",
                "Perimeter Zone 3 (North) MainTerminal": "RPD_Test_System 12_CAV_SZ_HW - "
                "Terminal for Prm Zone 3 (North)",
                "Perimeter Zone 4 (West)": "Prm Zone 4 (West)",
                "Perimeter Zone 4 (West) MainTerminal": "RPD_Test_System 12_CAV_SZ_HW - "
                "Terminal for Prm Zone 4 (West)",
                "SZ CV 1": "RPD_Test_System 12_CAV_SZ_HW Prm Zone 1 (South)",
                "SZ CV 2": "RPD_Test_System 12_CAV_SZ_HW Prm Zone 2 (East)",
                "SZ CV 3": "RPD_Test_System 12_CAV_SZ_HW Prm Zone 3 (North)",
                "SZ CV 4": "RPD_Test_System 12_CAV_SZ_HW Prm Zone 4 (West)",
                "SZ CV 5": "RPD_Test_System 12_CAV_SZ_HW Core Zone 1",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f200_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-200.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-200", "229 Test Case F-200 (SZ CV ER).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "CHW Pump (Primary)": "Chiller Pump 1",
                "Chilled Water Loop (Primary)": "CHW Loop 1",
                "Chiller 1": "Chiller 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone": "Core Zone 1",
                "Core Zone MainTerminal": "RPD_Test_System 13_CAV_SZ_ER - Terminal for Core "
                "Zone 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 N Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 W Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 S Wall": "Core Zone 1 North Wall",
                "Perimeter Space 3 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 E Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Perimeter Zone 1 (South)": "Prm Zone 1 (South)",
                "Perimeter Zone 1 (South) MainTerminal": "RPD_Test_System 13_CAV_SZ_ER - "
                "Terminal for Prm Zone 1 (South)",
                "Perimeter Zone 2 (East)": "Prm Zone 2 (East)",
                "Perimeter Zone 2 (East) MainTerminal": "RPD_Test_System 13_CAV_SZ_ER - "
                "Terminal for Prm Zone 2 (East)",
                "Perimeter Zone 3 (North)": "Prm Zone 3 (North)",
                "Perimeter Zone 3 (North) MainTerminal": "RPD_Test_System 13_CAV_SZ_ER - "
                "Terminal for Prm Zone 3 (North)",
                "Perimeter Zone 4 (West)": "Prm Zone 4 (West)",
                "Perimeter Zone 4 (West) MainTerminal": "RPD_Test_System 13_CAV_SZ_ER - "
                "Terminal for Prm Zone 4 (West)",
                "SZ CV 1": "RPD_Test_System 13_CAV_SZ_ER Prm Zone 1 (South)",
                "SZ CV 2": "RPD_Test_System 13_CAV_SZ_ER Prm Zone 2 (East)",
                "SZ CV 3": "RPD_Test_System 13_CAV_SZ_ER Prm Zone 3 (North)",
                "SZ CV 4": "RPD_Test_System 13_CAV_SZ_ER Prm Zone 4 (West)",
                "SZ CV 5": "RPD_Test_System 13_CAV_SZ_ER Core Zone 1",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f210_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-210.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-210", "229 Test Case F-210 (FC).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "CHW-PUMP": "Chiller Pump 1",
                "Chilled Water Loop (Primary)": "CHW Loop 1",
                "Chiller 1": "Chiller 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_P_FCU - Terminal for Core Zone 1",
                "Fan Coil Units": "RPD_Test_System_P_FCU Core Zone 1",
                "Fan Coil Units - Prm Zone 1 (South) Zn": "RPD_Test_System_P_FCU Prm Zone 1 "
                "(South)",
                "Fan Coil Units - Prm Zone 2 (East) Zn": "RPD_Test_System_P_FCU Prm Zone 2 "
                "(East)",
                "Fan Coil Units - Prm Zone 3 (North)": "RPD_Test_System_P_FCU Prm Zone 3 "
                "(North)",
                "Fan Coil Units - Prm Zone 4 (West)": "RPD_Test_System_P_FCU Prm Zone 4 "
                "(West)",
                "Hot Water Loop": "HHW Loop 1",
                "Hot Water Pumps": "HW Pump 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_P_FCU - Terminal for "
                "Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_P_FCU - Terminal for "
                "Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_P_FCU - Terminal for Prm "
                "Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_P_FCU - Terminal for Prm "
                "Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f220_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-220.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-220", "229 Test Case F-220 (FC Purch).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "CHW-PUMP": "Chiller Pump 1",
                "Chilled Water Loop (Primary)": "CHW Loop 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_P_FCU_purchased - Terminal for "
                "Core Zone 1",
                "Fan Coil Units": "RPD_Test_System_P_FCU_purchased Core Zone 1",
                "Fan Coil Units - Prm Zone 1 (South) Zn": "RPD_Test_System_P_FCU_purchased "
                "Prm Zone 1 (South)",
                "Fan Coil Units - Prm Zone 2 (East) Zn": "RPD_Test_System_P_FCU_purchased Prm "
                "Zone 2 (East)",
                "Fan Coil Units - Prm Zone 3 (North)": "RPD_Test_System_P_FCU_purchased Prm "
                "Zone 3 (North)",
                "Fan Coil Units - Prm Zone 4 (West)": "RPD_Test_System_P_FCU_purchased Prm "
                "Zone 4 (West)",
                "Hot Water Loop": "HHW Loop 1",
                "Hot Water Pumps": "HW Pump 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_P_FCU_purchased - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_P_FCU_purchased - "
                "Terminal for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_P_FCU_purchased - "
                "Terminal for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_P_FCU_purchased - Terminal "
                "for Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f230_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-230.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-230", "229 Test Case F-230 (WSHP).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "CW-PUMP": "Condenser Pump 1",
                "Condenser Water Loop": "CW Loop 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_P_WSHP - Terminal for Core Zone "
                "1",
                "Heat Rejection 1": "Cooling Tower 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_P_WSHP - Terminal for "
                "Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_P_WSHP - Terminal for "
                "Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_P_WSHP - Terminal for Prm "
                "Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_P_WSHP - Terminal for Prm "
                "Zone 4 (West)",
                "WSHP Units": "RPD_Test_System_P_WSHP Core Zone 1",
                "WSHP Units - Prm Zone 1 (South) Zn": "RPD_Test_System_P_WSHP Prm Zone 1 "
                "(South)",
                "WSHP Units - Prm Zone 2 (East) Zn": "RPD_Test_System_P_WSHP Prm Zone 2 "
                "(East)",
                "WSHP Units - Prm Zone 3 (North)": "RPD_Test_System_P_WSHP Prm Zone 3 (North)",
                "WSHP Units - Prm Zone 4 (West)": "RPD_Test_System_P_WSHP Prm Zone 4 (West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_map_f240_objects(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "F-240.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        generated_json_path = os.path.join(
            current_dir, "F-240", "229 Test Case F-240 (WSHP DOAS).json"
        )
        with open(generated_json_path, "r") as f:
            generated_json = json.load(f)

        object_id_map, warnings, errors = rpd_tests.map_objects(
            generated_json, reference_json
        )
        self.assertEqual(
            {
                "Boiler 1": "Boiler 1",
                "CW-PUMP": "Condenser Pump 1",
                "Condenser Water Loop": "CW Loop 1",
                "Core Space 1 Roof": "Core Zone 1 Roof",
                "Core Space 1 Slab on Grade": "Core Zone 1 Floor",
                "Core Zone 1": "Core Zone 1",
                "Core Zone 1 DOASTerminal": "RPD_Test_System_P_WSHP_DOAS - Terminal for Core "
                "Zone 1",
                "Core Zone 1 MainTerminal": "RPD_Test_System_P_WSHP_no_OA - Terminal for Core "
                "Zone 1",
                "DOAS 1": "RPD_Test_System_P_WSHP_DOAS",
                "Heat Rejection 1": "Cooling Tower 1",
                "Perimeter Space 1 Ext Wall": "Prm Zone 1 South Wall",
                "Perimeter Space 1 NE Wall": "Prm Zone 1 East Wall",
                "Perimeter Space 1 NW Wall": "Prm Zone 4 South Wall",
                "Perimeter Space 1 North Wall": "Core Zone 1 South Wall",
                "Perimeter Space 1 Roof": "Prm Zone 1 Roof",
                "Perimeter Space 1 Slab on Grade": "Prm Zone 1 Floor",
                "Perimeter Space 2 Ext Wall": "Prm Zone 2 East Wall",
                "Perimeter Space 2 NW Wall": "Prm Zone 2 North Wall",
                "Perimeter Space 2 Roof": "Prm Zone 2 Roof",
                "Perimeter Space 2 SW Wall": "Prm Zone 3 West Wall",
                "Perimeter Space 2 Slab on Grade": "Prm Zone 2 Floor",
                "Perimeter Space 2 South Wall": "Core Zone 1 North Wall",
                "Perimeter Space 2 West Wall": "Core Zone 1 East Wall",
                "Perimeter Space 3 Ext Wall": "Prm Zone 3 North Wall",
                "Perimeter Space 3 Roof": "Prm Zone 3 Roof",
                "Perimeter Space 3 Slab on Grade": "Prm Zone 3 Floor",
                "Perimeter Space 4 East Wall": "Core Zone 1 West Wall",
                "Perimeter Space 4 Ext Wall": "Prm Zone 4 West Wall",
                "Perimeter Space 4 Roof": "Prm Zone 4 Roof",
                "Perimeter Space 4 Slab on Grade": "Prm Zone 4 Floor",
                "Prm Zone 1 (South) Zn": "Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn DOASTerminal": "RPD_Test_System_P_WSHP_DOAS - Terminal "
                "for Prm Zone 1 (South)",
                "Prm Zone 1 (South) Zn MainTerminal": "RPD_Test_System_P_WSHP_no_OA - "
                "Terminal for Prm Zone 1 (South)",
                "Prm Zone 2 (East) Zn": "Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn DOASTerminal": "RPD_Test_System_P_WSHP_DOAS - Terminal "
                "for Prm Zone 2 (East)",
                "Prm Zone 2 (East) Zn MainTerminal": "RPD_Test_System_P_WSHP_no_OA - Terminal "
                "for Prm Zone 2 (East)",
                "Prm Zone 3 (North)": "Prm Zone 3 (North)",
                "Prm Zone 3 (North) DOASTerminal": "RPD_Test_System_P_WSHP_DOAS - Terminal "
                "for Prm Zone 3 (North)",
                "Prm Zone 3 (North) MainTerminal": "RPD_Test_System_P_WSHP_no_OA - Terminal "
                "for Prm Zone 3 (North)",
                "Prm Zone 4 (West)": "Prm Zone 4 (West)",
                "Prm Zone 4 (West) DOASTerminal": "RPD_Test_System_P_WSHP_DOAS - Terminal for "
                "Prm Zone 4 (West)",
                "Prm Zone 4 (West) MainTerminal": "RPD_Test_System_P_WSHP_no_OA - Terminal "
                "for Prm Zone 4 (West)",
                "WSHP Units": "RPD_Test_System_P_WSHP_no_OA Core Zone 1",
                "WSHP Units - Prm Zone 1 (South) Zn": "RPD_Test_System_P_WSHP_no_OA Prm Zone "
                "1 (South)",
                "WSHP Units - Prm Zone 2 (East) Zn": "RPD_Test_System_P_WSHP_no_OA Prm Zone 2 "
                "(East)",
                "WSHP Units - Prm Zone 3 (North)": "RPD_Test_System_P_WSHP_no_OA Prm Zone 3 "
                "(North)",
                "WSHP Units - Prm Zone 4 (West)": "RPD_Test_System_P_WSHP_no_OA Prm Zone 4 "
                "(West)",
            },
            object_id_map,
        )
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [])

    def test_find_all_simple(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        json_path = (
            "$.ruleset_model_descriptions[*].buildings[*].building_segments[*].zones[*]"
        )
        result = rpd_tests.find_all(json_path, reference_json)
        self.assertEqual(len(result), 5)

    def test_find_all_end_filter(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        json_path = '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*][?(@.adjacent_to = "EXTERIOR")]'
        result = rpd_tests.find_all(json_path, reference_json)
        self.assertEqual(9, len(result))

    def test_find_all_mid_filter(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        json_path = '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*][?(@.adjacent_to = "EXTERIOR")].optical_properties.absorptance_thermal_exterior'
        result = rpd_tests.find_all(json_path, reference_json)
        self.assertEqual(9, len(result))

    def test_find_all_combo_filter(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        json_path = '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*][?(@.adjacent_to = "EXTERIOR" and @.id = "Prm Zone 1 South Wall")].optical_properties.absorptance_thermal_exterior'
        result = rpd_tests.find_all(json_path, reference_json)
        self.assertEqual(1, len(result))

    def test_find_all_multi_filter(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        correct_answer_e1_path = os.path.join(
            current_dir, "Correct Answer RPDs", "E-2.json"
        )
        with open(correct_answer_e1_path, "r") as f:
            reference_json = json.load(f)

        json_path = '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*][?(@.id = "Prm Zone 1 (South)")].surfaces[*][?(@.adjacent_to = "EXTERIOR")].optical_properties.absorptance_thermal_exterior'
        result = rpd_tests.find_all(json_path, reference_json)
        self.assertEqual(2, len(result))
