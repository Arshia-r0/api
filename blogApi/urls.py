from django.urls import path
from rest_framework.routers import DefaultRouter

from blogApi.views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register(r'post/(?P<pid>\d+)/comment', CommentViewSet, basename='comment')
urlpatterns = router.urls
