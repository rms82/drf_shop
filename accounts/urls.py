from django.urls import path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register("profile", viewset=views.ProfileViewSet, basename="profile")


urlpatterns = [
    path("register", views.RegisterView.as_view(), name="email"),
    path("activate/<str:token>", views.EmailView.as_view(), name="email"),

    # JWT
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


]
urlpatterns += router.urls
