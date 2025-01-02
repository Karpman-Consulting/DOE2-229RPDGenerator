"""This module exports the dictionary bdl_enums that provides access to the
enumerations in the BDL files.

The keys of bdl_enums are the names of the enumeration objects; each value
is a class with an attribute for each item in the enumeration. The value
of the attribute is the same as the attribute name.
"""


class _ListEnum:
    """A utility class used to convert a list into a class

    Each item in the list must be a string and becomes a class attribute (hyphens replaced with underscores) where the value is the string.
    """

    def __init__(self, _list):
        for str_item in _list:
            item_key = (
                str_item.replace("-", "_")
                .replace("/", "_")
                .replace("&", "_")
                .replace("+", "_")
                .replace(" ", "_")
                .upper()
            )
            setattr(self, item_key, str_item)

    def get_list(self):
        return list(self.__dict__)


class BDLEnums:
    bdl_enums = {
        "Commands": _ListEnum(
            [
                "RUN-PERIOD-PD",
                "SITE-PARAMETERS",
                "MASTER-METERS",
                "FUEL-METER",
                "ELEC-METER",
                "STEAM-METER",
                "CHW-METER",
                "CURVE-FIT",
                "FIXED-SHADE",
                "GLASS-TYPE",
                "MATERIAL",
                "LAYERS",
                "CONSTRUCTION",
                "HOLIDAYS",
                "DAY-SCHEDULE-PD",
                "WEEK-SCHEDULE-PD",
                "SCHEDULE-PD",
                "PUMP",
                "CIRCULATION-LOOP",
                "BOILER",
                "CHILLER",
                "DW-HEATER",
                "HEAT-REJECTION",
                "GROUND-LOOP-HX",
                "FLOOR",
                "SYSTEM",
                "ZONE",
                "SPACE",
                "EXTERIOR-WALL",
                "INTERIOR-WALL",
                "UNDERGROUND-WALL",
                "WINDOW",
                "DOOR",
                "LOAD-MANAGEMENT",
                "EQUIP-CTRL",
                "DESIGN-DAY",
                "CONDENSING-UNIT",
                "ELEC-GENERATOR",
                "UTILITY-RATE",
            ]
        ),
        "FuelTypes": _ListEnum(
            [
                "ELECTRICITY",
                "NATURAL-GAS",
                "LPG",
                "FUEL-OIL",
                "DIESEL-OIL",
                "COAL",
                "METHANOL",
                "OTHER-FUEL",
            ]
        ),
        "WallLocationOptions": _ListEnum(
            [
                "TOP",
                "BOTTOM",
                "LEFT",
                "RIGHT",
                "FRONT",
                "BACK",
                *[f"SPACE-V{i}" for i in range(1, 121)],
            ]
        ),
        "BoilerTypes": _ListEnum(
            [
                "HW-BOILER",
                "HW-BOILER-W/DRAFT",
                "ELEC-HW-BOILER",
                "STM-BOILER",
                "STM-BOILER-W/DRAFT",
                "ELEC-STM-BOILER",
                "HW-CONDENSING",
            ]
        ),
        "BoilerKeywords": _ListEnum(
            [
                "TYPE",
                "HW-PUMP",
                "HW-LOOP",
                "FUEL-METER",
                "MIN-RATIO",
                "HW-FLOW-CTRL",
            ]
        ),
        "ChillerTypes": _ListEnum(
            [
                "ELEC-OPEN-CENT",
                "ELEC-OPEN-REC",
                "ELEC-HERM-CENT",
                "ELEC-HERM-REC",
                "ELEC-SCREW",
                "ELEC-HTREC",
                "ABSOR-1",
                "ABSOR-2",
                "GAS-ABSOR",
                "ENGINE",
                "HEAT-PUMP",
                "LOOP-TO-LOOP-HP",
                "WATER-ECONOMIZER",
                "STRAINER-CYCLE",
            ]
        ),
        "FlowControlOptions": _ListEnum(
            [
                "CONSTANT-FLOW",
                "VARIABLE-FLOW",
            ]
        ),
        "ChillerKeywords": _ListEnum(
            [
                "TYPE",
                "RATED-CHW-T",
                "RATED-COND-T",
                "DESIGN-CHW-T",
                "DESIGN-COND-T",
                "MIN-RATIO",
                "CHW-LOOP",
                "CW-LOOP",
                "HW-LOOP",
                "HTREC-LOOP",
                "CHW-PUMP",
                "CW-PUMP",
                "HW-PUMP",
                "HTREC-PUMP",
                "CHW-FLOW-CTRL",
                "CW-FLOW-CTRL",
                "HW-FLOW-CTRL",
                "HTREC-FLOW-CTRL",
            ]
        ),
        "CirculationLoopTypes": _ListEnum(
            [
                "CHW",
                "HW",
                "CW",
                "DHW",
                "PIPE2",
                "WLHP",
            ]
        ),
        "CirculationLoopSubtypes": _ListEnum(
            [
                "PRIMARY",
                "SECONDARY",
            ]
        ),
        "CirculationLoopSizingOptions": _ListEnum(
            [
                "COINCIDENT",
                "NON-COINCIDENT",
                "PRIMARY",
                "SECONDARY",
            ]
        ),
        "CirculationLoopOperationOptions": _ListEnum(
            [
                "STANDBY",
                "DEMAND",
                "SNAP",
                "SCHEDULED",
                "SUBHOUR-DEMAND",
            ]
        ),
        "CirculationLoopTemperatureResetOptions": _ListEnum(
            [
                "FIXED",
                "OA-RESET",
                "SCHEDULED",
                "LOAD-RESET",
                "WETBULB-RESET",
            ]
        ),
        "CirculationLoopSecondaryValveTypes": _ListEnum(
            [
                "TWO-WAY",
                "THREE-WAY",
            ]
        ),
        "CirculationLoopKeywords": _ListEnum(
            [
                "LOOP-PUMP",
                "LOOP-OPERATION",
                "TYPE",
                "SUBTYPE",
                "PRIMARY-LOOP",
                "VALVE-TYPE-2ND",
                "DESIGN-HEAT-T",
                "DESIGN-COOL-T",
                "LOOP-DESIGN-DT",
                "SIZING-OPTION",
                "LOOP-MIN-FLOW",
                "HEAT-SETPT-CTRL",
                "COOL-SETPT-CTRL",
                "HEAT-RESET-SCH",
                "COOL-RESET-SCH",
                "MIN-RESET-T",
                "MAX-RESET-T",
                "DHW-INLET-T",
                "DHW-INLET-T-SCH",
                "COOLING-SCHEDULE",
                "HEATING-SCHEDULE",
            ]
        ),
        "ConstructionTypes": _ListEnum(
            [
                "LAYERS",
                "U-VALUE",
            ]
        ),
        "ConstructionKeywords": _ListEnum(
            [
                "TYPE",
                "LAYERS",
                "ABSORPTANCE",
                "U-VALUE",
            ]
        ),
        "DayScheduleKeywords": _ListEnum(
            [
                "TYPE",
                "VALUES",
                "OUTSIDE-HI",
                "OUTSIDE-LO",
                "SUPPLY-HI",
                "SUPPLY-LO",
            ]
        ),
        "DOASAttachedToOptions": _ListEnum(
            [
                "AHU-MIXED-AIR",
                "CONDITIONED-ZONES",
            ]
        ),
        "DomesticWaterHeaterTypes": _ListEnum(
            [
                "GAS",
                "ELEC",
                "HEAT-PUMP",
            ]
        ),
        "DomesticWaterHeaterLocationOptions": _ListEnum(
            [
                "OUTDOOR",
                "ZONE",
            ]
        ),
        "DomesticWaterHeaterKeywords": _ListEnum(
            [
                "TYPE",
                "DHW-LOOP",
                "FUEL-METER",
                "LOCATION",
                "ZONE-NAME",
                "TANK-VOLUME",
                "AQUASTAT-SETPT-T",
                "DHW-LOOP",
                "ELEC-INPUT-RATIO",
                "HEAT-INPUT-RATIO",
            ]
        ),
        "DoorKeywords": _ListEnum(
            [
                "CONSTRUCTION",
                "HEIGHT",
                "WIDTH",
            ]
        ),
        "ExteriorWallKeywords": _ListEnum(
            [
                "AREA",
                "HEIGHT",
                "WIDTH",
                "LOCATION",
                "TILT",
                "AZIMUTH",
                "CONSTRUCTION",
                "SHADING-SURFACE",
                "OUTSIDE-EMISS",
                "INSIDE-SOL-ABS",
                "INSIDE-VIS-REFL",
            ]
        ),
        "ShadingSurfaceOptions": _ListEnum(
            [
                "YES",
                "NO",
            ]
        ),
        "FloorKeywords": _ListEnum(
            [
                "AZIMUTH",
            ]
        ),
        "GlassTypeOptions": _ListEnum(
            [
                "GLASS-TYPE-CODE",
                "SHADING-COEF",
            ]
        ),
        "GlassTypeKeywords": _ListEnum(
            [
                "TYPE",
                "GLASS-CONDUCT",
                "SHADING-COEF",
                "VIS-TRANS",
                "OUTSIDE-EMISS",
            ]
        ),
        "HeatRejectionTypes": _ListEnum(
            [
                "OPEN-TWR",
                "OPEN-TWR&HX",
                "FLUID-COOLER",
                "DRYCOOLER",
            ]
        ),
        "HeatRejectionFanSpeedControlOptions": _ListEnum(
            [
                "ONE-SPEED-FAN",
                "FLUID-BYPASS",
                "TWO-SPEED-FAN",
                "VARIABLE-SPEED-FAN",
                "DISCHARGE-DAMPER",
            ]
        ),
        "HeatRejectionKeywords": _ListEnum(
            [
                "CW-LOOP",
                "TYPE",
                "CW-PUMP",
                "CW-FLOW-CTRL",
                "CAPACITY-CTRL",
                "RATED-RANGE",
                "RATED-APPROACH",
                "DESIGN-WETBULB",
            ]
        ),
        "InteriorWallTypes": _ListEnum(
            [
                "STANDARD",
                "AIR",
                "ADIABATIC",
                "INTERNAL",
            ]
        ),
        "InteriorWallKeywords": _ListEnum(
            [
                "INT-WALL-TYPE",
                "NEXT-TO",
                "AREA",
                "HEIGHT",
                "WIDTH",
                "LOCATION",
                "TILT",
                "AZIMUTH",
                "CONSTRUCTION",
                "SHADING-SURFACE",
                "INSIDE-SOL-ABS",
                "INSIDE-VIS-REFL",
            ]
        ),
        "MaterialTypes": _ListEnum(
            [
                "PROPERTIES",
                "RESISTANCE",
            ]
        ),
        "MaterialKeywords": _ListEnum(
            [
                "TYPE",
                "THICKNESS",
                "CONDUCTIVITY",
                "DENSITY",
                "SPECIFIC-HEAT",
                "RESISTANCE",
            ]
        ),
        "LayerKeywords": _ListEnum(
            [
                "MATERIAL",
                "INSIDE-FILM-RES",
            ]
        ),
        "MasterMeterKeywords": _ListEnum(
            [
                "MSTR-ELEC-METER",
                "LIGHT-ELEC-METER",
                "TASK-ELEC-METER",
                "EQUIP-ELEC-METER",
                "SOURCE-ELEC-METER",
                "HEAT-ELEC-METER",
                "COOL-ELEC-METER",
                "HTREJ-ELEC-METER",
                "AUX-ELEC-METER",
                "VENT-ELEC-METER",
                "REFG-ELEC-METER",
                "SUPP-ELEC-METER",
                "DHW-ELEC-METER",
                "MSTR-FUEL-METER",
                "SOURCE-FUEL-METER",
                "HEAT-FUEL-METER",
                "COOL-FUEL-METER",
                "SUPP-FUEL-METER",
                "DHW-FUEL-METER",
                "EXCLUDE-FROM-TDV",
            ]
        ),
        "FuelMeterKeywords": _ListEnum(
            [
                "TYPE",
                "ENERGY/UNIT",
                "SOURCE-SITE-EFF",
                "UNIT-INDEX",
                "DEM-UNIT-INDEX",
            ]
        ),
        "AirflowConditionOptions": _ListEnum(
            [
                "SEA-LEVEL",
                "BLDG-ALTITUDE",
            ]
        ),
        "SiteParameterKeywords": _ListEnum(
            [
                "DAYLIGHT-SAVINGS",
                "GROUND-T",
                "SPECIFY-AIRFLOWS",
                "ALTITUDE",
                "LATITUDE",
                "LONGITUDE",
            ]
        ),
        "RunPeriodKeywords": _ListEnum(
            [
                "END-YEAR",
            ]
        ),
        "HolidayTypes": _ListEnum(
            [
                "OFFICIAL-US",
                "ALTERNATE",
            ]
        ),
        "HolidayKeywords": _ListEnum(
            [
                "TYPE",
                "MONTHS",
                "DAYS",
            ]
        ),
        "GroundLoopHXKeywords": _ListEnum(
            [
                "CIRCULATION-LOOP",
                "HX-FLOW-CTRL",
            ]
        ),
        "PumpCapacityControlOptions": _ListEnum(
            [
                "ONE-SPEED-PUMP",
                "TWO-SPEED-PUMP",
                "VAR-SPEED-PUMP",
            ]
        ),
        "PumpKeywords": _ListEnum(
            [
                "NUMBER",
                "PUMP-KW",
                "HEAD",
                "CAP-CTRL",
                "FLOW",
            ]
        ),
        "ScheduleTypes": _ListEnum(
            [
                "ON/OFF",
                "FRACTION",
                "MULTIPLIER",
                "TEMPERATURE",
                "RADIATION",
                "ON/OFF/TEMP",
                "ON/OFF/FLAG",
                "FRAC/DESIGN",
                "EXP-FRACTION",
                "FLAG",
                "RESET-TEMP",
                "RESET-RATIO",
            ]
        ),
        "ScheduleKeywords": _ListEnum(
            [
                "TYPE",
                "MONTH",
                "DAY",
                "WEEK-SCHEDULES",
            ]
        ),
        "InfiltrationAlgorithmOptions": _ListEnum(
            [
                "NONE",
                "AIR-CHANGE",
                "RESIDENTIAL",
                "S-G",
                "CRACK",
                "ASHRAE-ENHANCED",
            ]
        ),
        "InternalEnergySourceOptions": _ListEnum(
            [
                "GAS",
                "ELECTRIC",
                "HOT-WATER",
                "PROCESS",
            ]
        ),
        "SpaceKeywords": _ListEnum(
            [
                "AZIMUTH",
                "VOLUME",
                "AREA",
                "LIGHTING-SCHEDUL",
                "EQUIP-SCHEDULE",
                "SOURCE-SCHEDULE",
                "PEOPLE-SCHEDULE",
                "INF-SCHEDULE",
                "LIGHTING-W/AREA",
                "LIGHTING-KW",
                "EQUIPMENT-W/AREA",
                "EQUIPMENT-KW",
                "EQUIP-SENSIBLE",
                "EQUIP-LATENT",
                "SOURCE-TYPE",
                "SOURCE-POWER",
                "SOURCE-SENSIBLE",
                "SOURCE-LATENT",
                "NUMBER-OF-PEOPLE",
                "PEOPLE-HG-SENS",
                "PEOPLE-HG-LAT",
                "INF-METHOD",
                "INF-FLOW/AREA",
                "AIR-CHANGES/HR",
            ]
        ),
        "SteamAndChilledWaterMeterKeywords": _ListEnum(
            [
                "CIRCULATION-LOOP",
            ]
        ),
        "SystemHeatingTypes": _ListEnum(
            [
                "NONE",
                "ELECTRIC",
                "HOT-WATER",
                "FURNACE",
                "HEAT-PUMP",
                "CONDENSING-UNIT",
                "DHW-LOOP",
                "STEAM",
            ]
        ),
        "SystemHeatControlOptions": _ListEnum(
            [
                "CONSTANT",
                "WARMEST",
                "COLDEST",
                "RESET",
                "SCHEDULED",
            ]
        ),
        "SystemHeatingValveTypes": _ListEnum(
            [
                "TWO-WAY",
                "THREE-WAY",
            ]
        ),
        "SystemCoolingTypes": _ListEnum(
            [
                "ELEC-DX",
                "CHILLED-WATER",
                "NONE",
            ]
        ),
        "SystemCoolControlOptions": _ListEnum(
            [
                "CONSTANT",
                "WARMEST",
                "COLDEST",
                "RESET",
                "SCHEDULED",
            ]
        ),
        "SystemCoolingValveTypes": _ListEnum(
            [
                "TWO-WAY",
                "THREE-WAY",
            ]
        ),
        "SystemCondenserValveTypes": _ListEnum(
            [
                "YES",
                "NO",
            ]
        ),
        "SystemTypes": _ListEnum(
            [
                "SUM",
                "SZRH",
                "MZS",
                "DDS",
                "SZCI",
                "UVT",
                "UHT",
                "FC",
                "IU",
                "VAVS",
                "RHFS",
                "HP",
                "HVSYS",
                "RESYS",
                "CBVAV",
                "PSZ",
                "PMZS",
                "PVAVS",
                "PTAC",
                "PIU",
                "FNSYS",
                "PTGSD",
                "PVVT",
                "RESYS2",
                "RESVVT",
                "EVAP-COOL",
                "DOAS",
                "FNSYS",
                "PTGSD",
            ]
        ),
        "SystemFanControlOptions": _ListEnum(
            [
                "SPEED",
                "INLET",
                "DISCHARGE",
                "CYCLING",
                "TWO-SPEED",
                "CONSTANT-VOLUME",
                "FAN-EIR-FPLR",
            ]
        ),
        "SystemNightCycleControlOptions": _ListEnum(
            [
                "CYCLE-ON-ANY",
                "CYCLE-ON-FIRST",
                "STAY-OFF",
                "ZONE-FANS-ONLY",
            ]
        ),
        "SystemEconomizerOptions": _ListEnum(
            [
                "FIXED",
                "OA-TEMP",
                "OA-ENTHALPY",
                "DUAL-TEMP",
                "DUAL-ENTHALPY",
            ]
        ),
        "SystemEnergyRecoveryTypes": _ListEnum(
            [
                "SENSIBLE-HX",
                "ENTHALPY-HX",
                "SENSIBLE-WHEEL",
                "ENTHALPY-WHEEL",
                "HEAT-PIPE",
            ]
        ),
        "SystemEnergyRecoveryOptions": _ListEnum(
            [
                "NO",
                "RELIEF-ONLY",
                "EXHAUST-ONLY",
                "RELIEF+EXHAUST",
                "YES",
            ]
        ),
        "SystemEnergyRecoveryOperationOptions": _ListEnum(
            [
                "WHEN-FANS-ON",
                "WHEN-MIN-OA",
                "ERV-SCHEDULE",
                "OA-EXHAUST-DT",
                "OA-EXHAUST-DH",
            ]
        ),
        "SystemEnergyRecoveryTemperatureControlOptions": _ListEnum(
            [
                "FLOAT",
                "FIXED-SETPT",
                "MIXED-AIR-RESET",
            ]
        ),
        "SystemMinimumOutdoorAirControlOptions": _ListEnum(
            [
                "FRAC-OF-DESIGN-FLOW",
                "FRAC-OF-HOURLY-FLOW",
                "DCV-RETURN-SENSOR",
                "DCV-ZONE-SENSORS",
            ]
        ),
        "SystemHumidificationOptions": _ListEnum(
            [
                "NONE",
                "ELECTRIC",
                "HOT-WATER",
                "STEAM",
                "FURNACE",
                "HEAT-PUMP",
                "DHW-LOOP",
            ]
        ),
        "SystemDualDuctFanOptions": _ListEnum(
            [
                "SINGLE-FAN",
                "DUAL-FAN",
            ]
        ),
        "SystemReturnFanLocationOptions": _ListEnum(
            [
                "COMMON",
                "COLD-DECK-ONLY",
                "RELIEF",
            ]
        ),
        "ZoneOAMethodOptions": _ListEnum(
            [
                "MAX-OCC-OR-AREA",
                "SUM-OCC-AND-AREA",
            ]
        ),
        "SystemIndoorFanModeOptions": _ListEnum(
            [
                "CONTINUOUS",
                "INTERMITTENT",
            ]
        ),
        "SystemReturnAirPathOptions": _ListEnum(
            [
                "DIRECT",
                "DUCT",
                "PLENUM-ZONES",
            ]
        ),
        "SystemKeywords": _ListEnum(
            [
                "TYPE",
                "SIZING-RATIO",
                "HEAT-SOURCE",
                "HW-LOOP",
                "HW-VALVE-TYPE",
                "HEAT-CONTROL",
                "HEAT-SET-T",
                "HEAT-MIN-RESET-T",
                "HEAT-MAX-RESET-T",
                "HEAT-SIZING-RATI",
                "HEATING-CAPACITY",
                "COOL-SOURCE",
                "CHW-LOOP",
                "CW-LOOP",
                "CHW-VALVE-TYPE",
                "CW_VALVE",
                "COOL-CONTROL",
                "COOL-SET-T",
                "COOL-MIN-RESET-T",
                "COOL-MAX-RESET-T",
                "COOL-SIZING-RATI",
                "COOL-SH-CAP",
                "COOLING-CAPACITY",
                "PREHEAT-SOURCE",
                "PHW-LOOP",
                "PHW-VALVE-TYPE",
                "PREHEAT-CAPACITY",
                "PREHEAT-T",
                "DDS-TYPE",
                "FAN-CONTROL",
                "FAN-SCHEDULE",
                "INDOOR-FAN-MODE",
                "NIGHT-CYCLE-CTRL",
                "MIN-OA-METHOD",
                "MIN-AIR-SCH",
                "MIN-FLOW-RATIO",
                "SIZING-RATIO",
                "HEAT-SIZING-RATI",
                "COOL-SIZING-RATI",
                "HEATING-CAPACITY",
                "COOLING-CAPACITY",
                "HUMIDIFIER-TYPE",
                "PREHEAT-SOURCE",
                "PREHEAT-CAPACITY",
                "PREHEAT-T",
                "SUPPLY-FLOW",
                "SUPPLY-STATIC",
                "SUPPLY-MTR-EFF",
                "SUPPLY-MECH-EFF",
                "RETURN-FLOW",
                "RETURN-STATIC",
                "RETURN-MTR-EFF",
                "RETURN-MECH-EFF",
                "RETURN-AIR-PATH",
                "RETURN-KW/FLOW",
                "RETURN-FAN-LOC",
                "HSUPPLY-FLOW",
                "HSUPPLY-STATIC",
                "HSUPPLY-MTR-EFF",
                "HSUPPLY-MECH-EFF",
                "HSUPPLY-KW/FLOW",
                "OA-CONTROL",
                "DOA-SYSTEM",
                "DOAS-ATTACHED-TO",
                "ECONO-LIMIT-T",
                "ECONO-LOCKOUT",
                "RECOVER-EXHAUST",
                "ERV-RECOVER-TYPE",
                "ERV-RUN-CTRL",
                "ERV-TEMP-CTRL",
                "ERV-SENSIBLE-EFF",
                "ERV-LATENT-EFF",
                "ERV-OA-FLOW",
                "ERV-EXH-FLOW",
                "ZONE-HEAT-SOURCE",
                "BASEBOARD-SOURCE",
                "ZONE-OA-METHOD",
                "BBRD-LOOP",
                "HP-SUPP-SOURCE",
                "MAX-HP-SUPP-T",
                "MIN-HP-T",
                "INDUCTION-RATIO",
                "MAX-SUPPLY-T",
                "MIN-SUPPLY-T",
                "HEAT-FUEL-METER",
            ]
        ),
        "UndergroundWallKeywords": _ListEnum(
            [
                "AREA",
                "HEIGHT",
                "WIDTH",
                "LOCATION",
                "TILT",
                "AZIMUTH",
                "CONSTRUCTION",
                "SHADING-SURFACE",
                "INSIDE-SOL-ABS",
                "INSIDE-VIS-REFL",
            ]
        ),
        "WeekScheduleKeywords": _ListEnum(
            [
                "TYPE",
                "DAY-SCHEDULES",
            ]
        ),
        "WindowTypes": _ListEnum(
            [
                "STANDARD",
                "SKYLIGHT-FLAT",
                "SKYLIGHT-DOME",
                "SKYLIGHT-TUBULAR",
            ]
        ),
        "WindowShadeTypes": _ListEnum(
            [
                "MOVABLE-INTERIOR",
                "MOVABLE-EXTERIOR",
                "FIXED-INTERIOR",
                "FIXED-EXTERIOR",
            ]
        ),
        "WindowKeywords": _ListEnum(
            [
                "WINDOW-TYPE",
                "HEIGHT",
                "WIDTH",
                "FRAME-WIDTH",
                "FRAME-CONDUCT",
                "CURB-HEIGHT",
                "CURB-CONDUCT",
                "LOCATION",
                "GLASS-TYPE",
                "LEFT-FIN-D",
                "RIGHT-FIN-D",
                "OVERHANG-D",
                "SHADING-SCHEDULE",
                "WIN-SHADE-TYPE",
            ]
        ),
        "TerminalTypes": _ListEnum(
            [
                "SVAV",
                "SERIES-PIU",
                "PARALLEL-PIU",
                "TERMINAL-IU",
                "CEILING-IU",
                "DUAL-DUCT",
                "MULTIZONE",
                "SUBZONE",
            ]
        ),
        "ZoneHeatSourceOptions": _ListEnum(
            [
                "NONE",
                "ELECTRIC",
                "HOT-WATER",
                "FURNACE",
                "DHW-LOOP",
                "STEAM",
                "HEAT-PUMP",
            ]
        ),
        "MinFlowControlOptions": _ListEnum(
            [
                "FIXED/SCHEDULED",
                "DCV-RESET-UP",
                "DCV-RESET-DOWN",
                "DCV-RESET-UP/DOWN",
            ]
        ),
        "BaseboardControlOptions": _ListEnum(
            [
                "NONE",
                "THERMOSTATIC",
                "OUTDOOR-RESET",
            ]
        ),
        "ZoneFanRunOptions": _ListEnum(
            [
                "HEATING-ONLY",
                "HEATING/DEADBAND",
                "CONTINUOUS",
                "HEATING/COOLING",
            ]
        ),
        "ZoneCWValveOptions": _ListEnum(
            [
                "YES",
                "NO",
            ]
        ),
        "ZoneInductionSourceOptions": _ListEnum(
            [
                "ZONE-RECIRC",
                "RETURN-PLENUM",
                "RETURN-AIR",
                "SUPPLY-AIR",
            ]
        ),
        "ZoneFanControlOptions": _ListEnum(
            [
                "CONSTANT-VOLUME",
                "VARIABLE-VOLUME",
            ]
        ),
        "ZoneKeywords": _ListEnum(
            [
                "TERMINAL-TYPE",
                "ZONE-FAN-CTRL",
                "DESIGN-HEAT-T",
                "DESIGN-COOL-T",
                "HEATING-CAPACITY",
                "COOLING-CAPACITY",
                "MAX-HEAT-RATE",
                "MAX-COOL-RATE",
                "REHEAT-DELTA-T",
                "HEAT-TEMP-SCH",
                "COOL-TEMP-SCH",
                "EXHAUST-FAN-SCH",
                "HW-LOOP",
                "EXHAUST-FLOW",
                "BASEBOARD-CTRL",
                "BASEBOARD-RATING",
                "ASSIGNED-FLOW",
                "HASSIGNED-FLOW",
                "FLOW/AREA",
                "HFLOW/AREA",
                "AIR-CHANGES/HR",
                "HAIR-CHANGES/HR",
                "MIN-FLOW/AREA",
                "HMIN-FLOW/AREA",
                "MIN-FLOW-SCH",
                "CMIN-FLOW-SCH",
                "HMIN-FLOW-SCH",
                "MIN-FLOW-CTRL",
                "MIN-FLOW-RATIO",
                "MIN-FLOW/AREA",
                "OA-FLOW/PER",
                "OUTSIDE-AIR-FLOW",
                "OA-CHANGES",
                "OA-FLOW/AREA",
                "EXHAUST-STATIC",
                "EXHAUST-EFF",
                "EXHAUST-KW/FLOW",
                "MIN-AIR-SCH",
                "ZONE-FAN-FLOW",
                "ZONE-FAN-CTRL",
                "ZONE-FAN-RUN",
                "CHW-LOOP",
                "CW-LOOP",
                "WSE-LOOP",
                "HW-VALVE-TYPE",
                "CHW-VALVE-TYPE",
                "CW-VALVE",
                "WSE-VALVE-TYPE",
                "INDUCTION-RATIO",
                "INDUCED-AIR-SRC",
                "SPACE",
            ]
        ),
        "HPSupplementSourceOptions": _ListEnum(
            [
                "ELECTRIC",
                "HOT-WATER",
                "FURNACE",
            ]
        ),
        "EquipCtrlKeywords": _ListEnum(
            [
                "CIRCULATION-LOOP",
                "LOADS-THRU-1",
                "LOADS-THRU-2",
                "LOADS-THRU-3",
                "LOADS-THRU-4",
                "LOADS-THRU-5",
                "BOILERS-1",
                "BOILERS-2",
                "BOILERS-3",
                "BOILERS-4",
                "BOILERS-5",
                "CHILLERS-1",
                "CHILLERS-2",
                "CHILLERS-3",
                "CHILLERS-4",
                "CHILLERS-5",
                "DW-HEATERS-1",
                "DW-HEATERS-2",
                "DW-HEATERS-3",
                "DW-HEATERS-4",
                "DW-HEATERS-5",
                "HEAT-REJ-1",
                "HEAT-REJ-2",
                "HEAT-REJ-3",
                "HEAT-REJ-4",
                "HEAT-REJ-5",
                "GLHX-1",
                "GLHX-2",
                "GLHX-3",
                "GLHX-4",
                "GLHX-5",
            ]
        ),
        "ElecGeneratorKeywords": _ListEnum(
            [
                "TYPE",
                "ELEC-METER",
                "SURPLUS-METER",
                "CAPACITY",
                "PV-MODULE",
                "ELEC-INPUT-RATIO",
                "HEAT-INPUT-RATIO",
                "NUM-INVERTERS",
                "MOUNT-TYPE",
                "MOUNT-TILT",
                "MIN-TRACK-VOLTS",
                "MAX-TRACK-VOLTS",
            ]
        ),
        "ElecGeneratorTypes": _ListEnum(
            [
                "ENGINE-GENERATOR",
                "GAS-TURBINE-GENERATOR",
                "STEAM-TURBINE-GENERATOR",
                "PV-ARRAY",
            ]
        ),
        "UtilityRateKeywords": _ListEnum(
            [
                "TYPE",
                "ENERGY-CHG",
            ]
        ),
        "UtilityRateTypes": _ListEnum(
            [
                "STEAM",
                "CHILLED-WATER",
                "ELECTRICITY",
                "ELECTRIC-SALE",
                "NATURAL-GAS",
                "LPG",
                "FUEL-OIL",
                "DIESEL-OIL",
                "COAL",
                "METHANOL",
                "OTHER-FUEL",
            ]
        ),
        "OutputCoolingTypes": _ListEnum(
            [
                "chilled water",
                "DX air cooled",
                "DX water cooled",
                "VRF",
            ]
        ),
        "OutputHeatingTypes": _ListEnum(
            [
                "hot water",
                "furnace",
                "electric",
                "heat pump air cooled",
                "heat pump water cooled",
                "VRF",
            ]
        ),
    }


def print_schema_enums():
    """Print all the schema enumerations with their names and values

    This is primarily useful for debugging purposes
    """

    for key in BDLEnums.bdl_enums:
        print(f"{key}:")
        for e in BDLEnums.bdl_enums[key].get_list():
            print(f"    {e}")
        print()


if __name__ == "__main__":
    print_schema_enums()
