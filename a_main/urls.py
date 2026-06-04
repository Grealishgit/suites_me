from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('info/', views.redirect_page, name='redirect'),
    path('info', views.redirect_page, name='redirect_no_slash'),
    path('login/', views.login_page, name='login'),
    path('login', views.login_page, name='login_no_slash'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-email', views.check_email, name='check_email_no_slash'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('enter-otp', views.enter_otp, name='enter_otp_no_slash'),
    path('thanks/', views.thanks, name='thanks'),
    path('thanks', views.thanks, name='thanks_no_slash'),
]
