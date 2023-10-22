from django.urls import path

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')

post_router = NestedDefaultRouter(router, 'post', lookup='post')
post_router.register('comments', viewset=views.PostCommentViewSet, basename='comments')

urlpatterns = router.urls + post_router.urls
