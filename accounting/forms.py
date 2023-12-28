from django import forms
from .models import Ledger

from django import forms
from .models import JournalEntry, JournalEntryRow
from inventory.models import Material
class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'  # Include all fields from the model

from .models import PurchaseReturn, PurchaseReturnItem

class PurchaseReturnForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturn
        fields = ['purchase']  # Add other fields as needed
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
    
class PurchaseReturnItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturnItem
        fields = ['material', 'product', 'quantity', 'cost_of_single', 'total_price']  # Add other fields as needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['material'].required = False
        self.fields['product'].required = False










