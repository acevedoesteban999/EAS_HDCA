from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.log.utils import MyLoginRequiredMixin
from core.modb.models import ModBus
from  core.i2c.models import I2C
# Create your views here.


class ProtocolView(MyLoginRequiredMixin,TemplateView):
    template_name="protocols.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocols"] =[
            {
                "count":ModBus.objects.all().count(),
                'url': reverse_lazy('modbus_list'),
                'text':"ModBus",
                'color':'info',
            },
            {
                "count":I2C.objects.all().count(),
                'url': reverse_lazy('i2c_list'),
                'text':"I2C",
                'color':'success',
            },
            ]
            
        return context
    