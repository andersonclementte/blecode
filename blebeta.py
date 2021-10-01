import bluepy, time, cmd, sys
from bluepy.btle import Scanner, DefaultDelegate
from bait import Bait

class BLEShell(cmd.Cmd):
    def __init__(self):
        super().__init__()
        #self.target = target
        self.last_scan = None
        self.bait = None
        self.services = None
        self.characteristics = None

    def get_characteristics(self):
        if self.characteristics == None:
            self.characteristics = self.bait.list_characteristics()
    
    def do_list(self, args): #implementar sistema de filtro
        scanner = Scanner().withDelegate(ScanDelegate())
        print('{: <5} {: <30} {: <12}'.format('ID', 'Name', 'Mac address'))
        print('{: <5} {: <30} {: <12}'.format('--', '----', '-----------'))
        self.last_scan = scanner.scan(1.0)
        for (i, dev) in enumerate(self.last_scan, start=1):
            # for (adtype, desc, value) in dev.getScanData():
            #     print('{: <5} {: <30} {: <12}'.format(i, value, dev.addr))
            # print("suposto nome: ", dev.getValueText(8))
            name = dev.getValueText(8)
            if name == None:
                print('{: <5} {: <30} {: <12}'.format(i, 'Void', dev.addr))
            else:
                print('{: <5} {: <30} {: <12}'.format(i, name, dev.addr))
            #print('\n')

        ''''Abaixo para testes'''
        # for dev in self.last_scan:
        #     # print ("Device address: %s | Device Type (%s)" % (dev.addr, dev.addrType))
        #     # for (adtype, desc, value) in dev.getScanData():
        #     #     print ("Description:(%s):\nValue: %s" % (desc, value))
        #     # print("\n")
        #     # for dev in devices:
        #     print("Device address: %s" % dev.addr)
        #     print("Device address type: %s" % dev.addrType)
        #     print("Device RSSI: %d dB" % dev.rssi)
        #     for (adtype, desc, value) in dev.getScanData():
        #         print("Descrição: %s" % desc)
        #         print("Valor: %s" % value)
        #     print("\n")


        


    def do_connect(self, args):
        if str.isdigit(args) and self.last_scan:
            dev_id = int(args) - 1

            # print(type(self.last_scan))
            # print(dir(list(self.last_scan)[dev_id]))
            # print('aaa', list(self.last_scan)[dev_id].getValueText(8))
            # print('aaa', list(self.last_scan)[dev_id].addrType)
            
            try:
                mac_address = list(self.last_scan)[dev_id].addr
                addr_type = list(self.last_scan)[dev_id].addrType
                self.bait = Bait(mac_address, addr_type)
                self.bait.connect()
            except Exception as e:
                print(e)

            # mac_address = list(self.last_scan)[dev_id].addr
            # addr_type = list(self.last_scan)[dev_id].addrType
            # self.bait = Bait(mac_address, addr_type)
            # self.bait.connect()
            # print('ok')
            # try:
            #     dev_id = int(args)
            #     mac_address = self.last_scan[dev_id].addr
            #     addr_type = self.last_scan[dev_id].addrType
            #     self.bait = Bait(mac_address, addr_type)
            #     self.bait.connect()
            #     print('ok')
            # except Exception:
            #     print("ID inválido")
            #     return False
        
        else:
            print('ID inválida ou lista vazia')

    def do_disconnect(self, args):
        self.bait.disconnect()
        self.bait = None

    def do_show_connection(self, args):
        if self.bait:
            return print(self.bait.is_connected())
        else:
            print("Desconectado")

    def do_services(self, args):
        self.services = self.bait.list_services()
        # print('{: <15} {: <15}'.format('Serviço', 'UUID'))
        for service in self.services:
            # print('{: <15} {: <15}'.format(service, service.uuid))
            print(service)
            print(service.uuid)
            # print(service.peripheral)
            print("fim do serviço")
            print('\n')

    def do_describe(self, args):
        self.characteristics = self.bait.list_characteristics()
        for characteristic in self.characteristics:
            # if characteristic.supportsRead():
            #     '''Algumas caracteristicas são desonhecidas e a conexão é perdida;
            #         exemplo: handle 41 da placa nrf suporta leitura, escrita e indicação mas desconecta'''
            #     print(f'Leitura: {characteristic.read()}')
            #     print('suporta leitura')    
            # print(f'Handle: {characteristic.getHandle()}')
            # print(f'UUID Descrição: {characteristic.uuid.getCommonName()}')
            # print(f'UUID: {characteristic.uuid}')
            # print(f'Bitmask da propriedade: {characteristic.properties}')
            # print(f'Propriedades de caracteristica: {characteristic.propertiesToString()}')
            # print("Fim de caracteristica")
            #print(dir(characteristic))
            print("---------------------------")
            print('descs ', characteristic.descs)
            print('valHandle ',characteristic.valHandle)
            print('descriptors ', characteristic.getDescriptors())
            print('props ',characteristic.props)
            print('propNames', characteristic.propNames)
            print('----------------------')
            print("\n")

    def do_read(self, args): ##Tratar caso de erro handle errado e handle faltando
        if args != None:
            self.bait.readChar(int(args))
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
    
    def do_notify(self, args):
        pass

    def do_quit(self, args):
        print ("Quitting.")
        raise SystemExit

class ScanDelegate(DefaultDelegate):
    def __init__(self): ##implementar output de filtro
        #DefaultDelegate.__init__(self)
        super().__init__()
        self.devices = []

        def handleDiscovery(self, dev, isNewDev, isNewData):
            print('called')
            if isNewDev:
                self.devices.append(dev)
                dev_name = dev.getValueText(9).split('\x00')[0]
                print('{: <5} {: <30} {: <12}'.format(len(self.devices), dev_name, dev.addr))

        def handleNotification(self, cHandle, data):
            print(f'Handle {cHandle} recebeu o dado: {data}')


if __name__ == '__main__':
    prompt = BLEShell()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')