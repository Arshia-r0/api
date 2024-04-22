from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from blogApi.models import *
from blogApi.serializers import *
from blogApi.permissions import *


class PostCommentViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']
    permission_classes = [PostCommentObjectPermissions]

    def update(self, request, *args, **kwargs):
        change = False
        obj = self.get_object()
        # edit
        if request.data.get('edit', 0):
            if obj.author == request.user:
                if isinstance(obj, Post):
                    if request.data.get('title', 0):
                        title = request.data.get('title', 0)
                        obj.title = title
                        change = True
                if request.data.get('content', 0):
                    content = request.data.get('content', 0)
                    obj.content = content
                    change = True
            else:
                raise PermissionDenied
        # vote
        vote = request.data.get('vote', None)
        if vote is not None:
            if str(vote) in ['-1', '0', '1']:
                vote_obj = PostVote if isinstance(obj, Post) else CommentVote
                user = UserProfile.objects.get(user=request.user)
                try:
                    vote_instance = vote_obj.objects.get(vote_for=obj, user=user)
                    vote_instance.vote = vote
                except vote_obj.DoesNotExist:
                    vote_instance = vote_obj(vote_for=obj, user=user, vote=vote)
                vote_instance.save()
                self.update_vote_count(obj, vote_obj)
                change = True
        # return
        if change:
            obj.save()
            return Response(self.get_serializer(obj).data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update_vote_count(self, obj, vote_obj):
        obj.likes = vote_obj.objects.filter(vote_for=obj, vote=1).count()
        obj.dislikes = vote_obj.objects.filter(vote_for=obj, vote=-1).count()
        obj.save()


class PostViewSet(PostCommentViewSet):
    queryset = Post.objects.filter(isDeleted=False).order_by('-postDate')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(PostCommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(isDeleted=False, post=self.kwargs['pid']).order_by('-postDate')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['pid'], isDeleted=False)
        serializer.save(author=self.request.user, post=post)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserPermissions]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'options']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(isDeleted=False)

    def get_serializer_class(self, *args, **kwargs):
        superuser = self.request.user.is_superuser
        authenticated = self.request.user.is_authenticated
        is_self = self.request.user == self.get_object().user
        follower = self.request.user in self.get_object().followers.all()
        if superuser or (authenticated and (is_self or follower)):
            return FullUserProfileSerializer
        return BaseUserProfileSerializer
