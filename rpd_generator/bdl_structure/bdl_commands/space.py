from rpd_generator.bdl_structure.parent_node import ParentNode
from rpd_generator.bdl_structure.child_node import ChildNode
from rpd_generator.schema.schema_enums import SchemaEnums
from rpd_generator.bdl_structure.bdl_enumerations.bdl_enums import BDLEnums


EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
InfiltrationMethodOptions = SchemaEnums.schema_enums["InfiltrationMethodOptions"]
BDL_Commands = BDLEnums.bdl_enums["Commands"]
BDL_SpaceKeywords = BDLEnums.bdl_enums["SpaceKeywords"]
BDL_InfiltrationAlgorithmOptions = BDLEnums.bdl_enums["InfiltrationAlgorithmOptions"]
BDL_InternalEnergySourceOptions = BDLEnums.bdl_enums["InternalEnergySourceOptions"]


class Space(ChildNode, ParentNode):
    """Space object in the tree."""

    bdl_command = BDL_Commands.SPACE

    infiltration_algorithm_map = {
        BDL_InfiltrationAlgorithmOptions.NONE: "None",
        BDL_InfiltrationAlgorithmOptions.AIR_CHANGE: "Air Change Method",
        BDL_InfiltrationAlgorithmOptions.RESIDENTIAL: "Residential Infiltration Coefficient",
        BDL_InfiltrationAlgorithmOptions.S_G: "Sherman-Grimsrud Infiltration Method",
        BDL_InfiltrationAlgorithmOptions.CRACK: "Crack Method",
        BDL_InfiltrationAlgorithmOptions.ASHRAE_ENHANCED: "2005 ASHRAE Handbook Fundamentals - Enhanced Infiltration Method",
    }

    energy_source_map = {
        BDL_InternalEnergySourceOptions.GAS: EnergySourceOptions.NATURAL_GAS,
        BDL_InternalEnergySourceOptions.ELECTRIC: EnergySourceOptions.ELECTRICITY,
        BDL_InternalEnergySourceOptions.HOT_WATER: EnergySourceOptions.NONE,
        BDL_InternalEnergySourceOptions.PROCESS: EnergySourceOptions.NONE,
    }

    def __init__(self, u_name, parent, rmd):
        super().__init__(u_name, parent, rmd)
        ParentNode.__init__(self, u_name, rmd)
        self.rmd.bdl_obj_instances[u_name] = self

        self.space_data_structure = {}
        self.zone = None

        # data elements with children
        self.interior_lighting = []
        self.miscellaneous_equipment = []
        self.service_water_heating_uses = []

        # data elements with no children
        self.floor_area = None
        self.number_of_occupants = None
        self.occupant_multiplier_schedule = None
        self.occupant_sensible_heat_gain = None
        self.occupant_latent_heat_gain = None
        self.status_type = None
        self.function = None
        self.envelope_space_type = None
        self.lighting_space_type = None
        self.ventilation_space_type = None
        self.service_water_heating_space_type = None

        # InteriorLighting data elements
        self.int_ltg_id = [None]
        self.int_ltg_reporting_name = [None]
        self.int_ltg_notes = [None]
        self.int_ltg_purpose_type = [None]
        self.int_ltg_power_per_area = [None]
        self.int_ltg_lighting_multiplier_schedule = [None]
        self.int_ltg_occupancy_control_type = [None]
        self.int_ltg_daylighting_control_type = [None]
        self.int_ltg_are_schedules_used_for_modeling_occupancy_control = [None]
        self.int_ltg_are_schedules_used_for_modeling_daylighting_control = [None]

        # MiscellaneousEquipment data elements
        self.misc_eq_id = [None]
        self.misc_eq_reporting_name = [None]
        self.misc_eq_notes = [None]
        self.misc_eq_energy_type = [None]
        self.misc_eq_power = [None]
        self.misc_eq_multiplier_schedule = [None]
        self.misc_eq_sensible_fraction = [None]
        self.misc_eq_latent_fraction = [None]
        self.misc_eq_remaining_fraction_to_loop = [None]
        self.misc_eq_energy_from_loop = [None]
        self.misc_eq_type = [None]
        self.misc_eq_has_automatic_control = [None]

    def __repr__(self):
        return f"Space(u_name='{self.u_name}', parent={self.parent})"

    def populate_data_elements(self):
        """Populate data elements that originate from eQUEST's SPACE command"""
        # Establish zone and populate the zone volume and space floor area first to use in other data elements
        self.zone = self.rmd.space_map.get(self.u_name)
        volume = self.get_inp(BDL_SpaceKeywords.VOLUME)
        if volume is not None:
            volume = self.try_float(volume)
            self.zone.volume = volume
        self.floor_area = self.try_float(self.get_inp(BDL_SpaceKeywords.AREA))

        # Populate interior lighting data elements
        space_ltg_scheds = self.get_inp(BDL_SpaceKeywords.LIGHTING_SCHEDUL)
        self.standardize_dict_values(
            self.keyword_value_pairs,
            [BDL_SpaceKeywords.LIGHTING_W_AREA, BDL_SpaceKeywords.LIGHTING_KW],
            self.try_length(space_ltg_scheds),
        )

        if not isinstance(space_ltg_scheds, list):
            space_ltg_scheds = [space_ltg_scheds]
        for i, sched in enumerate(space_ltg_scheds):
            self.populate_interior_lighting(i, sched)

        # Populate miscellaneous equipment data elements
        space_misc_eq_scheds = self.get_inp(BDL_SpaceKeywords.EQUIP_SCHEDULE)
        self.standardize_dict_values(
            self.keyword_value_pairs,
            [
                BDL_SpaceKeywords.EQUIPMENT_W_AREA,
                BDL_SpaceKeywords.EQUIPMENT_KW,
                BDL_SpaceKeywords.EQUIP_SENSIBLE,
                BDL_SpaceKeywords.EQUIP_LATENT,
            ],
            self.try_length(space_misc_eq_scheds),
        )

        space_int_energy_source_scheds = self.get_inp(BDL_SpaceKeywords.SOURCE_SCHEDULE)
        if space_int_energy_source_scheds is not None:
            self.standardize_dict_values(
                self.keyword_value_pairs,
                [
                    BDL_SpaceKeywords.SOURCE_TYPE,
                    BDL_SpaceKeywords.SOURCE_POWER,
                    BDL_SpaceKeywords.SOURCE_KW,
                    BDL_SpaceKeywords.SOURCE_SENSIBLE,
                    BDL_SpaceKeywords.SOURCE_LATENT,
                ],
                self.try_length(space_int_energy_source_scheds),
            )
        else:
            space_int_energy_source_scheds = []

        if not isinstance(space_misc_eq_scheds, list):
            space_misc_eq_scheds = [space_misc_eq_scheds]

        if not isinstance(space_int_energy_source_scheds, list):
            space_int_energy_source_scheds = [space_int_energy_source_scheds]

        # Populate one instance of miscellaneous equipment for each schedule associated with equipment or internal energy sources
        misc_eq_counter = 0
        for i, sched in enumerate(space_misc_eq_scheds):
            misc_eq_counter += 1
            self.populate_miscellaneous_equipment(
                i, misc_eq_counter, sched, "EQUIPMENT"
            )

        for i, sched in enumerate(space_int_energy_source_scheds):
            misc_eq_counter += 1
            self.populate_miscellaneous_equipment(
                i, misc_eq_counter, sched, "INTERNAL_ENERGY_SOURCE"
            )

        # Populate the corresponding zone volume and infiltration from the DOE-2 SPACE command
        self.populate_zone_infiltration()

        # Populate space data elements
        self.number_of_occupants = self.try_float(
            self.get_inp(BDL_SpaceKeywords.NUMBER_OF_PEOPLE)
        )

        self.occupant_multiplier_schedule = self.get_inp(
            BDL_SpaceKeywords.PEOPLE_SCHEDULE
        )

        self.occupant_sensible_heat_gain = self.get_inp(
            BDL_SpaceKeywords.PEOPLE_HG_SENS
        )

        self.occupant_sensible_heat_gain = self.try_float(
            self.occupant_sensible_heat_gain
        )

        self.occupant_latent_heat_gain = self.get_inp(BDL_SpaceKeywords.PEOPLE_HG_LAT)

        self.occupant_latent_heat_gain = self.try_float(self.occupant_latent_heat_gain)

    def populate_data_group(self):
        """Populate schema structure for space object."""
        self.interior_lighting = self.populate_data_group_with_prefix("int_ltg_")
        self.miscellaneous_equipment = self.populate_data_group_with_prefix("misc_eq_")

        self.space_data_structure = {
            "id": self.u_name,
            "interior_lighting": self.interior_lighting,
            "miscellaneous_equipment": self.miscellaneous_equipment,
            "service_water_heating_uses": self.service_water_heating_uses,
        }

        no_children_attributes = [
            "reporting_name",
            "notes",
            "floor_area",
            "number_of_occupants",
            "occupant_multiplier_schedule",
            "occupant_sensible_heat_gain",
            "occupant_latent_heat_gain",
            "status_type",
            "function",
            "envelope_space_type",
            "lighting_space_type",
            "ventilation_space_type",
            "service_water_heating_space_type",
        ]

        # Iterate over the no_children_attributes list and populate if the value is not None
        for attr in no_children_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                self.space_data_structure[attr] = value

    def insert_to_rpd(self, rmd):
        """Insert space object into the rpd data structure."""
        # find the zone that has the "SPACE" attribute value equal to the space object's u_name
        self.zone.spaces.append(self.space_data_structure)

    def populate_interior_lighting(self, n, schedule):
        """Populate interior lighting data elements for an instance of InteriorLighting"""
        int_ltg_id = f"{self.u_name} IntLtg{n}"
        int_ltg_lpd = self.try_float(
            self.try_access_index(self.get_inp(BDL_SpaceKeywords.LIGHTING_W_AREA), n)
        )
        int_ltg_power = self.try_float(
            self.try_access_index(self.get_inp(BDL_SpaceKeywords.LIGHTING_KW), n)
        )
        total_lpd = (
            int_ltg_lpd + int_ltg_power * 1000 / self.floor_area
            if int_ltg_lpd is not None
            and int_ltg_power is not None
            and self.floor_area is not None
            else int_ltg_lpd
        )
        int_ltg_lighting_multiplier_schedule = schedule

        if n == 0:
            self.int_ltg_id = [int_ltg_id]
            self.int_ltg_power_per_area = [total_lpd]
            self.int_ltg_lighting_multiplier_schedule = [
                int_ltg_lighting_multiplier_schedule
            ]
        else:
            self.int_ltg_id.append(int_ltg_id)
            self.int_ltg_power_per_area.append(total_lpd)
            self.int_ltg_lighting_multiplier_schedule.append(
                int_ltg_lighting_multiplier_schedule
            )

            # Lists must be the same length, even when elements are not populated
            self.int_ltg_reporting_name.append(None)
            self.int_ltg_notes.append(None)
            self.int_ltg_purpose_type.append(None)
            self.int_ltg_occupancy_control_type.append(None)
            self.int_ltg_daylighting_control_type.append(None)
            self.int_ltg_are_schedules_used_for_modeling_occupancy_control.append(None)
            self.int_ltg_are_schedules_used_for_modeling_daylighting_control.append(
                None
            )

    def populate_miscellaneous_equipment(self, i, n, schedule, equip_type):
        """Populate miscellaneous equipment data elements for an instance of MiscellaneousEquipment"""
        misc_eq_id = f"{self.u_name} MiscEqp{n}"

        if equip_type == "EQUIPMENT":
            misc_epd = self.try_float(
                self.try_access_index(
                    self.get_inp(BDL_SpaceKeywords.EQUIPMENT_W_AREA),
                    i,
                )
            )
            misc_eq_power = self.try_float(
                self.try_access_index(self.get_inp(BDL_SpaceKeywords.EQUIPMENT_KW), i)
            )
            total_eq_power = (
                misc_eq_power + misc_epd * self.floor_area / 1000
                if misc_eq_power is not None
                and misc_epd is not None
                and self.floor_area is not None
                else misc_eq_power
            )
            misc_eq_multiplier_schedule = schedule
            misc_eq_sensible_fraction = self.try_float(
                self.try_access_index(
                    self.get_inp(BDL_SpaceKeywords.EQUIP_SENSIBLE),
                    i,
                )
            )
            misc_eq_latent_fraction = self.try_float(
                self.try_access_index(self.get_inp(BDL_SpaceKeywords.EQUIP_LATENT), i)
            )

            if n == 1:
                self.misc_eq_id = [misc_eq_id]
                self.misc_eq_energy_type = [EnergySourceOptions.ELECTRICITY]
                self.misc_eq_power = [total_eq_power]
                self.misc_eq_multiplier_schedule = [misc_eq_multiplier_schedule]
                self.misc_eq_sensible_fraction = [misc_eq_sensible_fraction]
                self.misc_eq_latent_fraction = [misc_eq_latent_fraction]
            else:
                self.misc_eq_id.append(misc_eq_id)
                self.misc_eq_energy_type.append(EnergySourceOptions.ELECTRICITY)
                self.misc_eq_power.append(total_eq_power)
                self.misc_eq_multiplier_schedule.append(misc_eq_multiplier_schedule)
                self.misc_eq_sensible_fraction.append(misc_eq_sensible_fraction)
                self.misc_eq_latent_fraction.append(misc_eq_latent_fraction)

                # Lists must be the same length, even when elements are not populated
                self.misc_eq_reporting_name.append(None)
                self.misc_eq_notes.append(None)
                self.misc_eq_remaining_fraction_to_loop.append(None)
                self.misc_eq_energy_from_loop.append(None)
                self.misc_eq_type.append(None)
                self.misc_eq_has_automatic_control.append(None)

        elif equip_type == "INTERNAL_ENERGY_SOURCE":
            source = self.try_access_index(
                self.get_inp(BDL_SpaceKeywords.SOURCE_TYPE), i
            )
            energy_type = self.energy_source_map.get(source)

            if n == 1:
                self.misc_eq_id = [misc_eq_id]
                self.misc_eq_energy_type = [energy_type]
            else:
                self.misc_eq_id.append(misc_eq_id)
                self.misc_eq_energy_type.append(energy_type)

                # Lists must be the same length, even when elements are not populated
                self.misc_eq_reporting_name.append(None)
                self.misc_eq_notes.append(None)
                self.misc_eq_power.append(None)
                self.misc_eq_multiplier_schedule.append(None)
                self.misc_eq_sensible_fraction.append(None)
                self.misc_eq_latent_fraction.append(None)
                self.misc_eq_remaining_fraction_to_loop.append(None)
                self.misc_eq_energy_from_loop.append(None)
                self.misc_eq_type.append(None)
                self.misc_eq_has_automatic_control.append(None)

    def populate_zone_infiltration(self):
        """Populate infiltration data elements for the zone object."""
        self.zone.infil_id = self.u_name + " Infil"
        self.zone.infil_multiplier_schedule = self.get_inp(
            BDL_SpaceKeywords.INF_SCHEDULE
        )
        infiltration_method = self.get_inp(BDL_SpaceKeywords.INF_METHOD)
        self.zone.infil_algorithm_name = self.infiltration_algorithm_map.get(
            infiltration_method
        )
        if infiltration_method == BDL_InfiltrationAlgorithmOptions.AIR_CHANGE:
            flow_per_area = self.try_float(
                self.get_inp(BDL_SpaceKeywords.INF_FLOW_AREA)
            )
            air_changes_per_hour = self.try_float(
                self.get_inp(BDL_SpaceKeywords.AIR_CHANGES_HR)
            )
            if (
                flow_per_area
                and air_changes_per_hour
                and self.zone.volume
                and self.floor_area
            ):
                self.zone.infil_flow_rate = (
                    flow_per_area * self.floor_area
                    + air_changes_per_hour * self.zone.volume / 60
                )
                self.zone.infil_modeling_method = (
                    InfiltrationMethodOptions.WEATHER_DRIVEN
                )
            elif flow_per_area and self.floor_area:
                self.zone.infil_flow_rate = flow_per_area * self.floor_area
                if self.zone.infil_multiplier_schedule:
                    self.zone.infil_modeling_method = (
                        InfiltrationMethodOptions.CONSTANT_SCHEDULED
                    )
                else:
                    self.zone.infil_modeling_method = InfiltrationMethodOptions.CONSTANT
            elif air_changes_per_hour and self.zone.volume:
                self.zone.infil_flow_rate = air_changes_per_hour * self.zone.volume / 60
                self.zone.infil_modeling_method = (
                    InfiltrationMethodOptions.WEATHER_DRIVEN
                )
        else:
            # infil_flow_rate will not populate if the infiltration method is not AIR-CHANGE
            self.zone.infil_modeling_method = InfiltrationMethodOptions.WEATHER_DRIVEN
