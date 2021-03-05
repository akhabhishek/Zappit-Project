from rest_framework import serializers
from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    # Make the posted_by field Read-only
    posted_by = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'posted_by', 'created']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
