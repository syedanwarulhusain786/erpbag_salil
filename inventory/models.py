from django.db import models

# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
def get_image_filename(instance, filename):
    """Generate a unique filename for each uploaded image."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"product_images/{filename}"



class Material(models.Model):
    PIECE = 'Piece'
    LITER = 'Liter'
    METER = 'Meter'
    CMS = 'Centimeter'
    YARD= 'Yard'
    INCH= 'Inch'
    

    UNIT_CHOICES = [
        (PIECE, 'Piece'),
        (LITER, 'Liter'),
        (METER, 'Meter'),
        (CMS, 'Centimeter'),
        (YARD, 'Yard'),
        (INCH, 'Inch'),
        
    ]
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_CHOICES, default=PIECE)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
    
class ProductBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name   

    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    productCost = models.DecimalField(max_digits=10, decimal_places=2)
    productSelling = models.DecimalField(max_digits=10, decimal_places=2)
    # materials = models.ManyToManyField(Material,blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT)
    # new_materials = models.ManyToManyField(Material, through='ProductMaterial', blank=True)
    image0 = models.ImageField(upload_to=get_image_filename)
    image1 = models.ImageField(upload_to=get_image_filename)
    image2 = models.ImageField(upload_to=get_image_filename)
    image3 = models.ImageField(upload_to=get_image_filename)
    image4 = models.ImageField(upload_to=get_image_filename)
    image5 = models.ImageField(upload_to=get_image_filename)
    image6 = models.ImageField(upload_to=get_image_filename)
    image7 = models.ImageField(upload_to=get_image_filename)
    image8 = models.ImageField(upload_to=get_image_filename)
    image9 = models.ImageField(upload_to=get_image_filename)
    
        
    def __str__(self):
        return self.name

    
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    material =models.ForeignKey(Material, on_delete=models.PROTECT)
    
    


    

    
    
    
    
    
    
    
    
    
    
    
    
   
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL ,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Qty = models.PositiveIntegerField()
    costing = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name   

from django.db.models import Sum    
    
class MaterialStock(models.Model):
    purchase = 'purchase'
    sales = 'sales'
    


    UNIT_CHOICES = [
        (purchase, 'Purchase'),
        (sales, 'Sales'),
        
        
    ]
    type = models.CharField(max_length=10, choices=UNIT_CHOICES, default=purchase)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL ,blank=True,null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,blank=True,null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost_of_single = models.DecimalField(max_digits=40, decimal_places=2)
    cost_of_all = models.DecimalField(max_digits=50, decimal_places=2)
    total_value = models.DecimalField(max_digits=50, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Calculate cost_of_all and total_value before saving
        self.cost_of_all = Decimal(self.cost_of_single * self.quantity)
       

        # Calculate total_value as the sum of cost_of_all for the same material
        total_cost_of_all = MaterialStock.objects.filter(material=self.material).aggregate(
            total_cost=Sum('cost_of_all')
        )['total_cost'] or self.cost_of_all
        self.total_value = Decimal(total_cost_of_all)+Decimal(self.cost_of_all)
        super().save(*args, **kwargs)

class ProductStock(models.Model):
    purchase = 'purchase'
    sales = 'return'
    


    UNIT_CHOICES = [
        (purchase, 'Purchase'),
        (sales, 'Return'),
        
        
    ]
    type = models.CharField(max_length=10, choices=UNIT_CHOICES, default=purchase)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,blank=True,null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost_of_single = models.DecimalField(max_digits=50, decimal_places=2)
    cost_of_all = models.DecimalField(max_digits=50, decimal_places=2)
    total_value = models.DecimalField(max_digits=50, decimal_places=2)
    entry_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        # Calculate cost_of_all and total_value before saving
        self.cost_of_all = self.cost_of_single * self.quantity
        

        # Calculate total_value as the sum of cost_of_all for the same product
        total_cost_of_all = ProductStock.objects.filter(product=self.product).aggregate(
            total_cost=Sum('cost_of_all')
        )['total_cost'] or self.cost_of_all
        self.total_value = Decimal(total_cost_of_all)+Decimal(self.cost_of_all)
        super().save(*args, **kwargs)
        
        

class AllocateMaterial(models.Model):
    idx=models.CharField(max_length=50,unique=True)
    rowItem = models.ForeignKey('sales.ItemRow', on_delete=models.CASCADE)
    
    sales = models.ForeignKey('sales.Sales', on_delete=models.CASCADE)
    material = models.ForeignKey(Material,related_name='production_product', on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    quantity_per_piece = models.IntegerField()
    order_quantity = models.IntegerField()
    required = models.IntegerField()
    available = models.IntegerField()
    
    allocated = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="Pending")
    material_stock = GenericRelation(MaterialStock)
    
    def __str__(self):
        return f"{self.material} --> {self.rowItem.product_name}"


    def save(self, *args, **kwargs):
        # Check if allocated is equal to required
        if self.allocated == self.required:
            self.status = "Completed"
        else:
            self.status = "Pending"


        super(AllocateMaterial, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
            # Delete related ProductStock instances
        self.material_stock.all().delete()
        super().delete(*args, **kwargs)
from datetime import datetime, timedelta
class JobList(models.Model):
    supplier = models.ForeignKey('accounting.Supplier', on_delete=models.CASCADE)
    material_send = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_send')
    
    quantity_sent = models.PositiveIntegerField()
    price_send = models.DecimalField(max_digits=50, decimal_places=2)
    sent_date = models.DateField()
    
    material_received = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_received',null=True,blank=True)
    
    price_received = models.DecimalField(max_digits=50, decimal_places=2,null=True,blank=True)
    quantity_received = models.PositiveIntegerField(null=True,blank=True)
    received_date = models.DateField(default=datetime.now() + timedelta(days=7))
    # Add other fields as needed

    def __str__(self):
        return f"{self.quantity_received} units received from {self.supplier} on {self.received_date}, " \
               f"{self.quantity_sent} units sent for {self.material_send} on {self.sent_date}"
