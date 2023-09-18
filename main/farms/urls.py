# django imports
from rest_framework import routers
from django.urls import path

# app imports
from . import views

router = routers.DefaultRouter()
router.register(r"farms", views.FarmViewSet)
router.register(r"visitor-entry", views.VisitorEntryViewSet)
router.register(r"ticketing", views.IssueTrackerViewSet)
router.register(r"attendance", views.FarmManagerAttendanceViewSet)

urlpatterns = [
    path("upload-image/", views.upload_image),
    path("cameras/<int:farm_id>/", views.show_camera_streams),
    *router.urls,
]
