import sys
import BaseHTTPServer

class RestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head></head>works...</html>")

if __name__ == '__main__':

    try:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    except:
        sys.exit('Usage: python -m frodo.rest HOST PORT')

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST, PORT), RestHandler)
    try:
        print 'rest api server staring up...'
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'rest api server going down...'
    httpd.server_close()
