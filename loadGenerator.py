#!/usr/bin/python

'''
Generates artificial interference via loading the channel and
targets a particular access point. Use at your own risk.
'''

__author__ = 'rkrish@cs.wisc.edu'

from threading import Timer
import argparse
from time import sleep
import subprocess

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def generatePulse(amplitude, server):
    print "Run iPerf to server ({0}) with amplitude={1}!".format(server, amplitude)
    iperfCommand = "iperf -c {0}".format(server)
    process = subprocess.Popen(iperfCommand, stdout=subprocess.PIPE, stderr=None, shell=True)
    for line in iter(process.stdout.readline,''):
        print line

def main(args):
    # print args.ap, args.channel, args.interval, args.type
    if args.type == "pulse":
        rt = RepeatedTimer(args.interval, generatePulse, args.amplitude, args.server)
    try:
        sleep(args.MAXVAL)
    finally:
        rt.stop()

if __name__ == "__main__":
    progName = "loadGenerator"
    parser = argparse.ArgumentParser(prog = progName)
    parser.add_argument("-a", "--ap", help="MAC address of the access point", dest="ap")
    parser.add_argument("-c", "--channel", help="WiFi Channel", dest="channel")
    parser.add_argument("-i", "--interval", help="Interval for generating pulses.", dest="interval", type=int)
    parser.add_argument("-t", "--type", help="Type of traffic.", dest="type")
    parser.add_argument("-g", "--height", help="Wave's amplitude.", dest="amplitude", type=int)
    parser.add_argument("-m", "--maxval", help="Max Value.", dest="MAXVAL", type=int)
    parser.add_argument("-s", "--server", help="Server address", dest="server")
    args = parser.parse_args()
    main(args)
