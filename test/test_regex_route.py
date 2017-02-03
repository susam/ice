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


"""Tests for class ice.WildcardRoute."""


import unittest
from unittest import mock
import ice


class RegexRouteTest(unittest.TestCase):
    def test_regex_without_capturing_groups(self):
        m = mock.Mock()

        r = ice.RegexRoute('/.*', m)
        self.assertEqual(r.match('/.*'), (m, [], {}))
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertEqual(r.match('foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('.*'))
        self.assertIsNone(r.match('foo'))

        r = ice.RegexRoute('^/.*$', m)
        self.assertEqual(r.match('/.*'), (m, [], {}))
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('.*'))
        self.assertIsNone(r.match('foo'))
        self.assertIsNone(r.match('foo/bar'))

        r = ice.RegexRoute(r'/\w{3}', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/bar'), (m, [], {}))
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('/.*'))

        r = ice.RegexRoute(r'^/\w{3}$', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/bar'), (m, [], {}))
        self.assertIsNone(r.match('/.*'))
        self.assertIsNone(r.match('/foo/bar'))

    def test_regex_with_capturing_groups(self):
        m = mock.Mock()

        r = ice.RegexRoute('/(.*)', m)
        self.assertEqual(r.match('/.*'), (m, ['.*'], {}))
        self.assertEqual(r.match('/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('/foo/bar'), (m, ['foo/bar'], {}))
        self.assertEqual(r.match('foo/bar'), (m, ['bar'], {}))
        self.assertIsNone(r.match('.*'))
        self.assertIsNone(r.match('foo'))

        r = ice.RegexRoute('^/(.*)$', m)
        self.assertEqual(r.match('/.*'), (m, ['.*'], {}))
        self.assertEqual(r.match('/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('/foo/bar'), (m, ['foo/bar'], {}))
        self.assertIsNone(r.match('.*'))
        self.assertIsNone(r.match('foo'))
        self.assertIsNone(r.match('foo/bar'))

        r = ice.RegexRoute('/<>/<a>/(.*)', m)
        self.assertEqual(r.match('/<>/<a>/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('~/<>/<a>/foo'), (m, ['foo'], {}))
        self.assertIsNone(r.match('/foo/bar/(.*)'))
        self.assertIsNone(r.match('/foo/bar/baz'))
        self.assertIsNone(r.match('/foo/bar/(baz)'))

        r = ice.RegexRoute('^/<>/<a>/(.*)$', m)
        self.assertEqual(r.match('/<>/<a>/foo'), (m, ['foo'], {}))
        self.assertIsNone(r.match('/foo/bar/(.*)'))
        self.assertIsNone(r.match('/foo/bar/baz'))
        self.assertIsNone(r.match('/foo/bar/(baz)'))
        self.assertIsNone(r.match('~/<>/<a>/foo'))

    def test_regex_with_symbolic_groups(self):
        m = mock.Mock()
        r = ice.RegexRoute('^/(?P<a>(?:foo|bar))$', m)
        self.assertEqual(r.match('/foo'), (m, [], {'a': 'foo'}))
        self.assertEqual(r.match('/bar'), (m, [], {'a': 'bar'}))
        self.assertIsNone(r.match('/foo/bar'))

    def test_regex_with_symbolic_and_non_symbolic_groups(self):
        m = mock.Mock()
        r = ice.RegexRoute('^/([a-z]+)(?:\d+)'
                           '/(?P<a>[a-z/]+)(?P<b>\d+)$', m)
        self.assertEqual(r.match('/foo123/bar456'),
                         (m, ['foo'], {'a': 'bar', 'b': '456'}))
        self.assertIsNone(r.match('/foo123/bar456/'))

    def test_like(self):
        self.assertTrue(ice.RegexRoute.like('^/(?P<a>(?:foo|bar))$'))
        self.assertFalse(ice.RegexRoute.like('^/.*'))
        self.assertFalse(ice.RegexRoute.like('^/<>'))
