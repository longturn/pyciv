# This file is part of pyciv.
#
# pyciv is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyciv is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyciv.  If not, see <https://www.gnu.org/licenses/>.

import dataclasses
import logging
import re


def section(section_regex):
    """
    Annotates a class as being represented by a section in data files.

    Any section whose name matches section_regex will be turned into objects of
    the decorated class when encountered.
    """
    def annotate(cls):
        setattr(cls, '__section_regex__', re.compile(section_regex))
        return cls
    return annotate


def as_list(value, target_content_type=None):
    """
    Coerces a value to a list. This is only valid in the context of data parsed
    using a SpecParser.
    """
    if type(value) == list:
        # Then coerce the contents!
        return [as_type(item, target_content_type) for item in value]
    elif value == '':
        # This is sometimes used as an empty list
        return []
    else:
        # The spec format cannot distinguish between a one-element list and a
        # value
        return [as_type(value, target_content_type)]


def as_type(value, target_type):
    """
    Coerces a value to the target type. This is only valid in the context of
    data parsed using a SpecParser.

    The supported types are:

    * int
    * str
    * typing.List[X]
    * typing.Set[X]
    """
    if hasattr(target_type, '__origin__') and hasattr(target_type, '__args__'):
        # Handle generic types from the typing module
        if target_type.__origin__ == list:
            return as_list(value, target_type.__args__[0])
        elif target_type.__origin__ == set:
            return set(as_list(value, target_type.__args__[0]))
        else:
            raise ValueError(f'Unknown generic type {target_type}')
    elif isinstance(value, target_type):
        # This is already good
        return value
    else:
        # Whoops
        raise TypeError(f'Expected {target_type.__name__}, got '
                        f'{type(value).__name__}')


def read_sections(section_class, sections):
    if not hasattr(section_class, '__section_regex__'):
        raise ValueError('Cannot find the section regex')

    result = []
    for section in sections:
        if section_class.__section_regex__.match(section.name):
            logging.debug('Processing section "%s"', section.name)

            fields = {f.name: f for f in dataclasses.fields(section_class)}
            dictionnary = {}

            for name, value in section.items():
                if name not in fields:
                    raise TypeError(f'Type {section_class.__name__} has no '
                                    f'field called "{name}"')

                target_type = fields[name].type
                dictionnary[name] = as_type(value, target_type)

            result.append(section_class(**dictionnary))
    return result


def read_section(section_class, sections):
    all_results = list(read_sections(section_class, sections))
    pattern = section_class.__section_regex__.pattern
    if not all_results:
        raise ValueError(f'No section matching "{pattern}" was found')
    if len(all_results) > 1:
        raise ValueError(f'Several sections matching "{pattern}" were found, '
                         f'expected only one')
    return all_results[0]
