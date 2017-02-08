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


"""Tests to verify examples in README.rst."""


import unittest
import urllib.request
import urllib.error
import threading
import time

import ice
from test import data

class ExamplesTest(unittest.TestCase):

    def setUp(self):
        self.app = ice.cube()

    def tearDown(self):
        self.app.exit()

    def run_app(self):
        threading.Thread(target=self.app.run).start()
        while not self.app.running():
            time.sleep(0.1)

    def assert200(self, path, *snippets):
        r = urllib.request.urlopen('http://localhost:8080' + path)
        response = r.read()
        for snippet in snippets:
            self.assertIn(snippet.encode(), response)

    def assert404(self, path):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            r = urllib.request.urlopen('http://localhost:8080' + path)
        self.assertEqual(cm.exception.code, 404)
        self.assertIn(b'<h1>404 Not Found</h1>', cm.exception.read())

    def test_getting_started_example(self):
        self.run_app()
        self.assert200('/', '<h1>It works!</h1>')
        self.assert404('/foo')

    def test_literal_route_example(self):
        app = self.app

        # Example
        @app.get('/')
        def home():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Home</title></head>'
                    '<body><p>Home</p></body></html>')

        @app.get('/foo')
        def foo():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>Foo</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/', '<p>Home</p>')
        self.assert200('/foo', '<p>Foo</p>')
        self.assert404('/foo/')
        self.assert404('/bar')

    def test_anonymous_wildcard_example(self):
        app = self.app

        # Example
        @app.get('/<>')
        def foo(a):
            return ('<!DOCTYPE html>'
                    '<html><head><title>' + a + '</title></head>'
                    '<body><p>' + a + '</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/bar', '<p>bar</p>')
        self.assert404('/foo/')
        self.assert404('/foo/bar')

    def test_named_wildcard_example1(self):
        app = self.app

        # Example
        @app.get('/<a>')
        def foo(a):
            return ('<!DOCTYPE html>'
                    '<html><head><title>' + a + '</title></head>'
                    '<body><p>' + a + '</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/bar', '<p>bar</p>')
        self.assert404('/foo/')
        self.assert404('/foo/bar')

    def test_named_wildcard_example2(self):
        app = self.app

        # Example
        @app.get('/foo/<>-<>/<a>-<b>/<>-<c>')
        def foo(*args, **kwargs):
            return ('<!DOCTYPE html> '
                    '<html><head><title>Example</title></head><body> '
                    '<p>args: {}<br>kwargs: {}</p> '
                    '</body></html>').format(args, kwargs)

        # Test
        self.run_app()
        self.assert200('/foo/hello-world/ice-cube/wsgi-rocks',
                       "args: ('hello', 'world', 'wsgi')",
                       "'a': 'ice'", "'b': 'cube'", "'c': 'rocks'")

    def test_named_wildcard_example3(self):
        app = self.app

        # Example
        @app.get('/<user>/<category>/<>')
        def page(page_id, user, category):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Example</title></head><body> '
                    '<p>page_id: {}<br>user: {}<br>category: {}</p> '
                    '</body></html>').format(page_id, user, category)

        # Test
        self.run_app()
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python<br>user: snowman<br>'
                       'category: articles</p>')

    def test_throwaway_wildcard_example1(self):
        app = self.app

        # Example
        @app.get('/<!>')
        def foo(*args, **kwargs):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Example</title></head><body>'
                    '<p>args: {}<br>kwargs: {}</p>'
                    '</body></html>').format(args, kwargs)

        # Test
        self.run_app()
        self.assert200('/foo', '<p>args: ()<br>kwargs: {}</p>')

    def test_throwaway_wildcard_example2(self):
        app = self.app

        # Example
        @app.get('/<!>/<!>/<>')
        def page(page_id):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Example</title></head><body>'
                    '<p>page_id: ' + page_id + '</p>'
                    '</body></html>')

        # Test
        self.run_app()
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python</p>')

    def test_wildcard_specification_example(self):
        app = self.app

        # Example
        @app.get('/notes/<:path>/<:int>')
        def note(note_path, note_id):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Example</title></head><body>'
                    '<p>note_path: {}<br>note_id: {}</p>'
                    '</body></html>').format(note_path, note_id)

        # Test
        self.run_app()
        self.assert200('/notes/tech/python/12',
                       '<p>note_path: tech/python<br>note_id: 12</p>')
        self.assert200('/notes/tech/python/0',
                       '<p>note_path: tech/python<br>note_id: 0</p>')
        self.assert404('/notes/tech/python/+12')
        self.assert404('/notes/tech/python/+0')
        self.assert404('/notes/tech/python/012')

    def test_regex_route_example1(self):
        app = self.app

        # Example
        @app.get('/(.*)')
        def foo(a):
            return ('<!DOCTYPE html>'
                    '<html><head><title>' + a + '</title></head>'
                    '<body><p>' + a + '</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/foo/bar/', '<p>foo/bar/</p>')

    def test_regex_route_example2(self):
        app = self.app

        # Example
        @app.get('/(?P<user>[^/]*)/(?P<category>[^/]*)/([^/]*)')
        def page(page_id, user, category):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Example</title></head><body>'
                    '<p>page_id: {}<br>user: {}<br>category: {}</p>'
                    '</body></html>').format(page_id, user, category)

        # Test
        self.run_app()
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python<br>user: snowman<br>'
                       'category: articles</p>')

    def test_explicit_literal_route_example(self):
        app = self.app

        # Example
        @app.get('literal:/<foo>')
        def foo():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>Foo</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/<foo>', '<p>Foo</p>')
        self.assert404('/foo')

    def test_explicit_wildcard_route_example(self):
        # Example
        app = self.app
        @app.get('wildcard:/(foo)/<>')
        def foo(a):
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>a: ' + a + '</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/(foo)/bar', '<p>a: bar</p>')
        self.assert404('/foo/<>')

    def test_explicit_regex_route_example(self):
        app = self.app

        # Example
        @app.get('regex:/foo\d*$')
        def foo():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>Foo</p></body></html>')

        # Test
        self.run_app()
        self.assert200('/foo123', '<p>Foo</p>')
        self.assert200('/foo', '<p>Foo</p>')
        self.assert404('/foo\d*$')

    def test_query_string_example1(self):
        app = self.app

        # Example
        @app.get('/')
        def home():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>name: {}</p></body>'
                    '</html>').format(app.request.query['name'])

        # Test
        self.run_app()
        self.assert200('/?name=Humpty+Dumpty',
                       '<p>name: Humpty Dumpty</p>')

    def test_query_string_example2(self):
        app = self.app

        # Example
        @app.get('/')
        def home():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><p>name: {}</p></body>'
                    '</html>').format(app.request.query.getall('name'))

        # Test
        self.run_app()
        self.assert200('/?name=Humpty&name=Santa',
                       "<p>name: ['Humpty', 'Santa']</p>")

    def test_form_example1(self):
        app = self.app

        # Example
        @app.get('/')
        def show_form():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><form action="/result" method="post">'
                    'First name: <input name="firstName"><br>'
                    'Last name: <input name="lastName"><br>'
                    '<input type="submit">'
                    '</form></body></html>')

        @app.post('/result')
        def show_post():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head><body>'
                    '<p>First name: {}<br>Last name: {}</p>'
                    '</body></html>').format(app.request.form['firstName'],
                                             app.request.form['lastName'])

        # Test
        self.run_app()
        self.assert200('/', 'First name')
        form = {'firstName': 'Humpty', 'lastName': 'Dumpty'}
        data = urllib.parse.urlencode(form).encode()
        response = urllib.request.urlopen(
                   'http://localhost:8080/result', data)
        self.assertIn(b'<p>First name: Humpty<br>Last name: Dumpty</p>',
                      response.read() )

    def test_form_example2(self):
        app = self.app

        # Example
        @app.get('/')
        def show_form():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head>'
                    '<body><form action="/result" method="post">'
                    'name1: <input name="name"><br>'
                    'name2: <input name="name"><br>'
                    '<input type="submit">'
                    '</form></body></html>')

        @app.post('/result')
        def show_post():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head><body>'
                    '<p>name (single): {}<br>name (multi): {}</p>'
                    '</body></html>').format(app.request.form['name'],
                                             app.request.form.getall('name'))

        # Test
        self.run_app()
        self.assert200('/', 'name1')
        form = (('name', 'Humpty'), ('name', 'Santa'))
        data = urllib.parse.urlencode(form).encode()
        response = urllib.request.urlopen(
                   'http://localhost:8080/result', data)
        self.assertIn(b'<p>name (single): Santa<br>'
                      b"name (multi): ['Humpty', 'Santa']</p>",
                      response.read() )

    def test_cookie_example(self):
        app = self.app

        @app.get('/')
        def show_count():
            count = int(app.request.cookies.get('count', 0)) + 1
            app.response.set_cookie('count', str(count))
            return ('<!DOCTYPE html>'
                    '<html><head><title>Foo</title></head><body>'
                    '<p>Count: {}</p></body></html>'.format(count))

        # Test
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/')
        self.assertEqual(response.getheader('Set-Cookie'), 'count=1')
        self.assertIn(b'<p>Count: 1</p>', response.read())

        response = urllib.request.urlopen(
            urllib.request.Request('http://localhost:8080/',
            headers={'Cookie': 'count=1'}))
        self.assertEqual(response.getheader('Set-Cookie'), 'count=2')
        self.assertIn(b'<p>Count: 2</p>', response.read())


    def test_error_example(self):
        app = self.app

        # Example
        @app.error(404)
        def error():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Page not found</title></head>'
                    '<body><p>Page not found</p></body></html>')

        # Test
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 404)
        self.assertIn(b'<p>Page not found</p>', cm.exception.read())

    # Set status code and return body
    def test_status_codes_example1(self):
        app = self.app

        # Example
        @app.get('/foo')
        def foo():
            app.response.status = 403
            return ('<!DOCTYPE html>'
                    '<html><head><title>Access is forbidden</title></head>'
                    '<body><p>Access is forbidden</p></body></html>')

        # Test
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 403)
        self.assertIn(b'<p>Access is forbidden</p>', cm.exception.read())

    # Set body and return status code (not recommended)
    def test_status_code_example2(self):
        app = self.app

        # Example
        @app.get('/foo')
        def foo():
            app.response.body = ('<!DOCTYPE html>'
                    '<html><head><title>Access is forbidden</title></head>'
                    '<body><p>Access is forbidden</p></body></html>')
            return 403

        # Test
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 403)
        self.assertIn(b'<p>Access is forbidden</p>', cm.exception.read())

    # Set status code and error handler (recommended)
    def test_status_code_example3(self):
        app = self.app

        # Example
        @app.get('/foo')
        def foo():
            return 403

        @app.error(403)
        def error403():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Access is forbidden</title></head>'
                    '<body><p>Access is forbidden</p></body></html>')

        # Test
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 403)
        self.assertIn(b'<p>Access is forbidden</p>', cm.exception.read())

    # Set return code only (generic error handler is invoked)
    def test_status_code_example4(self):
        app = self.app

        # Example
        @app.get('/foo')
        def foo():
            return 403

        # Test
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 403)
        self.assertIn(b'<h1>403 Forbidden</h1>\n<p>Request forbidden '
                      b'-- authorization will not help</p>\n',
                      cm.exception.read())

    def test_redirect_example1(self):
        app = self.app

        @app.get('/foo')
        def foo():
            return 303, '/bar'

        @app.get('/bar')
        def bar():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Bar</title></head>'
                    '<body><p>Bar</p></body></html>')

        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/foo')
        self.assertIn(b'<p>Bar</p>', response.read())

    def test_redirect_example2(self):
        app = self.app

        @app.get('/foo')
        def foo():
            app.response.add_header('Location', '/bar')
            return 303

        @app.get('/bar')
        def bar():
            return ('<!DOCTYPE html>'
                    '<html><head><title>Bar</title></head>'
                    '<body><p>Bar</p></body></html>')

        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/foo')
        self.assertIn(b'<p>Bar</p>', response.read())

    # Static file with media type guessing
    def test_static_file_example1(self):
        app = self.app

        # Example
        @app.get('/code/<:path>')
        def send_code(path):
            return app.static(data.dirpath, path)

        # Test regular request
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/code/foo.txt')
        self.assertEqual(response.read(), b'foo\n')
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=UTF-8')

        # Test directory traversal attack
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/code/%2e%2e/foo.txt')
        self.assertEqual(cm.exception.code, 403)

    # Static file with explicit media type
    def test_static_file_example2(self):
        app = self.app

        # Example
        @app.get('/code/<:path>')
        def send_code(path):
            return app.static(data.dirpath, path,
                              media_type='text/plain', charset='ISO-8859-1')

        # Test regular request
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/code/foo.c')
        self.assertEqual(b'#include <stdio.h>\n\n'
                         b'int main()\n{\n'
                         b'    printf("hello, world\\n");\n'
                         b'    return 0;\n'
                         b'}\n', response.read())
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=ISO-8859-1')

        # Test directory traversal attack
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/code/%2e%2e/foo.txt')
        self.assertEqual(cm.exception.code, 403)

    def test_download_example1(self):
        app = self.app

        # Example
        @app.get('/foo')
        def foo():
            return app.download('hello, world', 'foo.txt')

        @app.get('/bar')
        def bar():
            return app.download('hello, world', 'bar',
                                media_type='text/plain', charset='ISO-8859-1')

        # Test
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(response.getheader('Content-Disposition'),
                         'attachment; filename="foo.txt"')
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=UTF-8')
        self.assertEqual(b'hello, world', response.read())

        response = urllib.request.urlopen('http://localhost:8080/bar')
        self.assertEqual(response.getheader('Content-Disposition'),
                         'attachment; filename="bar"')
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=ISO-8859-1')
        self.assertEqual(b'hello, world', response.read())

    def test_download_example2(self):
        app = self.app

        # Example
        @app.get('/code/<:path>')
        def send_download(path):
            return app.download(app.static(data.dirpath, path))

        # Test
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/code/foo.txt')
        self.assertEqual(response.getheader('Content-Disposition'),
                         'attachment; filename="foo.txt"')
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=UTF-8')
        self.assertEqual(b'foo\n', response.read())

    def test_download_example3(self):
        app = self.app

        # Example
        @app.get('/<!:path>')
        def send_download():
            return app.download('hello, world')

        # Test
        self.run_app()
        response = urllib.request.urlopen('http://localhost:8080/foo.txt')
        self.assertEqual(response.getheader('Content-Disposition'),
                         'attachment; filename="foo.txt"')
        self.assertEqual(response.getheader('Content-Type'),
                         'text/plain; charset=UTF-8')
        self.assertEqual(b'hello, world', response.read())

        with self.assertRaises(urllib.error.HTTPError) as cm:
            r = urllib.request.urlopen('http://localhost:8080/foo/')
        self.assertEqual(cm.exception.code, 500)

    def test_environ(self):
        app = self.app

        # Example
        @app.get('/')
        def foo():
            user_agent = app.request.environ.get('HTTP_USER_AGENT', None)
            return ('<!DOCTYPE html>'
                    '<html><head><title>User Agent</title></head>'
                    '<body><p>{}</p></body></html>'.format(user_agent))

        # Test
        self.run_app()
        self.assert200('/', 'Python-urllib')
