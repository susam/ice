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


"""Tests for class Request."""


import unittest
import io
import ice


class RequestTest(unittest.TestCase):

    def test_environ(self):
        r = ice.Request({'foo': 'bar'})
        self.assertEqual(r.environ, {'foo': 'bar'})

    def test_method(self):
        r = ice.Request({'REQUEST_METHOD': 'HEAD'})
        self.assertEqual(r.method, 'HEAD')

    def test_missing_method(self):
        r = ice.Request({})
        self.assertEqual(r.method, 'GET')

    def test_path(self):
        r = ice.Request({'PATH_INFO': '/foo'})
        self.assertEqual(r.path, '/foo')

    def test_missing_path(self):
        r = ice.Request({})
        self.assertEqual(r.path, '/')

    def test_empty_path(self):
        r = ice.Request({'PATH_INFO': ''})
        self.assertEqual(r.path, '/')

    def test_query_with_two_names(self):
        r = ice.Request({'QUERY_STRING': 'a=foo&b=bar'})
        self.assertEqual(r.query.data, {'a': ['foo'], 'b': ['bar']})

    def test_query_with_duplicate_names(self):
        r = ice.Request({'QUERY_STRING': 'a=foo&b=bar&a=baz'})
        self.assertEqual(r.query.data, {'a': ['foo', 'baz'],
                                        'b': ['bar']})

    def test_query_with_missing_value(self):
        r = ice.Request({'QUERY_STRING': 'a=foo&b='})
        self.assertEqual(r.query.data, {'a': ['foo']})

    def test_query_with_no_data(self):
        r = ice.Request({'QUERY_STRING': ''})
        self.assertEqual(r.query.data, {})

    def test_query_with_no_query_string(self):
        r = ice.Request({})
        self.assertEqual(r.query.data, {})

    def test_query_with_plus_sign(self):
        r = ice.Request({'QUERY_STRING': 'a=foo+bar&b=baz'})
        self.assertEqual(r.query.data, {'a': ['foo bar'], 'b': ['baz']})

    def test_query_with_percent_encoding(self):
        r = ice.Request({'QUERY_STRING': 'a=f%6f%6f&b=bar'})
        self.assertEqual(r.query.data, {'a': ['foo'], 'b': ['bar']})

    # environ['REQUEST_METHOD'] = 'POST' is required by cgi.FieldStorage
    # to read bytes from environ['wsgi.input']. Hence, it is defined in
    # every form test.

    def test_form_with_two_names(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo&b=bar'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '11',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo'], 'b': ['bar']})

    def test_form_with_duplicate_names(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo&b=bar&a=baz'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '17',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo', 'baz'],
                                             'b': ['bar']})

    def test_form_with_missing_value(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo&b='),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '8',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo']})

    def test_form_with_no_data(self):
        environ = {
            'wsgi.input': None,
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '0',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {})

    def test_form_with_no_wsgi_input(self):
        r = ice.Request({'REQUEST_METHOD': 'POST'})
        self.assertEqual(r.form.data, {})

    def test_form_with_truncated_data(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '11',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo']})

    def test_form_with_excess_data(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo&b=bar'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '4',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['fo']})

    def test_form_with_plus_sign(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=foo+bar&b=baz'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '15',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo bar'], 'b': ['baz']})

    def test_form_with_percent_encoding(self):
        environ = {
            'wsgi.input': io.BytesIO(b'a=f%6f%6f&b=bar'),
            'REQUEST_METHOD': 'POST',
            'CONTENT_LENGTH': '15',
        }
        r = ice.Request(environ)
        self.assertEqual(r.form.data, {'a': ['foo'], 'b': ['bar']})

    def test_cookies(self):
        environ = {
            'HTTP_COOKIE': 'a=foo; b="bar"; c="baz qux"'
        }
        r = ice.Request(environ)
        self.assertEqual(r.cookies, {'a': 'foo', 'b': 'bar', 'c': 'baz qux'})
