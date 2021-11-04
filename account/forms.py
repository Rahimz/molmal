from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'),
    widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_("Passwords don\'t match."))
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'photo')

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'fav_address']
