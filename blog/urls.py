from django.urls import path

from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')

urlpatterns = router.urls
