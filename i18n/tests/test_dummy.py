# -*- coding: utf-8 -*-
"""Tests of i18n/dummy.py"""

import os, string, random
from unittest import TestCase

import ddt
from polib import POEntry

import dummy


@ddt.ddt
class TestDummy(TestCase):
    """
    Tests functionality of i18n/dummy.py
    """

    def setUp(self):
        self.converter = dummy.Dummy()

    @ddt.data(
        (u"hello my name is Bond, James Bond",
         u"héllø mý nämé ïs Bønd, Jämés Bønd 𝕃σяєм ι#"),

        (u"don't convert <a href='href'>tag ids</a>",
         u"døn't çønvért <a href='href'>täg ïds</a> 𝕃σяєм ιρѕυ#"),

        (u"don't convert %(name)s tags on %(date)s",
         u"døn't çønvért %(name)s tägs øn %(date)s 𝕃σяєм ιρѕ#"),
    )
    def test_dummy(self, data):
        """
        Tests with a dummy converter (adds spurious accents to strings).
        Assert that embedded HTML and python tags are not converted.
        """
        source, expected = data
        result = self.converter.convert(source)
        self.assertEquals(result, expected, "Mismatch: %r != %r" % (result, expected))

    def test_singular(self):
        entry = POEntry()
        entry.msgid = 'A lovely day for a cup of tea.'
        expected = u'À løvélý däý før ä çüp øf téä. 𝕃σяєм ι#'
        self.converter.convert_msg(entry)
        self.assertEquals(entry.msgstr, expected)

    def test_plural(self):
        entry = POEntry()
        entry.msgid = 'A lovely day for a cup of tea.'
        entry.msgid_plural = 'A lovely day for some cups of tea.'
        expected_s = u'À løvélý däý før ä çüp øf téä. 𝕃σяєм ι#'
        expected_p = u'À løvélý däý før sømé çüps øf téä. 𝕃σяєм ιρ#'
        self.converter.convert_msg(entry)
        result = entry.msgstr_plural
        self.assertEquals(result['0'], expected_s)
        self.assertEquals(result['1'], expected_p)
