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

def index(request):
	# time.sleep(0.5)
	if request.COOKIES.get('auth') == None:
		messages.error(request, "Must login to saynomore.")
		form = LoginForm()
		return render(request, 'frontend/login.html', {'form': form})
	if request.COOKIES.get('auth') != None:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
		if r.json()['ok'] == False:
			messages.error(request, "Must login to saynomore.")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
	reqHair = urllib.request.Request('http://exp-api:8000/api/v1/all_hairs/')
	resp_jsonHair = urllib.request.urlopen(reqHair).read().decode('utf8')
	respHair = json.loads(resp_jsonHair)['resp']
	reqStylists = urllib.request.Request('http://exp-api:8000/api/v1/all_stylists/')
	resp_jsonStylists = urllib.request.urlopen(reqStylists).read().decode('utf8')
	respStylists = json.loads(resp_jsonStylists)['resp']
	return render(request, 'frontend/index.html', {'respHair': respHair, 'respStylists': respStylists})

def hair_detail(request, hair_id):
	if request.COOKIES.get('auth') == None:
		messages.error(request, "Must login to saynomore.")
		form = LoginForm()
		return render(request, 'frontend/login.html', {'form': form})
	else:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
		if r.json()['ok'] == False:
			messages.error(request, "Must login to saynomore.")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://exp-api:8000/api/v1/hairs/' + hair_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)['resp']
		return render(request, 'frontend/hair_detail.html', {'resp': resp})

def stylist_detail(request, stylist_id):
	if request.COOKIES.get('auth') == None:
		messages.error(request, "Must login to saynomore.")
		form = LoginForm()
		return render(request, 'frontend/login.html', {'form': form})
	else:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
		if r.json()['ok'] == False:
			messages.error(request, "Must login to saynomore.")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
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

def create_hair(request):
	if request.COOKIES.get('auth') == None:
		messages.error(request, "Must login to saynomore.")
		form = LoginForm()
		return render(request, 'frontend/login.html', {'form': form})
	else:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
		if r.json()['ok'] == False:
			messages.error(request, "Must login to saynomore.")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
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
			# author = request.user.id
			jsonLogin = {'userAuth': request.COOKIES.get('auth')}
			r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
			if r.json()['ok'] == True:
				author = r.json()['resp']['user_id']
			else:
				form = HairForm()
				messages.error(request, 'Could not find author.')
				return render(request, 'frontend/create_hair.html', {'form': form})
			upvotes = 0
			# return HttpResponse(upvotes)
			jsonHair = {'location':location, 'price':price, 'hair_phone_number': phone_number, 'stylist':stylist, 'hair_upvotes': upvotes, 'author': author, 'name':name}
			# return HttpResponse(jsonStylist)
			r = requests.post('http://exp-api:8000/api/v1/create_hair/', data=jsonHair)
			if r.json()['ok'] == True:
				return HttpResponseRedirect(reverse('index'))
			form = HairForm()
			messages.error(request, 'Error creating hair, please try again.')
			return render(request, 'frontend/create_hair.html', {'form': form})
	else:
		return _error_response(request, 'Must be POST or GET request')
	return render(request, 'frontend/create_hair.html', {'form': form})

def create_user(request):
	if request.COOKIES.get('auth') != None:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
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
			# return HttpResponse(userdata)
			r = requests.post('http://exp-api:8000/api/v1/create_user/', data=userdata)
			if r.json()['ok'] == True:
				form = LoginForm()
				return render(request, 'frontend/login.html', {'form': form})
			form = UserForm()
			messages.error(request, r.json()['error'])
			return render(request, 'frontend/create_user.html', {'form': form})
	else:
		return _error_response(request, 'Must be POST or GET request')
	return render(request, 'frontend/create_user.html', {'form': form})

#Check login through all the layers
def login(request):
	#Check to see if cookie is already stored. If yes,
	if request.COOKIES.get('auth') != None:
		jsonLogin = {'userAuth': request.COOKIES.get('auth')}
		r = requests.post('http://exp-api:8000/api/v1/authenticators/check/', data=jsonLogin)
		if r.json()['ok'] == True:
			return HttpResponseRedirect(reverse('index'))
	if request.method == 'GET':
		form = LoginForm()
	elif request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			input_username = form.cleaned_data['username']
			input_password = form.cleaned_data['password']
			jsonLogin = {'username':input_username, 'password':input_password}
			r = requests.post('http://exp-api:8000/api/v1/login_exp/', data=jsonLogin)
			# return HttpResponse(r.json().items())
			# return HttpResponse(request.COOKIES.get('auth'))

			if r.json()['ok'] == True:
				# return HttpResponse(r)
				authenticator = r.json()['resp']['authenticator_id']
				# return HttpResponse(authenticator)
				response = HttpResponseRedirect(reverse('index'))
				response.set_cookie("auth", authenticator, max_age=1800)
				return response
			form = LoginForm()
			messages.error(request, 'Invalid username/password combination.')
			return render(request, 'frontend/login.html', {'form': form})
	else:
		return _error_response(request, 'Must be POST or GET request')

	return render(request, 'frontend/login.html', {'form': form})

def logout(request):
	if request.method == 'GET':
		if request.COOKIES.get('auth') != None:
			jsonLogin = {'userAuth': request.COOKIES.get('auth')}
			r = requests.post('http://exp-api:8000/api/v1/authenticators/delete/', data=jsonLogin)
			# return HttpResponse(r)
			if r.json()['ok'] == True:
				messages.success(request, "Successfully Logged Out")
				form = LoginForm()
				return render(request, 'frontend/login.html', {'form': form})
			else:
				return _error_response(request, "Could not find authenticator.")
		else:
			messages.error(request, "Must be logged in to logout")
			form = LoginForm()
			return render(request, 'frontend/login.html', {'form': form})
	else:
		return _error_response(request, 'Must be GET request')
	
def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})