Ice - WSGI on the rocks
=======================

Ice is a Python module with a WSGI microframework meant for developing
small web applications in Python.

.. image:: https://travis-ci.org/susam/ice.svg?branch=master
   :target: https://travis-ci.org/susam/ice

.. image:: https://coveralls.io/repos/susam/ice/badge.svg?branch=master
   :target: https://coveralls.io/r/susam/ice?branch=master

.. contents::
   :backlinks: none


Requirements
------------
This module should be used with Python 3.4 or any later version of
Python interpreter.

This module depends only on the Python standard library. It does not
depend on any third party libraries.


Installation
------------
You can install this module using pip3 using the following command. ::

    pip3 install ice

You can install this module from source distribution. To do so,
download the latest .tar.gz file from https://pypi.python.org/pypi/ice,
extract it, then open command prompt or shell, and change your current
directory to the directory where you extracted the source distribution,
and then execute the following command. ::

    python3 setup.py install

Note that on a Windows system, you may have to replace ``python3`` with
the path to your Python 3 interpreter.


Support
-------
To report any bugs, or ask any question, please visit
https://github.com/susam/ice/issues.


Resources
---------
Here is a list of useful links about this project.

- `Latest release on PyPI <https://pypi.python.org/pypi/ice>`_
- `Source code on GitHub <https://github.com/susam/ice>`_
- `Issue tracker on GitHub <https://github.com/susam/ice/issues>`_
- `Changelog on GitHub
  <https://github.com/susam/ice/blob/master/CHANGES.rst>`_


License
-------
This is free software. You are permitted to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of it, under the
terms of the MIT License. See `LICENSE.rst`_ for the complete license.

This software is provided WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
`LICENSE.rst`_ for the complete disclaimer.

.. _LICENSE.rst: https://github.com/susam/ice/blob/master/LICENSE.rst


Tutorial
========

Getting started
---------------
The simplest way to get started with an ice application is to write a
minimal application that serves a default web page.

.. code:: python

    import ice
    app = ice.cube()
    if __name__ == '__main__':
       app.run()

Save the above code in a file and execute it with your Python
interpreter. Then open your browser, visit http://localhost:8080/, and
you should be able to see a web page that says, 'It works!'.

..  reST convention
    ---------------
    - URLs are written in plain text.
    - Request paths are written in plain text.
    - Request path patterns are enclosed in `` and ``.
    - Code samples are written in literal blocks constructed with the
      code directive.
    - Strings, even when they are part of a request path, are enclosed
      in ``' and '``.


Routes
------
Once you are able to run a minimal ice application as mentioned in the
previous section, you'll note that while visiting http://localhost:8080/
displays the default 'It works!' page, visiting any other URL, such as
http://localhost:8080/foo displays the '404 Not Found' page. This
happens because the application object returned by the ``ice.cube``
function has a default route defined to invoke a function that returns
the default page when the client requests / using the HTTP GET method.
There is no such route defined by default for /foo or any request path
other than /.

In this document, a request path is defined as the part of the URL after
the domain name and before the query string. For example, in a request
for http://localhost:8080/foo/bar?x=10, the request path is /foo/bar.

A route is used to map an HTTP request to a Python callable. A route
consists of three objects:

1. HTTP request method, e.g. ``'GET'``, ``'POST'``.
2. Request path pattern, e.g. ``'/foo'``, ``'/post/<id>'``, ``'/(.*)'``.
3. Callable, e.g. Python function

A route is said to match a request path when the request pattern of the
route matches the request path. When a client makes a request to an ice
application, if a route matches the request path, then the callable of
the route is invoked and the value returned by the callable is used to
send a response to the client.

The request path pattern of a route can be specified in one of three
ways:

1. Literal path, e.g. ``'/'``, ``'/contact/'``, ``'/about/'``.
2. Pattern with wildcards, e.g. ``'/blog/<id>'``, ``'/order/<:int>'``.
3. Regular expression, e.g. ``'/blog/\w+'``, ``'/order/\d+'``.

These three types of routes are described in the subsections below.

Literal routes
~~~~~~~~~~~~~~
The following application overrides the default 'It works!' page for /
with a custom page. Additionally, it sets up a route for /foo.

