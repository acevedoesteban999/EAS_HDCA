# from ..utils import Base
# from ..models import I2CProtocol
# import time

# class I2C(Base):
#     object=I2CProtocol
#     def __init__(self) -> None:
#         super().__init__()
#         self.__devices=I2CProtocol.objects.all()
        
#     def loop(self):
#         while True:
#             with self._look:
#                 if self._active==False:
#                     break
                
#             print("loop")
#             time.sleep(1) 
            
# _I2C=I2C()
