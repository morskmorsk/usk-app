from django.urls import path
from . import views

urlpatterns = [
    # other URLs ...

    path('locations/', views.LocationListView.as_view(),
         name='location_list'),
    path('devices/', views.DeviceListView.as_view(),
         name='device_list'),
    path('workorders/', views.WorkOrderListView.as_view(),
         name='workorder_list'),
]
