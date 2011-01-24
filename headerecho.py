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
import sys, os.path

# only do stdout redirection if we're not running from
# the command-line
if __name__ != '__main__':
  sys.stdout = sys.stderr

def application(environ, start_response):
  script_filename = environ.get('SCRIPT_FILENAME')
  query = environ.get('QUERY_STRING')
  path  = environ.get('PATH_INFO')

  try:
    # if there isn't a querystring, return the client-side
    # test page.
    if query is '' and path in ['/','']: 
      html_path = os.path.join( os.path.dirname(script_filename), 'headerecho.html')
      return response(
             start_response,
             '200 OK',
             ''.join( open(html_path).readlines() ),
             'text/html'
      )

    # return the header provided in the query string 
    # iff the header is in the environ dict
    req_header = environ.get( 'HTTP_%s' % query.upper().replace('-','_'), None )
    if req_header == None:
      return response(start_response, '404 Not Found', 'Request header %s not defined.\n' % query)

    # build and return the JSON response 
    return response(
           start_response,
           '200 OK',
           '{"%s" : "%s"}\n' % (query, req_header),
           'application/json'
    )
  except Exception, e:
    return response(start_response, '500 Server Error', str(e) )

def response(start_response, status, resp_string, resp_type='text/plain'):
    resp_len = str(len(resp_string))
    resp_headers = [('Content-type', resp_type), ('Content-length', resp_len) ]
    start_response(status, resp_headers)
    return [resp_string]
      
# run standalone if we're invoked from the command-line
if __name__ == '__main__':
  from wsgiref import simple_server
  PORT = 8000
  httpd = simple_server.WSGIServer( ('', PORT), simple_server.WSGIRequestHandler )
  httpd.set_app(application)
  print 'headerecho server listening at %s' % ( PORT )
  print 'ctrl-c to kill me ...'
  httpd.serve_forever()
