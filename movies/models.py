from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Platform(models.Model):
    """Platform in which movies will be hosted"""
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=255)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie Model"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='movie')
    is_active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=255, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " + self.movie.name
