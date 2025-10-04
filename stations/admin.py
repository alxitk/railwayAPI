from django.contrib import admin

from stations.models import (Station,
                             Ticket,
                             Train,
                             TrainType,
                             Crew,
                             Route,
                             Journey,
                             Order)

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("name", "cargo_number", "places_in_cargo", "train_type")
    list_filter = ("train_type",)

admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Journey)
admin.site.register(Order)
admin.site.register(Ticket)
