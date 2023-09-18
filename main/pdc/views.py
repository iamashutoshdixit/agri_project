# django imports
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from farms.models import Farm
from libs.paginations import CustomCursorPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

# user imports
from farms.models import Farm
from .models import (
    Batch,
    Controller,
    CoolingPad,
    DomeParameters,
    Harvesting,
    HarvestingSample,
    InnerWaterTank,
    LeafTemperature,
    NurseryHealth,
    OuterWaterTank,
    OutsideParameters,
    PlantAnalysis,
    ReproductiveGrowth,
    Pollination,
    RootWeight,
    RootZoneTemperature,
    Specimen,
    SpecimenOutput,
    LeafAreaDetection,
    VegetativeGrowth,
)
from .serializers import (
    BatchSerializer,
    ControllerSerializer,
    CoolingPadSerializer,
    DomeParametersSerializer,
    HarvestingSerializer,
    HarvestingSampleSerializer,
    InnerWaterTankSerializer,
    LeafTemperatureSerializer,
    NurseryHealthSerializer,
    OuterWaterTankSerializer,
    OutsideParametersSerializer,
    PlantAnalysisSerializer,
    ReproductiveGrowthSerializer,
    PollinationSerializer,
    RootWeightSerializer,
    RootZoneTemperatureSerializer,
    SpecimenOutputSerializer,
    SpecimenSerializer,
    LeafAreaDetectionSerializer,
    VegetativeGrowthSerializer,
)

# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS


