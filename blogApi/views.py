from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from blogApi.models import Post, Comment, UserProfile
from blogApi.serializers import PostSerializer, CommentSerializer
from blogApi.permissions import PostCommentObjectPermissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(isDeleted=False).order_by('-postDate')
    serializer_class = PostSerializer
    permission_classes = [PostCommentObjectPermissions]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [PostCommentObjectPermissions]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Comment.objects.filter(isDeleted=False, post=self.kwargs['pid']).order_by('-postDate')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pid'], isDeleted=False)
        serializer.save(author=self.request.user, post=post)

# user subs
