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

import argparse
import logging

from ..secfile import SpecParser, read_section
from . import DataFileHeader

_log = logging.getLogger(__name__)

def parse_files(ruleset, data_path):
    """
    Parses the data file for a ruleset and returns a dict containing the section
    data.
    """
    sections = dict()
    for name in ('buildings', 'cities', 'effects', 'game', 'governments',
                 'nations', 'techs', 'terrain', 'units'):
        try:
            _log.info('Loading %s/%s.ruleset', ruleset, name)
            sections[name] = list(SpecParser(f'{ruleset}/{name}.ruleset', data_path))
        except FileNotFoundError:
            # In versions <2.5, files could be omitted and would be taken from
            # the default ruleset.
            # The fallback only works if files for the corresponding version are
            # in the path.
            _log.warn('Could not find %s/%s.ruleset, trying default/%s.ruleset',
                      ruleset, name, name)
            _log.warn('This behavior is supported for backwards compatibility. '
                      'Use *include instead.')
            sections[name] = list(SpecParser(f'default/{name}.ruleset', data_path))

    return sections

def check_version(all_sections):
    """
    Checks that all the files target the same Freeciv version.
    """
    version = None
    for name, sections in all_sections.items():
        header = read_section(DataFileHeader, sections)
        header_version = header.freeciv_version()
        _log.debug(f'{name}.ruleset uses version {header_version}')
        if version and version != header_version:
            raise ValueError('Conflicting versions in ruleset files: '
                             f'{version} and {header_version}')
        else:
            version = header_version
    return version

def document_ruleset():
    """
    Parses a ruleset and writes documentation. This should be used from the
    command line.
    """
    # Override the logger when the entry point is used
    global _log
    _log = logging.getLogger('freeciv-doc')

    parser = argparse.ArgumentParser(
        description='Create documentation for a ruleset')

    # The name of the ruleset directory, equivalent to /rulesetdir on the server
    parser.add_argument('ruleset', type=str, help='ruleset name')

    # The output directory for the documentation
    parser.add_argument('output', type=str, default='.', nargs='?',
                        help='output directory')

    # Path to use for data files. Later we may try to discover freeciv
    # installations and/or support FREECIV_DATA_PATH
    parser.add_argument('-p', '--path', action='append',
                        help='add a directory to the search path')

    # Verbosity flag
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level (repeat for more verbose)')

    args = parser.parse_args()

    # Default to WARNING, -v is INFO and -vv is DEBUG
    logging.basicConfig(level=logging.WARNING-10*args.verbose)

    # Start by parsing the files so we fail immediately if any of them is
    # missing or has a syntax error
    sections = parse_files(args.ruleset, args.path)

    # Determine the Freeciv version. This needs to be done first in order to set
    # up version upgrade hooks.
    version = check_version(sections)
