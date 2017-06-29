#! /usr/bin/env python3

import socket
import subprocess
import sys
import re
from datetime import datetime

def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


# clear the console
subprocess.call('clear', shell=True)

rgx_option = re.compile(r'^(--[a-z]{2})|(-[a-z])$')
rgx_host = re.compile(r'^www.')

# read the remote host and options
options = []
remote_server = None

for arg in sys.argv:
    if re.match(rgx_host, arg):
        remote_server = arg
    if re.match(rgx_option, arg):
        options.append(arg)

if not remote_server:
	sys.exit("[ERROR] You have to pass the remote host to scan as a parameter !")

# get the ip adress of this host
remote_server_ip = socket.gethostbyname(remote_server)

print ("-" * 60)
print ("HOST TO SCAN \"%s\"" % remote_server)
print ("-" * 60 + '\n')
print ("IP adress : %s \n" % remote_server_ip)

print ("Scanning the remote host, please wait...")
start_time = datetime.now()

if '--fast' in options:
    # try only the common ports
    ports = [20, 21, 22, 23, 25, 53, 68, 80, 110, 137, 138, 139, 143, 220, 443, 445]
else:
    # try each port from 1 to 1024
    print("it can take a while")
    ports = range(1, 1025)

try:
    for port in ports:
        if is_port_open(remote_server_ip, port):
            print ("Port %d: 	 Open" % port)

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
