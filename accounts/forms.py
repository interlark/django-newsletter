from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fio_name', 'gender', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'fio_name', 'gender', ]
