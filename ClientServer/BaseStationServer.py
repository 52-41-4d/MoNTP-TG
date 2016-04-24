import socket
import getpass
import subprocess

def main(sudoPassword):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('0.0.0.0', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(1024)
        if not buf:
            command, typ, value  = buf.split(":")
            if command == "set" and typ == "tx-power":
                iwconfig_command = "echo {0}| sudo -S sudo iwconfig wlan1 txpower {1}".format(sudoPassword, value)
                process = subprocess.Popen(iwconfig_command, stdout=subprocess.PIPE, stderr=None, shell=True)
                if process!=None and process > 0:
                    print "Tx power changed to {0}".format(value)

if __name__ == "__main__":
    sudoPassword = getpass.getpass()
    main(sudoPassword)
