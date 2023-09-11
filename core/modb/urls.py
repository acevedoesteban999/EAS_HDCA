from django.urls import path,include
from .views import ModBusView,ModBusCreate,ModBusUpdate,ModBusDevice,ModBusDelete,ModBusIden

urlpatterns = [
    path('',ModBusView.as_view(),name='modbus_list'),
    path('create/',ModBusCreate.as_view(),name='modbus_create'),
    path('update/<int:pk>/',ModBusUpdate.as_view(),name='modbus_update'),
    path('ident/<int:pk>/',ModBusIden.as_view(),name='modbus_iden'),
    path('device/<int:pk>/',ModBusDevice.as_view(),name='modbus_device'),
    path('delete/<int:pk>/',ModBusDelete.as_view(),name='modbus_delete'),
]
