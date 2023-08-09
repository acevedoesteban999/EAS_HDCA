from django.shortcuts import render
from django.views.generic import TemplateView
from core.log.utils import MyLoginRequiredMixin


# Create your views here.


class HomeView(MyLoginRequiredMixin,TemplateView):
    template_name='home.html'
    
        