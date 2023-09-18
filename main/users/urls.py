# django imports
from django.urls import path
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

# app imports
from . import views

router = DefaultRouter()
# router.register(r"labours", views.LabourViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"fcm", FCMDeviceAuthorizedViewSet)

urlpatterns = [
    # path("api/manager/<str:id>", views.get_manager),
    path("login/", views.CustomAuthToken.as_view()),
    path("camera-access/", views.camera_access),
    path("profile/", views.get_user_profile),
    *router.urls,
]
