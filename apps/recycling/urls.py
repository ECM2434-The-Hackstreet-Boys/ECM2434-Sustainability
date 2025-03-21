from django.urls import path
from . import views


# URL patterns for the recycling app /recycling/
urlpatterns = [
    path('<int:bin_id>/', views.recyclepage, name='recycling'),
    path('submit_recycling', views.submit_recycling, name='submit_recycling'),
]