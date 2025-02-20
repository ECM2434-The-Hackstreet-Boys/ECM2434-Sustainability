
# garden/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_garden_page, name='garden'),
    path('admin/', views.get_admin_page, name='admin'),
    path('save_garden/', views.save_garden, name='save_garden'),
    path('load_garden/', views.load_garden, name='load_garden'),
]

