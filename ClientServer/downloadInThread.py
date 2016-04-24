import threading
import time
from Queue import Queue
from fileDownloader import runDownloader
print_lock = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]

    def run(self):
        print threading.currentThread().getName(), self.receive_messages
        while True:
            val = self.queue.get()
            if val is None:
                print("Returning")
                return
            self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        if self.receive_messages:
            with print_lock:
                print threading.currentThread().getName(), "Received {}".format(message)
                if "download" in message:
                    sec = message.split(":")[1]
                    runDownloader(int(sec))
                elif "sleep" in message:
                    sec = message.split(":")[1]
                    time.sleep(int(sec))


if __name__ == '__main__':
    downloaderQ = Queue()
    downloaderThread = MyThread(downloaderQ, args=(True,))
    downloaderThread.start()

    downloaderThread.queue.put("download:10")
    downloaderThread.queue.put("sleep:15")
    downloaderThread.queue.put(None)
    downloaderThread.join()
