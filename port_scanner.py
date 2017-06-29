#! /usr/bin/env python3

import socket
import subprocess
import sys
from datetime import datetime

# clear the console
subprocess.call('clear', shell=True)

# read the remote host
if len(sys.argv) < 2:
	sys.exit("[ERROR] You have to pass the remote host to scan as a parameter !")
remote_server = sys.argv[1]

# get the ip adress of this host
remote_server_ip = socket.gethostbyname(remote_server)

print ("-" * 60)
print ("HOST TO SCAN \"%s\"" % remote_server)
print ("-" * 60 + '\n')
print ("IP adress : %s \n" % remote_server_ip)

print ("Scanning the remote host, please wait...")
start_time = datetime.now()

# try each port from 1 to 1024
try:
    print("it can take a while")
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((remote_server_ip, port))
        if result == 0:
            print ("Port %d: 	 Open" % port)
        sock.close()

# handle quit
except KeyboardInterrupt:
    print ("Scan stopped: You pressed Ctrl+C")
    sys.exit()

# handle errors
except socket.gaierror:
    print ("Hostname could not be resolved. Exiting")
    sys.exit()
except socket.error:
    print ("Couldn't connect to server")
    sys.exit()

end_time = datetime.now()
print ("scan done in %s seconds" % str((end_time - start_time).total_seconds()))
