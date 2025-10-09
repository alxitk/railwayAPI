from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_from"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_to"
    )
    distance = models.FloatField()

    @property
    def full_route(self):
        return f"{self.source.name} -> {self.destination.name}"

    def __str__(self):
        return f"{self.source} → {self.destination}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} <UNK> {self.train_type}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField("Crew", related_name="journeys")

    def __str__(self):
        return f"{self.route} {self.train} {self.departure_time} {self.arrival_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self):
        return f"{self.created_at} {self.user}"


class Ticket(models.Model):
    cargo_number = models.IntegerField()
    seat_number = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("cargo_number", "seat_number", "journey")

    @staticmethod
    def validate_ticket(cargo_number, seat_number, journey, error_to_raise):
        for ticket_attr_value, ticket_attr_name, journey_attr_train_name in [
            (cargo_number, "cargo_number", "cargo"),
            (seat_number, "seat_number", "places_in_cargo"),
        ]:
            count_attrs = getattr(journey.train, journey_attr_train_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise({
                    ticket_attr_name: f"{ticket_attr_name} must be between 1 and {count_attrs}"
                })
    def clean(self):
        Ticket.validate_ticket(
            self.cargo_number,
            self.seat_number,
            self.journey,
            ValidationError,
        )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.cargo_number} {self.seat_number} {self.journey}"