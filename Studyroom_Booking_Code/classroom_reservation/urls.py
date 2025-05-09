"""
URL configuration for classroom_reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from reservation.views import redirect_to_user_profile, user_profile_view, custom_login, redirect_to_login

urlpatterns = [
    path("reservation/", include("reservation.urls")),
    path("admin/logout/", redirect_to_login, name='redirect_to_login'),
    path("admin/", admin.site.urls),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Modify this line
    path("booking/", include("booking.urls")),
    path('redirect-to-profile/', redirect_to_user_profile, name='redirect_to_profile'),
    path('user/<str:user_id>/profile/', user_profile_view, name='user_profile'),
]
