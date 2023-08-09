from django.db import models


class BasePortocol(models.Model):
    slug=models.SlugField(max_length=25)    
    def __str__(self) -> str:
        return self.slug
# Create your models here.
