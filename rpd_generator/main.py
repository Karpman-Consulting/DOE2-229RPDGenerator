import json
import shutil
import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

from rpd_generator.artifacts.ruleset_project_description import (
    RulesetProjectDescription,
)
from rpd_generator.artifacts.ruleset_model_description import RulesetModelDescription
from rpd_generator.artifacts.building_segment import BuildingSegment
from rpd_generator.artifacts.building import Building
from rpd_generator.doe2_file_readers.bdlcio32 import process_input_file
from rpd_generator.doe2_file_readers.model_input_reader import ModelInputReader
from rpd_generator.bdl_structure import *
from rpd_generator.config import Config
from rpd_generator.utilities import validate_configuration
from rpd_generator.utilities import unit_converter
from rpd_generator.utilities import ensure_valid_rpd


def write_rpd_json_from_inp(inp_path_str):
    inp_path = Path(inp_path_str)
    # Create a temporary directory to store the files for processing
    with tempfile.TemporaryDirectory() as temp_dir:

        # Prepare the inp file for processing and save the revised copy to the temporary directory
        temp_file_path = prepare_inp(inp_path, Path(temp_dir))

        # Copy the model output files to the temporary directory (.erp, .lrp, .srp, .nhk)
        copy_files_to_temp_dir(inp_path, Path(temp_dir))

        # Set the paths for the inp file, json file, and the directories
        temp_inp_path = Path(temp_file_path)
        bdl_path = temp_inp_path.with_suffix(".BDL")
        json_path = temp_inp_path.with_suffix(".json")
        doe23_path = Path(Config.DOE23_DATA_PATH) / "DOE23"
        bdlcio32_path = Path(Config.EQUEST_INSTALL_PATH) / "Bdlcio32.dll"

        # Process the inp file to create the BDL file with Diagnostic Comments (defaults and evaluated values) in the temporary directory
        process_input_file(
            str(bdlcio32_path),
            str(doe23_path) + "\\",
            str(temp_inp_path.parent) + "\\",
            temp_inp_path.name,
        )
        shutil.copy(str(bdl_path), inp_path.parent)
        # Generate the RPD json file in the temporary directory
        write_rpd_json_from_bdl(str(bdl_path), str(json_path))

        # Copy the json file from the temporary directory back to the project directory
        shutil.copy(str(json_path), inp_path.parent)


def write_rpd_json_from_bdl(bdl_path: str, json_file_path: str):
    bdl_input_reader = ModelInputReader()
    RulesetProjectDescription.bdl_command_dict = bdl_input_reader.bdl_command_dict
    rpd = RulesetProjectDescription()
    rmd = generate_rmd_structures_from_bdls(bdl_input_reader, [bdl_path])[0]
    # Add the RPD object to the bdl_obj_instances dictionary
    rmd.bdl_obj_instances["ASHRAE 229"] = rpd
    # Populate 229 data structures associated with the BDL objects
    rmd.populate_rmd_data()
    # Insert the RMD data into the RPD data structure
    rmd.insert_to_rpd(rpd)

    rpd.populate_data_group()
    ensure_valid_rpd.make_ids_unique(rpd.rpd_data_structure)
    unit_converter.convert_to_schema_units(rpd.rpd_data_structure)
    with open(json_file_path, "w") as json_file:
        json.dump(rpd.rpd_data_structure, json_file, indent=4)

    print(f"RPD JSON file created.")


def write_rpd_json_from_rmds(
    rpd: RulesetProjectDescription, rmds: list, json_file_path: str
):
    for rmd in rmds:
        rmd.insert_to_rpd(rpd)
    rpd.populate_data_group()

    ensure_valid_rpd.make_ids_unique(rpd.rpd_data_structure)
    unit_converter.convert_to_schema_units(rpd.rpd_data_structure)

    with open(json_file_path, "w") as json_file:
        json.dump(rpd.rpd_data_structure, json_file, indent=4)

    print(f"RPD JSON file created.")


def generate_rmd_structures_from_bdls(
    bdl_input_reader: ModelInputReader, selected_models: list
):
    rmds = []
    for model_path_str in selected_models:
        model_path = Path(model_path_str)
        rmd = RulesetModelDescription(model_path.stem)
        rmd.file_path = str(model_path.with_suffix(""))

        default_building = Building("Default Building", rmd)
        default_building_segment = BuildingSegment(
            "Default Building Segment", default_building
        )
        rmd.bdl_obj_instances["Default Building"] = default_building
        rmd.bdl_obj_instances["Default Building Segment"] = default_building_segment

        model_input_data = bdl_input_reader.read_input_bdl_file(str(model_path))
        rmd.doe2_version = model_input_data["doe2_version"]
        if rmd.doe2_version is not None:
            rmd.doe2_data_path = (
                Config.DOE23_DATA_PATH
                if rmd.doe2_version.split("-")[1] == "2.3"
                else Config.DOE22_DATA_PATH
            )

        for command in rmd.COMMAND_PROCESSING_ORDER:
            special_handling = {}
            if command == "ZONE":
                special_handling["ZONE"] = (
                    lambda obj, cmd_dict: rmd.space_map.setdefault(
                        cmd_dict["SPACE"], obj
                    )
                )
            _process_command_group(
                command,
                model_input_data["file_commands"],
                rmd,
                special_handling,
            )
        rmds.append(rmd)
    return rmds


