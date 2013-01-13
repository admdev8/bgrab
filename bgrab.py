#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" bgrab

    Multi-threaded TCP banner grabbing.

    Author: marpie (marpie@a12d404.net)

    Last Update:  20130113
    Created:      20130113

"""
import socket
from Queue import Queue
from threading import Thread, Event
from time import sleep

# Version Information
__version__ = "0.0.1"
__program__ = "bgrab v" + __version__
__author__ = "marpie"
__email__ = "marpie+bgrab@a12d404.net"
__license__ = "BSD License"
__copyright__ = "Copyright 2013, a12d404.net"
__status__ = "Prototype"  # ("Prototype", "Development", "Testing", "Production")

#SCRIPT_PATH = os.path.dirname( os.path.realpath( __file__ ) )


def grab_banner(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = ""
    try:
        sock.connect((host, port))
        res = sock.recv(4096)
    except:
        pass
    sock.close()
    return (host, port, res,)

def parse_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                host, port = line.strip().replace('"', '').split(",")
                port = int(port)
                lines.append((host,port,))
            except:
                pass
    if (len(lines) == 1):
        return None
    return lines

def thread_grab(input_queue, output_queue):
    while not input_queue.empty():
        host, port = input_queue.get(False)
        output_queue.put(grab_banner(host, port))
        input_queue.task_done()

class OutputThread(Thread):
    def __init__(self, output_queue):
        super(OutputThread, self).__init__()
        self._stop = Event()
        self._output_queue = output_queue

    def run(self):
        while not self.stopped():
            host, port, result = self._output_queue.get()
            print("%s:%d --> %s" % (host, port, repr(result)))
            self._output_queue.task_done()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

# Main
def main(argv):
    MAX_THRADS = 10
    TIMEOUT = 2
    socket.setdefaulttimeout(TIMEOUT) # two seconds

    if len(argv) < 2:
        print("bgrab.py [filename]")
    
    services = parse_file(argv[1])
    if not services:
        print("[X] Error parsing input file!")
        return False

    input_queue = Queue()
    output_queue = Queue()

    # fill input queue
    for host,port in services:
        input_queue.put((host, port,))

    # start processing threads
    for i in xrange(0,MAX_THRADS):
        Thread(target=thread_grab, args=(input_queue,output_queue,)).start()

    # start output thread
    out_thread = OutputThread(output_queue)
    out_thread.setDaemon(True)
    out_thread.start()

    input_queue.join()
    output_queue.join()

    out_thread.stop()

    print("[*] Done.")

    return True


if __name__ == "__main__":
    import sys
    print( __doc__ )
    sys.exit( not main( sys.argv ) )
