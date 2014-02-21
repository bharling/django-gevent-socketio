from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from socketio.mixins import BroadcastMixin
import logging
import gevent
from gevent import Greenlet
import time
import random
from game_types import Vector2

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
        
    def unsubscribe(self, other):
        if other in self.clients: self.clients.remove(other)
        
    def tick(self):
        for client in self.clients:
            client.update(self.frame)
            
main_loop = MainloopGreenlet()
main_loop.start()

def getRandomColour():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def clamp(n, minN, maxN):
    return max(min(maxN,n), minN)


    
        
                

class Player(object):
    def __init__(self, id, colour, x, y):
        self.id = id
        self.colour = colour
        self.position = Vector2.random()
        self.velocity = Vector2.random()
        self.nextVelocity = Vector2.random()
        self.transition = 0.0
        self.turningSpeed = 0.1 + random.uniform(0.0, 0.8)
        
    def update(self):
        if random.random() < 0.2 and self.transition == 0.0:
            # lets change direction
            self.nextVelocity = Vector2.random()
            self.transition += self.turningSpeed
        if self.transition:
            self.velocity = self.velocity.lerp(self.nextVelocity, self.transition)
            if self.transition >= 1.0:
                self.transition = 0.0
        self.move()
        
    @property
    def x(self):
        return self.position.x 
    
    @property
    def y(self):
        return self.position.y
            
        
    def move(self):
        self.position += self.velocity
        if self.position.x < 0:
            self.velocity.x *= -1
            self.position.x = 1.0
            self.transition = 0.0
        if self.position.x > 600:
            self.velocity.x *= -1
            self.position.x = 599.0
            self.transition = 0.0
        if self.position.y < 0:
            self.velocity.y *= -1
            self.position.y = 1.0
            self.transition = 0.0
        if self.position.y > 600:
            self.velocity.y *= -1
            self.position.y = 599.0
            self.transition = 0.0
        
    def __str__(self):
        return "Player: " + self.id

        
@namespace('/player')
class PlayerNamespace(BaseNamespace, BroadcastMixin):
    players = []
    
    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")
        id = "p_" + self.socket.sessid
        colour = getRandomColour()
        self.player = Player(id, colour, 0, 0)
        self.players.append(self.player)
        self.log(",".join([str(p) for p in self.players]))
        self.broadcast_event('player_joined', self.player.id, self.player.colour, self.player.position.x, self.player.position.y)
        self.send_current_players()
        main_loop.subscribe(self)
        
    def send_current_players(self):
        for p in self.players:
            if p is not self.player:
                self.emit('player_joined', p.id, p.colour, p.position.x, p.position.y)
        
    def recv_disconnect(self):
        main_loop.unsubscribe(self)
        self.players.remove(self.player)
        self.broadcast_event_not_me('player_left', self.player.id)
        BaseNamespace.recv_disconnect(self)
            
    def update(self, t):
        self.player.update()
        self.broadcast_event('update_player', self.player.id, self.player.position.x, self.player.position.y)
        
    def on_mouse(self, x, y):
        return True
    
    def on_echo(self, message):
        self.log(message)
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
        
        
    