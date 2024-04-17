from rest_framework import serializers

from blogApi.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['isDeleted']
        read_only_fields = ['id', 'author',
            'postDate', 'editedDate', 'likes', 'dislikes']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['isDeleted']
        read_only_fields = ['id', 'author', 'post',
            'postDate', 'editedDate', 'likes', 'dislikes']