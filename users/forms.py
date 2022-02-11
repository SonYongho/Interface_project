from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username", "email")

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['address','avatar', 'phone', 'Mobile', 'Git_url', 'Twit_url', 'Ins_url', 'face_url']