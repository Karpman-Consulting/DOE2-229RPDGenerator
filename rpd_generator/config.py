from rpd_generator.schema.ruleset import Ruleset
from rpd_generator.schema.schema_enums import SchemaEnums


class Config:
    """
    Class to store a user's file paths for various files referenced by the program
    """

    RULESETS = {
        "ASHRAE 90.1-2019": {
            "enum_filename": "Enumerations2019ASHRAE901.schema.json",
            "output_filename": "Output2019ASHRAE901.schema.json",
        }
    }

    EQUEST_INSTALL_PATH = None
    DOE22_DATA_PATH = None
    DOE23_DATA_PATH = None
    ACTIVE_RULESET_DICT = RULESETS["ASHRAE 90.1-2019"]
    ACTIVE_RULESET = Ruleset(
        name="ASHRAE 90.1-2019",
        enum_filename=ACTIVE_RULESET_DICT.get("enum_filename"),
        output_filename=ACTIVE_RULESET_DICT.get("output_filename"),
    )
    SchemaEnums.update_schema_enum(ACTIVE_RULESET)

    @staticmethod
    def set_active_ruleset(ruleset_name: str):
        ruleset_dict = Config.RULESETS.get(ruleset_name)
        if ruleset_dict:
            Config.ACTIVE_RULESET = Ruleset(
                name=ruleset_name,
                enum_filename=ruleset_dict.get("enum_filename"),
                output_filename=ruleset_dict.get("output_filename"),
            )
            SchemaEnums.update_schema_enum(Config.ACTIVE_RULESET)
