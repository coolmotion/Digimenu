from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from main.models import Profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'block w-full mb-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'block w-full mb-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'block w-full mb-2 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'block w-full rounded-md border-0 mb-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = 'Username'
		self.fields['username'].help_text = '<span class="text-left text-xs text-gray-500"><Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'

		self.fields['password1'].widget.attrs['class'] = 'block w-full rounded-md border-0 mb-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = 'Password'
		self.fields['password1'].help_text = '<ul class="text-left text-xs text-gray-500"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'block w-full rounded-md border-0 mb-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = 'Confirm Password'
		self.fields['password2'].help_text = '<span class="text-center text-sm text-gray-500"><br>Enter the same password as before, for verification.</span>'

		if self.errors.get('password2'):
                  self.errors['password'] = self.errors.pop('password2')