.. code:: python

    import ice
    app = ice.cube()

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

    if __name__ == '__main__':
        app.run()

The routes defined in the above example are called literal routes
because they match the request path exactly as specified in the argument
to ``app.get`` decorator. Routes defined with the ``app.get`` decorator
matches HTTP GET requests. Now, visiting http://localhost:8080/ displays
a page with the following text.

    | Home

Visiting http://localhost:8080/foo displays a page with the following
text.

    | Foo

However, visiting http://localhost:8080/foo/ or
http://localhost:8080/foo/bar displays the '404 Not Found' page because
the literal pattern ``'/foo'`` does not match the request path
``'/foo/'`` or ``'/foo/bar'``.

Wildcard routes
~~~~~~~~~~~~~~~
Anonymous wildcards
'''''''''''''''''''
The following code example is the simplest application demonstrating a
wildcard route that matches request path of the form ``/`` followed by
any string devoid of ``/``, ``<`` and ``>``. The characters ``<>`` is an
anonymous wildcard because there is no name associated with this
wildcard. The part of the request path matched by an anonymous wildcard
is passed as a positional argument to the route's callable.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/<>')
    def foo(a):
        return ('<!DOCTYPE html>'
                '<html><head><title>' + a + '</title></head>'
                '<body><p>' + a + '</p></body></html>')

    if __name__ == '__main__':
        app.run()

Save the above code in a file and execute it with Python interpreter.
Then open your browser, visit http://localhost:8080/foo, and you should
be able to see a page with the followning text.

    | foo

If you visit http://localhost:8080/bar instead, you should see a page
with the following text.

    | bar

However, visiting http://localhost:8080/foo/ or
http://localhost:8080/foo/bar displays the '404 Not Found' page because
the wildcard based pattern ``/<>`` does not match ``/foo/`` or
``/foo/bar``.

Named wildcards
'''''''''''''''
A wildcard with a valid Python identifier as its name is called a named
wildcard. The part of the request path matched by a named wildcard is
passed as a keyword argument, with the same name as that of the
wildcard, to the route's callable.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/<a>')
    def foo(a):
        return ('<!DOCTYPE html>'
                '<html><head><title>' + a + '</title></head>'
                '<body><p>' + a + '</p></body></html>')

    if __name__ == '__main__':
        app.run()

The ``a``, in ``<a>``, is the name of the wildcard. The ice application
in this example with a named wildcard behaves similar to the earlier one
with an anonymous wildcard. The following example code clearly
demonstrates how matches due to anonymous wildcards are passed
differently from the matches due to named wildcards.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/foo/<>-<>/<a>-<b>/<>-<c>')
    def foo(*args, **kwargs):
        return ('<!DOCTYPE html> '
                '<html><head><title>Example</title></head><body> '
                '<p>args: {}<br>kwargs: {}</p> '
                '</body></html>').format(args, kwargs)

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/foo/hello-world/ice-cube/wsgi-rocks displays a
page with the following text.

    | args: ('hello', 'world', 'wsgi')
    | kwargs: {'a': 'ice', 'b': 'cube', 'c': 'rocks'}

Here is a more typical example that demonstrates how anonymous wildcard
and named wildcard may be used together.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/<user>/<category>/<>')
    def page(page_id, user, category):
        return ('<!DOCTYPE html>'
                '<html><head><title>Example</title></head><body> '
                '<p>page_id: {}<br>user: {}<br>category: {}</p> '
                '</body></html>').format(page_id, user, category)

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/snowman/articles/python displays a page with the
following text.

    | page_id: python
    | user: snowman
    | category: articles

Note: Since parts of the request path matched by anonymous wildcards are
passed as positional arguments and parts of the request path matched by
named wildcards are passed as keyword arguments to the route's callable,
it is required by the Python language that all positional arguments
must come before all keyword arguments in the function definition.
However, the wildcards may appear in any order in the route's pattern.

Throwaway wildcard
''''''''''''''''''
A wildcard with exclamation mark, ``!``, as its name is a throwaway
wildcard. The part of the request path matched by a throwaway wildcard
is not passed to the route's callable. *They are thrown away!*

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/<!>')
    def foo(*args, **kwargs):
        return ('<!DOCTYPE html>'
                '<html><head><title>Example</title></head><body>'
                '<p>args: {}<br>kwargs: {}</p>'
                '</body></html>').format(args, kwargs)

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | args: ()
    | kwargs: {}

The output confirms that no argument is passed to the ``foo`` function.
Here is a more typical example that demonstrates how a throwaway
wildcard may be used with other wildcards.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/<!>/<!>/<>')
    def page(page_id):
        return ('<!DOCTYPE html>'
                '<html><head><title>Example</title></head><body>'
                '<p>page_id: ' + page_id + '</p>'
                '</body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/snowman/articles/python should display a page with
the following text.

    | page_id: python

There are three wildcards in the route's request path pattern but there
is only one argument in the route's callable because two out of the
three wildcards are throwaway wildcards.

Wildcard specification
''''''''''''''''''''''
The complete syntax of a wildcard specification is: <*name*:*type*>.

