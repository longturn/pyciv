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
import os
import re

from ply.lex import lex

_log = logging.getLogger(__name__)

class SpecLexer:
    """
    A PLY-compatible lexer for Freeciv INI-like file format.

    This lexer can be used to parse Freeciv rulesets, tilesets and saved games.
    See utility/registry_ini.c in the original Freeciv distribution for a
    description of the syntax. Most of it is implemented, except for the
    following items:

    * Old-style arrays (with commas in the identifier) are not supported and
      raise a syntax error.
    * Identifiers are restricted to letters, [A-Za-z_]. The Freeciv
      implementation is more permissive, even though all identifiers used by
      Freeciv seem to follow this schema.
    * String literals included from files, *filename*, are identified correctly
      but the file is not read. A placeholder is used instead.
    * Probably more.

    File inclusion (*include statement) is handled by the lexer, as is done in
    the original implementation.
    """

    # Tokens produced by the lexer (in addition to the literals below)
    tokens = (
        'STRING_LITERAL',
        'SECTION_HEADER',
        'BOOLEAN',
        'NUMBER',
        'INCLUDE',
        'IDENTIFIER',
    )
    # \n matched by WHITESPACE below, include it so we can produce '\n' tokens
    literals = ',.=}{\n'

    def t_GETTEXT_LITERAL(self, t):
        r'''
        _\("                    # Opening
        (
            ([^"]|\\")*[^\\]    # Contents: \" or anything else, no \ at the end
            |                   # Or empty
        )
        "\)                     # Closing
        '''
        t.value = t.value[3:-2]
        t.type = 'STRING_LITERAL'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_PLAIN_LITERAL(self, t):
        r'''
        "                       # Opening
        (
            ([^"]|\\")*[^\\]    # Contents: \" or anything else, no \ at the end
            |                   # Or empty
        )
        "                       # Closing
        '''
        t.value = t.value[1:-1]
        t.type = 'STRING_LITERAL'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_STRING_FROM_FILE(self, t):
        r'\*[^\r\n]+\*'
        t.value = '<Contents of %s>' % t.value[1:-1]
        t.type = 'STRING_LITERAL'
        return t

    def t_COMMENT(self, t):
        r'[;#].*$'

    def t_SECTION_HEADER(self, t):
        r'\[.*\]'
        t.value = t.value[1:-1]
        return t

    def t_NUMBER(self, t):
        r'-?[0-9]+'
        t.value = int(t.value)
        return t

    def t_WHITESPACE(self, t):
        r'\s+'
        if '\n' in t.value:
            # If the whitespace included new lines, produce a newline token
            t.lexer.lineno += t.value.count('\n')
            t.type = '\n'
            return t

    def t_INCLUDE(self, t):
        r'^\*include'
        return t

    def t_IDENTIFIER(self, t):
        r'\w+'
        if t.value.lower() in ('true', 'false'):
            t.type = 'BOOLEAN'
            t.value = (t.value.lower() == 'true')
        return t

    def t_error(self, t):
        """
        Called by PLY when it cannot match any token.
        """
        escaped = t.lexer.lexdata[t.lexer.lexpos].encode('ascii', 'backslashreplace')
        self._error(t, 'illegal character "%s":' % escaped.decode('ascii'))

    def _error(self, t, message):
        """
        Prints an error message pointing to the given token t.
        """
        if t:
            for path in self._file_stack:
                _log.error('In %s:' % path)
            line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
            line_end = t.lexer.lexdata.find('\n', t.lexpos)
            _log.error('Line %d: %s' % (t.lineno, message))
            _log.error(t.lexer.lexdata[line_start:line_end])
            _log.error(' ' * (t.lexpos - line_start) + '^')
        else:
            _log.error('In global context:')
            _log.error(message)

    def __init__(self, file_name, data_path):
        """
        Initializes a parser to read data from the given file. The file is
        located by appending its name to all entries of data_path.
        """
        self.data_path = data_path
        self._lexer_stack = list()
        self._file_stack = list()
        self._push_file(file_name, None)

    def _current_lexer(self):
        """
        Returns the path of the lexer for the file currently being processed.
        """
        return self._lexer_stack[-1]

    def _current_file(self):
        """
        Returns the path of the file currently being processed.
        """
        return self._file_stack[-1]

    def _push_file(self, name, token):
        """
        Pushes a file on the internal stack. The file is looked up in data_path
        (absolute file names are not supported). The token is used in error
        messages.
        """
        # Prevent recursion beyond 20 files.
        if len(self._file_stack) >= 20:
            self._error(token, 'too much recursion')
            return

        # Try to locate the file.
        for location in self.data_path:
            full_path = os.path.join(location, name)
            if os.path.isfile(full_path):
                # Found!
                full_path = os.path.realpath(full_path)

                if full_path in self._file_stack:
                    # But we're already parsing the same file...
                    self._error(token, 'infinite recursion')
                    return

                try:
                    # Push the file to the stacks
                    with open(full_path) as f:
                        lexer = lex(module=self,
                                    reflags=re.UNICODE | re.VERBOSE | re.MULTILINE)
                        lexer.lexpos = 0
                        lexer.lineno = 1
                        lexer.input(f.read())

                        self._file_stack.append(full_path)
                        self._lexer_stack.append(lexer)
                        return
                except e:
                    self._error(token, f'could not open "{full_path}": {e}')

        self._error(token, f'could not find file "{name}"')
        _log.warn('Skipping...')

    def _pop_file(self):
        """
        Pops a file off the internal stack.
        """
        if not self._file_stack:
            raise ValueError('No file to pop')

        self._file_stack = self._file_stack[:-1]
        self._lexer_stack = self._lexer_stack[:-1]

    def _next_token_unwinding_stack(self):
        """
        Unwind the stack until a file with tokens left is found. Returns the
        next token to process (or None if we're really at the end of
        everything).
        """
        token = self._current_lexer().token()
        # Unwind the stack when reaching EOF
        while token is None:
            self._pop_file()
            if not self._file_stack:
                # Reached the end of the stack
                return None
            # Is there something else to process at this level?
            token = self._current_lexer().token()
        return token

    def token(self):
        """
        Retrieves the next token in the stream, or None. Handles file includes.
        """
        token = self._next_token_unwinding_stack()

        # Process *include directives. This is also handled at the token level
        # by the native code.
        if token and token.type == 'INCLUDE':
            # Fetch the next token. It should be a string with the file name.
            next_token = self._current_lexer().token()
            if next_token is None:
                # Got EOF instead.
                self._error(token, f'unexpected end of file')
                # Rewind the stack and present the next token to the parser.
                return self._next_token_unwinding_stack()
            elif next_token.type != 'STRING_LITERAL':
                # Got something that's not a string literal.
                self._error(
                    next_token,
                    f'unexpected token after *include: {next_token.type}')
                # Present whatever we got to the parser.
                return next_token

            # Try to push the file. Does nothing if the file is not found or
            # cannot be read because reasons.
            self._push_file(next_token.value, next_token)

            # Maybe the included file is empty, or its first statement is
            # another *include.
            return self.token()

        return token
