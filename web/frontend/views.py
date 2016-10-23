from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .forms import NameForm, HairForm, LoginForm
from django.core.urlresolvers import reverse
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
		reqStylist = urllib.request.Request('http://exp-api:8000/api/v1/stylists/' + stylist_id + '/')
		resp_jsonStylist = urllib.request.urlopen(reqStylist).read().decode('utf8')
		respStylist = json.loads(resp_jsonStylist)['resp']
		# return JsonResponse(resp)
		reqReviews = urllib.request.Request('http://exp-api:8000/api/v1/stylists/reviews/' + stylist_id + '/')
		resp_jsonReviews = urllib.request.urlopen(reqReviews).read().decode('utf8')
		respReviews = json.loads(resp_jsonReviews)['resp']
		return render(request, 'frontend/stylist_detail.html', {'stylist': respStylist, 'reviews': respReviews})

def create_hair(request):
	if request.method == 'GET':
		form = HairForm()
	elif request.method == 'POST':
		form = HairForm(request.POST)
		if form.is_valid():
			return HttpResponse("Valid Hair yay!")
	else:
		return _error_response(request, 'Must be GET request')
	return render(request, 'frontend/create_hair.html', {'form': form})

def get_name(request):
	# if this is a Post request we need to process the form data
	if request.method == 'POST':
		#create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required 
			# ...
			# redirect to new URL:
			return HttpResponseRedirect('/thanks/')
		# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request, 'name.html', {'form': form})

#Check login through all the layers
def login(request):
	f = LoginForm(request.POST)
	if request.method == 'GET':
		next = request.GET.get('index') or reverse('LoginForm')
		return render(request, 'frontend/login.html', {'form': f})
	
	if not f.is_valid():
		return render(request, 'frontend/login.html', {'form': f})
	username = f.cleaned_data['username']
	password = f.cleaned_data['password']
	next = f.cleaned_data.get('index') or reverse('LoginForm')
	
	#CALL EXP LAYER BELOW
	resp = urllib.request.Request('http://exp-api:8000/api/v1/login-exp/')
	resp_jsonLogin = urllib.request.urlopen(resp).read().decode('utf8')
	respLogin = json.loads(resp_jsonLogin)['resp']
	if not resp or not resp['ok']:
		return render(request, 'frontend/login.html', {'form': f})
	authenticator = resp['resp']['authenticator']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator)
	return response

def _error_response(request, error_msg):
	return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'ok': True, 'resp': resp})
	else:
		return JsonResponse({'ok': True})