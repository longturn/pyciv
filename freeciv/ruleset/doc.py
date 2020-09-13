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

from ..secfile import SpecParser

def parse_files(ruleset, data_path):
    """
    Parses the data file for a ruleset and returns a dict containing the section
    data.
    """
    sections = dict()
    for name in ('buildings', 'cities', 'effects', 'game', 'governments',
                 'nations', 'techs', 'terrain', 'units'):
        sections[name] = list(SpecParser(f'{ruleset}/{name}.ruleset', data_path))
    return sections

def document_ruleset():
    """
    Parses a ruleset and writes documentation. This should be used from the
    command line.
    """
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

    args = parser.parse_args()

    # Start by parsing the files so we fail immediately if any of them is
    # missing or has a syntax error
    sections = parse_files(args.ruleset, args.path)
