from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename="category")
router.register('product', views.ProductViewSet, basename="product")


urlpatterns = router.urls