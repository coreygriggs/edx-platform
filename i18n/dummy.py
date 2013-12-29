# -*- coding: utf-8 -*-
from converter import Converter

# Creates new localization properties files in a dummy language
# Each property file is derived from the equivalent en_US file, except
# 1. Every vowel is replaced with an equivalent with extra accent marks
# 2. Every string is padded out to +30% length to simulate verbose languages (e.g. German)
#    to see if layout and flows work properly
# 3. Every string is terminated with a '#' character to make it easier to detect truncation


# --------------------------------
# Example use:
# >>> from dummy import Dummy
# >>> c = Dummy()
# >>> c.convert("hello my name is Bond, James Bond")
# u'h\xe9ll\xf6 my n\xe4m\xe9 \xefs B\xf6nd, J\xe4m\xe9s B\xf6nd Lorem i#'
#
# >>> c.convert('don\'t convert <a href="href">tag ids</a>')
# u'd\xf6n\'t \xe7\xf6nv\xe9rt <a href="href">t\xe4g \xefds</a> Lorem ipsu#'
#
# >>> c.convert('don\'t convert %(name)s tags on %(date)s')
# u"d\xf6n't \xe7\xf6nv\xe9rt %(name)s t\xe4gs \xf6n %(date)s Lorem ips#"


# Substitute plain characters with accented lookalikes.
# http://tlt.its.psu.edu/suggestions/international/web/codehtml.html#accent
TABLE = {
    'A': u'À',
    'a': u'ä',
    'b': u'ß',
    'C': u'Ç',
    'c': u'ç',
    'E': u'É',
    'e': u'é',
    'I': u'Ì',
    'i': u'ï',
    'O': u'Ø',
    'o': u'ø',
    'U': u'Û',
    'u': u'ü',
    'Y': u'Ý',
    'y': u'ý',
}


# The print industry's standard dummy text, in use since the 1500s
# see http://www.lipsum.com/, then fed through a "fancy-text" converter.

LOREM = " " + " ".join(u"""
    𝕃σяєм ιρѕυм ∂σłσя ѕιт αмєт, ¢σηѕє¢тєтυя α∂ιριѕι¢ιηg єłιт, ѕє∂ ∂σ єιυѕмσ∂
    тємρσя ιη¢ι∂ι∂υηт υт łαвσяє єт ∂σłσяє мαgηα αłιqυα. υт єηιм α∂ мιηιм
    νєηιαм, qυιѕ ησѕтяυ∂ єχєя¢ιтαтιση υłłαм¢σ łαвσяιѕ ηιѕι υт αłιqυιρ єχ єα
    ¢σммσ∂σ ¢σηѕєqυαт.  ∂υιѕ αυтє ιяυяє ∂σłσя ιη яєρяєнєη∂єяιт ιη νσłυρтαтє
    νєłιт єѕѕє ¢ιłłυм ∂σłσяє єυ ƒυgιαт ηυłłα ραяιαтυя. єχ¢єρтєυя ѕιηт σ¢¢αє¢αт
    ¢υρι∂αтαт ηση ρяσι∂єηт, ѕυηт ιη ¢υłρα qυι σƒƒι¢ια ∂єѕєяυηт мσłłιт αηιм ι∂
    єѕт łαвσяυм.""".split()
)

# To simulate more verbose languages (like German), pad the length of a string
# by a multiple of PAD_FACTOR
PAD_FACTOR = 1.3


class Dummy(Converter):
    """
    A string converter that generates dummy strings with fake accents
    and lorem ipsum padding.

    """
    def convert(self, string):
        result = Converter.convert(self, string)
        return self.pad(result)

    def inner_convert_string(self, string):
        for k, v in TABLE.items():
            string = string.replace(k, v)
        return string

    def pad(self, string):
        """add some lorem ipsum text to the end of string"""
        size = len(string)
        if size < 7:
            target = size * 3
        else:
            target = int(size*PAD_FACTOR)
        return string + self.terminate(LOREM[:(target-size)])

    def terminate(self, string):
        """replaces the final char of string with #"""
        return string[:-1] + '#'

    def convert_msg(self, msg):
        """
        Takes one POEntry object and converts it (adds a dummy translation to it)
        msg is an instance of polib.POEntry
        """
        source = msg.msgid
        if not source:
            # don't translate empty string
            return

        plural = msg.msgid_plural
        if plural:
            # translate singular and plural
            foreign_single = self.convert(source)
            foreign_plural = self.convert(plural)
            plural = {
                '0': self.final_newline(source, foreign_single),
                '1': self.final_newline(plural, foreign_plural),
            }
            msg.msgstr_plural = plural
        else:
            foreign = self.convert(source)
            msg.msgstr = self.final_newline(source, foreign)

    def final_newline(self, original, translated):
        """ Returns a new translated string.
            If last char of original is a newline, make sure translation
            has a newline too.
        """
        if original:
            if original[-1] == '\n' and translated[-1] != '\n':
                translated += '\n'
        return translated
