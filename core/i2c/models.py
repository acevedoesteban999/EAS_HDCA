from django.db import models
from core.prot.models import BasePortocol
# Create your models here.

class I2C(BasePortocol):
    addr=models.IntegerField()
    
    