"""
URLs for the garden page
garden/urls.py

@Author: Edward Pratt
"""
from django.urls import path
from . import views

# URL patterns for the garden app /garden/
urlpatterns = [
    path('', views.get_garden_page, name='garden'),
    path('admin/', views.get_admin_page, name='admin'),
    path('save_garden/', views.save_garden, name='save_garden'),
    path('load_garden/', views.load_garden, name='load_garden'),
    path('assets/', views.asset_list, name='assets'),
    path('place_block/', views.place_block, name='place_block'),
    path('remove_block/', views.remove_block_from_inventory, name='remove_block_from_inventory'),
    path('get_store_items/', views.get_store_items, name='get_store_items'),
    path('buy_item/', views.buy_item, name='buy_item'),
]

