from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SimpleWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print(self.path)
            if self.path == '/':
                self.path = '/index.html'
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError:
            file_to_open = "File not found!"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        print(data)

        self.send_response(200)
        self.end_headers()
        response = bytes("Post request processed", 'utf-8')
        self.wfile.write(response)

def run(server_class=HTTPServer, handler_class=SimpleWebServer, port=8700):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

run()
