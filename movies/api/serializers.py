from rest_framework import serializers
from movies.models import Movie, Platform, Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ['movie']


class MovieSerializer(serializers.ModelSerializer):
    review = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"


class PlatformSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Platform
        fields = "__all__"
