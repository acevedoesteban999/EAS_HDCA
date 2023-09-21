from core.prot.utils import BaseObject
from .models import ModBus
import time
import random
import struct
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
class ModBusObject():
    object=None
    client=None
    
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
        client=ModbusTcpClient(str(ip))
        try:
            _bool= client.connect()
            client.close()
            return _bool
        except:
            return False      

    async def write_coil(self,coil,value):
        self.client.connect()
        self.client.write_coil(coil,value)
        time.sleep(1)
        self.client.close()
            
    async def read_coil(self,coil):
        try:
            self.client.connect()
            coil=self.client.read_coils(coil)
            #time.sleep(1)
            self.client.close()
            return coil.bits[0]
        except:
            time.sleep(2)
            self.client.connect()
            coil=self.client.read_coils(coil)
            #time.sleep(1)
            self.client.close()
            return coil.bits[0]
            #return None
    async def read_register(self,register):
        try:
            self.client.connect()
            _register=self.client.read_holding_registers(register)
            self.client.close()
            #time.sleep(1)
            return int(_register.registers[0])  
        except:
            time.sleep(2)
            self.client.connect()
            _register=self.client.read_holding_registers(register)
            self.client.close()
            #time.sleep(1)
            return int(_register.registers[0])  
            #return None
    async def write_register(self,register,value):
        self.client.connect()
        self.client.write_register(register,value)
        time.sleep(1)
        self.client.close()
    async def write_registers(self,register,value):
            self.client.connect()
            # Convert the float value to a binary representation
            binary_data = struct.pack('!f', value)
            # Extract the two unsigned integers from the binary representation
            uint1, uint2 = struct.unpack('!HH', binary_data)
            self.client.write_registers(register,[uint1,uint2])
            time.sleep(1)
            self.client.close()
            
    async def read_registers(self,register):
        try:
            self.client.connect()
            _register=self.client.read_holding_registers(register,2)
            self.client.close()
            combined_uint = (_register.registers[0] << 16) | (_register.registers[1] & 0xFFFF)
            float_value = struct.unpack('!f', struct.pack('!I', combined_uint))[0]
            return float_value
        except:
            time.sleep(2)
            self.client.connect()
            _register=self.client.read_holding_registers(register,2)
            self.client.close()
            combined_uint = (_register.registers[0] << 16) | (_register.registers[1] & 0xFFFF)
            float_value = struct.unpack('!f', struct.pack('!I', combined_uint))[0]
            return float_value
            #return None
    def set_mode(self,data):
        asyncio.run(self.write_coil(self.object.coil_mode,False if data=='false' else True))
        return self.get_mode()
        
    def set_motor(self,data):
        if self.get_mode() == False:
            if data=='true':
                asyncio.run(self.write_coil(self.object.coil_motor,True))
            else:
                asyncio.run(self.write_coil(self.object.coil_motor,False))
        return self.get_motor()
    
    def set_valve(self,data):
        if self.get_mode() == False:
            asyncio.run(self.write_register(self.object.register_valve,int(data)))
        return self.get_valve()
    
    def set_setpoint(self,data):
        asyncio.run(self.write_registers(self.object.register_setpoint,int(data)))
        return self.get_setpoint()
    
    def get_motor(self):
        
        return asyncio.run(self.read_coil(self.object.coil_motor))
        
    def get_valve(self):
        return asyncio.run(self.read_register(self.object.register_valve))
    
    def get_mode(self):
        return asyncio.run(self.read_coil(self.object.coil_mode))
        
    def get_setpoint(self):
        return asyncio.run(self.read_registers(self.object.register_setpoint))
        
    def get_conduct(self):
        return asyncio.run(self.read_coil(self.object.coil_conductor))
        
    def get_tank(self):
        return asyncio.run(self.read_registers(self.object.register_tank))
        
    def get_cistern(self):
        return asyncio.run(self.read_registers(self.object.register_cistern))
        
    def get_output(self):
        return asyncio.run(self.read_registers(self.object.registers_output))
        
    def get_data(self):
        return {
            'NT':self.get_tank(),
            'NC':self.get_cistern(),
            'SP':self.get_setpoint(),
            'motor':self.get_motor(),
            'valve':self.get_valve(),
            'conduct':self.get_conduct(),
            }
    def get_data1(self):
        return {
            'AC':self.get_output(),
            'V':self.get_valve(),
            }
    
    def get_datas(self,count=10):
        if count==0:
            return None
        try:
            return {
                'mode':self.get_mode(),
                'motor':self.get_motor(),
                'valve':self.get_valve(),
                'setpoint':self.get_setpoint(),
                }
        except:
            time.sleep(1)
            return self.get_datas(count-1)
    
   

