from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location, Device, WorkOrder


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'locations/location_list.html'
    context_object_name = 'locations'


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'devices/device_list.html'
    context_object_name = 'devices'


class WorkOrderListView(LoginRequiredMixin, ListView):
    model = WorkOrder
    template_name = 'workorders/workorder_list.html'
    context_object_name = 'workorders'
