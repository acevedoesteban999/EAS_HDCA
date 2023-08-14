from core.prot.utils import BaseThread
from .models import ModBus
import time
import random

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
class ModBusThread(BaseThread):
    object=ModBus
    mode=False
    motor=False
    valve=0
    setpoint=0
    def __init__(self) -> None:
        super().__init__()
        
    def get_active(self):    
        return True
        return self.is_active(self.object.ip,self.object.type)
    @staticmethod
    def is_active(ip,type):
        if random.randint(1,2)==1:
            return True
        return False        
    
    def set_mode(self,data):
        if data=='true':
            self.mode=True
        else:
            self.mode=False
        return self.mode
    
    def set_motor(self,data):
        if self.mode == False:
            if data=='true':
                self.motor=False
            else:
                self.motor=True
        return self.motor
    
    def set_valve(self,data):
        print(self.mode)
        if self.mode == False:
            self.valve=data
        return self.valve
     
    def set_setpoint(self,setpoint):
        self.setpoint=setpoint
        return self.setpoint
        
    def get_data(self):
        return {
            'NT':random.randint(0,100),
            'NC':random.randint(0,100),
            'AC':random.randint(0,100),
            }
    
    def loop(self):
        while True:
            with self._look:
                if self._active==False:
                    break
                
            print("loop")
            time.sleep(1) 


