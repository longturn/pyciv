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

import re
from dataclasses import dataclass

from typeguard import typechecked

from ..secfile import section

_KNOWN_FORMAT_VERSIONS = {10: "3.0", 20: "3.1"}
"""Maps Freeciv ruleset format versions to Freeciv release versions."""


@section("datafile")
@typechecked
@dataclass
class DataFileHeader:
    """The [data_file] section"""

    __section_regex__ = re.compile("datafile")

    options: str
    """Required server capabilities"""

    description: str = ""
    """
    Description of the data file. This was never used anywhere and can be
    ignored.
    """

    format_version: int = 0
    """
    The version of the file format. This is 10 for Freeciv 3.0, 20 for Freeciv
    3.1 and 0 otherwise
    """

    def freeciv_version(self):
        """
        Retrieves the Freeciv version targeted by the data file by parsing the
        capability string. Returns it as a string (eg "2.6").

        Raises ValueError when the version detection heuristics fail.
        """
        # When present, prefer format_version since it is used by Freeciv
        # itself.
        if self.format_version > 0:
            if self.format_version in _KNOWN_FORMAT_VERSIONS:
                return _KNOWN_FORMAT_VERSIONS[self.format_version]
            else:
                raise ValueError(f"Unknown format version {self.format_version}")

        # Versions before 3.0 did not have a format_version field. Use the
        # capability string.
        # Older versions used just the release version in options, we don't
        # support these.
        match = re.search(r"\+Freeciv-([\d\.]+)-ruleset", self.options)
        if match:
            return match.group(1)

        # Development version?
        match = re.search(
            r"\+Freeciv-ruleset-Devel-(\d{4}\.[a-zA-Z]{3}\.\d{2})", self.options
        )
        if match:
            # FIXME Could use a dictionary of known development capstrings.
            # In the meantime provide a somewhat helpful error message.
            raise ValueError("Development versions of Freeciv are not supported")
        else:
            raise ValueError("Could not deduce the Freeciv version")
