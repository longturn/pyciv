from dataclasses import dataclass, field

from typeguard import typechecked

from .secfile.loader import rename, section


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
    negated: bool = None  # 2.5- syntax

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
            raise TypeError(
                "Both negated and present were provided (mixing 2.5 and 2.6 syntax)"
            )
        del self.negated


@rename(name="type")
@section("effect_.+")
@typechecked
@dataclass
class Effect:
    value: int
    multiplier: str = None
    type: str = None
    name: str = None
    reqs: list[Requirement] = field(default_factory=list)
    nreqs: list[Requirement] = None

    def __post_init__(self):
        if self.type is None:
            raise ValueError(f"Effect has no type")

        if not self.nreqs is None:
            for nreq in self.nreqs:
                nreq.present = False
                self.reqs.append(nreq)
        del self.nreqs
