from django.urls import path
from movies.api import views

urlpatterns = [
    path('movie/', views.MovieList.as_view(), name='movie-list'),
    path('movie/<int:pk>/', views.MovieDetail.as_view(), name='movie-detail'),
    path('platform/', views.PlatformList.as_view(), name='platform-list'),
    path('platform/<int:pk>/', views.PlatformDetail.as_view(), name='platform-detail'),
    path('movie/<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('movie/reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('movie/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),

]
