from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    t_email = 'Email '
    t_fname = 'Nama Depan '
    t_lname = 'Nama Belakang '
    t_password1 = 'Password '
    t_password2 = 'Konfirmasi Password '
    
    email = forms.EmailField(max_length=64, label=_(t_email), widget=forms.TextInput(attrs={'placeholder': t_email}))
    # email = forms.CharField(max_length=64, label=_(t_email), widget=forms.TextInput(attrs={'placeholder': t_email}))

    first_name = forms.CharField(max_length=32, label=_(t_fname), widget=forms.TextInput(attrs={'placeholder': t_fname}))
    last_name = forms.CharField(max_length=32, label=_(t_lname), required=False, widget=forms.TextInput(attrs={'placeholder': t_lname}))
    password1 = forms.CharField(max_length=64, label=_(t_password1), widget=forms.PasswordInput(attrs={'placeholder': t_password1}))
    password2 = forms.CharField(max_length=64, label=_(t_password2), widget=forms.PasswordInput(attrs={'placeholder': t_password2}))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['hp'].widget.attrs['placeholder'] = 'No. HP'

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'hp', 'password1', 'password2')


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.size
    # filesize = 10*1024*1024 #FOR DEBUG
    megabyte_limit = models.IMAGE_SIZE_LIMIT
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class KonfirmasiPembayaranForm(forms.ModelForm):
    # img_field = forms.ImageField(label='', validators=[validate_image])
    class Meta:
        model = models.Order
        fields = ('bukti_pembayaran',)
