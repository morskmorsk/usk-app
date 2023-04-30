from django.forms import ModelForm
from .models import WorkOrderItem


class UpdateWorkOrderItemForm(ModelForm):
    class Meta:
        model = WorkOrderItem
        fields = ['repair_price']
