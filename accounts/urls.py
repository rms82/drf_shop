from django.urls import path


from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = routers.DefaultRouter()
router.register("profile", viewset=views.ProfileViewSet, basename="profile")


urlpatterns = [
    path("register", views.RegisterView.as_view(), name="email"),
    path("activate/<str:token>", views.EmailActivationView.as_view(), name="email"),
    
    # JWT
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # PASSWORD
    path('profile/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', views.PasswordResetRequestJWTView.as_view(), name='forgot_password'),
    path('forgot_password/confirm/', views.PasswordResetConfirmView.as_view(), name='forgot_password_confirm'),

    # Email
    path('send_mail', views.SendEmailView.as_view(), name='send_mail')
]

urlpatterns += router.urls
