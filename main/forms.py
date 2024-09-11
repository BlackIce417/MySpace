from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
			'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(MyUserCreationForm, self).__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

class UserProfileModelForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['bio', 'avatar']


