from decimal import Decimal
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
    device_model = models.CharField(max_length=25)
    imei = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    defect = models.CharField(max_length=255)
    estimated_repair_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_of_repair = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    part_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(
        upload_to='static/images/product_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkOrder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Work Order"

    def get_sales_tax(self):
        tax_rate = 0.09  # 9% sales tax rate
        taxable_items = WorkOrderItem.objects.filter
        total_taxable = sum(
            item.price * item.quantity for item in taxable_items)
        return total_taxable * Decimal(tax_rate)


class WorkOrderItem(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    cart = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
