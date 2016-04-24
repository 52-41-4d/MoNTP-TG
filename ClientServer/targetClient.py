import socket
import sys
import subprocess
import time

def getPingData():
    p = subprocess.Popen(['ping', '-c', '1', '-t', '1', 'www.google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if "64 bytes" in out:
        p_out = out.split('\n')
        rtt = p_out[-2:-1][0].split(" ")[3].split("/")[0]
    else:
        rtt = "-1.0"

    return rtt

def sendPingData(commandServer, commandServerPort, rtt):
    clientsocket = None
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientsocket.sendto(rtt, (commandServer, commandServerPort))
    except:
        print "Socket hang"
    finally:
        clientsocket.close()

if __name__ == "__main__":
    commandServer = sys.argv[1]
    commandServerPort = int(sys.argv[2])
    iterations = int(sys.argv[3])

    for i in range(0, iterations):
        rtt = getPingData()
        print rtt
        sendPingData(commandServer, commandServerPort, rtt)
        time.sleep(1)

    sendPingData(commandServer, commandServerPort, "END")
