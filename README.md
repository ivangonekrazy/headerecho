# headerEcho v0.1
#### Ivan Tam (ivangonekrazy@gmail.com)
#### Copyright (c) 2011 Ivan Tam

A small WSGI application to echo back request headers.
Used in testing for HTTP headers tomfoolery or shenanigans
in HTTP load balancers and/or proxies.

Responds to GET requests of the following format:

    http://server/headerecho?header_string

with a JSON response of the following format:

    {"<header_string": "<header_value>"}

Example:
    http://localhost/headerecho?X-Requested-With

  yields

    {"X-Requested-With" : "XmlHttpRequest"}

An HTML/jQuery Test page that will repeatedly request
for a header echo is served up at

    http://server/headerecho

An example Apache conf file is provided in example-wsgi.conf. 
This config file sets up a WSGIScriptAlias at _/headerecho_. 

You can also start headerEcho as a stand-alone WSGI (no Apache needed) server
by running it on the command-line:

    python headerecho.py

The _/headerecho_ path fragment is not necessary when running in stand-alone mode. Thus:

    http://server

and 
    
    http://server?header_string

will, respectively, bring up the HTML test page and echo the given header.
