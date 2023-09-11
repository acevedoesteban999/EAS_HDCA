from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DetailView,DeleteView,FormView
from core.log.utils import MyLoginRequiredMixin
from core.modb.models import ModBus
from .forms import ModBusForm,ModBusIdent
from django.contrib import messages
from .utils import ModBusObject
from django.http import JsonResponse  
from .utils import ModBusObject
from django.db.models import F,Value,IntegerField
# Create your views here.

class ModBusView(MyLoginRequiredMixin,ListView):
    template_name="list_modbus.html"
    #permission_required="user\.is_development"
    model=ModBus
    # def get_queryset(self):
    #     data=super().get_queryset()
    #     for ob in data.values():
    #         ob.update({'active':ModBusObject.is_active(ob.get('ip'),ob.get('type'))})
    #     print(data.values())            
    #     return data
    def post(self,request, *args, **kwargs):
        if self.is_ajax():
            print(request.POST)
            if request.POST.get('action')=="check_data":
                return JsonResponse({'response':{"active":ModBusObject.is_active(ModBus.objects.get(id=request.POST.get("data")).ip)}},safe=False)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ModBus"
        context["url"]=reverse_lazy("modbus_list")
        # mlist=[]
        # for ob in ModBus.objects.all().values('type','id'):
        #     mlist.append(ModBusObject.is_active(ob.get('id')))
        # context['zlist']=list(zip(context.get('object_list'), mlist))
        context['back_url']=reverse_lazy('prot')
        return context

class ModBusCreate(MyLoginRequiredMixin,CreateView):
    model=ModBus
    form_class=ModBusForm
    #permission_required="user\.is_development"
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
        context['back_url']=reverse_lazy('modbus_list')
        return context
    
class ModBusUpdate(MyLoginRequiredMixin,UpdateView):
    model=ModBus
    #permission_required="user\.is_development"
    template_name="update_modbus.html"
    form_class=ModBusForm   
    
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            #form=self.get_form()
            form.save()
            messages.success(self.request,'Actualizado dispositivo:{}:{}'.format(form.data.get('slug'),form.data.get('ip')))
        else:
            messages.error(request,'Error al Actualizar')
        
        return redirect('modbus_list')
        
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Actualizar Diospositivo ModBus"
        context['url_cancel']=reverse_lazy('modbus_list')
        context['back_url']=reverse_lazy('modbus_list')
        return context
       
class ModBusDevice(MyLoginRequiredMixin,DetailView):
    template_name='device_modbus.html'
    model=ModBus
    #permission_required="user\.is_development"
    modbus_object=None
    
    def user_auth_test(self):
        return self.modbus_object.get_active()
    
    
    def dispatch(self, request, *args, **kwargs):
        self.pk=kwargs.get('pk')
        self.modbus_object=ModBusObject(self.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.is_ajax():
            #print(request.POST)
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
            elif request.POST.get('action')=="get_datas":
                return JsonResponse({'response':self.modbus_object.get_datas()},safe=False)
            
            
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['url']=reverse_lazy('modbus_device',kwargs={'pk':self.pk})
        context['back_url']=reverse_lazy('modbus_list')
        return context
    
class ModBusDelete(MyLoginRequiredMixin,DeleteView):
    model=ModBus
    template_name = 'delete_modbus.html'
    #permission_required="user\.is_development"
    success_url=reverse_lazy('modbus_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Eliminar Dispositivo Modbus"
        context['url_cancel']=reverse_lazy('modbus_list')   
        context['slug']=self.object.slug
        return context
    
class ModBusIden(MyLoginRequiredMixin,FormView):
    template_name="ident_modbus.html"
    #permission_required="user\.is_development"
    form_class=ModBusIdent
    
    def dispatch(self, request, *args, **kwargs):
        self.pk=kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)
    
    # def form_valid(self, form):
    #     form.send_email()
    #     return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = ModBus.objects.get(pk=self.pk)
        context['back_url']=reverse_lazy('modbus_list')
        return context
    
    
    
