import nmap
import pprint

nm =nmap.PortScanner()

scanrange=nm.scan(hosts="192.168.1.100-105")
pprint.pprint(scanrange["scan"])

# ==========================
def scan_network():
    nm = nmap.PortScanner()
    scan_range = nm.scan(hosts="192.168.0.104")
    data = scan_range['scan']
    for value in data.values():
        print(value['addresses'])
        print('status: ', value['status']['state'])
        print(value['tcp'])


scan_network()