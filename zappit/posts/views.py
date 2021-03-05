from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from django.views.generic import TemplateView
from rest_framework.exceptions import ValidationError


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


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # The query set must return only the particular vote of the logged in user
    # for a particular post.
    def get_queryset(self):
        user = self.request.user
        # Fetch the correct post using the pk that is passed in the url for voting
        post = Post.objects.get(pk=self.kwargs['pk'])

        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        # Check if user has already voted by checking if queryset returned anything
        if self.get_queryset().exists():
            raise ValidationError("You have already voted for this post :)")
        serializer.save(voter=self.request.user, post = Post.objects.get(pk=self.kwargs['pk']))
