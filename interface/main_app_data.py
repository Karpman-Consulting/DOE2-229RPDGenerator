import atexit
import tempfile
import customtkinter as ctk
from pathlib import Path

from rpd_generator import main as rpd_generator
from rpd_generator.doe2_file_readers.model_input_reader import ModelInputReader
from rpd_generator.config import Config
from rpd_generator.schema.schema_enums import SchemaEnums


class MainAppData:

    def __init__(self):
        self.set_enumeration_data()
        self.processing_dir = tempfile.TemporaryDirectory()
        atexit.register(self.processing_dir.cleanup)

        self.bdl_reader = ModelInputReader()
        self.rpd = None

        # Config data
        self.installation_path = ctk.StringVar()
        self.user_lib_path = ctk.StringVar()
        self.files_verified = False

        # Test data
        self.test_inp_path = ctk.StringVar()

        # Project data
        self.project_name = ctk.StringVar()
        self.selected_ruleset = ctk.StringVar()
        self.selected_ruleset.set("ASHRAE 90.1-2019")
        self.has_rotation_exception = ctk.BooleanVar()
        self.is_all_new_construction = ctk.BooleanVar()
        self.ruleset_model_file_paths = {}
        self.output_directory = ctk.StringVar()

        self.rmds = []
        self.warnings = []
        self.errors = []

        self.installation_path.set(Config.EQUEST_INSTALL_PATH)

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

    def generate_rmd_data(self, rpd):
        for ruleset_model_type, file_path in self.ruleset_model_file_paths.items():
            if file_path:
                rmd = rpd_generator.generate_rmd_structure_from_inp(
                    rpd, file_path, self.processing_dir
                )

                rmd.populate_all_child_data_elements()
                rmd.type = ruleset_model_type
                self.rmds.append(rmd)

    def call_write_rpd_json_from_inp(self):
        rpd_generator.write_rpd_json_from_inp(str(self.test_inp_path.get()))

    def call_write_rpd_json_from_rmds(self):
        rpd_generator.write_rpd_json_from_rpd(
            self.rpd,
            self.rmds,
            str(Path(self.output_directory.get()) / f"{self.project_name.get()}.json"),
        )

    def set_enumeration_data(self):
        enumerators = [
            "SubsurfaceClassificationOptions",
            "CommonConstructionClassificationOptions",
            "CommonRulesetModelOptions",
            "ComponentLocationOptions",
            "CoolingDesignDayOptions",
            "DehumidificationOptions",
            "DrawPatternOptions",
            "HeatRejectionFanOptions",
            "HeatingDesignDayOptions",
            "MiscellaneousEquipmentOptions",
            "SpaceFunctionOptions",
            "StatusOptions",
            "WeatherFileDataSourceOptions",
            "ClimateZoneOptions2019ASHRAE901",
            "CompliancePathOptions2019ASHRAE901",
            "ConstructionClassificationOptions2019ASHRAE901",
            "EnvelopeSpaceOptions2019ASHRAE901",
            "ExteriorLightingZoneOptions2019ASHRAE901",
            "HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901",
            "LightingBuildingAreaOptions2019ASHRAE901T951TG38",
            "LightingPurposeOptions2019ASHRAE901",
            "LightingSpaceOptions2019ASHRAE901TG37",
            "LightingOccupancyControlOptions",
            "LightingDaylightingControlOptions",
            "OutputSchemaOptions2019ASHRAE901",
            "RulesetModelOptions2019ASHRAE901",
            "ServiceWaterHeatingSpaceOptions2019ASHRAE901",
            "SubsurfaceFrameOptions2019ASHRAE901",
            "SubsurfaceSubclassificationOptions2019ASHRAE901",
            "VentilationSpaceOptions2019ASHRAE901",
            "VerticalFenestrationBuildingAreaOptions2019ASHRAE901",
        ]
        for enumerator in enumerators:
            schema_enums = SchemaEnums.schema_enums[enumerator]
            schema_descriptions = SchemaEnums.schema_descriptions[enumerator]
            setattr(self, enumerator, schema_enums.get_list())
            setattr(
                self,
                f"{enumerator.replace('Options', 'Descriptions')}",
                schema_descriptions.get_list(),
            )

    @staticmethod
    def validate_entry(arg):
        if str.isdigit(arg) or arg == "":
            return True
        else:
            return False
