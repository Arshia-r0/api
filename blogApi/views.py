from django.shortcuts import get_object_or_404

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [GeneralObjectPermissions]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Comment.objects.filter(isDeleted=False, post=self.kwargs['pid']).order_by('-postDate')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pid'], isDeleted=False)
        serializer.save(author=self.request.user, post=post)

# todo: voting api
# user subs
