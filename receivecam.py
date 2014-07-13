import argparse
from collections import deque
import thread
import socket

import cv

argparser = argparse.ArgumentParser()
argparser.add_argument("--ip", default="0.0.0.0",
    help="IP address to listen on")
argparser.add_argument("--port", default=7331, type=int,
    help="Port to listen on")
argparser.add_argument("--windowwidth", default=300, type=int,
    help="Width of the image display window")
argparser.add_argument("--windowheight", default=300, type=int,
    help="Height of the image display window")

args = argparser.parse_args()


class CamReceiver:

    _temp_image_file = "/tmp/goatse2.jpg"

    def __init__(self, ip, port, windowsize):
        self._ip = ip
        self._port = port
        self._windowsize = windowsize

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._ip, self._port))

    def _image_resized(self, image, newsize):
        newimage = cv.CreateImage(newsize, image.depth, image.nChannels)
        cv.Resize(image, newimage)
        return newimage

    def run(self):
        buffer_queue = deque(['']*4)
        filestream = None
        written = 0
        while True:
            data, addr = self._sock.recvfrom(2**14)
            
            for char in data:
                buffer_queue.popleft()
                buffer_queue.append(char)
                buffer_string = ''.join(buffer_queue)

                if buffer_string == 'lol1':
                    filestream = open(self._temp_image_file, 'w')
                    cv.DestroyAllWindows()
                elif buffer_string == 'lol2' and filestream is not None:
                    filestream.close()
                    filestream = None
                    image = cv.LoadImage(self._temp_image_file)
                    image = self._image_resized(image, self._windowsize)
                    cv.ShowImage('image', image)
                    thread.start_new_thread(cv.WaitKey, (0,))
                    written = 0
                elif filestream is not None:
                    if written >= 2**14:
                        print "too much data, screw this kthxbai"
                        quit()
                    filestream.write(char)
                    written += 1

if __name__ == "__main__":
    camreceiver = CamReceiver(args.ip, args.port,
        (args.windowwidth, args.windowheight))
    camreceiver.run()
