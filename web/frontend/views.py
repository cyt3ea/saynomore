from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import urllib.request
import urllib.parse
import json

def index(request):
	if request.method != 'GET':
		return _error_response(request, 'Must be GET request')
	else:
		req = urllib.request.Request('http://exp-api:8000/all_hairs/')
		resp_json = urllib.request.urlopen(req).read().decode('utf8')
		resp = json.loads(resp_json)['resp']
		# return JsonResponse(resp)
		return render(request, 'frontend/index.html', {'resp': resp})

def hair_detail(request, hair_id):
	return HttpResponse("Hair detail " + hair_id)

