import os
import pint
from itertools import islice
from pathlib import Path


from rpd_generator.doe2_file_readers.model_output_reader import (
    get_string_result,
    get_multiple_results,
)
from rpd_generator.config import Config


path_to_ureg = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "utilities",
    "resources",
    "unit_registry.txt",
)
ureg = pint.UnitRegistry(path_to_ureg, autoconvert_offset_to_baseunit=True)


class Base:

    def populate_data_group_with_prefix(self, prefix):
        attributes = [attr for attr in dir(self) if attr.startswith(prefix)]
        keys = [attr.replace(prefix, "") for attr in attributes]

        value_lists = []
        for attr in attributes:
            value = getattr(self, attr)
            if isinstance(value, list):
                value_lists.append(value)
            else:
                value_lists.append([value])

        result = []
        for values in zip(*value_lists):
            attr_dict = {
                key: value for key, value in zip(keys, values) if value is not None
            }
            if attr_dict:
                result.append(attr_dict)

        return result

    @staticmethod
    def get_single_string_output(rmd, entry_id, report_key="", row_key=""):
        """
        Get single result from the simulation output files expected to be a string
        ------------------
        Arguments
        ---------
        :param rmd: (RulesetModelDescription) object containing the path to the simulation output files
        :param entry_id: (int) id from NHRList.txt corresponding to the value to retrieve
        :param report_key: (str) to use when RI > 0 and when value to retrieve refers to a particular BDL component
        :param row_key: (str) to use when KT > 0 and when a report has multiple row where each row provides results for a separate building component or month of the year
        :return: value from binary simulation output files
        """
        return get_string_result(
            str(Path(Config.EQUEST_INSTALL_PATH) / "D2Result.dll"),
            rmd.doe2_data_path,
            str(Path(rmd.file_path).with_suffix("")),
            entry_id,
            report_key,
            row_key,
        )

    @staticmethod
    def get_output_data(rmd, requests):
        """
        Get data from the simulation output.
        :param rmd: (RulesetModelDescription) object containing the path to the simulation output files
        :param requests: (dict) dictionary of description (str): (tuple) of entry_id: (int), report_key: (str), and row_key: (str)
        :return: (dict) dictionary of description (str): value (float)
        """

        chunk_size = 12  # Max number of requests to process at a time
        results = {}  # To store the reassociated keys and values

        # Split requests into chunks of at most 12
        for chunk in _chunked_dict(requests, chunk_size):
            # Extract and combine values into a list of tuples for get_multiple_results
            values_list = list(chunk.values())

            # Call the function with the current chunk of values
            chunk_results = get_multiple_results(
                str(Path(Config.EQUEST_INSTALL_PATH) / "D2Result.dll"),
                rmd.doe2_data_path,
                str(Path(rmd.file_path).with_suffix("")),
                values_list,
            )

            # Reassociate returned values with their corresponding keys
            if len(chunk_results) == len(chunk):
                results.update(zip(chunk.keys(), chunk_results))

        results = {key: value for key, value in results.items() if value != -99999}
        return results


class BaseNode(Base):
    """
    Base class for all nodes in the tree.
    'Node' refers to rpd_generator objects that map directly to a 229 schema data group.
    """

    bdl_command = None
    boolean_map = {
        "YES": True,
        "NO": False,
    }

    def __init__(self, u_name, rmd):
        self.rmd = rmd
        self.u_name = u_name
        self.reporting_name = None
        self.notes = None
        self.keyword_value_pairs = {}

    def __repr__(self):
        return f"BaseNode('{self.u_name}')"

    def add_inputs(self, key_val_dict):
        """Insert a keyword-value pair for the BDL command."""
        self.keyword_value_pairs = key_val_dict

    def populate_data_group(self):
        """This method will be overridden by each child class"""
        return None

    def populate_data_elements(self):
        """This method will be overridden by each child class"""
        return None

    def insert_to_rpd(self, container):
        """This method will be overridden by each child class"""
        return None

    def get_obj(self, u_name):
        """
        Return the object instance by its u_name.
        :param u_name: str
        """
        return self.rmd.bdl_obj_instances.get(u_name, None)

    def get_inp(self, keyword, default=None):
        """
        Return the value of the keyword from the keyword_value_pairs.
        :param keyword: str
        :param default: any
        :return: value: str
        """
        return self.keyword_value_pairs.get(keyword, default)

    def get_output_data(self, requests):
        """
        Get data from the simulation output.
        :param requests: (dict) dictionary of description (str): (tuple) of entry_id: (int), report_key: (str), and row_key: (str)
        :return: (dict) dictionary of description (str): value (float)
        """
        return super().get_output_data(self.rmd, requests)

    @staticmethod
    def try_float(value):
        """Attempt to convert a value to a float, returning None if it fails."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            # TODO log error for future GUI error window
            return None

    @staticmethod
    def try_int(value):
        """Attempt to convert a value to an int, returning None if it fails."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            # TODO log error for future GUI error window
            return None

    @staticmethod
    def try_access_index(lst: list, index: int):
        """Attempt to access an index in a list, returning None if it fails."""
        if isinstance(lst, list):
            try:
                return lst[index]
            except (IndexError, TypeError):
                # TODO log error for future GUI error window
                return None
        else:
            return None

    @staticmethod
    def try_length(data: any):
        """Attempt to get the length of data, return 1 if it is a string, or number; otherwise return 0."""
        if isinstance(data, (list, dict)):
            return len(data)
        elif isinstance(data, (str, float, int)):
            return 1
        else:
            return 0

    @staticmethod
    def try_abs(data: any):
        """Attempt to get the absolute value of data, return None if it fails."""
        try:
            return abs(float(data))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def try_convert_units(value: any, from_units: str, to_units: str) -> float | None:
        """
        Convert a value from one unit to another.

        Parameters:
        value (any): The value to convert.
        from_units (str): The units to convert from.
        to_units (str): The units to convert to.

        Returns:
        float | None: The converted value or None if not possible to convert.
        """
        if isinstance(value, (int, float)):
            try:
                return value * ureg(from_units).to(to_units).magnitude
            except pint.errors.DimensionalityError:
                return None
        else:
            return None

    @staticmethod
    def standardize_dict_values(data: dict, keys: list, n: int):
        """
        Standardizes the values of specified keys in a dictionary to lists of length n.

        Parameters:
        data (dict): The dictionary to standardize.
        keys (list): List of keys to standardize in the dictionary.
        n (int): The desired length of the list for each key.

        Returns:
        dict: The dictionary with standardized values.
        """
        for key in keys:
            list_of_values = data.get(key, [])
            new_list_of_values = (
                list_of_values if isinstance(list_of_values, list) else [list_of_values]
            )
            new_list_of_values = (new_list_of_values + ["0"] * n)[:n]
            data[key] = new_list_of_values

        return data


def _chunked_dict(d, n):
    """Yield successive n-sized chunks from dictionary d."""
    it = iter(d)
    for i in range(0, len(d), n):
        yield {k: d[k] for k in islice(it, n)}
