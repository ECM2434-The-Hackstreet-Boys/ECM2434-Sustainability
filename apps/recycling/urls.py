from django.urls import path
from . import views


# URL patterns for the recycling app /recycling/
urlpatterns = [
    path('', views.recyclepage, name='recycling'),
]