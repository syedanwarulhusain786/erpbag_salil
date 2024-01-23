from django import forms
from .models import Material

from .models import Product

from django import forms
from .models import ProductMaterial, Material

        
from django_select2.forms import ModelSelect2MultipleWidget     
        
from django import forms
from .models import Service, ServiceCategory,ProductBrand,ProductCategory
class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
        
        

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name']
        labels = {'name': 'Category Name'}

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price','Qty','costing']
        labels = {
            'name': 'Service Name',
            'description': 'Description',
            'category': 'Category',
            'price': 'Price',
            'Qty': 'Qty',
            'costing': 'Costing',
        }
        
class ProductBrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['name', 'description']
        labels = {
            'name': 'ProductBrand Name',
            'description': 'Description',
            
        }
        
        
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        labels = {
            'name': 'ProductCategory Name',
            'description': 'Description',
           
        }
        
        
        
        
        
# forms.py

class ProductMaterialForm(forms.ModelForm):
    # materials = forms.ModelMultipleChoiceField(
    #     queryset=Material.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'data-placeholder': 'Select materials'}),
    #     required=False,
    # )

    class Meta:
        model = ProductMaterial
        fields = ['product','quantity_per_piece', 'material']
# forms.py
class ProductMaterialEditForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ['product', 'quantity_per_piece', 'material']

class ProductMaterialForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ['product', 'material', 'quantity_per_piece']

    widgets = {
        'product': ModelSelect2MultipleWidget(
            model=Product,
            search_fields=['name__icontains'],
            attrs={'class': 'form-control select2'}
        ),
        'material': ModelSelect2MultipleWidget(
            model=Material,
            search_fields=['name__icontains'],
            attrs={'class': 'form-control select2'}
        ),
        'quantity_per_piece': forms.NumberInput(attrs={'class': 'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super(ProductMaterialForm, self).__init__(*args, **kwargs)

        # Adding Bootstrap form group to all fields
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control form-group'
            self.fields[field_name].widget.attrs['placeholder'] = field.label

            
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'productCost', 'productSelling', 'category', 'brand', 'image0', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9']

    materials = forms.inlineformset_factory(Product, ProductMaterial, form=ProductMaterialForm, extra=1)
    

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'unit_of_measurement', 'unit_cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    

class MaterialListForm(forms.Form):
    # You can add any filters or search fields you need for listing materials
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))
    
from django import forms
from .models import MaterialStock, ProductStock

class MaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = ['material', 'quantity', 'cost_of_single']

    def __init__(self, *args, **kwargs):
        super(MaterialStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['product', 'quantity', 'cost_of_single']

    def __init__(self, *args, **kwargs):
        super(ProductStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AddMaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(AddMaterialStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AddProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(AddProductStockForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
# forms.py
from django import forms
from .models import JobList

class SendMaterialForm(forms.ModelForm):
    class Meta:
        model = JobList
        fields = ['supplier', 'material_send', 'quantity_sent', 'price_send', 'sent_date']
        widgets = {
            'sent_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'material_send': forms.Select(attrs={'class': 'form-control'}),
            'quantity_sent': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_send': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class ReceiveMaterialForm(forms.ModelForm):
    class Meta:
        model = JobList
        fields = ['supplier', 'material_send', 'quantity_sent', 'price_send', 'material_received', 'sent_date', 'quantity_received', 'price_received', 'received_date']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'material_send': forms.Select(attrs={'class': 'form-control'}),
            'quantity_sent': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_send': forms.NumberInput(attrs={'class': 'form-control'}),
            'material_received': forms.Select(attrs={'class': 'form-control'}),
            'sent_date': forms.DateInput(attrs={'class': 'form-control'}),
            'quantity_received': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_received': forms.NumberInput(attrs={'class': 'form-control'}),
            'received_date': forms.DateInput(attrs={'class': 'form-control' , 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReceiveMaterialForm, self).__init__(*args, **kwargs)
        