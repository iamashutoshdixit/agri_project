# django imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# app imports
from .models import Config
from .serializers import ConfigSerializer


@api_view(["get"])
def get_config(request):
    """
    get api for the config
    """
    queryset = Config.objects.all()
    query_params = request.GET.get("key", None)
    resultset = []
    if query_params is None:
        resultset = queryset
    else:
        keys = query_params.split(",")
        for key in keys:
            filtered = queryset.filter(key__iexact=key)
            if len(filtered) > 0:
                resultset.append(*filtered)
    serializer = ConfigSerializer(resultset, many=True)
    if len(serializer.data) == 1:
        return Response(serializer.data[0])
    return Response(serializer.data)
