from django.urls import path,include
from .views import ProtocolView

urlpatterns = [
    path('prot/',ProtocolView.as_view(),name='prot'),
    path('i2c/',include('core.i2c.urls')),
    path('modb/',include('core.modb.urls')),
]
