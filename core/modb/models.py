from django.db import models
from core.prot.models import BasePortocol

# Create your models here.
MODB_TYPE = [
    ("T", "TCP"),
    ("U", "UDP"),
]
class ModBus(BasePortocol):
    ip=models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    type=models.CharField(verbose_name="Tipo",default='T',max_length=1,choices=MODB_TYPE) 
    coil_motor=models.IntegerField(verbose_name="Motor",default=0)
    coil_mode=models.IntegerField(verbose_name="Modo",default=0)
    coil_conductor=models.IntegerField(verbose_name="Conductividad",default=0)
    register_valve=models.IntegerField(verbose_name="Valvúla",default=0)
    register_cistern=models.IntegerField(verbose_name="Cisterna",default=0)
    register_tank=models.IntegerField(verbose_name="Tanque",default=0)
    registers_output=models.IntegerField(verbose_name="Cotrol",default=0)
    register_setpoint=models.IntegerField(verbose_name="SetPoint",default=0)
    
   