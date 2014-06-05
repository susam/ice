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
from unittest import mock
import ice
import threading
import urllib.request
import textwrap
import time

class IceTest(unittest.TestCase):
    def setUp(self):
        self.app = ice.Ice() 

    def tearDown(self):
        self.app.exit()    

    def run_app(self):
        threading.Thread(target=self.app.run).start()
        while not self.app.running():
            time.sleep(0.1)

    def test_run_and_exit(self):
        self.run_app()

    def test_exit_without_run(self):
        pass

    def test_not_found(self):
        self.app.get('/')(mock.Mock())
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 404)

    def test_get_route(self):
        @self.app.get('/foo')
        def foo():
            return '<p>Foo</p>'
        self.run_app()
        response = urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(response.read(), b'<p>Foo</p>')

    def test_post_route(self):
        @self.app.post('/foo')
        def foo():
            return '<p>Foo</p>'
        self.run_app()
        data = urllib.parse.urlencode({'a': 'foo'}).encode()
        response = urllib.request.urlopen(
                   'http://127.0.0.1:8080/foo', data)
        self.assertEqual(response.read(), b'<p>Foo</p>')

    def test_error_in_callback(self):
        @self.app.get('/foo')
        def foo():
            raise NotImplementedError()
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 500)

    def test_not_implemented_method(self):
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 501)

    def test_error_callback(self):
        self.app.get('/')(mock.Mock())
        @self.app.error(404)
        def error404():
            return '<p>Page does not exist</p>'
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 404)
        self.assertEqual(cm.exception.read(), b'<p>Page does not exist</p>')
