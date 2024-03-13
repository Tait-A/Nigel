import json
import io
import socket
import struct
import time
import sys
from config import PI_IPV4


class ControlReceiver(object):
    def __init__(self):
        ip_addr = PI_IPV4
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip_addr, 65024))
        server_socket.listen(1)
        print("Waiting for connection...")
        self.connection, address = server_socket.accept()
        print("Connection from ", address)
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

    def listen_and_read(self):
        while True:
            try:
                # Wait for an item in the buffer

                json_object = self.receive_json_object()
                print(json_object)

            except Exception as e:
                print(f"Error occurred while listening and reading: {str(e)}")
                # Handle the error or exit the loop if necessary
                break


if __name__ == "__main__":
    receiver = ControlReceiver()
    receiver.listen_and_read()
    receiver.connection.close()
    print("Connection closed")
    sys.exit(0)
