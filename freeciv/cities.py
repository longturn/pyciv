import re
from dataclasses import dataclass, field
from typing import Literal, Union

from typeguard import typechecked

from freeciv.effects import Requirement

from .secfile.loader import read_section, section


@section("parameters")
@typechecked
@dataclass
class CityParametersData:
    add_to_size_limit: int = 8
    angry_citizens: bool = True
    celebrate_size_limit: int = 3
    changable_budget: bool = True
    forced_science: int = 0
    forced_luxury: int = 0
    forced_gold: int = 0
    vision_reveal_tiles: bool = False
    pop_report_zeroes: int = 4


@section("citizen")
@typechecked
@dataclass
class CityCitizenData:
    nationality: bool = True
    convert_speed: int = 50
    partisans_pct: int = 0
    conquest_convert_pct: int = 0


@section("missing_unit_upkeep")
@typechecked
@dataclass
class CityMissingUnitUpkeepData:
    food_protected: str = ""
    food_unit_act: list[str] = field(default_factory=list)
    food_wipe: bool = False
    gold_protected: str = ""
    gold_unit_act: list[str] = field(default_factory=list)
    gold_wipe: bool = False
    shield_protected: str = ""
    shield_unit_act: list[str] = field(default_factory=list)
    shield_wipe: bool = False


class CitySettings:
    def __init__(self, sections):
        self.parameters = read_section(CityParametersData, sections)
        self.citizens = read_section(CityCitizenData, sections, missing_ok=True)
        self.missing_unit_upkeep = read_section(CityMissingUnitUpkeepData, sections, missing_ok=True)
