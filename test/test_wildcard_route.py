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
        self.assertEqual(r.match('/<baz>'), (m, ['<baz>'], {}))
        self.assertIsNone(r.match('/'))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))

        r = ice.WildcardRoute('/<>/<>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo', 'bar'], {}))
        self.assertEqual(r.match('/<foo>/bar'), (m, ['<foo>', 'bar'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('//bar/'))

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
        self.assertEqual(r.match('/<baz>'), (m, [], {'a': '<baz>'}))
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

    def test_anonymous_str_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('/<:str>', m)
        self.assertEqual(r.match('/foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('/bar'), (m, ['bar'], {}))
        self.assertEqual(r.match('/<baz>'), (m, ['<baz>'], {}))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar'))
        self.assertIsNone(r.match('/'))

        r = ice.WildcardRoute('/<:str>/<:str>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo', 'bar'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/foo/'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('//bar/'))

        r = ice.WildcardRoute('/<:str>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo'], {}))
        self.assertEqual(r.match('/<foo>/bar'), (m, ['<foo>'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_named_str_wildcard(self):
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
        self.assertIsNone(r.match('//foo'), (m, [], {}))

        r = ice.WildcardRoute('/<a:str>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': 'foo'}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

    def test_anonymous_path_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('<:path>', m)
        self.assertEqual(r.match('/foo'), (m, ['/foo'], {}))
        self.assertEqual(r.match('/bar'), (m, ['/bar'], {}))
        self.assertEqual(r.match('/<baz>'), (m, ['/<baz>'], {}))
        self.assertEqual(r.match('/foo/'), (m, ['/foo/'], {}))
        self.assertEqual(r.match('/foo/bar'), (m, ['/foo/bar'], {}))
        self.assertEqual(r.match('foo'), (m, ['foo'], {}))
        self.assertEqual(r.match('foo/'), (m, ['foo/'], {}))
        self.assertEqual(r.match('foo/bar'), (m, ['foo/bar'], {}))

        r = ice.WildcardRoute('<:path><:path>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['/foo/ba', 'r'], {}))
        self.assertEqual(r.match('/foo/bar/baz'), (m, ['/foo/bar/ba', 'z'], {}))
        self.assertEqual(r.match('/foo'), (m, ['/fo', 'o'], {}))

        r = ice.WildcardRoute('/<:path>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo'], {}))
        self.assertEqual(r.match('/<foo>/bar'), (m, ['<foo>'], {}))
        self.assertEqual(r.match('/foo/bar/bar'), (m, ['foo/bar'], {}))
        self.assertIsNone(r.match('/foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

        r = ice.WildcardRoute('/<:path>', m)
        self.assertEqual(r.match('/foo/bar'), (m, ['foo/bar'], {}))
        self.assertIsNone(r.match('/'))

    def test_named_path_wildcard(self):
        m = mock.Mock()

        r = ice.WildcardRoute('<a:path>', m)
        self.assertEqual(r.match('/foo'), (m, [], {'a': '/foo'}))
        self.assertEqual(r.match('/bar'), (m, [], {'a': '/bar'}))
        self.assertEqual(r.match('/<baz>'), (m, [], {'a': '/<baz>'}))
        self.assertEqual(r.match('/foo/'), (m, [], {'a': '/foo/'}))
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': '/foo/bar'}))
        self.assertEqual(r.match('foo'), (m, [], {'a': 'foo'}))
        self.assertEqual(r.match('foo/'), (m, [], {'a': 'foo/'}))
        self.assertEqual(r.match('foo/bar'), (m, [], {'a': 'foo/bar'}))

        r = ice.WildcardRoute('<a:path><b:path>', m)
        self.assertEqual(r.match('/foo/bar'),
                         (m, [], {'a': '/foo/ba', 'b': 'r'}))
        self.assertEqual(r.match('/foo/bar/baz'),
                         (m, [], {'a': '/foo/bar/ba', 'b': 'z'}))
        self.assertEqual(r.match('/foo'),
                         (m, [], {'a': '/fo', 'b': 'o'}))

        r = ice.WildcardRoute('/<a:path>/bar', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': 'foo'}))
        self.assertIsNone(r.match('foo'))
        self.assertIsNone(r.match('/bar'))
        self.assertIsNone(r.match('/foo/bar/'))
        self.assertIsNone(r.match('/foo/bar/baz'))

        r = ice.WildcardRoute('/<a:path>', m)
        self.assertEqual(r.match('/foo/bar'), (m, [], {'a': 'foo/bar'}))
        self.assertIsNone(r.match('/'))

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
