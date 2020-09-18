from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import HttpResponseForbidden
from recipes.models import Recipe
from recipes.models import Author
from recipes.forms import AddRecipeForm, AddAuthorForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.admin.views.decorators import staff_member_required
from django import forms


def index(request):
    my_title = Recipe.objects.all()
    return render(request, "index.html", {"title": my_title, 'welcome_name': 'se-9'})

def recipe_detail(request, recipe_id):
    my_title = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_title})

def author_view(request, author_id):
    my_title = Author.objects.filter(id=author_id).first()
    return render(request, "author.html", {"author": my_title})

@login_required
# @staff_member_required
def add_author(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get('username'), password=data.get('password'))  
                Author.objects.create(
                    name=data.get('username'),
                    bio=data.get('bio'),
                    user=new_user
                )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        return HttpResponseForbidden("This action is forbidden")
    form = AddAuthorForm()
    return render(request, "generic_form.html", {'form': form})

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        if request.user.is_staff:
            staff_auth=data.get('author')
        else:
            staff_auth=request.user.author
            Recipe.objects.create(
                title=data.get('title'),
                time_required=data.get('time_required'),
                description=data.get('description'),
                instructions=data.get('instructions'),
                author=request.user.author,
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddRecipeForm()
    return render(request, "generic_form.html", {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    form = None
    edit = Recipe.objects.get(id=recipe_id)
    data = {"title": edit.title, "description": edit.description, "time_required": edit.time_required, "instructions": edit.instructions, "author": edit.author}
    if request.user.is_staff or request.user.username == edit.author.name:
        if request.method == "POST":
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                edit.title = data["title"]
                edit.description = data["description"]
                edit.time_required = data["time_required"]
                edit.instructions = data["instructions"]
                edit.author = data["author"]
                edit.save()
                return redirect("recipe", edit.pk)
        else:
            form = AddRecipeForm(initial=data)
            return render(request, "generic_form.html", {'form':form})
    else:
        return HttpResponseRedirect(reverse('homepage'))
    #need to figure out how to put edit into urls and recipedetail.html

def favorite_view(request, favorite_id):
    current_author = Author.objects.get(user__username=request.user.username)
    current_author.favorite.add(Recipe.objects.get(id=favorite_id))
    current_author.save()
    return HttpResponseRedirect(reverse('homepage'))


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
    form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))