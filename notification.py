from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)


p = btle.Peripheral("08:6b:d7:e1:93:6e", btle.ADDR_TYPE_PUBLIC) #ca:ed:18:af:35:01
p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID("adb88100-8ade-48c0-bbfd-7dace7160901") 
ch = svc.getCharacteristics()[0]

print(ch.valHandle)

print(f'{p.writeCharacteristic(ch.valHandle, "hello world".encode())}')

while True:
    if p.waitForNotifications():
        # handleNotification() was called
        continue

    print("Waiting...")
    # Perhaps do something else here
