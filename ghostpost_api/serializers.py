from rest_framework import serializers
from .models import Posts


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = [
            'id',
            'boast',
            'text',
            'up_votes',
            'down_votes',
            'post_date',
            'score'
        ]
