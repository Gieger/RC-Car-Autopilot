import tornado.ioloop
import tornado.web
import tornado.websocket
import asyncio
import random
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
            (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/workspace/RC-Car-Autopilot/parts/webserver/image'}),
            (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/workspace/RC-Car-Autopilot/parts/webserver/css'}),
            (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': '/home/ocp/Schreibtisch/workspace/RC-Car-Autopilot/parts/webserver/js'})
            ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)



    def update(self):
        """ Start the tornado web server. """
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.listen(8889)
        tornado.ioloop.IOLoop.instance().start()

    def run_threaded(self, frame="None", psteer="None"):
        self.psteer = psteer
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

            img = self.application.frame
            psteer = -0.5
            thrott = 0.5
            psteer = round(psteer, 2)
            psteer1 = int(psteer * 220)

            if self.get_argument('fd') == "false":
                cv2.line(img,(80,460),(560,460),(0,0,255),2)

                cv2.line(img,(80,450),(80,470),(0,0,255),2)
                cv2.line(img,(140,455),(140,465),(0,0,255),2)
                cv2.line(img,(200,450),(200,470),(0,0,255),2)
                cv2.line(img,(260,455),(260,465),(0,0,255),2)
                cv2.line(img,(320,450),(320,470),(0,0,255),2)
                cv2.line(img,(380,455),(380,465),(0,0,255),2)
                cv2.line(img,(440,450),(440,470),(0,0,255),2)
                cv2.line(img,(500,455),(500,465),(0,0,255),2)
                cv2.line(img,(560,450),(560,470),(0,0,255),2)

                cv2.line(img,(320 + psteer1,470),(320 + psteer1,450),(0,255,0),6)               

            if self.get_argument('fd') == "true":
                img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
                cv2.rectangle(img,(0,0),(640,220),(0,0,0),-1)

                
                cv2.line(img,(80,160),(560,160),(0,0,255),2)

                cv2.line(img,(80,150),(80,170),(0,0,255),2)
                cv2.line(img,(140,155),(140,165),(0,0,255),2)
                cv2.line(img,(200,150),(200,170),(0,0,255),2)
                cv2.line(img,(260,155),(260,165),(0,0,255),2)
                cv2.line(img,(320,150),(320,170),(0,0,255),2)
                cv2.line(img,(380,155),(380,165),(0,0,255),2)
                cv2.line(img,(440,150),(440,170),(0,0,255),2)
                cv2.line(img,(500,155),(500,165),(0,0,255),2)
                cv2.line(img,(560,150),(560,170),(0,0,255),2)


                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (250,100)
                bottomLeftCornerOfText1 = (194,80)

                fontScale              = 0.5
                fontColor              = (0,255,0)
                fontColor1              = (255,255,255)
                lineType               = 2

                cv2.putText(img,"Lenkung: " + str(psteer), 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)

                cv2.putText(img,"Beschleunigung: " + str(thrott), 
                    bottomLeftCornerOfText1, 
                    font, 
                    fontScale,
                    fontColor1,
                    lineType)

                cv2.line(img,(320 + psteer1,170),(320 + psteer1,150),(0,255,0),6)


            ret, jpeg = cv2.imencode('.jpg', img)




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