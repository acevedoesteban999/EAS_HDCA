from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DetailView
from core.log.utils import MyLoginRequiredMixin
from core.modb.models import ModBus
from .forms import ModBusForm
from django.contrib import messages
from .utils import ModBusThread
from django.http import JsonResponse  
from .utils import ModBusThread
from django.db.models import F,Value,IntegerField
# Create your views here.

class ModBusView(MyLoginRequiredMixin,ListView):
    template_name="list_modbus.html"
    permission_required="user.is_development"
    model=ModBus
    # def get_queryset(self):
    #     data=super().get_queryset()
    #     for ob in data.values():
    #         ob.update({'active':ModBusThread.is_active(ob.get('ip'),ob.get('type'))})
    #     print(data.values())            
    #     return data
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ModBus"
        mlist=[]
        for ob in ModBus.objects.all().values('type','id'):
            mlist.append(ModBusThread.is_active(ob.get('id'),ob.get('type')))
        context['zlist']=list(zip(context.get('object_list'), mlist))
        return context

class ModBusCreate(MyLoginRequiredMixin,CreateView):
    model=ModBus
    form_class=ModBusForm
    permission_required="user.is_development"
    template_name="update_modbus.html"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(self.request,'Creado nuevo dispositivo ModBus:{}:{}'.format(form.data.get('slug'),form.data.get('ip')))
        else:
            messages.error(request,'Error al crear')
        return redirect('modbus_list')
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Crear nuevo dispositivo ModBus"
        context['url_cancel']=reverse_lazy('modbus_list')
        return context
    
class ModBusUpdate(MyLoginRequiredMixin,UpdateView):
    model=ModBus
    permission_required="user.is_development"
    template_name="update_modbus.html"
    form_class=ModBusForm   
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            #form=self.get_form()
            form.save(kwargs.get('pk'))
            messages.success(self.request,'Actualizado dispositivo:{}:{}'.format(form.data.get('slug'),form.data.get('ip')))
        else:
            messages.error(request,'Error al Actualizar')
        
        return redirect('modbus_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Diospositivo ModBus"
        context['url_cancel']=reverse_lazy('modbus_list')
        return context
    
    
class ModBusDevice(MyLoginRequiredMixin,DetailView):
    template_name='device_modbus.html'
    model=ModBus
    permission_required="user.is_development"
    modbus_object=ModBusThread()
    
    def user_auth_test(self):
        return self.modbus_object.get_active()
    
    
    def dispatch(self, request, *args, **kwargs):
        self.pk=kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.is_ajax():
            if request.POST.get('action')=="data":
                return JsonResponse({'response':self.modbus_object.get_data()},safe=False)
            elif request.POST.get('action')=="mode":
                return JsonResponse({'response':self.modbus_object.set_mode(request.POST.get('data'))},safe=False)
            elif request.POST.get('action')=="setpoint":
                return JsonResponse({'response':self.modbus_object.set_setpoint(request.POST.get('data'))},safe=False)
            elif request.POST.get('action')=="motor":
                return JsonResponse({'response':self.modbus_object.set_motor(request.POST.get('data'))},safe=False)
            elif request.POST.get('action')=="valve":
                return JsonResponse({'response':self.modbus_object.set_valve(request.POST.get('data'))},safe=False)
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['url']=reverse_lazy('modbus_device',kwargs={'pk':self.pk})
        return context