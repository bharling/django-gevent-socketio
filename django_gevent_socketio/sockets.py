from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
import logging

@namespace('/gevent_socketio_isworking')
class GeventSocketioTestNamespace(BaseNamespace):
    
    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")
    
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
    
    def on_echo(self, message):
        self.emit('echo', {'message':message})
        return True
        
        
    