from rpd_generator.bdl_structure.base_node import BaseNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums

BoilerCombustionOptions = SchemaEnums.schema_enums["BoilerCombustionOptions"]
EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
BoilerEfficiencyMetricOptions = SchemaEnums.schema_enums[
    "BoilerEfficiencyMetricOptions"
]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_BoilerKeywords = BDLEnums.bdl_enums["BoilerKeywords"]
BDL_BoilerTypes = BDLEnums.bdl_enums["BoilerTypes"]
BDL_FuelTypes = BDLEnums.bdl_enums["FuelTypes"]
BDL_MasterMeterKeywords = BDLEnums.bdl_enums["MasterMeterKeywords"]
BDL_FuelMeterKeywords = BDLEnums.bdl_enums["FuelMeterKeywords"]
BDL_EquipCtrlKeywords = BDLEnums.bdl_enums["EquipCtrlKeywords"]


class Boiler(BaseNode):
    """Boiler object in the tree."""

    bdl_command = BDL_Commands.BOILER

    draft_type_map = {
        BDL_BoilerTypes.HW_BOILER: BoilerCombustionOptions.NATURAL,
        BDL_BoilerTypes.HW_BOILER_W_DRAFT: BoilerCombustionOptions.FORCED,
        BDL_BoilerTypes.ELEC_HW_BOILER: BoilerCombustionOptions.NATURAL,
        BDL_BoilerTypes.STM_BOILER: BoilerCombustionOptions.NATURAL,
        BDL_BoilerTypes.STM_BOILER_W_DRAFT: BoilerCombustionOptions.FORCED,
        BDL_BoilerTypes.ELEC_STM_BOILER: BoilerCombustionOptions.NATURAL,
        BDL_BoilerTypes.HW_CONDENSING: BoilerCombustionOptions.FORCED,
    }
    energy_source_map = {
        BDL_BoilerTypes.HW_BOILER: None,
        BDL_BoilerTypes.HW_BOILER_W_DRAFT: None,
        BDL_BoilerTypes.ELEC_HW_BOILER: EnergySourceOptions.ELECTRICITY,
        BDL_BoilerTypes.STM_BOILER: None,
        BDL_BoilerTypes.STM_BOILER_W_DRAFT: None,
        BDL_BoilerTypes.ELEC_STM_BOILER: EnergySourceOptions.ELECTRICITY,
        BDL_BoilerTypes.HW_CONDENSING: None,
    }

    def __init__(self, u_name, rmd):
        super().__init__(u_name, rmd)
        self.rmd.boiler_names.append(u_name)

        self.boiler_data_structure = {}

        # data elements with children
        self.output_validation_points = []
        self.efficiency_metrics = []
        self.efficiency = []

        # data elements with no children
        self.loop = None
        self.design_capacity = None
        self.rated_capacity = None
        self.minimum_load_ratio = None
        self.draft_type = None
        self.energy_source_type = None
        self.auxiliary_power = None
        self.operation_lower_limit = None
        self.operation_upper_limit = None

    def __repr__(self):
        return f"Boiler(u_name='{self.u_name}')"

    def populate_data_elements(self):
        """Populate data elements for boiler object."""
        fuel_meter = self.get_obj(self.get_inp(BDL_BoilerKeywords.FUEL_METER))
        fuel_type = None
        if fuel_meter is None:
            master_meters = self.get_obj(self.rmd.master_meters)
            if master_meters:
                heat_fuel_meter = self.get_obj(
                    master_meters.get_inp(BDL_MasterMeterKeywords.HEAT_FUEL_METER)
                )
                if heat_fuel_meter:
                    fuel_type = heat_fuel_meter.fuel_type

        else:
            fuel_type = fuel_meter.fuel_type

        self.energy_source_map.update(
            {
                BDL_BoilerTypes.HW_BOILER: fuel_type,
                BDL_BoilerTypes.HW_BOILER_W_DRAFT: fuel_type,
                BDL_BoilerTypes.STM_BOILER: fuel_type,
                BDL_BoilerTypes.STM_BOILER_W_DRAFT: fuel_type,
                BDL_BoilerTypes.HW_CONDENSING: fuel_type,
            }
        )

        self.loop = self.get_inp(BDL_BoilerKeywords.HW_LOOP)

        self.energy_source_type = self.energy_source_map.get(
            self.get_inp(BDL_BoilerKeywords.TYPE)
        )

        self.draft_type = self.draft_type_map.get(self.get_inp(BDL_BoilerKeywords.TYPE))
        self.minimum_load_ratio = self.try_float(
            self.get_inp(BDL_BoilerKeywords.MIN_RATIO)
        )

        requests = self.get_output_requests()
        output_data = self.get_output_data(requests)
        for key in [
            "Boilers - Design Parameters - Capacity",
            "Boilers - Rated Capacity at Peak (Btu/hr)",
        ]:
            if key in output_data:
                output_data[key] = self.try_convert_units(
                    output_data[key], "Btu/hr", "MMBtu/hr"
                )

        if not self.rated_capacity:
            self.rated_capacity = self.try_abs(
                output_data.get("Boilers - Rated Capacity at Peak (Btu/hr)")
            )
        self.design_capacity = self.try_abs(
            output_data.get("Boilers - Design Parameters - Capacity")
        )
        self.populate_operation_limits()
        self.auxiliary_power = output_data.get(
            "Boilers - Design Parameters - Auxiliary Power"
        )
        if self.energy_source_type == EnergySourceOptions.ELECTRICITY:
            boiler_e_i_r = output_data.get(
                "Boilers - Design Parameters - Electric Input Ratio"
            )
            if boiler_e_i_r:
                self.efficiency.append(1 / boiler_e_i_r)
                self.efficiency_metrics.append(BoilerEfficiencyMetricOptions.THERMAL)
            if boiler_e_i_r and boiler_e_i_r == 1:
                self.efficiency.extend([1, 1])
                self.efficiency_metrics.extend(
                    [
                        BoilerEfficiencyMetricOptions.COMBUSTION,
                        BoilerEfficiencyMetricOptions.ANNUAL_FUEL_UTILIZATION,
                    ]
                )

        else:
            boiler_f_i_r = output_data.get(
                "Boilers - Design Parameters - Fuel Input Ratio"
            )
            if boiler_f_i_r:
                self.efficiency.append(1 / boiler_f_i_r)
                self.efficiency_metrics.append(BoilerEfficiencyMetricOptions.THERMAL)
                self.efficiency.append(1 / boiler_f_i_r + 0.02)
                self.efficiency_metrics.append(BoilerEfficiencyMetricOptions.COMBUSTION)
                # EQUATIONS DERIVED FROM PRM REFERENCE MANUAL
                if 0.825 > self.efficiency[0] > 0.8:
                    self.efficiency.append((self.efficiency[0] - 0.725) / 0.1)
                    self.efficiency_metrics.append(
                        BoilerEfficiencyMetricOptions.ANNUAL_FUEL_UTILIZATION
                    )
                elif 0.825 <= self.efficiency[0] <= 0.98:
                    self.efficiency.append((self.efficiency[0] - 0.105) / 0.875)
                    self.efficiency_metrics.append(
                        BoilerEfficiencyMetricOptions.ANNUAL_FUEL_UTILIZATION
                    )

        # Assign pump data elements populated from the boiler keyword value pairs
        pump = self.get_obj(self.get_inp(BDL_BoilerKeywords.HW_PUMP))
        if pump:
            pump.loop_or_piping = [self.loop] * pump.qty

    def get_output_requests(self):
        """Get the output requests for the boiler object."""

        requests = {
            "Boilers - Design Parameters - Capacity": (
                2315003,
                self.u_name,
                "",
            ),
            "Boilers - Design Parameters - Flow": (
                2315004,
                self.u_name,
                "",
            ),
            "Boilers - Design Parameters - Electric Input Ratio": (
                2315005,
                self.u_name,
                "",
            ),
            "Boilers - Design Parameters - Fuel Input Ratio": (
                2315006,
                self.u_name,
                "",
            ),
            "Boilers - Design Parameters - Auxiliary Power": (
                2315007,
                self.u_name,
                "",
            ),
        }

        if not self.rated_capacity:
            requests["Boilers - Rated Capacity at Peak (Btu/hr)"] = (
                2315901,
                self.u_name,
                "",
            )

        return requests

    def populate_data_group(self):
        """Populate schema structure for boiler object."""
        self.boiler_data_structure = {
            "id": self.u_name,
            "efficiency": self.efficiency,
            "efficiency_metrics": self.efficiency_metrics,
            "output_validation_points": self.output_validation_points,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "loop",
            "design_capacity",
            "rated_capacity",
            "minimum_load_ratio",
            "draft_type",
            "energy_source_type",
            "auxiliary_power",
            "operation_lower_limit",
            "operation_upper_limit",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.boiler_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        rmd.boilers.append(self.boiler_data_structure)

    def populate_operation_limits(self):
        requests = {}
        boiler_capacities = {}
        for boiler_name in self.rmd.boiler_names:
            boiler = self.get_obj(boiler_name)
            if boiler.rated_capacity:  # boiler is gauranteed to exist
                boiler_capacities[boiler_name] = boiler.rated_capacity
            else:
                requests[boiler_name] = (
                    2315901,
                    boiler_name,
                    "",
                )
        output_data = self.get_output_data(requests)
        for boiler_name, capacity in boiler_capacities.items():
            boiler_capacities[boiler_name] = self.try_abs(
                self.try_convert_units(capacity, "Btu/hr", "MMBtu/hr")
            )
            boiler = self.get_obj(boiler_name)
            boiler.rated_capacity = boiler_capacities[boiler_name]

        hw_loop_equip_ctrls = []
        for equip_ctrl_name in self.rmd.equip_ctrl_names:
            equip_ctrl = self.get_obj(equip_ctrl_name)
            if equip_ctrl.get_inp(BDL_EquipCtrlKeywords.CIRCULATION_LOOP) == self.loop:
                hw_loop_equip_ctrls.append(equip_ctrl)

        if len(hw_loop_equip_ctrls) > 1:
            return

        sequence = []
        if len(hw_loop_equip_ctrls) == 1:
            equip_ctrl = hw_loop_equip_ctrls[0]
            hw_loop = self.get_obj(self.loop)
            sequence = hw_loop.get_hw_equipment_sequencing(equip_ctrl)

        if len(hw_loop_equip_ctrls) == 0:
            hw_loop = self.get_obj(self.loop)
            sequence = hw_loop.get_hw_equipment_sequencing()

        operation_lower_limit = 0
        for boiler_name in sequence:
            if boiler_name == self.u_name:
                self.operation_lower_limit = operation_lower_limit
                self.operation_upper_limit = (
                    operation_lower_limit + boiler_capacities[self.u_name]
                )
                return
            if boiler_name != self.u_name:
                operation_lower_limit += boiler_capacities[boiler_name]