class NoContentViewSet(viewsets.ModelViewSet):
    """
    class to send 204 No content status on post request
    """

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SpecimenViewSet(viewsets.ModelViewSet):
    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["get", "post"]

    # @method_decorator(cache_page(60 * 15))
    # @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        paginator = self.pagination_class()
        paginator.page_size = 20
        farm = request.GET.get("farm", None)
        queryset = self.get_queryset()
        if farm:
            queryset = queryset.filter(farm__exact=farm)
        # return queryset
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        # Determine if the data is object or list of object and
        # choose serializer accordingly
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.filter(is_active=True)
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["get", "post", "patch"]

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        paginator = self.pagination_class()
        paginator.page_size = 30
        farm = request.GET.get("farm", None)
        type = request.GET.get("type", None)
        farms = request.user.farms.filter(is_active=True)
        if farm is not None:
            farms = farms.filter(id=farm)
        if type is not None and type == "all":
            queryset = self.queryset.filter()
        else:
            queryset = self.queryset.filter(
                commercial_farm__in=farms.values_list("id"), is_active=True
            )
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # api to transplant from nursery to commercial
        data = request.data
        errors = {}
        try:
            batch = Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return Response(
                {"batch": f"Batch {pk} does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )

        farm = data.get("commercial_farm", None)
        trans_date = data.get("transplantation_date", None)
        dome = data.get("dome", None)
        no_of_plants = data.get("no_of_plants", None)

        if farm is None:
            errors["commercial_farm"] = "this field is required"
        if trans_date is None:
            errors["transplantation_date"] = "this field is required"
        if dome is None:
            errors["dome"] = "this field is required"
        if no_of_plants is None:
            errors["no_of_plants"] = "this field is required"

        if errors:
            return Response(errors, status=HTTP_400_BAD_REQUEST)

        try:
            farm = Farm.objects.get(id=farm)
            if farm.type == Farm.FarmType.NURSERY:
                return Response(
                    {"commercial_farm": "must be a commercial farm"},
                )
        except Farm.DoesNotExist:
            return Response({"farm": f"farm {farm} does not exist"})

        active_batches = (
            self.get_queryset()
            .filter(
                farm=farm,
                dome=dome,
            )
            .count()
        )

        if active_batches > 0:
            return Response(
                {
                    "error": """active batches already exist for the dome in
                    this farm. mark the batches inactive before assigning."""
                },
                status=HTTP_400_BAD_REQUEST,
            )

        batch.commercial_farm = farm
        batch.transplantation_date = trans_date
        batch.dome = dome
        batch.no_of_plants = no_of_plants
        batch.save()

        serializer = BatchSerializer(batch)

        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class PlantAnalysisViewSet(NoContentViewSet):
    queryset = PlantAnalysis.objects.all()
    serializer_class = PlantAnalysisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    http_method_names = ["get", "post"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class NurseryHealthViewSet(NoContentViewSet):
    queryset = NurseryHealth.objects.all()
    serializer_class = NurseryHealthSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class VegetativeGrowthViewSet(NoContentViewSet):
    queryset = VegetativeGrowth.objects.all()
    serializer_class = VegetativeGrowthSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class ReproductiveGrowthViewSet(NoContentViewSet):
    queryset = ReproductiveGrowth.objects.all()
    serializer_class = ReproductiveGrowthSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class SpecimenOutputViewSet(NoContentViewSet):
    queryset = SpecimenOutput.objects.all()
    serializer_class = SpecimenOutputSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class PollinationViewSet(NoContentViewSet):
    queryset = Pollination.objects.all()
    serializer_class = PollinationSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class HarvestingViewSet(NoContentViewSet):
    queryset = Harvesting.objects.all()
    serializer_class = HarvestingSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class HarvestingSampleViewSet(NoContentViewSet):
    queryset = HarvestingSample.objects.all()
    serializer_class = HarvestingSampleSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class RootWeightViewSet(NoContentViewSet):
    queryset = RootWeight.objects.all()
    serializer_class = RootWeightSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class LeafTemperatureViewSet(NoContentViewSet):
    queryset = LeafTemperature.objects.all()
    serializer_class = LeafTemperatureSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class RootZoneTemperatureViewSet(NoContentViewSet):
    queryset = RootZoneTemperature.objects.all()
    serializer_class = RootZoneTemperatureSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class OutsideParametersViewSet(NoContentViewSet):
    queryset = OutsideParameters.objects.all()
    serializer_class = OutsideParametersSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class DomeParametersViewSet(NoContentViewSet):
    queryset = DomeParameters.objects.all()
    serializer_class = DomeParametersSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class ControllerViewSet(NoContentViewSet):
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class OuterWaterTankViewSet(NoContentViewSet):
    queryset = OuterWaterTank.objects.all()
    serializer_class = OuterWaterTankSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class InnerWaterTankViewSet(NoContentViewSet):
    queryset = InnerWaterTank.objects.all()
    serializer_class = InnerWaterTankSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class CoolingPadViewSet(NoContentViewSet):
    queryset = CoolingPad.objects.all()
    serializer_class = CoolingPadSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


class LeafAreaDetectionViewSet(NoContentViewSet):
    queryset = LeafAreaDetection.objects.all()
    serializer_class = LeafAreaDetectionSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)


# @api_view(["get"])
# @permission_classes([IsAuthenticated])
# def get_data_from_influxdb(request):
#     farm = request.GET.get("farm", None)
#     measurement = request.GET.get("topic", None)
#     start = request.GET.get("start", None)
#     if start is None:
#         start = "-5m"
#     stop = request.GET.get("stop", None)
#     if farm is None and measurement is None:
#         return Response(
# "Missing farm and topic",
# status=HTTP_400_BAD_REQUEST,)
#     results = {}
#     creds = {
#         "url": "http://65.1.138.124:8086",
#         "token": "f4T2hQtw4jqE619jIX4SUqTJwiMwr2z7flTKbkEz\
# V89mZ63Bdx1dm4ZPFTRlJrh3TlQbVvXEQO-r86yXLVTnqA==",
#         "org": "eekifoods",
#     }
#     bucket = "test"
#     rng = f"start: {start}, stop: {stop}" if stop else f"start: {start}"
#     with InfluxDBClient(**creds) as client:
#         query = f"""
#         from(bucket: "{bucket}")
#             |> range({rng})
#             |> filter(fn: (r) => r["farm"] == "{farm}")
#             |> filter(fn: (r) => r["_measurement"] == "{measurement}")
#         """
#         tables = client.query_api().query(query, org=creds["org"])
#         for table in tables:
#             for record in table:
#                 field = record.values.get("_field")
#                 if field not in results:
#                     results[field] = {}
#                 results[field][str(record.values.get("_time"))] =
# record.get_value()
#     return Response(results)
