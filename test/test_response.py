# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Susam Pal
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


"""Tests for class Response."""


import unittest
from unittest import mock
import ice


class ResponseTest(unittest.TestCase):

    def test_start_with_no_body(self):
        m = mock.Mock()
        ice.Response(m).response()
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', '0')
        ])

    def test_start_with_body(self):
        m = mock.Mock()
        r = ice.Response(m)
        r.body = 'foo'
        r.response()
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', '3')
        ])

    def test_response_return_value_with_no_body(self):
        self.assertEqual(ice.Response(mock.Mock()).response(), [b''])

    def test_response_return_value_with_str_body(self):
        r = ice.Response(mock.Mock())
        r.body = 'foo'
        self.assertEqual(r.response(), [b'foo'])

    def test_response_return_value_with_bytes_body(self):
        r = ice.Response(mock.Mock())
        r.body = b'foo'
        self.assertEqual(r.response(), [b'foo'])

    def test_status_line(self):
        r = ice.Response(mock.Mock())
        r.status = 400
        self.assertEqual(r.status_line, '400 Bad Request')

    def test_status_phrase(self):
        r = ice.Response(mock.Mock())
        r.status = 400
        self.assertEqual(r.status_detail,
                         'Bad request syntax or unsupported method')

    def test_none_media_type(self):
        m = mock.Mock()
        r = ice.Response(m)
        r.media_type = None
        r.response()
        m.assert_called_with('200 OK', [
            ('Content-Length', '0'),
        ])

    def test_text_media_type(self):
        m = mock.Mock()
        r = ice.Response(m)
        r.media_type = 'text/css'
        r.response()
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/css; charset=UTF-8'),
            ('Content-Length', '0'),
        ])

    def test_non_text_media_type(self):
        m = mock.Mock()
        r = ice.Response(m)
        r.media_type = 'image/png'
        r.response()
        m.assert_called_with('200 OK', [
            ('Content-Type', 'image/png'),
            ('Content-Length', '0'),
        ])

    def test_cookies(self):
        m = mock.Mock()
        r = ice.Response(m)
        r.set_cookie('a', 'foo')
        r.set_cookie('b', 'bar', {'path': '/blog'})
        r.set_cookie('c', 'baz', {'secure': True, 'httponly': True})
        r.set_cookie('d', 'qux', {'PaTh': '/blog', 'SeCuRe': True})
        r.response()
        m.assert_called_with('200 OK', [
            ('Set-Cookie', 'a=foo'),
            ('Set-Cookie', 'b=bar; Path=/blog'),
            ('Set-Cookie', 'c=baz; httponly; secure'),
            ('Set-Cookie', 'd=qux; Path=/blog; secure'),
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', '0')
        ])
