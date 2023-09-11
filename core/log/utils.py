from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
from django.urls import reverse_lazy
#last_url=None
class MyLoginRequiredMixin(LoginRequiredMixin,PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    permission_required=None
    permission_denied_message="Permisos insuficientes para acceder a esta zona"
    
    def user_auth_test(self) -> bool:
        """A test that is needed (although not sufficient) to authorized the user
        to perform the view's action"""
        return True
    
    def dispatch(self, request, *args, **kwargs):
        #self.last_url=request.get_full_path()
        if not self.user_auth_test():
            return self.handle_no_permission()
        return super().dispatch(request,args,kwargs)
    
    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
    
    def has_permission(self) -> bool:
        if self.permission_required==None:
            return True

        return super().has_permission()
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     global last_url
    #     context['back_url']=last_url
    #     last_url=self.last_url
    #     return context   