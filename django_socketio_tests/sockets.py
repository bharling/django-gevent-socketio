from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from socketio.mixins import BroadcastMixin
import logging
import datetime
import gevent
from gevent import Greenlet
import time
import random

class MainloopGreenlet(Greenlet):
    def __init__(self):
        Greenlet.__init__(self)
        self.logger = logging.getLogger("socketio.chat")
        self.log("Creating Main Loop")
        self.lastFrameTime = 0
        self.clients = []
        self.running = True
        self.threshold = 1.0 / 30.0
        self.frame = 0
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format("MAINLOOP", message))
        
    def run(self):
        while self.running:
            t = time.clock()
            if t - self.lastFrameTime >= self.threshold:
                self.tick()
                self.lastFrameTime = t
                self.frame += 1
            gevent.sleep(0.001)
            
    def subscribe(self, other):
        self.clients.append(other)
        
    def tick(self):
        for client in self.clients:
            client.update(self.frame)
            
main_loop = MainloopGreenlet()
main_loop.start()

def getRandomColour():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

        
@namespace('/player')
class PlayerNamespace(BaseNamespace, BroadcastMixin):
    
    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")
        main_loop.subscribe(self)
        self.id = "p_" + self.socket.sessid
        self.colour = getRandomColour()
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 600)
        self.broadcast_event_not_me('player_joined', self.id, self.colour, self.x, self.y)
        
    def move(self):
        self.x += random.randint(-1,1)
        self.y += random.randint(-1,1)
            
    def update(self, t):
        self.move()
        self.broadcast_event_not_me('update_player', self.id, self.x, self.y)
        
    def on_mouse(self, x, y):
        return True
    
    def on_echo(self, message):
        self.log(message)
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
        
        
    