# django imports
from rest_framework import routers

# app imports
from . import views

router = routers.DefaultRouter()


router.register(r"batch", views.BatchViewSet)
router.register(r"plant-analysis", views.PlantAnalysisViewSet)

router.register(r"specimen/specimen", views.SpecimenViewSet)
router.register(r"specimen/health", views.NurseryHealthViewSet)
router.register(r"specimen/growth", views.VegetativeGrowthViewSet)
router.register(r"specimen/flowering", views.ReproductiveGrowthViewSet)
router.register(r"specimen/output", views.SpecimenOutputViewSet)
router.register(r"specimen/lad", views.LeafAreaDetectionViewSet)

router.register(r"dome/pollination", views.PollinationViewSet)
router.register(r"dome/harvesting", views.HarvestingViewSet)
router.register(r"dome/harvesting-sample", views.HarvestingSampleViewSet)
router.register(r"dome/root-weight", views.RootWeightViewSet)
router.register(r"dome/leaf-temperature", views.LeafTemperatureViewSet)
router.register(
    r"dome/root-zone-temperature",
    views.RootZoneTemperatureViewSet,
)

router.register(r"climate/outside", views.OutsideParametersViewSet)
router.register(r"climate/dome", views.DomeParametersViewSet)
router.register(r"climate/controller", views.ControllerViewSet)

router.register(r"irrigation/outer-tank", views.OuterWaterTankViewSet)
router.register(r"irrigation/inner-tank", views.InnerWaterTankViewSet)
router.register(r"irrigation/cooling-pad", views.CoolingPadViewSet)

urlpatterns = [
    # path("influx-data", views.get_data_from_influxdb),
    *router.urls,
]
