from dataclasses import dataclass, field
from warnings import warn
from typeguard import typechecked

def section(section_regex):
    def annotate(cls):
        import re
        cls._section_regex = re.compile(section_regex)
        return cls
    return annotate

@section('advance_.+')
@typechecked
@dataclass
class Advance:
    name: str
    req1: 'Advance'
    req2: 'Advance'
    graphic: str = None
    rule_name: str = None
    root_req: 'Advance' = None
    graphic_alt: str = None
    helptext: str = ''
    bonus_message: str = None
    flags: set = field(default_factory=set)
    cost: int = None

    def __post_init__(self):
        if self.rule_name is None:
            self.rule_name = self.name

        if self.name == 'None':
            raise ValueError('An advance cannot be named "None"')

        if self.req1 == 'None':
            self.req1 = None
        if self.req2 == 'None':
            self.req2 = None
        if self.root_req == 'None':
            self.root_req = None

        if type(self.helptext) is list:
            self.helptext = '\n\n'.join(self.helptext)

    def __hash__(self):
        return self.name.__hash__()

    def __lt__(self, other):
        return self.name < other.name

    @property
    def reqs(self):
        return filter(lambda req: not req is None, (self.req1, self.req2))
