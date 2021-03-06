import argparse
import time
import socket

import cv

argparser = argparse.ArgumentParser()
argparser.add_argument("ip", metavar="ip",
    help="Server IP address to transmit video to")
argparser.add_argument("--port", default=7331, type=int,
    help="Server port (default: 7331)")
argparser.add_argument("--framewidth", default=50, type=int,
    help="Frame width (default: 50)")
argparser.add_argument("--frameheight", default=50, type=int,
    help="Frame height (default: 50)")
argparser.add_argument("--fps", default=1, type=int,
    help="Frames per second (default: 1)")

args = argparser.parse_args()


class CamTransmitter:

    _temp_image_file = "/tmp/goatse.jpg"
    
    def __init__(self, ip, port, framesize, fps):
        self._ip = ip
        self._port = port
        self._framesize = framesize
        self._fps = fps

        self._capture = cv.CaptureFromCAM(0)
        self._udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _capture_webcam_frame(self):
        img = cv.QueryFrame(self._capture)

        thumbnail = cv.CreateImage(self._framesize, img.depth,
            img.nChannels)
        
        cv.Resize(img, thumbnail)

        return thumbnail

    def _blast_image(self, image):
        cv.SaveImage(self._temp_image_file, image)
        filestream = open(self._temp_image_file, 'r')
        self._send_udp_message(filestream.read())
        filestream.close()

    def _send_udp_message(self, message):
        return self._udp_sock.sendto(message, (self._ip, self._port))

    def run(self):
        while True:
            self._send_udp_message("lol1")
            self._blast_image(self._capture_webcam_frame())
            self._send_udp_message("lol2")
            time.sleep(1.0 / self._fps)

if __name__ == "__main__":
    camtransmitter = CamTransmitter(args.ip, args.port,
        (args.framewidth, args.frameheight), args.fps)
    camtransmitter.run()
