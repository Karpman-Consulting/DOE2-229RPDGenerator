from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


PumpSpecificationMethodOptions = SchemaEnums.schema_enums[
    "PumpSpecificationMethodOptions"
]
PumpSpeedControlOptions = SchemaEnums.schema_enums["PumpSpeedControlOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_PumpKeywords = BDLEnums.bdl_enums["PumpKeywords"]
BDL_PumpCapacityControlOptions = BDLEnums.bdl_enums["PumpCapacityControlOptions"]


class Pump(BaseNode):
    """Pump object in the tree."""

    bdl_command = BDL_Commands.PUMP

    pump_speed_control_map = {
        BDL_PumpCapacityControlOptions.ONE_SPEED_PUMP: PumpSpeedControlOptions.FIXED_SPEED,
        BDL_PumpCapacityControlOptions.TWO_SPEED_PUMP: PumpSpeedControlOptions.TWO_SPEED,
        BDL_PumpCapacityControlOptions.VAR_SPEED_PUMP: PumpSpeedControlOptions.VARIABLE_SPEED,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.pump_names.append(u_name)
        self.rmd.bdl_obj_instances[u_name] = self

        self.qty = None
        self.pump_data_structures = []
        self.output_data = None
        # data elements with children
        self.output_validation_points = []

        # data elements with no children
        self.loop_or_piping = []
        self.specification_method = []
        self.design_electric_power = []
        # self.motor_nameplate_power = None  # Commented because eQUEST does not support this attribute, nor will we
        self.design_head = []
        self.impeller_efficiency = []
        self.motor_efficiency = []
        self.speed_control = []
        self.design_flow = []
        self.is_flow_sized_based_on_design_day = []

    def __repr__(self):
        return f"Pump(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate the schema data elements for the pump object."""

        self.qty = self.try_int(self.try_float(self.get_inp(BDL_PumpKeywords.NUMBER)))
        requests = self.get_output_requests()
        self.output_data = self.get_output_data(requests)
        self.loop_or_piping = [None] * self.qty
        self.speed_control = [None] * self.qty
        self.is_flow_sized_based_on_design_day = [None] * self.qty
        spec_method = (
            PumpSpecificationMethodOptions.SIMPLE
            if self.get_inp(BDL_PumpKeywords.PUMP_KW) is not None
            else PumpSpecificationMethodOptions.DETAILED
        )
        self.specification_method = [spec_method] * self.qty
        if spec_method == PumpSpecificationMethodOptions.SIMPLE:
            self.design_electric_power = [
                self.try_float(self.get_inp(BDL_PumpKeywords.PUMP_KW))
            ] * self.qty
        else:
            self.design_electric_power = [
                self.output_data.get("Pump - Power (kW)")
            ] * self.qty
        self.design_head = [
            self.try_float(self.get_inp(BDL_PumpKeywords.HEAD))
        ] * self.qty
        self.impeller_efficiency = [
            self.output_data.get("Pump - Mechanical Eff (frac)")
        ] * self.qty
        self.motor_efficiency = [
            self.output_data.get("Pump - Motor Eff (frac)")
        ] * self.qty
        self.design_flow = [self.output_data.get("Pump - Flow (gal/min)")] * self.qty
        if self.get_inp(BDL_PumpKeywords.CAP_CTRL):
            self.speed_control = [
                self.pump_speed_control_map.get(self.get_inp(BDL_PumpKeywords.CAP_CTRL))
            ] * self.qty
        if self.try_float(self.get_inp(BDL_PumpKeywords.FLOW)):
            self.is_flow_sized_based_on_design_day = [False] * self.qty
        else:
            self.is_flow_sized_based_on_design_day = [True] * self.qty

    def get_output_requests(self):
        """Get the output requests for the pump object."""

        requests = {
            "Pump - Flow (gal/min)": (2401002, "", self.u_name),
            "Pump - Power (kW)": (2401005, "", self.u_name),
            "Pump - Mechanical Eff (frac)": (2401006, "", self.u_name),
            "Pump - Motor Eff (frac)": (2401007, "", self.u_name),
        }
        return requests

    def populate_data_group(self):
        """Populate the schema data structure for the pump object."""

        no_children_attributes = [
            "loop_or_piping",
            "specification_method",
            "design_electric_power",
            "design_head",
            "impeller_efficiency",
            "motor_efficiency",
            "speed_control",
            "design_flow",
            "is_flow_sized_based_on_design_day",
        ]

        for i in range(self.qty):
            pump_data_structure = {
                "id": self.u_name + f" {i}".replace(" 0", ""),
                "output_validation_points": [],
            }
            # Iterate over the no_children_attributes list and populate if the value is not None
            for attr in no_children_attributes:
                values = getattr(self, attr, None)
                value = values[i]
                if value is not None:
                    pump_data_structure[attr] = value
            self.pump_data_structures.append(pump_data_structure)

    def insert_to_rpd(self, rmd):
        """Insert window object into the rpd data structure."""
        rmd.pumps.extend(self.pump_data_structures)
