from rest_framework import serializers, status
from rest_framework.response import Response

from restaurant.serializer import RestSerializer
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """ list: user_id, restaurant_id Serializer"""

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'restaurant',
            'bookmarked_user',
        )


class UserBookMarkSerializer(serializers.ModelSerializer):
    """ 식당 정보 Serializer"""
    restaurant = RestSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = (
            'restaurant',
        )
