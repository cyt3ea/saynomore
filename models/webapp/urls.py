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

from webapp import views

urlpatterns = [
    url(r'^api/v1/users/create/$', views.create_user, name='create-user'),
    url(r'^api/v1/users/(\d+)/$', views.lookup_user, name='lookup-user'),
    url(r'^api/v1/users/delete/(\d+)/$', views.delete_user, name='delete-user'),
    url(r'^api/v1/users/update/(\d+)/$', views.update_user, name='update-user'),

    url(r'^api/v1/hairs/create/$', views.create_hair, name='create-hair'),
    url(r'^api/v1/hairs/(\d+)/$', views.lookup_hair, name='lookup-hair'),
    url(r'^api/v1/hairs/delete/(\d+)/$', views.delete_hair, name='delete-hair'),
    url(r'^api/v1/hairs/update/(\d+)/$', views.update_hair, name='update-hair'),
    url(r'^api/v1/hairs/popular_hairs/$', views.popular_hairs, name='popular-hairs'),
    url(r'^api/v1/hairs/all_hairs/$', views.all_hairs),

    url(r'^api/v1/reviews/create/$', views.create_review, name='create-review'),
    url(r'^api/v1/reviews/(\d+)/$', views.lookup_review, name='lookup-review'),
    url(r'^api/v1/reviews/delete/(\d+)/$', views.delete_review, name='delete-review'),
    url(r'^api/v1/reviews/update/(\d+)/$', views.update_review, name='update-review'),

    url(r'^api/v1/stylists/create/$', views.create_stylist, name='create-stylist'),
    url(r'^api/v1/stylists/(\d+)/$', views.lookup_stylist, name='lookup-stylist'),
    url(r'^api/v1/stylists/delete/(\d+)/$', views.delete_stylist, name='delete-stylist'),
    url(r'^api/v1/stylists/update/(\d+)/$', views.update_stylist, name='update-stylist'),
    url(r'^api/v1/stylists/all_stylists/$', views.all_stylists, name='all-stylists'),
    url(r'^api/v1/stylists/reviews/(\d+)/$', views.stylist_reviews, name='stylist-reviews'),
]
