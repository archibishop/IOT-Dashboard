from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('home',  (views.Home.as_view()), name='dashboard'),
    path('temp', views.Temperature.as_view(), name='temp'),
    path('mositure', views.Moisture.as_view(), name='moisture'),
    path('pressure', views.Pressure.as_view(), name='pressure'),
    path('readings', views.get_readings, name='readings'),
    path('pdf/<int:page>', views.PDF.as_view(), name='pdf'),
    path('generate-pdf/<int:page>', views.GeneratePdf.as_view(),
         name='generate-pdf'),        
]
