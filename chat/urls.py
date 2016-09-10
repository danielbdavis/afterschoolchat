from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    url(r'^$',  views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
