from rest_framework import routers

# app imports
from . import views

router = routers.DefaultRouter()

router.register(r"reimbursement", views.ReimbursementViewSet)

urlpatterns = [
    *router.urls,
]
