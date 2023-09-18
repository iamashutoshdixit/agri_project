# python imports

import threading
import uuid

# django imports

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# project imports
from libs.paginations import CustomCursorPagination

# app imports
from .helpers import uploader
from .models import (
    Farm,
    VisitorEntry,
    IssueTracker,
    Camera,
    IOTBox,
    FarmManagerAttendance,
)
from .serializers import (
    FarmSerializer,
    VisitorEntrySerializer,
    IssueTrackerSerializer,
    FarmManagerAttendanceSerializer,
    CameraSerializer,
    IOTBoxSerializer,
)


class FarmManagerAttendanceViewSet(viewsets.ModelViewSet):
    queryset = FarmManagerAttendance.objects.all()
    serializer_class = FarmManagerAttendanceSerializer
    http_method_names = ["post", "get"]
    pagination_class = CustomCursorPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FarmManagerAttendance.objects.filter(
            user=self.request.user,
        )

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(FarmManagerAttendanceViewSet, self).get_serializer(
            *args,
            **kwargs,
        )


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.filter(is_active=True)
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["get"]

    # @method_decorator(cache_page(60 * 60))
    # @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        farms = request.user.farms.filter(is_active=True)
        sno = request.GET.get("sno")
        if sno:
            box = IOTBox.objects.filter(serial_number=sno).first()
            if box is not None:
                farms = [box.farm]
        serializer = FarmSerializer(farms, many=True)
        return Response(serializer.data)

    # @method_decorator(cache_page(60 * 60))
    # @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, **kwargs):
        return super().retrieve(request, **kwargs)


class VisitorEntryViewSet(viewsets.ModelViewSet):
    queryset = VisitorEntry.objects.all()
    serializer_class = VisitorEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["post", "get"]


class IssueTrackerViewSet(viewsets.ModelViewSet):
    queryset = IssueTracker.objects.all()
    serializer_class = IssueTrackerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["post", "get"]


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.filter(is_active=True)
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


class IOTBoxViewSet(viewsets.ModelViewSet):
    queryset = IOTBox.objects.all()
    serializer_class = IOTBoxSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]


@api_view(["POST"])
def upload_image(request):
    BUCKET = settings.AWS_S3_BUCKET
    REGION = settings.AWS_REGION
    file = request.data.get("file", None)
    filename = f"{uuid.uuid4()}.webp"
    if not file:
        return HttpResponse(
            "400 Bad Request",
            status=status.HTTP_400_BAD_REQUEST,
        )
    t = threading.Thread(target=uploader, args=(file.read(), filename))
    t.start()
    s3_url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com"
    return Response(
        {
            "filename": filename,
            "url": f"{s3_url}/eeki-images/{filename}",
        }
    )


def show_camera_streams(request, farm_id):
    css_url = settings.CSS_URL
    cameras = Camera.objects.filter(farm=farm_id).select_related("farm")
    context = {"cameras": cameras, "css_url": css_url}
    return render(request, "farms/cameras.html", context=context)
