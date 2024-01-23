from django.db import models

# Create your models here.
from sales.models import *
class Production(models.Model):
    # Assuming each production entry is associated with a sales order
    productionUnit= models.CharField(max_length=250)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"Production for Sales Order #{self.sales_order.sale_number}"
    
from django.db import models

# Create your models here.
from sales.models import *
from accounting.models import *


class AllocatedMaterialProductionFlow(models.Model):
    ROW_TYPE_CHOICES = [
    ('Unit 1', 'Unit 1'),
    ('Unit 2', 'Unit 2'),
    ]
    ROW_TYPE_CHOICES_status=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    
    sales_order = models.ForeignKey(Sales, on_delete=models.CASCADE)
    Material = models.ForeignKey(AllocateMaterial,related_name='production_product', on_delete=models.CASCADE)
    cutting= models.BooleanField(default=False)
    cutting_unit= models.CharField(max_length=20, choices=ROW_TYPE_CHOICES,blank=True,null=True)
    cutting_status= models.CharField(max_length=20, choices=ROW_TYPE_CHOICES_status,default='Pending')
    last_update_cutting=models.PositiveIntegerField(default=0)
    
    printing= models.BooleanField(default=False)
    printing_status= models.CharField(max_length=20, choices=ROW_TYPE_CHOICES_status,default='Pending')
    last_update_printing=models.PositiveIntegerField(default=0)
    
    stitching= models.BooleanField(default=True)
    stitching_unit= models.CharField(max_length=20, choices=ROW_TYPE_CHOICES,blank=True,null=True)
    stitching_status= models.CharField(max_length=20, choices=ROW_TYPE_CHOICES_status,default='Pending')
    last_update_stitching=models.PositiveIntegerField(default=0)
    
    # packaginganddispatch = models.BooleanField(default=False)
    # packaginganddispatch_status = models.CharField(max_length=20, choices=ROW_TYPE_CHOICES_status,default='Pending')
    # last_update_packaginganddispatch=models.PositiveIntegerField(default=0)
    
    
    production_date = models.DateField(auto_now_add=True)
    
    

    def save(self, *args, **kwargs):
        # Calculate total price before saving the ProductionRow
        super().save(*args, **kwargs)
class ProducedRow(models.Model):
    ROW_TYPE_CHOICES = [
    ('Raw', 'Raw'),
    ('Package', 'Package'),
    ]
    alloca = models.ForeignKey(AllocatedMaterialProductionFlow, on_delete=models.CASCADE)
    
    sales_order = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='post_product', on_delete=models.CASCADE)
    
    unit = models.DecimalField(max_digits=50, decimal_places=2)
    productionUnit= models.CharField(max_length=250)
    TotalprocessedNow = models.PositiveIntegerField()
    
    TotalQuantity = models.PositiveIntegerField()
    TotalProcessed = models.PositiveIntegerField()
    TotalLeft = models.PositiveIntegerField()
    
    
    production_date = models.DateField(auto_now_add=True)
    production_time = models.TimeField(auto_now_add=True)
    
    

    def save(self, *args, **kwargs):
        sale=ItemRow.objects.get(sale=self.sales_order,product_name=self.product.name)
        # Calculate total price before saving the ProductionRow
        self.unit=Decimal(sale.unit_price)
        self.TotalCost=self.unit*Decimal(self.TotalQuantity)
        super().save(*args, **kwargs)
        
        
        
class ReadyToDispatch(models.Model):
    ROW_TYPE_CHOICES_status = [
    ('Pending', 'Pending'),
    ('Packed', 'Packed'),
    ('Dispatched', 'Dispatched'),
    
    ]
    alloca = models.ForeignKey(AllocatedMaterialProductionFlow, on_delete=models.CASCADE)
    product_stock= models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    sales_order = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='dispatch_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    ledt = models.PositiveIntegerField(default=0)
    disp_left = models.PositiveIntegerField(default=0)
    
    cost_of_single = models.DecimalField(max_digits=50, decimal_places=2)
    total_value = models.DecimalField(max_digits=50, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250,choices=ROW_TYPE_CHOICES_status,default='Pending')
    
    def save(self, *args, **kwargs):
        # Calculate cost_of_all and total_value before saving
        self.total_value = self.cost_of_single * self.quantity
        

     
        
        super().save(*args, **kwargs)
        
        