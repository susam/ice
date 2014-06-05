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

class WildcardRouteTest(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(ice.WildcardRoute.tokens(''), [])
        self.assertEqual(ice.WildcardRoute.tokens('/'), ['/'])
        self.assertEqual(ice.WildcardRoute.tokens('//'), ['/', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo//bar'),
                         ['/', 'foo', '/', '/', 'bar'])
        self.assertEqual(ice.WildcardRoute.tokens('foo/'), ['foo', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo'), ['/', 'foo'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/bar'),
                         ['/', 'foo', '/', 'bar'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/bar/'),
                         ['/', 'foo', '/', 'bar', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<>'),
                         ['/', 'foo', '/', '<>'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<>/'),
                         ['/', 'foo', '/', '<>', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<>-<>'),
                         ['/', 'foo', '/', '<>', '-', '<>'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<bar>-<baz>'),
                         ['/', 'foo', '/', '<bar>', '-', '<baz>'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<bar>-<baz>/'),
                         ['/', 'foo', '/', '<bar>', '-', '<baz>', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/<foo:int>-<bar:>/'),
                         ['/', '<foo:int>', '-', '<bar:>', '/'])

    def test_tokens_with_delimiters_in_path(self):
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<<>>/'),
                         ['/', 'foo', '/', '<', '<>', '>', '/'])
        self.assertEqual(ice.WildcardRoute.tokens('/foo/<bar/baz>'),
                         ['/', 'foo', '/', '<', 'bar', '/', 'baz', '>'])

    def test_no_wildcard(self):
        m = mock.Mock()
        r = ice.WildcardRoute('/foo', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'))

    def test_anonymous_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<>', m)
        self.assertEqual(r.match('/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('/bar'), (m, ['bar'], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<>/<>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo', 'bar'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar/'))

        r = ice.WildcardRoute('/<>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_named_wildcard(self):
        m = mock.Mock()
        
        r = ice.WildcardRoute('/<a>', m)
        self.assertEqual(r.match('/foo'), (m, [], {'a': 'foo'}))
        self.assertEqual(r.match('/bar'), (m, [], {'a': 'bar'}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<a>/<b>', m)
        self.assertEqual(r.match('/foo/bar'),
                         (m, [], {'a': 'foo', 'b': 'bar'}))
        self.assertIsNone(r.match('/foo'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))

        r = ice.WildcardRoute('/<a>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': 'foo'}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_throwaway_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<!>', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<!>/<!>', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))

        r = ice.WildcardRoute('/<!>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_throwaway_wildcard_with_colon(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<!:>', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<!:>/<!:>', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))

        r = ice.WildcardRoute('/<!:>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_throwaway_wildcard_with_type(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<!:str>', m)
        self.assertEqual(r.match('/foo'), (m, [], {}))
        self.assertEqual(r.match('/bar'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<!:int>/<!:-int>', m)
        self.assertEqual(r.match('/10/-20'), (m, [], {}))
        self.assertIsNone(r.match('/-10/-20'))
        self.assertIsNone(r.match('/-10'))
        self.assertIsNone(r.match('/foo/bar'))
        self.assertIsNone(r.match('/'))

    def test_anonymous_explicit_str_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<:str>', m)
        self.assertEqual(r.match('/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('/bar'), (m, ['bar'], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<:str>/<:str>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo', 'bar'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar/'))

        r = ice.WildcardRoute('/<:str>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_named_explicit_str_wildcard(self):
        m = mock.Mock()
        
        r = ice.WildcardRoute('/<a:str>', m)
        self.assertEqual(r.match('/foo'), (m, [], {'a': 'foo'}))
        self.assertEqual(r.match('/bar'), (m, [], {'a': 'bar'}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<a:str>/<b:str>', m)
        self.assertEqual(r.match('/foo/bar'),
                         (m, [], {'a': 'foo', 'b': 'bar'}))
        self.assertIsNone(r.match('/foo'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))
        self.assertIsNone(r.match('/foo/'), (m, [], {}))

        r = ice.WildcardRoute('/<a:str>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': 'foo'}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_anonymous_int_wildcard(self):
        m = mock.Mock()
        r = ice.WildcardRoute('/<:int>', m)
        self.assertEqual(r.match('/0'), (m, [0], {}))
        self.assertEqual(r.match('/1'), (m, [1], {}))
        self.assertEqual(r.match('/12'), (m, [12], {}))
        self.assertEqual(r.match('/123'), (m, [123], {}))
        self.assertIsNone(r.match('/-0'))
        self.assertIsNone(r.match('/+0'))
        self.assertIsNone(r.match('/-1'))
        self.assertIsNone(r.match('/+1'))
        self.assertIsNone(r.match('/-12'))
        self.assertIsNone(r.match('/+12'))
        self.assertIsNone(r.match('/-123'))
        self.assertIsNone(r.match('/+123'))
        self.assertIsNone(r.match('/-01'))
        self.assertIsNone(r.match('/01'))
        self.assertIsNone(r.match('/+01'))
        self.assertIsNone(r.match('/-012'))
        self.assertIsNone(r.match('/012'))
        self.assertIsNone(r.match('/+012'))
        self.assertIsNone(r.match('/1foo'))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/1/2'))

    def test_anonymous_positive_int_wildcard(self):
        m = mock.Mock()
        r = ice.WildcardRoute('/<:+int>', m)
        self.assertEqual(r.match('/1'), (m, [1], {}))
        self.assertEqual(r.match('/12'), (m, [12], {}))
        self.assertEqual(r.match('/123'), (m, [123], {}))
        self.assertIsNone(r.match('/-0'))
        self.assertIsNone(r.match('/0'))
        self.assertIsNone(r.match('/+0'))
        self.assertIsNone(r.match('/-1'))
        self.assertIsNone(r.match('/+1'))
        self.assertIsNone(r.match('/-12'))
        self.assertIsNone(r.match('/+12'))
        self.assertIsNone(r.match('/-123'))
        self.assertIsNone(r.match('/+123'))
        self.assertIsNone(r.match('/-01'))
        self.assertIsNone(r.match('/01'))
        self.assertIsNone(r.match('/+01'))
        self.assertIsNone(r.match('/-012'))
        self.assertIsNone(r.match('/012'))
        self.assertIsNone(r.match('/+012'))
        self.assertIsNone(r.match('/1foo'))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/1/2'))

    def test_anonymous_negative_int_wildcard(self):
        m = mock.Mock()
        r = ice.WildcardRoute('/<:-int>', m)
        self.assertEqual(r.match('/0'), (m, [0], {}))
        self.assertEqual(r.match('/-1'), (m, [-1], {}))
        self.assertEqual(r.match('/1'), (m, [1], {}))
        self.assertEqual(r.match('/-12'), (m, [-12], {}))
        self.assertEqual(r.match('/12'), (m, [12], {}))
        self.assertEqual(r.match('/-123'), (m, [-123], {}))
        self.assertEqual(r.match('/123'), (m, [123], {}))
        self.assertIsNone(r.match('/-0'))
        self.assertIsNone(r.match('/+0'))
        self.assertIsNone(r.match('/+1'))
        self.assertIsNone(r.match('/+12'))
        self.assertIsNone(r.match('/+123'))
        self.assertIsNone(r.match('/-01'))
        self.assertIsNone(r.match('/01'))
        self.assertIsNone(r.match('/+01'))
        self.assertIsNone(r.match('/-012'))
        self.assertIsNone(r.match('/012'))
        self.assertIsNone(r.match('/+012'))
        self.assertIsNone(r.match('/1foo'))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/1/2'))

    def test_consecutive_int_wildcard(self):
        m = mock.Mock()
        r = ice.WildcardRoute('/<:int><:-int>', m)
        self.assertEqual(r.match('/123'), (m, [12, 3], {}))
        self.assertEqual(r.match('/00'), (m, [0, 0], {}))
        self.assertEqual(r.match('/12-3'), (m, [12, -3], {}))
        self.assertIsNone(r.match('/12+3'))
        self.assertIsNone(r.match('/-12-3'))
        self.assertIsNone(r.match('/12-3-4'))
        self.assertIsNone(r.match('/000'))
        self.assertIsNone(r.match('/0000'))

    def test_regex_ineffective_in_wildcard(self):
        # Any regular expression should get escaped by ice.WildcardRoute
        # so that they match literal strings
        m = mock.Mock()

        r = ice.WildcardRoute('/.*', m)
        self.assertEqual(r.match('/.*'), (m, [], {}))
        self.assertIsNone(r.match('/foo'))

        r = ice.WildcardRoute('/(.*)', m)
        self.assertEqual(r.match('/(.*)'), (m, [], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/(foo)'))

        r = ice.WildcardRoute(r'/\w{3}', m)
        self.assertEqual(r.match('/\w{3}'), (m, [], {}))
        self.assertIsNone(r.match('/foo'))

        r = ice.WildcardRoute('/<>/<a>/(.*)', m)
        self.assertEqual(r.match('/foo/bar/(.*)'),
                         (m, ['foo'], {'a': 'bar'}))
        self.assertIsNone(r.match('/foo/bar/baz'))
        self.assertIsNone(r.match('/foo/bar/(baz)'))

    def test_like(self):
        self.assertTrue(ice.WildcardRoute.like('/<>'))
        self.assertTrue(ice.WildcardRoute.like('/<<>>'))
        self.assertTrue(ice.WildcardRoute.like('/<foo>'))
        self.assertFalse(ice.WildcardRoute.like('/</>'))
        self.assertFalse(ice.WildcardRoute.like('/<foo/bar>'))
        self.assertFalse(ice.WildcardRoute.like('/.*'))
        self.assertFalse(ice.WildcardRoute.like('/(.*)'))
        self.assertFalse(ice.WildcardRoute.like('/foo'))
