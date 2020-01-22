from django.shortcuts import render
from .models import Post
from .serializer import PostSerializer
from rest_framework import viewsets, permissions

# @action 처리
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS 
            return True
        return obj.owner_id == request.user.id

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

@action(detail=True, renderer_classes = [renderers.StaticHTMLRenderer])

def highlight(self, request, *args, **kwargs):
    return HttpResponse("얍?")
        
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


