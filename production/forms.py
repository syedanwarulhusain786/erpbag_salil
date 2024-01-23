# forms.py
from sales.models import *
from accounting.models import *
from django import forms
from .models import ProducedRow
from .models import AllocatedMaterialProductionFlow

class AllocatedMaterialProductionFlowForm(forms.ModelForm):
    class Meta:
        model = AllocatedMaterialProductionFlow
        exclude = ['sales_order', 'production_date', 'cutting_status', 'last_update_cutting',
                   'printing_status', 'last_update_printing', 'stitching_status', 'last_update_stitching',
                   'packaginganddispatch_status', 'last_update_packaginganddispatch']  # Exclude fields you don't want in the form

    def __init__(self, *args, **kwargs):
        super(AllocatedMaterialProductionFlowForm, self).__init__(*args, **kwargs)
        boolean_choices = (
            (False, 'No'),
            (True, 'Yes'),
        )

        # Update the widgets for boolean fields to use a dropdown (select) input
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                self.fields[field_name] = forms.ChoiceField(
                    choices=boolean_choices,
                    widget=forms.Select(attrs={'class': 'form-control'}),
                )
            if field_name == 'Material' or field_name == 'cutting_unit' or field_name == 'stitching_unit':
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            # Corrected indentation of the comment

# class ProductionRowForm(forms.ModelForm):
#     class Meta:
#         model = ProductionRow
#         fields = ['product', 'packageQuantity', 'quantityPerPackage','TotalQuantity','TotalCost']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = Product.objects.exclude(category__name='Package')
#         # Filter products by category 'packaging'
#         # packaging_products = Product.objects.filter(category=ProductCategory.objects.get(name='Package'))
#         # Update the queryset for the 'product' field
#         # self.fields['package'].queryset = packaging_products

#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})


class PostProductionRowForm(forms.ModelForm):
    class Meta:
        model = ProducedRow
        fields = ['product', 'TotalQuantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['product'].queryset = Product.objects.exclude(category__name='Package')
        # Filter products by category 'packaging'
        # packaging_products = Product.objects.filter(category=ProductCategory.objects.get(name='Package'))
        # Update the queryset for the 'product' field
        # self.fields['package'].queryset = packaging_products

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})