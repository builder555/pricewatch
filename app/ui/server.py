from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from app.db import item_service, item_repo, Item
from app.readers import get_item_price_with_retries, SiteNotSupported
from typing import Union


def fetch_price_and_add_item(name: str, url: str):
    price = get_item_price_with_retries(url)
    item_service.add_item(Item(name, url, price))


def update_item_and_fetch_price(item_index: int, name: str, url: str):
    items = item_service.get_items()
    item = items[item_index]
    if item.url != url:
        item.last_price = get_item_price_with_retries(url)
    item.name = name
    item.url = url
    item_service.update_item(item_index, item)


class SimpleWebServer(BaseHTTPRequestHandler):
    def __send_response(self, response_code: int, response: Union[str, bytes]):
        self.send_response(response_code)
        self.end_headers()
        if isinstance(response, str):
            response = response.encode("utf-8")
        self.wfile.write(response)

    def do_GET(self):
        try:
            path = self.path.strip("/")
            if path == "items":
                data_to_send = json.dumps(item_repo.get_items_json())
                self.__send_response(200, data_to_send)
                return
            file_path = os.path.join(os.path.dirname(__file__), path or "index.html")
            with open(file_path, "rb") as fp:
                self.__send_response(200, fp.read())
        except FileNotFoundError:
            self.__send_response(404, "File not found!")

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)

        data = json.loads(put_data)
        item_index = int(self.path.split("/")[-1])
        try:
            update_item_and_fetch_price(item_index, data["name"], data["url"])
        except SiteNotSupported as e:
            self.__send_response(400, str(e))
            return
        self.__send_response(200, "Success")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        try:
            fetch_price_and_add_item(data["name"], data["url"])
        except SiteNotSupported as e:
            self.__send_response(400, str(e))
            return
        self.__send_response(200, "Success")

    def do_DELETE(self):
        item_index = int(self.path.split("/")[-1])
        item_service.delete_item(item_index)
        self.__send_response(200, "Success")


def run(server_class=HTTPServer, handler_class=SimpleWebServer, port=8700):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


run()
