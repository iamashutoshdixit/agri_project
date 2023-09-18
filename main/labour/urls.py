# django imports
from django.urls import include, path
from rest_framework import routers

# user imports
from . import views

router = routers.DefaultRouter()

router.register(r"work", views.WorkViewSet)
router.register(r"labours", views.LabourViewSet)
router.register(r"attendance", views.AttendanceViewSet)

urlpatterns = [
    path("mark-inactive/", views.mark_labours_inactive),
    *router.urls,
]
