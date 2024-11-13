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
        "ChillerKeywords": _ListEnum(
            [
                "TYPE",
                "CHW-LOOP",
                "CW-LOOP",
                "HTREC-LOOP",
                "RATED-CHW-T",
                "RATED-COND-T",
                "DESIGN-CHW-T",
                "DESIGN-COND-T",
                "CHW-PUMP",
                "CW-PUMP",
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
                "DEMAND-ONLY",
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
        "CirculationLoopKeywords": _ListEnum(
            [
                "LOOP-PUMP",
                "TYPE",
                "SUBTYPE",
                "PRIMARY-LOOP",
                "DESIGN-HEAT-T",
                "DESIGN-COOL-T",
                "LOOP-DESIGN-DT",
                "SIZING-OPTION",
                "LOOP-MIN-FLOW",
                "HEAT-SETPT-CTRL",
                "COOL-SETPT-CTRL",
                "MIN-RESET-T",
                "MAX-RESET-T",
                "DHW-INLET-T",
                "DHW-INLET-T-SCH",
            ]
        ),
        "ConstructionKeywords": _ListEnum(["LAYERS", "ABSORPTANCE", "U-VALUE"]),
        "DayScheduleKeywords": _ListEnum(
            [
                "TYPE",
                "VALUES",
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
            ]
        ),
        "DoorKeywords": _ListEnum(
            [
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
        "FloorKeywords": _ListEnum(
            [
                "AZIMUTH",
            ]
        ),
        "GlassTypeKeywords": _ListEnum(
            [
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
            ]
        ),
        "MasterMeterKeywords": _ListEnum(
            [
                "TYPE",
            ]
        ),
        "SiteParameterKeywords": _ListEnum(
            [
                "DAYLIGHT-SAVINGS",
                "GROUND-T",
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
        "PumpKeywords": _ListEnum(
            [
                "NUMBER",
                "PUMP-KW",
                "HEAD",
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
                "SOURCE-KW",
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
                "HEAT-PUMP",
                "FURNACE",
                "ELECTRIC",
                "HOT-WATER",
                "NONE",
                "STEAM",
                "DHW-LOOP",
            ]
        ),
        "SystemCoolingTypes": _ListEnum(
            [
                "ELEC-DX",
                "CHILLED-WATER",
                "NONE",
            ]
        ),
        "SystemTypes": _ListEnum(
            [
                "PTAC",
                "PSZ",
                "PMZS",
                "PVAVS",
                "PVVT",
                "HP",
                "SZRH",
                "VAVS",
                "RHFS",
                "DDS",
                "MZS",
                "PIU",
                "FC",
                "IU",
                "UVT",
                "UHT",
                "RESYS2",
                "CBVAV",
                "SUM",
                "DOAS",
            ]
        ),
        "SystemSupplyFanTypes": _ListEnum(
            [
                "CONSTANT-VOLUME",
                "SPEED",
                "INLET",
                "DISCHARGE",
                "FAN-EIR-FPLR",
            ]
        ),
        "SystemUnoccupiedFanOperationOptions": _ListEnum(
            ["CYCLE-ON-ANY", "CYCLE-ON-FIRST", "STAY-OFF", "ZONE-FANS-ONLY"]
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
        "SystemKeywords": _ListEnum(
            [
                "TYPE",
                "HEAT-SOURCE",
                "COOL-SOURCE",
                "HW-LOOP",
                "CHW-LOOP",
                "CW-LOOP",
                "DDS-TYPE",
                "FAN-CONTROL",
                "NIGHT-CYCLE-CTRL",
                "MIN-OA-METHOD",
                "MIN-AIR-SCH",
                "SIZING-RATIO",
                "HEAT-SIZING-RATI",
                "COOL-SIZING-RATI",
                "HEATING-CAPACITY",
                "COOLING-CAPACITY",
                "HUMIDIFIER-TYPE",
                "HEAT-T",
                "PREHEAT-SOURCE",
                "PREHEAT-CAPACITY",
                "PREHEAT-T",
                "SUPPLY-STATIC",
                "RETURN-STATIC",
                "HSUPPLY-STATIC",
                "RETURN-KW/FLOW",
                "RETURN-FAN-LOC",
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
                "ZONE-OA-METHOD",
                "BBRD-LOOP",
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
        "WindowKeywords": _ListEnum(
            [
                "HEIGHT",
                "WIDTH",
                "FRAME-WIDTH",
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
        "ZoneKeywords": _ListEnum(
            [
                "TERMINAL-TYPE",
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
                "BASEBOARD-SOURCE",
                "BASEBOARD-RATING",
                "MIN-FLOW-SCH",
                "CMIN-FLOW-SCH",
                "HMIN-FLOW-SCH",
                "MIN-FLOW-CONTROL",
                "MIN-FLOW-RATIO",
                "MIN-FLOW/AREA",
                "OA-FLOW/PER",
                "OUTSIDE-AIR-FLOW",
                "OA-CHANGES",
                "OA-FLOW/AREA",
                "EXHAUST-STATIC",
                "EXHAUST-EFF",
                "EXHAUST-KW/FLOW",
            ]
        ),
    }


# def print_schema_enums():
#     """Print all the schema enumerations with their names and values
#
#     This is primarily useful for debugging purposes
#     """
#
#     for key in BDLEnums.bdl_enums:
#         print(f"{key}:")
#         for e in BDLEnums.bdl_enums[key].get_list():
#             print(f"    {e}")
#         print()
#
#
# print_schema_enums()
