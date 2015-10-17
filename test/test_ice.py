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


"""Tests for class Ice."""


import unittest
import unittest.mock
import ice
import threading
import urllib.request
import textwrap
import time


class IceTest(unittest.TestCase):
    def setUp(self):
        self.app = ice.cube()

    def tearDown(self):
        self.app.exit()    

    def test_not_found(self):
        # Add a route for GET method to ensure HTTP GET is implemented.
        app = ice.Ice()
        app.get('/')(unittest.mock.Mock())
        m = unittest.mock.Mock()
        # Now try to invoke a route that does not exist.
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/foo'}, m)
        expected = '404 Not Found'
        m.assert_called_with(expected, [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_get_route(self):
        expected = '<p>Foo</p>'
        app = ice.Ice()
        @app.get('/')
        def foo():
            return expected

        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '501 Not Implemented'
        r = app({'REQUEST_METHOD': 'POST', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_post_route(self):
        expected = '<p>Foo</p>'
        app = ice.Ice()
        @app.post('/')
        def foo():
            return expected

        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'POST', 'PATH_INFO': '/'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '501 Not Implemented'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_error_in_callback(self):
        app = ice.Ice()
        @app.get('/')
        def foo():
            raise NotImplementedError()

        with self.assertRaises(NotImplementedError) as cm:
            app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'},
                unittest.mock.Mock())

    def test_error_callback(self):
        expected = '<p>HTTP method not implemented</p>'
        app = ice.Ice()
        @app.error(501)
        def error():
            return expected
        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with('501 Not Implemented', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_return_code_from_callback(self):
        app = ice.Ice()
        @app.get('/')
        def foo():
            return 200

        @app.get('/bar')
        def bar():
            return 404

        expected2 = '<p>Baz</p>'
        @app.get('/baz')
        def baz():
            app.response.body = expected2
            return 200

        expected = '200 OK'
        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '404 Not Found'
        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/baz'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected2)))
        ])
        self.assertEqual(r, [expected2.encode()])

    def test_invalid_return_type_from_callback(self):
        app = ice.Ice()
        @app.get('/')
        def foo():
            return []

        with self.assertRaises(ice.Error) as cm:
            app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'},
                unittest.mock.Mock())
        self.assertEqual(str(cm.exception), 'Route callback for GET / '
                         'returned invalid value: list: []')

    def test_invalid_return_code_from_callback(self):
        app = ice.Ice()
        @app.get('/')
        def foo():
            return 1000

        with self.assertRaises(ice.Error) as cm:
            app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'},
                unittest.mock.Mock())
        self.assertEqual(str(cm.exception), 'Route callback for GET / '
                         'returned invalid value: int: 1000')

    def test_run_and_exit(self):
        app = ice.Ice() 
        threading.Thread(target=app.run).start()
        while not app.running():
            time.sleep(0.1)
        app.exit()    
        # Calling another unnecessary exit should cause no problem.
        app.exit()

    def test_run_exit_without_run(self):
        app = ice.Ice()
        app.exit()    
        # Calling another unnecessary exit should cause no problem.
        app.exit()

    def test_run_serve_and_exit(self):
        app = self.app = ice.Ice()
        expected = '<p>Foo</p>'

        @app.get('/')
        def foo():
            return expected

        @app.get('/bar')
        def bar():
            raise NotImplementedError()

        threading.Thread(target=app.run).start()
        while not app.running():
            time.sleep(0.1)

        # 200 OK
        r = urllib.request.urlopen('http://127.0.0.1:8080/')
        self.assertEqual(r.status, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(r.getheader('Content-Type'),
                        'text/html; charset=UTF-8')
        self.assertEqual(r.getheader('Content-Length'),
                         str(len(expected)))
        self.assertEqual(r.read(), expected.encode())

        # 404 Not Found
        expected = '404 Not Found'
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 404)
        self.assertEqual(cm.exception.reason, 'Not Found')
        h = dict(cm.exception.headers)
        self.assertEqual(h['Content-Type'], 'text/html; charset=UTF-8')
        self.assertEqual(h['Content-Length'], str(len(expected)))
        self.assertEqual(cm.exception.read(), expected.encode())

        # 501 Not Implemented
        expected = '501 Not Implemented'
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/', b'')
        self.assertEqual(cm.exception.code, 501)
        self.assertEqual(cm.exception.reason, 'Not Implemented')
        h = dict(cm.exception.headers)
        self.assertEqual(h['Content-Type'], 'text/html; charset=UTF-8')
        self.assertEqual(h['Content-Length'], str(len(expected)))
        self.assertEqual(cm.exception.read(), expected.encode())

        # Exception while processing request
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/bar')
        self.assertEqual(cm.exception.code, 500)
        self.assertEqual(cm.exception.reason, 'Internal Server Error')
