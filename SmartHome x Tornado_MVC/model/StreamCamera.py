import time

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import video
import gen
import os
import tornado.gen
cam = None

cam = video.UsbCamera()
class StreamCamera(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def streamCamera(self):
        
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header( 'Pragma', 'no-cache')
        self.set_header( 'Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        self.served_image_timestamp = time.time()
        my_boundary = "--jpgboundary"
        while True:
        	img = cam.get_frame(False)
        	interval = 0.1
        	if self.served_image_timestamp + interval < time.time():
        		self.write(my_boundary)
        		self.write("Content-type: image/jpeg\r\n")
        		self.write("Content-length: %s\r\n\r\n" % len(img))
        		self.write(img)
        		self.served_image_timestamp = time.time()
        		yield tornado.gen.Task(self.flush)
        	else:
        		yield tornado.gen.Task(ioloop.add_timeout, ioloop.time() + interval)

                     
                
    def get(self):
        self.streamCamera()
    def post(self):
        key = self.get_argument("key") 
        status = self.get_argument("value")
        if key == "switch-camera-1":
            if status == "off":
                cam.stop()
            if status == "on":
               cam.start()