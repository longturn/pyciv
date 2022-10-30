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

import logging
import re
from typing import NewType, TypeVar, Union, get_args, get_origin, get_type_hints

from typeguard import check_type


def NamedReference(T):
    ref_type = NewType("NamedReference", Union[str, T])
    ref_type.wrapped = T.__name__ if type(T) == type else T
    return ref_type


def rewrite(fn):
    def annotate(cls):
        cls._rewrite_fn = fn
        return cls

    return annotate


def rename(**kwargs):
    def rename_fn(values):
        for old, new in kwargs.items():
            if old in values:
                values[new] = values[old]
                del values[old]
        return values

    return rewrite(rename_fn)


def section(section_regex):
    """
    Annotates a class as being represented by a section in data files.

    Any section whose name matches section_regex will be turned into objects of
    the decorated class when encountered.
    """

    def annotate(cls):
        setattr(cls, "_section_regex", re.compile(section_regex))
        return cls

    return annotate


def _list_from_value(value, target_content_type=None):
    """
    Coerces a value to a list. This is only valid in the context of data parsed
    using a SpecParser.
    """
    if type(value) == list:
        # Then coerce the contents!
        return [_instance_from_value(item, target_content_type) for item in value]
    elif value == "":
        # This is sometimes used as an empty list
        return []
    else:
        # The spec format cannot distinguish between a one-element list and a
        # value
        return [_instance_from_value(value, target_content_type)]


def _instance_from_value(value, target_class, name=""):
    # A few supported "primitive" types
    if target_class in (bool, dict, float, int, str):
        return target_class(value)
    elif hasattr(target_class, "wrapped"):
        # NamedReference
        return str(value)
    elif hasattr(target_class, "__origin__"):
        # Generic class
        origin, args = get_origin(target_class), get_args(target_class)
        if origin == list:  # List[X]
            return _list_from_value(value, args[0])
        elif origin == set:  # Set[X]
            return set(_list_from_value(value, args[0]))

    # Maybe we're already good
    try:  # try/catch for control flow :(
        check_type(name, value, target_class)
        return value
    except TypeError:
        ...

    # "General" case. Convert arguments to the requested types

    # Check for unknown keys
    hints = get_type_hints(target_class)
    unknown = value.keys() - hints.keys()
    if unknown:
        fields = '", "'.join(unknown)
        raise ValueError(f'Type {target_class.__name__} has no field called "{fields}"')

    # Fetch default values
    args = {
        name: getattr(target_class, name)
        for name in hints.keys()
        if hasattr(target_class, name)
    }

    # Insert provided arguments
    args.update(
        {
            name: _instance_from_value(val, hints[name], name)
            for name, val in value.items()
        }
    )

    return target_class(**args)


def read_sections(section_class, sections):
    if not hasattr(section_class, "_section_regex"):
        raise TypeError("Cannot find the section regex")

    result = []
    for section in sections:
        if section_class._section_regex.match(section.name):
            logging.debug(f'Processing section "%s"', section.name)
            fields = list(
                filter(lambda name: not name.startswith("_"), dir(section_class))
            )
            default_values = {name: getattr(section_class, name) for name in fields}
            annotations = section_class.__annotations__

            if hasattr(section_class, "_rewrite_fn"):
                section = section_class._rewrite_fn(section)

            result.append(_instance_from_value(section, section_class))
    return result


def read_section(section_class, sections, *, missing_ok=False):
    all_results = list(read_sections(section_class, sections))
    pattern = section_class._section_regex.pattern
    if not all_results:
        if missing_ok:
            return None
        else:
            raise ValueError(f'No section matching "{pattern}" was found')
    if len(all_results) > 1:
        raise ValueError(
            f'Several sections matching "{pattern}" were found, expected only one'
        )
    return all_results[0]


def read_named_sections(section_class, sections):
    return {obj.name: obj for obj in read_sections(section_class, sections)}
