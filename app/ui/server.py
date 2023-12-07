from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os
from app.db import add_item, get_items, delete_item, ItemJSONEncoder, Item, save_items
from app.readers import get_item_price_with_retries

def fetch_price_and_add_item(name: str, url: str):
    items = get_items()
    price = get_item_price_with_retries(url)
    items.append(Item(name, url, price))
    save_items(items)

class SimpleWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            base_path = os.path.dirname(__file__)
            if self.path == '/':
                path = '/index.html'
            else:
                path = self.path
            if path == '/items':
                data_to_send = json.dumps(get_items(), cls=ItemJSONEncoder)
            else:
                with open(os.path.join(base_path,path[1:]), 'rb') as file_to_open:
                    data_to_send = file_to_open.read()
            self.send_response(200)
        except FileNotFoundError:
            data_to_send = "File not found!"
            self.send_response(404)
        self.end_headers()
        if isinstance(data_to_send, str):
            data_to_send = data_to_send.encode('utf-8')
        self.wfile.write(data_to_send)
    
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        
        data = json.loads(put_data)
        
        item_index = int(self.path.split('/')[-1])
        items = get_items()
        items[item_index].name = data['name']
        items[item_index].url = data['url']
        save_items(items)
        
        self.send_response(200)
        self.end_headers()
        response = bytes("Put request processed", 'utf-8')
        self.wfile.write(response)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        data = json.loads(post_data)
        fetch_price_and_add_item(data['name'], data['url'])
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
