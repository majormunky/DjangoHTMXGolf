from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('accounts/login/', auth_views.login),
    path('accounts/logout/', auth_views.logout),
]
