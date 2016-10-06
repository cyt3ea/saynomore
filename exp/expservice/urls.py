"""saynomore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from expservice import views

urlpatterns = [
	url(r'^api/v1/all_hairs/$', views.all_hairs),
    url(r'^api/v1/popular_hairs/$', views.popular_hairs),
    url(r'^api/v1/hairs/(\d+)/$', views.detail_hair),
    url(r'^api/v1/all_stylists/$', views.all_stylists),
    url(r'^api/v1/stylists/(\d+)/$', views.detail_stylist),

]
