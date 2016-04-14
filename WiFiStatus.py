#!/usr/bin/python
import os
import subprocess
import time
import getpass
import argparse

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

def _log(text):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    values = []
    for line in iter(process.stdout.readline,''):
        if "agrCtlRSSI" in line:
            values.append(line.strip())
        if "BSSID" in line:
            values.append(line.strip())
        if "agrCtlNoise" in line:
            values.append(line.strip())
    print ", ".join(values)

def parseArgs():
    parser = argparse.ArgumentParser(description='Display airport interface statistics')
    parser.add_argument('-o', help="path for output", required=False, dest='outpath')
    return args

if __name__ == '__main__':
    args = parseArgs()
    while True:
        _log('')
        arr =[]
        time.sleep(interval)
