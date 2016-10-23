from django import forms

class NameForm(forms.Form):
	your_first_name = forms.CharField(label='First Name', max_length=100)
	#your_last_name = forms.CharField(label='Last Name'), max_length=100)

class HairForm(forms.Form):
	location = forms.CharField(label='Location', max_length=100)
	price = forms.DecimalField(label='Price')
	stylist = forms.CharField(label='Stylist', max_length=15)
	name = forms.CharField(label='Hair Name', max_length=100)