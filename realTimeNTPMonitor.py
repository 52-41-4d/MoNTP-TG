#!/usr/bin/python
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import time
import collections
import numpy as np
from sntp_client import SNTP_main

__author__ = 'rkrish@cs.wisc.edu'

interval = 25
arr = []
args = ""

class DynamicPlotter():
    def __init__(self, sampleinterval=0.5, timewindow=100., size=(1200,300)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        # For SNTP
        self.databuffer4 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x4 = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y4 = np.zeros(self._bufsize, dtype=np.float)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="MoNTP Realtime Plotting")
        self.win.resize(*size)

        self.plt3 = self.win.addPlot(title='NTP Measurements')
        self.plt3.addLegend()
        self.plt3.showGrid(x=True, y=True)
        self.plt3.setLabel('left', 'Offset', 's')
        self.plt3.setLabel('bottom', 'time', 's')
        self.curve4 = self.plt3.plot(self.x4, self.y4, pen=(0,255,255), name="SNTP")

        # QTimer
        self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.updateplotTest)
        self.timer.timeout.connect(self.updateplotMain)
        self.timer.start(self._interval)

    def updateplotMain(self):
        milli, sntp_offset = SNTP_main()
        if milli!='N' and sntp_offset!='N':
            self.databuffer4.append(float(sntp_offset))
            print "{0},{1}".format(int(time.time()), sntp_offset)
        else:
            self.databuffer4.append(None)

        self.y4[:] = self.databuffer4
        self.curve4.setData(self.x4, self.y4)
        self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    m = DynamicPlotter(sampleinterval=20, timewindow=100.)
    m.run()
