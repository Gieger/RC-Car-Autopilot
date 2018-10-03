import tornado.ioloop
import tornado.web
import tornado.websocket
import asyncio
import time
import io
import os
import cv2
from PIL import Image
import numpy as np
from tornado.options import define, parse_command_line,options

html_page_path = os.path.dirname(os.path.realpath(__file__)) + '/www/'
class WebServer(tornado.web.Application):
    name = "Web-Server"
    

    def __init__(self):
        self.frame = "None"


        handlers = [
            (r'/', HtmlPageHandler),
            (r'/video_feed', StreamHandler),
            (r'/setparams', SetParamsHandler),
            (r'/(?P<file_name>[^\/]+htm[l]?)+', HtmlPageHandler),
            (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/RC-Car-Autopilot/parts/webserver/image'}),
            (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/RC-Car-Autopilot/parts/webserver/css'}),
            (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/RC-Car-Autopilot/parts/webserver/js'})
            ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)



    def update(self):
        """ Start the tornado web server. """
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

    def run_threaded(self, frame="None"): 
        self.frame = frame

        
    

class StreamHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header( 'Pragma', 'no-cache')
        self.set_header( 'Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        self.served_image_timestamp = time.time()
        my_boundary = "--jpgboundary"
        while True:
            # Generating images for mjpeg stream and wraps them into http resp

            image = self.application.frame

            if self.get_argument('fd') == "true":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, jpeg = cv2.imencode('.jpg', image)




            img = jpeg.tobytes()
  
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


class HtmlPageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, file_name='index.html'):
        # Check if page exists
        index_page = os.path.join(html_page_path, file_name)
        if os.path.exists(index_page):
            # Render it
            self.render('www/' + file_name)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=file_name)
            # Send response
            self.finish(err_html)


class SetParamsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        # print self.request.body
        # get args from POST request

        # try to change resolution
        try:
            
            self.write({'resp': 'ok'})
        except:
            self.write({'resp': 'bad'})
            self.flush()
            self.finish()