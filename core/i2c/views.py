from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from core.log.utils import MyLoginRequiredMixin
from core.i2c.models import I2C
from .forms import I2CForm
from django.contrib import messages
from .utils import I2CThread
from django.http import JsonResponse  
# Create your views here.

class I2CView(MyLoginRequiredMixin,ListView):
    template_name="list_i2c.html"
    permission_required="user.is_development"
    model=I2C
    
    def post(self,request):
        if self.is_ajax():
            if request.POST.get('action')=="scan":
                #return JsonResponse({'response':I2CThread.scan()},safe=False)
                return JsonResponse({'response':[]},safe=False)
        return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "I2C" 
        return context

class I2CCreate(MyLoginRequiredMixin,CreateView):
    model=I2C
    form_class=I2CForm
    permission_required="user.is_development"
    template_name="update_i2c.html"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(self.request,'Creado nuevo dispositivo I2C:{}:{}'.format(form.data.get('slug'),form.data.get('addr')))
        else:
            messages.error(request,'Error al crear')
        return redirect('i2c_list')
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Crear nuevo dispositivo I2C"
        context['url_cancel']=reverse_lazy('i2c_list')
        return context
    
class I2CUpdate(MyLoginRequiredMixin,UpdateView):
    model=I2C
    form_class=I2CForm
    permission_required="user.is_development"
    template_name="update_i2c.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            #form=self.get_form()
            form.save(kwargs.get('pk'))
            messages.success(self.request,'Actualizado dispositivo:{}:{}'.format(form.data.get('slug'),form.data.get('addr')))
        else:
            messages.error(request,'Error al Actualizar')
        
        return redirect('i2c_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Diospositivo I2C"
        context['url_cancel']=reverse_lazy('i2c_list')
        return context