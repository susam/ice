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
