from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from app.db import add_item, get_items, delete_item, ItemJSONEncoder, Item, update_item
from app.readers import get_item_price_with_retries
from typing import Union

def fetch_price_and_add_item(name: str, url: str):
    price = get_item_price_with_retries(url)
    add_item(Item(name, url, price))

class SimpleWebServer(BaseHTTPRequestHandler):


    def __send_response(self, response_code: int, response: Union[str, bytes]):
        self.send_response(200)
        self.end_headers()
        if isinstance(response, str):
            response = response.encode('utf-8')
        self.wfile.write(response)

    def do_GET(self):
        try:
            path = self.path.strip('/')
            if path == 'items':
                data_to_send = json.dumps(get_items(), cls=ItemJSONEncoder)
                self.__send_response(200, data_to_send)
                return
            file_path = os.path.join(os.path.dirname(__file__), path or 'index.html')
            with open(file_path, 'rb') as fp:
                self.__send_response(200, fp.read())
        except FileNotFoundError:
            self.__send_response(404, "File not found!")
    
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        
        data = json.loads(put_data)
        
        item_index = int(self.path.split('/')[-1])
        items = get_items()
        item = items[item_index]
        item.name = data['name']
        item.url = data['url']
        update_item(item_index, item)
        
        self.__send_response(200, "Success")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        data = json.loads(post_data)
        fetch_price_and_add_item(data['name'], data['url'])
        self.__send_response(200, "Success")
    
    def do_DELETE(self):
        item_index = int(self.path.split('/')[-1])
        delete_item(item_index)
        self.__send_response(200, "Success")

def run(server_class=HTTPServer, handler_class=SimpleWebServer, port=8700):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

run()
