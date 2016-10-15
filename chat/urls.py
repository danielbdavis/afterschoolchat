from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers
from .views import RoomViewSet
from .views import MessageViewSet
from .views import UserViewSet
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'users', UserViewSet)
# router.register(r'accounts', views.UserView, 'list')

urlpatterns = [
    url(r'^', include(router.urls)),

    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    
    # these are the django-registation urls
    url(r'^accounts/', include('registration.backends.simple.urls')),
    
    # these are from django-rest-auth
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),    
    
    
    url(r'^$',  views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
