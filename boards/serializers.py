from rest_framework import serializers
from .models import Board, Topic


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('url', 'id', 'name', 'description')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'board', 'starter', 'views')


