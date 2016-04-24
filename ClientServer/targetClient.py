import socket
import sys
import subprocess
import time

def getPingData():
    p = subprocess.Popen(['ping', '-c', '1', 'www.google.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if "64 bytes" in out:
        p_out = out.split('\n')
        rtt = p_out[-2:-1][0].split(" ")[3].split("/")[0]
    else:
        rtt = "-1.0"

    return rtt

if __name__ == "__main__":
    commandServer = sys.argv[1]
    commandServerPort = int(sys.argv[2])
    iterations = int(sys.argv[3])

    
    for i in range(0, iterations):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((commandServer, commandServerPort))
        rtt = getPingData()
        clientsocket.send(rtt)
        clientsocket.close()
        time.sleep(1)
