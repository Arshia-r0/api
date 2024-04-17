from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from blogApi.models import Post, Comment
from blogApi.serializers import PostSerializer, CommentSerializer
from blogApi.permissions import GeneralObjectPermissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(isDeleted=False).order_by('-postDate')
    serializer_class = PostSerializer
    permission_classes = [GeneralObjectPermissions]
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(isDeleted=False)
    serializer_class = CommentSerializer
    permission_classes = [GeneralObjectPermissions]
    pagination_class = PageNumberPagination
