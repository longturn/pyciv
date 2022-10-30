from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .secfile.loader import NamedReference, read_named_sections, section


@section("advance_.+")
@typechecked
@dataclass
class Advance:
    name: str
    req1: NamedReference("Advance")
    req2: NamedReference("Advance")
    graphic: str = None
    rule_name: str = None
    root_req: NamedReference("Advance") = None
    graphic_alt: str = None
    helptext: list[str] = field(default_factory=list)
    bonus_message: str = None
    flags: set[str] = field(default_factory=set)
    cost: int = None

    def __post_init__(self):
        if self.rule_name is None:
            self.rule_name = self.name

        if self.name == "None":
            raise ValueError('An advance cannot be named "None"')

        if self.req1 == "None":
            self.req1 = None
        if self.req2 == "None":
            self.req2 = None
        if self.root_req == "None":
            self.root_req = None

        if type(self.helptext) is list:
            self.helptext = "\n\n".join(self.helptext)

    def __hash__(self):
        return self.name.__hash__()

    def __lt__(self, other):
        return self.name < other.name

    @property
    def reqs(self):
        return filter(lambda req: not req is None, (self.req1, self.req2))


class ScienceSettings:
    def __init__(self, sections):
        self.advances = read_named_sections(Advance, sections)
