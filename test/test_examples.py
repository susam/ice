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


"""Tests to verify examples in README.rst."""


import unittest
import urllib
import threading
import time

import ice

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
        # Example
        app = self.app
        @app.get('/')
        def home():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Home</title></head>' \
                   '<body><p>Home</p></body></html>'

        @app.get('/foo')
        def foo():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>Foo</p></body></html>'
        # Test
        self.run_app()
        self.assert200('/', '<p>Home</p>')
        self.assert200('/foo', '<p>Foo</p>')
        self.assert404('/foo/')
        self.assert404('/bar')

    def test_anonymous_wildcard_example(self):
        # Example
        app = self.app
        @app.get('/<>')
        def foo(a):
            return '<!DOCTYPE html>' \
                   '<html><head><title>' + a + '</title></head>' \
                   '<body><p>' + a + '</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/bar', '<p>bar</p>')
        self.assert404('/foo/')
        self.assert404('/foo/bar')

    def test_named_wildcard_example1(self):
        # Example
        app = self.app
        @app.get('/<a>')
        def foo(a):
            return '<!DOCTYPE html>' \
                   '<html><head><title>' + a + '</title></head>' \
                   '<body><p>' + a + '</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/bar', '<p>bar</p>')
        self.assert404('/foo/')
        self.assert404('/foo/bar')

    def test_named_wildcard_example2(self):
        # Example
        app = self.app
        @app.get('/foo/<>-<>/<a>-<b>/<>-<c>')
        def foo(*args, **kwargs):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>args: {}<br>kwargs: {}</p>' \
                   '</body></html>'.format(args, kwargs)
        self.run_app()

        # Test
        self.assert200('/foo/hello-world/ice-cube/wsgi-rocks',
                       "args: ('hello', 'world', 'wsgi')",
                       "'a': 'ice'", "'b': 'cube'", "'c': 'rocks'")

    def test_named_wildcard_example3(self):
        # Example
        app = self.app
        @app.get('/<user>/<category>/<>')
        def page(page_id, user, category):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>page_id: {}<br>user: {}<br>category: {}</p>' \
                   '</body></html>'.format(page_id, user, category)
        self.run_app()

        # Test
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python<br>user: snowman<br>'
                       'category: articles</p>')

    def test_throwaway_wildcard_example1(self):
        # Example
        app = self.app
        @app.get('/<!>')
        def foo(*args, **kwargs):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>args: {}<br>kwargs: {}</p>' \
                   '</body></html>'.format(args, kwargs)
        self.run_app()

        # Test
        self.assert200('/foo', '<p>args: ()<br>kwargs: {}</p>')

    def test_throwaway_wildcard_example2(self):
        # Example
        app = self.app
        @app.get('/<!>/<!>/<>')
        def page(page_id):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>page_id: ' + page_id + '</p>' \
                   '</body></html>'
        self.run_app()

        # Test
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python</p>')

    def test_wildcard_specification_example(self):
        # Example
        app = self.app
        @app.get('/notes/<:int>')
        def note(note_id):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>note_id: {}</p></body></html>'.format(note_id)
        self.run_app()

        # Test
        self.assert200('/notes/12', '<p>note_id: 12</p>')
        self.assert200('/notes/0', '<p>note_id: 0</p>')
        self.assert404('/notes/+12')
        self.assert404('/notes/+0')
        self.assert404('/notes/012')

    def test_regex_route_example1(self):
        # Example
        app = self.app
        @app.get('/(.*)')
        def foo(a):
            return '<!DOCTYPE html>' \
                   '<html><head><title>' + a + '</title></head>' \
                   '<body><p>' + a + '</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/foo', '<p>foo</p>')
        self.assert200('/foo/bar/', '<p>foo/bar/</p>')

    def test_regex_route_example2(self):
        # Example
        app = self.app
        @app.get('/(?P<user>[^/]*)/(?P<category>[^/]*)/([^/]*)')
        def page(page_id, user, category):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Example</title></head><body>' \
                   '<p>page_id: {}<br>user: {}<br>category: {}</p>' \
                   '</body></html>'.format(page_id, user, category)
        self.run_app()

        # Test
        self.assert200('/snowman/articles/python',
                       '<p>page_id: python<br>user: snowman<br>'
                       'category: articles</p>')

    def test_explicit_literal_route_example(self):
        # Example
        app = self.app
        @app.get('literal:/<foo>')
        def foo():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>Foo</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/<foo>', '<p>Foo</p>')
        self.assert404('/foo')

    def test_explicit_wildcard_route_example(self):
        # Example
        app = self.app
        @app.get('wildcard:/(foo)/<>')
        def foo(a):
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>a: ' + a + '</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/(foo)/bar', '<p>a: bar</p>')
        self.assert404('/foo/<>')

    def test_explicit_regex_route_example(self):
        # Example
        app = self.app
        @app.get('regex:/foo\d*$')
        def foo():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>Foo</p></body></html>'
        self.run_app()

        # Test
        self.assert200('/foo123', '<p>Foo</p>')
        self.assert200('/foo', '<p>Foo</p>')
        self.assert404('/foo\d*$')

    def test_query_string_example1(self):
        # Example
        app = self.app
        @app.get('/')
        def home():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>name: {}</p></body>' \
                   '</html>'.format(app.request.query['name'])
        self.run_app()

        # Test
        self.assert200('/?name=Humpty+Dumpty',
                       '<p>name: Humpty Dumpty</p>')

    def test_query_string_example2(self):
        # Example
        app = self.app
        @app.get('/')
        def home():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><p>name: {}</p></body>' \
                   '</html>'.format(app.request.query.getall('name'))
        self.run_app()

        # Test
        self.assert200('/?name=Humpty&name=Santa',
                       "<p>name: ['Humpty', 'Santa']</p>")

    def test_form_example1(self):
        # Example
        app = self.app
        @app.get('/')
        def show_form():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><form action="/result" method="post">' \
                   'First name: <input name="firstName"><br>' \
                   'Last name: <input name="lastName"><br>' \
                   '<input type="submit">' \
                   '</form></body></html>'

        @app.post('/result')
        def show_post():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head><body>' \
                   '<p>First name: {}<br>Last name: {}</p>' \
                   '</body></html>'.format(app.request.form['firstName'],
                                           app.request.form['lastName'])
        self.run_app()

        # Test
        self.assert200('/', 'First name')
        form = {'firstName': 'Humpty', 'lastName': 'Dumpty'}
        data = urllib.parse.urlencode(form).encode()
        response = urllib.request.urlopen(
                   'http://localhost:8080/result', data)
        self.assertIn(b'<p>First name: Humpty<br>Last name: Dumpty</p>',
                      response.read() )

    def test_form_example2(self):
        # Example
        app = self.app
        @app.get('/')
        def show_form():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head>' \
                   '<body><form action="/result" method="post">' \
                   'name1: <input name="name"><br>' \
                   'name2: <input name="name"><br>' \
                   '<input type="submit">' \
                   '</form></body></html>'

        @app.post('/result')
        def show_post():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Foo</title></head><body>' \
                   '<p>name (single): {}<br>name (multi): {}</p>' \
                   '</body></html>'.format(app.request.form['name'],
                                           app.request.form.getall('name'))
        self.run_app()

        # Test
        self.assert200('/', 'name1')
        form = (('name', 'Humpty'), ('name', 'Santa'))
        data = urllib.parse.urlencode(form).encode()
        response = urllib.request.urlopen(
                   'http://localhost:8080/result', data)
        self.assertIn(b'<p>name (single): Santa<br>' \
                      b"name (multi): ['Humpty', 'Santa']</p>",
                      response.read() )

    def test_error_example(self):
        # Example
        app = self.app
        @app.error(404)
        def error():
            return '<!DOCTYPE html>' \
                   '<html><head><title>Page not found</title></head>' \
                   '<body><p>Page not found</p></body></html>'
        self.run_app()

        # Test
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://localhost:8080/foo')
        self.assertEqual(cm.exception.code, 404)
        self.assertIn(b'<p>Page not found</p>', cm.exception.read())
