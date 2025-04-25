from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Plant identification routes
    path('', views.index, name='home'),
    path('plants/', views.index, name='plants_index'),
    path('plants/identify/', views.identify, name='plants_identify'),
    
    # Authentication routes
    path('login/', auth_views.LoginView.as_view(template_name='plants/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]
