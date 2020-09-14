from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
Author model:
Name (CharField)
Bio (TextField)
Recipe Model:
Title (CharField)
Author (ForeignKey)
Description (TextField)
Time Required (Charfield) (for example, "One hour")
Instructions (TextField)
"""

class Author(models.Model):
    name = models.CharField(max_length=80, null=True)
    bio = models.TextField(max_length=80, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=80, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=50, null=True)
    instructions = models.TextField()
    

    def __str__(self):
        return f"{self.title} - {self.author.name}"


class Favorites(models.Model):
    person = models.ForeignKey(Author, on_delete=models.CASCADE )
    food = models.ForeignKey(Recipe, on_delete=models.CASCADE )