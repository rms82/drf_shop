from django.urls import path

from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet, basename="category")
router.register('product', views.ProductViewSet, basename="product")
router.register('cart', views.CartViewSet, basename="cart")

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='items')

urlpatterns = router.urls + cart_router.urls