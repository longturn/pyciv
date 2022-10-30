from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .effects import Requirement
from .science import Advance
from .secfile.loader import read_named_sections, rewrite, section


def building_compat(values):
    obsolete_by = values["obsolete_by"]
    if type(obsolete_by) == str:
        del values["obsolete_by"]
        if obsolete_by != "None":
            values["obsolete_by"] = Requirement(
                type="Tech", name=obsolete_by, range="Player"
            )

    return values


@rewrite(building_compat)
@section("building_.+")
@typechecked
@dataclass
class Building:
    name: str
    genus: str
    graphic: str
    build_cost: int
    upkeep: int
    sabotage: int
    reqs: list[Requirement] = field(default_factory=list)  # Requirements
    obsolete_by: list[Requirement] = field(default_factory=list)  # Requirements
    rule_name: str = None
    graphic_alt: str = None
    helptext: list[str] = field(default_factory=list)
    sound: str = None
    sound_alt: str = None
    flags: set[str] = field(default_factory=set)

    # 2.3
    replaced_by: object = None

    def __post_init__(self):
        if self.rule_name is None:
            self.rule_name = self.name

        if self.name == "None":
            raise ValueError('A building cannot be named "None"')

        if type(self.helptext) is list:
            self.helptext = "\n\n".join(self.helptext)

        if self.reqs == ["None"]:
            self.reqs = []

    def __hash__(self):
        return self.name.__hash__()

    def __lt__(self, other):
        return self.name < other.name


class BuildingsSettings:
    def __init__(self, sections):
        self.buildings = read_named_sections(Building, sections)
