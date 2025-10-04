from django.urls import path, include
from rest_framework import routers

from stations.views import StationViewSet, CrewViewSet, TrainTypeViewSet, TrainViewSet

app_name = "stations"

router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)


urlpatterns = [path("", include(router.urls))]
