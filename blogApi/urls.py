from rest_framework.routers import DefaultRouter

from blogApi.views import *


router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register(r'post/(?P<pid>\d+)/comment', CommentViewSet, basename='comment')
router.register('user', UserViewSet, basename='user')
urlpatterns = router.urls
