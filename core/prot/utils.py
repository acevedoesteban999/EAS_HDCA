from django.db import models
from threading import Thread,Lock,Timer
from abc import ABC, abstractmethod
class BaseObject(ABC):
    object=None
    def __init__(self):
        #print('init')
        self._look=Lock()
        self._thread=Thread(target=self.loop)
        self._active=False
    
    def start(self,id):
        #print('start')
        self.stop()
        if self.set_device(id):
            self._active=True
            self._thread.start()

    def set_device(self,id):
        try:
            self.device=self.object.objects.get(id=id)
        except:
            return False
        return True
    
    def stop(self):
        #print('stop')
        with self._look:
            if self._active:
                self._active=False
        try:
            self._thread.join()
        except:
            pass    
    
    def __del__(self):
        #print('del')
        self.stop()
        
    @abstractmethod
    def loop(self):
        pass

class Main(BaseObject):
    def start(self,id):
        self.stop()
        self._active=True
        self._thread.start()
    
    def loop():
        pass
