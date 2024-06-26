import io
import socket
import struct
import time
import picamera
import sys

sys.path.insert(1, "/home/pi/Jenson/src")
from config import HOST_IPV4


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

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


def send_images():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting connection to " + str(HOST_IPV4) + "...")
    client_socket.connect((HOST_IPV4, 65024))
    print("Connected")
    connection = client_socket.makefile("wb")
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution=(1920, 1080), framerate=30) as camera:
            time.sleep(2)
            start = time.time()
            camera.start_recording(output, format="mjpeg")
            camera.wait_recording(10)
            camera.stop_recording()
            # Write the terminating 0-length to the connection to let the
            # server know we're done
            connection.write(struct.pack("<L", 0))
    finally:
        connection.close()
        client_socket.close()
        finish = time.time()
    print(
        "Sent %d images in %d seconds at %.2ffps"
        % (output.count, finish - start, output.count / (finish - start))
    )


if __name__ == "__main__":
    send_images()
    sys.exit(0)
