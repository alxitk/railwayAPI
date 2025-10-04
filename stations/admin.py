from django.contrib import admin

from stations.models import (Station,
                             Ticket,
                             Train,
                             TrainType,
                             Crew,
                             Route,
                             Journey,
                             Order)

admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Journey)
admin.site.register(Order)
admin.site.register(Ticket)
