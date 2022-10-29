from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .science import Advance
from .secfile.loader import section


def rewrite(rules):
    def annotate(cls):
        cls._rewrite_rules = rules
        return cls

    return annotate


# TODO should be moved to a more general parsing code
def as_list(value):
    """
    If value is a list, returns it. Otherwise return a list with value as its
    only element. This is required because the spec file format doesn't
    distinguish between scalars and lists of size 1.
    """
    if type(value) == list:
        return value
    else:
        return [value]


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
    # Turn them all into lists
    veteran_names = as_list(veteran_names)
    veteran_raise_chance = as_list(veteran_raise_chance)
    veteran_work_raise_chance = as_list(veteran_work_raise_chance)
    veteran_power_fact = as_list(veteran_power_fact)
    veteran_move_bonus = as_list(veteran_move_bonus)

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
    flags: set = field(default_factory=set)
    helptext: str = ""  # 3.0

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


@rewrite({"class": "uclass"})
@section("unit_.+")
@typechecked
@dataclass
class UnitType:
    name: str
    uclass: UnitClass
    tech_req: set
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
    obsolete_by: "UnitType" = None
    impr_req: "Improvement" = None
    gov_req: "Government" = None
    cargo: set = field(default_factory=set)
    targets: set = field(default_factory=set)
    embarks: set = field(default_factory=set)
    disembarks: set = field(default_factory=set)
    bonuses: list = field(default_factory=list)
    flags: set = field(default_factory=set)
    roles: set = field(default_factory=set)
    helptext: str = None
    gov_req: "Government" = None
    rule_name: str = None

    convert_to: "UnitType" = None
    convert_time: int = None

    veteran_names: list = None
    veteran_raise_chance: list = None
    veteran_work_raise_chance: list = None
    veteran_power_fact: list = None
    veteran_move_bonus: list = None
    veteran_levels: list = None  # Cannot be set from outside

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

        if type(self.tech_req) == str:
            self.tech_req = {self.tech_req}
        else:
            self.tech_req = set(self.tech_req)
        if "None" in self.tech_req:
            self.tech_req.remove("None")

        if self.obsolete_by == "None":
            self.obsolete_by = None

        if type(self.flags) is str and self.flags:
            self.flags = {self.flags}

        if type(self.roles) is str and self.roles:
            self.roles = {self.roles}

        if type(self.cargo) is str and self.cargo:
            self.cargo = {self.cargo}

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
