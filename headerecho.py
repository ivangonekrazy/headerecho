def headerEcho(environ, start_response):
  try:
    query = environ.get('QUERY_STRING')
    path  = environ.get('PATH_INFO')
    if len(query) == 0 and path == '/': 
      print 'returning html'
      start_response('200 OK', [('Content-type', 'text/html')])
      return open('headerecho.html').readlines()

    req_header = environ.get( 'HTTP_%s' % query.upper().replace('-','_') )
    if req_header is None:
      start_response('404 Not Found', [('Content-type', 'text/plain')])
      return ['Request header %s not defined.\n' % query]

    start_response('200 OK', [('Content-type', 'application/json')])
    return ['{"%s" : "%s"}\n' % (query, req_header)]
  except Exception, e:
    print e
      
if __name__ == '__main__':
  from wsgiref import simple_server
  PORT = 8000
  httpd = simple_server.WSGIServer( ('', PORT), simple_server.WSGIRequestHandler )
  httpd.set_app(headerEcho)
  print 'Server listening at %s' % ( PORT )
  httpd.serve_forever()
