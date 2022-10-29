from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .effects import Requirement
from .science import Advance
from .secfile.loader import section


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
    reqs: list = field(default_factory=list)  # Requirements
    obsolete_by: list = field(default_factory=list)  # Requirements
    rule_name: str = None
    graphic_alt: str = None
    helptext: str = ""
    sound: str = None
    sound_alt: str = None
    flags: set = field(default_factory=set)

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
        else:
            self.reqs = [Requirement(**req) for req in self.reqs]

        if self.obsolete_by == ["None"]:
            self.obsolete_by = []
        else:
            for i, req in enumerate(self.obsolete_by):
                if type(req) == str:
                    # Freeciv 2.5 and earlier.
                    self.obsolete_by[i] = Requirement(
                        type="Tech", name=req, range="Player"
                    )
                else:
                    self.obsolete_by[i] = Requirement(**req)

    def __hash__(self):
        return self.name.__hash__()

    def __lt__(self, other):
        return self.name < other.name
