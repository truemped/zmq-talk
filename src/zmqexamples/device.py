import sys
import time
import zmq


def device():
    ctx = zmq.Context()

    frontend = ctx.socket(zmq.XREP)
    frontend.bind("tcp://127.0.0.1:12345")

    backend = ctx.socket(zmq.XREQ)
    backend.bind("tcp://127.0.0.1:12346")

    zmq.device(zmq.QUEUE, frontend, backend)


def device_worker():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.setsockopt(zmq.IDENTITY, sys.argv[1])
    socket.connect("tcp://127.0.0.1:12346")

    try:
        while True:
            request = socket.recv()
            response = "Worker: '%s'" % sys.argv[1]
            print response
            time.sleep(.5)
            socket.send(response)
    except:
        pass

    socket.close()
    ctx.term()
