from knox import views as knox_views
from .views import *
from django.urls import path, include

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"verify-otp", OTPView, basename="verify-otp")
# router.register(r'user-info', UserInfoView, basename='user-info')

urlpatterns = [
    path(r"login/", LoginView.as_view(), name="knox_login"),
    path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path("", include(router.urls)),
    path("user-info/<str:email>", UserInfoView.as_view({"get": "getInfo"})),
    path("isValid", CheckAuth.as_view({"get": "isValid"})),
]
