from django.shortcuts import render
from recipes.models import Recipe
from recipes.models import Author


def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, 'welcome_name': 'se-9'})

def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_view(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    return render(request, "author.html", {"author": my_title})


# Create your views here.
