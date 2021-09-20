import bluepy.btle

class Bait:
    def __init__(self, mac_address, address_type):
        self.mac_address = mac_address
        self._addr_type = address_type
        self.connection = None

    def connect(self):
        try:
            self.connection = bluepy.btle.Peripheral(self.mac_address, self._addr_type,0)
        except:
            print("Falha de conexão\n")
            return False
        print("Conectado\n")
        return True

    def disconnect(self):
        self.connection.disconnect()
        print("Desconectado")
        self.connection = None
    
    def is_connected(self):
        return self.connection

    def list_services(self):
        self.services = self.connection.getServices()
        return self.services

    def list_characteristics(self):
        self.characteristics = self.connection.getCharacteristics()
        return self.characteristics

    def list_descriptors(self):
        self.descriptors = self.connection.getDescriptors()
        return self.descriptors

    def characteristic_handle(self, handle):
        return self.connection.readCharacteristic(handle)

    def get_service_by_uuid(self, uuid):
        return self.connection.getServiceByUUID(uuid)