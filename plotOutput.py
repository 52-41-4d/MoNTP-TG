import matplotlib.pyplot as plt
import sys

def main(prefix):
    offset = []
    ts = []
    rssi = []
    noise = []
    rtt = []
    with open('runOutput_'+prefix+'.txt', 'r') as fH:
        for line in fH:
            line = line.strip()
            vals = line.split(",")
            ts.append(float(vals[0]))
            rssi.append(float(vals[1]))
            noise.append(float(vals[2]))
            rtt.append(float(vals[3]))
            try:
                if len(vals)==5:
                    offset.append(float(vals[4]))
                else:
                    offset.append(0.0)
            except:
                print "Error"


    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].grid()
    axarr[0].plot(ts, rssi, label="Signal strength (dBm)", lw=3)
    axarr[0].plot(ts, noise, label="Noise strength (dBm)", lw=3)
    axarr[0].legend()
    axarr[1].grid()
    axarr[1].bar(ts, offset, label="SNTP offset (s)", lw=3)
    axarr[1].legend()

    f.text(0.5, 0.04, 'Timestamp', ha='center')
    f.text(0.04, 0.5, 'Measured values', va='center', rotation='vertical')
    f.savefig('plot_'+prefix+'.eps', format='eps', dpi=1000)

if __name__ == "__main__":
    prefix = sys.argv[1]
    main(prefix)
