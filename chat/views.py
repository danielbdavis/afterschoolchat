import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
import haikunator
from .models import Room
from .models import Message
from .permissions import IsStaffOrTargetUser
from .serializers import RoomSerializer
from .serializers import MessageSerializer
from .serializers import UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()),
    
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# @api_view(['POST'])
# def create_auth(request):
#     serialized = UserSerializer(data=request.DATA)
#     if serialized.is_valid():
#         User.objects.create_user(
#             serialized.init_data['email'],
#             serialized.init_data['username'],
#             serialized.init_data['password']
#         )
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    

def about(request):
    return render(request, "chat/about.html")

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)

def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
