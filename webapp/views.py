import datetime
from django.contrib.auth import hashers


from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django import db
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict


from webapp import models

def create_stylist(request):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	if 'stylist_phone_number' not in request.POST or 'years_experience' not in request.POST or 'location' not in request.POST or 'client_gender' not in request.POST:
		return _error_response(request, "400 Bad Request - missing required fields")
	s = models.Stylist(stylist_phone_number=request.POST['stylist_phone_number'],
					   years_experience=request.POST['years_experience'],
					   location = request.POST['location'],
	       			   client_gender = request.POST['client_gender'])

	try:
		s.save()
	except db.Error:
		return _error_response(request, "db error")
	return _success_response(request, model_to_dict(s))

def lookup_stylist(request, stylist_id):
	if request.method != 'GET':
		return _error_response(request, "400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		s = models.Stylist.objects.get(pk=stylist_id)
	except models.Stylist.DoesNotExist:
		return _error_response(request, "Stylist not found")
	return _success_response(request, model_to_dict(s))

def delete_stylist(request, stylist_id):
	if request.method != 'DELETE':
		return _error_response(request, "400 Bad Request - must make HTTP DELETE request")
	try:
		s = models.Stylist.objects.get(pk=stylist_id)
	except models.Stylist.DoesNotExist:
		return _error_response(request, "Stylist not found")
	s.delete()
	return _success_response(request)


def update_stylist(request, stylist_id):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	try:
		s = models.Stylist.objects.get(pk=stylist_id)
	except models.Stylist.DoesNotExist:
		return _error_response(request, "Stylist not found")

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
		return _error_response(request, "No fields updated")

	s.save()
	return _success_response(request, model_to_dict(s))


def create_user(request):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	if 'f_name' not in request.POST or 'l_name' not in request.POST or  'password' not in request.POST or 'username' not in request.POST:
		return _error_response(request, "400 Bad Request - missing required fields")

	u = models.User(f_name=request.POST['f_name'], 
					l_name=request.POST['l_name'],
					password=hashers.make_password(request.POST['password']),
					username=request.POST['username'],
					date_joined=datetime.datetime.now(),
					is_active=False)
	try:
	    u.save()
	except db.Error:
	    return _error_response(request, "db error")
	return _success_response(request, model_to_dict(u))

def lookup_user(request, user_id):
	if request.method != 'GET':
		return _error_response(request, "400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		u = models.User.objects.get(pk=user_id)
	except models.User.DoesNotExist:
		return _error_response(request, "User not found")
	return _success_response(request, model_to_dict(u))

def delete_user(request, user_id):
	if request.method != 'DELETE':
		return _error_response(request, "400 Bad Request - must make HTTP DELETE request")
	try:
		u = models.User.objects.get(pk=user_id)
	except models.User.DoesNotExist:
		return _error_response(request, "User not found")
	u.delete()
	return _success_response(request)

def update_user(request, user_id):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	try:
		u = models.User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return _error_response(request, "User not found")

	changed = False
	if 'username' in request.POST:
		u.username = request.POST['username']
		changed = True
	if 'f_name' in request.POST:
		u.f_name = request.POST['f_name']
		changed = True
	if 'l_name' in request.POST:
		u.l_name = request.POST['l_name']
		changed = True
	if 'email' in request.POST:
		u.email = request.POST['email']
		changed = True
	if 'password' in request.POST:
		u.password = request.POST['password']
		changed = True

	if not changed:
		return _error_response(request, "No fields updated")

	u.save()
	return _success_response(request, model_to_dict(u))

# Tested using django client tool -- go into python manage.py shell
# from django.test import Client
# c = Client()
# response = c.post('/api/hairs/create', {'location': 'Charlottesville', 'stylist': 'George McBucket', 'hair_phone_number': '18009002233', 'price': '22.33'})
# response.status_code
# print(response.content)
def create_hair(request):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	if 'location' not in request.POST or 'price' not in request.POST or 'hair_phone_number' not in request.POST or 'stylist' not in request.POST:
		return _error_response(request, "400 Bad Request - missing required fields")

	h = models.Hair(location=request.POST['location'], 
					price=request.POST['price'],
					hair_phone_number=request.POST['hair_phone_number'],
					stylist=request.POST['stylist'],
					hair_upvotes=0)
	try:
	    h.save()
	except db.Error:
	    return _error_response(request, "db error")
	return _success_response(request, model_to_dict(h))

def lookup_hair(request, hair_id):
	if request.method != 'GET':
		return _error_response(request, "400 Bad Request - must make HTTP GET request")
	# h = get_object_or_404(models.Hair, pk=hair_id)
	try:
		h = models.Hair.objects.get(pk=hair_id)
	except models.Hair.DoesNotExist:
		return _error_response(request, "Hair not found")
	return _success_response(request, model_to_dict(h))

def delete_hair(request, hair_id):
	if request.method != 'DELETE':
		return _error_response(request, "400 Bad Request - must make HTTP DELETE request")
	try:
		h = models.Hair.objects.get(pk=hair_id)
	except models.Hair.DoesNotExist:
		return _error_response(request, "Hair not found")
	h.delete()
	return _success_response(request)

# Tested using django client tool -- go into python manage.py shell
# from django.test import Client
# c = Client()
# response = c.post('/api/hairs/update/3', {'location': 'Charlottesville', 'stylist': 'George McBucket', 'hair_phone_number': '911', 'price': '22.33'})
# response.status_code
# print(response.content)
def update_hair(request, hair_id):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	try:
		h = models.Hair.objects.get(pk=hair_id)
	except models.Hair.DoesNotExist:
		return _error_response(request, "Hair not found")

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
		return _error_response(request, "No fields updated")

	h.save()
	return _success_response(request, model_to_dict(h))

def create_review(request):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	if 'title' not in request.POST or 'body' not in request.POST or 'author' not in request.POST or 'rating' not in request.POST:      
		return _error_response(request, "400 Bad Request - missing required fields")
	if not models.User.objects.filter(pk=request.POST['author']).exists():
		return _error_response("User does not exist")
	u = models.User.objects.get(pk=request.POST['author'])

	r = models.Review(title=request.POST['title'],
					body=request.POST['body'],
					author=u,
					rating=request.POST['rating'],
					review_upvotes=0)
	try:
	    r.save()
	except db.Error:
	    return _error_response(request, "db error: saving reviews - " + str(u.id))
	return _success_response(request, model_to_dict(r))

def lookup_review(request, review_id):
	if request.method != 'GET':
		return _error_response(request, "400 Bad Request - must make HTTP GET request")
	# r = get_object_or_404(models.Review, pk=review_id)
	try:
		r = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return _error_response(request, "Review not found")
	return _success_response(request, model_to_dict(r))

def delete_review(request, review_id):
	if request.method != 'DELETE':
		return _error_response(request, "400 Bad Request - must make HTTP DELETE request")
	try:
		r = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return _error_response(request, "Review not found")
	r.delete()
	return _success_response(request)

def update_review(request, review_id):
	if request.method != 'POST':
		return _error_response(request, "400 Bad Request - must make HTTP POST request")
	try:
		r = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return _error_response(request, "Review not found")

	if not models.User.objects.filter(pk=request.POST['author']).exists():
		return _error_response("User does not exist")
	u = models.User.objects.get(pk=request.POST['author'])

	changed = False
	if 'title' in request.POST:
		r.title = request.POST['title']
		changed = True
	if 'body' in request.POST:
		r.body = request.POST['body']
		changed = True
	if 'author' in request.POST:
		r.author = u
		changed = True
	if 'rating' in request.POST:
		r.rating = request.POST['rating']
		changed = True
	if 'review_upvotes' in request.POST:
		r.review_upvotes = request.POST['review_upvotes']
		changed = True

	if not changed:
		return _error_response(request, "No fields updated")

	r.save()
	return _success_response(request, model_to_dict(r))

def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})