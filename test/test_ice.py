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


"""Tests for class Ice."""


import unittest
import unittest.mock
import ice
import threading
import urllib.request
import textwrap
import time

from test import data


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
            ('Content-Type', 'text/plain; charset=UTF-8'),
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
            ('Content-Type', 'text/plain; charset=UTF-8'),
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
            ('Content-Type', 'text/plain; charset=UTF-8'),
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
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '404 Not Found'
        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/plain; charset=UTF-8'),
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

    def test_redirect(self):
        app = ice.Ice()

        expected = '303 See Other'

        @app.get('/')
        def foo():
            return 303, '/foo'

        expected2 = '<p>Bar</p>'
        @app.get('/bar')
        def bar():
            app.response.body = expected2
            return 303, '/baz'

        m = unittest.mock.Mock()
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Location', '/foo'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with(expected, [
            ('Location', '/baz'),
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected2)))
        ])
        self.assertEqual(r, [expected2.encode()])

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
        self.assertEqual(h['Content-Type'], 'text/plain; charset=UTF-8')
        self.assertEqual(h['Content-Length'], str(len(expected)))
        self.assertEqual(cm.exception.read(), expected.encode())

        # 501 Not Implemented
        expected = '501 Not Implemented'
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/', b'')
        self.assertEqual(cm.exception.code, 501)
        self.assertEqual(cm.exception.reason, 'Not Implemented')
        h = dict(cm.exception.headers)
        self.assertEqual(h['Content-Type'], 'text/plain; charset=UTF-8')
        self.assertEqual(h['Content-Length'], str(len(expected)))
        self.assertEqual(cm.exception.read(), expected.encode())

        # Exception while processing request
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/bar')
        self.assertEqual(cm.exception.code, 500)
        self.assertEqual(cm.exception.reason, 'Internal Server Error')

    def test_static(self):
        app = ice.Ice()

        @app.get('/foo')
        def foo():
            return app.static(data.dirpath, 'foo.txt')

        @app.get('/bar')
        def bar():
            return app.static(data.dirpath, 'bar', 'text/html')

        m = unittest.mock.Mock()

        expected = 'foo\n'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/foo'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '<p>bar</p>\n'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_static_403_error(self):
        app = ice.Ice()

        @app.get('/')
        def foo():
            return app.static(data.filepath('subdir'), '../foo.txt')

        m = unittest.mock.Mock()

        expected = '403 Forbidden'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_static_avoid_403_error(self):
        app = ice.Ice()

        @app.get('/')
        def foo():
            return app.static('/', data.filepath('foo.txt'))

        m = unittest.mock.Mock()

        expected = 'foo\n'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_static_404_error(self):
        app = ice.Ice()

        @app.get('/')
        def foo():
            return app.static(data.dirpath, 'nonexistent.txt')

        m = unittest.mock.Mock()

        expected = '404 Not Found'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_download_with_filename_argument(self):
        app = ice.Ice()

        expected1 = 'foo'
        expected2 = 'echo "hi"'

        @app.get('/')
        def foo():
            return app.download(expected1, 'foo.txt')

        @app.get('/bar')
        def bar():
            return app.download(expected2, 'foo.sh', 'text/plain')

        m = unittest.mock.Mock()

        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="foo.txt"'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected1)))
        ])
        self.assertEqual(r, [expected1.encode()])

        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="foo.sh"'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected2)))
        ])
        self.assertEqual(r, [expected2.encode()])

    def test_download_without_filename_argument(self):
        app = ice.Ice()

        @app.get('/<!>')
        def foo():
            return app.download('foo')

        m = unittest.mock.Mock()
        expected = 'foo'

        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/foo.txt'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="foo.txt"'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/foo.css'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="foo.css"'),
            ('Content-Type', 'text/css; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_download_without_filename(self):
        app = ice.Ice()

        @app.get('/')
        def foo():
            return app.download('foo')

        m = unittest.mock.Mock()
        expected = 'foo'
        with self.assertRaises(ice.LogicError) as cm:
            app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        self.assertEqual(str(cm.exception),
                         'Cannot determine filename for download')

    def test_download_static(self):
        app = ice.Ice()

        @app.get('/')
        def foo():
            return app.download(app.static(data.dirpath, 'foo.txt'))

        m = unittest.mock.Mock()
        expected = 'foo\n'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="foo.txt"'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

    def test_download_with_status_code(self):
        app = ice.Ice()

        # Return an error from app.static.
        @app.get('/')
        def foo():
            return app.download(app.static(data.dirpath, 'nonexistent.txt'))

        # Return an error status code.
        @app.get('/bar')
        def bar():
            return app.download(410)

        # Set body and return status code 200.
        @app.get('/baz')
        def baz():
            app.response.body =  'baz'
            return app.download(200, 'baz.txt')

        m = unittest.mock.Mock()

        expected = '404 Not Found'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = '410 Gone'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/bar'}, m)
        m.assert_called_with(expected, [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])

        expected = 'baz'
        r = app({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/baz'}, m)
        m.assert_called_with('200 OK', [
            ('Content-Disposition', 'attachment; filename="baz.txt"'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(expected)))
        ])
        self.assertEqual(r, [expected.encode()])
