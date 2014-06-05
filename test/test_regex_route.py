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
