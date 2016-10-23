from django.shortcuts import render
from django.http import JsonResponse

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
			getUserAndStylist(hair)
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
		getUserAndStylist(hair)
		return JsonResponse(resp)

def getUserAndStylist(obj):
	reqStylist = urllib.request.Request('http://models-api:8000/api/v1/stylists/' + str(obj["stylist"]) + '/')
	resp_jsonStylist = urllib.request.urlopen(reqStylist).read().decode('utf8')
	respStylist = json.loads(resp_jsonStylist)
	obj["stylist"] = respStylist["resp"]
	reqUser = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(obj["stylist"]["user"]) + '/')
	resp_jsonUser = urllib.request.urlopen(reqUser).read().decode('utf8')
	respUser = json.loads(resp_jsonUser)
	obj["stylist"]["user"] = respUser["resp"]
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
			getUserAndStylist(review)
		return JsonResponse(resp)

def getStylistFK(stylist):
	reqStylist = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(stylist["user"]) + '/')
	resp_jsonStylist = urllib.request.urlopen(reqStylist).read().decode('utf8')
	respStylist = json.loads(resp_jsonStylist)
	stylist["user"] = respStylist["resp"]

def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})