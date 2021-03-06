from rest_framework import serializers
from .models import Board, Topic, Post, History


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('url', 'id', 'name', 'description')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'board', 'starter', 'views')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'message', 'topic', 'created_at', 'created_by', 'updated_at', 'updated_by')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('url', 'id', 'board_name', 'action', 'action_at')
