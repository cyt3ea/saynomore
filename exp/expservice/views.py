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
		return JsonResponse(resp)

def popular_hairs(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://models-api:8000/api/v1/hairs/popular_hairs/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)
		return JsonResponse(resp)