from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name='Home'),
    path('About/', views.About, name='About'),
    path('Result/', views.Result, name='Result'),
]
