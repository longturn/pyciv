from dataclasses import dataclass
from typeguard import typechecked

import re

def section(section_regex):
    def annotate(cls):
        cls._section_regex = re.compile(section_regex)
        setattr(cls, '__section_regex__', re.compile(section_regex))
        return cls
    return annotate

@section('datafile')
@typechecked
@dataclass
class DataFileHeader:
    description: str
    options: str

@section('about')
@typechecked
@dataclass
class AboutData:
    name: str
    version: str = ''
    summary: str = ''
    description: str = ''
    capabilities: str = '' # 3.0

@typechecked
class Ruleset:
    freeciv_version: str
    name: str
    version: str
    summary: str
    description: str

    unit_classes: list
    unit_types: list
    advances: list
    veteran_levels: list
