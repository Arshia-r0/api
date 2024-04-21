from rest_framework import serializers

from blogApi.models import Post, Comment, UserProfile


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


class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)
    postVotes = serializers.StringRelatedField(read_only=True,  many=True)
    commentVotes = serializers.StringRelatedField(read_only=True,  many=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'following', 'postVotes', 'commentVotes']
