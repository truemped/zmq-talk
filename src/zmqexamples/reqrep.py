import time
import sys
import zmq


def rep():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://0.0.0.0:12345")

    try:
        while True:
            request = socket.recv()
            print request
            time.sleep(.5)
            socket.send(request)
    except:
        pass

    socket.close()
    ctx.term()


def req():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.setsockopt(zmq.IDENTITY, sys.argv[1])
    socket.connect("tcp://0.0.0.0:12345")

    try:
        while True:
            socket.send("Hello World %s" % sys.argv[1])
            print socket.recv()
    except:
        raise

    socket.close()
    ctx.term()
