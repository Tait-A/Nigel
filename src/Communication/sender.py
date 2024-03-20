import json
import io
import socket
import struct
import time
import sys
from config import PI_IPV4, DICE_IPV4


# Replace 'your_object' with your actual Python object
your_object = {
    "name": "Example Object",
    "type": "Example Type",
    "details": {
        "description": "This is a sample object for demonstration purposes.",
        "id": 123,
    },
}


class ControlSender(object):
    def __init__(self):
        ip_addr = DICE_IPV4
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting connection to " + str(ip_addr) + "...")
        client_socket.connect((ip_addr, 65024))
        print("Connected")
        self.connection = client_socket.makefile("wb")

    def send_json_object(self, json_object):
        json_data = json.dumps(json_object)

        data = json_data.encode("utf-8")
        size = len(data)
        self.connection.sendall(size.to_bytes(4, "big"))
        self.connection.sendall(data)

    def write(self, buf):
        if buf.startswith(b"\xff\xd8"):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack("<L", size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

    class ControlReceiver(object):
        def __init__(self):
            ip_addr = PI_IPV4
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip_addr, 1883))
            server_socket.listen(1)
            print("Waiting for connection...")
            self.connection, address = server_socket.accept()
            print("Connection from {address}")
            self.stream = io.BytesIO()

        def receive_json_object(self):
            size_bytes = self.connection.recv(4)
            size = struct.unpack("<L", size_bytes)[0]
            data = self.connection.recv(size)
            json_data = data.decode("utf-8")
            json_object = json.loads(json_data)
            return json_object

        def read(self, size):
            while len(self.stream.getvalue()) < size:
                data = self.connection.recv(size - len(self.stream.getvalue()))
                if not data:
                    raise Exception("Connection closed unexpectedly")
                self.stream.write(data)
            buf = self.stream.getvalue()[:size]
            self.stream = io.BytesIO(self.stream.getvalue()[size:])
            return buf


if __name__ == "__main__":
    sender = ControlSender()
