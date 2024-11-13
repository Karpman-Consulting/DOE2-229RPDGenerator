from itertools import islice
from pathlib import Path

from rpd_generator.doe2_file_readers.model_output_reader import get_string_result
from rpd_generator.config import Config


class BaseDefinition:
    """
    Base class for BDL commands that are not nodes in the tree, but are used to populate 229 schema data elements.
    """

    bdl_command = None
    boolean_map = {
        "YES": True,
        "NO": False,
    }

    def __init__(self, u_name, rmd):
        self.rmd = rmd
        self.u_name = u_name
        self.keyword_value_pairs = {}

    def __repr__(self):
        return f"BaseDefinition('{self.u_name}')"

    def add_inputs(self, key_val_dict):
        """Insert a keyword-value pair for the BDL command."""
        self.keyword_value_pairs = key_val_dict

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

    def populate_data_elements(self):
        """This method will be overridden by each child class"""
        return None

    def get_single_string_output(self, entry_id):
        """
        Get single result from the simulation output files expected to be a string
        ------------------
        Arguments
        ---------
        :param entry_id: (int) id from NHRList.txt corresponding to the value to retrieve
        :return: value from binary simulation output files
        """
        return get_string_result(
            str(Path(Config.EQUEST_INSTALL_PATH) / "D2Result.dll"),
            self.rmd.doe2_data_path,
            str(Path(self.rmd.file_path).with_suffix("")),
            entry_id,
        )

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


def _chunked_dict(d, n):
    """Yield successive n-sized chunks from dictionary d."""
    it = iter(d)
    for i in range(0, len(d), n):
        yield {k: d[k] for k in islice(it, n)}
