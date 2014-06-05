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

    def test_response_return_value_with_body(self):
        r = ice.Response(mock.Mock())
        r.body = 'foo'
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
