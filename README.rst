Ice - WSGI on the rocks
=======================

Ice is a Python module with a WSGI microframework meant for developing
small web applications in Python.

.. image:: https://travis-ci.org/susam/ice.png?branch=master
   :target: https://travis-ci.org/susam/ice

.. image:: https://coveralls.io/repos/susam/ice/badge.png?branch=master
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
You can install this package using pip3 using the following command. ::

    pip3 install ice

You can install this package from source distribution. To do so,
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
This is free software. You are permitted to redistribute and use it in
source and binary forms, with or without modification, under the terms
of the Simplified BSD License. See the LICENSE.rst file for the complete
license.

This software is provided WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
LICENSE.rst file for the complete disclaimer.


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

A route is used to map an HTTP request made to an ice application to a
Python callable. A route consists of three objects:

1. HTTP request method, e.g. ``'GET'``, ``'POST'``.
2. Request path pattern, e.g. ``'/foo'``, ``'/post/<id>'``, ``/(.*)``.
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
        return '<!DOCTYPE html>' \
               '<html><head><title>Home</title></head>' \
               '<body><p>Home</p></body></html>'

    @app.get('/foo')
    def foo():
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>Foo</p></body></html>'

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
the literal pattern ``'/foo'`` does not match ``'/foo/'`` or
``'/foo/bar'``.

Wildcard routes
~~~~~~~~~~~~~~~
Anonymous wildcards
'''''''''''''''''''
The following code example is the simplest application demonstrating a
wildcard route that matches request path of the form ``/`` followed by
any string devoid of ``/``, ``<`` and ``>`` . The characters ``<>`` is
an anonymous wildcard because there is no name associated with this
wildcard. The part of the request path matched by an anonymous wildcard
is passed as a positional argument to the route's callable.

.. code:: python 

    import ice
    app = ice.cube()

    @app.get('/<>')
    def foo(a):
        return '<!DOCTYPE html>' \
               '<html><head><title>' + a + '</title></head>' \
               '<body><p>' + a + '</p></body></html>'

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
        return '<!DOCTYPE html>' \
               '<html><head><title>' + a + '</title></head>' \
               '<body><p>' + a + '</p></body></html>'

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>args: {}<br>kwargs: {}</p>' \
               '</body></html>'.format(args, kwargs)

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>page_id: {}<br>user: {}<br>category: {}</p>' \
               '</body></html>'.format(page_id, user, category)

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
it is required by the Python language that all positional parameters
must come before all keyword parameters in the function definition.
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
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>args: {}<br>kwargs: {}</p>' \
               '</body></html>'.format(args, kwargs)

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page the following text.

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>page_id: ' + page_id + '</p>' \
               '</body></html>'

    if __name__ == '__main__':
        app.run()

After running this application, visiting
http://localhost:8080/snowman/articles/python should display a page with
the following text.

    | page_id: python

There are three wildcards in the route's request path pattern but there
is only one parameter in the route's callable because two out of the
three wildcards are throwaway wildcards.

Wildcard specification
''''''''''''''''''''''
The complete syntax of a wildcard specification is: <*name*:*type*>.

The following rules describe how a wildcard is interpreted.

1.  The delimiters ``<`` (less-than sign) and ``>`` (greater-than sign),
    are mandatory.
2.  However, *name*, ``:`` (colon) and *type* are optional.
3.  Either a valid Python identifier or the exclamation mark, ``!``,
    should be used for *name*.
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
9.  If *type* is present but it is not ``str``, ``int``, ``+int`` and
    ``-int``, ice.RouteError is raised.
10.  If *type* is missing, it is assumed to be ``str``.
11. If *type* is ``str``, it matches a string not containing ``/``. The
    path of the request path matched by the wildcard is passed as an
    ``str`` object to the route's callable.
12. If *type* is ``int``, ``+int`` or ``-int``, the path of the request
    path matched by the wildcard is passed as an ``int`` object to the
    route's callable.
13. If *type* is ``+int``, the wildcard matches a positive integer where
    the positive integer beginning with a non-zero digit.
14. If *type* is ``int``, the wildcard matches ``0`` as well as
    everything that a wildcard of type ``+int`` matches.
15. If *type* is ``-int``, the wildcard matches a negative integer that
    begins with the ``-`` sign followed by a non-zero digit as well as
    everything that a wildcard of type ``int`` matches.

Here is an example that demonstrates a typical route with an ``int``
wildcard.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('/notes/<:int>')
    def note(note_id):
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>note_id: {}</p></body></html>'.format(note_id)

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/notes/12
displays a page with the following text.

    | note_id: 12

Visiting http://localhost:8080/notes/0 displays a page with the
following text.

    | note_id: 0

However, visiting http://localhost:8080/notes/+12,
http://localhost:8080/notes/+0 or http://localhost:8080/notes/012,
displays the '404 Not Found' page because ``<:int>`` does not match an
integer with a leading ``+`` sign or with a leading ``0``. It matches
``0`` and a positive integer beginning with a non-zero digit only.

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
        return '<!DOCTYPE html>' \
               '<html><head><title>' + a + '</title></head>' \
               '<body><p>' + a + '</p></body></html>'

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Example</title></head><body>' \
               '<p>page_id: {}<br>user: {}<br>category: {}</p>' \
               '</body></html>'.format(page_id, user, category)

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
positional parameters must come before all keyword parameters in the
function definition.  However, the capturing groups may appear in any
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
   capturing group, i.e. it contains ``(`` before ``)`` somewhere in
   the pattern, then it is automatically interpreted as a regular
   expression route.
5. If a route's request path pattern contains what looks like a
   wildcard, i.e. it contains ``<`` before ``>`` somewhere in the
   pattern with no ``/``, ``<`` and ``>`` in between them, then it is
   automatically interpreted as a wildcard route.
6. If none of the above rules succeed in determining how to interpret
   the request path, then it is interpreted as a literal route.
   literal route.

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>Foo</p></body></html>'

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
``(foo)`` in the pattern looks like a capturing group.

.. code:: python

    import ice
    app = ice.cube()

    @app.get('wildcard:/(foo)/<>')
    def foo(a):
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>a: ' + a + '</p></body></html>'

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

    @app.get('regex:/foo\d*')
    def foo():
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>Foo</p></body></html>'

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>name: {}</p></body>' \
               '</html>'.format(app.request.query['name'])

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
        return '<!DOCTYPE html>' \
               '<html><head><title>Foo</title></head>' \
               '<body><p>name: {}</p></body>' \
               '</html>'.format(app.request.query.getall('name'))

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
generic fallback error handler that displays a simple error page with
the HTTP status line, a short description of the status and the version
of the ice package.

This error handler may be overridden using the ``error`` decorator. This
decorator accepts one optional integer argument that may be used to
explicitly specify the HTTP status code of responses for which the
handler should be invoked to generate an error page. If no argument is
provided, the error handler is defined as a fallback error handler. A
fallback error handler is invoked to generate an error page for any HTTP
response representing an error when there is no error handler defined
explicitly for the response tatus code of the HTTP response.

Here is an example.

.. code:: python

    import ice
    app = ice.cube()

    @app.error(404)
    def error():
        return '<!DOCTYPE html>' \
               '<html><head><title>Page not found</title></head>' \
               '<body><p>Page not found</p></body></html>'

    if __name__ == '__main__':
        app.run()

After running this application, visiting http://localhost:8080/foo
displays a page with the following text.

    | Page not found
