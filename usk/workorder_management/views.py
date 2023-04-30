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
from .models import Device, WorkOrder, OrderItem, Order
from .forms import UpdateWorkOrderItemForm


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'workorder_management/device_list.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'workorder_management/device_detail.html'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['device_model', 'imei', 'description', 'defect',
              'estimated_repair_price']
    template_name = 'workorder_management/device_create.html'
    success_url = reverse_lazy('workorder_management:workorder_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['owner', 'device_model', 'imei', 'description', 'defect',
              'estimated_repair_price', 'cost_of_repair', 'part_cost',
              'location', 'image', 'is_repaired', 'is_repairable']
    template_name = 'workorder_management/device_update.html'
    success_url = reverse_lazy('workorder_management:workorder_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WorkOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'workorder_management/workorder_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # workorder = get_object_or_404(WorkOrder, user=self.request.user)
        workorder = get_object_or_404(WorkOrder, user=self.request.user)
        items = OrderItem.objects.filter(workorder_id=workorder)
        context.update({'items': items})
        return context


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    model = WorkOrder
    template_name = 'workorder_management/workorder_detail.html'


class AddToWorkOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        repair_price = request.POST.get('repair_price', 0)
        device = get_object_or_404(Device, pk=self.kwargs['pk'])
        workorder, _ = WorkOrder.objects.get_or_create(user=request.user)
        item, created = OrderItem.objects.get_or_create(
            workorder=workorder, device=device, repair_price=repair_price)
        item.save()
        return redirect('workorder_management:workorder_list')


class RemoveFromWorkOrderView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    success_url = reverse_lazy('workorder_management:workorder_list')

    def get_object(self, queryset=None):
        workorder = get_object_or_404(WorkOrder, user=self.request.user)
        workorderitem = OrderItem.objects.filter(
            workorder=workorder, pk=self.kwargs['pk']).first()

        if not workorderitem:
            raise Http404("Work order item not found")

        return workorderitem

    def render_to_response(self, context, **response_kwargs):
        if not context.get('object'):
            return render(self.request, 'workorder_management/device_not_found.html',
                          status=404)

        return super().render_to_response(context, **response_kwargs)


class UpdateWorkOrderItemView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = UpdateWorkOrderItemForm
    template_name = 'workorder_management/update_workorder_item.html'
    success_url = reverse_lazy('workorder_management:workorder_list')

    def get_queryset(self):
        return OrderItem.objects.filter(workorder__user=self.request.user)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'workorder_management/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the checkout process here
        return context

    def post(self, request, *args, **kwargs):
        workorder = get_object_or_404(Order, user=request.user)
        workorder_items = OrderItem.objects.filter(workorder=workorder)

        # Create Order
        Order = Order(user=request.user)
        Order.save()

        # Create OrderItems
        for item in workorder_items:
            work_order_item = OrderItem(
                Order=Order,
                device=item.device,
                repair_price=item.repair_price,
            )
            work_order_item.save()

        # Clear the cart
        workorder_items.delete()

        # Redirect to a success page or any other appropriate page
        return redirect('workorder_management:checkout_success')


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'workorder_management/checkout_success.html'

# logout the user when the checkout is successful
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return super().get(request, *args, **kwargs)
