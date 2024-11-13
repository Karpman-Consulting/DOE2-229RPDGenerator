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

    def read_input_bdl_file(self, bdl_file_path: str):
        """
        Read BDL input file and return a dictionary of object instances.

        :param bdl_file_path: Path to the BDL file.
        :return: A dictionary with BDL commands as keys and lists of .
        """

        with open(bdl_file_path, "r") as bdl_file:
            doe2_version = None
            file_commands = {}

            active_command_dict = None
            record_data_for = False

            for line in bdl_file:
                if not line.strip():
                    continue

                if "JJHirsch DOE-2 Version:" in line:
                    doe2_version = line.split(":")[1].split()[0].strip()
                    continue

                if record_data_for and line[0] != "-":
                    record_data_for = False

                if '" = ' in line or "$LIBRARY-ENTRY" in line:
                    unique_name, command = (
                        self._parse_command_line(line)
                        if '" = ' in line
                        else self._parse_library_entry(line)
                    )
                    if command in self.bdl_command_dict:
                        command_dict = {"unique_name": unique_name}
                        self._track_current_parents(command, command_dict)
                        command_dict = self._set_parent(command, command_dict)
                        if command_dict not in file_commands.setdefault(command, []):
                            file_commands[command].append(command_dict)
                        active_command_dict = command_dict
                    continue

                elif "DATA FOR" in line:
                    record_data_for = True
                    obj_u_name = line.split("DATA FOR ")[1].strip()
                    if (
                        active_command_dict is None
                        or obj_u_name != active_command_dict["unique_name"]
                    ):
                        active_command_dict = next(
                            (
                                cmd_dict
                                for cmd_list in file_commands.values()
                                for cmd_dict in cmd_list
                                if cmd_dict["unique_name"] == obj_u_name
                            ),
                            None,
                        )
                    continue

                elif (
                    record_data_for
                    and " = " in line
                    and active_command_dict is not None
                ):
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
        return unique_name, command

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
            value = parts[1].strip()
            return keyword, value, units
        else:
            parts = line.split(" = ")
            keyword = re.split(r" {2,}", parts[0])[1].strip()
            value = parts[1].strip()
            return keyword, value, None

    def _track_current_parents(self, command, command_dict):
        """
        Keep track of the most recent floor, space, or other parent objects. Floor and space parents are stored
        separately to ensure that the correct parent is set for child objects in multi-tiered nodes.
        :param command:
        :param command_dict:
        :return: None
        """
        # plain parents are parents that cannot have grandchildren
        plain_parent_commands = ["SYSTEM", "EXTERIOR-WALL", "INTERIOR-WALL"]
        if command == "FLOOR":
            self.current_parent_floor = command_dict["unique_name"]
        elif command == "SPACE":
            self.current_parent_space = command_dict["unique_name"]
        elif command in plain_parent_commands:
            self.current_parent = command_dict["unique_name"]
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
