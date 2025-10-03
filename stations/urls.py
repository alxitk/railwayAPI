from django.urls import path, include
from rest_framework import routers

from stations.views import StationViewSet

app_name = "stations"

router = routers.DefaultRouter()
router.register("stations", StationViewSet)


urlpatterns = [path("", include(router.urls))]