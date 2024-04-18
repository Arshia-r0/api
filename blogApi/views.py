from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from blogApi.models import Post, Comment, UserProfile, PostVote, CommentVote
from blogApi.serializers import PostSerializer, CommentSerializer
from blogApi.permissions import PostCommentObjectPermissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(isDeleted=False).order_by('-postDate')
    serializer_class = PostSerializer
    permission_classes = [PostCommentObjectPermissions]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        vote = request.data['vote']
        if vote in [-1, 0, 1]:
            post = self.get_object()
            user = UserProfile.objects.get(user=request.user)
            vote_obj = PostVote(post=post, user=user, vote=vote)
            vote_obj.save()
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [PostCommentObjectPermissions]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_queryset(self):
        return Comment.objects.filter(isDeleted=False, post=self.kwargs['pid']).order_by('-postDate')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pid'], isDeleted=False)
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        vote = request.data['vote']
        if vote in [-1, 0, 1]:
            comment = self.get_object()
            user = UserProfile.objects.get(user=request.user)
            vote_obj = CommentVote(comment=comment, user=user, vote=vote)
            vote_obj.save()
            return Response(CommentSerializer(Comment).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# user subs
