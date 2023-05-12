from django.urls import path
from . import views

# URLs for the applications
urlpatterns = [
    path('', views.index, name = 'index'),
]