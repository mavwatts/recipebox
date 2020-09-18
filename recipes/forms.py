from django import forms
from django.forms import ModelForm
from recipes.models import Author, Recipe

class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields=['title','description','time_required','instructions', 'author']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
