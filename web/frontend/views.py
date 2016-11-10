from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .forms import UserForm, HairForm, LoginForm
from django.contrib import messages

import requests
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
import json
import time

def login_required(f):
	def wrap(request, *args, **kwargs):
		# try authenticating the user
		if request.COOKIES.get('auth') == None:
			messages.error(request, "Must login to saynomore.")
			return HttpResponseRedirect(reverse('login')+'?next='+request.path)
		elif request.COOKIES.get('auth') != None:
			jsonLogin = {'userAuth': request.COOKIES.get('auth')}
			r = requests.post('http://exp-api:8000/api/v1/authenticators/check_user/', data=jsonLogin)
			if r.json()['ok'] == False:
				messages.error(request, "Must login to saynomore.")
				return HttpResponseRedirect(reverse('login')+'?next='+request.path)
		return f(request, *args, **kwargs)
	return wrap

@login_required
def index(request):
	reqHair = urllib.request.Request('http://exp-api:8000/api/v1/all_hairs/')
	resp_jsonHair = urllib.request.urlopen(reqHair).read().decode('utf8')
	respHair = json.loads(resp_jsonHair)['resp']
	reqStylists = urllib.request.Request('http://exp-api:8000/api/v1/all_stylists/')
	resp_jsonStylists = urllib.request.urlopen(reqStylists).read().decode('utf8')
	respStylists = json.loads(resp_jsonStylists)['resp']
	return render(request, 'frontend/index.html', {'respHair': respHair, 'respStylists': respStylists})

@login_required
def hair_detail(request, hair_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://exp-api:8000/api/v1/hairs/' + hair_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)['resp']
		return render(request, 'frontend/hair_detail.html', {'resp': resp})

@login_required
def stylist_detail(request, stylist_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		reqStylist = urllib.request.Request('http://exp-api:8000/api/v1/stylists/' + stylist_id + '/')
		resp_jsonStylist = urllib.request.urlopen(reqStylist).read().decode('utf8')
		respStylist = json.loads(resp_jsonStylist)['resp']
		reqReviews = urllib.request.Request('http://exp-api:8000/api/v1/stylists/reviews/' + stylist_id + '/')
		resp_jsonReviews = urllib.request.urlopen(reqReviews).read().decode('utf8')
		respReviews = json.loads(resp_jsonReviews)['resp']
		return render(request, 'frontend/stylist_detail.html', {'stylist': respStylist, 'reviews': respReviews})

@login_required
def create_hair(request):
	if request.method == 'GET':
		form = HairForm()
	elif request.method == 'POST':
		form = HairForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			stylist = form.cleaned_data['stylist']
			location = form.cleaned_data['location']
			price = form.cleaned_data['price']
			phone_number = form.cleaned_data['phone_number']
			jsonLogin = {'userAuth': request.COOKIES.get('auth')}
			r = requests.post('http://exp-api:8000/api/v1/authenticators/check_user/', data=jsonLogin)
			if r.json()['ok'] == True:
				author = r.json()['resp']['user_id']
			else:
				messages.error(request, 'Could not find author.')
				return HttpResponseRedirect(reverse('create-hair'))
			upvotes = 0
			jsonHair = {'location':location, 'price':price, 'hair_phone_number': phone_number, 'stylist':stylist, 'hair_upvotes': upvotes, 'author': author, 'name':name}
			r = requests.post('http://exp-api:8000/api/v1/create_hair/', data=jsonHair)
			if r.json()['ok'] == True:
				return HttpResponseRedirect(reverse('index'))
			messages.error(request, 'Error creating hair, please try again.')
			return HttpResponseRedirect(reverse('create-hair'))
	else:
		return _error_response(request, 'Must be POST or GET request')
	return render(request, 'frontend/create_hair.html', {'form': form})

def create_user(request):
	if request.COOKIES.get('auth') != None:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check_user/', data=jsonLogin)
		if r.json()['ok'] == True:
			return HttpResponseRedirect(reverse('index'))
	if request.method == 'GET':
		form = UserForm()
	elif request.method == 'POST':
		#create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			userdata = {'firstname':firstname, 'lastname': lastname, 'username':username, 'password':password}
			r = requests.post('http://exp-api:8000/api/v1/create_user/', data=userdata)
			if r.json()['ok'] == True:
				return HttpResponseRedirect(reverse('login'))
			form = UserForm()
			messages.error(request, r.json()['error'])
			return HttpResponseRedirect(reverse('create-user'))
	else:
		return _error_response(request, 'Must be POST or GET request')
	return render(request, 'frontend/create_user.html', {'form': form})

from django.conf import settings
#Check login through all the layers
def login(request):
	# return HttpResponse(settings.STATICFILES_DIRS)
	#Check to see if cookie is already stored. If yes,
	if request.COOKIES.get('auth') != None:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check_user/', data=jsonLogin)
		if r.json()['ok'] == True:
			return HttpResponseRedirect(reverse('index'))
	if request.method == 'GET':
		form = LoginForm()
	elif request.method == 'POST':
		# return HttpResponse(request.GET.get('next'))
		form = LoginForm(request.POST)
		if form.is_valid():
			input_username = form.cleaned_data['username']
			input_password = form.cleaned_data['password']
			jsonLogin = {'username':input_username, 'password':input_password}
			r = requests.post('http://exp-api:8000/api/v1/login_exp/', data=jsonLogin)
			if r.json()['ok'] == True:
				authenticator = r.json()['resp']['authenticator_id']
				response = HttpResponseRedirect(request.GET.get('next', '/index/'))
				response.set_cookie("auth", authenticator, max_age=1800)
				return response
			form = LoginForm()
			messages.error(request, 'Invalid username/password combination.')
			return render(request, 'frontend/login.html', {'form': form})
	else:
		return _error_response(request, 'Must be POST or GET request')

	return render(request, 'frontend/login.html', {'form': form})

@login_required
def logout(request):
	if request.method == 'GET':
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/logout/', data=jsonLogin)
		if r.json()['ok'] == True:
			messages.success(request, "Successfully Logged Out")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
		else:
			return _error_response(request, "Could not find authenticator.")
	else:
		return _error_response(request, 'Must be GET request')
	
def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})

def search_hairstyle(request):
	search = {'query': request.POST['hairstyle_search']}
	r = requests.post('http://exp-api:8000/api/v1/find_hairs/', data=search)
	return HttpResponse(r)
	return render(request, 'frontend/search_results.html', {'search': search})