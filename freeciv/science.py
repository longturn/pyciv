from dataclasses import dataclass, field
from warnings import warn

from typeguard import typechecked

from .game import ResearchData
from .secfile.loader import NamedReference, read_named_sections, section


def calculate_cost(advance, game_info):
    """
    Function to calculate the full cost of a technology advance.
    Pulled formulas from freeciv21 tech.cpp.
    Thanks to pepeto, Matthias, and cazfi
    """
    recursive_reqs = set()
    def walk(adv):
        recursive_reqs.add(adv)
        for req in adv.reqs:
            walk(req)

    walk(advance)
    num_reqs = len(recursive_reqs)

    if game_info.tech_cost_style in ("Civ1Civ2", "Linear"):
        cost = game_info.base_tech_cost * num_reqs
    elif game_info.tech_cost_style in ("Classic", "ClassicPreset"):
        cost = game_info.base_tech_cost * (1.0 + num_reqs) * math.sqrt(1.0 + num_reqs) / 2
    elif game_info.tech_cost_style in ("Experimental", "ExperimentalPreset"):
        cost = game_info.base_tech_cost * ((num_reqs) * (num_reqs) / (1 + math.sqrt(math.sqrt(num_reqs + 1))) - 0.5);
    else:
        raise ValueError(f'Unknown tech cost style "{game_info.base_tech_cost}"')

    if "Preset" in game_info.tech_cost_style:
        cost = max(cost, game_info.base_tech_cost)

    if advance.tclass:
        cost *= advance.tclass.cost_pct / 100

    return cost


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

        if self.cost == "None":
            self.cost = calculate_cost(advance, game_info)

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