def generate_rmd_structure_from_inp(
    inp_path_str: str, processing_dir: TemporaryDirectory
):
    inp_path = Path(inp_path_str)
    temp_dir = processing_dir.name

    # Prepare the inp file for processing and save the revised copy to the temporary directory
    temp_file_path = prepare_inp(inp_path, Path(temp_dir))

    # Copy the model output files to the temporary directory (.erp, .lrp, .srp, .nhk)
    copy_files_to_temp_dir(inp_path, Path(temp_dir))

    # Set the paths for the inp file, json file, and the directories
    temp_inp_path = Path(temp_file_path)
    bdl_path = temp_inp_path.with_suffix(".BDL")
    doe23_path = Path(Config.DOE23_DATA_PATH) / "DOE23"
    bdlcio32_path = Path(Config.EQUEST_INSTALL_PATH) / "Bdlcio32.dll"

    # Process the inp file to create the BDL file with Diagnostic Comments (defaults and evaluated values) in the temporary directory
    process_input_file(
        str(bdlcio32_path),
        str(doe23_path) + "\\",
        str(temp_inp_path.parent) + "\\",
        temp_inp_path.name,
    )

    # Generate the RMD object from the BDL file in the temporary directory
    bdl_input_reader = ModelInputReader()
    rmd = generate_rmd_structures_from_bdls(bdl_input_reader, [str(bdl_path)])[0]

    return rmd


def prepare_inp(model_path: Path, output_dir: Path = None) -> str:
    model_dir = model_path.parent
    model_name = model_path.name
    base_name = model_path.stem
    extension = model_path.suffix

    if output_dir:
        temp_file_path = output_dir / model_name
    else:
        temp_file_path = model_dir / f"{base_name}_temp{extension}"

    with Path(model_path).open("r") as inp_file, temp_file_path.open("w") as out_file:
        lines_after_target = 0

        for line in inp_file:

            if "$              Abort, Diagnostics" in line:
                lines_after_target = 3

            elif lines_after_target == 1:
                out_file.write("DIAGNOSTIC COMMENTS ..")
                lines_after_target = 0
            elif lines_after_target > 0:
                lines_after_target -= 1

            elif line.lstrip().startswith("LIGHTING-KW"):
                line = line.replace("&D", "0")

            elif line.lstrip().startswith("EQUIPMENT-KW"):
                line = line.replace("&D", "0")

            out_file.write(line)
    return str(temp_file_path)


def copy_files_to_temp_dir(inp_path, temp_dir):
    file_extensions = [".erp", ".lrp", ".srp", ".nhk"]
    model_dir = inp_path.parent
    model_name = inp_path.stem

    for ext in file_extensions:

        model_file = model_dir / f"{model_name}{ext}"
        alternate_search_file = model_dir / f"{model_name} - Baseline Design{ext}"

        if model_file.exists():
            shutil.copy2(model_file, temp_dir)

        elif alternate_search_file.exists():
            destination_file = temp_dir / f"{model_name}{ext}"
            shutil.copy2(alternate_search_file, destination_file)

        else:
            print(f"File {model_file} not found in {model_dir}")


def _create_obj_instance(u_name, command, command_dict, rmd):
    command_class = RulesetProjectDescription.bdl_command_dict[command]
    is_child = command in [
        "SPACE",
        "EXTERIOR-WALL",
        "INTERIOR-WALL",
        "UNDERGROUND-WALL",
        "ZONE",
        "WINDOW",
        "DOOR",
    ]
    inherits_base_node = issubclass(command_class, BaseNode)

    if inherits_base_node and is_child:
        obj_instance = command_class(
            u_name,
            rmd.bdl_obj_instances[command_dict["parent"]],
            rmd,
        )
    else:
        obj_instance = command_class(u_name, rmd)
    return obj_instance


def _process_command_group(
    command_group: str,
    file_bdl_commands: dict,
    rmd: RulesetModelDescription,
    special_handling=None,
):
    for u_name in file_bdl_commands.get(command_group, {}):
        cmd_dict = file_bdl_commands[command_group][u_name]
        obj = _create_obj_instance(u_name, command_group, cmd_dict, rmd)
        if special_handling and command_group in special_handling:
            special_handling[command_group](obj, cmd_dict)
        obj.add_inputs(cmd_dict)
        rmd.bdl_obj_instances[u_name] = obj


if __name__ == "__main__":

    # Test generating an RPD JSON file from one of the test BDL files
    validate_configuration.find_equest_installation()
    # write_rpd_json_from_inp(r"")
    write_rpd_json_from_bdl(
        str(
            Path(__file__).parents[1]
            / "test"
            / "full_rpd_test"
            / "E-1"
            / "229 Test Case E-1 (PSZHP).BDL"
        ),
        str(
            Path(__file__).parents[1]
            / "test"
            / "full_rpd_test"
            / "E-1"
            / "229 Test Case E-1 (PSZHP).json"
        ),
    )
