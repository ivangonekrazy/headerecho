import cgi

class HeaderEcho:
  """ Echo the requests headers back
      in the response
  """

  resp_code = {
    'OK'       : '200 OK',
    'NOT_FOUND': '404 Not Found',
    'ERROR'    : '500 Server Error'
  }

  default_resp_headers = [
    ('Content-type', 'text/plain')
  ]

  def __init__(self, environ, start_response):
    self.environ = environ
    self.start_response = start_response

  def __iter__(self):
    """ Takes a request like <server>?header=REMOTE_HOST
        and returns the value of that header if found
        returns 404 if not found
    """
    resp_headers = []

    try:
      target = self.query_params().get('header')
      if target is None:
        self.start_response(self.resp_code['NOT_FOUND'], self.default_resp_headers)
        yield 'No target request header defined.\n'

      req_header = self.environ.get(target)
      if req_header is None:
        self.start_response(self.resp_code['NOT_FOUND'], self.default_resp_headers)
        yield 'Request header %s not defined.\n' % target

      self.start_response(self.resp_code['OK'], self.default_resp_headers + resp_headers)
      yield 'Request header %s set to %s.\n' % (target, req_header)
    except:
      self.start_response(self.resp_code['ERROR'], self.default_resp_headers)
      yield 'Server Error\n'
      

  def query_params(self, environ=None):
    """ Converts the URL query string into a dict
    """
    params = {}

    if environ is None:
      environ = self.environ

    query_string = environ.get('QUERY_STRING', '')
    param_strings = query_string.split('&')

    for param_string in param_strings:
      k,v = param_string.split('=')
      params[k] = v

    return params


if __name__ == '__main__':
  from wsgiref import simple_server
  PORT = 8000
  print 'Server listening at %s' % ( PORT )
  httpd = simple_server.WSGIServer( ('', PORT), simple_server.WSGIRequestHandler )
  httpd.set_app(HeaderEcho)
  httpd.serve_forever()
