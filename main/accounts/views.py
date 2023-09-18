# django imports
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from libs.paginations import CustomCursorPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

# user imports
from .models import Reimbursement

from .serializers import ReimbursementSerializer


class ReimbursementViewSet(viewsets.ModelViewSet):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["post", "get"]

    def list(self, request):
        paginator = self.pagination_class()
        paginator.page_size = 10
        queryset = self.queryset.filter(created_by=self.request.user)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": self.request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
