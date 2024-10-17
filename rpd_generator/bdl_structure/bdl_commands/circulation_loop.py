from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

FluidLoopOptions = SchemaEnums.schema_enums["FluidLoopOptions"]
FluidLoopOperationOptions = SchemaEnums.schema_enums["FluidLoopOperationOptions"]
FluidLoopFlowControlOptions = SchemaEnums.schema_enums["FluidLoopFlowControlOptions"]
TemperatureResetOptions = SchemaEnums.schema_enums["TemperatureResetOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_CirculationLoopKeywords = BDLEnums.bdl_enums["CirculationLoopKeywords"]
BDL_CirculationLoopTypes = BDLEnums.bdl_enums["CirculationLoopTypes"]
BDL_CirculationLoopSubtypes = BDLEnums.bdl_enums["CirculationLoopSubtypes"]
BDL_CirculationLoopSizingOptions = BDLEnums.bdl_enums["CirculationLoopSizingOptions"]
BDL_CirculationLoopOperationOptions = BDLEnums.bdl_enums[
    "CirculationLoopOperationOptions"
]
BDL_CirculationLoopTemperatureResetOptions = BDLEnums.bdl_enums[
    "CirculationLoopTemperatureResetOptions"
]
BDL_SecondaryLoopValveTypes = BDLEnums.bdl_enums["CirculationLoopSecondaryValveTypes"]
BDL_SystemCoolingValveTypes = BDLEnums.bdl_enums["SystemCoolingValveTypes"]
BDL_SystemHeatingValveTypes = BDLEnums.bdl_enums["SystemHeatingValveTypes"]
BDL_FlowControlOptions = BDLEnums.bdl_enums["FlowControlOptions"]
BDL_ZoneCondenserValveOptions = BDLEnums.bdl_enums["ZoneCWValveOptions"]
BDL_ChillerKeywords = BDLEnums.bdl_enums["ChillerKeywords"]
BDL_BoilerKeywords = BDLEnums.bdl_enums["BoilerKeywords"]
BDL_HeatRejectionKeywords = BDLEnums.bdl_enums["HeatRejectionKeywords"]
BDL_SystemKeywords = BDLEnums.bdl_enums["SystemKeywords"]
BDL_GroundLoopHXKeywords = BDLEnums.bdl_enums["GroundLoopHXKeywords"]
BDL_ZoneKeywords = BDLEnums.bdl_enums["ZoneKeywords"]
BDL_EquipCtrlKeywords = BDLEnums.bdl_enums["EquipCtrlKeywords"]


class CirculationLoop(BaseNode):
    """CirculationLoop object in the tree."""

    bdl_command = BDL_Commands.CIRCULATION_LOOP

    loop_type_map = {
        BDL_CirculationLoopTypes.CHW: FluidLoopOptions.COOLING,
        BDL_CirculationLoopTypes.HW: FluidLoopOptions.HEATING,
        BDL_CirculationLoopTypes.CW: FluidLoopOptions.CONDENSER,
        BDL_CirculationLoopTypes.PIPE2: FluidLoopOptions.HEATING_AND_COOLING,
        BDL_CirculationLoopTypes.WLHP: FluidLoopOptions.OTHER,
    }

    sizing_option_map = {
        BDL_CirculationLoopSizingOptions.COINCIDENT: True,
        BDL_CirculationLoopSizingOptions.NON_COINCIDENT: False,
        BDL_CirculationLoopSizingOptions.PRIMARY: False,
        BDL_CirculationLoopSizingOptions.SECONDARY: True,
    }

    loop_operation_map = {
        BDL_CirculationLoopOperationOptions.STANDBY: None,  # This is a special case
        BDL_CirculationLoopOperationOptions.DEMAND: FluidLoopOperationOptions.INTERMITTENT,
        BDL_CirculationLoopOperationOptions.SNAP: FluidLoopOperationOptions.INTERMITTENT,
        BDL_CirculationLoopOperationOptions.SCHEDULED: None,  # This is a special case
        BDL_CirculationLoopOperationOptions.SUBHOUR_DEMAND: FluidLoopOperationOptions.INTERMITTENT,
    }

    temp_reset_map = {
        BDL_CirculationLoopTemperatureResetOptions.FIXED: TemperatureResetOptions.NO_RESET,
        BDL_CirculationLoopTemperatureResetOptions.OA_RESET: TemperatureResetOptions.OUTSIDE_AIR_RESET,
        BDL_CirculationLoopTemperatureResetOptions.SCHEDULED: TemperatureResetOptions.OTHER,
        BDL_CirculationLoopTemperatureResetOptions.LOAD_RESET: TemperatureResetOptions.LOAD_RESET,
        BDL_CirculationLoopTemperatureResetOptions.WETBULB_RESET: TemperatureResetOptions.OTHER,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.circulation_loop_names.append(u_name)

        # keep track of the type of circulation loop (different from self.type which is the schema data element: FluidLoop.type)
        self.circulation_loop_type = None  # "ServiceWaterPiping", "ServiceWaterHeatingDistributionSystem", "FluidLoop", or "SecondaryFluidLoop"

        # Initialize the data structure for the different types of circulation loops
        self.data_structure = {}

        # FluidLoop data elements with children
        self.cooling_or_condensing_design_and_control = {}
        self.heating_design_and_control = {}
        self.child_loops = []

        # FluidLoop data elements with no children
        self.type = None
        self.pump_power_per_flow_rate = None

        # ServiceWaterHeatingDistributionSystem data elements with children
        self.service_water_piping = {}
        self.tanks = {}

        # FluidLoopDesignAndControl data elements with no children [cooling, heating]
        self.design_supply_temperature: list = [None, None]
        self.design_return_temperature: list = [None, None]
        self.is_sized_using_coincident_load: list = [None, None]
        self.minimum_flow_fraction: list = [None, None]
        self.operation: list = [None, None]
        self.operation_schedule: list = [None, None]
        self.flow_control: list = [None, None]
        self.temperature_reset_type: list = [None, None]
        self.outdoor_high_for_loop_supply_reset_temperature: list = [None, None]
        self.outdoor_low_for_loop_supply_reset_temperature: list = [None, None]
        self.loop_supply_temperature_at_outdoor_high: list = [None, None]
        self.loop_supply_temperature_at_outdoor_low: list = [None, None]
        self.loop_supply_temperature_at_low_load: list = [None, None]
        self.has_integrated_waterside_economizer: list = [None, None]

        # ServiceWaterHeatingDistributionSystem data elements with no children
        self.swh_design_supply_temperature = None
        self.design_supply_temperature_difference = None
        self.is_central_system = None
        self.distribution_compactness = None
        self.control_type = None
        self.configuration_type = None
        self.is_recovered_heat_from_drain_used_by_water_heater = None
        self.drain_heat_recovery_efficiency = None
        self.drain_heat_recovery_type = None
        self.flow_multiplier_schedule = None
        self.entering_water_mains_temperature_schedule = None
        self.is_ground_temperature_used_for_entering_water = None

        # ServiceWaterPiping data elements with no children
        self.is_recirculation_loop = None
        self.insulation_thickness = None
        self.loop_pipe_location = None
        self.location_zone = None
        self.length = None
        self.diameter = None
        # self.child = None   this is commented out because in eQUEST every secondary loop is a child of a primary loop

    def __repr__(self):
        return f"CirculationLoop(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements from the keyword_value pairs returned from model_input_reader"""

        # Assign pump data elements populated from the circulation loop keyword value pairs
        pump_name = self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_PUMP)
        if pump_name is not None:
            self.populate_pump_data_elements(pump_name)

        self.circulation_loop_type = self.determine_circ_loop_type()
        if self.circulation_loop_type in ["FluidLoop", "SecondaryFluidLoop"]:
            loop_type = self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.TYPE)
            self.type = self.loop_type_map.get(loop_type, FluidLoopOptions.OTHER)

            # Populate the data elements for FluidLoopDesignAndControl
            if self.circulation_loop_type in ["FluidLoop", "SecondaryFluidLoop"]:
                if self.type == FluidLoopOptions.COOLING:
                    self.populate_cool_fluid_loop_design_and_control()
                elif self.type == FluidLoopOptions.CONDENSER:
                    self.populate_cond_fluid_loop_design_and_control()
                elif self.type == FluidLoopOptions.HEATING:
                    self.populate_heat_fluid_loop_design_and_control()
                elif self.type == FluidLoopOptions.HEATING_AND_COOLING:
                    self.populate_heat_cool_fluid_loop_design_and_control()

        if self.circulation_loop_type == "ServiceWaterHeatingDistributionSystem":
            self.populate_service_water_heating_distribution_system()

        if self.circulation_loop_type == "ServiceWaterPiping":
            # None of the data elements for ServiceWaterPiping can be populated from model inputs or outputs
            pass

        # Populate pump_power_per_flow_rate
        if pump_name is not None:
            loop_pump = self.rmd.bdl_obj_instances.get(pump_name)
            output_data = loop_pump.output_data
            self.pump_power_per_flow_rate = (
                output_data.get("Pump - Power (kW)")
                / output_data.get("Pump - Flow (gal/min)")
                * 1000
            )

    def populate_data_group(self):
        """Populate schema structure for circulation loop object."""

        design_and_control_elements = [
            "design_supply_temperature",
            "design_return_temperature",
            "is_sized_using_coincident_load",
            "minimum_flow_fraction",
            "operation",
            "operation_schedule",
            "flow_control",
            "temperature_reset_type",
            "outdoor_high_for_loop_supply_reset_temperature",
            "outdoor_low_for_loop_supply_reset_temperature",
            "loop_supply_temperature_at_outdoor_high",
            "loop_supply_temperature_at_outdoor_low",
            "loop_supply_temperature_at_low_load",
            "has_integrated_waterside_economizer",
        ]

        service_water_heating_distribution_system_elements = [
            "design_supply_temperature",
            "design_supply_temperature_difference",
            "is_central_system",
            "distribution_compactness",
            "control_type",
            "configuration_type",
            "is_recovered_heat_from_drain_used_by_water_heater",
            "drain_heat_recovery_efficiency",
            "drain_heat_recovery_type",
            "flow_multiplier_schedule",
            "entering_water_mains_temperature_schedule",
            "is_ground_temperature_used_for_entering_water",
        ]

        service_water_piping_elements = [
            "is_recirculation_loop",
            "insulation_thickness",
            "loop_pipe_location",
            "location_zone",
            "length",
            "diameter",
        ]

        if self.circulation_loop_type == "ServiceWaterPiping":
            self.data_structure = {
                "id": self.u_name,
            }

            for attr in service_water_piping_elements:
                value = getattr(self, attr, None)
                if value is not None:
                    self.data_structure[attr] = value

        elif self.circulation_loop_type == "ServiceWaterHeatingDistributionSystem":
            self.data_structure = {
                "id": self.u_name,
                "tanks": self.tanks,
                "service_water_piping": self.service_water_piping,
            }

            for attr in service_water_heating_distribution_system_elements:
                # design_supply_temperature exists in both the circulation loop and the swh distribution system
                if attr == "design_supply_temperature":
                    value = self.swh_design_supply_temperature
                else:
                    value = getattr(self, attr, None)
                if value is not None:
                    self.data_structure[attr] = value

        else:
            for attr in design_and_control_elements:
                value_list = getattr(self, attr, None)
                if value_list[0] is not None:
                    self.cooling_or_condensing_design_and_control[attr] = value_list[0]
                if value_list[1] is not None:
                    self.heating_design_and_control[attr] = value_list[1]

            self.data_structure = {
                "id": self.u_name,
                "cooling_or_condensing_design_and_control": self.cooling_or_condensing_design_and_control,
                "heating_design_and_control": self.heating_design_and_control,
                "child_loops": self.child_loops,
            }

            fluid_loop_elements = [
                "reporting_name",
                "notes",
                "type",
                "pump_power_per_flow_rate",
            ]

            # Iterate over the no_children_attributes list and populate if the value is not None
            for attr in fluid_loop_elements:
                value = getattr(self, attr, None)
                if value is not None:
                    self.data_structure[attr] = value

    def insert_to_rpd(self, rmd):

        if self.circulation_loop_type == "FluidLoop":
            rmd.fluid_loops.append(self.data_structure)

        elif self.circulation_loop_type == "SecondaryFluidLoop":
            primary_loop = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.PRIMARY_LOOP
            )
            for fluid_loop in rmd.fluid_loops:
                if fluid_loop["id"] == primary_loop:
                    fluid_loop["child_loops"].append(self.data_structure)

        elif self.circulation_loop_type == "ServiceWaterHeatingDistributionSystem":
            rmd.service_water_heating_distribution_systems.append(self.data_structure)

        elif self.circulation_loop_type == "ServiceWaterPiping":
            primary_loop = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.PRIMARY_LOOP
            )
            for swh_distribution_sys in rmd.service_water_heating_distribution_systems:
                if swh_distribution_sys["id"] == primary_loop:
                    swh_distribution_sys["service_water_piping"].append(
                        self.data_structure
                    )

    def determine_circ_loop_type(self):

        if (
            self.keyword_value_pairs[BDL_CirculationLoopKeywords.TYPE]
            == BDL_CirculationLoopTypes.DHW
            and self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SUBTYPE)
            == BDL_CirculationLoopSubtypes.SECONDARY
        ):
            return "ServiceWaterPiping"

        elif (
            self.keyword_value_pairs[BDL_CirculationLoopKeywords.TYPE]
            == BDL_CirculationLoopTypes.DHW
        ):
            return "ServiceWaterHeatingDistributionSystem"

        elif (
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.PRIMARY_LOOP)
            is None
        ):
            return "FluidLoop"

        else:
            return "SecondaryFluidLoop"

    def populate_heat_fluid_loop_design_and_control(self):
        self.heating_design_and_control["id"] = self.u_name + " HeatingDesign/Control"
        self.design_supply_temperature[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_HEAT_T)
        )
        loop_design_dt = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_DESIGN_DT)
        )
        if loop_design_dt is not None:
            self.design_return_temperature[1] = (
                self.design_supply_temperature[1] - loop_design_dt
            )
        self.is_sized_using_coincident_load[1] = self.sizing_option_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SIZING_OPTION)
        )
        self.minimum_flow_fraction[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_MIN_FLOW)
        )
        self.temperature_reset_type[1] = self.temp_reset_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL)
        )
        self.loop_supply_temperature_at_low_load[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.MIN_RESET_T)
        )
        self.flow_control[1] = self.determine_loop_flow_control()
        operation = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.LOOP_OPERATION
        )
        if operation == BDL_CirculationLoopOperationOptions.SCHEDULED:
            schedule = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.HEATING_SCHEDULE
            )
            if schedule and self.is_operation_schedule_continuous(schedule):
                self.operation[1] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[1] = FluidLoopOperationOptions.SCHEDULED
        elif operation == BDL_CirculationLoopOperationOptions.STANDBY:
            if self.is_loop_operation_continuous():
                self.operation[1] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[1] = FluidLoopOperationOptions.INTERMITTENT
        else:
            self.operation[1] = self.loop_operation_map.get(operation)

    def populate_cool_fluid_loop_design_and_control(self):
        self.cooling_or_condensing_design_and_control["id"] = (
            self.u_name + " CoolingDesign/Control"
        )
        self.design_supply_temperature[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_COOL_T)
        )
        loop_design_dt = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_DESIGN_DT)
        )
        if loop_design_dt is None:
            pass
        else:
            self.design_return_temperature[0] = (
                self.design_supply_temperature[0] + loop_design_dt
            )
        self.is_sized_using_coincident_load[0] = self.sizing_option_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SIZING_OPTION)
        )
        self.minimum_flow_fraction[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_MIN_FLOW)
        )
        self.temperature_reset_type[0] = self.temp_reset_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.COOL_SETPT_CTRL)
        )
        self.loop_supply_temperature_at_low_load[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.MAX_RESET_T)
        )
        self.flow_control[0] = self.determine_loop_flow_control()
        operation = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.LOOP_OPERATION
        )
        if operation == BDL_CirculationLoopOperationOptions.SCHEDULED:
            schedule = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.COOLING_SCHEDULE
            )
            if schedule and self.is_operation_schedule_continuous(schedule):
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.SCHEDULED
        elif operation == BDL_CirculationLoopOperationOptions.STANDBY:
            if self.is_loop_operation_continuous():
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.INTERMITTENT
        else:
            self.operation[0] = self.loop_operation_map.get(operation)

    def populate_cond_fluid_loop_design_and_control(self):
        self.cooling_or_condensing_design_and_control["id"] = (
            self.u_name + " CondensingDesign/Control"
        )
        self.design_supply_temperature[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_COOL_T)
        )
        loop_design_dt = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_DESIGN_DT)
        )
        if loop_design_dt is None:
            pass
        else:
            self.design_return_temperature[0] = (
                self.design_supply_temperature[0] + loop_design_dt
            )
        self.is_sized_using_coincident_load[0] = self.sizing_option_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SIZING_OPTION)
        )
        self.minimum_flow_fraction[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_MIN_FLOW)
        )
        self.temperature_reset_type[0] = self.temp_reset_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.COOL_SETPT_CTRL)
        )
        self.loop_supply_temperature_at_low_load[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.MAX_RESET_T)
        )
        self.flow_control[0] = self.determine_loop_flow_control()
        operation = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.LOOP_OPERATION
        )
        if operation == BDL_CirculationLoopOperationOptions.SCHEDULED:
            schedule = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.COOLING_SCHEDULE
            )
            if schedule and self.is_operation_schedule_continuous(schedule):
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.SCHEDULED
        elif operation == BDL_CirculationLoopOperationOptions.STANDBY:
            if self.is_loop_operation_continuous():
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.INTERMITTENT
        else:
            self.operation[0] = self.loop_operation_map.get(operation)

    def populate_heat_cool_fluid_loop_design_and_control(self):
        self.cooling_or_condensing_design_and_control["id"] = (
            self.u_name + " CoolingDesign/Control"
        )
        self.design_supply_temperature[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_COOL_T)
        )
        loop_design_dt = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_DESIGN_DT)
        )
        if loop_design_dt is None:
            pass
        else:
            self.design_return_temperature[0] = (
                self.design_supply_temperature[0] + loop_design_dt
            )
        self.is_sized_using_coincident_load[0] = self.sizing_option_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SIZING_OPTION)
        )
        self.minimum_flow_fraction[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_MIN_FLOW)
        )
        self.temperature_reset_type[0] = self.temp_reset_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.COOL_SETPT_CTRL)
        )
        self.loop_supply_temperature_at_low_load[0] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.MAX_RESET_T)
        )
        self.flow_control[0] = self.determine_loop_flow_control()
        operation = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.LOOP_OPERATION
        )
        if operation == BDL_CirculationLoopOperationOptions.SCHEDULED:
            schedule = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.COOLING_SCHEDULE
            )
            if schedule and self.is_operation_schedule_continuous(schedule):
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.SCHEDULED
        elif operation == BDL_CirculationLoopOperationOptions.STANDBY:
            if self.is_loop_operation_continuous():
                self.operation[0] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[0] = FluidLoopOperationOptions.INTERMITTENT
        else:
            self.operation[0] = self.loop_operation_map.get(operation)
        self.heating_design_and_control["id"] = self.u_name + " HeatingDesign/Control"
        self.design_supply_temperature[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_HEAT_T)
        )
        if loop_design_dt is None:
            pass
        else:
            self.design_return_temperature[1] = (
                self.design_supply_temperature[1] - loop_design_dt
            )
        self.is_sized_using_coincident_load[1] = self.sizing_option_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.SIZING_OPTION)
        )
        self.minimum_flow_fraction[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.LOOP_MIN_FLOW)
        )
        self.temperature_reset_type[1] = self.temp_reset_map.get(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.HEAT_SETPT_CTRL)
        )
        self.loop_supply_temperature_at_low_load[1] = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.MIN_RESET_T)
        )
        self.flow_control[1] = self.determine_loop_flow_control()
        operation = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.LOOP_OPERATION
        )
        if operation == BDL_CirculationLoopOperationOptions.SCHEDULED:
            schedule = self.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.HEATING_SCHEDULE
            )
            if schedule and self.is_operation_schedule_continuous(schedule):
                self.operation[1] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[1] = FluidLoopOperationOptions.SCHEDULED
        elif operation == BDL_CirculationLoopOperationOptions.STANDBY:
            if self.is_loop_operation_continuous():
                self.operation[1] = FluidLoopOperationOptions.CONTINUOUS
            else:
                self.operation[1] = FluidLoopOperationOptions.INTERMITTENT
        else:
            self.operation[1] = self.loop_operation_map.get(operation)

    def populate_service_water_heating_distribution_system(self):
        self.swh_design_supply_temperature = self.try_float(
            self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DESIGN_HEAT_T)
        )
        inlet_t = self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.DHW_INLET_T)
        inlet_t_sch = self.keyword_value_pairs.get(
            BDL_CirculationLoopKeywords.DHW_INLET_T_SCH
        )
        if inlet_t is not None or inlet_t_sch is not None:
            self.is_ground_temperature_used_for_entering_water = False
        else:
            self.is_ground_temperature_used_for_entering_water = True

    def populate_service_water_piping(self):
        pass

    def populate_pump_data_elements(self, pump_name):
        pump = self.rmd.bdl_obj_instances.get(pump_name)
        if not pump:
            return

        pump.loop_or_piping = [self.u_name] * pump.qty
        for i in range(pump.qty):
            if pump.is_flow_sized_based_on_design_day[i]:
                # Override is_flow_sized_based_on_design_day if the circulation loop is not sized based on design loads
                pump.is_flow_sized_based_on_design_day[i] = (
                    self.keyword_value_pairs.get(
                        BDL_CirculationLoopKeywords.SIZING_OPTION
                    )
                    != BDL_CirculationLoopSizingOptions.PRIMARY
                )

    def determine_loop_flow_control(self):
        """Determine the flow control type for the circulation loop"""
        loop_type = self.keyword_value_pairs.get(BDL_CirculationLoopKeywords.TYPE)

        for circulation_loop_name in self.rmd.circulation_loop_names:
            circulation_loop = self.rmd.bdl_obj_instances.get(circulation_loop_name)
            primary_loop = circulation_loop.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.PRIMARY_LOOP
            )
            valve_type = circulation_loop.keyword_value_pairs.get(
                BDL_CirculationLoopKeywords.VALVE_TYPE_2ND
            )
            if (
                primary_loop == self.u_name
                and valve_type == BDL_SecondaryLoopValveTypes.TWO_WAY
            ):
                return FluidLoopFlowControlOptions.VARIABLE_FLOW

        for system_name in self.rmd.system_names:
            system = self.rmd.bdl_obj_instances.get(system_name)
            if loop_type == BDL_CirculationLoopTypes.CHW:
                cooling_loop = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.CHW_LOOP
                )
                valve_type = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.CHW_VALVE_TYPE
                )
                if (
                    cooling_loop == self.u_name
                    and valve_type == BDL_SystemCoolingValveTypes.TWO_WAY
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.HW:
                heating_loop = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.HW_LOOP
                )
                valve_type = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.HW_VALVE_TYPE
                )
                if (
                    heating_loop == self.u_name
                    and valve_type == BDL_SystemHeatingValveTypes.TWO_WAY
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.CW:
                pass
            elif loop_type == BDL_CirculationLoopTypes.PIPE2:
                cooling_loop = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.CHW_LOOP
                )
                heating_loop = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.HW_LOOP
                )
                cooling_valve_type = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.CHW_VALVE_TYPE
                )
                heating_valve_type = system.keyword_value_pairs.get(
                    BDL_SystemKeywords.HW_VALVE_TYPE
                )
                if (
                    cooling_loop == self.u_name
                    and cooling_valve_type == BDL_SystemCoolingValveTypes.TWO_WAY
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
                if (
                    heating_loop == self.u_name
                    and heating_valve_type == BDL_SystemHeatingValveTypes.TWO_WAY
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.WLHP:
                pass

        for zone_name in self.rmd.zone_names:
            zone = self.rmd.bdl_obj_instances.get(zone_name)
            if loop_type == BDL_CirculationLoopTypes.CHW:
                cooling_loop = zone.keyword_value_pairs.get(BDL_ZoneKeywords.CHW_LOOP)
                valve_type = zone.keyword_value_pairs.get(
                    BDL_ZoneKeywords.CHW_VALVE_TYPE
                )
                if (
                    cooling_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.HW:
                heating_loop = zone.keyword_value_pairs.get(BDL_ZoneKeywords.HW_LOOP)
                valve_type = zone.keyword_value_pairs.get(
                    BDL_ZoneKeywords.HW_VALVE_TYPE
                )
                if (
                    heating_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type in [
                BDL_CirculationLoopTypes.CW,
                BDL_CirculationLoopTypes.WLHP,
            ]:
                condensing_loop = zone.keyword_value_pairs.get(BDL_ZoneKeywords.CW_LOOP)
                has_valve = zone.keyword_value_pairs.get(BDL_ZoneKeywords.CW_VALVE)
                if (
                    condensing_loop == self.u_name
                    and has_valve == BDL_ZoneCondenserValveOptions.YES
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.PIPE2:
                heating_loop = zone.keyword_value_pairs.get(BDL_ZoneKeywords.HW_LOOP)
                cooling_loop = zone.keyword_value_pairs.get(BDL_ZoneKeywords.CHW_LOOP)
                heating_valve_type = zone.keyword_value_pairs.get(
                    BDL_ZoneKeywords.HW_VALVE_TYPE
                )
                cooling_valve_type = zone.keyword_value_pairs.get(
                    BDL_ZoneKeywords.CHW_VALVE_TYPE
                )
                if (
                    heating_loop == self.u_name
                    and heating_valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
                if (
                    cooling_loop == self.u_name
                    and cooling_valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW

        for chiller_name in self.rmd.chiller_names:
            chiller = self.rmd.bdl_obj_instances.get(chiller_name)
            if loop_type == BDL_CirculationLoopTypes.CHW:
                cooling_loop = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CHW_LOOP
                )
                valve_type = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CHW_FLOW_CTRL
                )
                if (
                    cooling_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.HW:
                heating_loop = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.HTREC_LOOP
                )
                valve_type = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.HTREC_FLOW_CTRL
                )
                if (
                    heating_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.CW:
                condensing_loop = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CW_LOOP
                )
                valve_type = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CW_FLOW_CTRL
                )
                if (
                    condensing_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.PIPE2:
                cooling_loop = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CHW_LOOP
                )
                heating_loop = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.HTREC_LOOP
                )
                cooling_valve_type = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.CHW_FLOW_CTRL
                )
                heating_valve_type = chiller.keyword_value_pairs.get(
                    BDL_ChillerKeywords.HTREC_FLOW_CTRL
                )
                if (
                    cooling_loop == self.u_name
                    and cooling_valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
                if (
                    heating_loop == self.u_name
                    and heating_valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW
            elif loop_type == BDL_CirculationLoopTypes.WLHP:
                pass  # Unused for chillers

        for boiler_name in self.rmd.boiler_names:
            boiler = self.rmd.bdl_obj_instances.get(boiler_name)

            if loop_type in [
                BDL_CirculationLoopTypes.CHW,
                BDL_CirculationLoopTypes.CW,
            ]:
                pass  # Unused for boilers
            elif loop_type in [
                BDL_CirculationLoopTypes.HW,
                BDL_CirculationLoopTypes.PIPE2,
                BDL_CirculationLoopTypes.WLHP,
            ]:
                heating_loop = boiler.keyword_value_pairs.get(
                    BDL_BoilerKeywords.HW_LOOP
                )
                valve_type = boiler.keyword_value_pairs.get(
                    BDL_BoilerKeywords.HW_FLOW_CTRL
                )
                if (
                    heating_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW

        for heat_rejection_name in self.rmd.heat_rejection_names:
            heat_rejection = self.rmd.bdl_obj_instances.get(heat_rejection_name)

            if loop_type in [
                BDL_CirculationLoopTypes.CHW,
                BDL_CirculationLoopTypes.HW,
                BDL_CirculationLoopTypes.PIPE2,
            ]:
                pass  # Unused for heat rejections

            elif loop_type in [
                BDL_CirculationLoopTypes.CW,
                BDL_CirculationLoopTypes.WLHP,
            ]:
                condensing_loop = heat_rejection.keyword_value_pairs.get(
                    BDL_HeatRejectionKeywords.CW_LOOP
                )
                valve_type = heat_rejection.keyword_value_pairs.get(
                    BDL_HeatRejectionKeywords.CW_FLOW_CTRL
                )
                if (
                    condensing_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW

        for ground_loop_hx_name in self.rmd.ground_loop_hx_names:
            ground_loop_hx = self.rmd.bdl_obj_instances.get(ground_loop_hx_name)

            if loop_type in [
                BDL_CirculationLoopTypes.CHW,
                BDL_CirculationLoopTypes.HW,
                BDL_CirculationLoopTypes.PIPE2,
            ]:
                pass  # Unused for ground loop heat exchangers
            elif loop_type in [
                BDL_CirculationLoopTypes.CW,
                BDL_CirculationLoopTypes.WLHP,
            ]:
                condensing_loop = ground_loop_hx.keyword_value_pairs.get(
                    BDL_GroundLoopHXKeywords.CIRCULATION_LOOP
                )
                valve_type = ground_loop_hx.keyword_value_pairs.get(
                    BDL_GroundLoopHXKeywords.HX_FLOW_CTRL
                )
                if (
                    condensing_loop == self.u_name
                    and valve_type == BDL_FlowControlOptions.VARIABLE_FLOW
                ):
                    return FluidLoopFlowControlOptions.VARIABLE_FLOW

        return FluidLoopFlowControlOptions.FIXED_FLOW

    def is_loop_operation_continuous(self):
        for system_name in self.rmd.system_names:
            system = self.rmd.bdl_obj_instances.get(system_name)
            system_fan_schedule = system.keyword_value_pairs.get(
                BDL_SystemKeywords.FAN_SCHEDULE
            )
            if system_fan_schedule:
                if self.is_operation_schedule_continuous(system_fan_schedule):
                    return True
        return False

    def is_operation_schedule_continuous(self, schedule_u_name):
        schedule = self.rmd.bdl_obj_instances.get(schedule_u_name)
        if schedule:
            hourly_values = schedule.hourly_values
            if hourly_values:
                # If hourly_values contains any 0 or -1, the system is not continuous
                return not any([x == 0 or x == -1 for x in hourly_values])
        else:
            raise ValueError(f"Schedule {schedule_u_name} not found in the RMD.")

    def get_hw_equipment_sequencing(self, equip_ctrl=None):
        default_staging_order = tuple(self.rmd.boiler_names)
        if not equip_ctrl:
            return default_staging_order

        sequence = []
        for i in range(1, 6):  # Loop through BOILERS_1 to BOILERS_5
            load_range_key = getattr(BDL_EquipCtrlKeywords, f"BOILERS_{i}")
            load_range_seq = equip_ctrl.keyword_value_pairs.get(load_range_key)

            if not load_range_seq:
                continue

            if not sequence:
                sequence = load_range_seq
                continue

            for j in range(len(load_range_seq)):
                if j >= len(
                    sequence
                ):  # Extend the sequence with any new boilers in the load range
                    sequence += (load_range_seq[j],)
                elif (
                    sequence[j] != load_range_seq[j]
                ):  # If any value differs, return an empty tuple
                    return ()

        if len(sequence) < len(default_staging_order):
            sequence += [
                boiler for boiler in default_staging_order if boiler not in sequence
            ]

        return sequence
