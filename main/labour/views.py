# python imports

# django imports
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# user imports
from libs.paginations import CustomCursorPagination
from .models import Attendance, Labour, Work
from .serializers import AttendanceSerializer, LabourSerializer, WorkSerializer


class NoContentViewSet(viewsets.ModelViewSet):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class LabourViewSet(viewsets.ModelViewSet):
    queryset = Labour.objects.all()
    serializer_class = LabourSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]
    pagination_class = CustomCursorPagination

    # @method_decorator(cache_page(2 * 60 * 60))
    def list(self, request):
        paginator = CustomCursorPagination()
        paginator.page_size = 20
        farm = request.GET.get("farm", None)
        queryset = Labour.objects.filter(is_active=True)
        if farm:
            queryset = queryset.filter(farms__exact=farm)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = LabourSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(AttendanceViewSet, self).get_serializer(*args, **kwargs)

    def create(self, request):
        if not isinstance(request.data, list):
            return Response(
                {"error": "expected list of objects"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = []
        for data in request.data:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response.append(
                    {
                        "status": 200,
                        "data": serializer.data,
                    }
                )
            else:
                response.append(
                    {
                        "status": 400,
                        "data": serializer.errors,
                    }
                )
        return Response(response)


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(WorkViewSet, self).get_serializer(*args, **kwargs)


@api_view(["post"])
def mark_labours_inactive(request):
    is_list = False
    if isinstance(request.data, list):
        queryset = Labour.objects.filter(id__in=request.data)
        is_list = True
    else:
        queryset = Labour.objects.filter(id=request.data)
    queryset.update(is_active=False)
    serializer = LabourSerializer(queryset, many=is_list)
    return Response(serializer.data)
