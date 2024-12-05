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
