from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.devices = []

    # def handleNotification(self, cHandle, data):
    #     print("A notification was received: %s" %data)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        print('called')
        if isNewDev:
            self.devices.append(dev)
            dev_name = dev.getValueText(9).split('\x00')[0]
            print('{: <5} {: <30} {: <12}'.format(len(self.devices), dev_name, dev.addr))

    def handleNotification(self, cHandle, data):
        print(f'Handle {cHandle} recebeu o dado: {data.decode()}')


p = btle.Peripheral("08:6b:d7:e1:93:5a", btle.ADDR_TYPE_PUBLIC) #ca:ed:18:af:35:01 
p.setDelegate(MyDelegate())
print('conectado')
# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID("00000000-1000-2000-3000-111122223333") 
ch = svc.getCharacteristics()
# n funcionou ch = p.getCharacteristics("4ffa859d-6bc8-4490-8379-0a292d9c7bd3")
print(*ch, sep = "\n")
print(ch[12].valHandle)
p.writeCharacteristic(ch.valHandle, "0x01".encode())
#print(f'{p.writeCharacteristic(ch.valHandle, "0x01".encode())}')

while True:
    if p.waitForNotifications(1):
        # handleNotification() was called
        continue

    print("Waiting...")
    # Perhaps do something else here
