from django.db import models

# Create your models here.
from sales.models import *
class Production(models.Model):
    # Assuming each production entry is associated with a sales order
    sales_order = models.ForeignKey(Sales, on_delete=models.CASCADE)  # Adjust with your actual SalesOrder model

    # Production stages
    cutting = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    stitching = models.BooleanField(default=False)
    packing = models.BooleanField(default=False)
    ready_to_dispatch = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Production for Sales Order #{self.sales_order.sale_number}"