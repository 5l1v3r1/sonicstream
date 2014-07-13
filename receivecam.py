import argparse
from collections import deque
import thread
import socket

import cv2

argparser = argparse.ArgumentParser()
argparser.add_argument("--ip", default="0.0.0.0",
    help="IP address to listen on")
argparser.add_argument("--port", default=7331, type=int,
    help="Port to listen on")

args = argparser.parse_args()


class CamReceiver:

    _temp_image_file = "/tmp/goatse2.jpg"

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._ip, self._port))

    def run(self):
        buffer_queue = deque(['']*4)
        filestream = None
        while True:
            data, addr = self._sock.recvfrom(2**14)
            
            for char in data:
                buffer_queue.popleft()
                buffer_queue.append(char)
                buffer_string = ''.join(buffer_queue)

                if buffer_string == 'lol1':
                    filestream = open(self._temp_image_file, 'w')
                    cv2.destroyAllWindows()
                elif buffer_string == 'lol2' and filestream is not None:
                    filestream.close()
                    filestream = None
                    cv2.imshow('image', cv2.imread(self._temp_image_file))
                    thread.start_new_thread(cv2.waitKey, (0,))
                elif filestream is not None:
                    filestream.write(char)

if __name__ == "__main__":
    camreceiver = CamReceiver(args.ip, args.port)
    camreceiver.run()
