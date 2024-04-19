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
            try:
                vote_obj = PostVote.objects.get(post=post, user=user)
                vote_obj.vote = vote
            except PostVote.DoesNotExist:
                vote_obj = PostVote(post=post, user=user, vote=vote)
            vote_obj.save()
            self.update_vote_count(post)
            return Response(PostSerializer(post).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update_vote_count(self, post):
        post.likes = PostVote.objects.filter(post=post, vote=1).count()
        post.dislikes = PostVote.objects.filter(post=post, vote=-1).count()
        post.save()


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
            try:
                vote_obj = CommentVote.objects.get(comment=comment, user=user)
                vote_obj.vote = vote
            except CommentVote.DoesNotExist:
                vote_obj = CommentVote(comment=comment, user=user, vote=vote)
            vote_obj.save()
            self.update_vote_count(comment)
            return Response(CommentSerializer(comment).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update_vote_count(self, comment):
        comment.likes = CommentVote.objects.filter(comment=comment, vote=1).count()
        comment.dislikes = CommentVote.objects.filter(comment=comment, vote=-1).count()
        comment.save()
# user subs
