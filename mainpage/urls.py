from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send', views.send, name='send'),
    path('reset', views.reset, name='reset'),
    path('random_menu', views.random_menu, name='random_menu'),
    path('send_os_info', views.send_os_info, name='send_os_info'),
    path('k_menu', views.k_menu, name='k_menu'),

]