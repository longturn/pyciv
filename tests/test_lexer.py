import pytest

from freeciv.secfile import SpecLexer

MULTILINE_TEST = r""""a\
 b \
c"
"""


def test_multiline(tmp_path):
    f = tmp_path / "multiline.spec"
    f.write_text(MULTILINE_TEST)
    lex = SpecLexer("multiline.spec", [tmp_path])
    tok = lex.token()
    assert tok is not None
    assert tok.type == "STRING_LITERAL"
    assert tok.value == "a\\\n b \\\nc"
