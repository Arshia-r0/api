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

    @action(methods=['GET'], detail=True, permission_classes=[PostCommentObjectPermissions])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk, isDeleted=False)
        user = UserProfile.objects.get(user=request.user)
        if post in user.postLikes.all():
            user.postLikes.remove(post)
            post.likes -= 1
        else:
            user.postLikes.add(post)
            post.likes += 1
        user.save()
        post.save()
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


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
