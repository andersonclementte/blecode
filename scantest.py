from bluepy.btle import Scanner, DefaultDelegate

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


for dev in devices:
    # print ("Device address: %s | Device Type (%s)" % (dev.addr, dev.addrType))
    # for (adtype, desc, value) in dev.getScanData():
    #     print ("Description:(%s):\nValue: %s" % (desc, value))
    # print("\n")
    # for dev in devices:
    print("Device address: %s" % dev.addr)
    print("Device address type: %s" % dev.addrType)
    print("Device RSSI: %d dB" % dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print("Descrição: %s" % desc)
        print("Valor: %s" % value)
    print("\n")

