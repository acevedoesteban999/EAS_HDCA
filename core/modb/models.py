from django.db import models
from core.prot.models import BasePortocol

# Create your models here.
MODB_TYPE = [
    ("T", "TCP"),
    ("U", "UDP"),
]
class ModBus(BasePortocol):
    ip=models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    type=models.CharField(default='T',max_length=1,choices=MODB_TYPE) 
    coil_motor=models.IntegerField(default=0)
    coil_mode=models.IntegerField(default=0)
    coil_conductor=models.IntegerField(default=0)
    register_valve=models.IntegerField(default=0)
    register_cistern=models.IntegerField(default=0)
    register_tank=models.IntegerField(default=0)
    registers_output=models.IntegerField(default=0)
    register_setpoint=models.IntegerField(default=0)
    
   