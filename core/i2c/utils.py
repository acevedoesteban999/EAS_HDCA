from core.prot.utils import BaseObject
from .models import I2C
import time
#from smbus2 import SMBus

class I2CThread(BaseObject):
    object=I2C
    def __init__(self) -> None:
        super().__init__()
        
    @staticmethod
    def scan():
        data=[]
        for i in range(128):
            try:
                #SMBus(1).write_byte(i,7)
                data.append(i)
            except:
                pass
        return data
    
    def loop(self):
        while True:
            with self._look:
                if self._active==False:
                    break
                
            print("loop")
            time.sleep(1) 


