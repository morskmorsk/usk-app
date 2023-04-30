from django.contrib import admin
from .models import (Device,
                     Location,
                     WorkOrder,
                     WorkOrderItem,
                     Defect)

# Register your models here.

admin.site.register(Device)
admin.site.register(Location)
admin.site.register(WorkOrder)
admin.site.register(WorkOrderItem)
admin.site.register(Defect)
