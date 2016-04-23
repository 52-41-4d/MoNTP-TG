from __future__ import division
import numpy as np
import sys
import matplotlib.pyplot as plt
from collections import Counter

def plotDeviations(offsets):
    meanVal = numpy.mean(offsets)
    diffs = [ f-meanVal for f in offsets]
    totalDiffs = len(diffs)
    plotX = []
    plotY = []
    for k,v in Counter(diffs).items():
        plotX.append(k)
        plotY.append(v/totalDiffs)

    print(plotX)
    print(plotY)

def main():
    fileStr = sys.argv[1]
    fileList = fileStr.strip().split(",")
    for f in fileList:
        offsets = []
        with open(f) as fh:
            for l in fh:
                ts, offset = l.strip().split(",")
                if offset != "N":
                    offsets.append(offset)
        print(f)
        plotDeviations(offsets)

if __name__ == "__main__":
    main()