The following rules describe how a wildcard is interpreted.

1.  The delimiters ``<`` (less-than sign) and ``>`` (greater-than sign),
    are mandatory.
2.  However, *name*, ``:`` (colon) and *type* are optional.
3.  Either a valid Python identifier or the exclamation mark, ``!``,
    must be specified as *name*.
4.  If *name* is missing, the part of the request path matched by the
    wildcard is passed as a positional argument to the route's callable.
5.  If *name* is present and it is a valid Python identifier, the part
    of the request path matched by the wildcard is passed as a keyword
    argument to the route's callable.
6.  If *name* is present and it is ``!``, the part of the request path
    matched by the wildcard is not passed to the route's callable.
7.  If *name* is present but it is neither ``!`` nor a valid Python
    identifier, ice.RouteError is raised.
8.  If *type* is present, it must be preceded by ``:`` (colon).
9.  If *type* is present but it is not ``str``, ``path``, ``int``,
    ``+int`` and ``-int``, ice.RouteError is raised.
10. If *type* is missing, it is assumed to be ``str``.
11. If *type* is ``str``, it matches a string of one or more characters
    such that none of the characters is ``/``. The path of the request
    path matched by the wildcard is passed as an ``str`` object to the
    route's callable.
12. If *type* is ``path``, it matches a string of one or more characters
    that may contain ``/``. The path of the request path matched by the
    wildcard is passed as an ``str`` object to the route's callable.
13. If *type* is ``int``, ``+int`` or ``-int``, the path of the request
    path matched by the wildcard is passed as an ``int`` object to the
    route's callable.
14. If *type* is ``+int``, the wildcard matches a positive integer
    beginning with a non-zero digit.
15. If *type* is ``int``, the wildcard matches ``0`` as well as
    everything that a wildcard of type ``+int`` matches.
16. If *type* is ``-int``, the wildcard matches a negative integer that
    begins with the ``-`` sign followed by a non-zero digit as well as
    everything that a wildcard of type ``int`` matches.

Here is an example that demonstrates a typical route with ``path`` and
``int`` wildcards.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/notes/<:path>/<:int>')
    def note(note_path, note_id):
        return ('<!DOCTYPE html>'
                '<html><head><title>Example</title></head><body>'
                '<p>note_path: {}<br>note_id: {}</p>'
                '</body></html>').format(note_path, note_id)

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/notes/tech/python/12 displays a page with the
following text.

    | note_path: tech/python
    | note_id: 12

Visiting http://localhost:8080/notes/tech/python/0 displays a page with
the following text.

    | note_path: tech/python
    | note_id: 0

However, visiting http://localhost:8080/notes/tech/python/+12
http://localhost:8080/notes/tech/python/+0 or
http://localhost:8080/notes/tech/python/012, displays the
'404 Not Found' page because ``<:int>`` does not match an integer with a
leading ``+`` sign or with a leading ``0``. It matches ``0`` and a
positive integer beginning with a non-zero digit only.

