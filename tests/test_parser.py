import pytest

from freeciv.secfile import Section, SpecParser

MULTILINE_TEST = r"""
[test]
str = "a\
 b \
c"
"""


def test_multiline(tmp_path):
    f = tmp_path / "multiline.spec"
    f.write_text(MULTILINE_TEST)
    parser = SpecParser("multiline.spec", [tmp_path])
    sections = [x for x in parser]
    assert len(sections) == 1
    assert isinstance(sections[0], Section)
    assert "str" in sections[0]
    assert sections[0]["str"] == "a b c"
