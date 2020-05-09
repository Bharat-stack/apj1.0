"""letsplay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from celebrate_api.views import BharatView



""" from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) """


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path(r'api/<endpoint>', BharatView),
    path(r'api/<endpoint>/', BharatView),

]

'''path(r'api/signup01/', create_user_01),
    path(r'api/sendotp01/', send_otp_01),
    path(r'api/login01/', get_token_01),
    path(r'api/getuser01/', get_user_01),
'''