Regular expression routes
~~~~~~~~~~~~~~~~~~~~~~~~~
The following code demonstrates a simple regular expression based route.
The part of the request path matched by a non-symbolic capturing group
is passed as a positional argument to the route's callable.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/(.*)')
    def foo(a):
        return ('<!DOCTYPE html>'
                '<html><head><title>' + a + '</title></head>'
                '<body><p>' + a + '</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | foo

Visiting http://localhost:8080/foo/bar/ displays a page with the
following text.

    | foo/bar/

The part of the request path matched by a symbolic capturing group in
the regular expression is passed as a keyword argument with the same
name as that of the symbolic group.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/(?P<user>[^/]*)/(?P<category>[^/]*)/([^/]*)')
    def page(page_id, user, category):
        return ('<!DOCTYPE html>'
                '<html><head><title>Example</title></head><body>'
                '<p>page_id: {}<br>user: {}<br>category: {}</p>'
                '</body></html>').format(page_id, user, category)

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/snowman/articles/python displays a page with the
following text.

    | page_id: python
    | user: snowman
    | category: articles

Note: Since parts of the request path matched by non-symbolic capturing
groups are passed as positional arguments and parts of the request path
matched by symbolic capturing groups are passed as keyword arguments to
the route's callable, it is required by the Python language that all
positional arguments must come before all keyword arguments in the
function definition. However, the capturing groups may appear in any
order in the route's pattern.

Interpretation of request path pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The request path pattern is interpreted according to the following
rules. The rules are processed in the order specified and as soon as one
of the rules succeeds in determining how the request path pattern should
be interpreted, further rules are not processed.

1. If a route's request path pattern begins with ``regex:`` prefix,
   then it is interpreted as a regular expression route.
2. If a route's request path pattern begins with ``wildcard:`` prefix,
   then it is interpreted as a wildcard route.
3. If a route's request path pattern begins with ``literal:`` prefix,
   then it is interpreted as a literal route.
4. If a route's request path pattern contains what looks like a
   regular expression capturing group, i.e. it contains ``(`` before
   ``)`` somewhere in the pattern, then it is automatically interpreted
   as a regular expression route.
5. If a route's request path pattern contains what looks like a
   wildcard, i.e. it contains ``<`` before ``>`` somewhere in the
   pattern with no ``/``, ``<`` and ``>`` in between them, then it is
   automatically interpreted as a wildcard route.
6. If none of the above rules succeed in determining how to interpret
   the request path, then it is interpreted as a literal route.

The next three sections clarify the above rules with some contrived
examples.

Explicit literal routes
'''''''''''''''''''''''
To define a literal route with the request path pattern as ``/<foo>``,
``literal:`` prefix must be used. Without it, the ``<foo>`` in the
pattern is interpreted as a wildcard and the route is defined as a
wildcard route. With the ``literal:`` prefix, the pattern is explicitly
defined as a literal pattern.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('literal:/<foo>')
    def foo():
        return ('<!DOCTYPE html>'
                '<html><head><title>Foo</title></head>'
                '<body><p>Foo</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/%3Cfoo%3E displays a page containing the
following text.

    | Foo

A request path pattern that seems to contain a wildcard or a capturing
group but needs to be treated as a literal pattern must be prefixed with
the string ``literal:``.

Explicit wildcard routes
''''''''''''''''''''''''
To define a wildcard route with the request path pattern as
``/(foo)/<>``, the ``wildcard:`` prefix must be used. Without it, the
pattern is interpreted as a regular expression pattern because the
``(foo)`` in the pattern looks like a regular expression capturing
group.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('wildcard:/(foo)/<>')
    def foo(a):
        return ('<!DOCTYPE html>'
                '<html><head><title>Foo</title></head>'
                '<body><p>a: ' + a + '</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/(foo)/bar
displays a page with the following text.

    | a: bar

A request path pattern that seems to contain a regular expression
capturing group but needs to be treated as a wildcard pattern must be
prefixed with the string ``wildcard:``.

Explicit regular expression routes
''''''''''''''''''''''''''''''''''
To define a regular expression route with the request path pattern as
``^/foo\d*$``, the ``regex:`` prefix must be used. Without it, the
pattern is interpreted as a literal pattern because there is no
capturing group in the pattern.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('regex:/foo\d*$')
    def foo():
        return ('<!DOCTYPE html>'
                '<html><head><title>Foo</title></head>'
                '<body><p>Foo</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo or
http://localhost:8080/foo123 displays a page containing the following
text.

    | Foo

A request path pattern that does not contain a regular expression
capturing group but needs to be treated as a regular expression pattern
must be prefixed with the string ``regex:``.


Query strings
-------------
The following example shows an application that can process a query
string in a GET request.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/')
    def home():
        return ('<!DOCTYPE html>'
                '<html><head><title>Foo</title></head>'
                '<body><p>name: {}</p></body>'
                '</html>').format(app.request.query['name'])

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/?name=Humpty+Dumpty displays a page with the
following text.

    | name: Humpty Dumpty

Note that the ``+`` sign in the query string has been properly URL
decoded into a space.

The ``app.request.query`` object in the code is an ``ice.MultiDict``
object that can store multiple values for every key. However, when used
like a dictionary, it returns the most recently added value for a key.
Therefore, visiting http://localhost:8080/?name=Humpty&name=Santa
displays a page with the following text.

    | name: Santa

Note that in this URL, there are two values passed for the ``name``
field in the query string, but accessing ``app.request.query['name']``
provides us only the value that is most recently added. To get all the
values for a key in ``app.request.query``, we can use the
``ice.MultiDict.getall`` method as shown below.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/')
    def home():
        return ('<!DOCTYPE html>'
                '<html><head><title>Foo</title></head>'
                '<body><p>name: {}</p></body>'
                '</html>').format(app.request.query.getall('name'))

    if __name__ == '__main__':
        app.run()

Now, visiting http://localhost:8080/?name=Humpty&name=Santa
displays a page with the following text.

    | name: ['Humpty', 'Santa']

Note that the ``ice.MultiDict.getall`` method returns all the values
belonging to the key as a ``list`` object.


Forms
-----
The following example shows an application that can process forms
submitted by a POST request.

.. code:: python

    import ice
    app = ice.cube()

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

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/, filling
up the form and submitting it displays the form data.

The ``app.request.form`` object in this code, like the
``app.request.query`` object in the previous section, is a MultiDict
object.

.. code:: python

    import ice
    app = ice.cube()

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

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/, filling
up the form and submitting it displays the form data. While
``app.request.form['name']`` returns the string entered in the second
input field, ``app.request.form.getall('name')`` returns strings entered
in both input fields as a list object.


Error pages
-----------
The application object returned by the ``ice.cube`` function contains a
generic fallback error handler that returns a simple error page with the
HTTP status line, a short description of the status and the version of
the ice module.

This error handler may be overridden using the ``error`` decorator. This
decorator accepts one optional integer argument that may be used to
explicitly specify the HTTP status code of responses for which the
handler should be invoked to generate an error page. If no argument is
provided, the error handler is defined as a fallback error handler. A
fallback error handler is invoked to generate an error page for any HTTP
response representing an error when there is no error handler defined
explicitly for the response status code of the HTTP response.

Here is an example.

.. code:: python

    import ice
    app = ice.cube()

    @app.error(404)
    def error():
        return ('<!DOCTYPE html>'
                '<html><head><title>Page not found</title></head>'
                '<body><p>Page not found</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | Page not found


Status codes
------------
In all the examples above, the response message body is returned as a
string from a route's callable. It is also possible to return the
response status code as an integer. In other words, a route's callable
must either return a string or an integer. When a string is returned, it
is sent as response message body to the client. When an integer is
returned and it is a valid HTTP status code, an HTTP response with this
status code is sent to the client. If the value returned by a route's
callable is neither a string nor an integer representing a valid HTTP
status code, then an error is raised.

Therefore there are two ways to return an HTTP response from a route's
callable.

1. Return message body and optionally set status code. This is the
   preferred way of returning content for normal HTTP responses (200
   OK). If the status code is not set explicitly in a route's callable,
   then it has a default value of 200.
2. Return status code and optionally set message body. This is the
   preferred way of returning content for HTTP errors. If the message
   body is not set explicitly in a route's callable, then the error
   handler for the returned status code is invoked to return a message
   body.

Here is an example where status code is set to 403 and a custom
error page is returned.

.. code:: python

    import ice

    app = ice.cube()

    @app.get('/foo')
    def foo():
        app.response.status = 403
        return ('<!DOCTYPE html>'
                '<html><head><title>Access is forbidden</title></head>'
                '<body><p>Access is forbidden</p></body></html>')

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | Access is forbidden

Here is another way of writing the above application. In this case, the
message body is set and the status code is returned.

.. code:: python

    import ice

    app = ice.cube()

    @app.get('/foo')
    def foo():
        app.response.body = ('<!DOCTYPE html>'
                '<html><head><title>Access is forbidden</title></head>'
                '<body><p>Access is forbidden</p></body></html>')
        return 403

    if __name__ == '__main__':
        app.run()

Although the above way of setting message body works, using an error
handler is the preferred way of defining the message body for an HTTP
error. Here is an example that demonstrates this.

.. code:: python

    import ice

    app = ice.cube()

    @app.get('/foo')
    def foo():
        return 403

    @app.error(403)
    def error403():
        return ('<!DOCTYPE html>'
                '<html><head><title>Access is forbidden</title></head>'
                '<body><p>Access is forbidden</p></body></html>')

    if __name__ == '__main__':
        app.run()

For simple web applications, just returning the status code is
sufficient. When neither a message body is defined nor an error handler
is defined, a generic fallback error handler set in the application
object returned by the ``ice.cube`` is used to return a simple error
page with the HTTP status line, a short description of the status and
the version of the ice module.

.. code:: python

    import ice

    app = ice.cube()

    @app.get('/foo')
    def foo():
        return 403

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | 403 Forbidden
    | Request forbidden -- authorization will not help


Static files
------------
In a typical production environment, a web server may be configured to
receive HTTP requests and forward it to a Python application via WSGI.
In such a setup, it might make more sense to configure the web server to
serve static files because web servers implement several standard file
handling capabilities and response headers, e.g. 'Last-Modified',
'If-Modified-Since', etc. However, it is possible to serve static files
from an ice application using the ``static()`` method that provides a
very rudimentary means of serving static files. This could be useful in
a development environment where one would want to test pages with static
content such as style sheets, images, etc. served by an ice application
without using a web server.

Here is an example.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/code/<:path>')
    def send_code(path):
        return app.static('/var/www/project/code', path)

    if __name__ == '__main__':
        app.run()

The first argument to the ``static()`` method must specify the path to
what is known as the document root directory. This is very important to
prevent `directory traversal attack`_. This method guarantees that only
files within the document root directory are served and no files outside
this directory can be accessed by a client.

.. _directory traversal attack: https://en.wikipedia.org/wiki/Directory_traversal_attack

The second argument is a path to the file to be returned as response.
This path must be relative to the document directory.

For example, if there is a file called
/var/www/project/code/data/foo.txt, then visiting
http://localhost:8080/code/data/foo.txt would return the content of
this file as response.

However, visiting http://localhost:8080/code/%2e%2e/foo.txt would
display a '403 Forbidden' page because this request attempts to access
foo.txt in the parent directory of the document directory (``%2e%2d`` is
URL encoding of ``..``).

In the above example, the 'Content-Type' header of the response is
automatically set to 'text/plain; charset=UTF-8'. With only two
arguments specified to the ``static()`` method, it uses the extension
name of the file being returned to automatically guess the media type to
be used in the 'Content-Type' header. For example, the media type of a
.txt file is typically *guessed* to be 'text/plain'. But this may be
different because system configuration files may be referred in order to
guess the media type and such configuration files may map a .txt file to
a different media type.

For example, on a Debian 8.0 system, /etc/mime.types maps a .c file to
'text/x-csrc'. This is one of the files that is referred to guess the
media type. Therefore, the 'Content-Type' header for a request to
http://localhost:8080/code/data/foo.c would be set to
'text/x-csrc; charset=UTF-8' on such a system.

To see the list of files that may be referred to guess media type,
execute this command. ::

    python3 -c "import mimetypes; print(mimetypes.knownfiles)"

The media type of static file being returned in a response can be set
explicitly to a desired value using the ``media_type`` keyword argument.

The charset defaults to 'UTF-8' for any media type of type 'text'
regardless of the subtype. This may be changed with the ``charset``
keyword argument.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/code/<:path>')
    def send_code(path):
        return app.static('/var/www/project/code', path,
                          media_type='text/plain', charset='ISO-8859-1')

    if __name__ == '__main__':
        app.run()

The above code guarantees that the 'Content-Type' header of a request to
http://localhost:8080/code/data/foo.c is set to
'text/plain; charset=ISO-8859-1' regardless of how the media type of a
.c file is defined in the system configuration files.
