from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .buildings import Building
from .effects import Requirement
from .science import Advance
from .secfile.loader import NamedReference, rename, section

KNOWN_UNIT_CLASS_FLAGS = {
    "TerrainSpeed",
    "TerrainDefense",
    "DamageSlows",
    "CanOccupyCity",
    "Missile",
    "BuildAnywhere",
    "Unreachable",
    "CollectRansom",
    "ZOC",
    "CanFortify",
    "CanPillage",
    "DoesntOccupyTile",
    "AttackNonNative",
    "AttFromNonNative",
    "KillCitizen",
    "Airliftable",
    # Pre-2.5 stuff
    "RiverNative",
    "RoadNative",
    # 3.0 stuff
    "Ground",
    "Flying",
    # New stuff
    "BorderPolice",
    "Expellable",
    "HeavyWeight",
    "LightWeight",
    "MediumWeight",
}


@section("veteran_system")
@typechecked
@dataclass
class VeteranLevel:
    name: str
    raise_chance: int
    work_raise_chance: int
    power_factor: int
    move_bonus: int


def load_veteran_levels(
    veteran_names,
    veteran_raise_chance,
    veteran_work_raise_chance,
    veteran_power_fact,
    veteran_move_bonus,
):
    if any(
        (
            len(veteran_names) != len(veteran_raise_chance),
            len(veteran_names) != len(veteran_work_raise_chance),
            len(veteran_names) != len(veteran_power_fact),
            len(veteran_names) != len(veteran_move_bonus),
        )
    ):
        raise ValueError("Veteran level vectors have inconsistent lengths")

    levels = []
    for args in zip(
        veteran_names,
        veteran_raise_chance,
        veteran_work_raise_chance,
        veteran_power_fact,
        veteran_move_bonus,
    ):
        levels.append(VeteranLevel(*args))
    if levels[-1].raise_chance != 0 or levels[-1].work_raise_chance != 0:
        warn(
            'The last veteran level "%s" has a non-zero raise chance' % levels[-1].name
        )

    return levels


@section("unitclass_.+")
@typechecked
@dataclass
class UnitClass:
    name: str
    min_speed: int
    hp_loss_pct: int
    non_native_def_pct: int = 100
    rule_name: str = None
    hut_behavior: str = "Normal"
    flags: set[str] = field(default_factory=set)
    helptext: list[str] = field(default_factory=list)  # 3.0

    # Pre-2.5 stuff
    move_type: str = None

    def __post_init__(self):
        if self.rule_name is None:
            self.rule_name = self.name

        if type(self.flags) == str:
            self.flags = {self.flags}
        else:
            self.flags = set(self.flags)
        unknown = self.flags - KNOWN_UNIT_CLASS_FLAGS
        if unknown:
            raise ValueError(
                'Unit class "%s" has unknown flags %s' % (self.name, unknown)
            )

    def __hash__(self):
        return self.name.__hash__()

    def __lt__(self, other):
        return self.name < other.name


@rename(**{"class": "uclass"})
@section("unit_.+")
@typechecked
@dataclass
class UnitType:
    name: str
    uclass: NamedReference(UnitClass)
    tech_req: set[NamedReference(Advance)]
    graphic: str
    graphic_alt: str
    sound_move: str
    sound_move_alt: str
    sound_fight: str
    sound_fight_alt: str
    build_cost: int
    pop_cost: int
    attack: int
    defense: int
    hitpoints: int
    firepower: int
    move_rate: int
    vision_radius_sq: int
    transport_cap: int
    fuel: int
    uk_happy: int
    uk_shield: int
    uk_food: int
    uk_gold: int
    obsolete_by: NamedReference("UnitType") = None
    impr_req: NamedReference(Building) = None
    cargo: set[NamedReference(UnitClass)] = field(default_factory=set)
    targets: set[NamedReference(UnitClass)] = field(default_factory=set)
    embarks: set[NamedReference(UnitClass)] = field(default_factory=set)
    disembarks: set[NamedReference(UnitClass)] = field(default_factory=set)
    bonuses: list[dict] = field(default_factory=list)  # TODO NamedReference(Bonus)
    flags: set[str] = field(default_factory=set)
    roles: set[str] = field(default_factory=set)
    helptext: list[str] = field(default_factory=list)
    gov_req: str = None  # TODO NamedReference(Government)
    rule_name: str = None

    convert_to: NamedReference("UnitType") = None
    convert_time: int = None

    veteran_names: list[str] = None
    veteran_raise_chance: list[int] = None
    veteran_work_raise_chance: list[int] = None
    veteran_power_fact: list[int] = None
    veteran_move_bonus: list[int] = None
    veteran_levels: list[str] = None  # Cannot be set from outside

    paratroopers_range: int = None
    paratroopers_mr_req: int = None
    paratroopers_mr_sub: int = None

    bombard_rate: int = None

    # Pre-2.5 stuff
    vision_range: int = None

    # 3.0 stuff
    city_size: int = None

    def __post_init__(self):
        if self.rule_name is None:
            self.rule_name = self.name

        if type(self.helptext) is list:
            self.helptext = "\n\n".join(self.helptext)

        if "None" in self.tech_req:
            self.tech_req.remove("None")

        if self.obsolete_by == "None":
            self.obsolete_by = None

        if self.veteran_levels:
            raise TypeError("veteran_levels cannot be set externally")
        if self.veteran_names:
            self.veteran_levels = load_veteran_levels(
                self.veteran_names,
                self.veteran_raise_chance,
                self.veteran_work_raise_chance,
                self.veteran_power_fact,
                self.veteran_move_bonus,
            )
        else:
            # FIXME Get the ruleset default
            pass

    def __lt__(self, other):
        return self.name < other.name
