##
## A very low level AR.Drone2.0 Python controller
## by Micah Sherr
## (use at your own risk)
##


import socket
import sys, tty, termios

def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def setBits( lst ):
    """
    set the bits in lst to 1.
    also set bits 18, 20, 22, 24, and 28 to one (since they should always be set)
    all other bits will be 0
    """
    res = 0
    for b in lst + [18,20,22,24,28]:
        res |= (1 << b)
    return res


def sendCommand( cmd ):
    global address
    global seqno
    global s
    print "DEBUG: Sending:  '%s'" % cmd.strip()
    s.sendto(cmd,address)
    seqno += 1


def reset():
    global seqno
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    seqno = 1
    roll_index = len(power_values) / 2
    pitch_index = len(power_values) / 2
    gaz_index = len(power_values) / 2
    yaw_index = len(power_values) / 2
    for i in xrange(1, 25):
        sendCommand("AT*FTRIM=%d\r" % seqno )

        
def takeoff():
    global seqno
    sendCommand("AT*FTRIM=%d\r" % seqno )
    takeoff_cmd = setBits([9])
    for i in xrange(1,25):   
        sendCommand("AT*REF=%d,%d\r" % (seqno,takeoff_cmd))

        
def land():
    global seqno
    land_cmd = setBits([])
    for i in xrange(1,25):
        sendCommand("AT*REF=%d,%d\r" % (seqno,land_cmd))


def toggleEmergencyMode():
    global seqno
    shutdown_cmd = setBits([8])
    sendCommand("AT*REF=%d,%d\r" % (seqno,shutdown_cmd))

def flyleft():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if roll_index > 0:
        roll_index -= 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def flyright():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_indexaaafffff
    global yaw_index
    if roll_index < len(power_values) - 1:
        roll_index += 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def flyforward():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if pitch_index > 0:
        pitch_index -= 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def flybackward():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if pitch_index < len(power_values) - 1:
        pitch_index += 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def flydown():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if gaz_index > 0:
        gaz_index -= 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def flyup():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if gaz_index < len(power_values) - 1:
        gaz_index += 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def spinleft():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if yaw_index > 0:
        yaw_index -= 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def spinright():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    if yaw_index < len(power_values) - 1:
        yaw_index += 1
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))

def toggleHoverMode():
    global seqno
    global mode
    global power_values
    global roll_index
    global pitch_index
    global gaz_index
    global yaw_index
    mode = 1 - mode
    for i in xrange(1, 25):
        sendCommand("AT*PCMD=%d,%d,%d,%d,%d,%d\r" % (seqno,mode,
            power_values[roll_index],power_values[pitch_index],power_values[gaz_index],power_values[yaw_index]))


def printUsage():
    print "\n\n"
    print "Keyboard commands:"
    print "\tq       - quit"
    print "\tt       - takeoff"
    print "\tl       - land"
    print "\t(space) - emergency shutoff"
    print "\ta       - fly left"
    print "\tf       - fly right"
    print "\ts       - fly forward"
    print "\td       - fly backward"
    print "\tw       - fly up"
    print "\tx       - fly down"
    print "\tg       - spin left"
    print "\th       - spin right"



print """
NOTE:  This program assumes you are already connected to the
       drone's WiFi network.
"""
    
address = ('192.168.1.1',5556)
seqno = 1
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 5554))

mode = 1 # 0 = hover, 1 = progr. cmd, 3 = progr. cmd w/ auto yaw

# range of power from full power one way to full power another
power_values = [-1082130432, -1086324736, -1090519040, -1098907648, 0, 1048576000, 1056964608, 1061158912, 1065353216]

# initialize indices to point to middle value in power_values
# lengh should be odd since there is symmetry in values around a middle 0
roll_index = len(power_values) / 2
pitch_index = len(power_values) / 2
gaz_index = len(power_values) / 2
yaw_index = len(power_values) / 2

while True:
    printUsage()
    ch = getChar()
    if ch == 'q':
        exit(0)
    elif ch == 't':
        takeoff()
    elif ch == 'l':
        land()
    elif ch == 'a':
        flyleft()
    elif ch == 'f':
        flyright()
    elif ch == 's':
        flyforward()
    elif ch == 'd':
        flybackward()
    elif ch == 'w':
        flyup()
    elif ch == 'x':
        flydown()
    elif ch == 'g':
        spinleft()
    elif ch == 'h':
        spinright()
    elif ch == 'v':
        reset() # we don't want drone to by swerving when untoggling
        toggleHoverMode()
    elif ch == ' ':
        reset() 
        toggleEmergencyMode()
    else:
        print "Invalid command!"
        
    