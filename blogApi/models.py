from django.contrib.auth.models import User
from django.db import models
from rules.contrib.models import RulesModel


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    postDate = models.DateTimeField(auto_now_add=True)
    editedDate = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    postDate = models.DateTimeField(auto_now_add=True)
    editedDate = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class UserProfile(models.Model):
    following = models.ManyToManyField(User, related_name='following', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    postLikes = models.ManyToManyField(Post, related_name='postLikes', blank=True)
    postDislikes = models.ManyToManyField(Post, related_name='postDislikes', blank=True)
    commentLikes = models.ManyToManyField(Comment, related_name='commentLikes', blank=True)
    commentDislikes = models.ManyToManyField(Comment, related_name='commentDislikes', blank=True)
    isPrivate = models.BooleanField(default=False)
