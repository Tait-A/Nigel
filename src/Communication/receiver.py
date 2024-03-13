from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the length of the incoming JSON data
        content_length = int(self.headers["Content-Length"])
        # Read the JSON data
        post_data = self.rfile.read(content_length)

        # Deserialize the JSON data to a Python object
        received_object = json.loads(post_data)

        # Process the object as needed
        print(f"Received object: {received_object}")

        # Send a response to the client
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"status": "Received"}
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=64024):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()
