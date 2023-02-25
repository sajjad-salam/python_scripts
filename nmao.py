import nmap
import pprint

nm =nmap.PortScanner()

scanrange=nm.scan(hosts="192.168.1.100-105")
pprint.pprint(scanrange["scan"])