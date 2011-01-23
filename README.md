headerEcho v0.1
---------------
Ivan Tam (ivangonekrazy@gmail.com)
Copyright (c) 2011 Ivan Tam

A small WSGI application to echo back request headers.
Used in testing for HTTP headers tomfoolery or shenanigans
in HTTP load balancers and/or proxies.

Responds to GET requests of the following format:

  http://server/?header_string

with a JSON response of the following format:

  {"<header_string": "<header_value>"}

E.g.
  http://localhost/?X-Requested-With

  yields

  {"X-Requested-With" : "XmlHttpRequest"}
