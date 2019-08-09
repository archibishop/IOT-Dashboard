from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.Login.as_view(), name='login'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('signout', views.Logout.as_view(), name='signout'),
]
