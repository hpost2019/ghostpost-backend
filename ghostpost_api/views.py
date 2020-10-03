from django.shortcuts import render
from .serializers import PostsSerializer
from .models import Posts
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.db.models import F


class PostsViewSets(viewsets.ModelViewSet):

    """Default action data"""
    queryset = Posts.objects.order_by('-post_date')
    serializer_class = PostsSerializer

    @action(detail=False)
    def boasts_only(self, request):
        boasts = Posts.objects.filter(boast=True).order_by('-post_date')
        page = self.paginate_queryset(boasts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)

        serializer = self.get_serializer(boasts, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def roasts_only(self, request):
        roasts = Posts.objects.filter(boast=False).order_by('-post_date')
        page = self.paginate_queryset(roasts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(roasts, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def score_sort(self, request):
        scores = Posts.objects.order_by(-(F('up_votes') - F('down_votes')))
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def up_vote(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        post.up_votes = F('up_votes') + 1
        post.save()
        return Response({'status': 'upvote set'})

    @action(detail=True, methods=['post'])
    def down_vote(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        post.down_votes = F('down_votes') + 1
        post.save()
        return Response({'status': 'downvote set'})

    def create(self, request):
        post_data = JSONParser().parse(request)
        print(post_data)
        post_serializer = PostsSerializer(data=post_data['data'])
        print(post_serializer)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({'status': 'Success'})
        return Response({'status': 'Failure'})
