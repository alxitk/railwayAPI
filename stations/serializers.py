from rest_framework import serializers

from stations.models import Station, Crew, TrainType, Train, Route


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