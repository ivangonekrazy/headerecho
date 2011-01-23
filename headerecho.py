"""
  headerEcho v0.1
  Ivan Tam (ivangonekrazy@gmail.com)
  Copyright (c) 2011 Ivan Tam

  A small WSGI application to echo back request headers.
  Used in testing for HTTP headers tomfoolery or shenanigans
  in HTTP load balancers and/or proxies.

  Responds to GET requests of the following format:
    http://<server>/?<header_string>
  with a JSON response of the following format:
    {"<header_string": "<header_value>"}

  E.g.
    http://localhost/?X-Requested-With
  -->
    {"X-Requested-With" : "XmlHttpRequest"}
"""

def application(environ, start_response):
  try:
    query = environ.get('QUERY_STRING')
    path  = environ.get('PATH_INFO')

    # if there isn't a querystring, return the client-side
    # test page.
    if len(query) == 0 and path == '/': 
      start_response('200 OK', [('Content-type', 'text/html')])
      return open('headerecho.html').readlines()

    # return the header provided in the query string 
    # iff the header is in the environ dict
    req_header = environ.get( 'HTTP_%s' % query.upper().replace('-','_') )
    if req_header is None:
      start_response('404 Not Found', [('Content-type', 'text/plain')])
      return ['Request header %s not defined.\n' % query]

    # build and return the JSON response 
    start_response('200 OK', [('Content-type', 'application/json')])
    return ['{"%s" : "%s"}\n' % (query, req_header)]
  except Exception, e:
    start_response('500 Server Error', [('Content-type', 'text/plain')])
    return ['Server error: %s' % str(e)]
      
# run standalone if we're invoked from the command-line
if __name__ == '__main__':
  from wsgiref import simple_server
  PORT = 8000
  httpd = simple_server.WSGIServer( ('', PORT), simple_server.WSGIRequestHandler )
  httpd.set_app(application)
  print 'headerEcho server listening at %s' % ( PORT )
  httpd.serve_forever()
