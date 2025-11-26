# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket
import sys
import datetime
import whois


def scan_ports():
    for port in range(1, 1025):
        if port % 10 == 0:
            print("Scanning port {}".format(port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            output.write("Port {}: 	 Open\n".format(port))
        sock.close()

# Ask for input
remoteServer = input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

w = whois.whois(remoteServer)
print("Domain name:", w["domain_name"], "\nname:",
    w["name"], "\norg:", w["org"], "\naddress:", w["address"], "\ncity:",
    w["city"], "\nstate:", w["state"], "\ncountry:", w["country"])

# Create a file to print the result of the port scan
output = open("open_ports.txt", "w")

# Print a nice banner with information on which host we are about to scan
print("-" * 60)
print("Please wait, scanning remote host", remoteServerIP)
print("-" * 60)
output.write("-" * 60 + "\n")
output.write("Please wait, scanning remote host {}\n".format(remoteServerIP))
output.write("-" * 60 + "\n")
output.close()

# Check what time the scan started
t1 = datetime.datetime.now()

# Using the range function to specify ports
# (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

output = open("open_ports.txt", "a")

try:
    scan_ports()

except KeyboardInterrupt:
    output.write("You pressed Ctrl+C\n")
    sys.exit()

except SystemExit:
    output.write("Execution terminated\n")
    sys.exit()

except socket.gaierror:
    output.write("Hostname could not be resolved. Exiting\n")
    sys.exit()

except socket.error:
    output.write("Couldn't connect to server\n")
    sys.exit()

# Checking the time again
t2 = datetime.datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total = t2 - t1

# Printing the scan duration in the file
output.write("Scanning Completed in: {}\n".format(total))

output.close()