from django.db import models

class User(models.Model):
    username = models.CharField(max_length=24, unique=True)
    date_joined = models.DateTimeField()
    f_name = models.CharField(max_length=16)
    l_name = models.CharField(max_length=16)
    password = models.CharField(max_length=96)
    is_active = models.BooleanField()

class Stylist(models.Model):
	stylist_phone_number = models.CharField(max_length=15)
	years_experience = models.IntegerField(default=0)
	location = models.CharField(max_length=100)
	client_gender = models.CharField(max_length=1)
	user = models.ForeignKey(User)

class Hair(models.Model):
	location = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	hair_phone_number = models.CharField(max_length=15)
	stylist = models.CharField(max_length=50)
	hair_upvotes = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	name = models.CharField(max_length=100)

class Review(models.Model):
	title = models.CharField(max_length=30)
	body = models.TextField()
	rating = models.IntegerField(default=0)
	review_upvotes = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	stylist = models.ForeignKey(Stylist)

class Authenticator(models.Model):
	user_id = models.ForeignKey(User)
	authenticator_id = models.CharField(max_length=96, primary_key=True)
	date_created = models.DateTimeField()