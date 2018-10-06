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
            (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/image/'}),
            (r'/(?:fonts)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/fonts/'}),
            (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/css/'}),
            (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/js/'})
            ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)



    def update(self):
        """ Start the tornado web server. """
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.listen(8889)
        tornado.ioloop.IOLoop.instance().start()

    def run_threaded(self, frame="None", steer="None",thrott ="None"):
        self.steer = steer
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
            img = self.application.frame
            steer = self.application.steer
            thrott = 0.5
            thrott1 = int(thrott * 100)
            psteer = round(psteer, 2)
            psteer1 = int(psteer * 200)

            if self.get_argument('fd') == "false":
                cv2.line(img,(200,560),(600,560),(0,0,255),2)

                cv2.line(img,(200,550),(200,570),(0,0,255),2)
                cv2.line(img,(250,555),(250,565),(0,0,255),2)
                cv2.line(img,(300,550),(300,570),(0,0,255),2)
                cv2.line(img,(350,555),(350,565),(0,0,255),2)
                cv2.line(img,(400,550),(400,570),(0,0,255),2)
                cv2.line(img,(450,555),(450,565),(0,0,255),2)
                cv2.line(img,(500,550),(500,570),(0,0,255),2)
                cv2.line(img,(550,555),(550,565),(0,0,255),2)
                cv2.line(img,(600,550),(600,570),(0,0,255),2)


                cv2.line(img,(50,200),(50,400),(255,0,0),2)

                cv2.line(img,(40,200),(60,200),(255,0,0),2)
                cv2.line(img,(45,225),(55,225),(255,0,0),2)
                cv2.line(img,(40,250),(60,250),(255,0,0),2)
                cv2.line(img,(45,275),(55,275),(255,0,0),2)
                cv2.line(img,(40,300),(60,300),(255,0,0),2)
                cv2.line(img,(45,325),(55,325),(255,0,0),2)
                cv2.line(img,(40,350),(60,350),(255,0,0),2)
                cv2.line(img,(45,375),(55,375),(255,0,0),2)
                cv2.line(img,(40,400),(60,400),(255,0,0),2)


                cv2.line(img,(40,300 + thrott1),(60, 300 + thrott1),(0,255,0),6)  
                cv2.line(img,(400 + psteer1,570),(400 + psteer1,550),(0,255,0),6)               

            if self.get_argument('fd') == "true":
                img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
                cv2.rectangle(img,(0,0),(800,200),(0,0,0),-1)
    
                cv2.line(img,(200,160),(600,160),(0,0,255),2)

                cv2.line(img,(200,150),(200,170),(0,0,255),2)
                cv2.line(img,(250,155),(250,165),(0,0,255),2)
                cv2.line(img,(300,150),(300,170),(0,0,255),2)
                cv2.line(img,(350,155),(350,165),(0,0,255),2)
                cv2.line(img,(400,150),(400,170),(0,0,255),2)
                cv2.line(img,(450,155),(450,165),(0,0,255),2)
                cv2.line(img,(500,150),(500,170),(0,0,255),2)
                cv2.line(img,(550,155),(550,165),(0,0,255),2)
                cv2.line(img,(600,150),(600,170),(0,0,255),2)

                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (250,100)
                bottomLeftCornerOfText1 = (194,80)

                fontScale              = 0.5
                fontColor              = (0,255,0)
                fontColor1              = (255,255,255)
                lineType               = 2

                if psteer > 0:
                    cv2.putText(img,"Lenkung: +" + str(psteer), 
                        bottomLeftCornerOfText, 
                        font, 
                        fontScale,
                        fontColor,
                        lineType)

                else:
                    cv2.putText(img,"Lenkung: " + str(psteer), 
                        bottomLeftCornerOfText, 
                        font, 
                        fontScale,
                        fontColor,
                        lineType)

                if thrott > 0:
                    cv2.putText(img,"Beschleunigung: +" + str(thrott), 
                        bottomLeftCornerOfText1, 
                        font, 
                        fontScale,
                        fontColor1,
                        lineType)
                else:
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