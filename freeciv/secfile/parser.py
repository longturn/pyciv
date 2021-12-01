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
import ply.yacc

from .lexer import SpecLexer

_newline_magic = {}
_translation_domain_regex = re.compile(r'\?\w+:(.*)', re.DOTALL)

_string_escape_regex = re.compile(r'\\(.)', re.DOTALL)


def _string_escape_replace(match):
    if match.group(1) == 'n':
        return '\n'
    else:
        return match.group(1)  # \", \\ or \ anything


class _Table:
    """
    Internal class used to represent table constructs in the input file. Turned
    into a list of dicts using to_list() when assigned to a value.
    """
    def __init__(self, columns):
        self.columns = columns
        self.rows = list()

    def __repr__(self):
        return f'Table({self.columns}, {len(self.rows)})'

    def to_list(self):
        """
        Turns the table into a list of dictionaries.
        """
        def make_object(row):
            return {name: value for name, value in zip(self.columns, row)}

        return [make_object(row) for row in self.rows]


class Section(dict):
    """
    Represents a section in a spec file.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"Section('{self.name}', {dict.__repr__(self)})"

    def __setitem__(self, name, value):
        if isinstance(value, _Table):
            value = value.to_list()

        if type(name) is tuple:
            # Qualified name
            if not name[0] in self:
                self[name[0]] = Section('[anonymous]')
            elif type(self[name[0]]) != Section:
                raise ValueError('duplicate name "%s"' % name[0])

            # Recurse
            if len(name) == 2:
                self[name[0]][name[1]] = value
            else:
                self[name[0]][name[1:]] = value
        elif name in self:
            raise ValueError('duplicate name "%s"' % name)
        else:
            super().__setitem__(name, value)


class SpecParser(SpecLexer):
    """
    A PLY-based parser for Freeciv INI-like file format.

    This parser can be used to parse Freeciv rulesets, tilesets and saved games.
    The syntax is analyzed by SpecLexer and SpecParser turns it into a list of
    sections. Every section is a dictionary with an additional 'name' attribute
    (see Section). The list of all sections in a file can be retrieved using
    get_all().

    The contents of the sections closely match the input file:

    * Values stored using a qualified name (a.b.c) are turned into nested
      dictionaries.
    * Values stored as a list of values (a, b, c) are turned into a Python list.
    * Values stored as a table ({"a", "b", "c" newline a, b, c} are turned into
      a list of dictionaries.

    Since Freeciv has another internal representation where the position of any
    list index is erased, some syntaxes accepted by Freeciv will not work with
    this parser. For instance, the following are equivalent in the native
    implementation:

        reqs =
            { "type", "name", "range", "present"
              "NationGroup", "Barbarian", "Player"
              "Age", "5", "Local", TRUE
            }

    and:

        reqs.type = "NationGroup", "Age"
        reqs.name = "Barbarian", "5"
        reqs.range = "Player", "Local"
        reqs.present = FALSE, TRUE

    The second form doesn't seem to be in use, and conversion to the first form
    results in more readable code. In general, other functions in this package
    assume the first form is used.
    """

    def p_file(self, p):
        '''
        file : file section
            | file nl
            | section
            | nl section
        '''
        if len(p) == 2:
            # section
            p[0] = [p[1]]
        elif len(p) == 3 and p[1] is _newline_magic:
            # nl section
            p[0] = [p[2]]
        elif len(p) == 3 and p[2] is _newline_magic:
            # file nl
            p[0] = p[1]
        else:
            # file section or file incluse
            p[0] = p[1] + [p[2]]

    def p_nl(self, p):  # New line (collapsing)
        r'''
        nl : '\n'
        | nl '\n'
        '''
        p[0] = _newline_magic  # To identify them later on

    def p_qualified_name(self, p):
        '''
        qualified_name : qualified_name '.' IDENTIFIER
                    | IDENTIFIER
        '''
        if len(p) == 4:
            # First line
            if type(p[1]) == tuple:
                p[0] = p[1] + (p[3],)
            else:
                p[0] = (p[1], p[3])
        else:
            # Second line
            p[0] = p[1]

    def p_scalar(self, p):
        '''
        scalar : STRING_LITERAL
            | NUMBER
            | BOOLEAN
        '''
        if type(p[1]) is str:
            # Drop the translation domain prefix if present
            match = _translation_domain_regex.match(p[1])
            if match:
                p[1] = match.group(1)
            # Resolve escaped characters
            p[1] = _string_escape_regex.sub(_string_escape_replace, p[1])
        p[0] = p[1]

    def p_list(self, p):
        '''
        list : list ',' scalar
            | list ',' nl scalar
            | scalar ',' scalar
            | scalar ',' nl scalar
        '''
        if isinstance(p[1], list):
            p[0] = p[1] + [p[len(p) - 1]]
        else:
            p[0] = [p[1], p[len(p) - 1]]

    def p_table_header(self, p):
        '''
        table_header : STRING_LITERAL
                    | table_header ',' STRING_LITERAL
        '''
        if isinstance(p[1], list):
            # Second line
            p[0] = p[1] + [p[len(p) - 1]]
        else:
            # First line
            p[0] = [p[1]]

    def p_table_contents(self, p):
        '''
        table_contents : table_header
                    | table_contents value
                    | table_contents nl value
        '''
        if len(p) == 2:
            # First line
            p[0] = _Table(p[1])
        else:
            # Second or third lines
            p[0] = p[1]
            p[0].rows += [p[len(p) - 1]]

    def p_table(self, p):
        '''
        table : '{' table_contents '}'
            | '{' nl table_contents '}'
            | '{' table_contents nl '}'
            | '{' nl table_contents nl '}'
        '''
        if p[2] is _newline_magic:
            # '{' nl table_contents...
            p[0] = p[3]
        else:
            # '{' table_contents...
            p[0] = p[2]

    def p_value(self, p):
        '''
        value : scalar
            | list
            | table
        '''
        p[0] = p[1]

    def p_assignment(self, p):
        '''
        assignment : qualified_name '=' value nl
                | qualified_name '=' nl value nl
        '''
        if p[3] is _newline_magic:
            p[0] = (p[1], p[4])
        else:
            p[0] = (p[1], p[3])

    def p_section(self, p):
        '''
        section : SECTION_HEADER nl
                | section assignment
        '''
        if p[2] is _newline_magic:
            # First line
            p[0] = Section(p[1])
        else:
            # Second line
            p[1][p[2][0]] = p[2][1]
            p[0] = p[1]

    def p_error(self, p):
        self._error(p, f'unexpected token: {p.type}')

    def __init__(self, *args):
        """
        Constructor. Arguments are passed to SpecLexer.
        """
        super().__init__(*args)
        self._parser = ply.yacc.yacc(module=self)

    def __iter__(self):
        """
        Returns the next section.
        """
        return self._parser.parse(lexer=self).__iter__()

    def get_all(self):
        """
        Returns a list of all sections.
        """
        return [section for section in self]
