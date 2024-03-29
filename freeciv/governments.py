from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from freeciv.effects import Requirement

from .secfile.loader import read_named_sections, read_section, section


@section("governments")
@typechecked
@dataclass
class GovernmentData:
    during_revolution: str


@section("government_.+")
@typechecked
@dataclass
class Government:
    name: str
    graphic: str
    graphic_alt: str
    ruler_male_title: str
    ruler_female_title: str
    ai_better: str = None
    rule_name: str = None
    helptext: list[str] = field(default_factory=list)
    reqs: list[Requirement] = field(default_factory=list)

    ai_better_help_rst: str = "The game AI will not consider this government for use if the government listed here is available. If the value is `None`, the setting is not enabled in this ruleset."

    def __post_init__(self):
        if type(self.helptext) is list:
            self.helptext = "\n\n".join(self.helptext)


class GovernmentSettings:
    def __init__(self, sections):
        self.government_parms = read_section(GovernmentData, sections)
        self.governments = read_named_sections(Government, sections)
