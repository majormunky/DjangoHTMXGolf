from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    #path('accounts/login/', auth_views.login, {"template_name": "core/login.html"}),
    path('accounts/login/', auth_views.login),
    path('accounts/logout/', auth_views.logout),
    #path('accounts/logout/', auth_views.logout, {"template_name": "core/logout.html"}),
    # path('accounts/profile/', views.show_user_profile),
    # path('manage/locations/', views.manage_locations),
    # path('manage/locations/new/', views.add_location),
    # path('manage/locations/<int:location_id>/add_address/', views.add_address_to_location),
    # path('manage/edit_address/<int:address_id>/', views.edit_address),
    # path('manage/users/', views.manage_users),
]
