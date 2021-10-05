from django import forms

class URLDataForm(forms.Form):
	EnterURL=forms.CharField(label='Enter Your URL ', max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Shorten URL Here'}))

class TestForm(forms.Form):
	name=forms.CharField(label='Enter Name ', max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
	age = forms.IntegerField()
	dob = forms.DateField()