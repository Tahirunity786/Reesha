from rest_framework import serializers
from core.models import ListApp
from django.contrib.auth import get_user_model

User = get_user_model()


class ListSerailizer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ListApp
        fields = '__all__'