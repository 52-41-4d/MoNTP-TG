import socket
from threading import Thread, Condition

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

class Client(Thread):
	def __init__(self,host,port,name):
		Thread.__init__(self)
		self.port = port
		self.host = host
		self.name = name
		self.bufsize = 1024
		self.addr = (host,port)

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def run(self):
		invalid = True
		while invalid:
			try:
				invalid = False
				self.socket.connect(self.addr)
			except:
				invalid = True
				'''
				while True:
					data = raw_input('> ')
					if not data:
						continue
			data = name+' said : '+data
			self.socket.send(data)
			'''
			global queue
			while True:
				condition.acquire()
				if not queue:
					condition.wait()
					num = queue.pop()
					if num == "10.6":
						commandVal = "set:tx-power:24"
						print "Consumed", commandVal
						self.socket.send(commandVal)
						condition.release()

hostServer = raw_input('Enter Server address: ').strip()
hostClient = raw_input('Enter Client address: ').strip()
p1 = int(raw_input('Enter Server port : '))
p2 = int(raw_input('Enter Client port : '))
name = raw_input('Enter Your Name: ').strip()

server = Server(hostServer,p1,name)
client = Client(hostClient,p2,name)

server.start()
client.start()

server.join()
