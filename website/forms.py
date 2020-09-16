from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.utils.translation import ugettext as _


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    t_email = 'Email'
    t_fname = 'Nama depan'
    t_lname = 'Nama belakang'
    t_password1 = 'Password'
    t_password2 = 'Konfirmasi password'
    # 
    # email = forms.EmailField(max_length=64, label=_(t_email), widget=forms.TextInput(attrs={'placeholder': t_email}))
    # DEBUG MODE
    email = forms.CharField(max_length=64, label=_(t_email), widget=forms.TextInput(attrs={'placeholder': t_email}))
    first_name = forms.CharField(max_length=32, label=_(t_fname), widget=forms.TextInput(attrs={'placeholder': t_fname}))
    last_name = forms.CharField(max_length=32, label=_(t_lname), required=False, widget=forms.TextInput(attrs={'placeholder': t_lname}))
    password1 = forms.CharField(max_length=64, label=_(t_password1), widget=forms.TextInput(attrs={'type':'password', 'placeholder': t_password1}))
    password2 = forms.CharField(max_length=64, label=_(t_password2), widget=forms.TextInput(attrs={'type':'password', 'placeholder': t_password2}))

    class Meta:
        # model = User
        model = models.User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )