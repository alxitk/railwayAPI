from django.db.models import F, Count
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from stations.models import Station, Crew, TrainType, Train, Route, Journey, Ticket, Order
from stations.permissions import IsAdminOrIfAuthenticatedReadOnly
from stations.serializers import StationSerializer, CrewSerializer, TrainTypeSerializer, TrainSerializer, \
    RouteSerializer, JourneyListSerializer, JourneyDetailSerializer, JourneySerializer, TicketSerializer, \
    OrderSerializer, OrderListSerializer, TrainImageSerializer


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
    queryset = Train.objects.all().select_related("train_type")
    serializer_class = TrainSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = self.get_serializer(instance=train, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Train.objects.all().select_related("train_type")
        train_type = self.request.query_params.get("train_type")

        if train_type:
            train_type_ids = [int(str_id) for str_id in train_type.split(",")]
            queryset = queryset.filter(train_type__id__in=train_type_ids)

        return queryset

    def get_serializer_class(self):

        if self.action == "upload_image":
            return TrainImageSerializer

        return TrainSerializer


class RouteViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,):
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = Route.objects.all()

    def get_queryset(self):
        queryset = Route.objects.all().select_related("source", "destination")
        sources = self.request.query_params.get("source")

        if sources:
            source_ids = [int(str_id) for str_id in sources.split(",")]
            queryset = queryset.filter(source__id__in=source_ids)

        return queryset


class JourneyViewSet(ModelViewSet):
    queryset = Journey.objects.select_related(
        "train__train_type",
        "route__source",
        "route__destination"
    ).prefetch_related(
        "crew"
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related("train")
                .annotate(tickets_available=F("train__places_in_cargo") - Count("tickets"))
            ).order_by("id")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all().select_related("journey", "order")
    serializer_class = TicketSerializer


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericViewSet,):
    queryset = Order.objects.all().select_related("user")
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


