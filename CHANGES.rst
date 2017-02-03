ChangeLog
=========

0.0.2 (UNRELEASED)
------------------
- NEW: Rudimentary error message when no error handler is defined.
- NEW: Return integer status code from a route's callable.
- NEW: Wildcard pattern of path type, e.g. <:path>, to match paths.
- NEW: static() method to return static files.
- NEW: download() method to force client to download content.
- NEW: Cookies dictionary in request object.
- NEW: set_cookie() method to set cookie to be sent to client.

0.0.1 (2014-06-05)
------------------
- NEW: Literal, wildcard and regular expression routes.
- NEW: Anonymous, named and throwaway wildcards.
- NEW: Query and form dictionaries in request object.
- NEW: Custom error pages.
