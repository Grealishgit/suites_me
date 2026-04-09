from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('info/', views.redirect_page, name='redirect'),
    path('login/', views.login_page, name='login'),
    path('check-email/', views.check_email, name='check_email'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('thanks/', views.thanks, name='thanks'),
]