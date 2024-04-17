from django.contrib import admin

from blogApi.models import Post,Comment, UserProfile


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
