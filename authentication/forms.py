import re

from django import forms
from django.forms import ModelForm

from authentication.models import Guest, User


class GuestForm(ModelForm):
    email = forms.CharField(label="", widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }))
    phone_number = forms.CharField(label="", max_length=15, min_length=10,widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
            }))
    first_name = forms.CharField(max_length=150, label="", widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }))
    last_name = forms.CharField(max_length=150, label="", widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }))
    next_of_kin_number = forms.CharField(label="", max_length=15, min_length=10, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Next of kin phone',
            }))

    class Meta:
        model = Guest
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'next_of_kin_number']

    # def clean_first_name(self):
    #     first_name = self.cleaned_data['first_name']
    #     if not re.search(r'^\[a-zA-Z]+$', first_name):
    #         raise forms.ValidationError('First name can only contain alphabetic characthers')
    #
    # def clean_last_name(self):
    #     last_name = self.cleaned_data['last_name']
    #     if not re.search(r'^\[a-zA-Z]+$', last_name):
    #         raise forms.ValidationError('Last name can only contain alphabetic characthers')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = User.objects.get(email=email)
            if user:
                raise forms.ValidationError('A user with this email already exists. Try another...!')
        except User.DoesNotExist:
            return email 

# I need to work on the create guest form and view.