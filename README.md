headerecho
----------

A small WSGI server that will respond to
request in the format of:

http://<server>?header=<some_header>

with the value of the requested header or
a 404 response if the request header is 
not found.

I wrote this with the intent of doing an
end-to-end test to see if the "X-Requested-With"
request header was getting dropped somewhere
along our infrastructure causing some request to
not appear to be of the XHR type.
