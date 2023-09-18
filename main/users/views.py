# python imports
import json

# django imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets

# user imports
from libs.paginations import CustomCursorPagination
from .models import User
from .serializers import UserSerializer


class CustomAuthToken(ObtainAuthToken):
    """
    custom auth token verification
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response("400", status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
            }
        )


@api_view(["get"])
@permission_classes((IsAuthenticated,))
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["get"]


@api_view(["get", "post"])
def camera_access(request):
    context = json.loads(request.body)
    status = "0"
    if context["token"] == "abcd":
        status = "1"
    return Response({"Status": status})
