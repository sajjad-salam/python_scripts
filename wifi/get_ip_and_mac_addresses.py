import os
import re

def get_ip_and_mac_addresses():
    result = os.popen("arp -a").read()
    print("Result: ", result)

    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+([a-fA-F0-9:]{17})')
    addresses = re.findall(pattern, result)
    print("Addresses: ", addresses)

    for address in addresses:
        print("IP:", address[0], "MAC:", address[1])

get_ip_and_mac_addresses()
