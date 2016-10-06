from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import urllib.request
import urllib.parse
import json

def index(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		reqHair = urllib.request.Request('http://exp-api:8000/api/v1/all_hairs/')
		resp_jsonHair = urllib.request.urlopen(reqHair).read().decode('utf8')
		respHair = json.loads(resp_jsonHair)['resp']
		# return JsonResponse(resp)
		reqStylists = urllib.request.Request('http://exp-api:8000/api/v1/all_stylists/')
		resp_jsonStylists = urllib.request.urlopen(reqStylists).read().decode('utf8')
		respStylists = json.loads(resp_jsonStylists)['resp']
		return render(request, 'frontend/index.html', {'respHair': respHair, 'respStylists': respStylists})

def hair_detail(request, hair_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://exp-api:8000/api/v1/hairs/' + hair_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)['resp']
		# return JsonResponse(resp)
		return render(request, 'frontend/hair_detail.html', {'resp': resp})

def stylist_detail(request, stylist_id):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://exp-api:8000/api/v1/stylists/' + stylist_id + '/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)['resp']
		# return JsonResponse(resp)
		return render(request, 'frontend/stylist_detail.html', {'resp': resp})

def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})