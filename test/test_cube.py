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


"""Tests for class ice cube."""


import unittest
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

    def run_app(self):
        threading.Thread(target=self.app.run).start()
        while not self.app.running():
            time.sleep(0.1)

    def test_default_page(self):
        self.run_app()
        response = urllib.request.urlopen('http://127.0.0.1:8080/')
        self.assertEqual(response.read(),
                         b'<!DOCTYPE html>\n'
                         b'<html>\n'
                         b'<head><title>It works!</title></head>\n'
                         b'<body>\n'
                         b'<h1>It works!</h1>\n'
                         b'<p>This is the default ice web page.</p>\n'
                         b'</body>\n'
                         b'</html>\n')

    def test_error_page(self):
        self.run_app()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen('http://127.0.0.1:8080/foo')
        self.assertEqual(cm.exception.code, 404)
        self.assertEqual(cm.exception.read(),
                         b'<!DOCTYPE html>\n'
                         b'<html>\n'
                         b'<head><title>404 Not Found</title></head>\n'
                         b'<body>\n'
                         b'<h1>404 Not Found</h1>\n'
                         b'<p>Nothing matches the given URI</p>\n'
                         b'<hr>\n'
                         b'<address>Ice/' + ice.__version__.encode() +
                         b'</address>\n'
                         b'</body>\n'
                         b'</html>\n')
