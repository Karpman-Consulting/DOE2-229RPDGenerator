import inspect
import pkgutil
import importlib
import re
from rpd_generator.bdl_structure import *


def _get_bdl_commands_for_rpd() -> dict:
    """
    Return a dictionary of BDL commands mapped to their respective class objects to facilitate instantiation.
    """
    commands_dict = {}
    prefix = bdl_commands.__name__ + "."
    # iterate through the modules in the bdl_commands package
    for _, name, _ in pkgutil.iter_modules(bdl_commands.__path__, prefix):
        module = importlib.import_module(name)
        # iterate through the classes in each module
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # if the class is a subclass of BaseNode or BaseDefinition
            if issubclass(obj, (BaseNode, BaseDefinition)):
                # get the bdl_command attribute
                bdl_command = getattr(obj, "bdl_command", None)
                # insert the bdl_command and class object into the dictionary to facilitate instantiation
                commands_dict[bdl_command] = obj
    return commands_dict


class ModelInputReader:
    """Model input reader class."""

    bdl_command_dict = None
    known_units = [
        "",
        "F",
        "F (DELTA)",
        "KNOTS",
        "FT",
        "IN",
        "DEGREES",
        "HR-SQFT-F /BTU",
        "BTU/HR-FT-F",
        "LB/CUFT",
        "BTU/LB-F",
        "BTU/HR-SQFT-F",
        "FRAC.OR MULT.",
        "SQFT",
        "CUFT",
        "CFM/SQFT",
        "BTU/HR/PERSON",
        "W/SQFT",
        "BTU/HR",
        "KW",
        "LB/SQFT",
        "CFM",
        "FOOTCANDLES",
        "LUMEN / WATT",
        "BTU/BTU",
        "BTU/UNIT",
        "LBS/KW",
        "$/UNIT",
        "GPM",
        "PERCENT",
        "GAL/MIN",
        "MBTU/HR",
        "BTU/HR-F",
        "KW/CFM",
        "IN-WATER",
        "CFM/TON",
        "HP",
        "R",
        "HOURS",
        "GALLONS/MIN/TON",
        "GAL",
        "KW/TON",
        "BTU/LB",
    ]

    def __init__(self):
        ModelInputReader.bdl_command_dict = _get_bdl_commands_for_rpd()
        self.current_parent_floor = None
        self.current_parent_space = None
        self.current_parent = None

    def read_input_bdl_file(self, bdl_file_path: str) -> dict:
        """
        Read BDL input file and return a dictionary of object instances.

        :param bdl_file_path: Path to the BDL file.
        :return: A dictionary with BDL commands as keys and dictionaries filled with keyword-value pairs as values.

        Example:
        {
            "doe2_version": "DOE-2.3",
            "file_commands": {
                "SYSTEM": {
                    "System 1": {
                        "TYPE": "FC",
                        "MIN-SUPPLY-T": 50.0,
                        "MAX-SUPPLY-T": 100.0,
                    },
                    "System 2": {
                        "TYPE": "FC",
                        "MIN-SUPPLY-T": 50.0,
                        "MAX-SUPPLY-T": 100.0,
                    },
                },
                "ZONE": {
                    "ZONE-1": {
                        "DESIGN-COOL-T": 75.0,
                        "DESIGN-HEAT-T": 70.0,
                    },
                    "ZONE-2": {
                        "DESIGN-COOL-T": 75.0,
                        "DESIGN-HEAT-T": 70.0,
                    },
                },
            }
        }
        """

        with open(bdl_file_path, "r") as bdl_file:
            doe2_version = None
            file_commands = {}

            active_command_dict = None
            record_data_for = False
            special_read_flag = False
            special_data = {}
            multiline_key = None
            multiline_value = []

            for line in bdl_file:

                # Skip empty lines
                if not line.strip():
                    record_data_for = False
                    continue

                # Extract the DOE-2 version from the file
                if "JJHirsch DOE-2 Version:" in line:
                    doe2_version = line.split(":")[1].split()[0].strip()
                    continue

                # When the data record is complete, reset the flag and add the command to the file_commands dictionary
                if record_data_for and line[0] != "-":
                    record_data_for = False

                # If the line contains a command, parse the command and set the active command dictionary
                if '" = ' in line or "$LIBRARY-ENTRY" in line:
                    unique_name, command = (
                        self._parse_command_line(line)
                        if '" = ' in line
                        else self._parse_library_entry(line)
                    )
                    # check if the command type is one that the RPD Generator uses:
                    if command in self.bdl_command_dict:

                        # check if the library entry requires special handling
                        if "CURVE-FIT" in line:
                            special_read_flag = True

                        command_dict = {"command": command}
                        self._track_current_parents(unique_name, command)
                        command_dict = self._set_parent(command, command_dict)
                        # Ensure every BDL command is accessible by unique name
                        file_commands[unique_name] = command_dict
                    continue

                # Flag the start of the data record and set the active command dictionary
                elif "DATA FOR" in line:
                    obj_u_name = line[32:].rstrip()
                    active_command_dict = file_commands.get(obj_u_name)
                    if active_command_dict:
                        record_data_for = True
                    continue

                # Parse the definition line and add the keyword and value to the active command dictionary
                elif record_data_for and " = " in line:
                    keyword, value, units = self._parse_definition_line(line)

                    if keyword in active_command_dict and isinstance(
                        active_command_dict[keyword], list
                    ):
                        active_command_dict[keyword].append(value)

                    elif keyword in active_command_dict:
                        active_command_dict[keyword] = [
                            active_command_dict[keyword],
                            value,
                        ]

                    else:
                        active_command_dict[keyword] = value

                elif special_read_flag:
                    active_command_dict = file_commands.get(unique_name)

                    # Parse keyword-value pairs
                    keywords_values = re.split(r"\s+(?![^(]*\))|=", line[15:])
                    if any("(" in item for item in keywords_values):
                        # Combine all parts starting from the "("
                        paren_idx = next(
                            i for i, item in enumerate(keywords_values) if "(" in item
                        )
                        keywords_values = keywords_values[:paren_idx] + [
                            " ".join(keywords_values[paren_idx:])
                        ]

                    # filter out empty strings and ".."
                    keywords_values = [
                        item for item in keywords_values if item and item != ".."
                    ]

                    if multiline_key:
                        keywords_values.insert(0, multiline_key)
                        multiline_value += line[15:].split(")")[0] + ")"
                        keywords_values[1] = multiline_value
                        multiline_key = None

                    for i in range(0, len(keywords_values), 2):
                        key = keywords_values[i]
                        value = keywords_values[i + 1]
                        if "(" in value:
                            special_data[key] = self._parse_parentheses_values(value)
                        else:
                            special_data[key] = value

                    if "(" in line and ")" not in line:
                        multiline_key = keywords_values[-2]
                        multiline_value = keywords_values[-1]

                    # End special read block at `..`
                    if ".." in line:
                        special_read_flag = False
                        if active_command_dict and "COEF" in special_data:
                            active_command_dict["COEF"] = special_data["COEF"]
                        special_data = {}

            file_commands = self._group_by_command(file_commands)
            return {"doe2_version": doe2_version, "file_commands": file_commands}

    @staticmethod
    def _parse_command_line(line):
        """
        Parse the line to extract unique name and command.

        :param line: Line to be parsed.
        :return: tuple: Unique name and command extracted from the line.
        """
        parts = line.split('" = ')
        unique_name = parts[0].strip().split('"')[1]
        command = parts[1].strip()
        return unique_name, command

    @staticmethod
    def _parse_library_entry(line):
        """
        Parse the line to extract unique name and command.

        :param line: Line to be parsed.
        :return: tuple: Unique name and command extracted from the line.
        """
        unique_name = line[28:60].strip()
        command = line[60:76].strip()
        command = command.replace("MAT", "MATERIAL")
        return unique_name, command

    @staticmethod
    def _parse_parentheses_values(text):
        """
        Extract values enclosed in parentheses.
        """
        match = re.search(r"\((.*?)\)", text)
        if match:
            return [v.strip() for v in match.group(1).split(",")]
        return []

    @staticmethod
    def _group_by_command(commands_dict):
        grouped_dict = {}
        for key, val in commands_dict.items():
            command = val["command"]
            if command not in grouped_dict:
                grouped_dict[command] = {}
            grouped_dict[command][key] = val
        return grouped_dict

    def _parse_definition_line(self, line):
        """
        Parse the line to extract keyword and value.

        :param line: Line to be parsed.
        :return: tuple: Keyword and value extracted from the line.
        """
        potential_units = line[104:].strip()
        has_expected_whitespace = line[75:80] == "     " and (
            len(line) < 105 or line[103] == " "
        )
        if potential_units in self.known_units and has_expected_whitespace:
            parts, units = line[:104].split(" = "), line[104:].strip()
            keyword = re.split(r" {2,}", parts[0])[1].strip()
            value = parts[1].rstrip()
            return keyword, value, units
        else:
            parts = line.split(" = ")
            keyword = re.split(r" {2,}", parts[0])[1].strip()
            value = parts[1].rstrip()
            return keyword, value, None

    def _track_current_parents(self, u_name, command):
        """
        Keep track of the most recent floor, space, or other parent objects. Floor and space parents are stored
        separately to ensure that the correct parent is set for child objects in multi-tiered nodes.
        :param u_name: Unique name of the object.
        :param command: Command type of the object.
        :return: None
        """
        # plain parents are parents that cannot have grandchildren
        plain_parent_commands = ["SYSTEM", "EXTERIOR-WALL", "INTERIOR-WALL"]
        if command == "FLOOR":
            self.current_parent_floor = u_name
        elif command == "SPACE":
            self.current_parent_space = u_name
        elif command in plain_parent_commands:
            self.current_parent = u_name
        return

    def _set_parent(self, command, command_dict):
        """
        Set the parent of the object based on the command type.
        :param command:
        :param command_dict:
        :return: command_dict
        """
        if command in ["EXTERIOR-WALL", "INTERIOR-WALL", "UNDERGROUND-WALL"]:
            command_dict["parent"] = self.current_parent_space
        elif command == "SPACE":
            command_dict["parent"] = self.current_parent_floor
        elif command in ["ZONE", "WINDOW", "DOOR"]:
            command_dict["parent"] = self.current_parent
        return command_dict
