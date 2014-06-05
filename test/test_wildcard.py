# Copyright (c) 2014 Susam Pal
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Tests for class Wildcard."""


import unittest
import ice


class WildcardTest(unittest.TestCase):

    def test_str_wildcards(self):
        wildcard = ice.Wildcard('<>')
        self.assertEqual(wildcard.value(''), '')
        self.assertEqual(wildcard.value('foo'), 'foo')
        self.assertEqual(wildcard.value('-15'), '-15')
        self.assertEqual(wildcard.value('0'), '0')
        self.assertEqual(wildcard.value('10'), '10')

        wildcard = ice.Wildcard('<a>')
        self.assertEqual(wildcard.value(''), '')
        self.assertEqual(wildcard.value('foo'), 'foo')
        self.assertEqual(wildcard.value('10.2'), '10.2')
        self.assertEqual(wildcard.value('-15'), '-15')
        self.assertEqual(wildcard.value('0'), '0')
        self.assertEqual(wildcard.value('10'), '10')

        wildcard = ice.Wildcard('<a:>')
        self.assertEqual(wildcard.value(''), '')
        self.assertEqual(wildcard.value('foo'), 'foo')
        self.assertEqual(wildcard.value('10.2'), '10.2')
        self.assertEqual(wildcard.value('-15'), '-15')
        self.assertEqual(wildcard.value('0'), '0')
        self.assertEqual(wildcard.value('10'), '10')

        wildcard = ice.Wildcard('<:str>')
        self.assertEqual(wildcard.value(''), '')
        self.assertEqual(wildcard.value('foo'), 'foo')
        self.assertEqual(wildcard.value('10.2'), '10.2')
        self.assertEqual(wildcard.value('-15'), '-15')
        self.assertEqual(wildcard.value('0'), '0')
        self.assertEqual(wildcard.value('10'), '10')

        wildcard = ice.Wildcard('<a:str>')
        self.assertEqual(wildcard.value(''), '')
        self.assertEqual(wildcard.value('foo'), 'foo')
        self.assertEqual(wildcard.value('10.2'), '10.2')
        self.assertEqual(wildcard.value('-15'), '-15')
        self.assertEqual(wildcard.value('0'), '0')
        self.assertEqual(wildcard.value('10'), '10')

    def test_int_wildcards(self):
        wildcard = ice.Wildcard('<:int>')
        self.assertEqual(wildcard.value('0'), 0)
        self.assertEqual(wildcard.value('10'), 10)

        wildcard = ice.Wildcard('<a:int>')
        self.assertEqual(wildcard.value('0'), 0)
        self.assertEqual(wildcard.value('10'), 10)

    def test_positive_int_wildcards(self):
        wildcard = ice.Wildcard('<:+int.')
        self.assertEqual(wildcard.value('10'), 10)

        wildcard = ice.Wildcard('<a:+int>')
        self.assertEqual(wildcard.value('10'), 10)

    def test_negative_int_wildcards(self):
        wildcard = ice.Wildcard('<:-int>')
        self.assertEqual(wildcard.value('-15'), -15)
        self.assertEqual(wildcard.value('0'), 0)
        self.assertEqual(wildcard.value('10'), 10)

        wildcard = ice.Wildcard('<a:-int>')
        self.assertEqual(wildcard.value('-15'), -15)
        self.assertEqual(wildcard.value('0'), 0)
        self.assertEqual(wildcard.value('10'), 10)

    def test_name_validation(self):
        # No errors on positive test cases 
        ice.Wildcard('<>')
        ice.Wildcard('<:>')
        ice.Wildcard('<_>')
        ice.Wildcard('<_:>')
        ice.Wildcard('<foo>')
        ice.Wildcard('<foo:>')
        ice.Wildcard('<_foo>')
        ice.Wildcard('<_foo:>')
        ice.Wildcard('<__foo_bar>')
        ice.Wildcard('<__foo_bar:>')
        ice.Wildcard('<!>')
        ice.Wildcard('<!:>')

        # Errors on negative test cases
        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<@foo>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '@foo' in '<@foo>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<foo!>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name 'foo!' in '<foo!>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('< >')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name ' ' in '< >'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<! >')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '! ' in '<! >'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<!!>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '!!' in '<!!>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<!_>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '!_' in '<!_>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<!foo>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '!foo' in '<!foo>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<!_foo>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '!_foo' in '<!_foo>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<!__foo_bar>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '!__foo_bar' in "
                         "'<!__foo_bar>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<%>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard name '%' in '<%>'")


    def test_type_validation(self):
        # No errors on positive test cases 
        ice.Wildcard('<>')
        ice.Wildcard('<:>')
        ice.Wildcard('<:str>')
        ice.Wildcard('<:int>')
        ice.Wildcard('<:+int>')
        ice.Wildcard('<:-int>')

        # Errors on negative test cases
        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<:int*>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard type 'int*' in '<:int*>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<:str+>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard type 'str+' in '<:str+>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<:str+>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard type 'str+' in '<:str+>'")

        with self.assertRaises(ice.RouteError) as cm:
            ice.Wildcard('<:!>')
        self.assertEqual(str(cm.exception),
                         "Invalid wildcard type '!' in '<:!>'")
