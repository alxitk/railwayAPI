from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from stations.models import Station
from stations.serializers import StationSerializer


class StationViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
