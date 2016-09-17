from django.db import models
from django.contrib.auth.models import User


class Hair(models.Model):
	id = models.AutoField(primary_key=True)
	location = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	hair_phone_number = models.CharField(max_length=15)
	stylist = models.CharField(max_length=30)
	hair_upvotes = models.IntegerField(default=0)

class Review(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=30)
	body = models.TextField()
	author = models.ForeignKey(User, unique=True)
	rating = models.IntegerField(default=0)
	review_upvotes =models.IntegerField(default=0)

class Stylist(models.Model):
	id = models.AutoField(primary_key=True)
	stylist_phone_number = models.CharField(max_length=15)
	years_experience = models.IntegerField(default=0)
	location = models.CharField(max_length=100)
	client_gender = models.CharField(max_length=1)
