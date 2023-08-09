# from ..utils import Base
# from ..models import UARTProtocol
# import time

# class UART(Base):
#     object=UARTProtocol
    
#     def __init__(self,id) -> None:
#         super().__init__()
#         self.device=None
        
#     def loop(self):
#         while True:
#             with self._look:
#                 if self._active==False:
#                     break
                
#             print("loop")
#             time.sleep(1) 
            
# _UART=UART()