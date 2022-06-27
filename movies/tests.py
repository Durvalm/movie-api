from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .api import serializers
from . import models


class PlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = models.Platform.objects.create(name="Netflix",
                                                       about="#1 Platform", website="https://www.netflix.com")

    def test_platform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('platform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_platform_list(self):
        response = self.client.get(reverse('platform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_platform_ind(self):
        response = self.client.get(reverse('platform-detail', args=(self.platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = models.Platform.objects.create(name="Netflix",
                                                       about="#1 Platform", website="https://www.netflix.com")
        self.movie = models.Movie.objects.create(platform=self.platform, name="Example Movie",
                                                 description="Example Movie", is_active=True)

    def test_movie_create(self):
        data = {
            "platform": self.platform,
            "title": "Example Movie",
            "storyline": "Example Story",
            "is_active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movie_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Movie.objects.count(), 1)
        self.assertEqual(models.Movie.objects.get().name, 'Example Movie')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = models.Platform.objects.create(name="Netflix",
                                                       about="#1 Platform", website="https://www.netflix.com")
        self.movie = models.Movie.objects.create(platform=self.platform, name="Example Movie",
                                                 description="Example Movie", is_active=True)
        self.movie2 = models.Movie.objects.create(platform=self.platform, name="Example Movie",
                                                  description="Example Movie", is_active=True)
        self.review = models.Review.objects.create(user=self.user, rating=5, description="Great Movie",
                                                   movie=self.movie2, is_active=True)

    def test_review_create(self):
        data = {
            "user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "movie": self.movie,
            "is_active": True
        }

        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "movie": self.movie,
            "is_active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "user": self.user,
            "rating": 4,
            "description": "Great Movie! - Updated",
            "movie": self.movie,
            "is_active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

