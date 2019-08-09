from django.urls import path

from . import views

urlpatterns = [
    path('home', views.Home.as_view(), name='dashboard'),
    path('temp', views.Temperature.as_view(), name='temp'),
    path('mositure', views.Moisture.as_view(), name='moisture'),
    path('pressure', views.Pressure.as_view(), name='pressure'),
    path('readings', views.get_readings, name='readings'),
]
