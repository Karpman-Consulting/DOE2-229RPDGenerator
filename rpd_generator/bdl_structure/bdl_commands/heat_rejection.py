from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


HeatRejectionOptions = SchemaEnums.schema_enums["HeatRejectionOptions"]
HeatRejectionFanOptions = SchemaEnums.schema_enums["HeatRejectionFanOptions"]
HeatRejectionFluidOptions = SchemaEnums.schema_enums["HeatRejectionFluidOptions"]
HeatRejectionFanSpeedControlOptions = SchemaEnums.schema_enums[
    "HeatRejectionFanSpeedControlOptions"
]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_HeatRejectionKeywords = BDLEnums.bdl_enums["HeatRejectionKeywords"]
BDL_HeatRejectionTypes = BDLEnums.bdl_enums["HeatRejectionTypes"]
BDL_HeatRejectionFanSpeedControlOptions = BDLEnums.bdl_enums[
    "HeatRejectionFanSpeedControlOptions"
]


class HeatRejection(BaseNode):
    """Heat Rejection object in the tree."""

    bdl_command = BDL_Commands.HEAT_REJECTION

    heat_rejection_type_map = {
        BDL_HeatRejectionTypes.OPEN_TWR: HeatRejectionOptions.OPEN_CIRCUIT_COOLING_TOWER,
        BDL_HeatRejectionTypes.OPEN_TWR_HX: HeatRejectionOptions.OPEN_CIRCUIT_COOLING_TOWER,  # Should this be OTHER?
        BDL_HeatRejectionTypes.FLUID_COOLER: HeatRejectionOptions.CLOSED_CIRCUIT_COOLING_TOWER,
        BDL_HeatRejectionTypes.DRYCOOLER: HeatRejectionOptions.DRY_COOLER,
        # "": HeatRejectionOptions.EVAPORATIVE_CONDENSER,  # eQUEST chrashes when selecting Evap Condenser. Not shown in Helptext.
    }

    fan_spd_ctrl_map = {
        BDL_HeatRejectionFanSpeedControlOptions.ONE_SPEED_FAN: HeatRejectionFanSpeedControlOptions.CONSTANT,
        BDL_HeatRejectionFanSpeedControlOptions.FLUID_BYPASS: HeatRejectionFanSpeedControlOptions.CONSTANT,
        BDL_HeatRejectionFanSpeedControlOptions.TWO_SPEED_FAN: HeatRejectionFanSpeedControlOptions.TWO_SPEED,
        BDL_HeatRejectionFanSpeedControlOptions.VARIABLE_SPEED_FAN: HeatRejectionFanSpeedControlOptions.VARIABLE_SPEED,
        BDL_HeatRejectionFanSpeedControlOptions.DISCHARGE_DAMPER: HeatRejectionFanSpeedControlOptions.OTHER,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.heat_rejection_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.heat_rejection_data_structure = {}

        # data elements with no children
        self.loop = None
        self.type = None
        self.fan_type = None
        self.fluid = None
        self.range = None
        self.approach = None
        self.fan_shaft_power = None
        self.fan_motor_efficiency = None
        self.fan_motor_nameplate_power = None
        self.fan_speed_control = None
        self.design_wetbulb_temperature = None
        self.design_water_flowrate = None
        self.rated_water_flowrate = None
        self.leaving_water_setpoint_temperature = None

    def __repr__(self):
        return f"HeatRejection(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for heat rejection object."""
        requests = self.get_output_requests()
        output_data = self.get_output_data(requests)

        self.loop = self.get_inp(BDL_HeatRejectionKeywords.CW_LOOP)

        self.type = self.heat_rejection_type_map.get(
            self.get_inp(BDL_HeatRejectionKeywords.TYPE)
        )

        self.fan_speed_control = self.fan_spd_ctrl_map.get(
            self.get_inp(BDL_HeatRejectionKeywords.CAPACITY_CTRL)
        )

        self.range = self.try_float(self.get_inp(BDL_HeatRejectionKeywords.RATED_RANGE))

        self.approach = self.try_float(
            self.get_inp(BDL_HeatRejectionKeywords.RATED_APPROACH)
        )

        self.design_wetbulb_temperature = self.try_float(
            self.get_inp(BDL_HeatRejectionKeywords.DESIGN_WETBULB)
        )

        self.rated_water_flowrate = self.try_float(
            output_data.get("Cooling Tower - Flow (gal/min)")
        )

        circulation_loop = self.get_obj(self.loop)
        if circulation_loop is not None:
            self.leaving_water_setpoint_temperature = (
                circulation_loop.design_supply_temperature[0]
            )

        # Assign pump data elements populated from the heat rejection keyword value pairs
        pump = self.get_obj(self.get_inp(BDL_HeatRejectionKeywords.CW_PUMP))
        if pump:
            pump.loop_or_piping = [self.loop] * pump.qty

    def get_output_requests(self):
        """Return the output requests for the heat rejection object."""
        requests = {
            "Cooling Tower - Capacity (Btu/hr)": (2401021, "", self.u_name),
            "Cooling Tower - Flow (gal/min)": (2401022, "", self.u_name),
            "Cooling Tower - Number of Cells": (2401023, "", self.u_name),
            "Cooling Tower - Fan Power per Cell (kW)": (2401024, "", self.u_name),
            "Cooling Tower - Spray Power per Cell (kW)": (2401025, "", self.u_name),
            "Cooling Tower - Auxiliary (kW)": (2401026, "", self.u_name),
        }
        return requests

    def populate_data_group(self):
        """Populate schema structure for heat rejection object."""
        self.heat_rejection_data_structure = {
            "id": self.u_name,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "loop",
            "type",
            "fan_type",
            "fluid",
            "range",
            "approach",
            "fan_shaft_power",
            "fan_motor_efficiency",
            "fan_motor_nameplate_power",
            "fan_speed_control",
            "design_wetbulb_temperature",
            "design_water_flowrate",
            "rated_water_flowrate",
            "leaving_water_setpoint_temperature",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.heat_rejection_data_structure[attr] = value

    def insert_to_rpd(self):
        """Insert window object into the rpd data structure."""
        self.rmd.heat_rejections.append(self.heat_rejection_data_structure)
