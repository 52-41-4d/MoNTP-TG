#!/usr/bin/python
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import netifaces
import pyping
import os
import subprocess
import getpass
import collections
import random
import time
import math
import numpy as np

'''
Sample output:
agrCtlRSSI: -61, agrExtRSSI: 0, agrCtlNoise: -89, agrExtNoise: 0, state: running, op mode: station, lastTxRate: 145, maxRate: 144,
lastAssocStatus: 0, 802.11 auth: open, link auth: none, BSSID: e8:ba:70:f8:3d:8e, SSID: COMPSCI-OPEN, MCS: 15, channel: 48
'''

__author__ = 'rkrish@cs.wisc.edu'

interval = 0.5
arr = []
args = ""
try:
    with open('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'): pass
except IOError:
    print "Airport is not where I am expecting it to be. Cannot setup symlink!"
try:
    with open('/usr/bin/airport'): pass
except IOError:
    sudoPassword = getpass.getpass()
    setitup = "sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/bin/airport"
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, setitup))

command = "airport -I"
outpath = ""

class DynamicPlotter():
    def __init__(self, sampleinterval=0.5, timewindow=100., size=(600,700)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        # For signals
        self.databuffer1 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer2 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x1 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y1 = np.zeros(self._bufsize, dtype=np.float)
        self.x2 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y2 = np.zeros(self._bufsize, dtype=np.float)
        # For ping
        self.databuffer3 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x3 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y3 = np.zeros(self._bufsize, dtype=np.float)

        # PyQtGraph stuff
        self.app = QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="MoNTP Realtime Plotting")
        self.win.resize(*size)

        self.plt1 = self.win.addPlot(title='WiFi Signals')
        self.plt1.addLegend()
        # self.plt.resize(*size)
        self.plt1.showGrid(x=True, y=True)
        self.plt1.setLabel('left', 'strength', 'dBm')
        self.plt1.setLabel('bottom', 'time', 's')
        self.curve1 = self.plt1.plot(self.x1, self.y1, pen=(0,255,0), name="Signal")
        self.curve2 = self.plt1.plot(self.x2, self.y2, pen=(255,0,0), name="Noise")
        self.win.nextRow()
        self.plt2 = self.win.addPlot(title='Ping Measurements')
        self.plt2.addLegend()
        self.plt2.showGrid(x=True, y=True)
        self.plt2.setLabel('left', 'RTT', 'ms')
        self.plt2.setLabel('bottom', 'time', 's')
        self.curve3 = self.plt2.plot(self.x3, self.y3, pen=(0,0,255), name="Min.")

        # QTimer
        self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.updateplotTest)
        self.timer.timeout.connect(self.updateplotMain)
        self.timer.start(self._interval)

    def getdata1(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def getdata2(self):
        frequency = 0.5
        noise = random.normalvariate(0.5, 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateplotTest(self):
        self.databuffer1.append( self.getdata1() )
        self.databuffer2.append( self.getdata2() )
        self.y1[:] = self.databuffer1
        self.y2[:] = self.databuffer2
        self.curve1.setData(self.x1, self.y1)
        self.curve2.setData(self.x2, self.y2)
        self.app.processEvents()

    def updateplotMain(self):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        for line in iter(process.stdout.readline,''):
            line = line.strip()
            vals = line.split(": ")
            if "BSSID" in vals[0]:
                ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
                r = pyping.ping(ip, count=1)
                self.databuffer3.append(float(r.min_rtt))
            if "agrCtlRSSI" in vals[0]:
                self.databuffer1.append(float(vals[1]))
            if "agrCtlNoise" in vals[0]:
                self.databuffer2.append(float(vals[1]))
            self.y1[:] = self.databuffer1
            self.y2[:] = self.databuffer2
            self.y3[:] = self.databuffer3
            self.curve1.setData(self.x1, self.y1)
            self.curve2.setData(self.x2, self.y2)
            self.curve3.setData(self.x3, self.y3)
            self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    m = DynamicPlotter(sampleinterval=0.5, timewindow=100.)
    m.run()
