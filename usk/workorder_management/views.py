from django.shortcuts import (render,
                              redirect,
                              get_object_or_404,
                              Http404)
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  View,
                                  TemplateView,
                                  )

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Device, WorkOrder, WorkOrderItem, WorkOrderOrder
from .forms import UpdateWorkOrderItemForm


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'device_list.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'devices/device_detail.html'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['owner', 'device_model', 'imei', 'description', 'defect',
              'estimated_repair_price', 'cost_of_repair', 'part_cost',
              'location', 'image', 'is_repaired', 'is_repairable']
    template_name = 'device_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['owner', 'device_model', 'imei', 'description', 'defect',
              'estimated_repair_price', 'cost_of_repair', 'part_cost',
              'location', 'image', 'is_repaired', 'is_repairable']
    template_name = 'device_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkOrderListView(LoginRequiredMixin, ListView):
    model = WorkOrder
    template_name = 'workorder_list.html'
    context_object_name = 'workorders'

    def get_queryset(self):
        return WorkOrder.objects.filter(user=self.request.user)


class AddToWorkOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        price = request.POST.get('price', 0)
        device = get_object_or_404(Device, pk=self.kwargs['pk'])
        workorder, _ = WorkOrder.objects.get_or_create(user=request.user)
        item, created = WorkOrderItem.objects.get_or_create(
            workorder=workorder, device=device, price=price)

        if not created:
            item.quantity += 1
            item.save()

        return redirect('workorder_management:workorder_list')


class RemoveFromWorkOrderView(LoginRequiredMixin, DeleteView):
    model = WorkOrderItem
    success_url = reverse_lazy('workorder_management:workorder_list')

    def get_object(self, queryset=None):
        workorder = get_object_or_404(WorkOrder, user=self.request.user)
        workorderitem = WorkOrderItem.objects.filter(
            workorder=workorder, pk=self.kwargs['pk']).first()

        if not workorderitem:
            raise Http404("Work order item not found")

        return workorderitem

    def render_to_response(self, context, **response_kwargs):
        if not context.get('object'):
            return render(self.request, 'device_not_found.html',
                          status=404)

        return super().render_to_response(context, **response_kwargs)


class UpdateWorkOrderItemView(LoginRequiredMixin, UpdateView):
    model = WorkOrderItem
    form_class = UpdateWorkOrderItemForm
    template_name = 'update_workorder_item.html'
    success_url = reverse_lazy('workorder_management:workorder_list')

    def get_queryset(self):
        return WorkOrderItem.objects.filter(cart__user=self.request.user)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the checkout process here
        return context

    def post(self, request, *args, **kwargs):
        workorder = get_object_or_404(WorkOrderOrder, user=request.user)
        workorder_items = WorkOrderItem.objects.filter(workorder=workorder)

        # Create Order
        workorderorder = WorkOrderOrder(user=request.user)
        workorderorder.save()

        # Create OrderItems
        for item in workorder_items:
            work_order_item = WorkOrderItem(
                workorderorder=workorderorder,
                device=item.device,
                repair_price=item.repair_price,
            )
            work_order_item.save()

        # Clear the cart
        workorder_items.delete()

        # Redirect to a success page or any other appropriate page
        return redirect('workorder_management:checkout_success')


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout_success.html'

# logout the user when the checkout is successful
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return super().get(request, *args, **kwargs)
