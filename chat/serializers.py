from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message
from .models import Room

class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Message
        fields = (
            'id',
            'room',
            'handle',
            'message',
            'timestamp',
            'owner')

class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'label',
            'owner')
            
class UserSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Message.objects.all())
    rooms = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Room.objects.all())
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'messages',
            'rooms',
            'password')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
        
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user