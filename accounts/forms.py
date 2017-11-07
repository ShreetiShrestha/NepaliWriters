from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import *




class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    bio = forms.Textarea()
    location = forms.CharField(max_length=30)
    birth_date = forms.DateField()
    profile_pic = forms.ImageField()
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','bio','location','birth_date', 'profile_pic', )

class PostToReviewForm(forms.ModelForm):
    caption = forms.CharField(max_length=30, required=False, help_text='Optional.')
    class Meta:
        model=PostToReview
        fields = ('title','caption','author','description','image','category',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = ('name','category_image')
