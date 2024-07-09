# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe,Comment,Rating,Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields=['title','ingredients','instructions','category','cooking_time','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ['text']

class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['score']


