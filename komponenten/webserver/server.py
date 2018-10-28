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

html_pfad = os.path.dirname(os.path.realpath(__file__)) + '/www/'

class WebServer(tornado.web.Application):
    name = "Web-Server"
    
    def __init__(self):
        self.bild = "None"

        handlers = [
            (r'/', HtmlPageHandler),
            (r'/video_feed', StreamHandler),
            (r'/setparams', SetParamsHandler),
            (r'/(?P<datei_name>[^\/]+htm[l]?)+', HtmlPageHandler),
            (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/image/'}),
            (r'/(?:fonts)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/fonts/'}),
            (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/css/'}),
            (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': os.path.dirname(os.path.realpath(__file__)) + '/js/'})
            ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def aktualisieren(self):
        """ Start the tornado web server. """
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.listen(8889)
        tornado.ioloop.IOLoop.instance().start()

    def ausfuehren_parallel(self, bild="None", lenkung="None",beschleunigung ="None"):
        self.lenkung = lenkung
        self.beschleunigung = beschleunigung
        self.bild = bild

        
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
            bild = self.application.bild
            bild = cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)
            lenkung = self.application.lenkung
            beschleunigung = self.application.beschleunigung
            beschleunigung1 = int(beschleunigung * 160)
            lenkung = round(lenkung, 2)
            lenkung1 = int(lenkung * 80)

            if self.get_argument('fd') == "false":
                cv2.line(bild,(160,460),(480,460),(0,0,255),2)

                cv2.line(bild,(160,450),(160,470),(0,0,255),2)
                cv2.line(bild,(200,455),(200,465),(0,0,255),2)
                cv2.line(bild,(240,450),(240,470),(0,0,255),2)
                cv2.line(bild,(280,455),(280,465),(0,0,255),2)
                cv2.line(bild,(320,450),(320,470),(0,0,255),2)
                cv2.line(bild,(360,455),(360,465),(0,0,255),2)
                cv2.line(bild,(400,450),(400,470),(0,0,255),2)
                cv2.line(bild,(440,455),(440,465),(0,0,255),2)
                cv2.line(bild,(480,450),(480,470),(0,0,255),2)

                cv2.line(bild,(30,160),(30,320),(255,0,0),2)

                cv2.line(bild,(20,160),(40,160),(255,0,0),2)
                cv2.line(bild,(25,180),(35,180),(255,0,0),2)
                cv2.line(bild,(20,200),(40,200),(255,0,0),2)
                cv2.line(bild,(25,220),(35,220),(255,0,0),2)
                cv2.line(bild,(20,240),(40,240),(255,0,0),2)
                cv2.line(bild,(25,260),(35,260),(255,0,0),2)
                cv2.line(bild,(20,280),(40,280),(255,0,0),2)
                cv2.line(bild,(25,300),(35,300),(255,0,0),2)
                cv2.line(bild,(20,320),(40,320),(255,0,0),2)

                cv2.line(bild,(20,240 + lenkung1),(40, 240 + lenkung1),(0,255,0),6)  
                cv2.line(bild,(320 + beschleunigung1,470),(320 + beschleunigung1,450),(0,255,0),6)               

            if self.get_argument('fd') == "true":
                bild = cv2.cvtColor(bild, cv2.COLOR_RGB2YUV)
                
                cv2.line(bild,(160,460),(480,460),(0,0,255),2)

                cv2.line(bild,(160,450),(160,470),(0,0,255),2)
                cv2.line(bild,(200,455),(200,465),(0,0,255),2)
                cv2.line(bild,(240,450),(240,470),(0,0,255),2)
                cv2.line(bild,(280,455),(280,465),(0,0,255),2)
                cv2.line(bild,(320,450),(320,470),(0,0,255),2)
                cv2.line(bild,(360,455),(360,465),(0,0,255),2)
                cv2.line(bild,(400,450),(400,470),(0,0,255),2)
                cv2.line(bild,(440,455),(440,465),(0,0,255),2)
                cv2.line(bild,(480,450),(480,470),(0,0,255),2)

                cv2.line(bild,(30,160),(30,320),(255,0,0),2)

                cv2.line(bild,(20,160),(40,160),(255,0,0),2)
                cv2.line(bild,(25,180),(35,180),(255,0,0),2)
                cv2.line(bild,(20,200),(40,200),(255,0,0),2)
                cv2.line(bild,(25,220),(35,220),(255,0,0),2)
                cv2.line(bild,(20,240),(40,240),(255,0,0),2)
                cv2.line(bild,(25,260),(35,260),(255,0,0),2)
                cv2.line(bild,(20,280),(40,280),(255,0,0),2)
                cv2.line(bild,(25,300),(35,300),(255,0,0),2)
                cv2.line(bild,(20,320),(40,320),(255,0,0),2)

                cv2.line(bild,(20,240 + lenkung1),(40, 240 + lenkung1),(0,255,0),6)  
                cv2.line(bild,(320 + beschleunigung1,470),(320 + beschleunigung1,450),(0,255,0),6)      

            erfolg, jpeg = cv2.imencode('.jpg', bild)
            bild = jpeg.tobytes()
  
            interval = 0.1
            if self.served_image_timestamp + interval < time.time():
                self.write(my_boundary)
                self.write("Content-type: image/jpeg\r\n")
                self.write("Content-length: %s\r\n\r\n" % len(bild))
                self.write(bild)
                self.served_image_timestamp = time.time()
                yield tornado.gen.Task(self.flush)

            else:
                yield tornado.gen.Task(ioloop.add_timeout, ioloop.time() + interval)


class HtmlPageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, datei_name='index.html'):
        start_seite = os.path.join(html_pfad, datei_name)
        if os.path.exists(start_seite):
            self.render('www/' + datei_name)

        else:
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=datei_name)

            self.finish(err_html)


class SetParamsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        try: 
            self.write({'resp': 'ok'})

        except:
            self.write({'resp': 'bad'})
            self.flush()
            self.finish()