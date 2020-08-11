from django import forms
from recipes.models import Author, Recipe

class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields=['title', 'author','description','time_required','instructions']
