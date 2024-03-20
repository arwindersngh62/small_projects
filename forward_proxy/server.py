# webapp.py

from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import requests

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        print(self.url)
        res = requests.get(f"http://{self.url.path[1:]}")
        print(res.headers)
        self.send_response(200)
        #for key,value in res.headers.items():
        #    self.send_header(key,value)
        #for value in res.iter_content():
        #    print(value)
        self.send_header("Content-type", res.headers["content-type"])
        self.end_headers()
       # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes(res.text, "utf-8"))
        #self.wfile.write(bytes("<body>", "utf-8"))
        #self.wfile.write(bytes("</body></html>", "utf-8"))
        
        #self.send_error(404, message="Its something but its not here")
        return 

    def do_POST(self):
        ...
        
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    print("Starting a new server!!!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("stoping server")
    server.server_close()