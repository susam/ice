# The MIT License (MIT)
#
# Copyright (c) 2014-2017 Susam Pal
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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

    def test_path_wildcards(self):
        wildcard = ice.Wildcard('<:path>')
        self.assertEqual(wildcard.value('/foo'), '/foo')

        wildcard = ice.Wildcard('<a:path>')
        self.assertEqual(wildcard.value('/foo'), '/foo')

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
        ice.Wildcard('<:path>')
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
