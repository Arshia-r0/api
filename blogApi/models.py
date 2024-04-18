from django.contrib.auth.models import User
from django.db import models


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

    def delete(self, **kwargs):
        self.isDeleted = True
        self.save()


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

    def delete(self, **kwargs):
        self.isDeleted = True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Votes = models.ManyToManyField(Post, related_name='Votes', through='Votes')
    isPrivate = models.BooleanField(default=False)


class Votes(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0, choices=[(-1, 'dislike'), (0, ''), (1, 'like')])
