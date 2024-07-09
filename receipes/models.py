from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    cooking_time = models.IntegerField()  # in minutes
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'Comment by {self.author} on {self.recipe}'
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return f'Rating of {self.score} by {self.author} on {self.recipe}'


class RecipeCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(Recipe, related_name='collections')

    def __str__(self):
        return self.name
