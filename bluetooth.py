import bluepy
#from bluepy import btle
# import numpy as np
from bluepy.btle import Scanner, DefaultDelegate
from bait import Bait


class BLEControl:
    def __init__(self, target):
        self.target = target
        self.last_scan = None
        self.bait = None
        
    def get_address_type(self):
        if self.target.addrType == 'random':
            return bluepy.btle.ADDR_TYPE_RANDOM
        else:
            return bluepy.btle.ADDR_TYPE_PUBLIC

    def get_address(self):
        return self.target.addr

    def control_connect(self):
       self.target_type = self.get_address_type()
       self.target_address = self.get_address()
       self.bait = Bait(self.target_address, self.target_type)
       self.bait.connect()


    def control_disconnect(self):
        self.bait.disconnect()
        self.bait = None

    def show_Connection(self):
        print(self.bait.is_connected())

    def control_services(self):
        services = self.bait.list_services()
        for service in services:
            print(service.uuid)
            print(service.peripheral)
            print("fim do serviço")
            print('\n')

    def print_characteristichandle(self, handle):
        print(self.bait.characteristic_handle(handle))

    def control_characteristics(self):
        self.characteristics = self.bait.list_characteristics()


        for characteristic in self.characteristics:
            #leitura funciona com falhas
            if characteristic.supportsRead():
                print(f'Leitura: {characteristic.read()}')
                # self.print_characteristichandle(characteristic.getHandle())
            
            print(f'Handle: {characteristic.getHandle()}')
            print(f'UUID Descrição: {characteristic.uuid.getCommonName()}')
            print(f'UUID: {characteristic.uuid}')
            print(f'Periferico: {characteristic.peripheral}')
            print(f'Bitmask da propriedade: {characteristic.properties}')
            print(f'Propriedades de caracteristica: {characteristic.propertiesToString()}')
            print("Fim de caracteristica")
            print("\n")

    def control_descriptors(self):
        print(self.bait.list_descriptors())

    def write_characteristic(self):
        # uuid = btle.UUID("00002a00-0000-1000-8000-00805f9b34fb")
        self.characteristics = self.bait.list_characteristics()
        #print(*self.characteristics, sep = "\n")
        #print(self.characteristics[3])
        to_write = self.characteristics[3]
        to_write.write('hello world'.encode())
        # print(f'Leitura: {self.characteristics[3].read()}')
        #print(self.characteristics[3].read())
        print("Escrita ok\n")
        

##Class to handle scanning
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.devices = []

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                self.devices.append(dev)
                print('{} {}'. format(len(self.devices), dev.addr))


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0) #lists devices
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
#shell.show_Connection()
#shell.control_disconnect()
#shell.show_Connection()#
#shell.control_services() ##listando serviços como objeto, ok
#shell.control_characteristics()
#shell.control_descriptors()
# shell.print_characteristichandle()
shell.write_characteristic()

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0) #lists devices

for dev in devices:
    print("Device address: %s" % dev.addr)
    print("Device address type: %s" % dev.addrType)
    print("Device RSSI: %d dB" % dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print("Descrição: %s" % desc)
        print("Valor: %s" % value)
    print("\n")