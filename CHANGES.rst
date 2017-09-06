ChangeLog
=========

0.0.2 (2017-09-06)
------------------
- NEW: Rudimentary error message when no error handler is defined.
- NEW: Return integer status code from a route's callable.
- NEW: Wildcard pattern of path type, e.g. ``<:path>``, to match paths.
- NEW: Return static files using the ``static()`` method.
- NEW: Send attachment to client using the ``download()`` method.
- NEW: Cookies dictionary in request object.
- NEW: Set cookie in response header using the ``set_cookie()`` method.
- NEW: Send redirects by returning tuple of status code and URL.

0.0.1 (2014-06-05)
------------------
- NEW: Literal, wildcard and regular expression routes.
- NEW: Anonymous, named and throwaway wildcards.
- NEW: Query and form dictionaries in request object.
- NEW: Custom error pages.
