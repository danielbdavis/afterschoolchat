from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message
from .models import Room


class MessageSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Message
        fields = (
            'id',
            'room',
            'handle',
            'message',
            'timestamp')


class RoomSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    
    # members = serializers.ReadOnlyField()
    members = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=User.objects.all())

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'label',
            'members')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',)
