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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index',views.index),
    path('aboutus',views.aboutus),
    path('',views.home),
    path('register',views.register),
    path('login',views.user_login),
    path('productdetails/<pid>',views.productdetails),
    path('kerala',views.kerala),
    path('kedarnath',views.kedarnath),
    path('ladakh',views.ladakh),
    path('goa',views.goa),
    path('rajasthan',views.rajasthan),
    path('logout',views.user_logout),
    path('range',views.range),
    path('sort/<sv>',views.sort),
    path('addcart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path("fetch-reviews/", views.fetch_reviews, name="fetch_reviews"),
    path('search/', views.search_products, name='search_products'),
    path('productdetails/<int:pid>/', views.productdetails, name='productdetails'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('enterotp/', views.enter_otp, name='enter_otp'),
    path('resetpassword/', views.reset_password, name='reset_password'),
    path('booking/<int:product_id>/', views.booking_page, name='booking'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('contactus/',views.contactus),
    path('contact/', views.contact_us, name='contact'),
    
    
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)