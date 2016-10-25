from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import requests
import urllib.request
import urllib.parse
import json


def all_hairs(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/hairs/all_hairs/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		all_hairs = resp["resp"]["all_hairs"]
		for hair in all_hairs:
			getUser(hair)
		return JsonResponse(resp)

def popular_hairs(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/hairs/popular_hairs/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		popular_hairs = resp["resp"]["popular_hairs"]
		for hair in popular_hairs:
			getUserAndStylist(hair)
		return JsonResponse(resp)

def detail_hair(request, hair_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/hairs/' + hair_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		hair = resp["resp"]
		getUser(hair)
		return JsonResponse(resp)

def getUser(obj):
	reqUser = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(obj["author"]) + '/')
	resp_jsonUser = urllib.request.urlopen(reqUser).read().decode('utf8')
	respUser = json.loads(resp_jsonUser)
	obj["author"] = respUser["resp"]


def all_stylists(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/stylists/all_stylists/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		all_stylists = resp["resp"]["all_stylists"]
		for stylist in all_stylists:
			getStylistFK(stylist)
		return JsonResponse(resp)

def detail_stylist(request, stylist_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/stylists/' + stylist_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		stylist = resp["resp"]
		getStylistFK(stylist)
		return JsonResponse(resp)

def review_stylist(request, stylist_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/stylists/reviews/' + stylist_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		stylist_reviews = resp["resp"]["reviews"]
		for review in stylist_reviews:
			getUser(review)
		return JsonResponse(resp)

def getStylistFK(stylist):
	reqStylist = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(stylist["user"]) + '/')
	resp_jsonStylist = urllib.request.urlopen(reqStylist).read().decode('utf8')
	respStylist = json.loads(resp_jsonStylist)
	stylist["user"] = respStylist["resp"]

def createHair(request):
	if request.method == 'POST':
		jsonHair = {'location':request.POST['location'], 'price':request.POST['price'], 'hair_phone_number': request.POST['hair_phone_number'], 'stylist':request.POST['stylist'], 'hair_upvotes': request.POST['hair_upvotes'], 'author': request.POST['author'], 'name':request.POST['name']}
		r = requests.post('http://models-api:8000/api/v1/hairs/create/', data=jsonHair)
		return HttpResponse(r)
	else:
		return _error_response(request, 'Must be POST request')

#Calls the Login API from the models layer
def login_exp(request):
	if request.method == 'POST':
		loginData = {'username': request.POST['username'], 'password': request.POST['password'],}
		r = requests.post('http://models-api:8000/api/v1/login_mod/', data=loginData)
		return HttpResponse(r)
	else:
		return _error_response(request, 'Must be POST request')

def check_authenticator(request):
	if request.method == 'POST':
		r = requests.get('http://models-api:8000/api/v1/authenticator/' + request.POST['userAuth'] + '/')
		return HttpResponse(r)
	else:
		return _error_response(request, 'Must be POST request')

def delete_authenticator(request):
	if request.method == 'POST':
		r = requests.delete('http://models-api:8000/api/v1/authenticator/delete/' + request.POST['userAuth'] + '/')
		return HttpResponse(r)
	else:
		return _error_response(request, 'Must be POST request')

def create_user(request):
	if request.method == 'POST':
		userdata = {'f_name':request.POST['firstname'], 'l_name': request.POST['lastname'], 'username':request.POST['username'], 'password':request.POST['password']}
		r = requests.post('http://models-api:8000/api/v1/users/exists/', data=userdata)
		if r.json()['ok'] == True: # user exists
			return HttpResponse(_error_response(request, "Username already exists."))		
		r = requests.post('http://models-api:8000/api/v1/users/create/', data=userdata)
		return HttpResponse(r)

	else:
		return _error_response(request, 'Must be POST request')

def all_users(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/users/all_users/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		all_users = resp["resp"]["all_users"]
		for user in all_users:
			getUser(users)
		return JsonResponse(resp)


def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})