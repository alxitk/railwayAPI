from django.urls import path, include
from rest_framework import routers

from stations.models import Journey
from stations.views import StationViewSet, CrewViewSet, TrainTypeViewSet, TrainViewSet, RouteViewSet, JourneyViewSet

app_name = "stations"

router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("routes", RouteViewSet)
router.register("journeys", JourneyViewSet)


urlpatterns = [path("", include(router.urls))]
