from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from stations.models import Station, Crew, TrainType, Train, Route, Journey, Ticket
from stations.permissions import IsAdminOrIfAuthenticatedReadOnly
from stations.serializers import StationSerializer, CrewSerializer, TrainTypeSerializer, TrainSerializer, \
    RouteSerializer, JourneyListSerializer, JourneyDetailSerializer, JourneySerializer, TicketSerializer


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


class TrainViewSet(ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class JourneyViewSet(ModelViewSet):
    queryset = Journey.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
