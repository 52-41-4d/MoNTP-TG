import socket
from threading import Thread, Condition
from downloadInThread import MyThread
import argparse
from collections import deque
from Queue import Queue

condition = Condition()
queue = []

class Server(Thread):
    def __init__(self,host,port,name):
        Thread.__init__(self)
        self.port = port
        self.host = host
        self.name = name
        self.bufsize = 1024
        self.addr = (host,port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.addr)

    def run(self):
        self.socket.listen(5)
        while True:
            print 'Waiting for connection..'
            client, caddr = self.socket.accept()
            print 'Connected To',caddr

            data = client.recv(self.bufsize)
            if not data:
                continue
            print data
            condition.acquire()
            queue.append(data)
            print "Produced", data
            condition.notify()
            condition.release()
            if data == "END":
                return

class Client(Thread):
    def __init__(self,host,port,name, delays, txpower, mintxpower, maxtxpower, incThreshold, decThreshold):
        Thread.__init__(self)
        self.port = port
        self.host = host
        self.name = name
        self.bufsize = 1024
        self.addr = (host,port)
        self.delays = delays
        self.txpower = txpower
        self.mintxpower = mintxpower
        self.maxtxpower = maxtxpower
        self.incThreshold = incThreshold
        self.decThreshold = decThreshold
        self.socket = None

    def sendSocketData(self, data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.addr)
        except Exception as e:
            print "Exception in Client", e
        self.socket.send(data)
        self.socket.close()

    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                condition.wait()
                num = queue.pop()
                if num == "END":
                    sendSocketData("END")
                    return
                num = float(num)
                self.delays.append(num)
                changePower = False
                if len(self.delays) == self.delays.maxlen and self.delays.count(-1) >= self.incThreshold  and self.txpower < self.maxtxpower:
                    self.txpower += 1
                    changePower = True
                    self.delays.clear()
                elif len(self.delays) == self.delays.maxlen and self.delays.count(-1) <= self.decThreshold  and self.txpower > self.mintxpower:
                    self.txpower -= 1
                    changePower = True
                    self.delays.clear()
                if changePower:
                    commandVal = "set:tx-power:" + str(self.txpower)
                    print "Consumed", commandVal
                    self.sendSocketData(commadVal)
                    condition.release()

if __name__ == "__main__":
    progName = "downloadInThread"
    parser = argparse.ArgumentParser(prog = progName)
    parser.add_argument("-s", "--baseIP", dest="baseIP", help="server address")
    parser.add_argument("-c", "--commandIP", dest="commandIP", help="client address")
    parser.add_argument("-a", "--basePort", dest="basePort", help="server port", type=int)
    parser.add_argument("-b", "--commandPort", dest="commandPort", help="client port", type=int)
    parser.add_argument("-n", "--name", dest="name", help="Name")
    parser.add_argument("-d", "--downloadTime", dest="dTime", help="Download time")
    parser.add_argument("-k", "--sleepTime", dest="sTime", help="Sleep time")
    parser.add_argument("-i", "--iterations", dest="iteration", help="No. of iterations", type=int)
    args = parser.parse_args()

    downloaderQ = Queue()
    downloaderThread = MyThread(downloaderQ, args=(True,))

    server = Server(args.commandIP, args.commandPort, args.name)
    client = Client(args.baseIP, args.basePort, args.name, deque(maxlen=15),22, 22, 27, 5, 2)
    server.start()
    client.start()
    downloaderThread.start()

    for i in range(0, args.iteration):
        downloaderThread.queue.put("download:"+args.dTime)
        downloaderThread.queue.put("sleep:"+args.sTime)

    downloaderThread.queue.put(None)
    downloaderThread.join()
    server.join()
