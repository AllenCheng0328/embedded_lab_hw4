from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate (DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery (self, dev, isNewDev , isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr
    def handleNotification(self, cHandle, data):
        if data == "\x00":
            print "button:released"
        elif data == "\x01":
            print "button:pressed"
        #data = list(data)
        #print data
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
for dev in devices:
    print "%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr ,dev.addrType , dev.rssi)
    n += 1
    for (adtype , desc , value) in dev.getScanData():
        print " %s = %s" % (desc ,value)
number = input('Enter your device number: ')
print('Device', number)
print(devices[number].addr)
print "Connecting..."
dev = Peripheral(devices[number].addr , 'random')
dev.setDelegate(ScanDelegate())

print "Services..."
for svc in dev.services:
    print str(svc)
try:
    '''for ch in testService.getCharacteristics():
        print str(ch)
    ch = dev.getCharacteristics(uuid=UUID(0xA001))[0]
    dev.writeCharacteristic(ch.valHandle+1, b"\x01\x00")'''
    testService = dev.getServiceByUUID(UUID(0xA000))
    testService1 = dev.getServiceByUUID(UUID(0xB000))
    testService2 = dev.getServiceByUUID(UUID(0xC000))

    for ch in testService.getCharacteristics():
        print str(ch)
    ch = dev.getCharacteristics(uuid=UUID(0xA001))[0]
    dev.writeCharacteristic(ch.valHandle+1, b"\x01\x00")

    for ch1 in testService1.getCharacteristics():
        print str(ch1)
    ch1 = dev.getCharacteristics(uuid=UUID(0xB001))[0]
    if (ch1.supportsRead()):
        print "studentID:", ch1.read()
    
    for ch2 in testService2.getCharacteristics():
        print str(ch2)
    ch2 = dev.getCharacteristics(uuid=UUID(0xC001))[0]
    hand = ch2.getHandle()
    dev.writeCharacteristic(ch2.valHandle+1, b"\x01\x00")


    while True:
        dev.writeCharacteristic(hand, bytes(1))
        time.sleep(0.3)
        dev.writeCharacteristic(hand, bytes(0))
        time.sleep(0.3)
        dev.waitForNotifications(0.5)

finally:
    dev.disconnect()