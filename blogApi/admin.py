from django.contrib import admin

from blogApi.models import *


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostVote)
admin.site.register(CommentVote)
