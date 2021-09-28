import bluepy, time, cmd, sys
from bluepy.btle import Scanner, DefaultDelegate
from bait import Bait

class BLEShell(cmd.Cmd):
    def __init__(self):
        
        super(BLEShell, self).__init__()
        #self.target = target
        self.last_scan = None
        self.bait = None
        self.services = None
        self.characteristics = None

    def get_characteristics(self):
        if self.characteristics == None:
            self.characteristics = self.bait.list_characteristics()
    
    def do_list(self, args):
        self.last_scan = ScanDelegate()
        scanner = Scanner().withDelegate(self.last_scan)
        print('{: <5} {: <30} {: <12}'.format('ID', 'Name', 'Mac address'))
        print('{: <5} {: <30} {: <12}'.format('--', '----', '-----------'))
        scanner.scan(10.0)

    def do_connect(self, args):
        if str.isdigit(args) and self.last_scan:
            try:
                dev_id = int(args)
                mac_address = self.last_scan[dev_id].addr
                addr_type = self.last_scan[dev_id].addrType
                self.bait = Bait(mac_address, addr_type)
                self.bait.connect()
            except Exception:
                print("ID inválido")
                return False

    def do_disconnect(self, args):
        self.bait.disconnect()
        self.bait = None

    def do_show_connection(self, args):
        print(self.bait.is_connected())

    def do_services(self, args):
        if self.services is None:
            self.services = self.bait.list_services()
        print('{: <15} {: <15}'.format('Serviço', 'UUID'))
        if self.services != None:
            for service in self.services:
                print('{: <15} {: <15}'.format(service, service.uuid))

    def do_characteristics(self, args):
        if self.characteristics is None:
            self.characteristics = self.bait.list_characteristics()
        
        if self.characteristics != None:

            for characteristic in self.characteristics:
                if characteristic.supportsRead():
                    print(f'Leitura: {characteristic.read()}')
                print(f'Handle: {characteristic.getHandle()}')
                print(f'UUID Descrição: {characteristic.uuid.getCommonName()}')
                print(f'UUID: {characteristic.uuid}')
                print(f'Bitmask da propriedade: {characteristic.properties}')
                print(f'Propriedades de caracteristica: {characteristic.propertiesToString()}')
                print("Fim de caracteristica")
                print("\n")

    def do_read(self, args): ##Tratar caso de erro handle errado e handle faltando
        if args != None:
            self.bait.readChar(args)
        else:
            print("Bad Handle")

    def do_write(self, args): ##Tratar caso de erro handle errado e handle faltando
        if args != None:
            value = input('Digite o valor: ')
            self.bait.writeChar(int(args), value.encode())
            print("Enviando...")
            time.sleep(5)
            print("Enviado") #implementar waitfornotification
            time.sleep(5)
        else:
            print("Bad Handle")

    def do_quit(self, args):
        print ("Quitting.")
        raise SystemExit

class ScanDelegate(DefaultDelegate):
    def __init__(self): ##rever args
        DefaultDelegate.__init__(self)
        self.devices = []

        def handleDiscovery(self, dev, isNewDev, isNewData):
            if isNewDev:
                self.devices.append(dev)
                dev_name = dev.getValueText(9).split('\x00')[0]
                print('{: <5} {: <30} {: <12}'.format(len(self.devices), dev_name, dev.addr))

        def handlenotification(self, cHandle, data):
            print(f'Handle {cHandle} recebeu o dado: {data.decode()}')


if __name__ == '__main__':
    prompt = BLEShell()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')