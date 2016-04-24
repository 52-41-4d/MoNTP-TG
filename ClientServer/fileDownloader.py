import time
from subprocess import STDOUT, check_output as qx
import subprocess as sub
import threading
import sys

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

def runDownloader(downloadTime):
    print("Starting download")
    RunCmd(["python", "download.py"], downloadTime).Run()
    print("Done - stopping")
