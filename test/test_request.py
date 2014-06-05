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
