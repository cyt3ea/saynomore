from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='First Name', max_length=100)
	#your_last_name = forms.CharField(label='Last Name'), max_length=100)

class HairForm(forms.Form):
	name = forms.CharField(label='Hair Name', max_length=100)
	stylist = forms.CharField(label='Stylist', max_length=15)
	location = forms.CharField(label='Location', max_length=100)
	price = forms.DecimalField(label='Price')
	phone_number = forms.CharField(max_length=15)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(label='Password', max_length=100)