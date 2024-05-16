from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
     path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('api/profile/', views.ProfileView.as_view(), name='api_profile'),
]
