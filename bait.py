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
            print("Falha de conexão")
            return False
        return True

    def disconnect(self):
        self.connection.disconnect()
    
    def is_connected(self):
        return self.connection