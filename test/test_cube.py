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
