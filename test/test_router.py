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


"""Tests for class Route."""


import unittest
from unittest import mock
import ice


class RouterTest(unittest.TestCase):

    # Implicit route tests

    def test_literal_route_absent(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo', m.f)
        self.assertIsNone(r.resolve('GET', '/'))
        self.assertIsNone(r.resolve('GET', '/bar'))

    def test_literal_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/', m.f)
        r.add('GET', '/foo/bar', m.g)
        r.add('GET', '/foo/bar/baz', m.h)

        self.assertEqual(r.resolve('GET', '/'), (m.f, [], {}))
        self.assertEqual(r.resolve('GET', '/foo/bar'), (m.g, [], {}))
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'), (m.h, [], {}))

    def test_explicit_literal_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'literal:/', m.f)
        r.add('GET', 'literal:/foo/bar', m.g)
        self.assertEqual(r.resolve('GET', '/'), (m.f, [], {}))
        self.assertEqual(r.resolve('GET', '/foo/bar'), (m.g, [], {}))

    def test_wildcard_like_explicit_literal_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'literal:/foo/<b>', m.f)
        r.add('GET', 'literal:/foo/<b:int>', m.g)
        r.add('GET', 'literal:/foo/bar/<:int>', m.h)
        self.assertIsNone(r.resolve('GET', '/foo/bar'))
        self.assertIsNone(r.resolve('GET', '/foo/1'))
        self.assertIsNone(r.resolve('GET', '/foo/bar/1'))
        self.assertEqual(r.resolve('GET', '/foo/<b>'), (m.f, [], {}))
        self.assertEqual(r.resolve('GET', '/foo/<b:int>'), (m.g, [], {}))
        self.assertEqual(r.resolve('GET', '/foo/bar/<:int>'), (m.h, [], {}))

    def test_regex_like_explicit_literal_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'literal:/(.*)', m.f)
        self.assertIsNone(r.resolve('GET', '/foo'))
        self.assertEqual(r.resolve('GET', '/(.*)'), (m.f, [], {}))

    def test_implicit_literal_route_overrides_implict(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo', m.f)
        r.add('GET', '/foo', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, [], {}))

    def test_explicit_literal_route_overrides_implicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo', m.f)
        r.add('GET', 'literal:/foo', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, [], {}))

    def test_implicit_literal_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'literal:/foo', m.h)
        r.add('GET', '/foo', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, [], {}))

    def test_explicit_literal_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'literal:/foo', m.h)
        r.add('GET', 'literal:/foo', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, [], {}))

    def test_regex_ignored_in_literal_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo/.*', m.f)
        self.assertIsNone(r.resolve('GET', '/foo/bar'))
        self.assertEqual(r.resolve('GET', '/foo/.*'), (m.f, [], {}))

    # Wildcard route tests

    def test_wildcard_route_absent(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo/<a>', m.f)
        self.assertIsNone(r.resolve('GET', '/'))
        self.assertIsNone(r.resolve('GET', '/foo'))
        self.assertIsNone(r.resolve('GET', '/foo/'))
        self.assertIsNone(r.resolve('GET', '/foo/bar/'))
        self.assertIsNone(r.resolve('GET', '/foo/bar/baz'))

    def test_explicit_wildcard_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'wildcard:/<>', m.f)
        self.assertEqual(r.resolve('GET', '/foo'), (m.f, ['foo'], {}))

    def test_literal_like_explicit_wildcard_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'wildcard:/foo', m.f)
        self.assertEqual(r.resolve('GET', '/foo'), (m.f, [], {}))

    def test_regex_like_explicit_wildcard_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'wildcard:/<>/(.*)', m.f)
        self.assertIsNone(r.resolve('GET', '/<>/foo'))
        self.assertEqual(r.resolve('GET', '/foo/(.*)'), (m.f, ['foo'], {}))

    def test_implicit_wildcard_route_overrides_implict(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/<>', m.f)
        r.add('GET', '/<>', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, ['foo'], {}))

    def test_explicit_wildcard_route_overrides_implicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/<>', m.f)
        r.add('GET', 'wildcard:/<>', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, ['foo'], {}))

    def test_implicit_wildcard_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'wildcard:/<>', m.f)
        r.add('GET', '/<>', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, ['foo'], {}))

    def test_explicit_wildcard_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'wildcard:/<>', m.f)
        r.add('GET', 'wildcard:/<>', m.g)
        self.assertEqual(r.resolve('GET', '/foo'), (m.g, ['foo'], {}))

    # Regex route test
    def test_regex_route_absent(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '^/([a-z]+)(\d+)$', m.f)
        self.assertIsNone(r.resolve('GET', '/foo'))

    def test_explicit_regex_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'regex:^/foo/.*', m.f)
        self.assertEqual(r.resolve('GET', '/foo/bar'), (m.f, [], {}))

    def test_literal_like_explicit_regex_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'regex:/bar', m.f)
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'), (m.f, [], {}))

    def test_wildcard_like_explicit_regex_route(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'regex:/foo/<:int>', m.f)
        self.assertEqual(r.resolve('GET', '/foo/<:int>'), (m.f, [], {}))

    def test_implicit_regex_route_overrides_implict(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo/(.*)/(.*)', m.f)
        r.add('GET', '/foo/(.*)', m.g)
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'),
                         (m.g, ['bar/baz'], {}))

    def test_explicit_regex_route_overrides_implicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', '/foo/(.*)/(.*)', m.f)
        r.add('GET', 'regex:/foo/(.*)', m.g)
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'),
                         (m.g, ['bar/baz'], {}))

    def test_implicit_regex_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'regex:/foo/(.*)/(.*)', m.f)
        r.add('GET', '/foo/(.*)', m.g)
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'),
                         (m.g, ['bar/baz'], {}))

    def test_explicit_regex_route_overrides_explicit(self):
        r = ice.Router()
        m = mock.Mock()
        r.add('GET', 'regex:/foo/(.*)/(.*)', m.f)
        r.add('GET', 'regex:/foo/(.*)', m.g)
        self.assertEqual(r.resolve('GET', '/foo/bar/baz'),
                         (m.g, ['bar/baz'], {}))
