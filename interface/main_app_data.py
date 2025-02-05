import customtkinter as ctk
from pathlib import Path

from rpd_generator import main as rpd_generator
from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.doe2_file_readers.model_input_reader import ModelInputReader
from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums


class MainAppData:

    CommonConstructionClassificationOptions = SchemaEnums.schema_descriptions[
        "CommonConstructionClassificationOptions"
    ]
    CommonRulesetModelOptions = SchemaEnums.schema_descriptions[
        "CommonRulesetModelOptions"
    ]
    ComponentLocationOptions = SchemaEnums.schema_descriptions[
        "ComponentLocationOptions"
    ]
    CoolingDesignDayOptions = SchemaEnums.schema_descriptions["CoolingDesignDayOptions"]
    DrawPatternOptions = SchemaEnums.schema_descriptions["DrawPatternOptions"]
    HeatRejectionFanOptions = SchemaEnums.schema_descriptions["HeatRejectionFanOptions"]
    HeatingDesignDayOptions = SchemaEnums.schema_descriptions["HeatingDesignDayOptions"]
    MiscellaneousEquipmentOptions = SchemaEnums.schema_descriptions[
        "MiscellaneousEquipmentOptions"
    ]
    SpaceFunctionOptions = SchemaEnums.schema_descriptions["SpaceFunctionOptions"]
    StatusOptions = SchemaEnums.schema_descriptions["StatusOptions"]
    WeatherFileDataSourceOptions = SchemaEnums.schema_descriptions[
        "WeatherFileDataSourceOptions"
    ]
    ClimateZoneOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "ClimateZoneOptions2019ASHRAE901"
    ]
    CompliancePathOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "CompliancePathOptions2019ASHRAE901"
    ]
    ConstructionClassificationOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "ConstructionClassificationOptions2019ASHRAE901"
    ]
    EnvelopeSpaceOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "EnvelopeSpaceOptions2019ASHRAE901"
    ]
    ExteriorLightingZoneOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "ExteriorLightingZoneOptions2019ASHRAE901"
    ]
    HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901 = (
        SchemaEnums.schema_descriptions[
            "HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901"
        ]
    )
    LightingBuildingAreaOptions2019ASHRAE901T951TG38 = SchemaEnums.schema_descriptions[
        "LightingBuildingAreaOptions2019ASHRAE901T951TG38"
    ]
    LightingPurposeOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "LightingPurposeOptions2019ASHRAE901"
    ]
    LightingSpaceOptions2019ASHRAE901TG37 = SchemaEnums.schema_descriptions[
        "LightingSpaceOptions2019ASHRAE901TG37"
    ]
    OutputSchemaOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "OutputSchemaOptions2019ASHRAE901"
    ]
    RulesetModelOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "RulesetModelOptions2019ASHRAE901"
    ]
    ServiceWaterHeatingSpaceOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "ServiceWaterHeatingSpaceOptions2019ASHRAE901"
    ]
    SubsurfaceFrameOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "SubsurfaceFrameOptions2019ASHRAE901"
    ]
    SubsurfaceSubclassificationOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "SubsurfaceSubclassificationOptions2019ASHRAE901"
    ]
    VentilationSpaceOptions2019ASHRAE901 = SchemaEnums.schema_descriptions[
        "VentilationSpaceOptions2019ASHRAE901"
    ]
    VerticalFenestrationBuildingAreaOptions2019ASHRAE901 = (
        SchemaEnums.schema_descriptions[
            "VerticalFenestrationBuildingAreaOptions2019ASHRAE901"
        ]
    )

    def __init__(self):
        self.bdl_reader = ModelInputReader()
        RulesetProjectDescription.bdl_command_dict = self.bdl_reader.bdl_command_dict
        self.rpd = RulesetProjectDescription()

        # Config data
        self.installation_path = ctk.StringVar()
        self.user_lib_path = None
        self.files_verified = False

        # Test data
        self.test_inp_path = ctk.StringVar()

        # Project data
        self.selected_ruleset = ctk.StringVar()
        self.selected_ruleset.set("ASHRAE 90.1-2019")
        self.ruleset_model_file_paths = {}

        self.rmds = []
        self.warnings = []
        self.errors = []

        self.installation_path.set(Config.EQUEST_INSTALL_PATH)
        self.configuration_data = {}

    @staticmethod
    def verify_associated_files(file_path: str) -> bool:
        """
        Check if the directory of the given file contains files with the same name
        or the same name with the suffix ' - Baseline Design' for the specified file types.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if all related files are found, False otherwise.
        """
        # Expected file extensions
        file_extensions = [".erp", ".srp", ".lrp", ".nhk"]

        file_path = Path(file_path)
        base_name = file_path.stem
        directory = file_path.parent

        # Check for each file type
        for ext in file_extensions:
            # Construct file names to check
            normal_file = directory / f"{base_name}{ext}"
            baseline_file = directory / f"{base_name} - Baseline Design{ext}"
            # Check existence
            if not normal_file.is_file() and not baseline_file.is_file():
                return False

        return True

    def generate_rmds(self):
        for ruleset_model_type, file_path in self.ruleset_model_file_paths.items():
            if file_path:
                rmd = rpd_generator.generate_rmd_from_inp(file_path)
                rmd.type = ruleset_model_type
                self.rmds.append(rmd)

    def call_write_rpd_json_from_inp(self):
        rpd_generator.write_rpd_json_from_inp(str(self.test_inp_path.get()))
