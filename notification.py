from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)


p = btle.Peripheral("ca:ed:18:af:35:01", btle.ADDR_TYPE_RANDOM) #ca:ed:18:af:35:01
p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID("0000180d-0000-1000-8000-00805f9b34fb") #Heart Rate 0000180d-0000-1000-8000-00805f9b34fb
ch = svc.getCharacteristics()[0]

print(ch.valHandle)

# p.writeCharacteristic(ch.valHandle, "\x02\x00\x05\x1e\x0c-\x1e\x01\x00\x01".encode())

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print("Waiting...")
    # Perhaps do something else here
