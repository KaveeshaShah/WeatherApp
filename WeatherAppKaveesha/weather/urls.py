from django.urls import path,include
from . import views

#Later make this home page
urlpatterns = [
    path('home/', views.home, name='weather-app-home'),
]
