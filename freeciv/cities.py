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
    # Object Attributes
    add_to_size_limit: int = 8
    angry_citizens: bool = True
    celebrate_size_limit: int = 3
    changable_budget: bool = True
    forced_science: int = 0
    forced_luxury: int = 0
    forced_gold: int = 0
    vision_reveal_tiles: bool = False
    pop_report_zeroes: int = 4

    # Help Strings
    add_to_size_limit_help_rst: str = "The size of a city has to be less than or equal to this value to be able to add population from a settler or other popluation containing unit."

    angry_citizens_help_rst: str = "If set to ``True``, cities can have angry citizens."

    celebrate_size_limit_help_rst: str = "Cities have to be greater than or equal in size of this value before they can celebrate."

    changable_budget_help_rst: str = "If set to ``True``, the game allows a changable national budget for science, luxury goods, and tax. If set to ``False``, the amounts are hard coded."

    forced_science_help_rst: str = (
        "Changeable Budget is ``False``. The forced science output is: "
    )

    forced_luxury_help_rst: str = (
        "Changeable Budget is ``False``. The forced luxury goods output is: "
    )

    forced_gold_help_rst: str = (
        "Changeable Budget is ``False``. The forced tax output is: "
    )

    vision_reveal_tiles_help_rst: str = (
        "If set to ``True``, terrain within a city vision area is revealed."
    )


@section("citizen")
@typechecked
@dataclass
class CityCitizenData:
    # Object Attributes
    nationality: bool = True
    convert_speed: int = 50
    partisans_pct: int = 0
    conquest_convert_pct: int = 0

    # Help Strings
    nationality_help_rst: str = (
        "If set to ``True``, then citizen nationality is enabled."
    )

    convert_speed_help_rst: str = "The value represents the base probability of converting a foreign citizen in a conquered city to your own nation as the city grows."

    partisans_pct_help_rst: str = "The percentage of own nationality to inspire partisans. If ``0``, original city owner information is used instead."

    conquest_convert_pct_help_rst: str = "The percentage of citizens which converts to the new nation after a city was  conquered. Applied separately for each nationality present in the city, and number of converted people rounded up."


@section("missing_unit_upkeep")
@typechecked
@dataclass
class CityMissingUnitUpkeepData:
    # Object Attributes
    food_protected: str = ""
    food_unit_act: list[str] = field(default_factory=list)
    food_wipe: bool = False
    gold_protected: str = ""
    gold_unit_act: list[str] = field(default_factory=list)
    gold_wipe: bool = False
    shield_protected: str = ""
    shield_unit_act: list[str] = field(default_factory=list)
    shield_wipe: bool = False

    # Help Strings
    food_protected_help_rst: str = "? helptext needs help ?"

    food_unit_act_help_rst: str = "? helptext needs help ?"

    food_wipe_help_rst: str = "? helptext needs help ?"

    gold_protected_help_rst: str = "? helptext needs help ?"

    gold_unit_act_help_rst: str = "? helptext needs help ?"

    gold_wipe_help_rst: str = "? helptext needs help ?"

    shield_protected_help_rst: str = "? helptext needs help ?"

    shield_unit_act_help_rst: str = "? helptext needs help ?"

    shield_wipe_help_rst: str = "? helptext needs help ?"


class CitySettings:
    def __init__(self, sections):
        self.parameters = read_section(CityParametersData, sections)
        self.citizens = read_section(CityCitizenData, sections, missing_ok=True)
        self.missing_unit_upkeep = read_section(
            CityMissingUnitUpkeepData, sections, missing_ok=True
        )
