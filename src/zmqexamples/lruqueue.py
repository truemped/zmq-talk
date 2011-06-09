from collections import deque
import sys
import time
import zmq


def lru_queue():
    ctx = zmq.Context()

    frontend = ctx.socket(zmq.XREP)
    frontend.bind("tcp://127.0.0.1:12345")

    backend = ctx.socket(zmq.XREP)
    backend.bind("tcp://127.0.0.1:12346")

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    workers = deque()

    while True:
        socks = dict(poller.poll())

        if (backend in socks and socks[backend] == zmq.POLLIN):
            worker_addr = backend.recv()
            print "Worker: '%s'" % worker_addr
            workers.appendleft(worker_addr)

            assert backend.recv() == ""
            client_addr = backend.recv()

            if client_addr != "READY":
                assert backend.recv() == ""
                rep = backend.recv()

                frontend.send(client_addr, zmq.SNDMORE)
                frontend.send("", zmq.SNDMORE)
                frontend.send(rep)

        if len(workers) > 0:
            if (frontend in socks and socks[frontend] == zmq.POLLIN):
                msg = frontend.recv_multipart()

                worker_addr = workers.pop()
                msg = [worker_addr, "", msg[0], "",  msg[2]]

                backend.send_multipart(msg)


def lru_worker():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.setsockopt(zmq.IDENTITY, sys.argv[1])
    socket.connect("tcp://127.0.0.1:12346")
    socket.send("READY")

    try:
        while True:
            [client_addr, empty, request] = socket.recv_multipart()
            response = "Client: '%s', Worker: '%s'" % (client_addr,
                sys.argv[1])
            print response
            time.sleep(.5)
            socket.send_multipart([client_addr, "", response])
    except:
        raise

    socket.close()
    ctx.term()
