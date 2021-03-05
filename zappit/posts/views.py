from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "posts/index.html" # Django will look for this template name


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override the function that saves the data posted by user to the database
    def perform_create(self, serializer):
        # While saving, we assign posted_by to the user who sent the POST request
        serializer.save(posted_by=self.request.user)
