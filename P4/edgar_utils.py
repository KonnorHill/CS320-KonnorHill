from bisect import bisect
import netaddr
import re
import pandas as pd


ips = pd.read_csv("ip2location.csv")


def lookup_region(ip_address):
    global ips
    
    ipaddr = re.sub(r'[a-z]', '0', ip_address)
    ip_int = int(netaddr.IPAddress(ipaddr))
    region = ips.iloc[(bisect(ips['low'], ip_int)) - 1][3]
    
    return region


class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"20\d{2}-\d{2}-\d{2}|19\d{2}-\d{2}-\d{2}", html)
        
        sic = re.search(r"SIC=\D*(\d*)", html)
        self.sic = int(sic.group(1)) if sic else None
        
        self.addresses = []
        for addr in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = [line.strip() for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr) if line.strip()]
            address = "\n".join(lines)
            self.addresses.append(address)
        self.addresses = [address for address in self.addresses if address]

    def state(self):
        for line in self.addresses:
            state = re.search(r"([A-Z]{2}) \d{5}", line)
            if state:
                return state.group(1)
        return None
