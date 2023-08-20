import nmap

nm = nmap.PortScanner()
nm.scan('192.168.0.0/24', arguments='-p 80')

for host in nm.all_hosts():
    print('Host: %s (%s)' % (host, nm[host].hostname()))
    print('State: %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        print('Protocol: %s' % proto)
        ports = nm[host][proto].keys()
        for port in ports:
            print('Port: %s\tState: %s' % (port, nm[host][proto][port]['state']))
            
            
            
            
            
            
            
import socket

for i in range(1, 255):
    ip = "192.168.0." + str(i)
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 80))
        print("Host at {} is responding".format(ip))
        s.close()
    except:
        pass
      
      
from scapy.all import *

for i in range(1, 255):
    ip = "192.168.0." + str(i)
    p = IP(dst=ip)/ICMP()
    res = sr1(p, timeout=1, verbose=0)
    if res:
        print("Host at {} is responding".format(ip))      
