from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', views.LoginView, name = 'login'),
    path('logout/',views.LogoutView,name='logout'),
    path('signup/',views.SignupView,name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
