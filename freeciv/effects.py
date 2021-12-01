from dataclasses import dataclass, field
from typing import List
from typeguard import typechecked

def rewrite(rules):
    def annotate(cls):
        cls._rewrite_rules = rules
        return cls
    return annotate

def section(section_regex):
    def annotate(cls):
        import re
        cls._section_regex = re.compile(section_regex)
        return cls
    return annotate

# FIXME Used in other places, move?
@typechecked
@dataclass
class Requirement:
    type: str
    name: str
    range: str
    present: bool = None
    survives: bool = False
    quiet: bool = False
    negated: bool = None # 2.5- syntax

    def __post_init__(self):
        # In 2.5-, requirements are negated by setting 'negated' to TRUE
        # In 2.6+, requirements are negated by setting 'present' to FALSE
        if self.present is None and self.negated is None:
            # Doesn't matter which version this is
            self.present = True
        elif self.negated is None and not self.present is None:
            # Modern (2.6+) syntax
            pass
        elif not self.negated is None and self.present is None:
            # Old (2.5-) syntax
            self.present = not self.negated
        else:
            raise TypeError('Both negated and present were provided (mixing 2.5 and 2.6 syntax)')
        del self.negated

@section('effect_.+')
@typechecked
@dataclass
class Effect:
    value: int
    multiplier: str = None
    type: str = None
    name: str = None
    reqs: List[Requirement] = field(default_factory=list)
    nreqs: List[Requirement] = None

    def __post_init__(self):
        self.reqs = [Requirement(**req) for req in self.reqs]

        if self.type is None:
            if not self.name is None: # 2.3, 2.4?
                self.type = self.name
                del self.name
            else:
                raise ValueError(f'Effect has no type')

        if not self.nreqs is None:
            self.reqs += [Requirement(**req, present=False) for req in self.nreqs]
        del self.nreqs
