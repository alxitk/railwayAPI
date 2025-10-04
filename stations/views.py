from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from stations.models import Station, Crew, TrainType
from stations.permissions import IsAdminOrIfAuthenticatedReadOnly
from stations.serializers import StationSerializer, CrewSerializer, TrainTypeSerializer


class StationViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CrewViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class TrainTypeViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
