from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django import db
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest

from webapp import models

from django.contrib.auth.models import User

def create_stylist(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	if 'stylist_phone_number' not in request.POST or 'years_experience' not in request.POST or 'location' not in request.POST or 'client_gender' not in request.POST:
		return HttpResponseBadRequest("400 Bad Request - missing required fields")
	s = models.Stylist(stylist_phone_number=request.POST['stylist_phone_number'],
					   years_experience=request.POST['years_experience'],
					   location = request.POST['location'],
	       			   client_gender = request.POST['client_gender'])

	try:
		s.save()
	except db.Error:
		return HttpResponseBadRequest("db error")
	data = serializers.serialize("json", [s])
	return HttpResponse(data)

def lookup_stylist(request, stylist_id):
	if request.method != 'GET':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		s = models.Stylist.objects.get(pk=stylist_id)
	except models.Stylist.DoesNotExist:
		return HttpResponseBadRequest("Stylist not found")
	data = serializers.serialize("json", [s])
	return HttpResponse(data)


def update_stylist(request, stylist_id):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	try:
		s = models.Stylist.objects.get(pk=stylist_id)
	except models.Stylist.DoesNotExist:
		return HttpResponseBadRequest("Stylist not found")

	changed = False
	if 'stylist_phone_number' in request.POST:
		s.stylist_phone_number = request.POST['stylist_phone_number']
		changed = True
	if 'years_experience' in request.POST:
		s.years_experience = request.POST['years_experience']
		changed = True
	if 'location' in request.POST:
		s.location = request.POST['location']
		changed = True
	if 'client_gender' in request.POST:
		s.client_gender = request.POST['client_gender']
		changed = True

	if not changed:
		return HttpResponseBadRequest("No fields updated")

	s.save()
	data = serializers.serialize("json", [s])
	return HttpResponse(data)


def create_user(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	if 'first_name' not in request.POST or 'last_name' not in request.POST or 'email' not in request.POST or 'password' not in request.POST or 'username' not in request.POST:
		return HttpResponseBadRequest("400 Bad Request - missing required fields")

	u = User.objects.create_user(first_name=request.POST['first_name'], 
					last_name=request.POST['last_name'],
					email=request.POST['email'],
					password=request.POST['password'],
					username=request.POST['username'])
	try:
	    u.save()
	except db.Error:
	    return HttpResponseBadRequest("db error")
	data = serializers.serialize("json", [u])
	return HttpResponse(data)

def lookup_user(request, user_id):
	if request.method != 'GET':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		u = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return HttpResponseBadRequest("User not found")
	data = serializers.serialize("json", [u])
	return HttpResponse(data)

def update_user(request, user_id):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	try:
		u = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return HttpResponseBadRequest("User not found")

	changed = False
	if 'username' in request.POST:
		u.username = request.POST['username']
		changed = True
	if 'first_name' in request.POST:
		u.first_name = request.POST['first_name']
		changed = True
	if 'last_name' in request.POST:
		u.last_name = request.POST['last_name']
		changed = True
	if 'email' in request.POST:
		u.email = request.POST['email']
		changed = True
	if 'password' in request.POST:
		u.password = request.POST['password']
		changed = True

	if not changed:
		return HttpResponseBadRequest("No fields updated")

	u.save()
	data = serializers.serialize("json", [u])
	return HttpResponse(data)

# Tested using django client tool -- go into python manage.py shell
# from django.test import Client
# c = Client()
# response = c.post('/api/hairs/create', {'location': 'Charlottesville', 'stylist': 'George McBucket', 'hair_phone_number': '18009002233', 'price': '22.33'})
# response.status_code
# print(response.content)
def create_hair(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	if 'location' not in request.POST or 'price' not in request.POST or 'hair_phone_number' not in request.POST or 'stylist' not in request.POST:     
		# 'price' not in request.POST or     
		# 'hair_phone_number' not in request.POST or   
		# 'stylist' not in request.POST:
		return HttpResponseBadRequest("400 Bad Request - missing required fields")

	h = models.Hair(location=request.POST['location'], 
					price=request.POST['price'],
					hair_phone_number=request.POST['hair_phone_number'],
					stylist=request.POST['stylist'],
					hair_upvotes=0)
	try:
	    h.save()
	except db.Error:
	    return HttpResponseBadRequest("db error")
	data = serializers.serialize("json", [h])
	return HttpResponse(data)

def lookup_hair(request, hair_id):
	if request.method != 'GET':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		h = models.Hair.objects.get(pk=hair_id)
	except models.Hair.DoesNotExist:
		return HttpResponseBadRequest("Hair not found")
	data = serializers.serialize("json", [h])
	return HttpResponse(data)

# Tested using django client tool -- go into python manage.py shell
# from django.test import Client
# c = Client()
# response = c.post('/api/hairs/update/3', {'location': 'Charlottesville', 'stylist': 'George McBucket', 'hair_phone_number': '911', 'price': '22.33'})
# response.status_code
# print(response.content)
def update_hair(request, hair_id):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	try:
		h = models.Hair.objects.get(pk=hair_id)
	except models.Hair.DoesNotExist:
		return HttpResponseBadRequest("Hair not found")

	changed = False
	if 'location' in request.POST:
		h.location = request.POST['location']
		changed = True
	if 'price' in request.POST:
		h.price = request.POST['price']
		changed = True
	if 'hair_phone_number' in request.POST:
		h.hair_phone_number = request.POST['hair_phone_number']
		changed = True
	if 'stylist' in request.POST:
		h.stylist = request.POST['stylist']
		changed = True
	if 'hair_upvotes' in request.POST:
		h.hair_upvotes = request.POST['hair_upvotes']
		changed = True

	if not changed:
		return HttpResponseBadRequest("No fields updated")

	h.save()
	data = serializers.serialize("json", [h])
	return HttpResponse(data)

def create_review(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	if 'title' not in request.POST or 'body' not in request.POST or 'author' not in request.POST or 'rating' not in request.POST:     
		# 'title' not in request.POST or
		# 'body' not in request.POST or
		# 'author' not in request.POST or     
		# 'rating' not in request.POST:  
		return HttpResponseBadRequest("400 Bad Request - missing required fields")

	r = models.Review(title=request.POST['title'], 
					body=request.POST['body'],
					author=request.POST['author'],
					rating=request.POST['rating'],
					review_upvotes=0)
	try:
	    r.save()
	except db.Error:
	    return HttpResponseBadRequest("db error: saving reviews")
	data = serializers.serialize("json", [r])
	return HttpResponse(data)

def lookup_review(request, review_id):
	if request.method != 'GET':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP GET request")
	# r = get_object_or_404(models.Review, pk=review_id)
	try:
		r = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return HttpResponseBadRequest("Review not found")
	data = serializers.serialize("json", [r])
	return HttpResponse(data)

def update_review(request, review_id):
	if request.method != 'POST':
		return HttpResponseBadRequest("400 Bad Request - must make HTTP POST request")
	try:
		r = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return HttpResponseBadRequest("Review not found")

	changed = False
	if 'title' in request.POST:
		r.title = request.POST['title']
		changed = True
	if 'body' in request.POST:
		r.body = request.POST['body']
		changed = True
	if 'author' in request.POST:
		r.author = request.POST['author']
		changed = True
	if 'rating' in request.POST:
		r.rating = request.POST['rating']
		changed = True
	if 'review_upvotes' in request.POST:
		r.review_upvotes = request.POST['review_upvotes']
		changed = True

	if not changed:
		return HttpResponseBadRequest("No fields updated")

	r.save()
	data = serializers.serialize("json", [r])
	return HttpResponse(data)