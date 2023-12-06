from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json

from app.db import add_item, get_items, delete_item

class SimpleWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                path = '/index.html'
            else:
                path = self.path
            if path == '/items':
                data_to_send = json.dumps(get_items())
            else:
                with open(path[1:], 'r') as file_to_open:
                    data_to_send = file_to_open.read()
            self.send_response(200)
        except FileNotFoundError:
            data_to_send = "File not found!"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(data_to_send, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        print(data)

        self.send_response(200)
        self.end_headers()
        response = bytes("Post request processed", 'utf-8')
        self.wfile.write(response)
    
    def do_DELETE(self):
        item_index = int(self.path.split('/')[-1])
        delete_item(item_index)
        self.send_response(200)
        self.end_headers()
        response = bytes("Delete request processed", 'utf-8')
        self.wfile.write(response)

def run(server_class=HTTPServer, handler_class=SimpleWebServer, port=8700):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

run()
