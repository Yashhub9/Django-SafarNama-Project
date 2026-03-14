"""
URL configuration for safarnama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from safarnama_app import views
from safarnama import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index',views.index, name='index'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('',views.home, name='home'),
    path('register',views.register, name='register'),
    path('login',views.user_login, name='user_login'),
    path('productdetails/<pid>',views.productdetails),
    path('logout',views.user_logout, name='logout'),
    path('range',views.range, name='range'),
    path('sort/<sv>',views.sort, name='sort'),
    path('search/', views.search_products, name='search_products'),
    path('productdetails/<int:pid>/', views.productdetails, name='productdetails'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('enterotp/', views.enter_otp, name='enter_otp'),
    path('resetpassword/', views.reset_password, name='reset_password'),
    path('booking/<int:product_id>/', views.booking_page, name='booking'),
    path('accounts/login/', views.user_login),
    path('contactus/',views.contactus, name='contactus'),
    path('contact/', views.contact_us, name='contact'),
    
    
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
