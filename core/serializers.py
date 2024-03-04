from rest_framework import serializers
from core.models import ListApp, Prefdefinelist, SocialPost
from django.contrib.auth import get_user_model

User = get_user_model()


class ListSerailizer(serializers.ModelSerializer):
    
    class Meta:
        model = ListApp
        fields = ['title', 'description', 'image_a', 'image_b', 'mark_as_completed', 'date_created']

class PrelistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Prefdefinelist
        fields = ['title', 'description', 'image_a', 'image_b']

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SocialPost
        fields = ['description','image_a', 'image_b']