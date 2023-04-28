from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    device_model = models.CharField(max_length=25, blank=True, null=True)
    imei = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    defect = models.CharField(max_length=255, blank=True, null=True)
    estimated_repair_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_of_repair = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    part_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(
        upload_to='static/images/product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_repaired = models.BooleanField(default=False)
    is_repairable = models.BooleanField(default=True)

    def __str__(self):
        return self.owner.username + "'s " + self.device_model

    def get_total_cost(self):
        return self.estimated_repair_price + self.part_cost


class WorkOrder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Work Order"


class WorkOrderItem(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class WorkOrderOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Order"


class WorkOrderOrderItem(models.Model):
    order = models.ForeignKey(WorkOrderOrder, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.device.owner} x {self.device.device_model}"
