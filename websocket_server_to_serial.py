
import serial
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

ser = serial.Serial('/dev/tty.usbmodem14101', 9600)

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.peer = request.peer
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        if "193.93.249.99" not in self.peer:
            print("closing connection")
            self.sendClose()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            ser.write(payload+"\n")     # write a string
        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://localhost:8024")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)


    reactor.listenTCP(8024, factory)
    reactor.run()
