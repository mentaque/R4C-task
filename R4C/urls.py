"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from orders.views import create_order
from robots.views import create_robot, download_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-robot/', create_robot, name='create-robot'),
    path('download-robots-info/', download_excel, name='download_excel'),
    path('create_order/', create_order, name='create-order'),
]
