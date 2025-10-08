from django.db import transaction
from django.template.defaultfilters import first
from rest_framework import serializers

from stations.models import Station, Crew, TrainType, Train, Route, Journey, Ticket, Order


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=TrainType.objects.all(),
        slug_field="name",
    )

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_number", "places_in_cargo", "train_type")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    destination = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    class Meta:
        model = Route
        fields = ("id", "distance", "source", "destination")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class JourneyListSerializer(JourneySerializer):
    route = serializers.StringRelatedField(read_only=True)
    train = serializers.StringRelatedField(read_only=True)
    crew = serializers.StringRelatedField(read_only=True, many=True)


class JourneyDetailSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        read_only=False,
        slug_field="full_route",
        queryset=Route.objects.all(),
    )
    train = serializers.StringRelatedField(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    class Meta:
        model = Journey
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("cargo_number", "seat_number", "journey", "order")
        extra_kwargs = {
            "order": {"required": False},
        }


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(read_only=False, many=True, allow_empty=False)
    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")
