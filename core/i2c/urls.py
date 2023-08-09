from django.urls import path
from .views import I2CView,I2CCreate,I2CUpdate

urlpatterns = [
    path('',I2CView.as_view(),name='i2c_list'),
    path('create/',I2CCreate.as_view(),name='i2c_create'),
    path('update/<int:pk>/',I2CUpdate.as_view(),name='i2c_update'),

]
