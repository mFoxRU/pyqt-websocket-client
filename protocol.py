# encoding: utf-8
__author__ = 'mFoxRU'

from autobahn.twisted import WebSocketClientProtocol, WebSocketClientFactory


class Protocol(WebSocketClientProtocol):

    callback = lambda x, y: None

    def __init__(self):
        super(Protocol, self).__init__()
        self.factory.con = self

    def onConnect(self, response):
        self.callback('WebSocket connected')

    def onOpen(self):
        self.callback('WebSocket ready')

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.callback('Binary message of size {}'.format(len(payload)))
        else:
            self.callback('Message: {}'.format(payload))

    def onClose(self, wasClean, code, reason):
        self.callback('Connection closed. Reason: {}(code {})'.format(
            reason, code))


class Factory(WebSocketClientFactory):
    def __init__(self, callback):
        super(Factory, self).__init__()
        self.callback = callback
        self.protocol = Protocol
        self.protocol.factory = self
        self.protocol.callback = callback
        self.con = None

    def disconnect(self):
        if self.con is not None:
            self.con.sendClose()
        self.con = None

    def send_msg(self, msg):
        if self.con is None or not msg:
            return
        self.con.sendMessage(msg)

    def clientConnectionFailed(self, connector, reason):
        self.callback(reason)
