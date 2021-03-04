from django.shortcuts import render
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from django.views.generic import TemplateView


# Create your views here.
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class IndexView(TemplateView):
    template_name = "posts/index.html"
