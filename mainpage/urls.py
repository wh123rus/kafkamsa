from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send', views.send_info, name='send_info'),
    path('random_menu', views.random_menu, name='random_menu'),
    path('k_menu', views.k_menu, name='k_menu'),

]