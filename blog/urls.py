from django.urls import path

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')
router.register('blog_category', views.CategoryViewSet, basename='blog_category')

post_router = NestedDefaultRouter(router, 'post', lookup='post')
post_router.register('comments', viewset=views.PostCommentViewSet, basename='comments')

urlpatterns = [
    path('post/<int:pk>/like/', views.LikeView.as_view(), name='post_like'),
]


urlpatterns += router.urls + post_router.urls
