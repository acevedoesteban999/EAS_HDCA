from core.prot.utils import BaseObject
from .models import ModBus
import time
import random
from pymodbus.client import ModbusTcpClient,ModbusUdpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder,BinaryPayloadDecoder
import asyncio
"""
from pymodbus.client import ModbusTcpClient
import asyncio
#import pymodbus

#pymodbus.register_write_message()
async def run():
    
    client=ModbusTcpClient("192.168.0.102")
  
    client.connect()
    print(client.read_coils(100,1))
    client.write_coil(110,True)
    print(client.read_coils(100,1))
    client.close()
  
    #print('OK',result.registers)
asyncio.run(run())
"""
class ModBusObject(BaseObject):
    object=None
    client=None
    mode=False
    motor=False
    valve=0
    setpoint=0
    
    def __init__(self,pk) -> None:
        self.object=ModBus.objects.get(pk=pk)
        if self.object.type=="T":
            self.client=ModbusTcpClient(str(self.object.ip))
        else:
            self.client=ModbusUdpClient(str(self.object.ip))

        super().__init__()
        
    def get_active(self):    
        #return True
        return self.is_active(self.object.ip)
    
    @staticmethod
    def is_active(ip):
        return True
        client=ModbusTcpClient(str(ip))
        try:
            return client.connect()
            client.close()
            return True
        except:
            return False
        #if random.randint(1,2)==1:
        #    return True
        #return False
        return True        

    async def write_coil(self,coil,value):
        self.client.connect()
        self.client.write_coil(coil,value)
        self.client.close()
    
    async def read_coil(self,coil):
        self.client.connect()
        self.client.read_coils(coil,1)
        self.client.close()
        
    async def read_register(self,register):
        self.client.connect()
        self.client.read_input_registers(register,1)
        self.client.close()
    
    async def write_register(self,register,value):
        self.client.connect()
        self.client.write_register(register,value)
        self.client.close()
        
    async def write_registers(self,register,value):
        self.client.connect()
        builder=BinaryPayloadBuilder(byteorder=Endian.BIG,wordorder=Endian.Big)
        builder.add_32bit_float(value)
        pyload=builder.build()
        self.client.write_registers(register,pyload,skip_encode=True)
        #self.client.write_register(register,value)
        self.client.close()
    
    def set_mode(self,data):
        if data=='true':
            pass
            #self.mode=True
        else:
            pass
            #self.mode=False
        return self.get_mode()
    
    def get_mode(self):
        return False
        return self.mode
    
    def set_motor(self,data):
        if self.mode == False:
            if data=='true':
                pass
                #asyncio.run(self.write_coil(self.object.coil_motor,False))
            else:
                pass
                #asyncio.run(self.write_coil(self.object.coil_motor,True))
        return self.get_motor()
    
    def get_motor(self):
        pass
        return False 
    
    def set_valve(self,data):
        if self.mode == False:
            pass
            #asyncio.run(self.write_register(self.object.coil_valve,int(data)))
        return self.get_valve()
    
    def get_valve(self):
        return random.randint(0,100)
    
    def set_setpoint(self,setpoint):
        return self.get_setpoint()
    
    def get_setpoint(self):
        return random.randint(0,100)
         
    def get_data(self):
        return {
            'NT':random.randint(0,100),
            'NC':random.randint(0,100),
            'AC':random.randint(0,100),
            'motor':random.randint(0,1),
            'valve':random.randint(0,1),
            'contin':random.randint(0,1),
            }
    
    def get_datas(self):
        return {
            'mode':self.get_mode(),
            'motor':self.get_motor(),
            'valve':self.get_valve(),
            'setpoint':self.get_setpoint(),
            }
    
    def loop(self):
        pass
        # while True:
        #     with self._look:
        #         if self._active==False:
        #             break
                
        #     print("loop")
        #     time.sleep(1) 


