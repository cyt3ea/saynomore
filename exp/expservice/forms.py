from django import forms

class NameForm(forms.Form):
	your_first_name = forms.CharField(label='First Name', max_length=100)
	#your_last_name = forms.CharField(label='Last Name'), max_length=100)
