from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
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


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Check to ensure users can delete only their posts
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(posted_by=self.request.user, pk=self.kwargs['pk'])
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("You are not allowed to delete this post!")


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
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

    def delete(self, request, *args, **kwargs):
        # Check if user has voted and then delete the vote
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("You never voted for this post!")
