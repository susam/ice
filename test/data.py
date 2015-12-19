# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Susam Pal
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


"""Test data related data and utility functions.

This module provides variables and functions to conveniently determine
paths of test data files. This module may be used by unit tests that
need to load test data from filesystem to perform tests.

Attributes:
dirpath -- Absolute path to the base of the test data directory
"""


import os


dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


def filepath(*paths):
    """Join test data directory path and specified path components.

    Arguments:
    paths -- One or more path components specified as separate arguments
             of type str (type: list)

    Return: Concatenation of test directory path and path components
            (type: str)
    """
    return os.path.join(dirpath, *paths)
