from django.urls import path
from . views import (
     DeviceListView,
     DeviceDetailView,
     WorkOrderListView,
     DeviceCreateView,
     DeviceUpdateView,
     AddToWorkOrderView,
     RemoveFromWorkOrderView,
     UpdateWorkOrderItemView,
     CheckoutView,
     CheckoutSuccessView,
     )

app_name = 'workorder_management'

urlpatterns = [
     path('devices/', DeviceListView.as_view(),
          name='device_list'),
     path('devices/<int:pk>/', DeviceDetailView.as_view(),
          name='device_detail'),
     path('devices/new/', DeviceCreateView.as_view(),
          name='device_create'),
     path('devices/<int:pk>/update/', DeviceUpdateView.as_view(),
          name='device_update'),
     path('workorders/', WorkOrderListView.as_view(),
          name='workorder_list'),
     path('workorders/<int:pk>/add/', AddToWorkOrderView.as_view(),
          name='add_to_workorder'),
     path('workorders/<int:pk>/remove/', RemoveFromWorkOrderView.as_view(),
          name='remove_from_workorder'),
     path('workorders/<int:pk>/update/', UpdateWorkOrderItemView.as_view(),
          name='update_workorderitem'),
     path('workorders/<int:pk>/checkout/', CheckoutView.as_view(),
          name='checkout'),
     path('workorders/<int:pk>/checkout/success/', CheckoutSuccessView.as_view(),
          name='checkout_success'),
]
