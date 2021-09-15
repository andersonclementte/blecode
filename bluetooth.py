import bluepy
from bluepy.btle import Scanner, DefaultDelegate
from bait import Bait


class BLEControl:
    def __init__(self, target):
        self.target = target
        self.last_scan = None
        self.bait = None
        
    def get_Address_Type(self):
        if self.target.addrType == 'random':
            return bluepy.btle.ADDR_TYPE_RANDOM
        else:
            return bluepy.btle.ADDR_TYPE_PUBLIC

    def get_Address(self):
        return self.target.addr

    def control_connect(self):
       self.target_type = self.get_Address_Type()
       self.target_address = self.get_Address()
       self.bait = Bait(self.target_address, self.target_type)
       self.bait.connect()


    def control_disconnect(self):
        self.bait.disconnect()
        self.bait = None

    def show_Connection(self):
        print(self.bait.is_connected())

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.devices = []

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                self.devices.append(dev)
                print('{} {}'. format(len(self.devices), dev.addr))


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
bait_devices = []

# for dev in devices:
#     print("Device address: %s" % dev.addr)
#     print("Device address type: %s" % dev.addrType)
#     print("Device RSSI: %d dB" % dev.rssi)
#     for (adtype, desc, value) in dev.getScanData():
#         print("Descrição: %s" % desc)
#         print("Valor: %s" % value)
#     print("\n")

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if 'Zephyr' in value:
            bait_devices.append(dev)

# for bait in bait_devices:
#     print("Device address: %s" % dev.addr)
#     print("Device address type: %s" % dev.addrType)
#     print("Device RSSI: %d dB" % dev.rssi)
#     for (adtype, desc, value) in bait.getScanData():
#         print("Descrição: %s" % desc)
#         print("Valor: %s" % value)
#     print("\n")

shell = BLEControl(bait_devices[0])
shell.control_connect()
shell.show_Connection()
shell.control_disconnect()
shell.show_Connection()#
