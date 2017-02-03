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


"""Tests for class MultiDict."""


import unittest
import ice


class MultiDictTest(unittest.TestCase):

    def test_setitem(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        d['b'] = 'bar'
        d['b'] = 'baz'
        self.assertEqual(d.data, {'a': ['foo'], 'b': ['bar', 'baz']})

    def test_getitem(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        self.assertEqual(d['a'], 'foo')

    def test_get(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        self.assertEqual(d.get('a'), 'foo')
        self.assertEqual(d.get('b', 'bar'), 'bar')

    def test_getitem_for_multiple_values(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        d['a'] = 'bar'
        self.assertEqual(d['a'], 'bar')

    def test_len(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        d['b'] = 'bar'
        d['b'] = 'baz'
        self.assertEqual(len(d), 2)

    def test_missing_key(self):
        d = ice.MultiDict()
        with self.assertRaises(KeyError) as cm:
            d['foo']
        self.assertEqual(str(cm.exception), "'foo'")

    def test_getall_for_single_value(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        self.assertEqual(d.getall('a'), ['foo'])

    def test_getall_for_multiple_value(self):
        d = ice.MultiDict()
        d['a'] = 'foo'
        d['a'] = 'bar'
        self.assertEqual(d.getall('a'), ['foo', 'bar'])

    def test_getall_for_missing_key(self):
        d = ice.MultiDict()
        self.assertEqual(d.getall('a'), [])

    def test_getall_default_value_for_missing_key(self):
        d = ice.MultiDict()
        self.assertEqual(d.getall('a', 'foo'), 'foo')
