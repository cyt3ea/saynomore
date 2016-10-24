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
	url(r'^api/v1/all_hairs/$', views.all_hairs, name='all-hairs'),
    url(r'^api/v1/popular_hairs/$', views.popular_hairs, name='popular-hairs'),
    url(r'^api/v1/hairs/(?P<hair_id>\d+)/$', views.detail_hair, name='detail-hair'),
    url(r'^api/v1/all_stylists/$', views.all_stylists, name='all-stylists'),
    url(r'^api/v1/stylists/(?P<stylist_id>\d+)/$', views.detail_stylist, name='detail-stylist'),
    url(r'^api/v1/stylists/reviews/(?P<stylist_id>\d+)/$', views.review_stylist, name='review-stylist'),
    url(r'^api/v1/create_hair/$', views.createHair, name='create-hair'),    
    url(r'^api/v1/create_user/$', views.create_user, name='create-user'),    
    url(r'^api/v1/login_exp/$', views.login_exp, name='login-exp'),
    url(r'^api/v1/users/all_users/$', views.all_users, name='all-users'),
    url(r'^api/v1/authenticators/check/$', views.check_authenticator, name='check-authenticator'),

]

